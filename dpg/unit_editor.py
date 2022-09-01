import dearpygui.dearpygui as d
from ui_layout_helpers import *
from globals import globals as g
from game_options import game_options as go
from ui_item_style_helpers import *
import unit_editor_functions as c
from ui_tooltips import make_tooltip
from ui_colorthemes import colorthemes as themes
from editor_save_load_unit import LoadUnit, SaveUnit
from ui_set_global_colors import htr
from ui_unit_editor_populates import *
import sys

g.active_window_widgets = w

class Unit():
    is_generic = False
    is_avatar = False
    has_stats = True
    base_stats = {}
    growth_rates = {}
    name = ""
    pronouns = ""
    unit_type = ""
    current_class = ""
    notes = ""
    description = ""

def add_unit_editor(params={}):
    buildUnitEditorAttributes()
    populateAttributes()
    buildUnitEditorAffinities()
    populateAffinities()
    add_menu()
    unit_editor_centers_in_column()
    make_functions()
    w.colors.set()
    g.editors.append("unit_editor")
    #remove this in favor of save/load, temporarily for dev
    u = Unit()
    #you can only be editing one thing at a time, technically, so this works
    g.is_editing = u
    g.is_editing.type = "unit"
    g.path = ""
    TimedEvent(g.autosave_time)
            
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
                  w.item_spacing, w.corners_round, w.autosave,
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
            d.add_menu_item(label="Open", tag="open", callback=c.ShowFileDialog)
            d.add_menu_item(label="New", tag="new", callback=c.NewUnitFile)
            d.add_menu_item(label="Save", callback=lambda:(SaveUnit(g.path),TimedInfoMessage("Unit saved", w.status_bar, 2)), tag="save")
            d.set_item_user_data("save", "user data")
            d.add_menu_item(label="Save As", callback=c.ShowFileDialog)
            d.add_menu_item(label="Exit", callback=lambda:sys.exit())
            
        with d.menu(label="View"):
            d.add_checkbox(label="Fullscreen", callback=fullscreen, tag="fullscreen", default_value=True)
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
            
            w.autosave_label = d.add_text("Autosave interval (in seconds)")
            set_font_size(w.autosave_label, -1)
            set_item_style(w.autosave_label, 0, d.mvStyleVar_ItemSpacing)
            
            w.autosave = d.add_input_int(min_clamped=True,max_clamped=True,
                                          min_value=15,max_value=600,step=15,
                                          callback=c.ChangeAutosave, default_value=g.autosave_time)
        
        w.info_left = d.add_spacer(width=0)
        with d.menu(label="",enabled=False) as w.status_bar:
            pass
            
            
def unit_editor_update_height():
    d.configure_item(w.info_left, width=d.get_viewport_width()-500)
    for row in g.unit_editor_rows:
            d.configure_item(row, 
                             height=int(g.current_height/len(g.unit_editor_rows)-(g.window_padding*6))
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

def fullscreen():
    g.fullscreen = not g.fullscreen
    d.toggle_viewport_fullscreen()
    d.set_viewport_pos([0,0])

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
        if g.now > g.timeout_event:
            TimedEvent(g.autosave_time)
            TimedInfoMessage("Auto-saved", w.status_bar, 2)
            SaveUnit(g.path)
    except:
        pass

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
    