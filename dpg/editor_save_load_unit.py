from os.path import exists
import json
from globals import globals as g

def LoadUnit(path):
    if g.is_editing.type == "unit": unit = g.is_editing 
    if not exists(path): 
        with open(path, "w") as f:
           
           save_dict = {"base_stats":unit.base_stats,
                        "growth_rates":unit.growth_rates,
                        "name":unit.name,
                        "pronouns":unit.pronouns,
                        "current_class":unit.current_class,
                        "unit_type":unit.unit_type,
                        "notes":unit.notes,
                        "description":unit.description,
                        "default_affinities":unit.default_affinities,
                        "behavior_preset":unit.behavior_preset,
                        "behavorial_sliders":unit.behavorial_sliders}
           json.dump(save_dict, f)
    else:
        with open(path, "r") as f:
            save_dict = json.load(f)
            unit.base_stats = save_dict["base_stats"]
            unit.growth_rates = save_dict["growth_rates"]

            unit.name = save_dict["name"]
            unit.pronouns = save_dict["pronouns"]
            unit.current_class = save_dict["current_class"]
            unit.unit_type = save_dict["unit_type"]
            unit.notes = save_dict["notes"]
            unit.description = save_dict["description"]
            unit.default_affinities = save_dict["default_affinities"]
            unit.behavorial_sliders = save_dict["behavorial_sliders"]
            unit.behavior_preset = save_dict["behavior_preset"]


            

def SaveUnit(path):
    if g.is_editing.type == "unit": unit = g.is_editing 
    with open(path, "w") as f:
        
        save_dict = {"base_stats":unit.base_stats,
                        "growth_rates":unit.growth_rates,
                        "name":unit.name,
                        "pronouns":unit.pronouns,
                        "current_class":unit.current_class,
                        "unit_type":unit.unit_type,
                        "notes":unit.notes,
                        "description":unit.description,
                        "default_affinities":unit.default_affinities,
                        "behavior_preset":unit.behavior_preset,
                        "behavorial_sliders":unit.behavorial_sliders}
        json.dump(save_dict, f)

