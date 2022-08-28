from viewport import *
from unit_editor import add_unit_editor
import dearpygui.dearpygui as d
from ui_set_global_colors import set_colors
from ui_set_global_font import set_fonts
from globals import globals as g
from editor_data_handling import LoadUserPrefs

d.create_context()
LoadUserPrefs()
    
d.bind_theme(set_colors(g.color_theme))
set_fonts()    

init_viewport(True)
add_global_menu()

add_unit_editor()
    
d.start_dearpygui()
d.destroy_context()