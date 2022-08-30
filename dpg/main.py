from viewport import *
from unit_editor import add_unit_editor, ue_do
import dearpygui.dearpygui as d
from ui_set_global_colors import set_colors
from ui_set_global_font import set_fonts
from globals import globals as g
from editor_data_handling import LoadUserPrefs

d.create_context()
LoadUserPrefs()
d.bind_theme(set_colors(g.color_theme))

init_viewport(True)
print(g.font_family)
set_fonts()   

add_unit_editor()


while d.is_dearpygui_running():
    d.render_dearpygui_frame()
    ue_do()
    
d.destroy_context()