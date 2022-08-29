from globals import globals as g
import dearpygui.dearpygui as d
from ui_set_global_colors import *

def set_item_color(item, color, what = d.mvThemeCol_Text):
    with d.theme() as item_theme:
        with d.theme_component(d.mvAll):
            d.add_theme_color(what, htr(color), category=d.mvThemeCat_Core)
    d.bind_item_theme(item, item_theme)

def set_item_colors(item, colors, whats = d.mvThemeCol_Text):
    with d.theme() as item_theme:
        i = -1
        for color in colors:
            i +=1
            with d.theme_component(d.mvAll):
                d.add_theme_color(whats[i], htr(colors[i]), category=d.mvThemeCat_Core)

    d.bind_item_theme(item, item_theme)

def set_item_style(item, style, what):
    with d.theme() as item_theme:
        with d.theme_component(d.mvAll):
            d.add_theme_style(what, style, style, category=d.mvThemeCat_Core)
    d.bind_item_theme(item, item_theme)

def set_font_size(item, scale):
    """Scale from -3 to 6, where 0 is font_size = 1.0"""
    s = scale + 3
    d.bind_item_font(item, g.font_sizes[s])
