from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import src.UI_colorTheme as UI_colorTheme
from src.UI_updateJSON import updateJSON
import json
data = updateJSON()
active_theme = getattr(UI_colorTheme, data["active_theme"])

LEFT = 0
MIDDLE = 1
RIGHT = 2

class FlagColor():
    def __init__(self, pos):
        self.pos = pos
        if self.pos == 0:
            self.color = QColor(active_theme.node_outliner_label_0)
        elif self.pos == 1:
            self.color = QColor(active_theme.node_outliner_label_1)
        elif self.pos == 2:
            self.color = QColor(active_theme.node_outliner_label_2)


class Flag():
    def __init__(self, list_item, position=LEFT, index = 0):
        super().__init__()
        self.list_item = list_item
        self.position = position
        self.on = True
        
        self.color = FlagColor(self.position)
        self.grFlag = OutlinerGraphicFlag(self, self.color)
        self.grFlag.setPos(*self.list_item.getFlagPosition(index, position))
        
    def getFlagPosition(self):
        res = self.list_item.getFlagPosition(self.position)
        return res
        
class OutlinerGraphicFlag(QGraphicsItem):
    def __init__(self, flag, color):
        super().__init__(flag.list_item.grListItem)
        self.color = color
        self.flag = flag
    
        self.pen = QPen(QColor("black"))
        self.pen.setWidth(1)
        self.brush = QBrush(self.color.color)
    
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        painter.setBrush(self.brush)
        painter.setPen(self.pen)
        painter.drawEllipse(-10,-10,10,10)
