import dearpygui.dearpygui as d
from ui_layout_helpers import *
from globals import globals as g
from ui_set_item_color import set_item_color

def add_unit_editor(params={}):
    add_menu()
    g.editors.append("unit_editor")
    
    line1 = PercentageBasedLayoutHelper(parent = "unit_editor")
    slider_int = line1.add_widget(d.add_slider_int(tag = "slider_int"), 25.0)
    line1.add_widget(d.add_text("This is a slider"), 75.0, False)
    line1.submit()

    line3 = PercentageBasedLayoutHelper(parent = "unit_editor")
    line3.add_widget(d.add_button(label="10%", tag="b5"), 10.0)
    line3.add_widget(d.add_button(label="20%", tag="b6"), 20.0)
    line3.add_widget(d.add_button(label="20%", tag="b7"), 20.0)
    line3.add_widget(d.add_button(label="50%", tag="b8"), 50.0)
    line3.submit()
    
    set_item_color(slider_int, "button_alt_text_color")
    
    for x in range(0,15):
        d.add_checkbox(parent = "unit_editor", label = "This is a checkbox")
    
def add_menu():
        with d.menu_bar(parent="unit_editor"):
            with d.menu(label="File"):
                d.add_menu_item(label="Save", callback=None)
                d.add_menu_item(label="Save As", callback=None)
    