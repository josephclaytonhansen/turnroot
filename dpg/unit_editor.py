import dearpygui.dearpygui as dpg
from ui_layout_helpers import *
from globals import globals as g


def add_unit_editor(params={}):
    line1 = PercentageBasedLayoutHelper(parent = "unit_editor")
    line1.add_widget(dpg.add_button(label="25%", tag="b1"), 25.0)
    line1.add_widget(dpg.add_button(label="75%", tag="b2"), 75.0)
    line1.submit()

    line2 = PercentageBasedLayoutHelper(parent = "unit_editor")
    line2.add_widget(dpg.add_button(label="50%", tag="b3"), 50.0)
    line2.add_widget(dpg.add_button(label="50%", tag="b4"), 50.0)
    line2.submit()

    line3 = PercentageBasedLayoutHelper(parent = "unit_editor")
    line3.add_widget(dpg.add_button(label="25%", tag="b5"), 25.0)
    line3.add_widget(dpg.add_button(label="25%", tag="b6"), 25.0)
    line3.add_widget(dpg.add_button(label="50%", tag="b7"), 50.0)
    line3.submit()
    
    g.editors.append("unit_editor")
