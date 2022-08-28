import dearpygui.dearpygui as d
from viewport import EditorGlobals
from globals import globals as g

class PercentageBasedLayoutHelper:
    def __init__(self, parent=""):
        self.table_id = d.add_table(header_row=False, policy=d.mvTable_SizingStretchProp, parent=parent)
        self.stage_id = d.add_stage()
        d.push_container_stack(self.stage_id)
        
    def add_widget(self, uuid, percentage, w=True):
        d.add_table_column(init_width_or_weight=percentage/100.0, parent=self.table_id)
        if w == True:
            d.set_item_width(uuid, -1)
        return uuid

    def submit(self):
        d.pop_container_stack() # pop stage
        with d.table_row(parent=self.table_id):
            d.unstage(self.stage_id)

def buildUnitEditor():
    g.unit_editor_rows = []
    g.unit_editor_cells = []
    g.u = EditorGlobals()

    with d.table(header_row=False, resizable=False, policy=d.mvTable_SizingStretchSame,
                borders_outerH=False, borders_innerV=False, borders_innerH=False, borders_outerV=False, parent = "unit_editor"):

        d.add_table_column(init_width_or_weight=.5)
        d.add_table_column(init_width_or_weight=.5)

        # once it reaches the end of the columns
        
        for i in range(0, 1):
            with d.table_row(height=6) as f:
                g.unit_editor_rows.append(f)
                for j in range(0, 3):
                    with d.table_cell() as cell:
                        g.unit_editor_cells.append(cell)
        
        g.unit_editor_left = g.unit_editor_cells[0]
        g.unit_editor_right = g.unit_editor_cells[1]