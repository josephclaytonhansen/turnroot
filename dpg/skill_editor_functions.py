from globals import globals as g
from ui_colorthemes import colorthemes as themes
from ui_set_global_colors import set_colors, htr, darken
from ui_set_global_font import set_fonts
import dearpygui.dearpygui as d
from editor_data_handling import SaveUserPrefs
from ui_item_style_helpers import *
from ui_layout_helpers import TimedInfoMessage, BuildTable

import random
from universal_behavior_presets import behavioral_presets

def basic(sender, app_data, user_data):
    print(sender, app_data, user_data)

def color_theme(sender, app_data, user_data):
    g.color_theme = themes[app_data]
    d.bind_theme(set_colors(g.color_theme))
    user_data.colors.set()
    SaveUserPrefs()

def font_size(sender, app_data, user_data):
    g.text_size = app_data
    set_fonts()
    SaveUserPrefs()
    TimedInfoMessage("Requires restart- no changes will be visible", g.active_window_widgets.status_bar)

def fullscreen():
    g.fullscreen = not g.fullscreen
    d.toggle_viewport_fullscreen()
    d.set_viewport_pos([0,0])
    SaveUserPrefs()

def font(sender, app_data, user_data):
    g.font_family = app_data
    set_fonts(label="Assets/Fonts/"+app_data+"-Regular.ttf")
    SaveUserPrefs()
    TimedInfoMessage("Requires restart- no changes will be visible", g.active_window_widgets.status_bar)
    
def window_padding(sender, app_data, user_data):
    g.window_padding = app_data
    d.bind_theme(set_colors(g.color_theme))
    SaveUserPrefs()

def corners_round(sender, app_data, user_data):
    g.corners_round = app_data
    d.bind_theme(set_colors(g.color_theme))
    SaveUserPrefs()

def padding(sender, app_data, user_data):
    g.padding = app_data
    d.bind_theme(set_colors(g.color_theme))
    SaveUserPrefs()

def ChangeAutosave(sender, app_data, user_data):
    g.autosave_time = app_data
    d.bind_theme(set_colors(g.color_theme))
    SaveUserPrefs()

def item_spacing(sender, app_data, user_data):
    g.item_spacing = app_data
    d.bind_theme(set_colors(g.color_theme))
    SaveUserPrefs()

def ShowFileDialog(sender, app_data, user_data):
    if sender == "open":
        d.show_item("SkillSelect")
        d.set_item_user_data("SkillSelect", "open")
    else:
        d.show_item("SkillSelect")
        d.set_item_user_data("SkillSelect", "save")
        
def NewSkillFile():
    pass