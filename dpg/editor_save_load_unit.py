from os.path import exists
import json, os
import ui_colorthemes
from globals import globals as g

def LoadUnit(path):
    if g.is_editing.type == "unit": unit = g.is_editing 
    if not exists(path+".truf"): 
        with open(path+".truf", "w") as f:
           
           save_dict = {"base_stats":unit.base_stats,
                        "growth_rates":unit.growth_rates}
           json.dump(save_dict, f)
    else:
        with open(path+".truf", "r") as f:
            save_dict = json.load(f)
            unit.base_stats = save_dict["base_stats"]
            unit.growth_rates = save_dict["growth_rates"]
            

def SaveUnit(path):
    if g.is_editing.type == "unit": unit = g.is_editing 
    with open(path+".truf", "w") as f:
        
        save_dict = {"base_stats":unit.base_stats,
                        "growth_rates":unit.growth_rates}
        json.dump(save_dict, f)