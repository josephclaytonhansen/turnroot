import dearpygui.dearpygui as dpg
from globals import globals as g

def add_unit_editor(params={}):
    dpg.add_text("I am unit editor", parent="unit_editor")
    g.editors.append("unit_editor")