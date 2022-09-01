from globals import globals as g
from ui_colorthemes import colorthemes as themes
from ui_set_global_colors import set_colors, htr, darken
from ui_set_global_font import set_fonts
import dearpygui.dearpygui as d
from editor_data_handling import SaveUserPrefs
from ui_item_style_helpers import *
from ui_layout_helpers import TimedInfoMessage, BuildTable
from editor_save_load_unit import SaveUnit, LoadUnit
import random

def basic(sender, app_data, user_data):
    print(sender, app_data, user_data)

def unit_type_pipe(sender, app_data, user_data):
    g.is_editing.unit_type = app_data
    try:
        if app_data == "Generic Unit":
            g.is_editing.is_generic = True
            g.is_editing.is_avatar = False
            g.is_editing.has_stats = True
        elif app_data == "Avatar/Player Character":
            g.is_editing.is_generic = False
            g.is_editing.is_avatar = True
            g.is_editing.has_stats = True
        elif app_data == "NPC":
            g.is_editing.is_generic = True
            g.is_editing.is_avatar = True
            g.is_editing.has_stats = False
        else:
            g.is_editing.is_generic = False
            g.is_editing.is_avatar = False
            g.is_editing.has_stats = True
        return True
    except:
        return False

def show_stat_variation(widgets):
    d.configure_item(widgets.stat_variation, show=True)

def hide_stat_variation(widgets):
    d.configure_item(widgets.stat_variation, show=False)

def show_stats(widgets):
    d.configure_item(widgets.right, show=True)

def hide_stats(widgets):
    d.configure_item(widgets.right, show=False)
    
def color_theme(sender, app_data, user_data):
    g.color_theme = themes[app_data]
    d.bind_theme(set_colors(g.color_theme))
    user_data.colors.set()
    SaveUserPrefs()

def font_size(sender, app_data, user_data):
    g.text_size = app_data
    set_fonts()
    SaveUserPrefs()
    TimedInfoMessage("Requires restart- no changes will be visible", g.active_window_widgets.status_bar)

def font(sender, app_data, user_data):
    g.font_family = app_data
    set_fonts(label="Assets/Fonts/"+app_data+"-Regular.ttf")
    SaveUserPrefs()
    TimedInfoMessage("Requires restart- no changes will be visible", g.active_window_widgets.status_bar)
    
def window_padding(sender, app_data, user_data):
    g.window_padding = app_data
    d.bind_theme(set_colors(g.color_theme))
    SaveUserPrefs()

def corners_round(sender, app_data, user_data):
    g.corners_round = app_data
    d.bind_theme(set_colors(g.color_theme))
    SaveUserPrefs()

def padding(sender, app_data, user_data):
    g.padding = app_data
    d.bind_theme(set_colors(g.color_theme))
    SaveUserPrefs()

def ChangeAutosave(sender, app_data, user_data):
    g.autosave_time = app_data
    d.bind_theme(set_colors(g.color_theme))
    SaveUserPrefs()

def item_spacing(sender, app_data, user_data):
    g.item_spacing = app_data
    d.bind_theme(set_colors(g.color_theme))
    SaveUserPrefs()

def ChangeBaseStatGrowth(sender, app_data, user_data):
    g.is_editing.growth_rates[user_data] = app_data

def ChangeBaseStat(sender, app_data, user_data):
    g.is_editing.base_stats[user_data] = app_data
    
def ChangeName(sender, app_data, user_data):
    g.is_editing.name = app_data

def ChangeCurrentClass(sender, app_data, user_data):
    g.is_editing.current_class = app_data

def ChangePronouns(sender, app_data, user_data):
    g.is_editing.pronouns = app_data

def ChangeNotes(sender, app_data, user_data):
    g.is_editing.notes = app_data

def ChangeDescription(sender, app_data, user_data):
    g.is_editing.description = app_data

def ShowFileDialog(sender, app_data, user_data):
    if sender == "open":
        d.show_item("UnitSelect")
        d.set_item_user_data("UnitSelect", "open")
    else:
        d.show_item("UnitSelect")
        d.set_item_user_data("UnitSelect", "save")

def GetUnitFile(sender, app_data, user_data):
    g.path = app_data["file_path_name"]
    if user_data == "open":
        LoadFromFile()
    else:
        SaveToFile()

def LoadFromFile():
    LoadUnit(g.path)
    UseLoadedData(Widgets = g.active_window_widgets, path = g.path)

def NewUnitFile():
    g.path = ""
    g.is_editing.is_generic = False
    g.is_editing.is_avatar = False
    g.is_editing.has_stats = True
    g.is_editing.base_stats = {}
    g.is_editing.growth_rates = {}
    g.is_editing.name = ""
    g.is_editing.pronouns = ""
    g.is_editing.unit_type = ""
    g.is_editing.current_class = ""
    g.is_editing.notes = ""
    g.is_editing.description = ""
    for bs in [g.active_window_widgets.hp, g.active_window_widgets.strength, g.active_window_widgets.speed, g.active_window_widgets.defense,
                  g.active_window_widgets.resistance, g.active_window_widgets.luck, g.active_window_widgets.magic, g.active_window_widgets.charisma,
                  g.active_window_widgets.skill, g.active_window_widgets.dexterity]:
        d.set_value(bs, 0)
    for gr in [g.active_window_widgets.hp_base_rate, g.active_window_widgets.strength_base_rate, g.active_window_widgets.speed_base_rate, g.active_window_widgets.defense_base_rate,
                  g.active_window_widgets.resistance_base_rate, g.active_window_widgets.luck_base_rate, g.active_window_widgets.magic_base_rate, g.active_window_widgets.charisma_base_rate,
                  g.active_window_widgets.skill_base_rate, g.active_window_widgets.dexterity_base_rate]: 
        d.set_value(gr, 0)
        d.set_value(g.active_window_widgets.name, g.is_editing.name)
        d.set_value(g.active_window_widgets.pronouns, g.is_editing.pronouns)
        d.set_value(g.active_window_widgets.current_class, g.is_editing.current_class)
        d.set_value(g.active_window_widgets.is_, g.is_editing.unit_type)
        d.set_value(g.active_window_widgets.notes, g.is_editing.notes)
        d.set_value(g.active_window_widgets.desc, g.is_editing.description)
        

def SaveToFile():
    SaveUnit(g.path)

class Widgets():
    use_class_stats = False

w = Widgets()
w.ignore_hp = False
def ignoreHP():
    w.ignore_hp = not w.ignore_hp
    largest_value = 0
    for stat in ["hp", "strength", "speed",
                 "magic","resistance", "defense",
                 "luck", "skill", "dexterity", "charisma"]:
        for x in g.is_editing.stat_data.keys():
            for y in g.is_editing.stat_data[x]:
                if w.ignore_hp and x.lower() == "hp":
                    pass
                else:
                    if y > largest_value:
                        largest_value = y
        
        d.set_axis_limits("y_axis", 0, largest_value)

def GrowOnce():
    if not w.use_class_stats:
        g.is_editing.datax.append(g.is_editing.datax[-1]+1)
        for stat in ["hp", "strength", "speed",
                    "magic","resistance", "defense",
                    "luck", "skill", "dexterity", "charisma"]:
            
            try:
                threshold = g.is_editing.growth_rates[stat]
            except:
                threshold = 0
            
            try:
                baseline = g.is_editing.base_stats[stat]
                if baseline < g.is_editing.stat_data[stat][-1]:
                    baseline = g.is_editing.stat_data[stat][-1]
            except Exception as e:
                if 0 < g.is_editing.stat_data[stat][-1]:
                    baseline = g.is_editing.stat_data[stat][-1]
                else:
                    baseline = 0
            
            growth = random.random() * 100

            if growth <= threshold: 
                g.is_editing.stat_data[stat].append(baseline+1)
            else:
                g.is_editing.stat_data[stat].append(baseline)
            d.set_value("growth"+stat.upper(), [g.is_editing.datax,g.is_editing.stat_data[stat]])
            d.set_axis_limits("x_axis", 0, len(g.is_editing.datax))
            
            largest_value = 0
            for x in g.is_editing.stat_data.keys():
                for y in g.is_editing.stat_data[x]:
                    if w.ignore_hp and x.lower() == "hp":
                        pass
                    else:
                        if y > largest_value:
                            largest_value = y
            
            d.set_axis_limits("y_axis", 0, largest_value)
            d.set_value("current_stat"+stat, str(g.is_editing.stat_data[stat][-1])+": up +"+
                        str(g.is_editing.stat_data[stat][-1]-g.is_editing.stat_data[stat][0])+" from base")
            
    else:
        pass #class stats are not yet implemented
            
def TestGrowthUseClassStats():
    w.use_class_stats = True
    
def TestGrowth():
    stat_data = {}
    for stat in ["hp", "strength", "speed",
                 "magic","resistance", "defense",
                 "luck", "skill", "dexterity", "charisma"]:
        try: 
            stat_data[stat]=[]
            stat_data[stat].append(g.is_editing.base_stats[stat])
        except:
            stat_data[stat]=[]
            stat_data[stat].append(0)

    g.is_editing.datax = [0]

    g.is_editing.stat_data = stat_data

    try: d.show_item("Growth")
    except:
        with d.window(label="Stat Growth Testing", tag = "Growth", height=800, width=1000, no_close=True, no_title_bar=False, no_collapse=True) as fi:
            tmp = Widgets()
            BuildTable(tmp,[65,35], fi)
            d.add_button(parent=tmp.columns[1],label="Close and reset",callback=lambda:(d.hide_item(fi)))
            d.set_item_pos(fi, [(d.get_viewport_width()-1000)/2, (d.get_viewport_height()-700)/2])
            
            with d.theme() as item_theme:
                with d.theme_component(d.mvAll):
                    d.add_theme_color(d.mvThemeCol_FrameBg, darken(htr("node_grid_background_color"),15), category=d.mvThemeCat_Core)
                    d.add_theme_color(d.mvPlotCol_PlotBg, darken(htr("node_grid_background_color"),30), category=d.mvThemeCat_Plots)
                    d.add_theme_style(d.mvPlotStyleVar_LineWeight, 3, category=d.mvThemeCat_Plots)
                    

            d.bind_item_theme(fi, item_theme)
        
            # create plot
            with d.plot(label="Line Series", width=-1, height=600, parent=tmp.columns[0], query=False, no_box_select=True) as f:
                d.add_plot_legend()
                # REQUIRED: create x and y axes
                d.add_plot_axis(d.mvXAxis, label="Times leveled up", tag ="x_axis")
                d.add_plot_axis(d.mvYAxis, label="Stat value", tag="y_axis")
            
                right = Widgets()
                BuildTable(right,[50,50], tmp.columns[1])
                
                # series belong to a y axis
                for stat in ["hp", "strength", "speed",
                    "magic","resistance", "defense",
                    "luck", "skill", "dexterity", "charisma"]:
                    d.add_line_series(g.is_editing.datax, stat_data[stat], label=stat.upper(), parent="y_axis", tag="growth"+stat.upper())
                    
                    d.add_text(parent=right.columns[0],default_value=stat)
                    d.add_text(parent=right.columns[1],default_value="-",tag="current_stat"+stat)
                    
                d.set_axis_limits("x_axis", 0, len(g.is_editing.datax))
            d.show_item("growthHP")
            
            wo = d.add_button(parent=tmp.columns[0],label="Test level up", callback=GrowOnce,width=-1)
            set_font_size(wo, 2)
        
            
            d.add_button(parent=tmp.columns[0],width=-1,label="Hide HP",
                         tag = "hidehp", callback=lambda:(d.hide_item("growthHP"),d.hide_item("hidehp"),d.show_item("showhp"),ignoreHP()))
            d.add_button(parent=tmp.columns[0],width=-1,label="Show HP",
                         tag = "showhp", callback=lambda:(d.show_item("growthHP"),d.hide_item("showhp"),d.show_item("hidehp"),ignoreHP()))
            d.hide_item("showhp")
            
            tmp = d.add_text("Right click to see graph options",parent=tmp.columns[0])
            set_item_style(tmp, 0, d.mvStyleVar_FramePadding)
            set_font_size(tmp, -2)
    
def UseLoadedData(Widgets, path):
    data = g.is_editing
    base_stats = data.base_stats
    growth_rates = data.growth_rates
    
    w = Widgets
    
    try:
        d.set_value(w.name, data.name)
        d.set_value(w.pronouns, data.pronouns)
        d.set_value(w.current_class, data.current_class)
        d.set_value(w.is_, data.unit_type)
        d.set_value(w.notes, data.notes)
        d.set_value(w.desc, data.description)
        
    except Exception as e:
        print(e)
    
    keys = ["hp", "strength", "speed", "defense", "resistance", "luck", "magic", "charisma", "skill", "dexterity"]
    i = -1
    for bs in [w.hp, w.strength, w.speed, w.defense,
                  w.resistance, w.luck, w.magic, w.charisma,
                  w.skill, w.dexterity]: 
        i+=1 
        try:
            d.set_value(bs, base_stats[keys[i]])
        except:
            d.set_value(bs, 0)
            base_stats[keys[i]] = 0
        
    i = -1
    for gr in [w.hp_base_rate, w.strength_base_rate, w.speed_base_rate, w.defense_base_rate,
                  w.resistance_base_rate, w.luck_base_rate, w.magic_base_rate, w.charisma_base_rate,
                  w.skill_base_rate, w.dexterity_base_rate]: 
        i+=1 
        try:
            d.set_value(gr, growth_rates[keys[i]])
        except:
            d.set_value(gr, 0)
            growth_rates[keys[i]] = 0
            
    SaveUnit(path)
        