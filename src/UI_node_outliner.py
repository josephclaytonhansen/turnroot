from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from src.UI_node_outliner_graphics_scene import OutlinerGraphicsScene
from src.UI_node_outliner_graphics_view import OutlinerGraphicsView
from src.UI_node_outliner_list_item import OutlinerListItem
from src.node_backend import getFiles, GET_FOLDERS, GET_FILES
import math

class OutlinerScene():
    def __init__(self):
        super().__init__()
        self.scene_width = 400
        self.scene_height = 1660
        self.list_items = []
        self.initUI()
        
    def initUI(self):
        self.grScene = OutlinerGraphicsScene(self)
        self.grScene.setGrScene(self.scene_width, self.scene_height)

    def addListItem(self, list_item):
        self.list_items.append(list_item)
        
class outlinerWnd(QWidget):
    def __init__(self, scene, parent=None):
        super().__init__(parent)
        self.stylesheet_filename = "src/node_outliner_style.qss"
        self.loadStyleSheet(self.stylesheet_filename)
        self.scene = scene
        self.initUI()
        self.addItems()
        
    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        
        self.setLayout(self.layout)
        self.grScene = self.scene.grScene
                
        self.view = OutlinerGraphicsView(self.grScene, self)
        self.view.centerOn(0,0)
        self.layout.addWidget(self.view)
        self.show()
    
    def addItems(self):
        items = [OutlinerListItem(self.scene)]
        tmp_height = items[0].grListItem.height
        height = 0
        items = {}
        x =0
        test_dir = "."
        file_list = getFiles(test_dir)[GET_FILES]
        
        for f in file_list:
            if f.name != "":
                if True:
                    items[x] = OutlinerListItem(self.scene, path=f.name, index = x)
                    items[x].setPos(0,height)
                    height += tmp_height
                    x += 1
                else:
                    items[x] = OutlinerListItem(self.scene, path="", index = x)
                    items[x].setPos(0,height)
                    height += tmp_height
                    x += 1
    
    def loadStyleSheet(self, filename):
        file = QFile(filename)
        file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = file.readAll()
        self.setStyleSheet(str(stylesheet, encoding="utf-8"))