import pickle

class unitClass():
    def __init__(self):
        
        self.unit_class_name = None
        self.desc = ""
        
        self.tactics = []
        self.tactics_criteria = []
        self.skills = []
        self.skill_criteria = {}
        self.skilled_blows = []
        self.skilled_blows_criteria = {}
        
        self.allowed_weapon_types = []
        self.disallowed_weapon_types = []
        self.minimum_level = 0
        self.is_mounted = False
        self.is_flying = False
        
        self.mounted_move_change = 0
        self.mounted_tile_changes = {}
        self.dismounted_tile_changes = {}
        
        self.weak_against = {}
        self.weak_against_amount = {}
        
        self.exp_gained_multiplier = 1.0
        self.class_type = None
        
        self.growth_rates = {}
        self.stat_bonuses = {}
        
        self.next_classes = {}
        
        self.portrait_changes = {}
        self.sprite_changes = {}
        self.gfx_changes = {}
        
    def selfToJSON(self, path, p = True):
        if self.unit_class_name != None:
            basic_attrs = ["unit_class_name", "tactics", "skills", "skilled_blows", "growth_rates",
                           "tactics_criteria", "skilled_blows_criteria", "desc", "portrait_changes",
                           "allowed_weapon_types", "disallowed_weapon_types", "minimum_level", "is_mounted",
                           "mounted_move_change", "mounted_tile_changes", "dismounted_tile_changes",
                           "weak_against", "weak_against_amount", "exp_gained_multiplier",
                           "class_type", "stat_bonuses", "next_classes", "skill_criteria", "is_flying",
                           "sprite_changes", "gfx_changes"]

            basic_attrs_dict = {}
            for b in basic_attrs:
                basic_attrs_dict[b] = getattr(self,b)
            if "Skill Name" in basic_attrs_dict["skills"]:
                basic_attrs_dict["skills"].remove("Skill Name")
                
            with open(path, "wb") as wf:
                #print(basic_attrs_dict)
                pickle.dump(basic_attrs_dict, wf)
                
            if p == True:
                pass
                # self.parent.getClassesInFolder()
    
    def selfFromJSON(self, path):
        basic_attrs = ["unit_class_name", "tactics", "skills", "skilled_blows", "growth_rates",
                           "tactics_criteria", "skilled_blows_criteria", "desc", "portrait_changes",
                           "allowed_weapon_types", "disallowed_weapon_types", "minimum_level", "is_mounted",
                           "mounted_move_change", "mounted_tile_changes", "dismounted_tile_changes",
                           "weak_against", "weak_against_amount", "exp_gained_multiplier",
                           "class_type", "stat_bonuses", "next_classes", "skill_criteria", "is_flying",
                           "sprite_changes", "gfx_changes"]
        
        with open(path, "rb") as rf:
            tmp_data = pickle.load(rf)
        
        for a in basic_attrs:
            setattr(self, a, tmp_data[a])
            if "Skill Name" in self.skills:
                    self.skills.remove("Skill Name")