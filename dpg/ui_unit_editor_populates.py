from xml.dom.pulldom import default_bufsize
import dearpygui.dearpygui as d
from ui_layout_helpers import *
from globals import globals as g
from game_options import game_options as go
from ui_item_style_helpers import *
import unit_editor_functions as c
from ui_tooltips import make_tooltip
from ui_set_global_colors import htr
from universal_behavior_presets import behavioral_presets

class Widgets():
    pwm = 2.26666
w = Widgets()

def populateAttributes():
    left = g.unit_editor_left
    right = d.add_child_window(parent=g.unit_editor_right)
    w.left = left
    w.right = right

    with d.file_dialog(directory_selector=False, show=False, width=700, modal=True, height = 600, callback=c.GetUnitFile, tag="UnitSelect") as w.unit_select:
        d.bind_item_theme(w.unit_select, set_colors(g.color_theme))
        d.add_file_extension(".truf", color=htr("node_selected_color"), custom_text="[Turnroot Unit File]")
    
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
    for x in ["Unit name", "Default class"]:
        i +=1
        tmp = d.add_text(parent=w.name_row.columns[i], default_value=x)
        #set padding to 0
        set_item_style(tmp, 0, d.mvStyleVar_ItemSpacing)
        set_font_size(tmp, -1)
        with d.tooltip(parent=tmp) as f:
            make_tooltip(g.tooltips.unit_editor, x, f)
    
    w.name = d.add_input_text(parent=w.name_row.columns[0], callback=c.ChangeName, hint="Unit Name",width=-1,height =-1)
    set_font_size(w.name, 1)
    
    w.current_class = d.add_combo(parent=w.name_row.columns[1], callback=c.ChangeCurrentClass, items=["Myrmidon", "Assassin"], width=-1)
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
        w.pronouns = d.add_combo(parent=w.pronouns_row.columns[0],callback=c.ChangePronouns,
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
        w.notes = d.add_input_text(multiline=True,parent=w.notes_row.columns[0],width=-1, callback = c.ChangeNotes)
        
        tmp = d.add_text(default_value="Description\n(added to game as flavor text)",parent=w.notes_row.columns[1])
        w.desc = d.add_input_text(multiline=True,parent=w.notes_row.columns[1],width=-1, callback=c.ChangeDescription)
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
        w.use_class_stats = d.add_checkbox(label="Use class stats for testing", enabled=False,
                     parent=tmp.columns[1], callback=c.TestGrowthUseClassStats)

def populateAffinities():
    left = d.add_child_window(parent=g.unit_editor_left)
    right = d.add_child_window(parent=g.unit_editor_right)
    w.left = left
    w.right = right
    
    with d.collapsing_header(label="Default Affinities", parent=left, default_open=True) as h:
        w.dwa_rows = {}
        for weapon in g.uw.weapon_types:
            label = d.add_text(default_value=weapon)
            set_item_style(label, 0, d.mvStyleVar_FramePadding)
            tmp = d.add_radio_button(g.uw.affinity_levels, horizontal=True, callback=c.SetAffinity)
            d.set_item_user_data(tmp, weapon)
            w.dwa_rows[weapon] = tmp
        d.add_spacer(height=g.item_spacing)
        d.add_button(label="Change weapon types?",callback=c.ShowChangeWeaponTypes)
    
    with d.collapsing_header(label="How does behavior work?", parent=right, default_open=False) as hi:
        set_item_color(hi, "list_background_color", d.mvThemeCol_Header)
        pass
    
    with d.collapsing_header(label="Basic Behavior", parent=right, default_open=True) as h:
        w.behavior_sliders = [None, None, None]
        labels = [["Soldier", "Lone Wolf"], ["Strategic", "Mindless"], ["Cautious", "Brash"]]
        for x in [0,1,2]:
            tmp = Widgets()
            BuildTable(tmp,[10,80,10], h)
            
            t = d.add_button(label=labels[x][0],parent=tmp.columns[0],callback=c.JumpToBehavior)
            set_item_color(t, "window_background_color", d.mvThemeCol_Button)
            d.set_item_user_data(t, [x, 0])
            
            w.behavior_sliders[x] = d.add_slider_int(format="", clamped=True,parent=tmp.columns[1], width=-1, callback=c.ChangeBehaviorSlider)
            d.set_item_user_data(w.behavior_sliders[x], x)
            
            t = d.add_button(label=labels[x][1],parent=tmp.columns[2],callback=c.JumpToBehavior)
            set_item_color(t, "window_background_color", d.mvThemeCol_Button)
            d.set_item_user_data(t, [x, 100])
        
        d.add_spacer(height=g.item_spacing, parent=h)
        tmp = Widgets()
        BuildTable(tmp,[20,80], h)
        w.behavior_preset = d.add_combo(items=[behavior.pretty_name for behavior in behavioral_presets],
                                        parent=tmp.columns[0],width=-1,default_value="", callback=c.ChangeBehavioralPreset)
        d.set_item_user_data(w.behavior_preset, behavioral_presets)
        
        w.preset_description = d.add_text(default_value="--Preset Description--", parent = tmp.columns[1])
    
    with d.collapsing_header(label="Special Behavior", parent=right, default_open=False) as h:
        pass
