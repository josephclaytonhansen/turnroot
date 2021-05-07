#specific imports
from src.skeletons.weapon_experience import weaponExperience
from src.skeletons.unit_class import unitClass
from src.skeletons.weakness_strength import Weakness, Strength
from src.skeletons.unit_level import Level
from src.skeletons.unit_class import unitClass
from src.skeletons.team_likes_dislikes import teamDislike, teamLike
from src.skeletons.identities import orientations, genders, pronouns

#general imports
from src.skeletons.Portrait import Portrait
from src.skeletons.Object import Object
from src.skeletons.Skill import Skill
from src.skeletons.Tactic import Tactic
from src.skeletons.Skilled_Blow import skilledBlow
from src.skeletons.Attack import Attack
from src.skeletons.Action import Action

from src.skeletons.Support_Level import supportLevel

import json
with open("src/skeletons/universal_stats.json", "r") as stats_file:
    universal_stats =  json.load(stats_file)

class Unit():
    def __init__(self):
        self.name = ""
        self.title = ""
        self.unique = True
        self.is_friendly = True
        self.is_ally = False
        self.is_recruitable = False
        self.is_lord = False
        self.has_dialogue = True
        self.is_permanently_dead = False
        
        self.AI_sheet = None
        
        self.description = ""
        self.notes = ""
        
        self.portraits = {}
        self.sprites = {}
        self.sounds =  {}
        
        self._gender = genders().MALE
        self.orientation = orientations().STRAIGHT
        self.pronouns = pronouns(self._gender).pronouns
        
        self.level = 1
        self.exp = 0
        self.exp_to_next_level = 0
        self.move = 0
        self.size = 1
        
        self.is_mounted = False
        self.is_currently_mounted = False
        
        self.weapon_exps = {}
        self.unit_classes_exps = {} 
        
        for stat in universal_stats:
            setattr(self,stat,0)
        
        self.unit_class = None
        self.mastered_unit_classes = {}
        self.future_unit_classes = {}
        self.unique_classes = {}
        self.unique_objects = {}
        
        self.strengths = {}
        self.weaknesses = {}
        
        self.skills = {}
        self.tactics = {}
        self.skilled_blows = {}
        
        self.inventory_objects = {}
        self.attacks = {}
        self.actions = {}
        
        self.team_likes = {}
        self.team_dislikes = {}
        self.support_levels = {}
    
    @property
    def gender(self):
        return self._gender
       
    @gender.setter
    def gender(self, g):
        self._gender = g
        self.setIdentity()
    
    def createUniversalStat(self, stat):
        universal_stats.append(stat)
        with open("universal_stats.json", "w") as stats_file:
            json.dump(universal_stats, stats_file)
        setattr(self, stat, 0)
    
    def setStats(self, unit_file):
        with open(unit_file, "r") as stats_file:
            unit_stats =  json.load(stats_file)
            for stat in unit_stats:
                setattr(self,stat,unit_stats[stat])
    
    def setIdentity(self):
        self.pronouns = pronouns(self.gender).pronouns
    
    def selfToJSON(self):
        basic_attrs = ["name","title","unique","is_friendly","is_ally","is_lord","is_recruitable",
                 "has_dialogue","is_permanently_dead","AI_sheet","gender","pronouns","orientation",
                       "portraits","sprites","sounds","level","exp","exp_to_next_level","move","size",
                       "is_mounted","is_currently_mounted","weapon_exps","unit_classes_exps",
                       "unit_class","mastered_unit_classes","future_unit_classes","unique_classes",
                       "unique_objects","strengths","weaknesses","skills","tactics",
                       "skilled_blows","inventory_objects","attacks","actions","team_likes",
                       "team_dislikes","support_levels","description","notes"]
        
        for stat in universal_stats:
            basic_attrs.append(stat)
        
        basic_attrs_dict = {}
        for b in basic_attrs:
            basic_attrs_dict[b] = getattr(self,b)
            
        with open("src/skeletons/unit_test_save.json", "w") as wf:
            json.dump(basic_attrs_dict, wf)






        