from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import src.UI_colorTheme as UI_colorTheme
from src.UI_updateJSON import updateJSON
data = updateJSON()
active_theme = getattr(UI_colorTheme, data["active_theme"])

AND = 0
OR = 1
ALL = 2

class OutlinerGraphicsScene(QGraphicsScene):
    def __init__(self,scene,parent=None):
        super().__init__(parent)
        
        self.scene = scene
        
        self.filter_view_update = False
        self.refresh_files = False
        self.filter_mode = ALL
        
        self.file_selection_path = None

        self.active_theme = getattr(UI_colorTheme, data["active_theme"])
        
        self.scene_width = 400
        self.scene_height = 1660
    
        self._color_background = QColor(self.active_theme.node_grid_background_color)

        self.setSceneRect(-self.scene_width//2, -self.scene_height//2, self.scene_width, self.scene_height)
        
        self.setBackgroundBrush(self._color_background)
        
    def setGrScene(self, width, height):
        self.setSceneRect(-width//2, -height //2, width, height)