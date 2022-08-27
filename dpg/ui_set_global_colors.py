import dearpygui.dearpygui as dpg
from globals import globals as g
    
def htr(h):
    w = g.color_theme.__getattribute__(h).lstrip('#')
    w = tuple(int(w[i:i+2], 16) for i in (0, 2, 4))
    return w

def set_colors(palette):
    g.color_theme = palette
    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, htr("window_background_color"), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Text, htr("window_text_color"), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Border, htr("list_background_color"), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg, htr("list_background_color"), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, htr("list_background_color"), category=dpg.mvThemeCat_Core)
    return global_theme