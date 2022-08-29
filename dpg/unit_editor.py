from ctypes import alignment
from subprocess import call
import dearpygui.dearpygui as d
from ui_layout_helpers import *
from globals import globals as g
from ui_item_style_helpers import *
import unit_editor_callbacks as c
from ui_tooltips import make_tooltip

class Widgets():
    pwm = 2.26666

w = Widgets()

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
        w.left_portrait_spacing = d.add_spacer(width=0,height = 400)
        w.portrait = d.add_image_button(
            height = 400, 
            width=300, 
            texture_tag=ImageToTexture("assets/ui_graphics/portrait_editor_placeholder.png"
                                                                ))
        with d.tooltip(parent=w.portrait) as f:
            make_tooltip(g.tooltips.unit_editor, "Portrait button", f)

    #Use this format for a percentage-based row: create a Widgets() row, then BuildTable()
    w.name_row = Widgets()
    BuildTable(w.name_row,[55,35,10],left)
    
    #d.add_spacer(parent=w.name_row.columns[0], height = int((0.466 * (g.padding*2 + g.text_size)/2)))
    
    i = -1
    for x in ["Unit name", "Current class"]:
        i +=1
        tmp = d.add_text(parent=w.name_row.columns[i], default_value=x)
        #set padding to 0
        set_item_style(tmp, 0, d.mvStyleVar_ItemSpacing)
        set_font_size(tmp, -1)
        with d.tooltip(parent=tmp) as f:
            make_tooltip(g.tooltips.unit_editor, x, f)
    
    w.name = d.add_input_text(parent=w.name_row.columns[0], callback=c.basic, hint="Unit Name",width=-1,height =-1)
    set_font_size(w.name, 1)
    
    w.current_class = d.add_combo(parent=w.name_row.columns[1], callback=c.basic, items=["Myrmidon", "Assassin"], width=-1)
    set_font_size(w.current_class, 1)
    d.add_image_button(parent=w.name_row.columns[2],texture_tag=ImageToTexture("assets/ui_icons/white/edit.png"))
            
def make_functions():
   set_item_colors(w.current_class, ["window_background_color", "button_alt_color"],
                   [d.mvThemeCol_Text, d.mvThemeCol_PopupBg])
   set_item_color(w.name, "list_background_color")
   d.set_item_user_data("save", "user data")

def add_menu():
    with d.menu_bar(parent="unit_editor"):
        with d.menu(label="File"):
            d.add_menu_item(label="Save", callback=c.basic, tag="save")
            d.set_item_user_data("save", "user data")
            d.add_menu_item(label="Save As", callback=None)
    
def unit_editor_update_height():
    for row in g.unit_editor_rows:
            d.configure_item(row, 
                             height=int(g.current_height/len(g.unit_editor_rows)-(g.window_padding*2)-30)
                             )

def center_in_column(n, spacer, width):
    p = 1/n
    w.column_width = (p-(g.item_spacing/170))* d.get_viewport_width()
    w.column_width_p = w.column_width / d.get_viewport_width()
    w.pwm = 1 / w.column_width_p 
    d.configure_item(spacer, width=int((w.column_width-width)/2)-g.item_spacing*2)

def unit_editor_centers_in_column():
    center_in_column(
        2, w.left_portrait_spacing, 300
    )

def ue_arrange():
    d.configure_item(w.unit_editor_table, header_row=True, reorderable=True)

def ue_no_arrange():
    d.configure_item(w.unit_editor_table, header_row=False, reorderable=False)
    