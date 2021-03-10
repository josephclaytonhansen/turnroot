import sys
import os
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QPalette, QIcon
import qtmodern.styles
import qtmodern.windows
from UI_updateJSON import updateJSON
from UI_ProxyStyle import ProxyStyle
from UI_Dialogs import confirmAction
import UI_colorTheme
from UI_color_test_widget import Color
hidev = False
showv = False
import json
with open("workspaces.json", "r") as read_file:
    workspaces = json.load(read_file)
    read_file.close()
    
class workspaceContainer(QWidget):
        def __init__(self, workspace, layout):
            self.hidev = hidev
            self.ws = workspace
            super().__init__()
            self.setAutoFillBackground(True)
            data = updateJSON()
            self.active_theme = getattr(UI_colorTheme, data["active_theme"])
            self.setStyleSheet("font-size: "+str(data["font_size"])+"px;color: "+self.active_theme.window_text_color)
            palette = self.palette()
            self.background_color = QColor(self.active_theme.workspace_background_color)
            self.workspaces = workspaces
            palette.setColor(QPalette.Window, self.background_color)
            self.setPalette(palette)
            self.layout = QVBoxLayout()
            self.layout.setContentsMargins(2,2,2,2)
            self.layout.setSpacing(4)
            self.label = QLabel("Label")
            font = self.label.font()
            font.setPointSize(int(data["icon_size"])/2)
            self.label.setFont(font)
            self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

            self.layout.addWidget(self.label)
            self.layout.addWidget(Color(self.active_theme.window_background_color))
            self.layout.addWidget(Color(self.active_theme.list_background_color))
            self.setLayout(self.layout)

class showWorkspace(QPushButton):
    def __init__(self, workspace, layout):
        super().__init__()
        data = updateJSON()
        self.workspace = workspace
        self.layout = layout
        self.active_theme = getattr(UI_colorTheme, data["active_theme"])
        self.setText("+")
        self.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.setFixedSize((int(data["icon_size"]) -3), (int(data["icon_size"]) -3))
        
class hideWorkspace(QPushButton):
    def __init__(self, workspace, layout):
        super().__init__()
        data = updateJSON()
        self.workspace = workspace
        self.layout = layout
        self.active_theme = getattr(UI_colorTheme, data["active_theme"])
        self.setText("—")
        self.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.setFixedSize((int(data["icon_size"])-3), (int(data["icon_size"])-3))

        

    

            


    