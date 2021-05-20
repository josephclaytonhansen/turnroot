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
    def __init__(self, node, contents, parent = None):
        super().__init__(parent)
        self.node = node
        self.contents = contents
        self.initUI()
        
    def initUI(self):
        self.active_theme = getattr(UI_colorTheme, data["active_theme"])
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,4,0,0)
        self.setLayout(self.layout)
        
        if self.node.height == None:
            self.spacer_height = 600
        else:
            self.spacer_height = self.node.height
        self.layout.setSpacing(10)
        for widget in self.contents:
            self.layout.addWidget(widget)
            widget.setStyleSheet("background-color: "+active_theme.node_background_color+"; color:"+active_theme.node_text_color+"; font-size: "+str(data["font_size"]))
            
            self.font = widget.font()
            self.font.setPointSize(16)
            widget.setFont(self.font)
            
            widget.setMinimumHeight(30)
            widget.setMaximumHeight(30)
            self.spacer_height -= 38
        self.spacer_height -= NODE_TITLE_HEIGHT
        self.spacer_height -= NODE_PADDING
        
        
        self.eval_order = QSpinBox()
        self.eval_order.setButtonSymbols(2)
        self.eval_order.valueChanged.connect(self.change_eval_order)
        self.eval_order.setPrefix("Order: ")
        self.eval_order.setMinimumHeight(42)
        self.eval_order.setStyleSheet("background-color: "+active_theme.node_background_color+"; color:"+active_theme.node_text_color)

        font = self.eval_order.font()
        font.setPointSize(data["font_size"])
        self.eval_order.setFont(font)

        #self.spacer_height -= 42
        #self.layout.addWidget(self.eval_order)
        
        self.layout.addSpacerItem(QSpacerItem(2, self.spacer_height))
    
    def change_eval_order(self, i):
        pass
    
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
        print(self.content.height())
        self.width = NODE_WIDTH
        if self.node.height == None:
            self.height = NODE_HEIGHT
        else:
            self.height = self.node.height
        self.title_height = NODE_TITLE_HEIGHT
        self.padding = NODE_PADDING
        self.edge_size = EDGE_SIZE
        
        self.initTitle()
        self.initUI()
        self.wasMoved = False
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
        self.wasMoved = True
    
    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)

        if self.wasMoved:
            self.wasMoved = False
            self.node.scene.history.storeHistory("Node moved")
    
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
    def __init__(self, scene, title="node item", inputs = [], outputs=[], contents = [], socket_content_index = 0, height = None):
        super().__init__()
        self.scene = scene
        self.socket_content_index = socket_content_index
        self.height = height
        self.node_preset = None
        
        self.load_index = 0
        
        self.contents = contents
        self.content = QDMNodeContentWidget(self, self.contents)
        self.grNode = QDMGraphicsNode(self)
        
        self.storage = []
        self.sw = []
        
        self._title = title
        self.title = title
        
        if self.title == "Combat Start":
            self.content.eval_order.setValue(1)
            self.content.eval_order.setEnabled(False)
        
        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)
        self.inputs = []
        self.outputs = []
        counter = 0
        for item in inputs:
            socket = Socket(node=self, index=counter, position=LEFT_BOTTOM, t=item, multi_edges=False)
            counter += 1
            self.inputs.append(socket)

        counter = 0
        for item in outputs:
            socket = Socket(node=self, index=counter, position=RIGHT_TOP, t=item, multi_edges=True)
            counter += 1
            self.outputs.append(socket)

    @property
    def pos(self):
        return self.grNode.pos()
    
    def setPos(self,x,y):
        self.grNode.setPos(x,y)
    
    @property
    def title(self):
        try:
            return self._title
        except:
            pass
    
    @title.setter
    def title(self, value):
        self._title = value
        self.grNode.title = self._title
    
    def getSocketPosition(self, index, position):
        if position in (LEFT_TOP, LEFT_BOTTOM):
            x = 0
        else:
            x = self.grNode.width
        
        y = self.grNode.title_height + self.grNode.padding + (1.5*self.grNode.edge_size) + (index * 20 * 2.0)
        y = self.socket_content_index * 40 + y
        return [x, y]
    
    def updateConnectedEdges(self):
        for socket in self.inputs + self.outputs:
            # if socket.hasEdge():
            for edge in socket.edges:
                edge.updatePositions()


    def remove(self):
        for socket in (self.inputs+self.outputs):
            # if socket.hasEdge():
            for edge in socket.edges:
                edge.remove()
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

    def deserialize(self, data, hashmap={}, restore_id=True):
        
        if restore_id: self.id = data['id']
        hashmap[data['id']] = self

        self.setPos(data['pos_x'], data['pos_y'])
        self.title = data['title']

        data['inputs'].sort(key=lambda socket: socket['index'] + socket['position'] * 10000 )
        data['outputs'].sort(key=lambda socket: socket['index'] + socket['position'] * 10000 )

        self.inputs = []
        for socket_data in data['inputs']:
            new_socket = Socket(node=self, index=socket_data['index'], position=socket_data['position'],
                                t=socket_data['socket_type'])
            new_socket.deserialize(socket_data, hashmap, restore_id)
            self.inputs.append(new_socket)

        self.outputs = []
        for socket_data in data['outputs']:
            new_socket = Socket(node=self, index=socket_data['index'], position=socket_data['position'],
                                t=socket_data['socket_type'])
            new_socket.deserialize(socket_data, hashmap, restore_id)
            self.outputs.append(new_socket)


        return True

    