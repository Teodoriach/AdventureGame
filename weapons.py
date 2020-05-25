loot1 = ["iron sword", "wooden shield", "steel rod", "potion of health"]

list = {
    "iron sword": {
        "strength": 1
    },
    "wooden shield": {
        "armour": 1
    },
    "steel rod": {
        "strength": 2,
    },
    "potion of health": {
        "max hp": 1
    }
}

def return_stat(weapon):
    if weapon in list:
        this = list[weapon]
        return this