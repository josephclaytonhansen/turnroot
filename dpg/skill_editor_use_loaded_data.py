from globals import globals as g
import dearpygui.dearpygui as d

class SkillConnectionEnds():
    skill_connection_ends = []
sce = SkillConnectionEnds().skill_connection_ends

#this has to be here to prevent circular imports
def UseLoadedData():
    from skill_editor_node_presets import (ActivateWhen, TileAttribute, TurnAttribute, UnitSelfAttribute, 
                                           AndNode, UnitStat, Number, MathOperation, MathCondition, PercentChance)
    #add nodes from pos dictionary
    pos = g.skill_editor_skill.data["pos"]
    awn = g.skill_editor_skill.data["awn"]
    sta = g.skill_editor_skill.data["sta"]
    con = g.skill_editor_skill.data["con"]
    
    g.window_widgets_skill.active_nodes = ["0:Activate When:0"]
    g.skill_editor_skill_statics = {}
    g.skill_editor_skill_connections = []
    try:
        d.set_value(g.do_not_delete_statics, sta["0"].split(":")[-1])
        g.skill_editor_skill_statics["0"] = sta["0"].split(":")[-1]
    except Exception as e:
        print(e)
        
    for node in awn:
        t = node.split(":")
        node_id = t[0]

        try:
            statics = sta[node_id]
            no_st = False
        except Exception as e:
            #this node doesn't have statics
            no_st = True
        node_type = t[1]

        #set node positions
        node_pos = pos[node_id]
        if node_type.startswith( "Tile Is"):
            tmp, st, attributes=TileAttribute()
            
            d.configure_item(tmp, pos=node_pos)
            Lines(con, attributes,g, node_id)
            if not no_st:
                d.set_value(st, statics.split(":")[-1])
                g.skill_editor_skill_statics[d.get_item_alias(tmp).split(":")[0]] = statics
            
        elif node_type.startswith( "Turn Is"):
            tmp, st, attributes=TurnAttribute()
            
            d.configure_item(tmp, pos=node_pos)
            Lines(con, attributes,g, node_id)
            if not no_st:
                d.set_value(st, statics.split(":")[-1])
                g.skill_editor_skill_statics[d.get_item_alias(tmp).split(":")[0]] = statics
            
        elif node_type.startswith( "Unit (Self) Is"):
            tmp, st, attributes=UnitSelfAttribute()
            
            d.configure_item(tmp, pos=node_pos)
            Lines(con, attributes,g, node_id)
            if not no_st:
                d.set_value(st, statics.split(":")[-1])
                g.skill_editor_skill_statics[d.get_item_alias(tmp).split(":")[0]] = statics
            
        elif node_type.startswith( "And"):
            tmp, st, attributes=AndNode()
            
            d.configure_item(tmp, pos=node_pos)
            Lines(con, attributes,g, node_id)
            
        elif node_type.startswith( "Unit (Self) Stat"):
            tmp, st, attributes=UnitStat()
            
            d.configure_item(tmp, pos=node_pos)
            Lines(con, attributes,g, node_id)
            if not no_st:
                d.set_value(st, statics.split(":")[-1])
                g.skill_editor_skill_statics[d.get_item_alias(tmp).split(":")[0]] = statics

        elif node_type.startswith( "Number"):
            tmp, st, attributes=Number()
            
            d.configure_item(tmp, pos=node_pos)
            Lines(con, attributes,g, node_id)
            if not no_st:
                d.set_value(st, float(statics.split(":")[-1]))
                g.skill_editor_skill_statics[d.get_item_alias(tmp).split(":")[0]] = statics

        elif node_type.startswith( "Math Operation"):
            tmp, st, attributes=MathOperation()
            
            d.configure_item(tmp, pos=node_pos)
            Lines(con, attributes,g, node_id)
            if not no_st:
                d.set_value(st, statics.split(":")[-1])
                g.skill_editor_skill_statics[d.get_item_alias(tmp).split(":")[0]] = statics

        elif node_type.startswith( "If Number Is"):
            tmp, st, attributes=MathCondition()
            
            d.configure_item(tmp, pos=node_pos)
            Lines(con, attributes,g, node_id)
            if not no_st:
                d.set_value(st, statics.split(":")[-1])
                g.skill_editor_skill_statics[d.get_item_alias(tmp).split(":")[0]] = statics

        elif node_type.startswith( "Percent Chance"):
            tmp, st, attributes=PercentChance()
            
            d.configure_item(tmp, pos=node_pos)
            Lines(con, attributes,g, node_id)
        
    
def Lines(con, attributes,g, node_id):  
    global sce
    for c in con:
        print(c)
        parts = c.split(":")
        left = [parts[1],parts[2],parts[3]]
        right = [parts[5],parts[6],parts[7]]
        parts = [left,right]
        socket_names = [":".join(parts[0]), ":".join(parts[1])]
        for attr in attributes:
            tmp = attr.split(":")
            h = ":".join([tmp[1], tmp[2], tmp[3]])
            
            for socket in socket_names:
                if h == socket:
                    sce.append(node_id+":"+h)
                    print(sce)
                    if len(sce) == 2:
                        g.skill_editor_skill_connections.append(sce[0]+sce[1])
                        sce = []
        

            


            
        