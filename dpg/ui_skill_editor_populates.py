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
    left = g.unit_editor_left
    right = d.add_child_window(parent=g.unit_editor_right)
    w_skill.left = left
    w_skill.right = right