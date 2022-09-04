from skill_editor_functions import addBasicNode, ShowAddNodeMenu
from globals import globals as g
import dearpygui.dearpygui as d

def ActivateWhen():
    addBasicNode(
            inputs={"bool":"if"},
            outputs={"trigger":"activate"},
            static={"combo":"when"},
            combo_items={"combowhen":["Passive (always active)", "Unit Action", "Enemy Action", "Player Turn Start", "Enemy Turn Start"]},
            name = "Activate When",
            node_editor=g.window_widgets_skill.node_editor,
            desc="""This node is a required node for all skills.\n\n
Define when a skill- the rest of the node tree- is activated. The if input is used to add conditions to skills.\n
Add an And node to use multiple conditions.\n
If the input is left empty, the skill will always activate.\n\n
You should only have one of these nodes. More will cause an error.""")
    ShowAddNodeMenu()

def TileAttribute():
    addBasicNode(
            inputs={},
            outputs={"bool":"if"},
            static={"combo":"attr"},
            combo_items={"comboattr":["Is Night", "Is Outdoors", "Is Water", "Is Raining", "Is Snowing", "Is Slow", "Is Danger"]},
            name = "Tile Is",
            node_editor=g.window_widgets_skill.node_editor,
            desc="""Get an attribute of the tile or map the unit is currently on. Outputs a True or False value.""")
    ShowAddNodeMenu()
    
def TurnAttribute():
    addBasicNode(
            inputs={},
            outputs={"bool":"if attribute", "int":"turn number"},
            static={"combo":"attribute"},
            combo_items={"comboattribute":["Is Even", "Is Odd"]},
            name = "Tile Is",
            node_editor=g.window_widgets_skill.node_editor,
            desc="""Get an attribute of the current turn. Outputs a True or False value and/or a turn number.""")
    ShowAddNodeMenu()

def UnitSelfAttribute():
    addBasicNode(
            inputs={},
            outputs={"bool":"if"},
            static={"combo":"attr"},
            combo_items={"comboattr":["Is Paired Up", "No Other Friendly Units within 1 Space",
                                      "No Other Friendly Units within 2 Spaces", "No Other Friendly Units within 3 Spaces"]},
            name = "Unit (Self) Is",
            node_editor=g.window_widgets_skill.node_editor,
            desc="""Get an attribute of this unit. Outputs True or False.""")
    ShowAddNodeMenu()

def AndNode():
    addBasicNode(
            inputs={"bool1":"if", "bool2":"if"},
            outputs={"bool":"if"},
            name = "And",
            node_editor=g.window_widgets_skill.node_editor,
            desc="""Combine two conditions. Outputs true if both are true, otherwise, outputs false.""")
    ShowAddNodeMenu()
