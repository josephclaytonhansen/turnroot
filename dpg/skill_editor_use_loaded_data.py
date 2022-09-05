from globals import globals as g
import dearpygui.dearpygui as d

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
    try:
        d.set_value(g.do_not_delete_statics, sta["0"].split(":")[-1])
    except Exception as e:
        print(e)
        
    for node in awn:
        t = node.split(":")
        
        node_id = t[0]
        

        try:
            statics = sta[node_id]
            print(node_id, statics)
            no_st = False
        except Exception as e:
            #this node doesn't have statics
            no_st = True
        node_type = t[1]

        #set node positions
        node_pos = pos[node_id]
        if node_type.startswith( "Tile Is"):
            tmp,st=TileAttribute()
            d.configure_item(tmp, pos=node_pos)
            if not no_st:
                d.set_value(st, statics.split(":")[-1])
                g.skill_editor_skill_statics[d.get_item_alias(tmp).split(":")[0]] = statics
            
        elif node_type.startswith( "Turn Is"):
            tmp,st=TurnAttribute()
            d.configure_item(tmp, pos=node_pos)
            if not no_st:
                d.set_value(st, statics.split(":")[-1])
                g.skill_editor_skill_statics[d.get_item_alias(tmp).split(":")[0]] = statics


            
        elif node_type.startswith( "Unit (Self) Is"):
            tmp,st=UnitSelfAttribute()
            d.configure_item(tmp, pos=node_pos)
            if not no_st:
                d.set_value(st, statics.split(":")[-1])
                g.skill_editor_skill_statics[d.get_item_alias(tmp).split(":")[0]] = statics


            
        elif node_type.startswith( "And"):
            tmp,st=AndNode()
            d.configure_item(tmp, pos=node_pos)



            
        elif node_type.startswith( "Unit (Self) Stat"):
            tmp,st=UnitStat()
            d.configure_item(tmp, pos=node_pos)
            if not no_st:
                d.set_value(st, statics.split(":")[-1])
                g.skill_editor_skill_statics[d.get_item_alias(tmp).split(":")[0]] = statics


            
        elif node_type.startswith( "Number"):
            tmp,st=Number()
            d.configure_item(tmp, pos=node_pos)
            if not no_st:
                d.set_value(st, float(statics.split(":")[-1]))
                g.skill_editor_skill_statics[d.get_item_alias(tmp).split(":")[0]] = statics

            
        elif node_type.startswith( "Math Operation"):
            tmp,st=MathOperation()
            d.configure_item(tmp, pos=node_pos)
            if not no_st:
                d.set_value(st, statics.split(":")[-1])
                g.skill_editor_skill_statics[d.get_item_alias(tmp).split(":")[0]] = statics

            
        elif node_type.startswith( "If Number Is"):
            tmp,st=MathCondition()
            d.configure_item(tmp, pos=node_pos)
            if not no_st:
                d.set_value(st, statics.split(":")[-1])
                g.skill_editor_skill_statics[d.get_item_alias(tmp).split(":")[0]] = statics

            
        elif node_type.startswith( "Percent Chance"):
            tmp,st=PercentChance()
            d.configure_item(tmp, pos=node_pos)

            


            
        