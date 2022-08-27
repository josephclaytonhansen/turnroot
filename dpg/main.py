from viewport import init_viewport
from unit_editor import add_unit_editor
import dearpygui.dearpygui as dpg

init_viewport(True)
add_unit_editor()

dpg.start_dearpygui()
dpg.destroy_context()