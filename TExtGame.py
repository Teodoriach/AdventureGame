import random as rd
import loot_list as loot
import weapons as wp


class Player:
    def __init__(self, name="Bob"):
        self.level = 1
        self.exp = 0
        self.maxxp = 20
        self.points = 0
        self.name = name
        self.loc = [0, 0]
        self.eq = {"steel rod": 1}
        self.active_eq = {}
        self.stats = {  # INT only!!!
            "hp": 1,  # health points
            "max hp": 1,
            "armour": 0,  # decreases damage
            "agility": 1,  # chance to evade, 1 = 1% and so on
            "strength": 1,  # damage and skill checks
            "magic": 0,  # magic
            "dexterity": 1  # in fight determines order
        }
        self.prevloc = self.loc

    def update_loc(self, change, direction):  # change = +1 or -1, direction = 0 for NS, 1 for WE
        self.prevloc = self.loc
        self.loc[direction] += change
        return self.loc

    def get_loc(self):
        return self.loc

    def get_prev_loc(self):  # get previous location
        return self.prevloc

    def set_loc_to_prev(self):
        self.loc = self.prevloc
        return self.loc

    def set_eq(self, new_eq, count):
        if new_eq in self.eq:
            self.eq[new_eq] += count
        else:
            self.eq[new_eq] = count

    def get_eq(self):
        return self.eq

    def get_active_eq(self):
        return self.active_eq

    def set_active_eq(self, eq):
        if eq in self.eq and eq not in self.active_eq:
            self.set_eq(eq, -1)
            self.active_eq[eq] = 1

    def change_stats(self, stat, change):
        self.stats[stat] += change

    def get_stats(self):
        return self.stats

    def get_stat(self, stat):
        return self.stats[stat]

    def check_experience(self):
        if self.exp >= self.maxxp:
            self.exp = 0
            self.maxxp = self.maxxp*2
            self.points = 1
            return True
        else:
            return False


class Room:
    def __init__(self, direction: str, location):
        self.direction = direction
        self.dirs = self.directions_gen()
        self.location = location
        self.multiplier = round((abs(location[0]) + abs(location[1]))/2)
        self.loot = False
        self.chest = self.chest_gen()
        self.enemy = None
        if rd.randint(0, 10) > 9:
            self.enemyExist = True
            self.enemy = Enemy(self.location, self.multiplier)
        else:
            self.enemyExist = None
        self.description = self.description_gen()

    def directions_gen(self):
        dirs = ["north", "west", "east", "south"]
        dirs.remove(self.direction)
        del dirs[rd.randint(0, 3):]
        dirs.append(self.direction)
        return dirs

    def chest_gen(self):
        if rd.randint(0, 1) == 1:
            chest = {
                "exists": True,
                "content": loot_table()
             }
            self.loot = True
            return chest
        else:
            chest = {
                "exists": False
            }
            return chest

    def description_gen(self):
        description = "\nThere is "
        if self.loot:
            description += "chest in room. "
        else:
            description += "no chest in room. "
        if self.enemyExist:
            description += "There is an enemy in room. "
        else:
            description += "There is no enemy in here. "
        description += "You can only go " + "{}, "*(len(self.dirs)-1) + "and {}."
        description = description.format(*self.dirs[:-1], self.dirs[-1])
        return description

    def check_direction(self, direction):
        if direction in self.dirs:
            return True
        else:
            return False

    def get_directions(self):
        return self.dirs

    def check_loot(self):
        return self.loot

    def check_enemy(self):
        return self.enemyExist

    def get_enemy(self):
        return self.enemy

    def set_enemy_exist(self, val):
        self.enemyExist = val
        return self.enemyExist


class StartRoom(Room):
    def __init__(self):
        self.dirs = ["north", "west", "east", "south"]
        self.loot = False
        self.enemy = False
        self.enemyExist = False
        self.description = self.description_gen()


class Enemy:
    def __init__(self, loc, mult):
        self.loc = loc
        self.givexp = 10
        self.multiplier = mult
        self.stats = {  # INT only!!!
            "hp": 1 * mult,  # health points
            "armour": 0 * mult,  # decreases damage
            "agility": 1 * mult,  # chance to evade, 1 = 1% and so on
            "strength": 1 * mult,  # damage and skill checks
            "magic": 0 * mult,  # magic
            "dexterity": 0 * mult  # in fight determinates order
        }
        self.corrects_stats()
        self.loot = loot_table()

    def corrects_stats(self):
        if self.multiplier >= 2:
            self.stats["armour"] = 1 * self.multiplier
            self.stats["magic"] = 1 * self.multiplier
            self.stats["dexterity"] = 1 * self.multiplier
            self.givexp = self.givexp*2
            return self.stats

    def get_stats(self):
        return self.stats

    def get_stat(self, stat):
        return self.stats[stat]

    def change_stats(self, stat, change):
        self.stats[stat] += change


def game():
    options = {"move": "go",
               "open chest": "open",
               "stats": "stats",
               "equipment": "eq",
               "test": "test",
               "points": "level"
               }  # Any interaction
    combat_options = ["attack", "block", "run"]
    directions = {"n": "north",
                  "w": "west",
                  "e": "east",
                  "s": "south",
                  "go north": "n",
                  "go west": "w",
                  "go east": "e",
                  "go south": "s",
                  "go back": "back",
                  }  # any possible direction
    # loc  [0] is +north -south, [1] is -west +east
    player = Player()
    rooms = {}  # LIST OF Room() OBJECTS!!!
    loc = (player.loc[0], player.loc[1])
    rooms[loc] = StartRoom()
    room = get_room(loc, rooms)
    while True:
        if not room.check_enemy():
            print(room.description)
            print("Your position: {}".format(player.loc))
            option = input("What do you want to do? ").lower().strip()
            print("")
            if check_dict_bool(option, options):
                if option == "move" or option == "go":
                    option = input("Where do you want to go? ").lower().strip()
                    if check_dict_return_value(option, directions):
                        direction = check_dict_return_value(option, directions)
                        room = get_room(loc, rooms)
                        if direction in room.dirs:
                            print("You are going {}".format(direction))
                            if direction == "north":
                                loc = tuple(player.update_loc(1, 0))
                                room = check_room(loc, rooms, "south")
                            elif direction == "west":
                                loc = tuple(player.update_loc(-1, 1))
                                room = check_room(loc, rooms, "east")
                            elif direction == "east":
                                loc = tuple(player.update_loc(1, 1))
                                room = check_room(loc, rooms, "west")
                            elif direction == "south":
                                loc = tuple(player.update_loc(-1, 0))
                                room = check_room(loc, rooms, "north")

                        else:
                            print("You can't go in there")
                elif option == "eq" or option == "equipment":
                    eq_options = ["equip", "stats", "exit"]
                    i = 1
                    for eq in player.get_eq():
                        print("{}. {}".format(i, eq))
                        i += 1
                    eq_input = input("What do you want to do? ").strip().lower()
                    if eq_input in eq_options:
                        if eq_input == "equip":
                            i = 1
                            temp_list = []
                            for eq in player.get_eq():
                                temp_list = [eq]
                                print("{}. {}".format(i, eq))
                                i += 1
                            eq_input = input("Please pick the eq to equip ")
                            eq = temp_list[int(eq_input)-1]
                            player.set_active_eq(eq)
                            print("You equipped {}".format(eq))
                            check = wp.return_stat(eq)
                            for key in check:
                                player.change_stats(key, check[key])
                        elif eq_input == "stats":
                            i = 1
                            temp_list = []
                            for eq in player.get_eq():
                                temp_list = [eq]
                                print("{}. {}".format(i, eq))
                                i += 1
                            eq_input = input("Pick a weapon to show its stats: ")
                            eq = temp_list[int(eq_input)-1]
                            wp_stats = wp.return_stat(eq)
                            for key in wp.return_stat(eq):
                                print("{} : {}".format(key, wp_stats[key]))
                        elif eq_input == "exit":
                            print("You didn't pick anything")
                    else:
                        print("I don't understand")
                elif option == "stats":
                    pc_stats = player.stats
                    for key in pc_stats:
                        print("{} : {}".format(key, pc_stats[key]))
                elif option == "points" or option == "level":
                    print("You have {} points left".format(player.points))
                    if player.points > 0:
                        answer = input("Do you want to distribute them? y/n").lower()
                        if answer == "y":
                            print(player.get_stats())
                            stat = input("Which stat do you want to improve? (Type its name)")
                            if stat in player.stats:
                                player.change_stats(stat, 1)
                                player.points -= 1
                                print("You've increased your {} by 1".format(stat))
                            else:
                                print("There is no stat with the name like that")
                        else:
                            print("Okay then")
                    else:
                        print("You have 0 points, you can't do anything.")

                elif option == "open" or option == "open chest":
                    if room.loot:
                        loot_options = ["pick", "all", "exit"]
                        print("You've opened the chest. Here is the content")
                        i = 1
                        for chest_loot in check_dict_return_value("content", room.chest):
                            print("{}. {}".format(i, chest_loot))
                            i += 1
                        chest_input = input("Please pick the item you want to take, type 'all' to pick all or type exit"
                                            "to exit")
                        if chest_input in loot_options:
                            if chest_input == "pick":
                                i = 1
                                temp_list = []
                                for chest_loot in check_dict_return_value("content", room.chest):
                                    temp_list = [chest_loot]
                                    print("{}. {}".format(i, chest_loot))
                                    i += 1
                                loot_input = input("Please pick the loot to collect ")
                                chest_loot = temp_list[int(loot_input)-1]
                                player.set_eq(chest_loot, 1)
                            elif chest_input == "all":
                                print("You've picked all the items. ")
                                for chest_loot in check_dict_return_value("content", room.chest):
                                    player.set_eq(chest_loot, 1)
                            elif chest_input == "exit":
                                print("You didn't pick anything")
                        else:
                            print("Wrong command")
                            continue
            else:
                print("I don't understand")
        else:
            print("There is an enemy in this room! Prepare for combat! You can't leave the room until you kill him!")
            enemy = room.get_enemy()
            enemy_hp = enemy.get_stat("hp")
            player_hp = player.get_stat("hp")
            first_round = True
            order = 1
            while room.check_enemy():
                if first_round:
                    if player.get_stat("dexterity") > enemy.get_stat("dexterity"):  # who start first
                        order = 1
                        first_round = False
                    else:
                        order = 0
                        first_round = False
                if order == 1:
                    string = "Your options: " + "{}, "*(len(combat_options)-1) + "and {}."
                    print(string.format(combat_options[:-1], combat_options[-1]))
                    option = input("What are you doing?").lower().strip()
                    if option in combat_options:
                        if option == "attack":
                            print("You have chosen to attack")
                            damage = damage_calc(player.get_stat("strength"), enemy.get_stat("armour"))
                            print("You have done {} points of damage!".format(damage))
                            enemy_hp -= damage
                            if enemy_hp <= 0:
                                print("You have defeated your enemy!")
                                room.set_enemy_exist(False)
                                room.description_gen()  # update description
                                player.exp += enemy.givexp
                                if player.check_experience():
                                    print("Congratulations, you leveled up. Type 'points' to distribute them.")

                            else:
                                print("Your enemy prevailed your attack, he is attacking!")
                                order = 0
                        if option == "block":
                            print("You are trying to block enemy's attack. Your armour increases by 1")
                            player.change_stats("armour", 1)
                            order = 0
                        if option == "run":
                            print("You try to run.")
                            if player.get_stat("agility") > enemy.get_stat("agility"):
                                print("You've successfully run away")
                                player.set_loc_to_prev()
                            else:
                                print("You can't run away")
                                order = 0

                else:
                    damage = damage_calc(enemy.get_stat("strength"), player.get_stat("armour"))
                    print("Your enemy have done {} points of damage!".format(damage))
                    player_hp -= damage
                    if player_hp >= 0:
                        print("You survived, you have {} points of health".format(player_hp))
                        order = 1
                        continue
                    else:
                        print("You died.")
                        exit()


def clear_output(table):
    pass


def damage_calc(dmg, armr):  # dmg = strength of attacking party, armr = armour of attacked party
    damage = dmg - armr
    return damage


def loot_table():  # typ = 0 enemy, typ = 1 chest
    chosen_item = rd.choices(loot.loot1, weights=loot.weights1)
    return chosen_item


def check_dict_bool(string, dct: dict):  # check if given key/value exists
    if string in dct:
        return True
    elif string in dct.values():
        return True
    else:
        return False


def check_dict_return_keyword(string, dct: dict):  # if string is already a key, return key
    if string in dct:
        return string
    else:
        get_key_from_val(string, dct)


def check_dict_return_value(string, dct: dict):  # return value of given key
    if string in dct:
        return dct[string]
    elif string in dct.values():
        return string
    else:
        return False


def get_key_from_val(val, dct):  # return key with given value
    for key, value in dct.items():
        if val == value:
            return key
        else:
            return False


def get_first_key(dct):  # FOR ITEMS, order: STAT, CLASS, RARITY
    for key, val in dct.items():
        return key


def check_room(loc, dit, direction):  # check if room exists
    if loc in dit:
        return get_room(loc, dit)
    else:
        dit[loc] = Room(direction, loc)
        return get_room(loc, dit)


def get_room(loc, dit):  # return room from given location
    return dit[loc]


game()
