from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from UI_node_graphics_scene import QDMGraphicsView, QDMGraphicsScene
from UI_node_node import Node
from UI_node_scene import Scene
class NodeEditorWnd(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.stylesheet_filename = "nodestyle.qss"
        self.loadStyleSheet(self.stylesheet_filename)
        self.initUI()
    
    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)
        
        self.scene = Scene()
        self.grScene = self.scene.grScene
        
        node = Node(self.scene, "Node Graphical Item")
        
        self.view = QDMGraphicsView(self.grScene, self)
        self.layout.addWidget(self.view)
        
        self.show()
    
    def loadStyleSheet(self, filename):
        file = QFile(filename)
        file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = file.readAll()
        QApplication.instance().setStyleSheet(str(stylesheet, encoding="utf-8"))

            
        