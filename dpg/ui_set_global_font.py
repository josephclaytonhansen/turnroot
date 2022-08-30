import dearpygui.dearpygui as d
from globals import globals as g
from editor_data_handling import LoadUserPrefs
LoadUserPrefs()
def set_fonts(label=g.font_family, mono="Assets/Fonts/FiraCode-Regular.ttf"):
    g.default_font = None
    g.font_sizes = []

    with d.font_registry():
        g.default_font = d.add_font(label, g.text_size)
        
        g.font_sizes = [
            d.add_font(label, int(g.text_size * 0.7)),
            d.add_font(label, int(g.text_size * 0.8)),
            d.add_font(label, int(g.text_size * 0.9)),
            d.add_font(label, int(g.text_size * 1.0)),
            d.add_font(label, int(g.text_size * 1.1)),
            d.add_font(label, int(g.text_size * 1.3)),
            d.add_font(label, int(g.text_size * 1.5)),
            d.add_font(label, int(g.text_size * 1.7)),
            d.add_font(label, int(g.text_size * 1.9)),
            d.add_font(label, int(g.text_size * 2.1)),
        ]
        g.monospace = d.add_font(mono, g.mono_text_size)
        d.bind_font(g.default_font)
        d.set_item_font("unit_editor", g.default_font)