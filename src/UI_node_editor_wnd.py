from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from UI_node_graphics_scene import QDMGraphicsView, QDMGraphicsScene
from UI_node_node import Node
from UI_node_scene import Scene
from UI_node_socket import (Socket,S_TRIGGER, S_FILE, S_OBJECT, S_NUMBER, S_TEXT, S_EVENT, S_BOOLEAN)
from UI_node_edge import Edge, EDGE_TYPE_BEZIER, EDGE_TYPE_DIRECT
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
        
        self.addNodes()
                
        self.view = QDMGraphicsView(self.grScene, self)
        self.layout.addWidget(self.view)
        
        self.show()
        
    def addNodes(self):
        node1 = Node(self.scene, "Node Graphical Item", inputs = [S_TRIGGER], outputs = [S_TRIGGER])
        node2 = Node(self.scene, "Node Graphical Item", inputs = [S_TRIGGER,S_TEXT,S_FILE],
                     outputs = [S_TRIGGER,S_EVENT,S_FILE])
        node3 = Node(self.scene, "All Sockets",
                     inputs = [S_TRIGGER, S_FILE, S_OBJECT, S_NUMBER, S_TEXT, S_EVENT, S_BOOLEAN],
                     outputs = [S_TRIGGER, S_FILE, S_OBJECT, S_NUMBER, S_TEXT, S_EVENT, S_BOOLEAN])
        node1.setPos(-350*2,-250*2)
        node2.setPos(-75*2, 0)
        node3.setPos(200*2, -150*2)
        
        edge1 = Edge(self.scene,node1.outputs[0], node2.inputs[0])
        edge2 = Edge(self.scene,node2.outputs[1], node3.inputs[5])
        
    def loadStyleSheet(self, filename):
        file = QFile(filename)
        file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = file.readAll()
        QApplication.instance().setStyleSheet(str(stylesheet, encoding="utf-8"))

            
        