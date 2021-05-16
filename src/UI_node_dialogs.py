from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QPalette, QIcon, QPixmap, QCursor, QFont
from src.UI_updateJSON import updateJSON
import src.UI_colorTheme
import shutil, os, pickle, json, sys
from src.node_presets import NODE_KEYS, NODES, Nodes

class addNodePreset(QDialog):
    def __init__(self, parent=None):
        self.chosen_node = None
        self.parent = parent
        self.add = False
        data = updateJSON()
        self.active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        super().__init__(parent)
        
        self.setWindowFlags(Qt.Popup)
        
        self.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(8,8,8,8)
        self.layout.addWidget(QLabel("Add node: "))
        
        self.add_options = NODE_KEYS
        self.add_dd = QComboBox()
        self.add_dd.setMaxVisibleItems(10)
        self.add_dd.textHighlighted.connect(self.add_enable)
        self.add_dd.currentTextChanged.connect(self.add_dd_changed)
        self.add_dd.setStyleSheet("QComboBox { combobox-popup: 0; };"+"background-color: "+self.active_theme.list_background_color+"; selection-background-color:"+self.active_theme.window_background_color)
        
        self.add_dd.addItem("--Select--")
        self.add_dd.addItems(self.add_options)
        self.layout.addWidget(self.add_dd)
        self.setLayout(self.layout)
        
        self.show()
    
    def add_enable(self,t):
        self.add = True
    
    def add_dd_changed(self, s):
        if self.add:
            self.chosen_node = NODES[s]
            g = Nodes(self.parent.grScene.NodeEditorWnd.scene, s).node
            self.parent.grScene.NodeEditorWnd.scene.added_nodes.append(g)
            i = self.parent.grScene.NodeEditorWnd.view.mapFromGlobal(self.position)
            h = self.parent.grScene.NodeEditorWnd.view.mapToScene(i.x(), i.y())
            g.setPos(h.x(), h.y())
            
        self.close()
        
    def showEvent(self, event):
        geom = self.frameGeometry()
        geom.moveCenter(QCursor.pos())
        self.setGeometry(geom)
        self.position = self.pos()
        self.move(self.position.x()+0,self.position.y()+48)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        super().showEvent(event)