import sys
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QPalette, QIcon
import json
from UI_updateJSON import updateJSON
import UI_colorTheme
return_confirm = False

class confirmAction(QDialog):
    def __init__(self, s, parent=None):
        data = updateJSON()
        self.s = s
        self.return_confirm = return_confirm
        self.active_theme = getattr(UI_colorTheme, data["active_theme"])
        super().__init__(parent)
        self.setStyleSheet("font-size: "+str(data["font_size"]+3)+"px; background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        
        layout = QVBoxLayout()
        layout.setContentsMargins( 8,8,8,8)
        layout.setSpacing(0)
        self.setFixedSize((data["font_size"] * 22)+40, data["font_size"] * 7.4)
        
        self.label =QLabel("Do you want to "+str(s)+"?")
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        layout.addWidget(self.label, 1)
        self.yes = QPushButton(QIcon(), "Yes", self)
        self.yes.setMinimumHeight(data["font_size"] * 2)
        self.no = QPushButton(QIcon(), "No", self)
        self.no.setMinimumHeight(data["font_size"] * 2)
        
        boxes = QWidget()
        boxes_layout = QHBoxLayout()
        boxes_layout.addWidget(self.yes, 50)
        boxes_layout.addWidget(self.no, 50)
        boxes.setLayout(boxes_layout)
        layout.addWidget(boxes, 2)
        
        self.yes.clicked.connect(self.yes_clicked)
        self.no.clicked.connect(self.no_clicked)
        self.setLayout(layout)
        self.show()
    
    def yes_clicked(self):
        self.return_confirm = True
        self.close()
    def no_clicked(self):
        self.return_confirm = False
        self.close()

    

        
