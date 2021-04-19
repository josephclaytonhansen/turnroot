from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import src.UI_colorTheme as UI_colorTheme
from src.UI_updateJSON import updateJSON
import json
data = updateJSON()
active_theme = getattr(UI_colorTheme, data["active_theme"])

with open("src/tmp/neec.json", "r") as readfile:
    const = json.load(readfile)
    
WIDTH = const[0]
SELECTED_WIDTH = const[1]
    
class QDMGraphicsEdge(QGraphicsPathItem):
    def __init__(self, edge, parent= None):
        super().__init__(parent)
        
        self.edge = edge
        
        self.color = QColor(active_theme.node_wire_color)
        self.color_selected = QColor(active_theme.node_selected_color)
        self.pen = QPen(self.color)
        self.pen.setWidthF(WIDTH)
        self.pen_selected = QPen(self.color_selected)
        self.pen_selected.setWidthF(SELECTED_WIDTH)
        
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setZValue(-1)
        self.posSource = [0,0]
        self.posDestination = [0,0]
        
    def setSource(self, x, y):
        self.posSource = [x,y]
        
    def setDestination(self, x, y,):
        self.posDestination = [x,y]
    
    def paint(self, painter, QStyleOptionsGraphicsItem, widget=None):
        self.updatePath()
        
        painter.setPen(self.pen if not self.isSelected() else self.pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(self.path())
    
    def updatePath(self):
        raise NotImplemented("This method has to be overriden in a child class")

class QDMGraphicsEdgeDirect(QDMGraphicsEdge):
    def updatePath(self):
        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        path.lineTo(self.posDestination[0], self.posDestination[1])
        self.setPath(path)
class QDMGraphicsEdgeBezier(QDMGraphicsEdge):
    def updatePath(self):
        s = self.posSource
        d = self.posDestination
        dist = (d[0] - s[0]) * 0.5
        if s[0] > d[0]: dist *= -1
        
        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        path.cubicTo(s[0]+dist, s[1], d[0] - dist, d[1],
                     self.posDestination[0], self.posDestination[1])
        self.setPath(path)
        
EDGE_TYPE_DIRECT = 1
EDGE_TYPE_BEZIER = 2

class Edge():
    def __init__(self,scene,start_socket,end_socket, type = 2):
        self.scene = scene
        self.start_socket = start_socket
        self.end_socket = end_socket
        self.start_socket.edge = self
        if self.end_socket is not None:
            self.end_socket.edge = self
        self.grEdge = QDMGraphicsEdgeDirect(self) if type == EDGE_TYPE_DIRECT else QDMGraphicsEdgeBezier(self)
        self.updatePositions()
        self.scene.grScene.addItem(self.grEdge)
   
    def updatePositions(self):
        source_pos = self.start_socket.getSocketPosition()
        source_pos[0] += self.start_socket.node.grNode.pos().x()
        source_pos[1] += self.start_socket.node.grNode.pos().y()
        self.grEdge.setSource(*source_pos)
        if self.end_socket is not None:
            end_pos = self.end_socket.getSocketPosition()
            end_pos[0] += self.end_socket.node.grNode.pos().x()
            end_pos[1] += self.end_socket.node.grNode.pos().y()
            self.grEdge.setDestination(*end_pos)
        self.grEdge.update()
   
    def remove_from_sockets(self):
        if self.start_socket is not None:
            self.start_socket.edge = None
        if self.end_socket is not None:
            self.end_socket = None
        self.end_socket = None
        self.end_socket = None
    
    def remove(self):
        self.remove_from_sockets()
        self.scene.grScene.removeItem(self.grEdge)
        self.grEdge = None
        self.scene.removeEdge(self)
        
