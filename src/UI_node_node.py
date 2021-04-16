from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import UI_colorTheme
from UI_updateJSON import updateJSON
data = updateJSON()


class QDMGraphicsNode(QGraphicsItem):
    def __init__(self, node, parent=None):
        super().__init__(parent)
        self.initTitle()
        self.initUI()
        active_theme = getattr(UI_colorTheme, data["active_theme"])
        self.node = node
        self.title = self.node.title
        
        self.width = 180*2.5
        self.height = 240*2.5
        self.edge_size = 10.0
        
        self.pen_default = QPen(QColor("#7f000000"))
        self.pen_selected = QPen(QColor(active_theme.node_selected_color))
        self.pen_selected.setWidth(3)
        
    def boundingRect(self):
        return QRectF(0,0,2*self.edge_size+self.width,
                      2*self.edge_size+self.height).normalized()

    def initUI(self):
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
    
    def initTitle(self):
        active_theme = getattr(UI_colorTheme, data["active_theme"])
        self._title_color = QColor(active_theme.node_title_color)
        self._title_font = QFont("Lucida Sans Unicode")
        self._title_font.setPointSize(22)
        self._title_font.setStyleStrategy(QFont.NoAntialias)
        self.title_item = QGraphicsTextItem(self)
        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setFont(self._title_font)
        
    @property
    def title(self): return self._title
    @title.setter
    def title(self, value):
        self._title = value
        self.title_item.setPlainText(self._title)
    
    def paint(self, QPainter, QStyleOptionGraphicsItem, widget=None):
        painter = QPainter
        path_outline = QPainterPath()
        path_outline.addRoundedRect(0,0,self.width,self.height,self.edge_size, self.edge_size)
        painter.setPen(self.pen_default if not self.isSelected() else self.pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path_outline.simplified())
              
class Node():
    def __init__(self, scene, title="undefined node"):
        self.scene = scene
        
        self.title = title
        
        self.grNode = QDMGraphicsNode(self)
        
        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)
        self.inputs = []
        self.outputs = []
        
        
