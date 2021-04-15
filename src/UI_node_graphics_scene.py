from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import UI_colorTheme
from UI_updateJSON import updateJSON
import math

data = updateJSON()

class QDMGraphicsScene(QGraphicsScene):
    def __init__(self,parent=None):
        super().__init__(parent)
        
        self.active_theme = getattr(UI_colorTheme, data["active_theme"])
        self.gridSize = 20
    
        self._color_background = QColor(self.active_theme.node_grid_background_color)
        self._color_light = QColor(self.active_theme.node_grid_lines_color)
        self._color_dark = QColor(self.active_theme.node_grid_alt_lines_color)
        
        self._pen_light = QPen(self._color_light)
        self._pen_dark = QPen(self._color_dark)
        self._pen_light.setWidth(1)
        self._pen_dark.setWidth(2)
        
        self.scene_width, self.scene_height = 64000, 64000
        self.setSceneRect(-self.scene_width//2, -self.scene_height//2, self.scene_width, self.scene_height)
        
        self.setBackgroundBrush(self._color_background)
    
    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)
        
        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))
        
        first_left = left - (left % self.gridSize)
        first_top = top - (top % self.gridSize)
        
        lines_light, lines_dark = [], []
        for x in range(first_left, right, self.gridSize):
            if x % 100 == 0:
                lines_dark.append(QLine(x,top,x,bottom))
            else:
                lines_light.append(QLine(x,top,x,bottom))
        
        for y in range(first_top, bottom, self.gridSize):
            if y % 100 == 0:
                lines_dark.append(QLine(left,y,right,y))
            else:
                lines_light.append(QLine(left,y,right,y))
            
        painter.setPen(self._pen_light)
        painter.drawLines(*lines_light)
        
        painter.setPen(self._pen_dark)
        painter.drawLines(*lines_dark)
        