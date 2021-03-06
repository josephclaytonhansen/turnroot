from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import src.UI_colorTheme as UI_colorTheme
from src.UI_updateJSON import updateJSON
from src.UI_node_outliner_label import Flag
import json, os
data = updateJSON()
active_theme = getattr(UI_colorTheme, data["active_theme"])

if os.sep != "\\":
    const_path = "src/tmp/nenc.json"
    with open(const_path, "r") as readfile:
        const = json.load(readfile)
    NODE_FONT = "Lucida Grande"
else:
    const_path = "src\\tmp\\nenc.json"
    with open(const_path, "r") as readfile:
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
        
        self.text = self.list_item.path
        self.index = self.list_item.index
        self.selected_text_dark = None
        self.selected_dark = None
        
        self.initContent()
        self.initUI()

        active_theme = getattr(UI_colorTheme, data["active_theme"])

        if self.index % 2 == 0:
            self.brush_background = QBrush(QColor(active_theme.node_background_color))
        else:
            self.brush_background = QBrush(QColor(active_theme.node_title_background_color))
            
        self.brush_selected = QBrush(QColor(active_theme.node_selected_color))
        
    
    def initContent(self):
        self.path_color = QColor(active_theme.node_title_color)
        self.selected_dark = self.determineTextColor(QColor(active_theme.node_selected_color))
        self.selected_text_dark = self.determineTextColor(QColor(active_theme.node_title_color))

        if self.selected_text_dark == self.selected_dark:
            if self.selected_dark == False:
                self.selected_color = QColor("white")
            else:
                self.selected_color = QColor("black")
        else:
            self.selected_color = QColor(active_theme.node_title_color)
        
        self.path_font = QFont(NODE_FONT)
        self.path_font.setPointSize(FONT_SIZE)
        self.path_item = QGraphicsTextItem(self)
        self.path_item.list_item = self.list_item
        self.path_item.setPlainText(self.list_item.path)
        self.path_item.setDefaultTextColor(QColor(active_theme.node_text_color))
        self.path_item.setFont(self.path_font)
        self.path_item.setPos((self.padding*2)+(self.list_item.indent*20), 0)
        self.path_item.setTextWidth(self.width-3*self.padding)
        self.path_item.setZValue(3)
    
    def boundingRect(self):
        return QRectF(0,0,self.width,
                      self.height).normalized()
    
    def determineTextColor(self,color):
        lightness = color.lightness()
        if lightness > 127:
            return True
        else:
            return False

    def initUI(self):
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        content = QPainterPath()
        content.setFillRule(Qt.WindingFill)
        content.addRect(0,0,self.width,self.height)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.brush_background if not self.isSelected() else self.brush_selected)
            
        if not self.isSelected():
            self.path_item.setDefaultTextColor(self.path_color)
        else:
            self.path_item.setDefaultTextColor(self.selected_color)   
            
        painter.drawPath(content.simplified())

class OutlinerListItem():
    def __init__(self, scene, path="", depth = 0, index = 0, flags = True, parent_scene=None, full_path = None):
        super().__init__()
        self.scene = scene
        self.indent = depth - 1
        self.path = path
        self.full_path = full_path
        self.parent_scene = parent_scene
        self.flags_init = flags
        self.index = index
        self.flags = []
        
        if self.indent > 0:
            self.collapse = True
        else:
            self.collapse = False
        
        self.grListItem = OutlinerGraphicsListItem(self)
        
        if self.flags_init:
            self.flags_status = {}
            for x in range(0,4):
                flag = Flag(list_item=self,position=x,index=self.index)
                self.flags.append(flag)
                self.flags_status[x] = flag.on
                self.scene.grScene.addItem(self.flags[x].grFlag)
        
        self.scene.addListItem(self)
        self.scene.grScene.addItem(self.grListItem)
    
    def setPos(self,x,y):
        self.grListItem.setPos(x,y)
    
    def remove(self):
        for f in self.flags:
            self.scene.grScene.removeItem(f.grFlag)
        self.flags=[]
        self.scene.grScene.removeItem(self.grListItem)
        self.grListItem = None
        self.scene.placement[self.scene.slots[self.index]] = None
        self.scene.removeListItem(self)
        
    def getFlagPosition(self, index, position):
        x = 395 - (position*20+self.grListItem.padding)
        y = (index * self.grListItem.height) + self.grListItem.padding + 54
        return [x, y]