import sys, json, os
import src.UI_colorTheme as UI_colorTheme
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QPalette, QIcon, QPixmap, QCursor

from PyQt5.QtWebEngineWidgets import QWebEngineView
from src.UI_updateJSON import updateJSON
from src.UI_Dialogs import confirmAction, infoClose, switchEditorDialog, REPLACE_WINDOW, NEW_WINDOW
from src.UI_node_editor_wnd import NodeEditorWnd
from src.node_presets import NODES, Nodes
from src.UI_ProxyStyle import ProxyStyle
from src.UI_node_preferences_dialog import NodePreferencesDialog
import qtmodern.styles
import qtmodern.windows, json

data = updateJSON()
active_theme = getattr(UI_colorTheme, data["active_theme"])

app = QApplication([])

myStyle = ProxyStyle('Fusion')    
app.setStyle(myStyle)

screen = app.primaryScreen()
size = screen.size()

title = "Turnroot Node Editor" 

if os.sep == "\\":
    font_string = "Lucida Sans Unicode"
else:
    font_string = "Lucida Grande"

with open("src/nodestyle.qss", "r") as style_file:
    style_file_content = style_file.read()
    t_style_file_content = style_file_content
    
    t_style_file_content = t_style_file_content.replace("~", font_string)
    with open("src/nodestyle.qss", "w") as style_file_write:
        style_file_write.write(t_style_file_content)

with open("src/tmp/aic.json", "r") as cons:
    const = json.load(cons)
    
OPEN_LAST_FILE = const[0]
OPEN_NEW_FILE = const[1]

class mainN(NodeEditorWnd):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(QSize(int(size.width()/3), int(size.height()/3)))
        self.setMaximumSize(QSize(int(size.width()), int(size.height())))

class main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(title)

        self.toolbar = QToolBar("")
        self.toolbar.setStyleSheet("background-color: "+active_theme.window_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
        self.toolbar.setIconSize(QSize(int(data["icon_size"]), int(data["icon_size"])))
        self.toolbar.setToolButtonStyle(Qt.ToolButtonIconOnly)
        
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.context_menu)
        
        self.optionsButton = QAction(QIcon("src/ui_icons/white/settings-17-32.png"),"Options (S)", self)
        self.helpButton = QAction(QIcon("src/ui_icons/white/question-mark-4-32.png"),"Read docs (H)", self)
        self.backButton = QAction(QIcon("src/ui_icons/white/grid-three-up-32.png"),"Return to editor selection (Esc)", self)
        self.forumButton = QAction(QIcon("src/ui_icons/white/speech-bubble-2-32.png"),"Access forum (Q)", self)
        
        self.toolbar.addAction(self.backButton)
        self.toolbar.addAction(self.optionsButton)
        self.toolbar.addAction(self.helpButton)
        self.toolbar.addAction(self.forumButton)
        
        self.optionsButton.triggered.connect(self.OptionsMenu)
        self.backButton.triggered.connect(self.editorSelect)
        
        self.addToolBar(self.toolbar)
        
        #add Menu, File
        self.menubar = self.menuBar()
        font = self.menubar.font()
        font.setPointSize(data["font_size"])
        self.menubar.setNativeMenuBar(False)
        fileMenu = self.menubar.addMenu('&File')
        self.bar = self.menuBar()
        
        #add Edit and View to menu
        self.menubar.setStyleSheet("background-color: "+active_theme.window_background_color+"; color: "+active_theme.window_text_color+"; padding: 2px; font:bold;font-size: "+str(data["font_size"]))
        editMenu = self.bar.addMenu("&Edit")
        viewMenu = self.bar.addMenu( "&View")
        
        self.m = mainN()
        self.setCentralWidget(self.m)
        
        self.setGeometry(
    QStyle.alignedRect(
        Qt.LeftToRight,
        Qt.AlignCenter,
        self.m.size(),
        app.desktop().availableGeometry()
        ))
        
        self.saveButton = QAction("&Save\tCrtl+S", self)
        self.saveButton.triggered.connect(self.m.scene.saveToFile)
        fileMenu.addAction(self.saveButton)
        
        self.saveAsButton = QAction("Save As\tCrtl+Shift+S", self)
        self.saveAsButton.triggered.connect(self.saveAs)
        fileMenu.addAction(self.saveAsButton)
        
        self.openButton = QAction("&Open\tCrtl+O", self)
        self.openButton.triggered.connect(self.m.scene.loadFromFile)
        self.openButton.triggered.connect(self.nameChange)
        fileMenu.addAction(self.openButton)
        
        self.newButton = QAction("&New\tCrtl+N", self)
        self.newButton.triggered.connect(self.New)
        fileMenu.addAction(self.newButton)
        
        self.quitButton = QAction("&Quit\tCrtl+Q", self)
        self.quitButton.triggered.connect(self.quitWindow)
        fileMenu.addAction(self.quitButton)
        
        self.copyButton = QAction("Copy\tCrtl+C", self)
        self.copyButton.triggered.connect(self.onEditCopy)
        editMenu.addAction(self.copyButton)
        
        self.pasteButton = QAction("Paste\tCrtl+V", self)
        self.pasteButton.triggered.connect(self.onEditPaste)
        editMenu.addAction(self.pasteButton)
        
        self.deleteButton = QAction("Delete\tDel or X", self)
        self.deleteButton.triggered.connect(self.m.view.deleteSelected)
        editMenu.addAction(self.deleteButton)
        
        self.clearButton = QAction("Clear\tShift+X", self)
        self.clearButton.triggered.connect(self.m.scene.clear)
        editMenu.addAction(self.clearButton)
        
        self.undoButton = QAction("Undo\tCrtl+Z", self)
        self.undoButton.triggered.connect(self.m.scene.history.undo)
        editMenu.addAction(self.undoButton)
        
        self.redoButton = QAction("Redo\tCrtl+Y", self)
        self.redoButton.triggered.connect(self.m.scene.history.redo)
        editMenu.addAction(self.redoButton)
        
        with open("src/tmp/wer.taic", "r") as tmp_reason:
            if tmp_reason.read() == OPEN_LAST_FILE:
                with open("src/tmp/lsf.taic", "r") as open_file:
                    try:
                        self.m.scene.path = open_file.read()
                        #print(self.m.grScene.file_name)
                        self.m.scene.loadFromFile()
                    except:
                        c = infoClose("Last saved file not found\n(opening new file)")
                        c.exec_()

    def onEditCopy(self):
        clip_data = self.m.scene.clipboard.serializeSelected(delete=False)
        str_data = json.dumps(clip_data, indent=4)
        app.instance().clipboard().setText(str_data)

    def onEditPaste(self):
        raw_data = app.instance().clipboard().text()

        try:
            clip_data = json.loads(raw_data)
        except ValueError as e:
            print("Pasting of not valid json data!", e)
            return

        # check if the json data are correct
        if 'nodes' not in clip_data:
            print("JSON does not contain any nodes!")
            return

        self.m.scene.clipboard.deserializeFromClipboard(clip_data)

    def New(self):
        self.m.scene.clear()
        self.m.scene.path = None
    
    def nameChange(self):
        if self.m.scene.path is not None:
            self.setWindowTitle(title + " - "+self.m.scene.path)
        
    def saveAs(self):
        self.m.scene.path = None
        self.m.scene.saveToFile()
        if self.m.scene.path is not None:
            self.setWindowTitle(title + " - "+self.m.scene.path)
    
    def quitWindow(self):
        c = confirmAction(parent=self, s="quit the node editor")
        c.exec_()
        with open("src/tmp/wer.taic", "w") as quit_reason:
            quit_reason.write(OPEN_NEW_FILE)
        if(c.return_confirm):
            sys.exit()
    
    def editorSelect(self):
        e = switchEditorDialog(parent=self)
        e.exec_()
        new_editor = e.editor
        if e.mode == REPLACE_WINDOW:
            pass
        elif e.mode == NEW_WINDOW:
            if new_editor == 0:
                from main_level_editor import main
            elif new_editor == 1:
                pass
            elif new_editor == 2:
                from main_world_editor import main
            elif new_editor == 3:
                from main_hub_editor import main
            elif new_editor == 4:
                from main_unit_editor import main
            elif new_editor == 5:
                from main_object_editor import main
            elif new_editor == 6:
                from main_portrait_editor import main
            elif new_editor == 7:
                from main_menu_editor import main
            elif new_editor == 8:
                from main_stores_editor import main
            elif new_editor == 9:
                from main_game_editor import main

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
                        with open("src/tmp/wer.taic", "w") as tmp_reason:
                            tmp_reason.write(OPEN_NEW_FILE)
                    
                os.execl(sys.executable, sys.executable, *sys.argv)
                
    def context_menu(self, pos):
        context = QMenu(self)
        self.tmp_pos = QCursor.pos()
        items_keys = self.m.scene.node_keys
        items = self.m.scene.node_presets
        context.setStyleSheet("background-color: "+active_theme.node_background_color+"; color: "+active_theme.node_text_color+"; padding: 2px;font-size: "+str(data["font_size"]))
        flow = QMenu("Events/Flow")
        nop = QMenu("Numbers/Operations")
        ub = QMenu("Unit Bonus")
        ab = QMenu("Ally Bonus")
        fp = QMenu("Foe Penalties")
        se = QMenu("Special Effects")
        
        submenus = [flow,nop,ub,ab,fp,se]
        for y in submenus:
            y.setStyleSheet("background-color: "+active_theme.node_background_color+"; color: "+active_theme.node_text_color+"; padding: 2px;font-size: "+str(data["font_size"]))
        
        nop_actions = [QAction("Math", self),QAction("Compare Numbers", self),QAction("Convert T/F to Event", self), QAction("And", self),
                       QAction("A or B", self), QAction("Not (If A is False, True)",self)]
        for n in nop_actions:
            nop.addAction(n)
            n.triggered.connect(self.submenu_item)
            
        flow_actions = [QAction("Combat Start", self),QAction("Unit Initiates Combat", self),QAction("Foe Initiates Combat", self),
                        QAction("Unit is Adjacent to Ally", self), QAction("Unit is Within N of Ally", self),
                        QAction("Unit Using Weapon Type", self), QAction("Foe Using Weapon Type", self), QAction("Unit Health Percentage", self),
                        QAction("Foe Health Percentage", self)]
        
        for n in flow_actions:
            flow.addAction(n)
            n.triggered.connect(self.submenu_item)
            
        ub_actions = [QAction("Unit +Bonus Strength/Magic", self),QAction("Unit +Bonus Defense", self),QAction("Unit +Bonus Resistance", self),
                        QAction("Unit +Bonus Charisma", self), QAction("Unit +Bonus Dexterity", self),QAction("Unit +Bonus Luck", self)]
        
        for n in ub_actions:
            ub.addAction(n)
            n.triggered.connect(self.submenu_item)
        
        ab_actions = [QAction("Ally +Bonus Strength/Magic", self),QAction("Ally +Bonus Defense", self),QAction("Ally +Bonus Resistance", self),
                        QAction("Ally +Bonus Charisma", self), QAction("Ally +Bonus Dexterity", self),QAction("Ally +Bonus Luck", self)]
        
        for n in ab_actions:
            ab.addAction(n)
            n.triggered.connect(self.submenu_item)
    
        for y in submenus:
            y.setStyleSheet("background-color: "+active_theme.node_background_color+"; color: "+active_theme.node_text_color+"; padding: 2px;font-size: "+str(data["font_size"]))
            context.addMenu(y)
            
        context.exec_(self.mapToGlobal(pos))
    
    def submenu_item(self):
        s = self.sender().text()
        self.chosen_node = NODES[s]
        g = Nodes(self.m.scene, s).node
        self.m.scene.added_nodes.append(g)
        i = self.m.view.mapFromGlobal(self.tmp_pos)
        h = self.m.view.mapToScene(i.x(), i.y())
        g.setPos(h.x(), h.y())

window = main()
window.show()
a = app.exec_()
