from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import src.UI_colorTheme as UI_colorTheme
from src.UI_updateJSON import updateJSON
import json
data = updateJSON()
active_theme = getattr(UI_colorTheme, data["active_theme"])

with open("src/tmp/nenc.json", "r") as readfile:
    const = json.load(readfile)

NODE_FONT = const[5]
FONT_SIZE = int(const[6]) / 2

class OutlinerGraphicsListItem(QGraphicsItem):
    def __init__(self, list_item, parent=None):
        super().__init__(parent)
        self.list_item = list_item
        self.width = 800
        self.height = FONT_SIZE * 2.5
        self.padding = 10
        
        self.initContent()
        self.initUI()
        self.text = self.list_item.path
        
        active_theme = getattr(UI_colorTheme, data["active_theme"])

        self.brush_background = QBrush(QColor(active_theme.node_background_color))
        self.brush_selected = QBrush(QColor(active_theme.node_selected_color))
    
    def initContent(self):
        self.path_color = QColor(active_theme.node_title_color)
        self.path_font = QFont(NODE_FONT)
        self.path_font.setPointSize(FONT_SIZE)
        self.path_item = QGraphicsTextItem(self)
        self.path_item.list_item = self.list_item
        self.path_item.setPlainText(self.list_item.path)
        self.path_item.setDefaultTextColor(self.path_color)
        self.path_item.setFont(self.path_font)
        self.path_item.setPos(self.padding, 0)
        self.path_item.setTextWidth(self.width-3*self.padding)
    
    def boundingRect(self):
        return QRectF(0,0,self.width,
                      self.height).normalized()

    def initUI(self):
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        content = QPainterPath()
        content.setFillRule(Qt.WindingFill)
        content.addRect(0,0,self.width,self.height)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.brush_background if not self.isSelected() else self.brush_selected)
        painter.drawPath(content.simplified())

class OutlinerListItem():
    def __init__(self, scene, path="/path/", depth = 0):
        super().__init__()
        self.scene = scene
        self.indent = depth
        self.path = path
        
        if self.indent > 0:
            self.collapse = True
        else:
            self.collapse = False
        
        self.grListItem = OutlinerGraphicsListItem(self)
        
        self.scene.addListItem(self)
        self.scene.grScene.addItem(self.grListItem)
    
    def setPos(self,x,y):
        self.grListItem.setPos(x,y)