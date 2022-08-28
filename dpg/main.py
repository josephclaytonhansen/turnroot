from viewport import *
from unit_editor import add_unit_editor
import dearpygui.dearpygui as d
from ui_set_global_colors import set_colors
from ui_set_global_font import set_fonts
from globals import globals as g
import json
import ui_colorthemes
from unit_editor import unit_editor_update_height
from os.path import exists

d.create_context()

def getGeometry():
    g.current_height = d.get_viewport_client_height()
    unit_editor_update_height()

d.set_viewport_resize_callback(callback=getGeometry)

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
    
d.bind_theme(set_colors(g.color_theme))
set_fonts()    

init_viewport(True)
add_global_menu()

add_unit_editor()

if not g.debug:
    d.set_primary_window("unit_editor", True)
    
d.start_dearpygui()
d.destroy_context()