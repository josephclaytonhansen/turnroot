from globals import globals as g

#this has to be here to prevent circular imports
def UseLoadedData():
    from skill_editor_node_presets import (ActivateWhen, TileAttribute, TurnAttribute, UnitSelfAttribute, 
                                           AndNode, UnitStat, Number, MathOperation, MathCondition, PercentChance)
    #add nodes from pos dictionary
    pos = g.skill_editor_skill.data["pos"]
    awn = g.skill_editor_skill.data["awn"]
    
    for node in awn:
        t = node.split(":")
        node_id = t[0]
        node_type = t[1]

        if node_type.startswith( "Tile Is"): TileAttribute()
        elif node_type.startswith( "Turn Is"): TurnAttribute()
        elif node_type.startswith( "Unit (Self) Is"):UnitSelfAttribute()
        elif node_type.startswith( "And"):AndNode()
        elif node_type.startswith( "Unit (Self) Stat"):UnitStat()
        elif node_type.startswith( "Number"):Number()
        elif node_type.startswith( "Math Operation"):MathOperation()
        elif node_type.startswith( "If Number Is"):MathCondition()
        elif node_type.startswith( "Percent Chance"):PercentChance()