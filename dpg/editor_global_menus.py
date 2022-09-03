import dearpygui.dearpygui as d
from globals import globals as g
from ui_layout_helpers import BuildTable
from ui_item_style_helpers import *

class Widgets():
    pass

def buildEditorMenu(parent):
    tmp = Widgets()
    BuildTable(tmp,[30,30,30], parent)
    editors = [
        "Unit Editor", "Skill Editor", "Class Editor",
        "World Map Editor", "Level Editor", "Dialogue Editor",
        "Game Options", "Menus Editor", "Music Editor",
        "Events Editor", "Export", "Load Resources"
    ]
    i = -1
    for x in ["node_selected_color", "node_socket_trigger_color",  "node_socket_file_color",
              "node_socket_object_color", "node_socket_number_color", "node_socket_text_color",
              "node_socket_list_color", "unit_editor_slider_color_1", "unit_editor_slider_color_0",
              "node_outliner_label_0", "node_outliner_label_1", "node_outliner_label_2"]:
        i += 1
        t = d.add_button(label = editors[i], parent=tmp.columns[i%3], width=160*(g.text_size/18.0), callback=SwitchEditors)
        d.set_item_user_data(t, editors[i])
        set_item_colors(t, [x, "black"],
                        [d.mvThemeCol_Button, d.mvThemeCol_Text])
    
    
def SwitchEditors(sender, app_data, user_data):
    if user_data == "Skill Editor":
        d.set_primary_window("skill_editor", True)
        g.active_window = "skill_editor"