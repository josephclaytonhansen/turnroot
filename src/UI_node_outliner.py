from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from src.UI_node_outliner_graphics_scene import OutlinerGraphicsScene
from src.UI_node_outliner_graphics_view import OutlinerGraphicsView
from src.UI_node_outliner_list_item import OutlinerListItem
from src.UI_node_outliner_header import OutlinerHeader
from src.node_backend import getFiles, GET_FOLDERS, GET_FILES
import math, json, os

if os.sep != "\\":
    const_path = "src/tmp/nenc.json"
    filter_icon_path = "src/ui_icons/white/filter.png"
    stylesheet_path = "src/node_outliner_style.qss"
    with open(const_path, "r") as readfile:
        const = json.load(readfile)
    NODE_FONT = const[5]
else:
    const_path = "src\\tmp\\nenc.json"
    filter_icon_path = "src\\ui_icons\\white\\filter.png"
    stylesheet_path = "src\\node_outliner_style.qss"
    with open(const_path, "r") as readfile:
        const = json.load(readfile)
    NODE_FONT = "Lucida Grande"

FONT_SIZE = int(const[6]) / 2

class OutlinerScene():
    def __init__(self):
        super().__init__()
        self.scene_width = 400
        self.scene_height = 1660
        self.list_items = []
        self.header = None
        self.initUI()
        
    def initUI(self):
        self.grScene = OutlinerGraphicsScene(self)
        self.grScene.setGrScene(self.scene_width, self.scene_height)

    def addListItem(self, list_item):
        self.list_items.append(list_item)
    
    def addHeader(self,header):
        self.header = header
        
    def removeListItem(self, list_item):
        self.list_items.remove(list_item)
        
class outlinerWnd(QWidget):
    def __init__(self, scene, parent_scene, parent=None):
        super().__init__(parent)
        self.stylesheet_filename = stylesheet_path
        self.loadStyleSheet(self.stylesheet_filename)
        self.scene = scene
        self.parent_scene = parent_scene
        self.scene_path = parent_scene.path
        self.path = "."
        self.initUI()
        self.addItems()
        self.scene.placement[self.scene.slots[0]].remove()
        print(self.scene.placement,self.scene.slots)
        self.addHeader()
        
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
    
    def addHeader(self):
        self.header = OutlinerHeader(self.scene,parent_scene = self.parent_scene)
        self.header.setPos(0,0)
        self.header.filter_icon = QPixmap(filter_icon_path)
        self.header_filter = QGraphicsPixmapItem(self.header.filter_icon)
        self.scene.grScene.addItem(self.header_filter)
        self.header_filter.setPos(275,8)
    
    def addItems(self):
        tmp_height = FONT_SIZE * 2.5
        height = 50
        items = {}
        self.scene.placement = {}
        self.scene.slots = []
        #placement stores the top of each list_item- slots holds this by index. So placement[slots[0]] will give the first, etc
        x = 0
        file_list = getFiles(self.path)[GET_FILES]
        
        for f in file_list:
            if f.ext.strip() == ".trnep":
                items[x] = OutlinerListItem(self.scene, path=f.name, index = x, depth=f.depth, parent_scene = self.parent_scene)
                items[x].setPos(0,height)
                self.scene.placement[height] = items[x]
                self.scene.slots.append(height)
                height += tmp_height
                x += 1

    
    def loadStyleSheet(self, filename):
        file = QFile(filename)
        file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = file.readAll()
        self.setStyleSheet(str(stylesheet, encoding="utf-8"))