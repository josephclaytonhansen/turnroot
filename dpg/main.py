from viewport import *
from unit_editor import add_unit_editor
import dearpygui.dearpygui as d
from ui_set_global_colors import set_colors
from ui_set_global_font import set_fonts
from globals import globals as g

d.create_context()

d.bind_theme(set_colors(g.color_theme))
set_fonts()
init_viewport(True)
add_global_menu()

add_unit_editor()

if not g.debug:
    d.set_primary_window("unit_editor", True)
    
d.start_dearpygui()
d.destroy_context()