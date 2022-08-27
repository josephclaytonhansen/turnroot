from viewport import init_viewport
from unit_editor import add_unit_editor
import dearpygui.dearpygui as dpg
from ui_set_global_colors import set_colors
from ui_set_global_font import set_fonts
import ui_colorthemes
from globals import globals as g

init_viewport(True)
add_unit_editor()

set_fonts()
dpg.bind_theme(set_colors(ui_colorthemes.ocean_waves()))

if not g.debug:
    dpg.set_primary_window("unit_editor", True)
    
dpg.start_dearpygui()
dpg.destroy_context()