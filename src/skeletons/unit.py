#specific imports
from src.skeletons.weapon_experience import weaponExperience
from src.skeletons.unit_class import unitClass
from src.skeletons.weakness_strength import Weakness, Strength
from src.skeletons.unit_level import Level
from src.skeletons.unit_class import unitClass
from src.skeletons.team_likes_dislikes import teamDislike, teamLike
from src.skeletons.weapon_types import weaponTypes

#general imports
from src.skeletons.Portrait import Portrait
from src.skeletons.Object import Object
from src.skeletons.Skill import Skill
from src.skeletons.Tactic import Tactic
from src.skeletons.Skilled_Blow import skilledBlow
from src.skeletons.Attack import Attack
from src.skeletons.Action import Action

from src.skeletons.Support_Level import supportLevel

import json, pickle

with open("src/skeletons/universal_stats.json", "r") as stats_file:
    universal_stats =  json.load(stats_file)
with open("src/skeletons/universal_classifications.json", "r") as stats_file:
    universal_classifications =  json.load(stats_file)

universal_weapon_types = weaponTypes().data

class Unit():
    def __init__(self):
        self.folder_index = 0
        self.parent = None
        
        self.name = ""
        self.title = ""
        self.classification = "Human"
        self.unique = True
        self.is_friendly = True
        self.is_ally = False
        self.is_recruitable = False
        self.is_lord = False
        self.has_dialogue = True
        self.is_permanently_dead = False
        
        self.description = ""
        self.notes = ""
        
        for stat in universal_stats:
            setattr(self,stat,0)
        
        self.portraits = {}
        self.sprites = {}
        self.sounds =  {}
        
        self.pronouns = ""
        
        self.level = 1
        self.exp = 0
        self.exp_to_next_level = 100
        self.move = 0
        self.size = 1
        self.current_hp = 0
        self.visibility_range = 0
        self.armored = False
        
        self.status = None
        self.status_duration = 0
        self.in_battle_dialogues = {}
        
        self.current_bonuses = {}
        self.current_penalties = {}
        
        self.is_mounted = False
        self.is_flying = False
        self.is_currently_mounted = False
        
        self.weapon_exps = {}
        self.current_weapon_levels = {}
        for stat in universal_stats:
            self.current_weapon_levels[stat] = "E"
        self.unit_classes_exps = {} 
        
        self.unit_class = None
        self.mastered_unit_classes = {}
        self.past_classes = []
        self.future_unit_classes = {}
        self.unique_classes = {}
        self.unique_objects = {}
        
        self.affinities = {}
        
        self.skills = []
        self.tactics = {}
        self.skilled_blows = {}
        
        self.stat_caps = {}
        
        self.inventory_objects = {}
        self.attacks = {}
        self.actions = {}
        
        self.max_support_levels = {}
        self.support_difficulty = {}
        self.support_levels = {}
        
        self.personal_enemy = None
        
        self.AI_soldier = 0
        self.AI_strategic = 0
        self.AI_cautious = 0
        
        self.AI_sheets = {}
        
        self.generic_stat_randomness = {}
        self.generic_stat_randomness_amount = {}
        self.generic_sprite_options = {}
        self.generic_gfx_options = {}
        
        self.growth_rates = {}
        self.current_goals = {}
        self.future_goals = {}
        
        self.pregnancy_type = ""
        self.child = None
        self.spouse = None
    
    def createUniversalStat(self, stat):
        stat = stat.lower()
        universal_stats.append(stat)
        with open("src/skeletons/universal_stats.json", "w") as stats_file:
            json.dump(universal_stats, stats_file)
        setattr(self, stat, 0)
    
    def removeUniversalStat(self, stat):
        universal_stats.remove(stat)
        with open("src/skeletons/universal_stats.json", "w") as stats_file:
            json.dump(universal_stats, stats_file)
    
    def createUniversalClassification(self, stat):
        stat = stat.lower()
        stat = stat[0].upper() + stat[1:]
        universal_classifications.append(stat)
        with open("src/skeletons/universal_classifications.json", "w") as stats_file:
            json.dump(universal_classifications, stats_file)
        setattr(self, stat, 0)
    
    def removeUniversalClassification(self, stat):
        universal_classifications.remove(stat)
        with open("src/skeletons/universal_classifications.json", "w") as stats_file:
            json.dump(universal_classifications, stats_file)
            
    def createUniversalWeaponsType(self, stat):
        stat = stat.lower()
        universal_weapon_types.append(stat)
        with open("src/skeletons/universal_weapon_types.json", "w") as stats_file:
            json.dump(universal_weapon_types, stats_file)
    
    def removeUniversalWeaponsType(self, stat):
        universal_weapon_types.remove(stat)
        with open("src/skeletons/universal_weapon_types.json", "w") as stats_file:
            json.dump(universal_weapon_types, stats_file)
    
    def selfToJSON(self, path, p = True):
        basic_attrs = ["name","title","unique","is_friendly","is_ally","is_lord","is_recruitable",
                 "has_dialogue","is_permanently_dead","pronouns",
                       "portraits","sprites","sounds","level","exp","exp_to_next_level","move","size",
                       "is_mounted","is_currently_mounted","weapon_exps","unit_classes_exps",
                       "unit_class","mastered_unit_classes","future_unit_classes","unique_classes",
                       "unique_objects","affinities","skills","tactics", "stat_caps",
                       "skilled_blows","inventory_objects","attacks","actions","support_difficulty",
                       "max_support_levels","support_levels","description","notes","AI_soldier",
                       "AI_strategic", "AI_cautious", "AI_sheets", "personal_enemy", "visibility_range",
                       "folder_index", "current_weapon_levels", "generic_stat_randomness", "generic_sprite_options",
                           "generic_gfx_options", "generic_stat_randomness_amount", "growth_rates", "current_goals",
                       "future_goals","past_classes", "armored", "status", "in_battle_dialogues", "status_duration",
                       "current_bonuses", "current_penalties", "is_flying", "classification", "current_hp",
                       "pregnancy_type", "child", "spouse"]
        
        for stat in universal_stats:
            basic_attrs.append(stat)
        
        basic_attrs_dict = {}
        for b in basic_attrs:
            basic_attrs_dict[b] = getattr(self,b)
            
        with open(path, "wb") as wf:
            pickle.dump(basic_attrs_dict, wf)
        
        if p == True:
            self.parent.getUnitsInFolder()
    
    def selfFromJSON(self, path):
        basic_attrs = ["name","title","unique","is_friendly","is_ally","is_lord","is_recruitable",
                 "has_dialogue","is_permanently_dead","pronouns",
                       "portraits","sprites","sounds","level","exp","exp_to_next_level","move","size",
                       "is_mounted","is_currently_mounted","weapon_exps","unit_classes_exps",
                       "unit_class","mastered_unit_classes","future_unit_classes","unique_classes",
                       "unique_objects","affinities","skills","tactics", "stat_caps",
                       "skilled_blows","inventory_objects","attacks","actions","support_difficulty",
                       "max_support_levels","support_levels","description","notes","AI_soldier",
                       "AI_strategic", "AI_cautious", "AI_sheets", "personal_enemy", "visibility_range",
                       "folder_index", "current_weapon_levels", "generic_stat_randomness", "generic_sprite_options",
                           "generic_gfx_options", "generic_stat_randomness_amount", "growth_rates","current_goals",
                       "future_goals", "past_classes", "armored", "status", "in_battle_dialogues", "status_duration",
                       "current_bonuses","current_penalties", "is_flying", "classification", "current_hp",
                       "pregnancy_type", "child", "spouse"]
        
        for stat in universal_stats:
            basic_attrs.append(stat)
        
        with open(path, "rb") as rf:
            tmp_data = pickle.load(rf)
        
        for a in basic_attrs:
            setattr(self, a, tmp_data[a])
            
    def addSkill(self,name):
        self.skills.append(name)
    
    def removeSkill(self,name):
        self.skills.pop(name)
      