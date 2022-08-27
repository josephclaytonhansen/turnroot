import dearpygui.dearpygui as dpg
from screeninfo import get_monitors


def init_viewport(use_screeninfo=True):
    dpg.create_context()
    if use_screeninfo:
        for m in get_monitors():
            if m.is_primary:
                screen_width = m.width
                screen_height = m.height

        dpg.create_viewport(title='Turnroot 0.0.1', width=screen_width, height=screen_height, clear_color=(25, 25, 25), x_pos = 0, y_pos = 0)
    else:
        dpg.create_viewport(title='Turnroot 0.0.1', width=1920, height=1080, clear_color=(25, 25, 25), x_pos = 0, y_pos = 0)
        

    with dpg.window(tag="unit_editor", label = "unit_editor"):
        pass


    dpg.setup_dearpygui()
    dpg.show_viewport()

        