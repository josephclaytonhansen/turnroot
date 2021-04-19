from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import src.UI_colorTheme as UI_colorTheme
from src.UI_updateJSON import updateJSON
import pickle

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
    def __init__(self, parent = None, t=0):
        super().__init__(parent)
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

class Socket():
    def __init__(self, node, index=0, position=LEFT_TOP, t=0):
        
        self.node = node
        self.index = index
        self.position = position
        self.type = t
        self.grSocket = QDMGraphicsSocket(self.node.grNode, self.type)
        
        self.grSocket.setPos(*self.node.getSocketPosition(index,position))
        
        self.edge = None
    def getSocketPosition(self):
        res = self.node.getSocketPosition(self.index,self.position)
        return res
    
    def setConnectedEdge(self,edge=None):
        self.edge = edge
    
    def hasEdge(self):
        return self.edge is not None
