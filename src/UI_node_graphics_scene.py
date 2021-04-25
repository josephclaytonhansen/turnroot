from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import src.UI_colorTheme as UI_colorTheme
from src.UI_updateJSON import updateJSON

from src.UI_node_socket import QDMGraphicsSocket
from src.UI_node_edge import QDMGraphicsEdge, Edge, EDGE_TYPE_BEZIER
from src.UI_node_graphics_cutline import QDMCutLine

from src.UI_Dialogs import confirmAction

import math, json, pickle, sys

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
MODE_EDGE_CUT = 3

EDGE_DRAG_THRESHOLD = 20

data = updateJSON()

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

socket_names = ["S_TRIGGER", "S_FILE", "S_OBJECT", "S_NUMBER", "S_TEXT", "S_EVENT", "S_BOOLEAN"]

class QDMGraphicsView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(parent)
        self.grScene = scene
        self.initUI()
        self.setScene(self.grScene)
        
        self.mode = MODE_NOOP
        self.editingFlag = False
        
        self.zoomInFactor = ZOOM_IN
        self.zoomClamp = False
        self.zoom = ZOOM
        self.scale(self.zoom, self.zoom)
        self.zoomStep = ZOOM_STEP
        self.zoomRange = ZOOM_RANGE
        
        self.cutline = QDMCutLine()
        self.grScene.addItem(self.cutline)
    
    def initUI(self):
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform )
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.RubberBandDrag)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            self.middleMouseButtonPress(event)
        elif event.button() == Qt.LeftButton:
            self.setDragMode(QGraphicsView.RubberBandDrag)
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
        
        if hasattr(item, "node") or isinstance(item, QDMGraphicsEdge) or item is None:
            if event.modifiers() == Qt.ShiftModifier:
                event.ignore()
                fakeEvent = QMouseEvent(QEvent.MouseButtonPress, event.localPos(), event.screenPos(),
                                        Qt.LeftButton, event.buttons() | Qt.LeftButton,
                                        event.modifiers() | Qt.ControlModifier)
                super().mousePressEvent(fakeEvent)
                return
        
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
        
        if self.dragMode() == QGraphicsView.RubberBandDrag:
            self.grScene.scene.history.storeHistory("Selection changed")

        
        if item is None:
            if event.modifiers() == Qt.ControlModifier:
                self.mode = MODE_EDGE_CUT
                fakeEvent = QMouseEvent(QEvent.MouseButtonRelease,
                                        event.localPos(),
                                        event.screenPos(),
                                        Qt.LeftButton,
                                        Qt.NoButton,
                                        event.modifiers())
                super().mouseReleaseEvent(fakeEvent)
                QApplication.setOverrideCursor(Qt.CrossCursor)
                return
            
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
            self.grScene.scene.history.storeHistory("Created new edge by dragging")
            print(socket_names[self.dragEdge.start_socket.type],
                  socket_names[self.dragEdge.end_socket.type])
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
            try:
                last_direction = self.last_start_socket.direction
                active_direction = item.direction
            except:
                pass
        
            if last_direction == active_direction:
                self.dragEdge.remove()
                self.dragEdge = None
                if self.previousEdge is not None:
                    self.previousEdge.start_socket.edge = self.previousEdge
                self.mode = MODE_NOOP
                
        if hasattr(item, "node") or isinstance(item, QDMGraphicsEdge) or item is None:
            if event.modifiers() == Qt.ShiftModifier:
                event.ignore()
                fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                        Qt.LeftButton, Qt.NoButton,
                                        event.modifiers() | Qt.ControlModifier)
                super().mouseReleaseEvent(fakeEvent)
                return
            
        if self.mode == MODE_EDGE_DRAG:
            
            new_lmb_release_scene_pos = self.mapToScene(event.pos())
            dist_scene = new_lmb_release_scene_pos -self.last_lmb_click_scene_pos
            
            EDGE_DRAG_THRESHOLD = 20
             
            if dist_scene.x()*dist_scene.x()+dist_scene.y()*dist_scene.y() > EDGE_DRAG_THRESHOLD * EDGE_DRAG_THRESHOLD:
                res = self.edgeDragEnd(item)
                if res: return
                
        if self.mode == MODE_EDGE_CUT:
            self.cutIntersectingEdges()
            self.cutline.line_points = []
            self.cutline.update()
            QApplication.setOverrideCursor(Qt.ArrowCursor)
            self.mode = MODE_NOOP
            return
            
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
        
        if self.mode == MODE_EDGE_CUT:
            pos = self.mapToScene(event.pos())
            self.cutline.line_points.append(pos)
            self.cutline.update()
            
        super().mouseMoveEvent(event)
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete or event.key() == Qt.Key_X:
            if event.modifiers() == Qt.ShiftModifier and not self.editingFlag:
                self.grScene.scene.clear()
            else:
                if not self.editingFlag:
                    self.deleteSelected()
                else:
                    super().keyPressEvent(event)
                    
        elif event.key() == Qt.Key_S:
            if event.modifiers() == Qt.ControlModifier:
                self.grScene.scene.saveToFile()
                
            elif event.modifiers() == Qt.ControlModifier | Qt.ShiftModifier:
                self.grScene.scene.path = None
                self.grScene.scene.saveToFile()
            else:
                if not self.editingFlag:
                    pass
                    #open preferences
                else:
                    super().keyPressEvent(event)
                    
        elif event.key() == Qt.Key_O:
            if event.modifiers() == Qt.ControlModifier:
                self.grScene.scene.loadFromFile()
            else:
                if not self.editingFlag:
                    pass
                else:
                    super().keyPressEvent(event)
                    
        elif event.key() == Qt.Key_N:
            if event.modifiers() == Qt.ControlModifier:
                self.grScene.scene.path = None
                self.grScene.scene.clear()
            else:
                super().keyPressEvent(event)
                
        elif event.key() == Qt.Key_Q:
            if event.modifiers() == Qt.ControlModifier:
                self.quitWindow()
            else:
                if not self.editingFlag:
                    pass
                    #open forums
                else:
                    super().keyPressEvent(event)
        
        elif event.key() == Qt.Key_Escape:
            if not self.editingFlag:
                pass
                #back
            else:
                super().keyPressEvent(event)
        
        elif event.key() == Qt.Key_H:
            if not self.editingFlag:
                pass
                #help
            else:
                super().keyPressEvent(event)
                
        elif event.key() == Qt.Key_Z and event.modifiers() == Qt.ControlModifier and self.editingFlag == False:
            self.grScene.scene.history.undo()
            
        elif event.key() == Qt.Key_Y and event.modifiers() == Qt.ControlModifier and self.editingFlag == False:
            self.grScene.scene.history.redo()
            
        else:
            super().keyPressEvent(event)
    
    def quitWindow(self):
        c = confirmAction(parent=self, s="quit the level editor")
        c.exec_()
        if(c.return_confirm):
            sys.exit()
            
    def cutIntersectingEdges(self):
        for ix in range(len(self.cutline.line_points) - 1):
            p1 = self.cutline.line_points[ix]
            p2 = self.cutline.line_points[ix + 1]

            for edge in self.grScene.scene.edges:
                if edge.grEdge.intersectsWith(p1, p2):
                    edge.remove()
        self.grScene.scene.history.storeHistory("Delete cutted edges")
            
    def deleteSelected(self):
        for item in self.grScene.selectedItems():
            if isinstance(item, QDMGraphicsEdge):
                item.edge.remove()
            elif hasattr(item, 'node'):
                item.node.remove()
        self.grScene.scene.history.storeHistory("Delete selected")
        

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
        
