import dearpygui.dearpygui as d
from globals import globals as g

def set_fonts(label="Assets/Fonts/FiraSans-Regular.ttf", mono="Assets/Fonts/FiraCode-Regular.ttf"):
    with d.font_registry():
        g.default_font = d.add_font(label, 20)
        g.monospace = d.add_font(mono, 20)
        d.bind_font(g.default_font)