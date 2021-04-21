from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import src.UI_colorTheme as UI_colorTheme
from src.UI_updateJSON import updateJSON
import json, math
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
        self.error_color = QColor("#ff3333")
        self.color_selected = QColor(active_theme.node_selected_color)
        self.pen = QPen(self.color)
        
        self.pen_selected = QPen(self.color_selected)
        self.pen_dragging = QPen(self.color)
        self.pen_error = QPen(self.error_color)
        
        self.pen.setWidthF(WIDTH)
        self.pen_error.setWidth(WIDTH)
        self.pen_dragging.setWidth(WIDTH)
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

        if self.edge.end_socket == None:
            painter.setPen(self.pen_dragging)
        else:
            #numbers and booleans can convert, so they don't change the pen to error
            end_type = self.edge.end_socket.type
            start_type = self.edge.start_socket.type
            if end_type == 3 or end_type == 6:
                end_type = 3
            if start_type == 3 or start_type == 6:
                start_type = 3
            
            #any other mismatch changes pen to error
            if start_type != end_type:
                painter.setPen(self.pen_error)
            else:
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

        cpx_s = +dist
        cpx_d = -dist
        cpy_s = 0
        cpy_d = 0

        sspos = self.edge.start_socket.position

        if (s[0] > d[0] and sspos in (3,3)) or (s[0] < d[0] and sspos in (1,1)):
            cpx_d *= -1
            cpx_s *= -1

            cpy_d = (
                (s[1] - d[1]) / math.fabs(
                    (s[1] - d[1]) if (s[1] - d[1]) != 0 else 0.00001
                )
            ) * EDGE_CP_ROUNDNESS
            cpy_s = (
                (d[1] - s[1]) / math.fabs(
                    (d[1] - s[1]) if (d[1] - s[1]) != 0 else 0.00001
                )
            ) * EDGE_CP_ROUNDNESS

        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        path.cubicTo( s[0] + cpx_s, s[1] + cpy_s, d[0] + cpx_d, d[1] + cpy_d, self.posDestination[0], self.posDestination[1])

        self.setPath(path)
        
EDGE_TYPE_DIRECT = 1
EDGE_TYPE_BEZIER = 2
EDGE_CP_ROUNDNESS = 100

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
        self.scene.addEdge(self)
   
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
        else:
            self.grEdge.setDestination(*source_pos)
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
        
