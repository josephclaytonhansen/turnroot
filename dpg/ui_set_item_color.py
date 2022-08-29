from globals import globals as g
import dearpygui.dearpygui as d
from ui_set_global_colors import *

def set_item_color(item, color, what = d.mvThemeCol_Text):
    with d.theme() as item_theme:
        with d.theme_component(d.mvAll):
            d.add_theme_color(what, htr(color), category=d.mvThemeCat_Core)
    d.bind_item_theme(item, item_theme)

def set_item_style(item, style, what):
    with d.theme() as item_theme:
        with d.theme_component(d.mvAll):
            d.add_theme_style(what, style, style, category=d.mvThemeCat_Core)
    d.bind_item_theme(item, item_theme)
