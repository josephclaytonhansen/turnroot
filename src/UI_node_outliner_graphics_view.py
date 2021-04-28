from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from src.UI_node_outliner_label import OutlinerGraphicFlag
from src.UI_node_outliner_list_item import OutlinerGraphicsListItem
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
        self.last_lmb_click_scene_pos = self.mapToScene(event.pos())
        
        if isinstance(item, OutlinerGraphicFlag):
            if item.flag.on:
                item.flag.on = False
            else:
                item.flag.on = True
            item.update()
            
        if hasattr(item, "list_item") and isinstance(item, OutlinerGraphicFlag) == False:
            print("clicked list item ", item, item.list_item.grListItem.text)
            
        super().mousePressEvent(event)
            
    def getItemAtClick(self,event):
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj
