import dearpygui.dearpygui as d
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
    
    with d.theme() as global_theme:
        for x in [d.mvFileDialog, d.mvAll, d.mvChildWindow]:
            with d.theme_component(x):
                for c in [
                    d.mvStyleVar_FrameRounding,
                    d.mvStyleVar_ScrollbarRounding,
                    d.mvStyleVar_ScrollbarRounding,
                    d.mvStyleVar_TabRounding,
                    d.mvStyleVar_GrabRounding,
                    d.mvStyleVar_GrabRounding,
                    d.mvStyleVar_PopupRounding,
                    d.mvStyleVar_ChildRounding,
                    ]:
                    
                    d.add_theme_style(c, g.corners_round, category=d.mvThemeCat_Core)
                d.add_theme_style(d.mvStyleVar_WindowPadding, g.window_padding, g.window_padding, category=d.mvThemeCat_Core) 
                d.add_theme_style(d.mvStyleVar_ItemSpacing, g.item_spacing, g.item_spacing, category=d.mvThemeCat_Core) 
                d.add_theme_style(d.mvStyleVar_FramePadding, g.padding, g.padding, category=d.mvThemeCat_Core) 
                d.add_theme_color(d.mvThemeCol_PopupBg, darken(htr("node_grid_lines_color"),5), category=d.mvThemeCat_Core)
                d.add_theme_color(d.mvThemeCol_WindowBg, htr("window_background_color"), category=d.mvThemeCat_Core)
                d.add_theme_color(d.mvThemeCol_Tab, htr("node_grid_background_color"), category=d.mvThemeCat_Core)
                d.add_theme_color(d.mvThemeCol_TabUnfocused, darken(htr("window_background_color"),20), category=d.mvThemeCat_Core)
                d.add_theme_color(d.mvThemeCol_TabUnfocusedActive, lighten(htr("window_background_color"),20), category=d.mvThemeCat_Core)
                d.add_theme_color(d.mvThemeCol_TabActive, htr("list_background_color"), category=d.mvThemeCat_Core)
                d.add_theme_color(d.mvThemeCol_TabHovered, darken(htr("node_grid_background_color"),30), category=d.mvThemeCat_Core)
                d.add_theme_color(d.mvThemeCol_TextSelectedBg, htr("node_selected_color"), category=d.mvThemeCat_Core)
                d.add_theme_color(d.mvThemeCol_ChildBg, darken(htr("window_background_color"),10), category=d.mvThemeCat_Core)
                d.add_theme_color(d.mvThemeCol_ScrollbarBg, htr("node_grid_lines_color"), category=d.mvThemeCat_Core)
                d.add_theme_color(d.mvThemeCol_MenuBarBg, htr("node_grid_lines_color"), category=d.mvThemeCat_Core)
                d.add_theme_color(d.mvThemeCol_Header, htr("node_grid_lines_color"), category=d.mvThemeCat_Core)
                d.add_theme_color(d.mvThemeCol_HeaderHovered, htr("list_background_color"), category=d.mvThemeCat_Core)
                d.add_theme_color(d.mvThemeCol_HeaderActive, darken(htr("list_background_color"),20),category=d.mvThemeCat_Core)
                d.add_theme_color(d.mvThemeCol_ScrollbarGrab, htr("node_grid_alt_lines_color"), category=d.mvThemeCat_Core)
                d.add_theme_color(d.mvThemeCol_Text, htr("window_text_color"), category=d.mvThemeCat_Core)
                d.add_theme_color(d.mvThemeCol_Border, htr("list_background_color"), category=d.mvThemeCat_Core)
                d.add_theme_color(d.mvThemeCol_TitleBg, htr("list_background_color"), category=d.mvThemeCat_Core)
                d.add_theme_color(d.mvThemeCol_TitleBgActive, htr("list_background_color"), category=d.mvThemeCat_Core)
                d.add_theme_color(d.mvThemeCol_Button, htr("list_background_color"), category=d.mvThemeCat_Core)
                d.add_theme_color(d.mvThemeCol_ButtonHovered, lighten(htr("list_background_color"),15), category=d.mvThemeCat_Core)
                d.add_theme_color(d.mvThemeCol_ButtonActive, darken(htr("list_background_color"),15), category=d.mvThemeCat_Core)
                d.add_theme_color(d.mvThemeCol_ButtonActive, darken(htr("list_background_color"),15), category=d.mvThemeCat_Core)
                d.add_theme_color(d.mvThemeCol_FrameBg, htr("button_alt_color"), category=d.mvThemeCat_Core)
                d.add_theme_color(d.mvThemeCol_FrameBgHovered, lighten(htr("button_alt_color"),10), category=d.mvThemeCat_Core)
                d.add_theme_color(d.mvThemeCol_FrameBgActive, htr("node_selected_color"), category=d.mvThemeCat_Core)
                d.add_theme_color(d.mvThemeCol_SliderGrab, htr("list_background_color"), category=d.mvThemeCat_Core)
                d.add_theme_color(d.mvThemeCol_SliderGrabActive, htr("node_wire_color"), category=d.mvThemeCat_Core)
                d.add_theme_color(d.mvThemeCol_ResizeGrip, darken(htr("window_background_color"),10), category=d.mvThemeCat_Core)
                d.add_theme_color(d.mvThemeCol_ResizeGripHovered, htr("node_selected_color"), category=d.mvThemeCat_Core)
                d.add_theme_color(d.mvThemeCol_ResizeGripActive, htr("node_selected_color"), category=d.mvThemeCat_Core)
                d.add_theme_color(d.mvThemeCol_CheckMark, htr("list_background_color"), category=d.mvThemeCat_Core)
    return global_theme