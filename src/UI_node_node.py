from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import UI_colorTheme
from UI_updateJSON import updateJSON
data = updateJSON()


class QDMGraphicsNode(QGraphicsItem):
    def __init__(self, node, title="Node Graphics Item", parent=None):
        super().__init__(parent)
        self.initTitle()
        self.initUI()
        
        self.title = title

    def initUI(self):
        pass
    
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
    
class Node():
    def __init__(self, scene, title="undefined node"):
        self.scene = scene
        
        self.title = title
        
        self.grNode = QDMGraphicsNode(self, self.title)
        
        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)
        self.inputs = []
        self.outputs = []
        
        
