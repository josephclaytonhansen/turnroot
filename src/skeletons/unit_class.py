import pickle

class unitClass():
    def __init__(self):
        
        self.unit_class_name = None
        
        self.tactics = {}
        self.skills = []
        self.skill_criteria = {}
        self.skilled_blows = {}
        
        self.tactics_minimum_class_exp = {}
        self.skills_minimum_class_exp = {}
        self.skilled_blows_minimum_class_exp = {}
        
        self.allowed_weapon_types = []
        self.disallowed_weapon_types = []
        self.minimum_level = 0
        self.is_mounted = False
        
        self.mounted_move_change = 0
        self.mounted_tile_changes = {}
        self.dismounted_tile_changes = {}
        
        self.weak_against = {}
        self.weak_against_amount = {}
        
        self.exp_gained_multiplier = 1.0
        self.class_type = None
        
        self.growth_rates = {}
        self.stat_bonuses = {}
        self.stat_bonuses_criteria = {}
        
        self.next_classes = {}
        
    def selfToJSON(self, path, p = True):
        if self.unit_class_name != None:
            basic_attrs = ["unit_class_name", "tactics", "skills", "skilled_blows", "growth_rates",
                           "tactics_minimum_class_exp", "skills_minimum_class_exp", "skilled_blows_minimum_class_exp",
                           "allowed_weapon_types", "disallowed_weapon_types", "minimum_level", "is_mounted",
                           "mounted_move_change", "mounted_tile_changes", "dismounted_tile_changes",
                           "weak_against", "weak_against_amount", "exp_gained_multiplier",
                           "class_type", "stat_bonuses", "stat_bonuses_criteria", "next_classes", "skill_criteria"]

            
            basic_attrs_dict = {}
            for b in basic_attrs:
                basic_attrs_dict[b] = getattr(self,b)
                
            with open(path, "wb") as wf:
                pickle.dump(basic_attrs_dict, wf)
                
            if p == True:
                pass
                # self.parent.getClassesInFolder()
    
    def selfFromJSON(self, path):
        basic_attrs = ["unit_class_name", "tactics", "skills", "skilled_blows", "growth_rates",
                       "tactics_minimum_class_exp", "skills_minimum_class_exp", "skilled_blows_minimum_class_exp",
                       "allowed_weapon_types", "disallowed_weapon_types", "minimum_level", "is_mounted",
                       "mounted_move_change", "mounted_tile_changes", "dismounted_tile_changes",
                       "weak_against", "weak_against_amount", "exp_gained_multiplier",
                       "class_type", "stat_bonuses", "stat_bonuses_criteria", "next_classes", "skill_criteria"]
        
        with open(path, "rb") as rf:
            tmp_data = pickle.load(rf)
        
        for a in basic_attrs:
            setattr(self, a, tmp_data[a])