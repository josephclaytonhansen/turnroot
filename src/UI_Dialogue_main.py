import sys, json, os, UI_colorTheme
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize
from UI_Dialogs import (confirmAction,
                        stackedInfoImgDialog,
                        infoClose)
from UI_updateJSON import updateJSON
from UI_node_editor_wnd import NodeEditorWnd

data = updateJSON()
active_theme = getattr(UI_colorTheme, data["active_theme"])

app = QApplication([])

screen = app.primaryScreen()
size = screen.size()

title = "Turnroot Game Dialogue Editor" 
class main(NodeEditorWnd):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(title)
        self.setMinimumSize(QSize(int(size.width()/3), int(size.height()/3)))
        self.setMaximumSize(QSize(int(size.width()), int(size.height())))
        self.resize(QSize(int(size.width()*.6), int(size.height()*.6)))

window = main()
window.show()
a = app.exec_()
