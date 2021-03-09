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

class workspaceContainer(QWidget):
        def __init__(self, workspace, layout):
            super().__init__()
            self.setAutoFillBackground(True)
            data = updateJSON()
            self.active_theme = getattr(UI_colorTheme, data["active_theme"])
            self.setStyleSheet("font-size: "+str(data["font_size"])+"px;color: "+self.active_theme.window_text_color)
            palette = self.palette()
            self.background_color = QColor(self.active_theme.workspace_background_color)

            palette.setColor(QPalette.Window, self.background_color)
            self.setPalette(palette)
            self.layout = QVBoxLayout()
            self.layout.setContentsMargins(0,0,0,0)
            self.layout.setSpacing(4)
            self.label = QLabel("Label")
            font = self.label.font()
            font.setPointSize(data["font_size"])
            self.label.setFont(font)
            self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.layout.addWidget(self.label)
            self.layout.addWidget(Color(self.active_theme.window_background_color))
            self.layout.addWidget(Color(self.active_theme.list_background_color))
            self.setLayout(self.layout)


    