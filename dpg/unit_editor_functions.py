from globals import globals as g
from ui_colorthemes import colorthemes as themes
from ui_set_global_colors import set_colors
import dearpygui.dearpygui as d
from editor_data_handling import SaveUserPrefs

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
    