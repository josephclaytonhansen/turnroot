import sys, json, os
import src.UI_colorTheme as UI_colorTheme
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QPalette, QIcon, QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView
from src.UI_updateJSON import updateJSON
from src.UI_Dialogs import confirmAction, infoClose, switchEditorDialog, REPLACE_WINDOW, NEW_WINDOW
from src.UI_ProxyStyle import ProxyStyle
from src.UI_unit_editor_wnd import UnitEditorWnd
import qtmodern.styles
import qtmodern.windows, json

data = updateJSON()
active_theme = getattr(UI_colorTheme, data["active_theme"])

app = QApplication([])

myStyle = ProxyStyle('Fusion')    
app.setStyle(myStyle)

screen = app.primaryScreen()
size = screen.size()

title = "Turnroot Unit Editor" 

if os.sep == "\\":
    font_string = "Lucida Sans Unicode"
else:
    font_string = "Lucida Grande"
    
with open("src/tmp/aic.json", "r") as cons:
    const = json.load(cons)
    
OPEN_LAST_FILE = const[0]
OPEN_NEW_FILE = const[1]

class mainN(UnitEditorWnd):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(QSize(int(size.width()/1.85), int(size.height()*.7)))
        self.setMaximumSize(QSize(int(size.width()), int(size.height())))

class main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(title)
        self.toolbar = QToolBar("")
        
        self.toolbar.setStyleSheet("background-color: "+active_theme.window_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
        self.toolbar.setIconSize(QSize(int(data["icon_size"]), int(data["icon_size"])))
        self.toolbar.setToolButtonStyle(Qt.ToolButtonIconOnly)
        
        self.menubar = self.menuBar()
        font = self.menubar.font()
        font.setPointSize(data["font_size"])
        
        self.m = mainN()
        self.setCentralWidget(self.m)
                        
window = main()
window.show()
a = app.exec_()