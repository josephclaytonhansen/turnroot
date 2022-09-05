from os.path import exists
import json
from globals import globals as g

def LoadSkill(path):
    if g.is_editing.type == "skill": skill = g.is_editing 
    if not exists(path): 
        with open(path, "w") as f:
           json.dump(g.skill_editor_skill.data, f)
    else:
        with open(path, "r") as f:
            g.skill_editor_skill.data = json.load(f)

def SaveSkill(path):
    if g.is_editing.type == "skill": skill = g.is_editing 
    with open(path, "w") as f:
        
        g.skill_editor_skill.data["pos"] = g.skill_editor_skill_positions
        g.skill_editor_skill.data["con"] = g.skill_editor_skill_connections
        g.skill_editor_skill.data["awn"] = g.window_widgets_skill.active_nodes
        g.skill_editor_skill.data["sta"] = g.skill_editor_skill_statics
        json.dump(g.skill_editor_skill.data, f)

