import ui_colorthemes
import pathlib

class globals:
    editors = []
    color_theme = ui_colorthemes.charcoal_blue()
    corners_round = 5
    padding = 5
    item_spacing = 10
    window_padding = 25
    text_size = 18
    mono_text_size = 14
    debug = False
    font_family = "Assets/Fonts/FiraSans-Regular.ttf"
    autosave_time = 120
    current_height = 771
    now = 0
    timeout = 0
    fullscreen=True
    prefs = {"color_theme":color_theme.tag, 
             "corners_round":corners_round,
             "padding":padding,
             "item_spacing":item_spacing,
             "window_padding":window_padding,
             "text_size":text_size,
             "mono_text_size":mono_text_size,
             "font_family":font_family,
             "autosave_time":autosave_time,
             "fullscreen":fullscreen}