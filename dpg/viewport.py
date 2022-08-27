import dearpygui.dearpygui as dpg
from screeninfo import get_monitors
from globals import globals as g

def init_viewport(use_screeninfo=True):
    dpg.create_context()
    if use_screeninfo:
        for m in get_monitors():
            if m.is_primary:
                screen_width = m.width
                screen_height = m.height

        dpg.create_viewport(title='Turnroot 0.0.1', width=int(screen_width*0.75), height=int(screen_height*0.75), clear_color=(25, 25, 25), x_pos = int(screen_width * .125), y_pos = int(screen_height * .125))
    else:
        dpg.create_viewport(title='Turnroot 0.0.1', width=800, height=600, clear_color=(25, 25, 25), x_pos = 0, y_pos = 0)
        

    with dpg.window(tag="unit_editor", label = "unit_editor", width = 600, height = 600):
        pass

    if g.debug:
        dpg.show_item_registry()
        dpg.show_debug()
        dpg.show_metrics()


    dpg.setup_dearpygui()
    dpg.show_viewport()

        