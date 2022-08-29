from subprocess import call
import dearpygui.dearpygui as d
from ui_layout_helpers import *
from globals import globals as g
from ui_set_item_color import set_item_color
import unit_editor_callbacks as c

def add_unit_editor(params={}):
    add_menu()
    buildUnitEditor()
    populate()
    unit_editor_centers_in_column()
    make_functions()
    g.editors.append("unit_editor")
    
    
def populate():
    left = g.unit_editor_left
    right = g.unit_editor_right
    
    #use this format (group, spacer, item) to center something of fixed width in a column
    #don't forget to add it to unit_editor_centers_in_column()
    with d.group(horizontal=True, parent=left):
        g.unit_editor_left_spacing = d.add_spacer(width=0,height = 400)
        d.add_button(height = 400, width=300)
    
    #for things that don't have to be fixed width, use a PercentageBasedLayoutHelper
    line1 = PercentageBasedLayoutHelper(parent = left)
    g.u.slider_int = line1.add_widget(d.add_slider_int(tag = "slider_int",
                                                       callback=c.basic), 30.0)
    line1.add_widget(d.add_text("These are sliders"), 20.0, False)
    g.u.slider_int2 = line1.add_widget(d.add_slider_int(tag = "slider_int2",
                                                       callback=c.basic), 30.0)
    line1.submit()
    
    for x in range(0, 30):
        d.add_checkbox(parent=right, tag = "checkbox"+str(x), label = "checkbox"+str(x), callback=c.basic)
            
def make_functions():
    set_item_color(g.u.slider_int, "button_alt_text_color")
    set_item_color(g.u.slider_int2, "button_alt_text_color")
    d.set_item_user_data("save", "user data")

def add_menu():
    with d.menu_bar(parent="unit_editor"):
        with d.menu(label="File"):
            d.add_menu_item(label="Save", callback=c.basic, tag="save")
            d.set_item_user_data("save", "user data")
            d.add_menu_item(label="Save As", callback=None)
    
def unit_editor_update_height():
    for row in g.unit_editor_rows:
            d.configure_item(row, height=int(g.current_height/len(g.unit_editor_rows)-(g.window_padding*2)-30))

def center_in_column(n, spacer, width):
    p = 1/n
    left_width = (p-(g.item_spacing/170))* d.get_viewport_width()
    d.configure_item(spacer, width=int((left_width-width)/2)-g.item_spacing*2)

def unit_editor_centers_in_column():
    center_in_column(
        2, g.unit_editor_left_spacing, 300
    )

def ue_arrange():
    d.configure_item(g.unit_editor_table, header_row=True, reorderable=True)

def ue_no_arrange():
    d.configure_item(g.unit_editor_table, header_row=False, reorderable=False)
    