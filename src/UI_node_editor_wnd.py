from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from src.UI_node_graphics_scene import QDMGraphicsView, QDMGraphicsScene
from src.UI_node_node import Node
from src.UI_node_scene import Scene
from src.UI_node_socket import (Socket,S_TRIGGER, S_FILE, S_OBJECT, S_NUMBER, S_TEXT, S_EVENT, S_BOOLEAN)
from src.UI_node_edge import Edge, EDGE_TYPE_BEZIER, EDGE_TYPE_DIRECT
from src.node_presets import number_number_math, create_variable

from src.UI_node_outliner import outlinerWnd, OutlinerScene

import src.UI_colorTheme as UI_colorTheme
from src.UI_updateJSON import updateJSON
data = updateJSON()
active_theme = getattr(UI_colorTheme, data["active_theme"])

class NodeEditorWnd(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.stylesheet_filename = "src/nodestyle.qss"
        self.loadStyleSheet(self.stylesheet_filename)
        self.initUI()
    
    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        
        self.scene = Scene()
        self.scene.added_nodes = []
        self.grScene = self.scene.grScene
        
        self.addNodes()
                
        self.view = QDMGraphicsView(self.grScene, self)
        self.layout.addWidget(self.view, 75)
        
        self.lower_half = QWidget()

        self.lower_half_preview = QTextEdit()
        self.lower_half_outliner = outlinerWnd(scene=OutlinerScene(),parent_scene=self.scene)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.lower_half)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy( Qt.ScrollBarAlwaysOff )
        self.scroll_area.setVerticalScrollBarPolicy( Qt.ScrollBarAlwaysOff )
        
        self.layout.addWidget(self.scroll_area, 25)
        
        self.lower_half_layout = QHBoxLayout()
        self.lower_half_layout.setContentsMargins(0,0,0,0)
        self.lower_half_layout.setSpacing(0)
        self.lower_half.setLayout(self.lower_half_layout)
        
        self.lower_half_layout.addWidget(self.lower_half_preview, 65)
        self.lower_half_layout.addWidget(self.lower_half_outliner, 35)
        
        self.lower_half_outliner.setMaximumWidth(400)
        self.lower_half_outliner.setMinimumWidth(400)

        
        self.show()
        
    def addNodes(self):
        node1 = number_number_math(scene=self.scene).n
        node2 = number_number_math(scene=self.scene).n
        node3 = create_variable(scene=self.scene).n
        node4 = create_variable(scene=self.scene).n
        self.scene.added_nodes.append(node1)
        self.scene.added_nodes.append(node2)
        self.scene.added_nodes.append(node3)
        self.scene.added_nodes.append(node4)
        node1.setPos(-350*2,-250*2)
        node2.setPos(-75*2, 0)
        node3.setPos(200*2, -150*2)

        
    def loadStyleSheet(self, filename):
        file = QFile(filename)
        file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = file.readAll()
        QApplication.instance().setStyleSheet(str(stylesheet, encoding="utf-8"))

            
        
