import dearpygui.dearpygui as d
from ui_layout_helpers import *
from globals import globals as g
from ui_set_item_color import set_item_color

def add_unit_editor(params={}):
    add_menu()
    g.editors.append("unit_editor")
    
    line1 = PercentageBasedLayoutHelper(parent = "unit_editor")
    line1.add_widget(d.add_button(label="25%", tag="b1"), 25.0)
    line1.add_widget(d.add_button(label="75%", tag="b2"), 75.0)
    line1.submit()

    line2 = PercentageBasedLayoutHelper(parent = "unit_editor")
    line2.add_widget(d.add_button(label="50%", tag="b3"), 50.0)
    line2.add_widget(d.add_button(label="50%", tag="b4"), 50.0)
    line2.submit()

    line3 = PercentageBasedLayoutHelper(parent = "unit_editor")
    line3.add_widget(d.add_button(label="25%", tag="b5"), 25.0)
    line3.add_widget(d.add_button(label="25%", tag="b6"), 25.0)
    line3.add_widget(d.add_button(label="50%", tag="b7"), 50.0)
    line3.submit()
    
    with d.group(horizontal=True, parent="unit_editor"):
        slider_int = d.add_slider_int(width=100)
        d.add_text("This is a slider")
    
    set_item_color(slider_int, "button_alt_text_color")
    
    with d.group(horizontal=True, parent="unit_editor"):
        d.add_checkbox(parent = "unit_editor", label = "This is a checkbox")
    
def add_menu():
        with d.menu_bar(parent="unit_editor"):
            with d.menu(label="File"):
                d.add_menu_item(label="Save", callback=None)
                d.add_menu_item(label="Save As", callback=None)
    