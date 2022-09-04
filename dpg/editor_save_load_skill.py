from os.path import exists
import json
from globals import globals as g

def LoadSkill(path):
    if g.is_editing.type == "skill": unit = g.is_editing 
    if not exists(path): 
        with open(path, "w") as f:
           
           save_dict = {"":""}
           json.dump(save_dict, f)
    else:
        with open(path, "r") as f:
            pass


            

def SaveSkill(path):
    if g.is_editing.type == "skill": skill = g.is_editing 
    with open(path, "w") as f:
        
        save_dict = {"":""}
        json.dump(save_dict, f)

