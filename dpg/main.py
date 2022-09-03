from viewport import *
from unit_editor import add_unit_editor, ue_do
from skill_editor import add_skill_editor, se_do
import dearpygui.dearpygui as d
from ui_set_global_colors import set_colors
from ui_set_global_font import set_fonts
from globals import globals as g
from editor_data_handling import LoadUserPrefs
from datetime import datetime

d.create_context()
LoadUserPrefs()
d.bind_theme(set_colors(g.color_theme))

init_viewport(True)

if g.fullscreen:
    d.maximize_viewport()
    d.toggle_viewport_fullscreen()

set_fonts()   

add_unit_editor()
add_skill_editor()

while d.is_dearpygui_running():
    d.render_dearpygui_frame()
    if g.is_editing.type == "unit":
        ue_do()
    elif g.is_editing.type == "skill":
        se_do()
    g.now = datetime.now()
    
d.destroy_context()