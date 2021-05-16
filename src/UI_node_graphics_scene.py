from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import src.UI_colorTheme as UI_colorTheme
from src.UI_updateJSON import updateJSON

from src.UI_node_socket import QDMGraphicsSocket
from src.UI_node_edge import QDMGraphicsEdge, Edge, EDGE_TYPE_BEZIER
from src.UI_node_graphics_cutline import QDMCutLine

from src.UI_Dialogs import confirmAction
from src.UI_node_preferences_dialog import NodePreferencesDialog

from src.UI_node_dialogs import addNodePreset

import math, json, pickle, sys

with open("src/tmp/nesc.json", "r") as readfile:
    const = json.load(readfile)

with open("src/tmp/aic.json", "r") as cons:
    q_const = json.load(cons)
    
OPEN_LAST_FILE = q_const[0]
OPEN_NEW_FILE = q_const[1]
    
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
    scenePosChanged = pyqtSignal(int, int)
    def __init__(self, scene, parent=None):
        super().__init__(parent)
        self.grScene = scene
        self.initUI()
        self.setScene(self.grScene)
        
        self.mode = MODE_NOOP
        self.editingFlag = False
        self.rubberBandDraggingRectangle = False
        
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
        self.grScene.scene.update_hex()
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
                self.edgeDragStart(item)
                
                return
        
        if self.mode == MODE_EDGE_DRAG:
            res = self.edgeDragEnd(item)
            if res: return
        
        if self.rubberBandDraggingRectangle:
            self.grScene.scene.history.storeHistory("Selection changed")
            self.rubberBandDraggingRectangle = False

        
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
            else:
                self.rubberBandDraggingRectangle = True

            
        super().mousePressEvent(event)
        
    def edgeDragStart(self, item):
        self.drag_start_socket = item.socket
        self.drag_edge = Edge(self.grScene.scene, item.socket, None, EDGE_TYPE_BEZIER)

    def edgeDragEnd(self, item):
        """ return True if skip the rest of the code """
        self.mode = MODE_NOOP

        self.drag_edge.remove()
        self.drag_edge = None

        if type(item) is QDMGraphicsSocket:
            if item.socket != self.drag_start_socket:
                # if we released dragging on a socket (other then the beginning socket)

                # we wanna keep all the edges comming from target socket
                if not item.socket.is_multi_edges:
                    item.socket.removeAllEdges()

                # we wanna keep all the edges comming from start socket
                if not self.drag_start_socket.is_multi_edges:
                    self.drag_start_socket.removeAllEdges()

                new_edge = Edge(self.grScene.scene, self.drag_start_socket, item.socket, edge_type=EDGE_TYPE_BEZIER)
                #new_edge.end_socket.reception = new_edge.start_socket.emission
                #print("reception ", new_edge.end_socket.reception)

                self.grScene.scene.history.storeHistory("Created new edge by dragging", setModified=True)
                return True


        return False

    
    INPUT = 1
    OUTPUT = 3
    
    def leftMouseButtonRelease(self, event):
        # get item which we release mouse button on
        item = self.getItemAtClick(event)

        # logic
        if hasattr(item, "node") or isinstance(item, QDMGraphicsEdge) or item is None:
            if event.modifiers() & Qt.ShiftModifier:
                event.ignore()
                fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                        Qt.LeftButton, Qt.NoButton,
                                        event.modifiers() | Qt.ControlModifier)
                super().mouseReleaseEvent(fakeEvent)
                return

        if self.mode == MODE_EDGE_DRAG:
            if self.distanceBetweenClickAndReleaseIsOff(event):
                res = self.edgeDragEnd(item)
                if res: return

        if self.mode == MODE_EDGE_CUT:
            self.cutIntersectingEdges()
            self.cutline.line_points = []
            self.cutline.update()
            QApplication.setOverrideCursor(Qt.ArrowCursor)
            self.mode = MODE_NOOP
            return


        if self.rubberBandDraggingRectangle:
            self.grScene.scene.history.storeHistory("Selection changed")
            self.rubberBandDraggingRectangle = False

        super().mouseReleaseEvent(event)

    
    def rightMouseButtonPress(self, event):
        super().mousePressEvent(event)
    
    def rightMouseButtonRelease(self, event):
        super().mouseReleaseEvent(event)
    
    def mouseMoveEvent(self, event):
        for x in self.grScene.scene.added_nodes:
            x.node_preset.updateEmission()
            x.node_preset.updateReception()
            
        if self.mode == MODE_EDGE_DRAG:
            pos = self.mapToScene(event.pos())
            self.drag_edge.grEdge.setDestination(pos.x(), pos.y())
            self.drag_edge.grEdge.update()

        if self.mode == MODE_EDGE_CUT:
            pos = self.mapToScene(event.pos())
            self.cutline.line_points.append(pos)
            self.cutline.update()

        self.last_scene_mouse_position = self.mapToScene(event.pos())

        self.scenePosChanged.emit(
            int(self.last_scene_mouse_position.x()), int(self.last_scene_mouse_position.y())
        )

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
                super().keyPressEvent(event)
                    
        elif event.key() == Qt.Key_O:
            if event.modifiers() == Qt.ControlModifier:
                self.grScene.scene.loadFromFile()
            else:
                super().keyPressEvent(event)
                    
        elif event.key() == Qt.Key_N:
            if event.modifiers() == Qt.ControlModifier:
                self.grScene.scene.path = None
                self.grScene.scene.clear()
            else:
                super().keyPressEvent(event)
                n = addNodePreset(parent=self)
                n.exec_()
                
        elif event.key() == Qt.Key_Q:
            if event.modifiers() == Qt.ControlModifier:
                self.quitWindow()
            else:
                super().keyPressEvent(event)
        
        elif event.key() == Qt.Key_Escape:
            if not self.editingFlag:
                pass
                #back
            else:
                super().keyPressEvent(event)
                
        elif event.key() == Qt.Key_Z and event.modifiers() == Qt.ControlModifier and self.editingFlag == False:
            self.grScene.scene.history.undo()
            
        elif event.key() == Qt.Key_Y and event.modifiers() == Qt.ControlModifier and self.editingFlag == False:
            self.grScene.scene.history.redo()
            
        elif event.key() == Qt.Key_C and event.modifiers() == Qt.ControlModifier and self.editingFlag == False:
            self.onEditCopy()
        
        elif event.key() == Qt.Key_V and event.modifiers() == Qt.ControlModifier and self.editingFlag == False:
            self.onEditPaste()
            
        else:
            super().keyPressEvent(event)
            
    def onEditCopy(self):
        clip_data = self.grScene.scene.clipboard.serializeSelected(delete=False)
        str_data = json.dumps(clip_data, indent=4)
        QApplication.instance().clipboard().setText(str_data)

    def onEditPaste(self):
        raw_data = QApplication.instance().clipboard().text()

        try:
            clip_data = json.loads(raw_data)
        except ValueError as e:
            print("Pasting of not valid json data!", e)
            return

        # check if the json data are correct
        if 'nodes' not in clip_data:
            print("JSON does not contain any nodes!")
            return

        self.grScene.scene.clipboard.deserializeFromClipboard(clip_data)
        
    def OptionsMenu(self):
        p = NodePreferencesDialog(parent=self)
        theme = p.exec_()
        data = updateJSON()
        
        #apply data from preferences
        if (theme != 0):
            active_theme = getattr(UI_colorTheme, data["active_theme"])
            if (data["theme_changed"] == True):
                self.m.scene.saveToFile()
                    
                with open("src/tmp/wer.taic", "w") as tmp_reason:
                    tmp_reason.write(OPEN_LAST_FILE)
                with open("src/tmp/lsf.taic", "w") as next_open_file:
                    try:
                        next_open_file.write(self.m.scene.path)
                    except:
                        c = infoClose("Invalid path")
                        c.exec_()
                    
                os.execl(sys.executable, sys.executable, *sys.argv)
                
    def quitWindow(self):
        c = confirmAction(parent=self, s="quit the level editor")
        c.exec_()
        with open("src/tmp/wer.taic", "w") as quit_reason:
            quit_reason.write(OPEN_NEW_FILE)
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
    
    def distanceBetweenClickAndReleaseIsOff(self, event):
        """ measures if we are too far from the last LMB click scene position """
        new_lmb_release_scene_pos = self.mapToScene(event.pos())
        dist_scene = new_lmb_release_scene_pos - self.last_lmb_click_scene_pos
        edge_drag_threshold_sq = EDGE_DRAG_THRESHOLD*EDGE_DRAG_THRESHOLD
        return (dist_scene.x()*dist_scene.x() + dist_scene.y()*dist_scene.y()) > edge_drag_threshold_sq

    
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
        self.NodeEditorWnd = None
        self.file_name = None
        
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
        
