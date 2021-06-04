#from src.skeletons.weapon_types import weaponTypes
#weapon_types = weaponTypes().data
import json

class Object():
    def __init__(self):
        self.name = ""
        self.desc = ""
        self.icon = None
        self.sprite_sheet = None
        self.event_to_sprites = {}
        self.price_if_sold = 0
        self.price = 0
        self.price_modifiers = []
        self.scope = ""
        self.inventories
        self.shop_pages = []
        self.buyable_quantity = 1
        
    def selfToJSON(self, path, basic_attrs=None):
        if basic_attrs == None:
            basic_attrs = self.attrs
        basic_attrs_dict = {}
        for b in basic_attrs:
            basic_attrs_dict[b] = getattr(self,b)
            
        with open(path, "w") as wf:
            json.dump(basic_attrs_dict, wf)
    
    def selfFromJSON(self, path, basic_attrs=None):
        if basic_attrs == None:
            basic_attrs = self.attrs
        with open(path, "r") as rf:
            tmp_data = json.load(rf)

        for a in basic_attrs:
            setattr(self, a, tmp_data[a])

class Weapon(Object):
    def __init__(self):
        super().__init__()
        self.might = 0
        self.hit = 0
        self.crit = 0
        self.range = 1
        self.weight = 1
        self.special_abilities = []
        self.conditional_special_abilities = []
        self.csa_conditions = {}
        self.can_forge = True
        self.can_repair = True
        self.repair_cost_per = 0
        self.minimum_experience_level  = "E"
        self.forge_into = {}
        self.forge_items = []
        self.forge_items_amounts = {}
        self.rarity = 0
        self.unique_to_unit = False
        self.type = None
        self.scope = "combat"
        self.inventories = ["unit_weapon_inventory", "convoy_weapon_inventory"]
        self.full_durability = 0
        self.current_durability = 0
        self.broken = False
        self.price_modifiers = ["durability"]
        
        self.attrs = ["name", "desc", "icon", "sprite_sheet", "event_to_sprites", "price_if_sold", "price",
                      "price_modifiers", "scope", "inventories", "might", "hit", "crit", "range", "special_abilities",
                      "conditional_special_abilities", "csa_conditions", "can_forge", "can_repair", "repair_cost_per",
                      "minimum_experience_level", "forge_into", "forge_items", "forge_items_amounts","rarity",
                      "unique_to_unit","type","scope","inventories","full_durability","current_durability",
                      "broken", "price_modifiers", "shop_pages", "weight"]
    
    def removeDurability(self, a):
        self.current_durability -= a
        if self.current_durability <= 0:
            self.broken = True
    
    def repair(self):
        cost = self.repair_cost_per * (self.full_durability - self.current_durability)
        self.current_durability = self.full_durability
        return cost