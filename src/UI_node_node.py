from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class QDMGraphicsNode(QGraphicsItem):
    def __init__(self, node, title="Node Graphics Item", parent=None):
        super().__init__(parent)
        self.initTitle()
        self.initUI()
        
        self.title = title

    def initUI(self):
        pass
    
    def initTitle(self):
        self._title_color = Qt.white
        self._title_font = QFont("Lucida Sans Unicode",25)
        self._title_font.setHintingPreference(3)
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
        
        