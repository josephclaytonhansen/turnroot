import pickle

class unitClass():
    def __init__(self):
        self.help_dict = {
            "tactics_minimum_class_exp": "how much class EXP must be gained for this tactic",
            "skills_minimum_class_exp": "how much class EXP must be gained for this skill",
            "skilled_blows_minimum_class_exp": "how much class EXP must be gained for this skilled blow",
            "minimum_level": "what level the unit must reach to unlock this class",
            "weak_against": "attack types that do more (or less) damage because of this class",
            "weak_against_amount": "if greater than 1, attack type does more damage. If less than 1, it does less. 2.0 would do double damage, .5 would do half.",
            "self.is_mounted": "If the unit has the Mount/Dismount command, which changes mobility",
            "mounted_move_change": "how much the move stat is increased by when mounted",
            "mounted_tile_changes": "how mounting changes the tile interactions",
            "dismounted_tile_changes": "how movement changes if unit is dismounted, or is_mounted is False",
            "exp_gained_multiplier": "how quickly or slowly the unit levels up- i.e., how much 1 EXP point is worth.",
            "class_type": "if classes are split into categories, class category",
            "growth_rates": "when leveling up, the chance of each stat getting an increase. 1 is 100% chance, 0 is 0, .5 is 50%",
            "stat_bonuses": "stat bonuses given when changing to this class",
            "stat_bonuses_criteria": "per stat_bonus, criteria for it. \n i.e.: If 'strength' + 5 is a stat_bonus, 'strength': self.unit.affinities['strength'] == 'B'",
            "next_classes": "if classes branch, next options. Ignored if classes are in grid"
            }
        
        self.unit_class_name = None
        
        self.tactics = {}
        self.skills = {}
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
                           "class_type", "stat_bonuses", "stat_bonuses_criteria", "next_classes"]

            
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
                       "class_type", "stat_bonuses", "stat_bonuses_criteria", "next_classes"]
        
        with open(path, "rb") as rf:
            tmp_data = pickle.load(rf)
        
        for a in basic_attrs:
            setattr(self, a, tmp_data[a])