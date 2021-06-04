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
        self.scopes = []
        self.inventories = []
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
    
    def removeFromMemory(self):
        pass
        #global_inventory.remove(self)

class usableItem(Object):
    def __init__(self):
        super().__init__()
        self.path = None
        self.uses = 1
        self.used_uses = 0
        self.used = False
        self.inventories = ["unit_object_inventory", "convoy_usable_inventory"]
        self.scopes = ["combat", "inventory menu"]
        self.attrs = ["name", "desc", "icon", "sprite_sheet", "event_to_sprites", "price_if_sold", "price",
                      "price_modifiers", "scopes", "inventories", "uses", "used_uses", "used"]

class Key(usableItem):
    def __init__(self):
        super().__init__()
        self.to_door = False
        self.to_chest = False
        self.scopes = ["combat", "inventory menu"]
        self.attrs = ["name", "desc", "icon", "sprite_sheet", "event_to_sprites", "price_if_sold", "price",
                      "price_modifiers", "scopes", "inventories", "to_chest", "to_door", "used"]

class healItem(usableItem):
    def __init__(self):
        super().__init__()
        self.heal_amount = 0
        self.status_removes = []
        self.scopes = ["combat", "inventory menu"]
        self.attrs = ["name", "desc", "icon", "sprite_sheet", "event_to_sprites", "price_if_sold", "price",
                      "price_modifiers", "scopes", "inventories", "status_removes", "used", "used_uses", "uses"]

class statIncreaseItem(usableItem):
    def __init__(self):
        super().__init__()
        self.stat = None
        self.stat_increase = 0
        self.scopes = ["combat", "inventory menu"]
        self.attrs = ["name", "desc", "icon", "sprite_sheet", "event_to_sprites", "price_if_sold", "price",
                      "price_modifiers", "scopes", "inventories", "stat", "stat_increase"]

class expIncreaseItem(usableItem):
    def __init__(self):
        super().__init__()
        self.exp_type = None
        self.exp_increase = 0
        self.scopes = ["combat", "inventory menu"]
        self.attrs = ["name", "desc", "icon", "sprite_sheet", "event_to_sprites", "price_if_sold", "price",
                      "price_modifiers", "scopes", "inventories", "exp_type", "exp_increase"]

class classChangeItem(usableItem):
    def __init__(self):
        super().__init__()
        self.type = None
        self.scopes = ["inventory menu", "reclass"]
        self.attrs = ["name", "desc", "icon", "sprite_sheet", "event_to_sprites", "price_if_sold", "price",
                      "price_modifiers", "scopes", "inventories", "type"]

class levelEffectItem(usableItem):
    def __init__(self):
        super().__init__()
        self.level_effect = ""
        self.duration = 0
        self.tile = None
        self.radius = 1
        self.scopes = ["combat", "inventory menu"]
        self.attrs = ["name", "desc", "icon", "sprite_sheet", "event_to_sprites", "price_if_sold", "price",
                      "price_modifiers", "scopes", "inventories", "duration", "tile", "radius"]

class equippableItem(Object):
    def __init__(self):
        super().__init__()
        self.path = None
        self.special_abilities = []
        self.conditional_special_abilities = []
        self.csa_conditions = {}
        self.can_forge = True
        self.can_repair = True
        self.repair_cost_per = 0
        self.forge_into = {}
        self.forge_items = []
        self.forge_items_amounts = {}
        self.rarity = 0
        self.type = None
        self.scopes = ["combat", "inventory menu"]
        self.inventories = ["unit_weapon_inventory", "convoy_weapon_inventory"]
        self.full_durability = 0
        self.current_durability = 0
        self.broken = False
        self.price_modifiers = ["durability"]
        
        self.attrs = ["name", "desc", "icon", "sprite_sheet", "event_to_sprites", "price_if_sold", "price",
                      "price_modifiers", "scopes", "inventories", "special_abilities",
                      "conditional_special_abilities", "csa_conditions", "can_forge", "can_repair", "repair_cost_per",
                      "minimum_experience_level", "forge_into", "forge_items", "forge_items_amounts","rarity",
                      "unique_to_unit","type","scope","inventories","full_durability","current_durability",
                      "broken", "price_modifiers", "shop_pages"]
    
    def removeDurability(self, a):
        self.current_durability -= a
        if self.current_durability <= 0:
            self.broken = True
        if self.path != None:
            self.selfToJSON(self.path)
    
    def repair(self):
        cost = self.repair_cost_per * (self.full_durability - self.current_durability)
        self.current_durability = self.full_durability
        return cost
        if self.path != None:
            self.selfToJSON(self.path)
    
class Weapon(equippableItem):
    def __init__(self):
        super().__init__()
        self.might = 0
        self.hit = 0
        self.crit = 0
        self.range = 1
        self.weight = 1
        self.minimum_experience_level  = "E"
        self.unique_to_unit = False
        
        self.attrs = ["name", "desc", "icon", "sprite_sheet", "event_to_sprites", "price_if_sold", "price",
              "price_modifiers", "scopes", "inventories", "might", "hit", "crit", "range", "special_abilities",
              "conditional_special_abilities", "csa_conditions", "can_forge", "can_repair", "repair_cost_per",
              "minimum_experience_level", "forge_into", "forge_items", "forge_items_amounts","rarity",
              "unique_to_unit","type","scope","inventories","full_durability","current_durability",
              "broken", "price_modifiers", "shop_pages", "weight"]
        
class Shield(equippableItem):
    def __init__(self):
        super().__init__()
        self.defense = 1
        self.resistance = 0
        self.weight = 1
        
        self.attrs = ["name", "desc", "icon", "sprite_sheet", "event_to_sprites", "price_if_sold", "price",
                      "price_modifiers", "scopes", "inventories", "special_abilities",
                      "conditional_special_abilities", "csa_conditions", "can_forge", "can_repair", "repair_cost_per",
                      "minimum_experience_level", "forge_into", "forge_items", "forge_items_amounts","rarity",
                      "unique_to_unit","type","scope","inventories","full_durability","current_durability",
                      "broken", "price_modifiers", "shop_pages", "weight", "defense", "resistance"]
    
