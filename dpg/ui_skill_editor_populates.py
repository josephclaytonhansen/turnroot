import dearpygui.dearpygui as d
from ui_layout_helpers import *
from globals import globals as g
from game_options import game_options as go
from ui_item_style_helpers import *
import skill_editor_functions as c_skill
from ui_tooltips import make_tooltip
from ui_set_global_colors import htr
from universal_behavior_presets import behavioral_presets
from skill_editor_node_presets import *

class WidgetsSkill():
    pwm = 2.26666
w_skill = WidgetsSkill()
gv = g

def populateSkillEditor():
    left = d.add_child_window(parent=g.unit_editor_left)
    right = d.add_child_window(parent=g.unit_editor_right)
    w_skill.left = left
    w_skill.right = right
    
    with d.collapsing_header(label="Instructions",parent=right):
        w_skill.instructions = d.add_text( default_value="""Right Click to add a skill node.\n
Right click again or double-click to close the add menu.\n
Press Delete or X to remove an added node.\n
Drag the middle mouse button or Space to move.\n
Ctrl+Click on node connections, Delete, or X to remove node connections.
""", wrap=350)
        
    d.add_spacer(height=gv.item_spacing*2, parent=left)
    w_skill.node_information = d.add_text(parent=w_skill.right, default_value="", wrap=350)
    
    with d.file_dialog(directory_selector=False, show=False, width=700, modal=True, height = 600, callback=c_skill.GetSkillFile, tag="SkillSelect") as w_skill.unit_select:
        d.bind_item_theme(w_skill.unit_select, set_colors(g.color_theme))
        d.add_file_extension(".trsf", color=htr("node_selected_color"), custom_text="[Turnroot Skill File]")
        
    # w_skill.name_row = WidgetsSkill()
    # BuildTable(w_skill.name_row,[55,35,10],left)
    
    w_skill.active_nodes = []
    w_skill.node_desc = {}
    
    with d.node_editor(callback=c_skill.link_callback, delink_callback=c_skill.delink_callback,
                       parent=left, minimap=True, menubar=False, minimap_location=d.mvNodeMiniMap_Location_BottomRight) as f:
        w_skill.node_editor = f
        g.show_add_node = False
        g.window_widgets_skill.add_nodes = d.add_window(no_title_bar=True, label = "Add Node", show=False,
                     width=g.text_size * 29, height = 300,
                     modal=True, tag="add_node", no_resize=False, popup=True)
        w_skill.add_nodes = g.window_widgets_skill.add_nodes
        
        ActivateWhen()
        
        tmp = d.add_text(default_value="Operations", parent=w_skill.add_nodes)
        set_font_size(tmp, 2)
        
        row1 = WidgetsSkill()
        BuildTable(row1,[50, 50],w_skill.add_nodes)
        tmp = d.add_text(default_value="Attributes", parent=w_skill.add_nodes)
        set_font_size(tmp, 2)
        
        d.add_button(parent=row1.columns[0], label="Number", callback=lambda:Number(m=None,c=True))
        d.add_button(parent=row1.columns[0], label="Math Operation", callback=lambda:MathOperation(m=None,c=True))
        d.add_button(parent=row1.columns[0], label="Math Condition", callback=lambda:MathCondition(m=None,c=True))
        d.add_button(parent=row1.columns[0], label="Number % Chance", callback=lambda:PercentChance(m=None,c=True))
        d.add_button(parent=row1.columns[1], label="And", callback=lambda:AndNode(m=None,c=True))
        d.add_button(parent=row1.columns[1], label="Or", callback=lambda:OrNode(m=None,c=True))
        d.add_button(parent=row1.columns[1], label="Not", callback=lambda:NotNode(m=None,c=True))
        
        
        
        row2 = WidgetsSkill()
        BuildTable(row2,[50, 50],w_skill.add_nodes)
        
        tmp = d.add_text(default_value="Effects", parent=w_skill.add_nodes)
        set_font_size(tmp, 2)
        
        d.add_button(parent=row2.columns[0], label="Unit (Self) Stat Value", callback=lambda:UnitStat(m=None,c=True))
        d.add_button(parent=row2.columns[0], label="Unit (Self) Secondary Stat Value", callback=lambda:UnitSStat(m=None,c=True))
        d.add_button(parent=row2.columns[0], label="Tile/Map Is", callback=lambda:TileAttribute(m=None,c=True))
        d.add_button(parent=row2.columns[0], label="Turn Is", callback=lambda:TurnAttribute(m=None,c=True))
        d.add_button(parent=row2.columns[1], label="Unit (Self) Is", callback=lambda:UnitSelfAttribute(m=None,c=True))
        d.add_button(parent=row2.columns[1], label="Unit (Self) Weapon Type Is", callback=lambda:UnitWeapon(m=None,c=True))
        d.add_button(parent=row2.columns[1], label="Enemy Weapon Type Is", callback=lambda:EnemyWeapon(m=None,c=True))
        
        row3 = WidgetsSkill()
        BuildTable(row3,[50, 50],w_skill.add_nodes)
        
        d.add_button(parent=row3.columns[0], label="Set Unit (Self) Stat To", callback=lambda:SetUnitStat(m=None,c=True))
        d.add_button(parent=row3.columns[1], label="Set Unit (Self) Secondary Stat To", callback=lambda:SetUnitSStat(m=None,c=True))
        d.add_button(parent=row3.columns[0], label="Affect Battle Flow", callback=lambda:AffectFlow(m=None,c=True))
        d.add_button(parent=row3.columns[1], label="Dual Effect", callback=lambda:SplitFlow(m=None,c=True))
        
        with d.handler_registry():
            d.add_key_press_handler(key=d.mvKey_LShift + d.mvKey_A, callback=c_skill.ShowAddNodeMenu)
            d.add_key_press_handler(key=d.mvKey_O, callback=c_skill.HardOpen)
            d.add_key_press_handler(key=d.mvKey_D, callback=c_skill.PrintSkillDebug)
            d.add_key_press_handler(key=d.mvKey_Delete, callback=c_skill.HideNode)
            d.add_key_press_handler(key=d.mvKey_X, callback=c_skill.HideNode)
            d.add_mouse_click_handler(button=d.mvMouseButton_Right, callback=c_skill.ShowAddNodeMenu)
            d.add_mouse_double_click_handler(button=d.mvMouseButton_Left, callback=lambda:d.hide_item("add_node"))
