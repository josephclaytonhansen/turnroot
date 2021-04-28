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
        self.on = False
        self.index = index
        
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
        
        if self.flag.index % 2 == 0:
            self.off_color = QBrush(QColor(active_theme.node_background_color))
            self.pen = QPen(QColor(active_theme.node_background_color).lighter(165))
        else:
            self.off_color = QBrush(QColor(active_theme.node_title_background_color))
            self.pen = QPen(QColor(active_theme.node_title_background_color).lighter(165))
        
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.on_color = QBrush(self.color.color)

        self.selected_pen = QPen(QColor(active_theme.node_selected_color))
        self.selected_pen.setWidth(3)
        self.selected_brush = QBrush(QColor(active_theme.node_selected_color))
        
        self.pen.setWidth(2)
        self.brush = self.off_color
        self.setZValue(2)
        self.show()
    
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        path_title = QPainterPath()
        painter.setBrush(self.off_color if not self.flag.on else self.on_color)
        painter.setPen(self.pen if not self.isSelected() else self.selected_pen)
        path_title.addRoundedRect(-10,-10,14,20, 1,1)
        painter.drawPath(path_title.simplified())
        
    def boundingRect(self):
        return QRectF(-10,
                      -10,
                      14,
                      20)
