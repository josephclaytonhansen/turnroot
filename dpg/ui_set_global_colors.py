def set_colors(palette="ocean_waves"):
    import dearpygui.dearpygui as dpg
    from globals import globals as g

    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            wbc = g.color_theme.window_background_color.lstrip('#')
            wbc = tuple(int(wbc[i:i+2], 16) for i in (0, 2, 4))
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, wbc, category=dpg.mvThemeCat_Core)
            
    return global_theme