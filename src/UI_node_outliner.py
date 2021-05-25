from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from src.UI_node_outliner_graphics_scene import OutlinerGraphicsScene
from src.UI_node_outliner_graphics_view import OutlinerGraphicsView
from src.UI_node_outliner_list_item import OutlinerListItem
from src.UI_node_outliner_header import OutlinerHeader, RefreshItem
from src.node_backend import getFiles, GET_FOLDERS, GET_FILES, condenseList
import math, json, os

if os.sep != "\\":
    const_path = "src/tmp/nenc.json"
    filter_icon_path = "src/ui_icons/white/filter.png"
    refresh_icon_path = "src/ui_icons/white/refresh_files.png"
    stylesheet_path = "src/node_outliner_style.qss"
    with open(const_path, "r") as readfile:
        const = json.load(readfile)
    NODE_FONT = "Lucida Grande"
else:
    const_path = "src\\tmp\\nenc.json"
    filter_icon_path = "src\\ui_icons\\white\\filter.png"
    refresh_icon_path = "src\\ui_icons\\white\\refresh_files.png"
    stylesheet_path = "src\\node_outliner_style.qss"
    with open(const_path, "r") as readfile:
        const = json.load(readfile)
    NODE_FONT = "Lucida Sans Unicode"

FONT_SIZE = int(const[6]) / 2

AND = 0
OR = 1
ALL = 2

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
        self.addHeader()
        
        self.Filter()
        
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
        self.filter_rect = QRect(275,8,38,38)
        
        self.header.refresh_icon = QPixmap(refresh_icon_path)
        self.header_refresh = RefreshItem(self.header.refresh_icon)
        self.scene.grScene.addItem(self.header_refresh)
        self.header_refresh.setPos(110,7)
        self.refresh_rect = QRect(110,7,38,38)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.leftMouseButtonPress(event)

    def leftMouseButtonPress(self, event):
        if self.grScene.filter_view_update and self.filter_rect.contains(event.pos()):
            print(self.grScene.filter_mode)
            self.Filter(flags=self.header.flags_status,AO=self.grScene.filter_mode)
            print("FILTERING: ", self.header.flags_status)
        
        elif self.grScene.refresh_files and self.refresh_rect.contains(event.pos()):
            self.addItems()
            self.update()
            self.grScene.refresh_files = False
        super().mousePressEvent(event)

    def addItems(self):
        tmp_height = FONT_SIZE * 2.5
        height = 50
        self.items = {}
        self.scene.placement = {}
        self.scene.slots = []
        #placement stores the top of each list_item- slots holds this by index. So placement[slots[0]] will give the first, etc
        x = 0
        file_list = getFiles(self.path)[GET_FILES]
        
        for f in file_list:
            if f.ext.strip() == ".trnep":
                self.items[x] = OutlinerListItem(self.scene, path=f.name, index = x, depth=f.depth,
                                                 parent_scene = self.parent_scene, full_path = f.fullPath)
                self.items[x].setPos(0,height)
                self.scene.placement[height] = self.items[x]
                self.scene.slots.append(height)
                height += tmp_height
                x += 1
    
    def Filter(self, flags={0: False, 1: False, 2: False, 3: False}, AO=ALL):
        print("CURRENT FILTER: ", AO)
        #if ao = AND; get and matches. if ao = OR; get or matches
        match_flags = flags
        
        item_amount = len(self.items)
        true_count = 0
        
        if AO == AND:
            true_count_threshold = 4
        elif AO == OR:
            true_count_threshold = 0
        elif AO == ALL:
            true_count_threshold = 4
        
        for g in range(item_amount): #check each OutlinerListItem
            true_count = 0
            current_item = self.items[g]
            if current_item == None:
                continue
            item_flags = current_item.flags_status
            
            if AO != OR:
                for flag in item_flags: #check each flag
                    if item_flags[flag] == match_flags[flag]:
                        true_count += 1
                        
            elif AO == OR:
                for flag in item_flags:
                    if flag:
                      if item_flags[flag] == match_flags[flag]:
                        true_count += 1
                        
            if AO != OR: 
                if true_count == true_count_threshold:
                    pass
                else:
                    if AO != ALL:
                        try:
                            self.scene.placement[self.scene.slots[g]].remove()
                        except:
                            pass
            
            elif AO == OR:
                if true_count > true_count_threshold:
                    pass
                else:
                    try:
                        self.scene.placement[self.scene.slots[g]].remove()
                    except:
                        pass
                
        
            #collapse list for filter results
            condenseList(self.scene.placement, self.scene.slots)

    
    def loadStyleSheet(self, filename):
        file = QFile(filename)
        file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = file.readAll()
        self.setStyleSheet(str(stylesheet, encoding="utf-8"))