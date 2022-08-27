from viewport import init_viewport
from unit_editor import add_unit_editor
import dearpygui.dearpygui as dpg
from ui_set_global_colors import set_colors
from ui_set_global_font import set_fonts
import ui_colorthemes
from globals import globals as g

dpg.create_context()

dpg.bind_theme(set_colors(g.color_theme))
set_fonts()
init_viewport(True)
add_unit_editor()



if not g.debug:
    dpg.set_primary_window("unit_editor", True)
    
dpg.start_dearpygui()
dpg.destroy_context()