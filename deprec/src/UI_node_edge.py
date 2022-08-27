from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import src.UI_colorTheme as UI_colorTheme
from src.UI_updateJSON import updateJSON

from collections import OrderedDict
from src.UI_node_serializable import Serializable

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
        self.error_color = QColor(active_theme.node_wire_error_color)
        self.color_selected = QColor(active_theme.node_selected_color)
        self.pen = QPen(self.color)
        
        self.pen_selected = QPen(self.color_selected)
        self.pen_dragging = QPen(self.color)
        self.pen_error = QPen(self.error_color)
        self.pen_error.setStyle(Qt.DotLine)
        self.pen_selected_error = QPen(self.color_selected)
        self.pen_selected_error.setStyle(Qt.DotLine)
        
        
        self.pen.setWidthF(WIDTH)
        self.pen_error.setWidth(WIDTH)
        self.pen_dragging.setWidth(WIDTH)
        self.pen_selected.setWidthF(SELECTED_WIDTH)
        self.pen_selected_error.setWidthF(SELECTED_WIDTH)
        
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setZValue(-1)
        self.posSource = [0,0]
        self.posDestination = [0,0]
        
    def setSource(self, x, y):
        self.posSource = [x,y]
        
    def setDestination(self, x, y,):
        self.posDestination = [x,y]
    
    def paint(self, painter, QStyleOptionsGraphicsItem, widget=None):
        self.setPath(self.updatePath())

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
                painter.setPen(self.pen_error if not self.isSelected() else self.pen_selected_error)
            else:
                painter.setPen(self.pen if not self.isSelected() else self.pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(self.path())
    
    def intersectsWith(self, p1, p2):
        cutpath = QPainterPath(p1)
        cutpath.lineTo(p2)
        path = self.updatePath()
        return cutpath.intersects(path)

    
    def updatePath(self):
        raise NotImplemented("This method has to be overriden in a child class")

class QDMGraphicsEdgeDirect(QDMGraphicsEdge):
    def updatePath(self):
        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        path.lineTo(self.posDestination[0], self.posDestination[1])
        return path
        
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

        return path
        
EDGE_TYPE_DIRECT = 1
EDGE_TYPE_BEZIER = 2
EDGE_CP_ROUNDNESS = 100

with open("src/tmp/node_preferences.json", "r") as r:
    node_data = json.load(r)
    default_edge = node_data["edge_type"]
    print(default_edge)

class Edge(Serializable):
    def __init__(self, scene, start_socket=None, end_socket=None, edge_type=default_edge):
        super().__init__()
        self.scene = scene
        
        self._start_socket = None
        self._end_socket = None
        
        self.start_socket = start_socket
        self.end_socket = end_socket
        self.edge_type = edge_type

        self.scene.addEdge(self)


    @property
    def start_socket(self): return self._start_socket

    @start_socket.setter
    def start_socket(self, value):
        # if we were assigned to some socket before, delete us from the socket
        if self._start_socket is not None:
            self._start_socket.removeEdge(self)

        # assign new start socket
        self._start_socket = value
        # addEdge to the Socket class
        if self.start_socket is not None:
            self.start_socket.addEdge(self)



    @property
    def end_socket(self): return self._end_socket

    @end_socket.setter
    def end_socket(self, value):
        # if we were assigned to some socket before, delete us from the socket
        if self._end_socket is not None:
            self._end_socket.removeEdge(self)

        # assign new end socket
        self._end_socket= value
        # addEdge to the Socket class
        if self.end_socket is not None:
            self.end_socket.addEdge(self)

    @property
    def edge_type(self): return self._edge_type

    @edge_type.setter
    def edge_type(self, value):
        if hasattr(self, 'grEdge') and self.grEdge is not None:
            self.scene.grScene.removeItem(self.grEdge)

        self._edge_type = value
        if self.edge_type == EDGE_TYPE_DIRECT:
            self.grEdge = QDMGraphicsEdgeDirect(self)
        elif self.edge_type == EDGE_TYPE_BEZIER:
            self.grEdge = QDMGraphicsEdgeBezier(self)
        else:
            self.grEdge = QDMGraphicsEdgeBezier(self)

        self.scene.grScene.addItem(self.grEdge)

        if self.start_socket is not None:
            self.updatePositions()


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
        self.end_socket = None
        self.start_socket = None


    def remove(self):
        self.remove_from_sockets()
        self.scene.grScene.removeItem(self.grEdge)
        self.grEdge = None
        try:
            self.scene.removeEdge(self)
        except ValueError:
            pass



