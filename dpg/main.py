from viewport import init_viewport
from unit_editor import add_unit_editor
import dearpygui.dearpygui as dpg
from ui_set_global_colors import set_colors
import ui_colorthemes
from globals import globals as g

init_viewport(True)
add_unit_editor()

dpg.bind_theme(set_colors(ui_colorthemes.ocean_waves()))
dpg.set_primary_window("unit_editor", True)
dpg.start_dearpygui()
dpg.destroy_context()