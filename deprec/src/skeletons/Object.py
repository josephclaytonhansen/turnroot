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
        
    def selfToJSON(self, path=None, basic_attrs=None):
        if basic_attrs == None:
            basic_attrs = self.attrs
        if path == None:
            path = self.path
        basic_attrs_dict = {}
        for b in basic_attrs:
            basic_attrs_dict[b] = getattr(self,b)
            
        with open(path, "w") as wf:
            json.dump(basic_attrs_dict, wf)
    
    def selfFromJSON(self, path=None, basic_attrs=None):
        if basic_attrs == None:
            basic_attrs = self.attrs
        if path == None:
            path = self.path
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

class summoningItem(usableItem):
    def __init__(self):
        super().__init__()
        self.summons = []
        self.summon_prob = {}
        self.scopes = ["inventory menu"]
        self.attrs = ["name", "desc", "icon", "sprite_sheet", "event_to_sprites", "price_if_sold", "price",
                      "price_modifiers", "scopes", "inventories", "summons", "summon_prob"]

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
        self.repair_items_amounts = 0
        self.repair_items = {}
        self.sell_cost_per = 0
        self.forge_into = {}
        self.forge_items = {}
        self.forge_into_items = {}
        self.forge_items_amounts = {}
        self.forge_costs = {}
        self.rarity = 0
        self.type = None
        self.scopes = ["combat", "inventory menu"]
        self.inventories = ["unit_weapon_inventory", "convoy_weapon_inventory"]
        self.full_durability = 0
        self.current_durability = 0
        self.broken = False
        self.price_modifiers = ["durability"]
        
        self.attrs = ["name", "desc", "icon", "sprite_sheet", "event_to_sprites", "price_if_sold", "price",
                      "price_modifiers", "scopes", "inventories", "special_abilities", "forge_into_items", "repair_items",
                      "conditional_special_abilities", "csa_conditions", "can_forge", "can_repair", "repair_cost_per",
                      "minimum_experience_level", "forge_into", "forge_items", "forge_items_amounts","rarity",
                      "unique_to_unit","type","scopes","inventories","full_durability","current_durability",
                      "broken", "price_modifiers", "shop_pages", "sell_cost_per", "repair_items_amounts", "forge_costs"]
    
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

class Healing(equippableItem):
    def __init__(self):
        super().__init__()
        self.buyable_quantity = 1
        self.heals_from_stats = True
        self.healing_amount_bonus = 0
        self.range = [1,1]
        self.range_change = False
        self.rc_amount = 0
        self.minimum_experience_level  = "E"
        self.weight = 1
        self.attrs = ["name", "desc", "icon", "sprite_sheet", "event_to_sprites", "price_if_sold", "price","rc_amount",
                      "price_modifiers", "scopes", "inventories", "special_abilities", "forge_into_items", "repair_items",
                      "conditional_special_abilities", "csa_conditions", "can_forge", "can_repair", "repair_cost_per",
                      "minimum_experience_level", "forge_into", "forge_items", "forge_items_amounts","rarity","type",
                      "scopes","inventories","full_durability","current_durability","range_change",
                      "broken", "price_modifiers", "shop_pages", "sell_cost_per", "repair_items_amounts", "forge_costs",
                      "heals_from_stats","healing_amount_bonus","range","minimum_experience_level","weight"]
        
class Weapon(equippableItem):
    def __init__(self):
        super().__init__()
        self.might = 0
        self.buyable_quantity = 1
        self.hit = 0
        self.crit = 0
        self.avo = 0
        self.asm = 0
        self.damage_type = "Physical"
        self.range = [1,1]
        self.weight = 1
        self.minimum_experience_level  = "E"
        self.unique_to_unit = False
        
        self.attrs = ["name", "desc", "icon", "sprite_sheet", "event_to_sprites", "price_if_sold", "price",
              "price_modifiers", "scopes", "inventories", "might", "hit", "crit", "range", "special_abilities",
              "conditional_special_abilities", "csa_conditions", "can_forge", "can_repair", "repair_cost_per",
              "minimum_experience_level", "forge_into", "forge_items", "forge_items_amounts","rarity",
              "unique_to_unit","type","scopes","inventories","full_durability","current_durability",
              "broken", "price_modifiers", "shop_pages", "weight", "buyable_quantity", "avo", "asm", "repair_items",
                      "sell_cost_per", "repair_items_amounts", "damage_type","forge_costs", "forge_into_items"]
        
class Shield(equippableItem):
    def __init__(self):
        super().__init__()
        self.defense = 1
        self.resistance = 0
        self.weight = 1
        
        self.attrs = ["name", "desc", "icon", "sprite_sheet", "event_to_sprites", "price_if_sold", "price",
                      "price_modifiers", "scopes", "inventories", "special_abilities", "forge_into_items",
                      "conditional_special_abilities", "csa_conditions", "can_forge", "can_repair", "repair_cost_per",
                      "minimum_experience_level", "forge_into", "forge_items", "forge_items_amounts","rarity",
                      "unique_to_unit","type","scopes","inventories","full_durability","current_durability",
                      "broken", "price_modifiers", "shop_pages", "weight", "defense", "resistance", "sell_cost_per", "forge_costs"]
    
