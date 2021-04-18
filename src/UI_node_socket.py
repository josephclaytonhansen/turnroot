from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import UI_colorTheme
from UI_updateJSON import updateJSON
data = updateJSON()
active_theme = getattr(UI_colorTheme, data["active_theme"])

S_TRIGGER = 0
S_FILE = 1
S_OBJECT = 2
S_NUMBER = 3
S_TEXT = 4
S_EVENT = 5
S_BOOLEAN = 6
socket_types = [S_TRIGGER, S_FILE, S_OBJECT, S_NUMBER, S_TEXT, S_EVENT, S_BOOLEAN]

socket_types_colors = [active_theme.node_socket_trigger_color,
               active_theme.node_socket_file_color, active_theme.node_socket_object_color,
               active_theme.node_socket_number_color, active_theme.node_socket_text_color,
               active_theme.node_socket_event_color, active_theme.node_socket_boolean_color]

class QDMGraphicsSocket(QGraphicsItem):
    def __init__(self, parent = None, t=0):
        super().__init__(parent)
        print("socket")
        self.radius = 12.0
        self.color_background = QColor(socket_types_colors[t])
        self.color_outline = QColor("#000000")
        
        self.pen = QPen(self.color_outline)
        self.pen.setWidth(2.5)
        self.brush = QBrush(self.color_background)
    
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        painter.setBrush(self.brush)
        painter.setPen(self.pen)
        painter.drawEllipse(-self.radius, -self.radius, 2 * self.radius, 2* self.radius)

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