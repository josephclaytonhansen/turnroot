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
        elif self.pos == 3:
            self.color = QColor(active_theme.node_outliner_label_3)


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

class Flag_Filter():
    def __init__(self, outliner_header, position=LEFT):
        super().__init__()
        self.outliner_header = outliner_header
        self.position = position
        self.on = False
        
        self.color = FlagColor(self.position)
        self.grFlag = OutlinerGraphicFlag_Filter(self, self.color)
        self.grFlag.setPos(*self.outliner_header.getFlagPosition(position))
        
    def getFlagPosition(self):
        res = self.outliner_header.getFlagPosition(self.position)
        return res
    
class FilterButton():
    def __init__(self, outliner_header, position=LEFT, label = ""):
        super().__init__()
        
        self.outliner_header = outliner_header
        self.position = position
        self.on = False
        self.label = label
        self.color = QColor(active_theme.node_grid_background_color)
        self.grButton = OutlinerGraphicButton(self, self.color)
        self.grButton.setPos(*self.outliner_header.getButtonPosition(position))
        
        self.initTitle()
        
    def getButtonPosition(self):
        res = self.outliner_header.getButtonPosition(self.position)
        return res
    
            
    def determineTextColor(self,color):
        lightness = color.lightness()
        if lightness > 127:
            return True
        else:
            return False
    
    def initTitle(self):
        active_theme = getattr(UI_colorTheme, data["active_theme"])
        self._title_color = QColor(active_theme.node_title_background_color)
        self._title_font = QFont("Lucida Sans Unicode")
        self._title_font.setPointSize(15)

        self.title_item = QGraphicsTextItem(self.grButton)
        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setFont(self._title_font)
        self.title_item.setPos(-12, -3)
        self.title_item.setPlainText(self.label)
        
class OutlinerGraphicFlag(QGraphicsItem):
    def __init__(self, flag, color):
        super().__init__(flag.list_item.grListItem)
        self.color = color
        self.flag = flag
        
        if self.flag.index % 2 == 0:
            self.off_color = QBrush(QColor(active_theme.node_background_color))
            self.pen = QPen(QColor(active_theme.node_background_color).lighter(130))
        else:
            self.off_color = QBrush(QColor(active_theme.node_title_background_color))
            self.pen = QPen(QColor(active_theme.node_title_background_color).lighter(130))
        
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
        
class OutlinerGraphicFlag_Filter(QGraphicsItem):
    def __init__(self, flag, color):
        super().__init__(flag.outliner_header.grHeaderItem)
        self.color = color
        self.flag = flag
        
        self.off_color = QBrush(QColor(active_theme.window_background_color))
        self.pen = QPen(QColor(active_theme.window_background_color).lighter(130))
        
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
    
class OutlinerGraphicButton(QGraphicsItem):
    def __init__(self, flag, color):
        super().__init__(flag.outliner_header.grHeaderItem)
        self.color = color
        self.flag = flag
        
        self.off_color = QBrush(QColor(active_theme.node_grid_background_color))
        
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.on_color = QBrush(QColor(active_theme.node_selected_color))
    
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        path_title = QPainterPath()
        painter.setBrush(self.off_color if not self.isSelected() else self.on_color)
        painter.setPen(Qt.NoPen)
        path_title.addRoundedRect(-10,-5,35,30, 1,1)
        painter.drawPath(path_title.simplified())

        
    def boundingRect(self):
        return QRectF(-10,
                      -10,
                      35,
                      30)

