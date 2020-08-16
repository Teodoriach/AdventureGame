loot1 = ["iron sword", "wooden shield", "steel rod", "potion of health"]

weapon_list = {
    "iron sword": {
        "strength": 1
    },
    "wooden shield": {
        "armour": 1
    },
    "steel rod": {
        "strength": 2,
        "agility": -1,
    },
    "potion of health": {
        "max hp": 1
    }
}


def return_stat(weapon):
    if weapon in weapon_list:
        this = weapon_list[weapon]
        return this