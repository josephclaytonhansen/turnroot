from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from src.UI_node_outliner_graphics_scene import OutlinerGraphicsScene
from src.UI_node_outliner_graphics_view import OutlinerGraphicsView

class OutlinerScene():
    def __init__(self):
        super().__init__()
        self.scene_width = 750
        self.scene_height = 1250
        self.initUI()
        
    def initUI(self):
        self.grScene = OutlinerGraphicsScene(self)
        self.grScene.setGrScene(self.scene_width, self.scene_height)

class outlinerWnd(QWidget):
    def __init__(self, scene, parent=None):
        super().__init__(parent)
        self.stylesheet_filename = "src/node_outliner_style.qss"
        self.loadStyleSheet(self.stylesheet_filename)
        self.scene = scene
        self.initUI()
        
    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        
        self.setLayout(self.layout)
        self.grScene = self.scene.grScene
                
        self.view = OutlinerGraphicsView(self.grScene, self)
        self.layout.addWidget(self.view)
        self.show()
    
    def loadStyleSheet(self, filename):
        file = QFile(filename)
        file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = file.readAll()
        self.setStyleSheet(str(stylesheet, encoding="utf-8"))