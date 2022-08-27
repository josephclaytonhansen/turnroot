import dearpygui.dearpygui as d

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
