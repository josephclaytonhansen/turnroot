from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import src.UI_colorTheme as UI_colorTheme
from src.UI_updateJSON import updateJSON
from src.UI_node_outliner_label import Flag_Filter, FilterButton
import json
data = updateJSON()
active_theme = getattr(UI_colorTheme, data["active_theme"])

class RefreshItem(QGraphicsPixmapItem):
    def __init__(self, QPixmap=None, parent=None):
        super().__init__(parent)
        self.setPixmap(QPixmap)

class OutlinerHeader():
    def __init__(self, scene, parent_scene=None):
        super().__init__()
        self.scene = scene
        self.parent_scene = parent_scene
        self.flags = []
        self.buttons = []
        self.grHeaderItem = OutlinerGraphicsHeader()

        self.scene.addHeader(self)
        self.scene.grScene.addItem(self.grHeaderItem)
        
        self.flags_status = {}
        for x in range(0,4):
            flag = Flag_Filter(outliner_header=self,position=x)
            self.flags.append(flag)
            self.flags_status[x] = flag.on
            self.scene.grScene.addItem(self.flags[x].grFlag)
        
        for x in range(0,3):
            button_labels = ["AND", " OR", "ALL"]
            button = FilterButton(outliner_header=self,position=x,label=button_labels[x])
            self.buttons.append(button)
            self.scene.grScene.addItem(self.buttons[x].grButton)
        self.buttons[2].grButton.setSelected(True)
            
    
    def setPos(self,x,y):
        self.grHeaderItem.setPos(x,y)
        
    def getFlagPosition(self, position):
        x = 395 - (position*20+self.grHeaderItem.padding)
        y = self.grHeaderItem.padding + 17
        return [x, y]

    def getButtonPosition(self, position):
        x = 250 - (position*38+self.grHeaderItem.padding)
        y = self.grHeaderItem.padding + 6
        return [x, y]
    
class OutlinerGraphicsHeader(QGraphicsItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.width = 800
        self.height = 50
        self.padding = 10
        
        self.brush = (QColor(active_theme.window_background_color))
        self.brush_title = QBrush(QColor(active_theme.node_title_background_color))
        
        self.initContent()
        self.initUI()
        self.show()
        
    def initContent(self):
        pass
    
    def initUI(self):
        pass
    
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        content = QPainterPath()
        content.setFillRule(Qt.WindingFill)
        content.addRect(0,0,self.width,self.height)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.brush)
        painter.drawPath(content.simplified())
        
    def boundingRect(self):
        return QRectF(0,0,self.width,
                      self.height).normalized()
