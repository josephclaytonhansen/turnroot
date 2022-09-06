from skill_editor_functions import addBasicNode, ShowAddNodeMenu
from globals import globals as g
from game_options import game_options as go
from universal_weapon_types import universal_weapons as uw
import dearpygui.dearpygui as d
import random

def ActivateWhen(m=None, c=True):
    tmp, st, attributes = addBasicNode(
            inputs={"bool":"if"},
            outputs={"trigger":"activate"},
            static={"combo":"when"},
            combo_items={"combowhen":["Passive (always active)", "Unit Action", "Enemy Action", "Unit or Enemy Action", "Player Turn Start", "Enemy Turn Start",
                                      "Player Takes Damage", "Enemy Takes Damage"]},
            name = "Activate When",
            tag = "0:Activate When:0",
            me="0",
            node_editor=g.window_widgets_skill.node_editor,
            desc="""This node is a required node for all skills.\n\n
Define when a skill- the rest of the node tree- is activated. The if input is used to add conditions to skills.\n
Add an And node to use multiple conditions.\n
If the input is left empty, the skill will always activate.\n\n
Since it's required, this node cannot be deleted or added.""")
    d.configure_item(tmp, pos=[d.get_viewport_width()/2, d.get_viewport_height()/2])
    g.do_not_delete_node = tmp
    g.do_not_delete_statics = st

def TileAttribute(m=None, c=True):
    tmp, st, attributes = addBasicNode(
            me=m,
            inputs={},
            outputs={"bool":"if"},
            static={"combo":"attr"},
            combo_items={"comboattr":["Is Night", "Is Outdoors", "Is Water", "Is Raining", "Is Snowing", "Is Slow", "Is Danger"]},
            name = "Tile Is",
            calc_me=c,
            node_editor=g.window_widgets_skill.node_editor,
            desc="""Get an attribute of the tile or map the unit is currently on. Outputs a True or False value.""")
    ShowAddNodeMenu()
    return [tmp, st, attributes]
    
def TurnAttribute(m=None, c=True):
    tmp, st, attributes = addBasicNode(
            me=m,
            inputs={},
            outputs={"bool":"if attribute", "int":"turn number"},
            static={"combo":"attribute"},
            combo_items={"comboattribute":["Is Even", "Is Odd"]},
            name = "Turn Is",
            calc_me=c,
            node_editor=g.window_widgets_skill.node_editor,
            desc="""Get an attribute of the current turn. Outputs a True or False value and/or a turn number.""")
    ShowAddNodeMenu()
    return [tmp, st, attributes]

def UnitSelfAttribute(m=None, c=True):
    tmp, st, attributes = addBasicNode(
            me=m,
            inputs={},
            outputs={"bool":"if"},
            static={"combo":"attr"},
            combo_items={"comboattr":["Is Paired Up", "No Other Friendly Units within 1 Space",
                                      "No Other Friendly Units within 2 Spaces", "No Other Friendly Units within 3 Spaces"]},
            name = "Unit (Self) Is",
            calc_me=c,
            node_editor=g.window_widgets_skill.node_editor,
            desc="""Get an attribute of this unit. Outputs True or False.""")
    ShowAddNodeMenu()
    return [tmp, st, attributes]

def AndNode(m=None, c=True):
    tmp, st, attributes = addBasicNode(
            me=m,
            inputs={"bool1":"if", "bool2":"if"},
            outputs={"bool":"if"},
            name = "And",
            calc_me=c,
            node_editor=g.window_widgets_skill.node_editor,
            desc="""Combine two conditions. Outputs true if both are true, otherwise, outputs false.""")
    ShowAddNodeMenu()
    return [tmp, st, attributes]

def OrNode(m=None, c=True):
    tmp, st, attributes = addBasicNode(
            me=m,
            inputs={"bool1":"if", "bool2":"if"},
            outputs={"bool":"if"},
            name = "Or",
            calc_me=c,
            node_editor=g.window_widgets_skill.node_editor,
            desc="""Combine two conditions. Outputs true if one or both is true. If both are false, outputs false.""")
    ShowAddNodeMenu()
    return [tmp, st, attributes]

def NotNode(m=None, c=True):
    tmp, st, attributes = addBasicNode(
            me=m,
            inputs={"bool1":"if"},
            outputs={"bool":"if"},
            name = "Not",
            calc_me=c,
            node_editor=g.window_widgets_skill.node_editor,
            desc="""Negates a condition. Outputs true if condition is false.""")
    ShowAddNodeMenu()
    return [tmp, st, attributes]

def UnitStat(m=None, c=True):
    l = ["HP", "Max HP", "Strength", "Speed", "Magic", "Defense", "Resistance", "Luck", "Skill"]
    if go["use_stat_dexterity"]:
        l.append("Dexterity")
    if go["use_stat_charisma"]:
        l.append("Charisma")
    tmp, st, attributes = addBasicNode(
            me=m,
            inputs={},
            outputs={"int":"stat"},
            static={"combo":"stat"},
            combo_items={"combostat":l},
            name = "Unit (Self) Stat",
            calc_me=c,
            node_editor=g.window_widgets_skill.node_editor,
            desc="""Get the stat value of this unit at the moment of skill activation. Outputs the stat value as a number.""")
    ShowAddNodeMenu()
    return [tmp, st, attributes]

def UnitSStat(m=None, c=True):
    l = ["Hit", "Avoid", "Critical", "Dodge"]
    tmp, st, attributes = addBasicNode(
            me=m,
            inputs={},
            outputs={"int":"stat"},
            static={"combo":"stat"},
            combo_items={"combostat":l},
            name = "Unit (Self) Secondary Stat",
            calc_me=c,
            node_editor=g.window_widgets_skill.node_editor,
            desc="""Get the secondary stat value of this unit at the moment of skill activation. Outputs the stat value as a number.""")
    ShowAddNodeMenu()
    return [tmp, st, attributes]

def UnitWeapon(m=None, c=True):
    l = uw().weapon_types
    tmp, st, attributes = addBasicNode(
            me=m,
            inputs={},
            outputs={"bool":"is type"},
            static={"combo":"weapon type"},
            combo_items={"comboweapon type":l},
            name = "Unit (Self) Weapon",
            calc_me=c,
            node_editor=g.window_widgets_skill.node_editor,
            desc="""Get the weapon type this unit is using. Outputs True or False- choose a weapon type in the dropdown to determine the output.""")
    ShowAddNodeMenu()
    return [tmp, st, attributes]

def EnemyWeapon(m=None, c=True):
    l = uw().weapon_types
    tmp, st, attributes = addBasicNode(
            me=m,
            inputs={},
            outputs={"bool":"is type"},
            static={"combo":"weapon type"},
            combo_items={"comboweapon type":l},
            name = "Enemy Weapon",
            calc_me=c,
            node_editor=g.window_widgets_skill.node_editor,
            desc="""Get the weapon type the enemy unit is using.\n
This is only calculated during combat, as enemies may change. Outputs True or False- choose a weapon type in the dropdown to determine the output.""")
    ShowAddNodeMenu()
    return [tmp, st, attributes]

def Number(m=None, c=True):
    tmp, st, attributes = addBasicNode(
            me=m,
            inputs={},
            outputs={"float":""},
            static={"float":"number"},
            name = "Number",
            calc_me=c,
            node_editor=g.window_widgets_skill.node_editor,
            desc="""Add a number, used for calcuations (for example, checking if HP is greater than 50%. This node would specify the '50' part of that.)""")
    ShowAddNodeMenu()
    return [tmp, st, attributes]

def MathOperation(m=None, c=True):
    tmp, st, attributes = addBasicNode(
                me=m,
                inputs={"float":"number","float2":"number"},
                outputs={"float":"result"},
                static={"combo":"operation"},
                combo_items={"combooperation":["Add","Subtract", "Multiply", "Divide"]},
                name = "Math Operation",
                calc_me=c,
                node_editor=g.window_widgets_skill.node_editor,
                desc="""Use a basic math operation on two numbers. Outputs a decimal number as the result.""")
    ShowAddNodeMenu()
    return [tmp, st, attributes]

def MathCondition(m=None, c=True):
    tmp, st, attributes = addBasicNode(
            me=m,
            inputs={"int":"number","float":"threshold"},
            outputs={"bool":"if"},
            static={"combo":"check"},
            combo_items={"combocheck":["Equals","Less Than", "Greater Than", "Less Than Or Equal To", "Greater Than Or Equal To"]},
            name = "If Number Is",
            calc_me=c,
            node_editor=g.window_widgets_skill.node_editor,
            desc="""Check a number against a (numerical) threshold. Outputs a True or False value.""")
    ShowAddNodeMenu()
    return [tmp, st, attributes]

def PercentChance(m=None, c=True):
    tmp, st, attributes = addBasicNode(
            me=m,
            inputs={"float":"percent"},
            outputs={"bool":"if chance"},
            name = "Percent Chance (N%)",
            calc_me=c,
            node_editor=g.window_widgets_skill.node_editor,
            desc="""This node has an n% chance of activating. Combine with unit stats generally.\n
For example, you could use this to do a 'luck % chance' activation. Outputs True or False- will vary per use.""")
    ShowAddNodeMenu()
    return [tmp, st, attributes]

def SetUnitStat(m=None, c=True):
    l = ["HP", "Max HP", "Strength", "Speed", "Magic", "Defense", "Resistance", "Luck", "Skill"]
    if go["use_stat_dexterity"]:
        l.append("Dexterity")
    if go["use_stat_charisma"]:
        l.append("Charisma")
    tmp, st, attributes = addBasicNode(
            me=m,
            inputs={"trigger":"activate", "int":"number"},
            outputs={"trigger":"activate"},
            static={"combo":"stat"},
            combo_items={"combostat":l},
            name = "Set Unit Stat",
            calc_me=c,
            node_editor=g.window_widgets_skill.node_editor,
            desc="""Change a stat for this unit to a new value. Will display as a bonus or penalty.\n
You should combine this with a UnitStat node to get dynamic values, rather then setting stats to arbitrary static values.\n
Outputs a trigger- this node takes an active trigger, changes the stats, and passes the trigger to the next node.""")
    ShowAddNodeMenu()
    return [tmp, st, attributes]

def SetUnitSStat(m=None, c=True):
    l = ["Hit", "Avoid", "Critical", "Dodge"]
    tmp, st, attributes = addBasicNode(
            me=m,
            inputs={"trigger":"activate", "int":"number"},
            outputs={"trigger":"activate"},
            static={"combo":"stat"},
            combo_items={"combostat":l},
            name = "Set Unit Secondary Stat",
            calc_me=c,
            node_editor=g.window_widgets_skill.node_editor,
            desc="""Change a secondary stat for this unit to a new value. Will display as a bonus or penalty.\n
You should combine this with a UnitSecondaryStat node to get dynamic values, rather then setting stats to arbitrary static values.\n
Outputs a trigger- this node takes an active trigger, changes the stats, and passes the trigger to the next node.""")
    ShowAddNodeMenu()
    return [tmp, st, attributes]