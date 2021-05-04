from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import src.UI_colorTheme as UI_colorTheme
from src.UI_updateJSON import updateJSON
import pickle

from collections import OrderedDict
from src.UI_node_serializable import Serializable

data = updateJSON()
active_theme = getattr(UI_colorTheme, data["active_theme"])

with open("src/tmp/nsp.trnes", "rb") as readfile:
    socket_data = pickle.load(readfile)
    
S_TRIGGER = socket_data[0][0]
S_FILE = socket_data[0][1]
S_OBJECT = socket_data[0][2]
S_NUMBER = socket_data[0][3]
S_TEXT = socket_data[0][4]
S_EVENT = socket_data[0][5]
S_BOOLEAN = socket_data[0][6]
socket_types = [S_TRIGGER, S_FILE, S_OBJECT, S_NUMBER, S_TEXT, S_EVENT, S_BOOLEAN]

socket_types_colors = [active_theme.node_socket_trigger_color,
               active_theme.node_socket_file_color, active_theme.node_socket_object_color,
               active_theme.node_socket_number_color, active_theme.node_socket_text_color,
               active_theme.node_socket_event_color, active_theme.node_socket_boolean_color]

RADIUS = socket_data[2]
OUTLINE_WIDTH = socket_data[3]
storage = (socket_types, socket_types_colors, RADIUS, OUTLINE_WIDTH)

class QDMGraphicsSocket(QGraphicsItem):
    def __init__(self, socket, t=0):
        super().__init__(socket.node.grNode)
        
        self.socket = socket
        self.direction = None
        self.radius = RADIUS
        self.color_background = QColor(socket_types_colors[t])
        self.color_outline = QColor("#000000")
        self.outline_width = OUTLINE_WIDTH
        
        self.pen = QPen(self.color_outline)
        self.pen.setWidth(self.outline_width)
        self.brush = QBrush(self.color_background)
    
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        painter.setBrush(self.brush)
        painter.setPen(self.pen)
        painter.drawEllipse(-self.radius, -self.radius, 2 * self.radius, 2* self.radius)
    
    def boundingRect(self):
        return QRectF(-self.radius - self.outline_width,
                      -self.radius - self.outline_width,
                      2 * (self.radius+self.outline_width),
                      2* (self.radius * self.outline_width))

LEFT_TOP = 1
LEFT_BOTTOM = 2
RIGHT_TOP = 3
RIGHT_BOTTOM = 4

INPUT = 1
OUTPUT = 3

class Socket(Serializable):
    def __init__(self, node, index=0, position=LEFT_TOP, t=0,multi_edges=True):
        super().__init__()
        self.node = node
        self.index = index
        self.position = position
        self.is_multi_edges = multi_edges

        if self.position == LEFT_TOP:
            self.direction = INPUT
            self.reception = None
        else:
            self.direction = OUTPUT
            self.emission = None
            
        self.type = t
        self.grSocket = QDMGraphicsSocket(self, self.type)
        self.grSocket.direction = self.direction
        self.socket_type = self.type
        self.grSocket.setPos(*self.node.getSocketPosition(index,position))
        
        self.edges = []
        
    def getSocketPosition(self):
        res = self.node.getSocketPosition(self.index,self.position)
        return res
    
    def addEdge(self, edge):
        self.edges.append(edge)
        for n in range(len(self.edges)):
            
            self.edges[n].start_socket.emission = self.edges[n].start_socket.node.node_preset.values[2]

    def removeEdge(self, edge):
        if edge in self.edges: self.edges.remove(edge)
        else: print("!W:", "Socket::removeEdge", "wanna remove edge", edge, "from self.edges but it's not in the list!")

    def removeAllEdges(self):
        while self.edges:
            edge = self.edges.pop(0)
            edge.remove()

    def serialize(self):
        return OrderedDict([
            ('id', self.id),
            ('index', self.index),
            ('multi_edges', self.is_multi_edges),
            ('position', self.position),
            ('socket_type', self.socket_type),
        ])

    def deserialize(self, data, hashmap={}, restore_id=True):
        if restore_id: self.id = data['id']
        self.is_multi_edges = data['multi_edges']
        hashmap[data['id']] = self
        return True


