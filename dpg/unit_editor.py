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
g.active_window_widgets = w

#remove this in favor of save/load, temporarily for dev
class Unit():
    is_generic = False
    is_avatar = False
    has_stats = True
    base_stats = {}
    growth_rates = {}
    
u = Unit()

#you can only be editing one thing at a time, technically, so this works
g.is_editing = u

def add_unit_editor(params={}):
    buildUnitEditor()
    populate()
    add_menu()
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
        tmp = d.add_text("Ctrl+Click to enter a value with your keyboard")
        set_item_style(tmp, 0, d.mvStyleVar_FramePadding)
        set_font_size(tmp, -2)
        
        w.hp = d.add_slider_int(label="HP", min_value=0, max_value=50, clamped=True,callback=c.ChangeBaseStat)
        w.strength = d.add_slider_int(label="Strength", max_value=50, clamped=True, min_value=0,callback=c.ChangeBaseStat)
        w.speed = d.add_slider_int(label="Speed", clamped=True,max_value=50,  min_value=0,callback=c.ChangeBaseStat)
        w.defense = d.add_slider_int(label="Defense", clamped=True,max_value=50, min_value=0,callback=c.ChangeBaseStat)
        w.resistance = d.add_slider_int(label="Resistance", max_value=50,clamped=True, min_value=0,callback=c.ChangeBaseStat)
        w.magic = d.add_slider_int(label="Magic", min_value=0, max_value=50,clamped=True,callback=c.ChangeBaseStat)
        w.luck = d.add_slider_int(label="Luck", min_value=0, max_value=50,clamped=True,callback=c.ChangeBaseStat)
        w.charisma = d.add_slider_int(label="Charisma", max_value=50,clamped=True, min_value=0,callback=c.ChangeBaseStat)
        w.skill = d.add_slider_int(label="Skill", min_value=0, max_value=50,clamped=True,callback=c.ChangeBaseStat)
        w.dexterity = d.add_slider_int(label="Dexterity", max_value=50,clamped=True, min_value=0,callback=c.ChangeBaseStat)
        
        t = d.add_button(label="What about inheritance?")
        set_font_size(t, -2)
        with d.tooltip(parent=t) as f:
            u = d.add_text(default_value=g.tooltips.unit_editor["what_about_inheritance"], parent =f)
            set_font_size(u, -2)
        
        d.add_spacer(height=g.item_spacing)
        
        tmp = Widgets()
        BuildTable(tmp,[50,50], h)
        
        w.compare_stats = d.add_button(label="Compare to other units", 
                     parent=tmp.columns[0],width=-1)
        w.all_growth_stats =d.add_button(label="Stats + class stats", 
                     parent=tmp.columns[1],width=-1)
        w.stat_variation =d.add_button(label="Stat variation", 
                     parent=tmp.columns[1],width=-1, show=False)

        with d.tooltip(parent=w.compare_stats) as f:
            make_tooltip(g.tooltips.unit_editor, "Compare stats", f)
        with d.tooltip(parent=w.all_growth_stats) as f:
            make_tooltip(g.tooltips.unit_editor, "All growth stats", f)
    
    with d.collapsing_header(label="Growth rates", parent=right, default_open=False) as h:
        tmp = d.add_text("Ctrl+Click to enter a value with your keyboard")
        set_item_style(tmp, 0, d.mvStyleVar_FramePadding)
        set_font_size(tmp, -2)
        
        w.hp_base_rate = d.add_slider_int(clamped=True, min_value=0,max_value=100,label="HP",callback=c.ChangeBaseStatGrowth,format="%d%%")
        w.strength_base_rate = d.add_slider_int(clamped=True, min_value=0,max_value=100,label="Strength",callback=c.ChangeBaseStatGrowth,format="%d%%")
        w.speed_base_rate = d.add_slider_int(clamped=True, min_value=0,max_value=100,label="Speed",callback=c.ChangeBaseStatGrowth,format="%d%%")
        w.defense_base_rate = d.add_slider_int(clamped=True, min_value=0,max_value=100,label="Defense",callback=c.ChangeBaseStatGrowth,format="%d%%")
        w.resistance_base_rate = d.add_slider_int(clamped=True, min_value=0,max_value=100,label="Resistance",callback=c.ChangeBaseStatGrowth,format="%d%%")
        w.magic_base_rate = d.add_slider_int(clamped=True, min_value=0,max_value=100,label="Magic",callback=c.ChangeBaseStatGrowth,format="%d%%")
        w.luck_base_rate = d.add_slider_int(clamped=True, min_value=0,max_value=100,label="Luck",callback=c.ChangeBaseStatGrowth,format="%d%%")
        w.charisma_base_rate = d.add_slider_int(clamped=True, min_value=0,max_value=100,label="Charisma",callback=c.ChangeBaseStatGrowth,format="%d%%")
        w.skill_base_rate = d.add_slider_int(clamped=True, min_value=0,max_value=100,label="Skill",callback=c.ChangeBaseStatGrowth,format="%d%%")
        w.dexterity_base_rate = d.add_slider_int(clamped=True, min_value=0,max_value=100,label="Dexterity",callback=c.ChangeBaseStatGrowth,format="%d%%")
        
        d.add_spacer(height=g.item_spacing)
        
        tmp = Widgets()
        BuildTable(tmp,[50,50], h)
        
        w.test_growth = d.add_button(label="Test stat growth", 
                     parent=tmp.columns[0],width=-1, callback=c.TestGrowth)
        
    
            
class Colors():
    def set(self):
        set_item_color(w.font_size, "node_grid_background_color", d.mvThemeCol_FrameBg)
        
        for x in [w.current_class, w.pronouns, w.theme_menu, w.font]:
            set_item_colors(x, ["window_background_color", "button_alt_color"],
                        [d.mvThemeCol_Text, d.mvThemeCol_PopupBg])
            
        set_item_color(w.name, "list_background_color")
        
        for x in [w.strength, w.hp, w.speed, w.defense,
                  w.magic, w.resistance, w.luck, w.charisma,
                  w.skill, w.dexterity, w.padding, w.window_padding,
                  w.item_spacing, w.corners_round,
                  w.hp_base_rate, w.strength_base_rate,
                  w.speed_base_rate, w.defense_base_rate,
                  w.resistance_base_rate, w.magic_base_rate,
                  w.luck_base_rate, w.charisma_base_rate,
                  w.skill_base_rate, w.dexterity_base_rate]:
            set_item_colors(x, ["window_background_color", "window_background_color", "list_background_color"],
                        [d.mvThemeCol_FrameBg, d.mvThemeCol_FrameBgHovered, d.mvThemeCol_FrameBgActive])

        set_item_color(w.notes, "list_background_color")
        set_item_color(w.desc, "list_background_color")
w.colors = Colors()
   
def make_functions():
   d.set_item_user_data(w.theme_menu, w)
   d.set_item_user_data(w.font_size, w)
   
   d.set_item_user_data(w.hp, "hp")
   d.set_item_user_data(w.strength, "strength")
   d.set_item_user_data(w.speed, "speed")
   d.set_item_user_data(w.defense, "defense")
   d.set_item_user_data(w.resistance, "resistance")
   d.set_item_user_data(w.magic, "magic")
   d.set_item_user_data(w.luck, "luck")
   d.set_item_user_data(w.charisma, "charisma")
   d.set_item_user_data(w.skill, "skill")
   d.set_item_user_data(w.dexterity, "dexterity")
   
   d.set_item_user_data(w.hp_base_rate, "hp")
   d.set_item_user_data(w.strength_base_rate, "strength")
   d.set_item_user_data(w.speed_base_rate, "speed")
   d.set_item_user_data(w.defense_base_rate, "defense")
   d.set_item_user_data(w.resistance_base_rate, "resistance")
   d.set_item_user_data(w.magic_base_rate, "magic")
   d.set_item_user_data(w.luck_base_rate, "luck")
   d.set_item_user_data(w.charisma_base_rate, "charisma")
   d.set_item_user_data(w.skill_base_rate, "skill")
   d.set_item_user_data(w.dexterity_base_rate, "dexterity")

def add_menu():
    w.status_bar = None
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
            w.font_size_label = d.add_text("Font size/Font (requires restart)")
            set_font_size(w.font_size_label, -1)
            set_item_style(w.font_size_label, 0, d.mvStyleVar_ItemSpacing)
            
            with d.group(horizontal=True):
                w.font_size = d.add_input_int(min_clamped=True,max_clamped=True,
                                            min_value=4,max_value=36, step =0, width = 30,
                                            callback=c.font_size, default_value=g.text_size)
                w.font = d.add_combo(items=["FiraCode","FiraSans","Montserrat","NotoSans"],callback=c.font,width=-1,
                                     default_value=g.font_family.split("/")[2].split("-")[0])
            
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
            
            w.corners_round_label = d.add_text("Corners rounded amount")
            set_font_size(w.corners_round_label, -1)
            set_item_style(w.corners_round_label, 0, d.mvStyleVar_ItemSpacing)
            
            w.corners_round = d.add_slider_int(clamped=True,
                                            min_value=0,max_value=10,
                                            callback=c.corners_round, default_value=g.corners_round)
        
        w.info_left = d.add_spacer(width=0)
        with d.menu(label="",enabled=False) as w.status_bar:
            pass
            
            
def unit_editor_update_height():
    d.configure_item(w.info_left, width=d.get_viewport_width()-500)
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
    try:
        if g.now > g.timeout:
            d.configure_item(w.status_bar, label="")
    except:
        d.configure_item(w.status_bar, label="")
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
    