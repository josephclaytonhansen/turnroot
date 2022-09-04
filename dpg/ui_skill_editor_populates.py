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
    
    with d.file_dialog(directory_selector=False, show=False, width=700, modal=True, height = 600, callback=c_skill.GetSkillFile, tag="SkillSelect") as w_skill.unit_select:
        d.bind_item_theme(w_skill.unit_select, set_colors(g.color_theme))
        d.add_file_extension(".trsf", color=htr("node_selected_color"), custom_text="[Turnroot Skill File]")
        
    # w_skill.name_row = WidgetsSkill()
    # BuildTable(w_skill.name_row,[55,35,10],left)
    
    with d.node_editor(callback=c_skill.link_callback, delink_callback=c_skill.delink_callback,
                       parent=left, minimap=True, menubar=False, minimap_location=d.mvNodeMiniMap_Location_BottomRight) as f:
        w_skill.node_editor = f
        c_skill.addBasicNode(
            inputs={"int":"integer","float":"float","bool":"boolean","trigger":"event"},
            outputs={"trigger":"text"},
            name = "Test Node",
            node_editor=w_skill.node_editor)
        c_skill.addBasicNode(
            inputs={"int":"integer","float":"float","bool":"boolean","trigger":"event"},
            outputs={"trigger":"much longer text"},
            name = "Test Node 2",
            node_editor=w_skill.node_editor)