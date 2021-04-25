import sys, json, os
import src.UI_colorTheme as UI_colorTheme
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize
from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QPalette, QIcon, QPixmap
from src.UI_updateJSON import updateJSON
from src.UI_Dialogs import confirmAction
from src.UI_node_editor_wnd import NodeEditorWnd
from src.UI_ProxyStyle import ProxyStyle
import qtmodern.styles
import qtmodern.windows

data = updateJSON()
active_theme = getattr(UI_colorTheme, data["active_theme"])

app = QApplication([])

myStyle = ProxyStyle('Fusion')    
app.setStyle(myStyle)

screen = app.primaryScreen()
size = screen.size()

RESIZE_F = .6

title = "Turnroot Game Dialogue Editor" 
class mainN(NodeEditorWnd):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(title)
        self.setMinimumSize(QSize(int(size.width()/3), int(size.height()/3)))
        self.setMaximumSize(QSize(int(size.width()), int(size.height())))
        self.resize(QSize(int(size.width()*RESIZE_F), int(size.height()*RESIZE_F)))

class main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.toolbar = QToolBar("")
        self.toolbar.setStyleSheet("background-color: "+active_theme.window_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
        self.toolbar.setIconSize(QSize(int(data["icon_size"]), int(data["icon_size"])))
        self.toolbar.setToolButtonStyle(Qt.ToolButtonIconOnly)
        
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
        
window = main()
window.show()
a = app.exec_()
