import json
class weaponTypes():
    def __init__(self):
        with open("src/skeletons/universal_weapon_types.json", "r") as weapons_file:
            weapon_types = json.load(weapons_file)
        self.data = weapon_types