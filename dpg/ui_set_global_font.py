import dearpygui.dearpygui as dpg
from globals import globals as g

def set_fonts(label="Assets/Fonts/FiraSans-Regular.ttf", mono="Assets/Fonts/FiraCode-Regular.ttf"):
    with dpg.font_registry():
        g.default_font = dpg.add_font(label, 20)
        g.monospace = dpg.add_font(mono, 20)
        dpg.bind_font(g.default_font)