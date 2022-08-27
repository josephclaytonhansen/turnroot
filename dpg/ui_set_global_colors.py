import dearpygui.dearpygui as dpg
from globals import globals as g
    
def htr(h):
    w = g.color_theme.__getattribute__(h).lstrip('#')
    w = tuple(int(w[i:i+2], 16) for i in (0, 2, 4))
    return w

def lighten(t, i = 10):
    w =  list(t)
    w[0] += i
    w[1] += i
    w[2] += i
    for x in [0,1,2]:
        if w[x] > 255:
            w[x] = 255
    return tuple(w)

def darken(t, i =10):
    w =  list(t)
    w[0] -= i
    w[1] -= i
    w[2] -= i
    for x in [0,1,2]:
        if w[x] < 0:
            w[x] = 0
    return tuple(w)

def set_colors(palette):
    g.color_theme = palette
    g.clear_color = darken(htr("window_background_color"),30)
    
    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            for c in [
                dpg.mvStyleVar_FrameRounding,
                dpg.mvStyleVar_ScrollbarRounding,
                dpg.mvStyleVar_ScrollbarRounding,
                dpg.mvStyleVar_TabRounding,
                dpg.mvStyleVar_GrabRounding,
                dpg.mvStyleVar_GrabRounding,
                dpg.mvStyleVar_PopupRounding,
                dpg.mvStyleVar_ChildRounding,
                ]:
                
                dpg.add_theme_style(c, g.corners_round, category=dpg.mvThemeCat_Core)
                
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, htr("window_background_color"), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, htr("node_grid_lines_color"), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg, htr("node_grid_lines_color"), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Header, htr("node_grid_lines_color"), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, htr("list_background_color"), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, darken(htr("list_background_color"),20),category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, htr("node_grid_alt_lines_color"), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Text, htr("window_text_color"), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Border, htr("list_background_color"), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg, htr("list_background_color"), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, htr("list_background_color"), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Button, htr("list_background_color"), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, lighten(htr("list_background_color"),15), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, darken(htr("list_background_color"),15), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, darken(htr("list_background_color"),15), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, htr("button_alt_color"), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, lighten(htr("button_alt_color"),10), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, htr("node_selected_color"), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, htr("list_background_color"), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, htr("node_wire_color"), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ResizeGrip, darken(htr("window_background_color"),10), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ResizeGripHovered, htr("node_selected_color"), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ResizeGripActive, htr("node_selected_color"), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark, htr("list_background_color"), category=dpg.mvThemeCat_Core)
    return global_theme