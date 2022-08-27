from globals import globals as g
import dearpygui.dearpygui as dpg
from ui_set_global_colors import *

def set_item_color(item, color, what = dpg.mvThemeCol_Text):
    with dpg.theme() as item_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(what, htr(color), category=dpg.mvThemeCat_Core)
    dpg.bind_item_theme(item, item_theme)