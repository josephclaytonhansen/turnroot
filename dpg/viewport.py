import dearpygui.dearpygui as dpg
from screeninfo import get_monitors
from globals import globals as g

def init_viewport(use_screeninfo=True):
    if use_screeninfo:
        for m in get_monitors():
            if m.is_primary:
                screen_width = m.width
                screen_height = m.height

        dpg.create_viewport(title='Turnroot 0.0.1', width=int(screen_width*0.75), height=int(screen_height*0.75), clear_color=g.clear_color, x_pos = int(screen_width * .125), y_pos = int(screen_height * .125))
    else:
        dpg.create_viewport(title='Turnroot 0.0.1', width=800, height=600, clear_color=(25, 25, 25), x_pos = 0, y_pos = 0)
        

    with dpg.window(tag="unit_editor", label = "unit_editor", width = 600, height = 600):
        pass

    with dpg.viewport_menu_bar():

        with dpg.menu(label="Settings"):
            dpg.add_menu_item(label="Setting 1", callback=None, check=True)
            dpg.add_menu_item(label="Setting 2", callback=None)
            dpg.add_checkbox(label="Pick Me", callback=None)

    if g.debug:
        dpg.show_item_registry()
        dpg.show_debug()
        dpg.show_metrics()
        dpg.show_style_editor()


    dpg.setup_dearpygui()
    dpg.show_viewport()

        