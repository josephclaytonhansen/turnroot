import dearpygui.dearpygui as dpg
from globals import globals as g

def set_fonts(label="Assets/Fonts/FiraSans-Regular.ttf", mono="Assets/Fonts/FiraCode-Regular.ttf"):
    with dpg.font_registry():
        default_font = dpg.add_font(label, 20)
        monospace = dpg.add_font(mono, 20)
        dpg.bind_font(default_font)