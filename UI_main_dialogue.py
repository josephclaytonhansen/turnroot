import sys, json, os
import src.UI_colorTheme as UI_colorTheme
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize
from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QPalette, QIcon, QPixmap
from src.UI_updateJSON import updateJSON
from src.UI_Dialogs import confirmAction, infoClose
from src.UI_node_editor_wnd import NodeEditorWnd
from src.UI_ProxyStyle import ProxyStyle
from src.UI_node_preferences_dialog import NodePreferencesDialog
import qtmodern.styles
import qtmodern.windows

data = updateJSON()
active_theme = getattr(UI_colorTheme, data["active_theme"])

app = QApplication([])

myStyle = ProxyStyle('Fusion')    
app.setStyle(myStyle)

screen = app.primaryScreen()
size = screen.size()

title = "Turnroot Game Dialogue Editor"

with open("src/tmp/aic.json", "r") as cons:
    const = json.load(cons)
    
OPEN_LAST_FILE = const[0]
OPEN_NEW_FILE = const[1]

class mainN(NodeEditorWnd):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(title)
        self.setMinimumSize(QSize(int(size.width()/3), int(size.height()/3)))
        self.setMaximumSize(QSize(int(size.width()), int(size.height())))

class main(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.toolbar = QToolBar("")
        self.toolbar.setStyleSheet("background-color: "+active_theme.window_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
        self.toolbar.setIconSize(QSize(int(data["icon_size"]), int(data["icon_size"])))
        self.toolbar.setToolButtonStyle(Qt.ToolButtonIconOnly)
        
        self.optionsButton = QAction(QIcon("src/ui_icons/white/settings-17-32.png"),"Options (S)", self)
        self.helpButton = QAction(QIcon("src/ui_icons/white/question-mark-4-32.png"),"Read docs (H)", self)
        self.backButton = QAction(QIcon("src/ui_icons/white/grid-three-up-32.png"),"Return to editor selection (Esc)", self)
        self.forumButton = QAction(QIcon("src/ui_icons/white/speech-bubble-2-32.png"),"Access forum (Q)", self)
        
        self.toolbar.addAction(self.backButton)
        self.toolbar.addAction(self.optionsButton)
        self.toolbar.addAction(self.helpButton)
        self.toolbar.addAction(self.forumButton)
        
        self.optionsButton.triggered.connect(self.OptionsMenu)
        
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
        
        self.saveButton = QAction("&Save\tCrtl+S", self)
        self.saveButton.triggered.connect(self.m.scene.saveToFile)
        fileMenu.addAction(self.saveButton)
        
        self.saveAsButton = QAction("Save As\tCrtl+Shift+S", self)
        self.saveAsButton.triggered.connect(self.saveAs)
        fileMenu.addAction(self.saveAsButton)
        
        self.openButton = QAction("&Open\tCrtl+O", self)
        self.openButton.triggered.connect(self.m.scene.loadFromFile)
        fileMenu.addAction(self.openButton)
        
        self.newButton = QAction("&New\tCrtl+N", self)
        self.newButton.triggered.connect(self.New)
        fileMenu.addAction(self.newButton)
        
        self.quitButton = QAction("&Quit\tCrtl+Q", self)
        self.quitButton.triggered.connect(self.quitWindow)
        fileMenu.addAction(self.quitButton)
        
        self.clearButton = QAction("Clear\tShift+X", self)
        self.clearButton.triggered.connect(self.m.scene.clear)
        editMenu.addAction(self.clearButton)
        
        with open("src/tmp/wer.taic", "r") as tmp_reason:
            if tmp_reason.read() == OPEN_LAST_FILE:
                with open("src/tmp/lsf.taic", "r") as open_file:
                    try:
                        self.m.scene.path = open_file.read()
                        self.m.scene.loadFromFile()
                    except:
                        c = infoClose("Last saved file not found\n(opening new file)")
                        c.exec_()
    
    def New(self):
        self.m.scene.clear()
        self.m.scene.path = None
        
    def saveAs(self):
        self.m.scene.path = None
        self.m.scene.saveToFile()
    
    def quitWindow(self):
        c = confirmAction(parent=self, s="quit the level editor")
        c.exec_()
        if(c.return_confirm):
            sys.exit()
    
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
        
window = main()
window.show()
a = app.exec_()
