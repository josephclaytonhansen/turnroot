import dearpygui.dearpygui as d
from ui_layout_helpers import *
from globals import globals as g
from game_options import game_options as go
from ui_item_style_helpers import *
import skill_editor_functions as c_skill
from ui_tooltips import make_tooltip
from ui_set_global_colors import htr
from universal_behavior_presets import behavioral_presets

class WidgetsSkill():
    pwm = 2.26666
w_skill = WidgetsSkill()

def populateSkillEditor():
    left = d.add_child_window(parent=g.unit_editor_left)
    right = d.add_child_window(parent=g.unit_editor_right)
    w_skill.left = left
    w_skill.right = right
    
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
        d.add_window(no_title_bar=True, label = "Add Node", show=False,
                     width=280, max_size=[280, 1000], height=300, min_size=[280,20],
                     modal=True, tag="add_node", no_resize=False, popup=True)
        
        with d.handler_registry():
            d.add_key_press_handler(key=d.mvKey_LShift + d.mvKey_A, callback=c_skill.ShowAddNodeMenu)
            d.add_key_press_handler(key=d.mvKey_Delete, callback=c_skill.HideNode)
            d.add_key_press_handler(key=d.mvKey_X, callback=c_skill.HideNode)
            d.add_mouse_click_handler(button=d.mvMouseButton_Right, callback=c_skill.ShowAddNodeMenu)

        
        t = c_skill.addBasicNode(
            inputs={"int":"integer","float":"float","bool":"boolean","trigger":"event"},
            outputs={"trigger":"text"},
            name = "Test Node",
            node_editor=w_skill.node_editor)
        w_skill.active_nodes.append(t)
        w_skill.node_desc[t] = "This is a basic node"
        
        t = c_skill.addBasicNode(
            inputs={"int":"integer","float":"float","bool":"boolean","trigger":"event"},
            outputs={"trigger":"much longer text"},
            static={"combo":"combo"},
            combo_items={"combocombo":["Choice 1", "Choice 2"]},
            name = "Test Node 2",
            node_editor=w_skill.node_editor)
        w_skill.active_nodes.append(t)
        w_skill.node_desc[t] = "This is a basic node, number 2"