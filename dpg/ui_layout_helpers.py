import dearpygui.dearpygui as d
from globals import globals as g
from datetime import datetime, timedelta

from ui_item_style_helpers import set_item_color

def ImageToTexture(path):
    width, height, channels, data = d.load_image(path)
    with d.texture_registry():
        texture_id = d.add_static_texture(width, height, data)
    return texture_id

def TimedInfoMessage(message, status_bar, time=4):
    g.timeout = datetime.now() + timedelta(seconds=time)
    d.configure_item(status_bar, label=message)
    set_item_color(status_bar, "node_selected_color", d.mvThemeCol_TextDisabled)

def TimedEvent(time=5):
    g.timeout_event = datetime.now() + timedelta(seconds=time)
    
class PercentageBasedLayoutHelper:
    def __init__(self, parent=""):
        self.table_id = d.add_table(header_row=False, policy=d.mvTable_SizingStretchProp, parent=parent)
        self.stage_id = d.add_stage()
        d.push_container_stack(self.stage_id)
        
    def add_widget(self, uuid, percentage, w=True):
        d.add_table_column(init_width_or_weight=percentage/100.0, width=percentage/100.0, parent=self.table_id)
        if w == True:
            d.set_item_width(uuid, -1)
        return uuid

    def add_column(self,percentage):
        g = d.add_table_column(init_width_or_weight=percentage/100.0, width=percentage/100.0, parent=self.table_id)
        print(d.get_item_configuration(g))
        return g

    def submit(self):
        d.pop_container_stack() # pop stage
        with d.table_row(parent=self.table_id):
            d.unstage(self.stage_id)

def buildUnitEditor():
    g.unit_editor_rows = []
    g.unit_editor_cells = []

    with d.table(reorderable=False,header_row=False, resizable=False, policy=d.mvTable_SizingStretchProp,
                borders_outerH=g.debug, borders_innerV=g.debug, borders_innerH=g.debug, borders_outerV=g.debug, parent = "unit_editor") as g.unit_editor_table:

        d.add_table_column(init_width_or_weight=.50-(g.item_spacing/170))
        d.add_table_column(init_width_or_weight=.0+((g.item_spacing/170)/2))
        d.add_table_column(init_width_or_weight=.50-(g.item_spacing/170))
        
        for i in range(0, 1, 2):
            with d.table_row(height=6) as f:
                g.unit_editor_rows.append(f)
                for j in range(0, 3):
                    with d.table_cell() as cell:
                        g.unit_editor_cells.append(cell)
        
        g.unit_editor_left = g.unit_editor_cells[0]
        g.unit_editor_gutter = g.unit_editor_cells[1]
        g.unit_editor_right = g.unit_editor_cells[2]

def BuildTable(cont, widths, parent):
    cont.rows = []
    cont.cells = []

    with d.table(reorderable=False,header_row=False, resizable=False, policy=d.mvTable_SizingStretchProp,
                borders_outerH=g.debug, borders_innerV=g.debug, borders_innerH=g.debug, borders_outerV=g.debug, parent = parent):

        for x in range(0, len(widths)):
            d.add_table_column(init_width_or_weight=widths[x]-(g.item_spacing/170))
        
        for i in range(0, len(widths)):
            if i == len(widths) - 1:
                with d.table_row(height=6) as f:
                    cont.rows.append(f)
                    for j in range(0, len(widths)):
                        with d.table_cell() as cell:
                            cont.cells.append(cell)
        
        cont.columns = cont.cells