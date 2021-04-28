from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from src.UI_node_outliner_label import OutlinerGraphicFlag, OutlinerGraphicFlag_Filter, filterButtonText
from src.UI_node_outliner_list_item import OutlinerGraphicsListItem

AND = 0
OR = 1
ALL = 2

class OutlinerGraphicsView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(parent)
        self.grScene = scene
        self.initUI()
        self.setScene(self.grScene)
        self.show()
        
    def initUI(self):
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform )
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QGraphicsView.AnchorViewCenter)
        self.setAlignment( Qt.AlignTop )
        self.setSceneRect (0,0,400, 1660)
        self.centerOn(0,0)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.leftMouseButtonPress(event)
    
    def leftMouseButtonPress(self, event):
        item = self.getItemAtClick(event)
        print(item)
        self.last_lmb_click_scene_pos = self.mapToScene(event.pos())
        
        if isinstance(item, OutlinerGraphicFlag):
            self.grScene.filter_view_update = True
            if item.flag.on:
                item.flag.on = False
                item.flag.list_item.flags_status[item.flag.position] = item.flag.on
            else:
                item.flag.on = True
                item.flag.list_item.flags_status[item.flag.position] = item.flag.on
            item.update()
            print("label at position", item.flag.position, "at index",item.flag.index, "with color", item.color.color.name(), "clicked on",item.flag.list_item.grListItem.text)
            print("Labels ", item.flag.list_item.flags_status)
            
        if hasattr(item, "list_item") and isinstance(item, OutlinerGraphicFlag) == False:
            self.grScene.filter_view_update = False
            print("clicked list item ", item.list_item.grListItem.text)
            item.list_item.parent_scene.path = item.list_item.full_path
            item.list_item.parent_scene.loadFromFile(dialog=False)
        
        if isinstance(item, OutlinerGraphicFlag_Filter):
            if item.flag.on:
                item.flag.on = False
                item.flag.outliner_header.flags_status[item.flag.position] = item.flag.on
            else:
                item.flag.on = True
                item.flag.outliner_header.flags_status[item.flag.position] = item.flag.on
            item.update()
            self.grScene.filter_view_update = True
        
        if isinstance(item, filterButtonText):
            self.grScene.filter_view_update = True
            print("FILTER BUTTON CLICKED")
            if item.position == 0:
                self.grScene.filter_mode = AND
            elif item.position == 1:
                self.grScene.filter_mode = OR
            elif item.position == 2:
                self.grScene.filter_mode = ALL
            print("GLOBAL FILTER MODE: ", self.grScene.filter_mode)
            
        super().mousePressEvent(event)
            
    def getItemAtClick(self,event):
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj
