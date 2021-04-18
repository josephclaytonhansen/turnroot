import sys, json, os
import src.UI_colorTheme as UI_colorTheme
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize
from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QPalette, QIcon, QPixmap
from src.UI_updateJSON import updateJSON
from src.UI_node_editor_wnd import NodeEditorWnd

data = updateJSON()
active_theme = getattr(UI_colorTheme, data["active_theme"])

app = QApplication([])

screen = app.primaryScreen()
size = screen.size()

title = "Turnroot Game Dialogue Editor" 
class mainN(NodeEditorWnd):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(title)
        self.setMinimumSize(QSize(int(size.width()/3), int(size.height()/3)))
        self.setMaximumSize(QSize(int(size.width()), int(size.height())))
        self.resize(QSize(int(size.width()*.6), int(size.height()*.6)))

class main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.toolbar = QToolBar("")
        self.toolbar.setStyleSheet("background-color: "+active_theme.window_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
        self.toolbar.setIconSize(QSize(int(data["icon_size"]), int(data["icon_size"])))
        self.toolbar.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.addToolBar(self.toolbar)
        self.setCentralWidget(mainN())
        
window = main()
window.show()
a = app.exec_()
