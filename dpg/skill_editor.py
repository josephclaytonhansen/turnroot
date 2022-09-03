import dearpygui.dearpygui as d
from ui_layout_helpers import *
from globals import globals as g
from ui_item_style_helpers import *
import unit_editor_functions as c
from ui_colorthemes import colorthemes as themes
from editor_save_load_unit import SaveUnit
from ui_unit_editor_populates import *
import sys
from universal_weapon_types import universal_weapons as uw
from editor_global_menus import buildEditorMenu

g.active_window_widgets = w
g.uw = uw()

class Skill():
    pass

def add_skill_editor(params={}):
    # buildSkillEditor()
    # populateSkillEditor()
    add_menu()
    # unit_editor_centers_in_column()
    # make_functions()
    w.colors.set()
    g.editors.append("unit_editor")
    #remove this in favor of save/load, temporarily for dev
    u = Skill()
    #you can only be editing one thing at a time, technically, so this works
    g.is_editing = u
    g.is_editing.type = "skill"
    g.path = ""
    TimedEvent(g.autosave_time)

def add_menu():
    pass