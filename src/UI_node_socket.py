from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import UI_colorTheme
from UI_updateJSON import updateJSON
data = updateJSON()
active_theme = getattr(UI_colorTheme, data["active_theme"])

class QDMGraphicsSocket(QGraphicsItem):
    def __init__(self, parent = None, t=0):
        super().__init__(parent)
        print("socket")
        self.radius = 6.0 * 2.5
        self.socket_types= [active_theme.node_socket_trigger_color,
                 active_theme.node_socket_file_color, active_theme.node_socket_object_color,
                 active_theme.node_socket_number_color, active_theme.node_socket_text_color]
        self.color_background = QColor(self.socket_types[t])
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
        self.positions = position
        self.type = t
        self.grSocket = QDMGraphicsSocket(self.node.grNode, self.type)