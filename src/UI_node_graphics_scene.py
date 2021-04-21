from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import src.UI_colorTheme as UI_colorTheme
from src.UI_updateJSON import updateJSON

from src.UI_node_socket import QDMGraphicsSocket
from src.UI_node_edge import QDMGraphicsEdge, Edge, EDGE_TYPE_BEZIER

import math, json

with open("src/tmp/nesc.json", "r") as readfile:
    const = json.load(readfile)
    
ZOOM_IN = const[0]
ZOOM = const[1]
ZOOM_STEP = const[2]
ZOOM_RANGE = const[3]
GRID_SIZE = const[4]
GRID_ALT = const[5]

MODE_NOOP = 1
MODE_EDGE_DRAG = 2

EDGE_DRAG_THRESHOLD = 20

data = updateJSON()
class QDMGraphicsView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(parent)
        self.grScene = scene
        self.initUI()
        self.setScene(self.grScene)
        
        self.mode = MODE_NOOP
        
        self.zoomInFactor = ZOOM_IN
        self.zoomClamp = False
        self.zoom = ZOOM
        self.scale(self.zoom, self.zoom)
        self.zoomStep = ZOOM_STEP
        self.zoomRange = ZOOM_RANGE
    
    def initUI(self):
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform )
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonPress(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonPress(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonPress(event)
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonRelease(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonRelease(event)
    
    def middleMouseButtonPress(self, event):
        releaseEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(), Qt.LeftButton, Qt.NoButton, event.modifiers())
        super().mouseReleaseEvent(releaseEvent)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(), Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
        super().mousePressEvent(fakeEvent)
        
    def middleMouseButtonRelease(self, event):
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons() and -Qt.LeftButton,
                                event.modifiers())
        super().mouseReleaseEvent(fakeEvent)
        self.setDragMode(QGraphicsView.NoDrag)
    
    def leftMouseButtonPress(self, event):
        
        item = self.getItemAtClick(event)
        self.last_lmb_click_scene_pos = self.mapToScene(event.pos())
        
        if type(item) is QDMGraphicsSocket:
            if self.mode == MODE_NOOP:
                self.mode = MODE_EDGE_DRAG
                self.previousEdge = item.socket.edge
                self.last_start_socket = item.socket
                self.dragEdge = Edge(self.grScene.scene,item.socket, None)
                
                return
        
        if self.mode == MODE_EDGE_DRAG:
            res = self.edgeDragEnd(item)
            if res: return
            
        super().mousePressEvent(event)
    
    def edgeDragEnd(self, item):
        """ return True if skip the rest of the code """
        self.mode = MODE_NOOP

        if type(item) is QDMGraphicsSocket:
            if item.socket.hasEdge():
                try:
                    item.socket.edge.remove()
                except:
                    pass
            try:
                if self.previousEdge is not None: self.previousEdge.remove()
            except:
                pass
            self.dragEdge.start_socket = self.last_start_socket
            self.dragEdge.end_socket = item.socket
            self.dragEdge.start_socket.setConnectedEdge(self.dragEdge)
            self.dragEdge.end_socket.setConnectedEdge(self.dragEdge)
            self.dragEdge.updatePositions()
            return True

        self.dragEdge.remove()
        self.dragEdge = None
        if self.previousEdge is not None:
            self.previousEdge.start_socket.edge = self.previousEdge

        return False
    
    INPUT = 1
    OUTPUT = 3
    
    def leftMouseButtonRelease(self, event):
        item = self.getItemAtClick(event)
        
        if type(item) is QDMGraphicsSocket:
            last_direction = self.last_start_socket.direction
            active_direction = item.direction
        
            if last_direction == active_direction:
                self.dragEdge.remove()
                self.dragEdge = None
                if self.previousEdge is not None:
                    self.previousEdge.start_socket.edge = self.previousEdge
                self.mode = MODE_NOOP
            
        if self.mode == MODE_EDGE_DRAG:
            
            new_lmb_release_scene_pos = self.mapToScene(event.pos())
            dist_scene = new_lmb_release_scene_pos -self.last_lmb_click_scene_pos
            
            EDGE_DRAG_THRESHOLD = 20
             
            if dist_scene.x()*dist_scene.x()+dist_scene.y()*dist_scene.y() > EDGE_DRAG_THRESHOLD * EDGE_DRAG_THRESHOLD:
                res = self.edgeDragEnd(item)
                if res: return
            
        super().mouseReleaseEvent(event)
    
    def rightMouseButtonPress(self, event):
        super().mousePressEvent(event)
    
    def rightMouseButtonRelease(self, event):
        super().mouseReleaseEvent(event)
    
    def mouseMoveEvent(self,event):
        
        if self.mode == MODE_EDGE_DRAG:
            self.dragEdge.updatePositions()
            pos = self.mapToScene(event.pos())
            self.dragEdge.grEdge.setDestination(pos.x(), pos.y())
            self.dragEdge.grEdge.update()
            
        super().mouseMoveEvent(event)

    def getItemAtClick(self,event):
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj
    
    def wheelEvent(self, event):
        zoomOutFactor = 1 / self.zoomInFactor
        if event.angleDelta().y() > 0:
            zoomFactor = self.zoomInFactor
            self.zoom += self.zoomStep
        else:
            zoomFactor = zoomOutFactor
            self.zoom -= self.zoomStep
        clamped = False
        
        if self.zoom > self.zoomRange[1]: self.zoom, clamped = self.zoomRange[0], True
        
        if not clamped:
            self.scale(zoomFactor, zoomFactor)

class QDMGraphicsScene(QGraphicsScene):
    def __init__(self,scene,parent=None):
        super().__init__(parent)
        
        self.scene = scene
        
        self.active_theme = getattr(UI_colorTheme, data["active_theme"])
        self.gridSize = GRID_SIZE
        
        self.scene_width = 64000
        self.scene_height = 64000
    
        self._color_background = QColor(self.active_theme.node_grid_background_color)
        self._color_light = QColor(self.active_theme.node_grid_lines_color)
        self._color_dark = QColor(self.active_theme.node_grid_alt_lines_color)
        
        self._pen_light = QPen(self._color_light)
        self._pen_dark = QPen(self._color_dark)
        self._pen_light.setWidth(1)
        self._pen_dark.setWidth(2)

        self.setSceneRect(-self.scene_width//2, -self.scene_height//2, self.scene_width, self.scene_height)
        
        self.setBackgroundBrush(self._color_background)
        
    
    def setGrScene(self, width, height):
        self.setSceneRect(-width//2, -height //2, width, height)
    
    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)
        
        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))
        
        first_left = left - (left % self.gridSize)
        first_top = top - (top % self.gridSize)
        
        lines_light, lines_dark = [], []
        for x in range(first_left, right, self.gridSize):
            if x % int(GRID_ALT*self.gridSize) == 0:
                lines_dark.append(QLine(x,top,x,bottom))
            else:
                lines_light.append(QLine(x,top,x,bottom))
        
        for y in range(first_top, bottom, self.gridSize):
            if y % int(GRID_ALT*self.gridSize) == 0:
                lines_dark.append(QLine(left,y,right,y))
            else:
                lines_light.append(QLine(left,y,right,y))
            
        painter.setPen(self._pen_light)
        painter.drawLines(*lines_light)
        
        painter.setPen(self._pen_dark)
        painter.drawLines(*lines_dark)
        
