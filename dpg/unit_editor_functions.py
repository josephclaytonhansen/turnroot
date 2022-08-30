from globals import globals as g
from ui_colorthemes import colorthemes as themes
from ui_set_global_colors import set_colors
from ui_set_global_font import set_fonts
import dearpygui.dearpygui as d
from editor_data_handling import SaveUserPrefs
from ui_item_style_helpers import *

def basic(sender, app_data, user_data):
    print(sender, app_data, user_data)

def unit_type_pipe(sender, app_data, user_data):
    try:
        if app_data == "Generic Unit":
            g.is_editing.is_generic = True
            g.is_editing.is_avatar = False
            g.is_editing.has_stats = True
        elif app_data == "Avatar/Player Character":
            g.is_editing.is_generic = False
            g.is_editing.is_avatar = True
            g.is_editing.has_stats = True
        elif app_data == "NPC":
            g.is_editing.is_generic = True
            g.is_editing.is_avatar = True
            g.is_editing.has_stats = False
        else:
            g.is_editing.is_generic = False
            g.is_editing.is_avatar = False
            g.is_editing.has_stats = True
        return True
    except:
        return False

def show_stat_variation(widgets):
    d.configure_item(widgets.stat_variation, show=True)

def hide_stat_variation(widgets):
    d.configure_item(widgets.stat_variation, show=False)

def show_stats(widgets):
    d.configure_item(widgets.right, show=True)

def hide_stats(widgets):
    d.configure_item(widgets.right, show=False)
    
def color_theme(sender, app_data, user_data):
    g.color_theme = themes[app_data]
    d.bind_theme(set_colors(g.color_theme))
    user_data.colors.set()
    SaveUserPrefs()

def font_size(sender, app_data, user_data):
    g.text_size = app_data
    print(g.text_size)
    set_fonts()
    SaveUserPrefs()

def window_padding(sender, app_data, user_data):
    g.window_padding = app_data
    d.bind_theme(set_colors(g.color_theme))
    SaveUserPrefs()

def padding(sender, app_data, user_data):
    g.padding = app_data
    d.bind_theme(set_colors(g.color_theme))
    SaveUserPrefs()

def item_spacing(sender, app_data, user_data):
    g.item_spacing = app_data
    d.bind_theme(set_colors(g.color_theme))
    SaveUserPrefs()