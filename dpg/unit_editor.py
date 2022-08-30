import dearpygui.dearpygui as d
from ui_layout_helpers import *
from globals import globals as g
from game_options import game_options as go
from ui_item_style_helpers import *
import unit_editor_functions as c
from ui_tooltips import make_tooltip
from ui_colorthemes import colorthemes as themes

class Widgets():
    pwm = 2.26666
w = Widgets()

#remove this in favor of save/load, temporarily for dev
class Unit():
    is_generic = False
    is_avatar = False
    has_stats = True
u = Unit()

#you can only be editing one thing at a time, technically, so this works
g.is_editing = u

def add_unit_editor(params={}):
    buildUnitEditor()
    add_menu()
    populate()
    unit_editor_centers_in_column()
    make_functions()
    w.colors.set()
    g.editors.append("unit_editor")
    
    
def populate():
    left = g.unit_editor_left
    right = d.add_child_window(parent=g.unit_editor_right)
    w.left = left
    w.right = right
    
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
    
    d.add_spacer(height=g.item_spacing,parent=left)
    
    w.left_lower = d.add_child_window(parent=left)
    
    with d.collapsing_header(label="Basic attributes", parent=w.left_lower, default_open=True) as f:
        w.pronouns_row = Widgets()
        BuildTable(w.pronouns_row,[50,50], f)
        
        w.pronouns_label = d.add_text(parent=w.pronouns_row.columns[0], default_value="Pronouns")
        set_item_style(w.pronouns_label, 0, d.mvStyleVar_ItemSpacing)
        set_font_size(w.pronouns_label, -1)
        w.pronouns = d.add_combo(parent=w.pronouns_row.columns[0],
                    items=["He/him", "She/her", "They/them", "Custom pronouns"], width=-1)
        
        w.is_ = d.add_radio_button(go["unit_types"], callback=c.unit_type_pipe,
                                parent=w.pronouns_row.columns[1])

        set_item_style(w.is_, 0, d.mvStyleVar_FramePadding)
        t = d.add_button(label="What do these mean?", parent = w.pronouns_row.columns[1])
        set_font_size(t, -2)
        with d.tooltip(parent=t) as f:
            for ty in go["unit_types"]:
                u = d.add_text(default_value=g.tooltips.unit_editor[ty], parent =f)
                set_font_size(u, -2)
        
    with d.collapsing_header(label="Notes", parent=w.left_lower, default_open=False) as f:
        w.notes_row = Widgets()
        BuildTable(w.notes_row,[50,50], f)
        
        tmp = d.add_text(default_value="Notes\n(not added to game)",parent=w.notes_row.columns[0])
        set_font_size(tmp, -1)
        w.notes = d.add_input_text(multiline=True,parent=w.notes_row.columns[0],width=-1)
        
        tmp = d.add_text(default_value="Description\n(added to game as flavor text)",parent=w.notes_row.columns[1])
        w.desc = d.add_input_text(multiline=True,parent=w.notes_row.columns[1],width=-1)
        set_font_size(tmp, -1)
    
    #right side
    d.add_text(default_value="Stats", parent=right)
    with d.collapsing_header(label="Base stats", parent=right, default_open=True) as h:
        w.hp = d.add_input_int(label="HP", min_value=0, min_clamped=True, width=-g.text_size*6)
        w.strength = d.add_input_int(label="Strength", min_clamped=True, min_value=0, width=-g.text_size*6)
        w.speed = d.add_input_int(label="Speed", min_clamped=True, min_value=0, width=-g.text_size*6)
        w.defense = d.add_input_int(label="Defense", min_clamped=True, min_value=0, width=-g.text_size*6)
        w.resistance = d.add_input_int(label="Resistance", min_clamped=True, min_value=0, width=-g.text_size*6)
        w.magic = d.add_input_int(label="Magic", min_value=0, min_clamped=True, width=-g.text_size*6)
        w.luck = d.add_input_int(label="Luck", min_value=0, min_clamped=True, width=-g.text_size*6)
        w.charisma = d.add_input_int(label="Charisma", min_clamped=True, min_value=0, width=-g.text_size*6)
        w.skill = d.add_input_int(label="Skill", min_value=0, min_clamped=True, width=-g.text_size*6)
        w.dexterity = d.add_input_int(label="Dexterity", min_clamped=True, min_value=0, width=-g.text_size*6)
        
        d.add_spacer(height=g.item_spacing)
        
        w.base_stats_buttons_row = Widgets()
        BuildTable(w.base_stats_buttons_row,[50,50], h)
        
        w.compare_stats = d.add_button(label="Compare to other units", 
                     parent=w.base_stats_buttons_row.columns[0],width=-1)
        w.all_growth_stats =d.add_button(label="Stats + class stats", 
                     parent=w.base_stats_buttons_row.columns[1],width=-1)
        w.stat_variation =d.add_button(label="Stat variation", 
                     parent=w.base_stats_buttons_row.columns[1],width=-1, show=False)

        with d.tooltip(parent=w.compare_stats) as f:
            make_tooltip(g.tooltips.unit_editor, "Compare stats", f)
        with d.tooltip(parent=w.all_growth_stats) as f:
            make_tooltip(g.tooltips.unit_editor, "All growth stats", f)
            
    
            
class Colors():
    def set(self):
        set_item_color(w.font_size, "node_grid_background_color", d.mvThemeCol_FrameBg)
        set_item_colors(w.current_class, ["window_background_color", "button_alt_color"],
                        [d.mvThemeCol_Text, d.mvThemeCol_PopupBg])
        set_item_colors(w.pronouns, ["window_background_color", "button_alt_color"],
                        [d.mvThemeCol_Text, d.mvThemeCol_PopupBg])
        set_item_colors(w.theme_menu, ["window_background_color", "button_alt_color"],
                        [d.mvThemeCol_Text, d.mvThemeCol_PopupBg])
        set_item_color(w.name, "list_background_color")
        for x in [w.strength, w.hp, w.speed, w.defense,
                  w.magic, w.resistance, w.luck, w.charisma,
                  w.skill, w.dexterity, w.padding, w.window_padding,
                  w.item_spacing]:
            set_item_color(x, "node_grid_background_color", d.mvThemeCol_FrameBg)

        set_item_color(w.notes, "list_background_color")
        set_item_color(w.desc, "list_background_color")
w.colors = Colors()
   
def make_functions():
   d.set_item_user_data(w.theme_menu, w)
   d.set_item_user_data(w.font_size, w)

def add_menu():
    with d.menu_bar(parent="unit_editor"):
        with d.menu(label="File"):
            d.add_menu_item(label="Save", callback=c.basic, tag="save")
            d.set_item_user_data("save", "user data")
            d.add_menu_item(label="Save As", callback=None)
        with d.menu(label="View"):
            d.add_checkbox(label="Arrange Layout", callback=arrange, tag="arrange")
            d.add_checkbox(label="Re-size Columns", callback=resize, tag="resize", default_value=False)
            w.theme_menu_label = d.add_text("Color theme:")
            set_item_style(w.theme_menu_label, 0, d.mvStyleVar_ItemSpacing)
            set_font_size(w.theme_menu_label, -1)
            w.theme_menu = d.add_combo(default_value=g.color_theme.tag,
                                       items=[themes[t].tag for t in themes],
                                       callback=c.color_theme)
            w.font_size_label = d.add_text("Font size (requires restart)")
            set_font_size(w.font_size_label, -1)
            set_item_style(w.font_size_label, 0, d.mvStyleVar_ItemSpacing)
            w.font_size = d.add_input_int(min_clamped=True,max_clamped=True,
                                          min_value=4,max_value=36,
                                          callback=c.font_size, default_value=g.text_size)
            w.padding_label = d.add_text("Padding/Item Spacing/Window Padding")
            set_font_size(w.padding_label, -1)
            set_item_style(w.padding_label, 0, d.mvStyleVar_ItemSpacing)
            
            with d.group(horizontal=True,width=80):
                w.padding = d.add_input_int(min_clamped=True,max_clamped=True,
                                          min_value=0,max_value=30,step=0,
                                          callback=c.padding, default_value=g.padding)
                w.item_spacing = d.add_input_int(min_clamped=True,max_clamped=True,
                                          min_value=0,max_value=30,step=0,
                                          callback=c.item_spacing, default_value=g.item_spacing)
                w.window_padding = d.add_input_int(min_clamped=True,max_clamped=True,
                                          min_value=0,max_value=30,step=0,
                                          callback=c.window_padding, default_value=g.window_padding)
            
            
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

def arrange():
    if g.is_arranging:
        g.is_arranging = False
        ue_no_arrange()
    else:
        g.is_arranging = True
        ue_arrange()
        
def ue_arrange():
    d.configure_item(g.unit_editor_table, header_row=True, reorderable=True, resizable=g.can_resize_columns)

def ue_no_arrange():
    d.configure_item(g.unit_editor_table, header_row=False, reorderable=True, resizable=g.can_resize_columns)

def resize():
    if g.can_resize_columns:
        g.can_resize_columns = False
        d.configure_item(g.unit_editor_table, resizable=False)
    else:
        g.can_resize_columns = True
        d.configure_item(g.unit_editor_table, resizable=True)
    
def ue_do():
    if g.is_editing.is_generic == True:
        c.show_stat_variation(w)
    else:
        c.hide_stat_variation(w)
    if g.is_editing.is_avatar == True:
        pass
    if g.is_editing.has_stats == True:
        c.show_stats(w)
    else:
        c.hide_stats(w)
    