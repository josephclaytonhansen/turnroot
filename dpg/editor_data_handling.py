from os.path import exists
import json
import ui_colorthemes
from globals import globals as g

def LoadUserPrefs():
    if not exists("user_preferences.trup"): 
        with open("user_preferences.trup", "w") as f:
            json.dump(g.prefs, f)
    else:
        with open("user_preferences.trup", "r") as f:
            g.prefs = json.load(f)
            g.color_theme = ui_colorthemes.colorthemes[g.prefs["color_theme"]]
            g.corners_round = g.prefs["corners_round"]
            g.padding = g.prefs["padding"]
            g.item_spacing = g.prefs["item_spacing"]
            g.window_padding = g.prefs["window_padding"]
            g.mono_text_size = g.prefs["mono_text_size"]
            g.text_size = g.prefs["text_size"]
            g.font_family = g.prefs["font_family"]
            g.autosave_time = g.prefs["autosave_time"]

def SaveUserPrefs():
    with open("user_preferences.trup", "w") as f:
        g.prefs["color_theme"] = ui_colorthemes.colorthemes[g.color_theme.tag].tag
        g.prefs["corners_round"] = g.corners_round
        g.prefs["padding"] = g.padding
        g.prefs["item_spacing"] = g.item_spacing
        g.prefs["window_padding"] = g.window_padding
        g.prefs["mono_text_size"] = g.mono_text_size
        g.prefs["text_size"] = g.text_size
        g.prefs["autosave_time"] = g.autosave_time
        
        if g.font_family.startswith("Assets"):
            g.prefs["font_family"] = g.font_family
        else:
            g.prefs["font_family"] = "Assets/Fonts/"+g.font_family+"-Regular.ttf"
        json.dump(g.prefs, f)
    
    