from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import src.UI_colorTheme as UI_colorTheme
from src.UI_updateJSON import updateJSON
from src.UI_node_socket import *
from collections import OrderedDict
from src.UI_node_serializable import Serializable

import json
data = updateJSON()

with open("src/tmp/nenc.json", "r") as readfile:
    const = json.load(readfile)
    
NODE_WIDTH = const[0]
NODE_HEIGHT = const[1]
NODE_TITLE_HEIGHT = const[2]
NODE_PADDING = const[3]
EDGE_SIZE = const[4]
NODE_FONT = const[5]
FONT_SIZE = const[6]

class QDMNodeContentWidget(QWidget, Serializable):
    def __init__(self, node, parent = None):
        super().__init__(parent)
        self.node = node
        self.initUI()
        
    def initUI(self):
        active_theme = getattr(UI_colorTheme, data["active_theme"])
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)
        self.w_label = QLabel("<font color='"+active_theme.node_text_color+"'>Some text</font>")
        self.layout.addWidget(self.w_label)
        self.layout.addWidget(QDMTextEdit())
    
    def setEditingFlag(self,value):
        self.node.scene.grScene.views()[0].editingFlag = value
    
    def serialize(self):
        return OrderedDict([

        ])

    def deserialize(self, data, hashmap={}):
        return False


class QDMTextEdit(QTextEdit):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.font = QFont(NODE_FONT)
        self.font.setPointSize(FONT_SIZE)
        self.setFont(self.font)
    def keyPressEvent(self,event):
        super().keyPressEvent(event)
    
    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.parentWidget().setEditingFlag(True)
    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.parentWidget().setEditingFlag(False)


class QDMGraphicsNode(QGraphicsItem):
    def __init__(self, node, parent=None):
        super().__init__(parent)
        self.node = node
        self.content = self.node.content
        self.width = NODE_WIDTH
        self.height = NODE_HEIGHT
        self.title_height = NODE_TITLE_HEIGHT
        self.padding = NODE_PADDING
        self.edge_size = EDGE_SIZE
        
        self.initTitle()
        self.initUI()
        self.title = self.node.title
        
        self.initContent()
        self.initSockets()
        
        active_theme = getattr(UI_colorTheme, data["active_theme"])

        self.pen_default = QPen(QColor("#7f000000"))
        self.pen_selected = QPen(QColor(active_theme.node_selected_color))
        self.brush_title = QBrush(QColor(active_theme.node_title_background_color))
        self.brush_background = QBrush(QColor(active_theme.node_background_color))
        self.pen_selected.setWidth(3)
        
    def boundingRect(self):
        return QRectF(0,0,2*self.edge_size+self.width,
                      2*self.edge_size+self.height).normalized()

    def initUI(self):
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
    
    def initTitle(self):
        active_theme = getattr(UI_colorTheme, data["active_theme"])
        self._title_color = QColor(active_theme.node_title_color)
        self._title_font = QFont(NODE_FONT)
        self._title_font.setPointSize(FONT_SIZE)
        self._title_font.setStyleStrategy(QFont.NoAntialias)
        self.title_item = QGraphicsTextItem(self)
        self.title_item.node = self.node
        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setFont(self._title_font)
        self.title_item.setPos(self.padding, 10)
        self.title_item.setTextWidth(self.width-3*self.padding)
    
    def mouseMoveEvent(self,event):
        super().mouseMoveEvent(event)
        self.node.updateConnectedEdges()
        
        for node in self.scene().scene.nodes:
            if node.grNode.isSelected():
                node.updateConnectedEdges()
    
    @property
    def title(self): return self._title
    @title.setter
    def title(self, value):
        self._title = value
        self.title_item.setPlainText(self._title)
    
    def initContent(self):
        self.grContent = QGraphicsProxyWidget(self)
        self.content.setGeometry(self.edge_size+20, self.title_height+self.edge_size,
                                 self.width - 2*self.edge_size-40,
                                 self.height - 2*self.edge_size-self.title_height)
        self.grContent.setWidget(self.content)
    
    def initSockets(self):
        pass
    
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        
        path_title = QPainterPath()
        path_title.setFillRule(Qt.WindingFill)
        path_title.addRoundedRect(0,0,self.width,self.title_height, self.edge_size,self.edge_size)
        
        path_title.addRect(0,self.title_height-self.edge_size, self.edge_size, self.edge_size)
        path_title.addRect(self.width-self.edge_size,self.title_height-self.edge_size, self.edge_size, self.edge_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.brush_title)
        painter.drawPath(path_title.simplified())
        
        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        path_content.addRoundedRect(0,self.title_height, self.width,
                                    self.height-self.title_height,self.edge_size, self.edge_size)
        path_content.addRect(0,self.title_height,self.edge_size,self.edge_size)
        path_content.addRect(self.width-self.edge_size,self.title_height,self.edge_size,self.edge_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.brush_background)
        painter.drawPath(path_content.simplified())
        
        
        path_outline = QPainterPath()
        path_outline.addRoundedRect(0,0,self.width,self.height,self.edge_size, self.edge_size)
        painter.setPen(self.pen_default if not self.isSelected() else self.pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path_outline.simplified())
              
class Node(Serializable):
    def __init__(self, scene, title="undefined node", inputs = [], outputs=[]):
        super().__init__()
        self.scene = scene
        self.title = title
        
        self.content = QDMNodeContentWidget(self)
        self.grNode = QDMGraphicsNode(self)
        
        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)
        self.inputs = []
        self.outputs = []
        counter = 0
        for item in inputs:
            self.inputs.append(Socket(node=self,t=item,index=counter, position = LEFT_TOP))
            counter += 1
        counter = 0
        for item in outputs:
            self.outputs.append(Socket(node=self,t=item, index=counter, position = RIGHT_TOP))
            counter += 1
    @property
    def pos(self):
        return self.grNode.pos()
    
    def setPos(self,x,y):
        self.grNode.setPos(x,y)
    
    def getSocketPosition(self, index, position):
        if position in (LEFT_TOP, LEFT_BOTTOM):
            x = 0
        else:
            x = self.grNode.width
        
        y = self.grNode.title_height + self.grNode.padding + (1.5*self.grNode.edge_size) + (index * 20 * 2.0)
        return [x, y]
    
    def updateConnectedEdges(self):
        for socket in self.inputs + self.outputs:
            if socket.hasEdge():
                try:
                    socket.edge.updatePositions()
                except:
                    pass
    
    def remove(self):
        for socket in (self.inputs + self.outputs):
            if socket.hasEdge():
                socket.edge.remove()
        self.scene.grScene.removeItem(self.grNode)
        self.grNode = None
        self.scene.removeNode(self)
        
    def serialize(self):
        inputs, outputs = [], []
        for socket in self.inputs: inputs.append(socket.serialize())
        for socket in self.outputs: outputs.append(socket.serialize())
        return OrderedDict([
            ('id', self.id),
            ('title', self.title),
            ('pos_x', self.grNode.scenePos().x()),
            ('pos_y', self.grNode.scenePos().y()),
            ('inputs', inputs),
            ('outputs', outputs),
            ('content', self.content.serialize()),
        ])

    def deserialize(self, data, hashmap={}):
        return False


        
        
