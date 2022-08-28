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