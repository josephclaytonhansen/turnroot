import dearpygui.dearpygui as d
from screeninfo import get_monitors
from globals import globals as g
from unit_editor import unit_editor_update_height, unit_editor_centers_in_column, ue_arrange, ue_no_arrange

def getGeometry():
    g.current_height = d.get_viewport_client_height()
    unit_editor_update_height()
    unit_editor_centers_in_column()

def add_global_menu():
    with d.viewport_menu_bar():
        with d.menu(label="Settings"):
            d.add_menu_item(label="Setting 1", callback=None, check=True)
            d.add_menu_item(label="Setting 2", callback=None)
            d.add_checkbox(label="Pick Me", callback=None)

def init_viewport(use_screeninfo=True):
    d.set_viewport_resize_callback(callback=getGeometry)
    if use_screeninfo:
        for m in get_monitors():
            if m.is_primary:
                screen_width = m.width
                screen_height = m.height

        d.create_viewport(title='Turnroot 0.0.1', width=int(screen_width*0.75), height=int(screen_height*0.75), clear_color=g.clear_color, x_pos = int(screen_width * .125), y_pos = int(screen_height * .125))
    else:
        d.create_viewport(title='Turnroot 0.0.1', width=800, height=600, clear_color=(25, 25, 25), x_pos = 0, y_pos = 0)
        
    with d.window(tag="unit_editor", label = "unit_editor", width = 600, height = 600, no_collapse=True, min_size=[300,300]):
        pass

    if g.debug:
        d.show_item_registry()
        d.show_debug()
        d.show_metrics()
        d.show_style_editor()

    d.setup_dearpygui()
    d.show_viewport()
    d.set_primary_window("unit_editor", True)

#This should be a toolbar/menu button - allows layouts to drap and drop columns
def global_arrange():
    ue_arrange()

def global_no_arrange():
    ue_no_arrange()
        