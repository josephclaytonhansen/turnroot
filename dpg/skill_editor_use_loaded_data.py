from globals import globals as g
import dearpygui.dearpygui as d

class SkillConnectionEnds():
    skill_connection_ends = {}
sce = SkillConnectionEnds().skill_connection_ends

#this has to be here to prevent circular imports
def UseLoadedData():
    from skill_editor_node_presets import (ActivateWhen, TileAttribute, TurnAttribute, UnitSelfAttribute, 
                                           AndNode, UnitStat, Number, MathOperation, MathCondition, PercentChance,
                                           UnitSStat, SetUnitSStat, SetUnitStat)
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
        sce["0"] = "0:Activate When:inputs:0"
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
            tmp, st, attributes=TileAttribute(me=node_id)
            
            d.configure_item(tmp, pos=node_pos)
            sce[tmp.split(":")[0]]=attributes
            Lines(con, attributes,g, d.get_item_alias(tmp).split(":")[0])
            if not no_st:
                d.set_value(st, statics.split(":")[-1])
                g.skill_editor_skill_statics[d.get_item_alias(tmp).split(":")[0]] = statics
            
        elif node_type.startswith( "Turn Is"):
            tmp, st, attributes=TurnAttribute(me=node_id)
            
            d.configure_item(tmp, pos=node_pos)
            sce[tmp.split(":")[0]]=attributes
            Lines(con, attributes,g, d.get_item_alias(tmp).split(":")[0])
            if not no_st:
                d.set_value(st, statics.split(":")[-1])
                g.skill_editor_skill_statics[d.get_item_alias(tmp).split(":")[0]] = statics
            
        elif node_type.startswith( "Unit (Self) Is"):
            tmp, st, attributes=UnitSelfAttribute(me=node_id)
            
            d.configure_item(tmp, pos=node_pos)
            sce[tmp.split(":")[0]]=attributes
            Lines(con, attributes,g, d.get_item_alias(tmp).split(":")[0])
            if not no_st:
                d.set_value(st, statics.split(":")[-1])
                g.skill_editor_skill_statics[d.get_item_alias(tmp).split(":")[0]] = statics
            
        elif node_type.startswith( "And"):
            tmp, st, attributes=AndNode(me=node_id)
            
            d.configure_item(tmp, pos=node_pos)
            sce[tmp.split(":")[0]]=attributes
            Lines(con, attributes,g, d.get_item_alias(tmp).split(":")[0])
            
        elif node_type.startswith( "Unit (Self) Stat"):
            tmp, st, attributes=UnitStat(me=node_id)
            
            d.configure_item(tmp, pos=node_pos)
            sce[tmp.split(":")[0]]=attributes
            Lines(con, attributes,g, d.get_item_alias(tmp).split(":")[0])
            if not no_st:
                d.set_value(st, statics.split(":")[-1])
                g.skill_editor_skill_statics[d.get_item_alias(tmp).split(":")[0]] = statics
        
        elif node_type.startswith( "Unit (Self) Secondary Stat"):
            tmp, st, attributes=UnitSStat(me=node_id)
            
            d.configure_item(tmp, pos=node_pos)
            sce[tmp.split(":")[0]]=attributes
            Lines(con, attributes,g, d.get_item_alias(tmp).split(":")[0])
            if not no_st:
                d.set_value(st, statics.split(":")[-1])
                g.skill_editor_skill_statics[d.get_item_alias(tmp).split(":")[0]] = statics

        elif node_type.startswith( "Number"):
            tmp, st, attributes=Number(me=node_id)
            
            d.configure_item(tmp, pos=node_pos)
            sce[tmp.split(":")[0]]=attributes
            Lines(con, attributes,g, d.get_item_alias(tmp).split(":")[0])
            if not no_st:
                d.set_value(st, float(statics.split(":")[-1]))
                g.skill_editor_skill_statics[d.get_item_alias(tmp).split(":")[0]] = statics

        elif node_type.startswith( "Math Operation"):
            tmp, st, attributes=MathOperation(me=node_id)
            
            d.configure_item(tmp, pos=node_pos)
            sce[tmp.split(":")[0]]=attributes
            Lines(con, attributes,g, d.get_item_alias(tmp).split(":")[0])
            if not no_st:
                d.set_value(st, statics.split(":")[-1])
                g.skill_editor_skill_statics[d.get_item_alias(tmp).split(":")[0]] = statics

        elif node_type.startswith( "If Number Is"):
            tmp, st, attributes=MathCondition(me=node_id)
            
            d.configure_item(tmp, pos=node_pos)
            sce[tmp.split(":")[0]]=attributes
            Lines(con, attributes,g, d.get_item_alias(tmp).split(":")[0])
            if not no_st:
                d.set_value(st, statics.split(":")[-1])
                g.skill_editor_skill_statics[d.get_item_alias(tmp).split(":")[0]] = statics

        elif node_type.startswith( "Percent Chance"):
            tmp, st, attributes=PercentChance(me=node_id)
            
            d.configure_item(tmp, pos=node_pos)
            sce[tmp.split(":")[0]]=attributes
            Lines(con, attributes,g, node_id)
        
        elif node_type.startswith( "Set Unit Stat"):
            tmp, st, attributes=SetUnitStat(me=node_id)
            
            d.configure_item(tmp, pos=node_pos)
            sce[tmp.split(":")[0]]=attributes
            Lines(con, attributes,g, node_id)
            if not no_st:
                d.set_value(st, statics.split(":")[-1])
                g.skill_editor_skill_statics[d.get_item_alias(tmp).split(":")[0]] = statics
        
        elif node_type.startswith( "Set Unit Secondary Stat"):
            tmp, st, attributes=SetUnitSStat(me=node_id)
            
            d.configure_item(tmp, pos=node_pos)
            sce[tmp.split(":")[0]]=attributes
            Lines(con, attributes,g, node_id)
            if not no_st:
                d.set_value(st, statics.split(":")[-1])
                g.skill_editor_skill_statics[d.get_item_alias(tmp).split(":")[0]] = statics
        
    
def Lines(con, attributes,g, node_id):  

    i = -1
    for c in con:
        connected_nodes = []
        real_conn = []
        i += 1

        tmp = c.split(":")
        left = ":".join([tmp[0], tmp[1], tmp[2], tmp[3]])
        left_socket = tmp[2]+":"+tmp[3]
        left_id = tmp[0]
        right = ":".join([tmp[4], tmp[5], tmp[6], tmp[7]])
        right_socket = tmp[2]+":"+tmp[3]
        right_id = tmp[4]

        
        for attr in sce.keys():
            if left_id == attr:
                connected_nodes.append(left)
            if right_id == attr:
                connected_nodes.append(right)
            if g.debug:
                print(connected_nodes)
        if len(connected_nodes) == 2:
            d.add_node_link(connected_nodes[1], connected_nodes[0], parent=g.window_widgets_skill.node_editor)
            if connected_nodes[0]+":"+connected_nodes[1] not in g.skill_editor_skill_connections:
                g.skill_editor_skill_connections.append(connected_nodes[0]+":"+connected_nodes[1])
                # try:
                #     d.add_node_link(sce[1], sce[0], parent=g.window_widgets_skill.node_editor)
                # except Exception as e:
                #     print(e, e.with_traceback, e.__context__, e.__cause__)
                # sce = []



        

            


            
        