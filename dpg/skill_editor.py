import dearpygui.dearpygui as d
from ui_layout_helpers import *
from globals import globals as g
from ui_item_style_helpers import *
import skill_editor_functions as c_skill
from ui_colorthemes import colorthemes as themes
from editor_save_load_skill import SaveSkill
from ui_skill_editor_populates import *
import sys
from universal_weapon_types import universal_weapons as uw
from editor_global_menus import buildEditorMenu

g.window_widgets_skill = w_skill
g.uw = uw()

class Skill():
    data = {"pos":None, "con":None, "sta":None, "awn":None}
    def PrettyPrint(self):
        print(
        "\n\n\n----------Current Skill Data----------\n",
        "Positions:\t"+str(self.data["pos"]),
        "\nConnections:\t"+str(self.data["con"]),
        "\nStatics:\t"+str(self.data["sta"]),
        "\nActive nodes:\t"+str(self.data["awn"]),
    )

class Colors():
    def set(self):
        set_item_color(w_skill.font_size, "node_grid_background_color", d.mvThemeCol_FrameBg)
        
        for x in [w_skill.theme_menu, w_skill.font]:
            set_item_colors(x, ["window_background_color", "button_alt_color"],
                        [d.mvThemeCol_Text, d.mvThemeCol_PopupBg])
            
        
        for x in [w_skill.padding, w_skill.window_padding,
                  w_skill.item_spacing, w_skill.corners_round, w_skill.autosave]:
            set_item_colors(x, ["window_background_color", "window_background_color", "list_background_color"],
                        [d.mvThemeCol_FrameBg, d.mvThemeCol_FrameBgHovered, d.mvThemeCol_FrameBgActive])

w_skill.colors = Colors()


def make_functions():
       d.set_item_user_data(w_skill.theme_menu, w_skill)

def skill_editor_set_wrap():
    d.configure_item(w_skill.info_left, width=d.get_viewport_width()-700)
    d.configure_item(w_skill.node_information, wrap=int((.12 * d.get_viewport_width())))
    d.configure_item(w_skill.instructions, wrap=int((.12 * d.get_viewport_width())))

def add_skill_editor(params={}):
    buildSkillEditor()
    populateSkillEditor()
    add_menu()
    # unit_editor_centers_in_column()
    make_functions()
    w_skill.colors.set()
    g.editors.append("skill_editor")
    #remove this in favor of save/load, temporarily for dev
    s = Skill()
    g.skill_editor_skill = s
    g.skill_editor_skill_connections = []
    g.skill_editor_skill_positions = {}
    g.skill_editor_skill_statics = {}
    
    #you can only be editing one thing at a time, technically, so this works
    g.path = ""
    TimedEvent(g.autosave_time)

def add_menu():
    w_skill.status_bar = None
    with d.menu_bar(parent="skill_editor"):
        with d.menu(label="Editor") as e:
            buildEditorMenu(e)
            
        with d.menu(label="File"):
            d.add_menu_item(label="Open", tag="skillopen", callback=c_skill.ShowFileDialog)
            d.add_menu_item(label="New", tag="skillnew", callback=c_skill.NewSkillFile)
            d.add_menu_item(label="Save", callback=lambda:(SaveSkill(g.path),TimedInfoMessage("Skill saved", w_skill.status_bar, 2)), tag="skillsave")
            d.set_item_user_data("skillsave", "user data")
            d.add_menu_item(label="Save As", callback=c_skill.ShowFileDialog)
            d.add_menu_item(label="Exit", callback=lambda:sys.exit())
            
        with d.menu(label="View"):
            d.add_checkbox(label="Fullscreen", callback=c_skill.fullscreen, tag="skillfullscreen", default_value=False)
            w_skill.theme_menu_label = d.add_text("Color theme:")
            set_item_style(w_skill.theme_menu_label, 0, d.mvStyleVar_ItemSpacing)
            set_font_size(w_skill.theme_menu_label, -1)
            w_skill.theme_menu = d.add_combo(default_value=g.color_theme.tag,
                                       items=[themes[t].tag for t in themes],
                                       callback=c_skill.color_theme)          
            w_skill.font_size_label = d.add_text("Font size/Font (requires restart)")
            set_font_size(w_skill.font_size_label, -1)
            set_item_style(w_skill.font_size_label, 0, d.mvStyleVar_ItemSpacing)
            
            with d.group(horizontal=True):
                w_skill.font_size = d.add_input_int(min_clamped=True,max_clamped=True,
                                            min_value=4,max_value=36, step =0, width = 30,
                                            callback=c_skill.font_size, default_value=g.text_size)
                w_skill.font = d.add_combo(items=["FiraCode","FiraSans","Montserrat","NotoSans"],callback=c_skill.font,width=-1,
                                     default_value=g.font_family.split("/")[2].split("-")[0])
            
            w_skill.padding_label = d.add_text("Padding/Item Spacing/Window Padding")
            set_font_size(w_skill.padding_label, -1)
            set_item_style(w_skill.padding_label, 0, d.mvStyleVar_ItemSpacing)
            
            with d.group(horizontal=True,width=80):
                w_skill.padding = d.add_input_int(min_clamped=True,max_clamped=True,
                                          min_value=0,max_value=30,step=0,
                                          callback=c_skill.padding, default_value=g.padding)
                w_skill.item_spacing = d.add_input_int(min_clamped=True,max_clamped=True,
                                          min_value=0,max_value=30,step=0,
                                          callback=c_skill.item_spacing, default_value=g.item_spacing)
                w_skill.window_padding = d.add_input_int(min_clamped=True,max_clamped=True,
                                          min_value=0,max_value=30,step=0,
                                          callback=c_skill.window_padding, default_value=g.window_padding)
            
            w_skill.corners_round_label = d.add_text("Corners rounded amount")
            set_font_size(w_skill.corners_round_label, -1)
            set_item_style(w_skill.corners_round_label, 0, d.mvStyleVar_ItemSpacing)
            
            w_skill.corners_round = d.add_slider_int(clamped=True,
                                            min_value=0,max_value=10,
                                            callback=c_skill.corners_round, default_value=g.corners_round)
            
            w_skill.autosave_label = d.add_text("Autosave interval (in seconds)")
            set_font_size(w_skill.autosave_label, -1)
            set_item_style(w_skill.autosave_label, 0, d.mvStyleVar_ItemSpacing)
            
            w_skill.autosave = d.add_input_int(min_clamped=True,max_clamped=True,
                                          min_value=15,max_value=600,step=15,
                                          callback=c_skill.ChangeAutosave, default_value=g.autosave_time)
        
        w_skill.info_left = d.add_spacer(width=0)
        with d.menu(label="",enabled=False) as w_skill.status_bar:
            pass

def se_do():
    if g.is_editing.type == "skill":
        try:
            for i in g.skill_editor_skill_positions.keys():
                if g.skill_editor_skill_positions[i] == None:
                    g.skill_editor_skill_positions.pop(i, None)
        except:
            pass
        node_is_hovered = False
        for node in w_skill.active_nodes:
            i = node.split(":")[0]
            try:
                g.skill_editor_skill_positions[i] = d.get_item_pos(node)
            except:
                g.skill_editor_skill_positions[i] = None
            try:
                if d.is_item_hovered(node):
                    d.set_value(w_skill.node_information, w_skill.node_desc[node])
                    node_is_hovered = True
                if not node_is_hovered:
                    try:
                        d.set_value(w_skill.node_information, "Hover over a node to learn more about it")
                    except:
                        pass
            except:
                pass

        try:
            if g.now > g.timeout_event:
                TimedEvent(g.autosave_time)
                TimedInfoMessage("Auto-saved skill file to "+g.path, w_skill.status_bar, 3)
                SaveSkill(g.path)
        except Exception as e:
            print(e)

        try:
            if g.now > g.timeout:
                if g.path == "":
                    d.configure_item(w_skill.status_bar, label="File not saved")
                else:
                    d.configure_item(w_skill.status_bar, label="")
        except:
                if g.path == "":
                    d.configure_item(w_skill.status_bar, label="File not saved")
                else:
                    d.configure_item(w_skill.status_bar, label="")
        
    else:
        pass