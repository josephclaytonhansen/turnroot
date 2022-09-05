from skill_editor_functions import addBasicNode, ShowAddNodeMenu
from globals import globals as g
from game_options import game_options as go
import dearpygui.dearpygui as d
import random

def ActivateWhen():
    tmp, st, attributes = addBasicNode(

            inputs={"bool":"if"},
            outputs={"trigger":"activate"},
            static={"combo":"when"},
            combo_items={"combowhen":["Passive (always active)", "Unit Action", "Enemy Action", "Player Turn Start", "Enemy Turn Start",
                                      "Player Takes Damage", "Enemy Takes Damage"]},
            name = "Activate When",
            tag = "0:Activate When:0",
            node_editor=g.window_widgets_skill.node_editor,
            desc="""This node is a required node for all skills.\n\n
Define when a skill- the rest of the node tree- is activated. The if input is used to add conditions to skills.\n
Add an And node to use multiple conditions.\n
If the input is left empty, the skill will always activate.\n\n
Since it's required, this node cannot be deleted or added.""")
    d.configure_item(tmp, pos=[d.get_viewport_width()/2, d.get_viewport_height()/2])
    g.do_not_delete_node = tmp
    g.do_not_delete_statics = st

def TileAttribute():
    tmp, st, attributes = addBasicNode(
            inputs={},
            outputs={"bool":"if"},
            static={"combo":"attr"},
            combo_items={"comboattr":["Is Night", "Is Outdoors", "Is Water", "Is Raining", "Is Snowing", "Is Slow", "Is Danger"]},
            name = "Tile Is",
            tag = str(int(random.random()*1000))+str(int(random.random()*1000))+":"+"Tile Is"+str(len(g.window_widgets_skill.active_nodes)),
            node_editor=g.window_widgets_skill.node_editor,
            desc="""Get an attribute of the tile or map the unit is currently on. Outputs a True or False value.""")
    ShowAddNodeMenu()
    return [tmp, st, attributes]
    
def TurnAttribute():
    tmp, st, attributes = addBasicNode(
            inputs={},
            outputs={"bool":"if attribute", "int":"turn number"},
            static={"combo":"attribute"},
            combo_items={"comboattribute":["Is Even", "Is Odd"]},
            name = "Turn Is",
            tag = str(int(random.random()*1000))+str(int(random.random()*1000))+":"+"Turn Is"+str(len(g.window_widgets_skill.active_nodes)),
            node_editor=g.window_widgets_skill.node_editor,
            desc="""Get an attribute of the current turn. Outputs a True or False value and/or a turn number.""")
    ShowAddNodeMenu()
    return [tmp, st, attributes]

def UnitSelfAttribute():
    tmp, st, attributes = addBasicNode(
            inputs={},
            outputs={"bool":"if"},
            static={"combo":"attr"},
            combo_items={"comboattr":["Is Paired Up", "No Other Friendly Units within 1 Space",
                                      "No Other Friendly Units within 2 Spaces", "No Other Friendly Units within 3 Spaces"]},
            name = "Unit (Self) Is",
            tag = str(int(random.random()*1000))+str(int(random.random()*1000))+":"+"Unit (Self) Is"+str(len(g.window_widgets_skill.active_nodes)),
            node_editor=g.window_widgets_skill.node_editor,
            desc="""Get an attribute of this unit. Outputs True or False.""")
    ShowAddNodeMenu()
    return [tmp, st, attributes]
def AndNode():
    tmp, st, attributes = addBasicNode(
            inputs={"bool1":"if", "bool2":"if"},
            outputs={"bool":"if"},
            name = "And",
            tag = str(int(random.random()*1000))+str(int(random.random()*1000))+":"+"And"+str(len(g.window_widgets_skill.active_nodes)),
            node_editor=g.window_widgets_skill.node_editor,
            desc="""Combine two conditions. Outputs true if both are true, otherwise, outputs false.""")
    ShowAddNodeMenu()
    return [tmp, st, attributes]

def UnitStat():
    l = ["HP", "Max HP", "Strength", "Speed", "Magic", "Defense", "Resistance", "Luck", "Skill"]
    if go["use_stat_dexterity"]:
        l.append("Dexterity")
    if go["use_stat_charisma"]:
        l.append("Charisma")
    tmp, st, attributes = addBasicNode(
            inputs={},
            outputs={"int":"stat"},
            static={"combo":"stat"},
            combo_items={"combostat":l},
            name = "Unit (Self) Stat",
            tag = str(int(random.random()*1000))+str(int(random.random()*1000))+":"+"Unit (Self) Stat"+str(len(g.window_widgets_skill.active_nodes)),
            node_editor=g.window_widgets_skill.node_editor,
            desc="""Get the stat value of this unit at the moment of skill activation. Outputs the stat value as a number.""")
    ShowAddNodeMenu()
    return [tmp, st, attributes]

def Number():
    tmp, st, attributes = addBasicNode(
            inputs={},
            outputs={"float":""},
            static={"float":"number"},
            name = "Number",
            tag = str(int(random.random()*1000))+str(int(random.random()*1000))+":"+"Number"+str(len(g.window_widgets_skill.active_nodes)),
            node_editor=g.window_widgets_skill.node_editor,
            desc="""Add a number, used for calcuations (for example, checking if HP is greater than 50%. This node would specify the '50' part of that.)""")
    ShowAddNodeMenu()
    return [tmp, st, attributes]

def MathOperation():
    tmp, st, attributes = addBasicNode(
                inputs={"float":"number","float2":"number"},
                outputs={"float":"result"},
                static={"combo":"operation"},
                combo_items={"combooperation":["Add","Subtract", "Multiply", "Divide"]},
                name = "Math Operation",
                tag = str(int(random.random()*1000))+str(int(random.random()*1000))+":"+"Math Operation"+str(len(g.window_widgets_skill.active_nodes)),
                node_editor=g.window_widgets_skill.node_editor,
                desc="""Use a basic math operation on two numbers. Outputs a decimal number as the result.""")
    ShowAddNodeMenu()
    return [tmp, st, attributes]

def MathCondition():
    tmp, st, attributes = addBasicNode(
            inputs={"int":"number","float":"threshold"},
            outputs={"bool":"if"},
            static={"combo":"check"},
            combo_items={"combocheck":["Equals","Less Than", "Greater Than", "Less Than Or Equal To", "Greater Than Or Equal To"]},
            name = "If Number Is",
            tag = str(int(random.random()*1000))+str(int(random.random()*1000))+":"+"If Number Is"+str(len(g.window_widgets_skill.active_nodes)),
            node_editor=g.window_widgets_skill.node_editor,
            desc="""Check a number against a (numerical) threshold. Outputs a True or False value.""")
    ShowAddNodeMenu()
    return [tmp, st, attributes]

def PercentChance():
    tmp, st, attributes = addBasicNode(
            inputs={"float":"percent"},
            outputs={"bool":"if chance"},
            name = "Percent Chance (N%)",
            tag = str(int(random.random()*1000))+str(int(random.random()*1000))+":"+"Percent Chance (N%)"+str(len(g.window_widgets_skill.active_nodes)),
            node_editor=g.window_widgets_skill.node_editor,
            desc="""This node has an n% chance of activating. Combine with unit stats generally.\n
For example, you could use this to do a 'luck % chance' activation. Outputs True or False- will vary per use.""")
    ShowAddNodeMenu()
    return [tmp, st, attributes]