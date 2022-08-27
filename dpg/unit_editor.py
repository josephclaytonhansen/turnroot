import dearpygui.dearpygui as d
from ui_layout_helpers import *
from globals import globals as g
from ui_set_item_color import set_item_color
import unit_editor_callbacks as c
from viewport import EditorGlobals

def add_unit_editor(params={}):
    g.u = EditorGlobals()
    add_menu()
    build()
    make_functions()
    g.editors.append("unit_editor")
    
def build():
    line1 = PercentageBasedLayoutHelper(parent = "unit_editor")
    g.u.slider_int = line1.add_widget(d.add_slider_int(tag = "slider_int",
                                                       callback=c.basic), 25.0)
    line1.add_widget(d.add_text("This is a slider"), 75.0, False)
    line1.submit()

    line3 = PercentageBasedLayoutHelper(parent = "unit_editor")
    line3.add_widget(d.add_button(label="10%", tag="b5"), 10.0)
    line3.add_widget(d.add_button(label="20%", tag="b6"), 20.0)
    line3.add_widget(d.add_button(label="20%", tag="b7"), 20.0)
    line3.add_widget(d.add_button(label="50%", tag="b8"), 50.0)
    line3.submit()    
        
    for x in range(0,15):
        d.add_checkbox(parent = "unit_editor", 
                       label = "This is a checkbox",
                       tag = "checkbox"+str(x),
                       callback=c.basic)

def make_functions():
    set_item_color(g.u.slider_int, "button_alt_text_color")
    d.set_item_user_data("save", "user data")
    d.set_item_user_data("checkbox0", "user data")

def add_menu():
    with d.menu_bar(parent="unit_editor"):
        with d.menu(label="File"):
            d.add_menu_item(label="Save", callback=c.basic, tag="save")
            d.set_item_user_data("save", "user data")
            d.add_menu_item(label="Save As", callback=None)
    