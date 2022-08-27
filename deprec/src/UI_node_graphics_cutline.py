from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import src.UI_colorTheme as UI_colorTheme
from src.UI_updateJSON import updateJSON
import json, math
data = updateJSON()

active_theme = getattr(UI_colorTheme, data["active_theme"])

with open("src/tmp/neec.json", "r") as readfile:
    const = json.load(readfile)
    
WIDTH = const[0]
SELECTED_WIDTH = const[1]

class QDMCutLine(QGraphicsItem):
    def __init__(self,parent=None):
        super().__init__(parent)
        
        self.line_points = []
        self.pen = QPen(Qt.white)
        self.pen.setWidth(WIDTH)
        self.pen.setDashPattern([3,3])
        
        self.setZValue(2)
    
    def boundingRect(self):
        return QRectF(0,0,1,1)
    
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.NoBrush)
        painter.setPen(self.pen)
        
        poly = QPolygonF(self.line_points)
        painter.drawPolyline(poly)