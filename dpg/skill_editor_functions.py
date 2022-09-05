from globals import globals as g
from ui_colorthemes import colorthemes as themes
from ui_set_global_colors import set_colors, htr, darken
from ui_set_global_font import set_fonts
import dearpygui.dearpygui as d
from editor_data_handling import SaveUserPrefs
from ui_item_style_helpers import *
from ui_layout_helpers import TimedInfoMessage, BuildTable
from editor_save_load_skill import SaveSkill, LoadSkill
from skill_editor_use_loaded_data import UseLoadedData
import random

def basic(sender, app_data, user_data):
    print(sender, app_data, user_data)

def color_theme(sender, app_data, user_data):
    g.color_theme = themes[app_data]
    d.bind_theme(set_colors(g.color_theme))
    user_data.colors.set()
    SaveUserPrefs()

def font_size(sender, app_data, user_data):
    g.text_size = app_data
    set_fonts()
    SaveUserPrefs()
    TimedInfoMessage("Requires restart- no changes will be visible", g.active_window_widgets.status_bar)
    
def fullscreen():
    g.fullscreen = not g.fullscreen
    d.toggle_viewport_fullscreen()
    d.set_viewport_pos([0,0])
    SaveUserPrefs()

def font(sender, app_data, user_data):
    g.font_family = app_data
    set_fonts(label="Assets/Fonts/"+app_data+"-Regular.ttf")
    SaveUserPrefs()
    TimedInfoMessage("Requires restart- no changes will be visible", g.active_window_widgets.status_bar)
    
def window_padding(sender, app_data, user_data):
    g.window_padding = app_data
    d.bind_theme(set_colors(g.color_theme))
    SaveUserPrefs()

def corners_round(sender, app_data, user_data):
    g.corners_round = app_data
    d.bind_theme(set_colors(g.color_theme))
    SaveUserPrefs()

def padding(sender, app_data, user_data):
    g.padding = app_data
    d.bind_theme(set_colors(g.color_theme))
    SaveUserPrefs()

def ChangeAutosave(sender, app_data, user_data):
    g.autosave_time = app_data
    d.bind_theme(set_colors(g.color_theme))
    SaveUserPrefs()

def item_spacing(sender, app_data, user_data):
    g.item_spacing = app_data
    d.bind_theme(set_colors(g.color_theme))
    SaveUserPrefs()

def HardOpen():
    d.show_item("SkillSelect")
    d.set_item_user_data("SkillSelect", "open")

def ShowFileDialog(sender, app_data, user_data):
    if sender == "skillopen":
        d.show_item("SkillSelect")
        d.set_item_user_data("SkillSelect", "open")
    else:
        d.show_item("SkillSelect")
        d.set_item_user_data("SkillSelect", "save")

def GetSkillFile(sender, app_data, user_data):
    g.path = app_data["file_path_name"]
    print(g.path)
    if user_data == "open":
        LoadFromFile()
    else:
        SaveToFile()

def LoadFromFile():
    LoadSkill(g.path)
    UseLoadedData()
     
def NewSkillFile():
    pass

def SaveToFile():
    SaveSkill(g.path)

def ShowAddNodeMenu():
    if g.show_add_node:
        d.show_item("add_node")
        g.show_add_node = False
        d.configure_item("add_node", pos=d.get_mouse_pos())
    else:
        g.show_add_node = True
        d.hide_item("add_node")

# callback runs when user attempts to connect attributes
def link_callback(sender, app_data, user_data):
    # app_data -> (link_id1, link_id2)
    d.add_node_link(app_data[0], app_data[1], parent=sender)
    attrs = [d.get_item_alias(app_data[0]), d.get_item_alias(app_data[1])]
    st = ""
    for a in attrs:
        st = st + a
        if a != attrs[1]:
            st = st + ":"
    g.skill_editor_skill_connections.append(st)
# callback runs when user attempts to disconnect attributes
def delink_callback(sender, app_data):
    # app_data -> link_id
    d.delete_item(app_data)

def HideNode():
    for node in d.get_selected_nodes(g.active_window_widgets.node_editor):
        if node != g.do_not_delete_node:
            g.skill_editor_skill_positions.pop(d.get_item_alias(node).split(":")[0])
            g.active_window_widgets.active_nodes.pop(g.active_window_widgets.active_nodes.index(d.get_item_alias(node)))
            d.delete_item(node)
    for line in d.get_selected_links(g.active_window_widgets.node_editor):
        d.delete_item(line)

def addBasicNode(inputs={}, static={}, outputs={}, name="", node_editor=None, combo_items={None:None},desc="",tag=""):
    statics = []
    with d.node(pos=d.get_mouse_pos(local=False),label=name,parent=node_editor, tag=tag) as f:
        me = str(int(random.random()*1000))+str(int(random.random()*1000))
        i = -1
        outputs_count = -1
        inputs_count = -1
        for socket in outputs.keys():
            outputs_count += 1
            i += 1
            
            with d.node_attribute(attribute_type=d.mvNode_Attr_Output, shape=d.mvNode_PinShape_CircleFilled,
                                  tag=me+":"+name+":output:"+str(outputs_count)) as tmp:
                d.set_item_user_data(tmp,name+":outputs:"+str(i)+":")
                if socket.startswith( "float"):
                    t= d.add_text(default_value=outputs[socket], indent=120, tag=me+":"+name+":output:float"+str(i))
                    set_item_color(t, "node_grid_background_color", d.mvThemeCol_FrameBg)
                    set_font_size(t,-1)
                    d.set_item_user_data(t,name+":static:bool"+str(i)+":")
                    set_node_colors(tmp, ["node_socket_object_color", "node_socket_object_color"],
                                    [d.mvNodeCol_Pin, d.mvNodeCol_PinHovered])

                elif socket.startswith( "int"):
                    t=d.add_text(default_value=outputs[socket], indent=120, tag=me+":"+name+":output:int"+str(i))
                    set_node_colors(tmp, ["node_socket_object_color", "node_socket_object_color"],
                                    [d.mvNodeCol_Pin, d.mvNodeCol_PinHovered])
                    set_item_color(t, "node_grid_background_color", d.mvThemeCol_FrameBg)
                    set_font_size(t,-1)
                    d.set_item_user_data(t,name+":static:bool"+str(i)+":")
                elif socket.startswith( "bool"):
                    t=d.add_text(default_value=outputs[socket], indent=120, tag=me+":"+name+":output:bool"+str(i))
                    set_node_colors(tmp, ["node_socket_boolean_color", "node_socket_boolean_color"],
                                    [d.mvNodeCol_Pin, d.mvNodeCol_PinHovered])
                    set_font_size(t,-1)
                    d.set_item_user_data(t,name+":static:bool"+str(i)+":")
                elif socket.startswith( "trigger"):
                    t=d.add_text(default_value=outputs[socket], indent=120, tag=me+":"+name+":output:trigger"+str(i))
                    set_node_colors(tmp, ["node_socket_trigger_color", "node_socket_trigger_color"],
                                    [d.mvNodeCol_Pin, d.mvNodeCol_PinHovered])
                    set_font_size(t,-1)
                    d.set_item_user_data(t,name+":static:bool"+str(i)+":")
        for socket in inputs.keys():
            i += 1
            inputs_count +=1
            with d.node_attribute(attribute_type=d.mvNode_Attr_Input,
                                  tag=me+":"+name+":inputs:"+str(inputs_count)) as tmp:
                d.set_item_user_data(tmp,name+":inputs:"+str(i)+":")
                if socket.startswith( "float"):
                    t= d.add_text(default_value=inputs[socket], tag=me+":"+name+":input:float"+str(i))
                    set_item_color(t, "node_grid_background_color", d.mvThemeCol_FrameBg)
                    set_node_colors(tmp, ["node_socket_object_color", "node_socket_object_color"],
                                    [d.mvNodeCol_Pin, d.mvNodeCol_PinHovered])
                    set_font_size(t,-1)
                    d.set_item_user_data(t,name+":static:bool"+str(i)+":")

                elif socket.startswith( "int"):
                    t=d.add_text(default_value=inputs[socket], tag=me+":"+name+":input:int"+str(i))
                    set_node_colors(tmp, ["node_socket_object_color", "node_socket_object_color"],
                                    [d.mvNodeCol_Pin, d.mvNodeCol_PinHovered])
                    set_item_color(t, "node_grid_background_color", d.mvThemeCol_FrameBg)
                    set_font_size(t,-1)
                    d.set_item_user_data(t,name+":static:bool"+str(i)+":")
                elif socket.startswith( "bool"):
                    t=d.add_text(default_value=inputs[socket], tag=me+":"+name+":input:bool"+str(i))
                    set_node_colors(tmp, ["node_socket_boolean_color", "node_socket_boolean_color"],
                                    [d.mvNodeCol_Pin, d.mvNodeCol_PinHovered])
                    set_font_size(t,-1)
                    d.set_item_user_data(t,name+":static:bool"+str(i)+":")
                elif socket.startswith( "trigger"):
                    t=d.add_text(default_value=inputs[socket], tag=me+":"+name+":input:trigger"+str(i))
                    set_node_colors(tmp, ["node_socket_trigger_color", "node_socket_trigger_color"],
                                    [d.mvNodeCol_Pin, d.mvNodeCol_PinHovered])
                    set_font_size(t,-1)
                    d.set_item_user_data(t,name+":static:bool"+str(i)+":")
        for socket in static.keys():
            i += 1
            with d.node_attribute(attribute_type=d.mvNode_Attr_Static,
                                  tag=me+":"+name+":statics:"+str(i)) as tmp:
                d.set_item_user_data(tmp,name+":static:"+str(i)+":")
                if socket.startswith( "float"):
                    t= d.add_input_float(label=static[socket],step=0, tag=me+":"+name+":static:float"+str(i)+":", callback=updateTag,
                                            width=40)
                    set_item_color(t, "node_grid_background_color", d.mvThemeCol_FrameBg)
                    set_node_colors(tmp, ["node_socket_object_color", "node_socket_object_color"],
                                    [d.mvNodeCol_Pin, d.mvNodeCol_PinHovered])
                    set_font_size(t,-1)
                    statics.append(t)

                if socket.startswith( "combo"):
                    t= d.add_combo(label=static[socket],items=combo_items[socket+static[socket]], tag=me+":"+name+":static:combo"+str(i)+":", callback=updateTag,
                                            width=100)
                    set_item_colors(t, ["button_alt_color", "window_background_color"],
                        [d.mvThemeCol_Text, d.mvThemeCol_PopupBg])
                    set_node_colors(tmp, ["node_socket_object_color", "node_socket_object_color"],
                                    [d.mvNodeCol_Pin, d.mvNodeCol_PinHovered])
                    set_item_color(tmp, "window_background_color", d.mvThemeCol_FrameBg)
                    set_font_size(t,-1)
                    statics.append(t)

                elif socket.startswith( "int"):
                    t=d.add_input_int(label=static[socket],step=0, tag=me+":"+name+":static:int"+str(i)+":", callback=updateTag,
                                            width=40)
                    set_node_colors(tmp, ["node_socket_object_color", "node_socket_object_color"],
                                    [d.mvNodeCol_Pin, d.mvNodeCol_PinHovered])
                    set_item_color(t, "node_grid_background_color", d.mvThemeCol_FrameBg)
                    set_font_size(t,-1)
                    statics.append(t)

                elif socket.startswith( "bool"):
                    t=d.add_checkbox(label=static[socket], callback=updateTag, tag=me+":"+name+":static:bool"+str(i))
                    set_node_colors(tmp, ["node_socket_boolean_color", "node_socket_boolean_color"],
                                    [d.mvNodeCol_Pin, d.mvNodeCol_PinHovered])
                    set_font_size(t,-1)
                    statics.append(t)

                elif socket.startswith( "trigger"):
                    t=d.add_text(default_value=static[socket], tag=me+":"+name+":static:trigger"+str(i))
                    set_node_colors(tmp, ["node_socket_trigger_color", "node_socket_trigger_color"],
                                    [d.mvNodeCol_Pin, d.mvNodeCol_PinHovered])
                    set_font_size(t,-1)
                    statics.append(t)

    g.window_widgets_skill.active_nodes.append(f)
    g.window_widgets_skill.node_desc[f] = desc
    return [f,t]
    
def updateTag(which, app_data, user_data):
    n = d.get_item_alias(d.get_item_parent(which))
    n = n.split(":")
    i = d.get_item_alias(d.get_item_parent(d.get_item_parent(which))).split(":")[0]
    n[3] = app_data
    n[0] = i
    t = ":".join(str(x) for x in n)
    g.skill_editor_skill_statics[i] = t

def PrintSkillDebug():
    try:
        if g.debug:
            g.skill_editor_skill.PrettyPrint()
    except Exception as e:
        print(e)
    