from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from UI_node_graphics_scene import QDMGraphicsView, QDMGraphicsScene
from UI_node_node import Node
from UI_node_scene import Scene
class NodeEditorWnd(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
    
    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)
        
        self.scene = Scene()
        self.grScene = self.scene.grScene
        
        node = Node(self.scene, "Node Graphical Item")
        
        self.view = QDMGraphicsView(self.grScene, self)
        self.view.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform )
        self.view.setOptimizationFlags(QGraphicsView.DontAdjustForAntialiasing)
        self.layout.addWidget(self.view)
        
        self.show()

            
        