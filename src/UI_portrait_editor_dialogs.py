import sys, json, os
import src.UI_colorTheme as UI_colorTheme
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from src.UI_updateJSON import updateJSON
from src.game_directory import gameDirectory
from src.UI_Dialogs import confirmAction, infoClose, switchEditorDialog, REPLACE_WINDOW, NEW_WINDOW
import qtmodern.styles
import qtmodern.windows

data = updateJSON()
active_theme = getattr(UI_colorTheme, data["active_theme"])

class portraitStackWidget(QWidget):
    def __init__(self, parent=None,font=None,stack=None):
        super().__init__(parent)
        self.body_font = font
        self.parent = parent
        self.stack = stack
        self.initUI()
        
    def initUI(self):
        self.path = None
        
        self.setStyleSheet("background-color: "+active_theme.window_background_color+"; color:"+active_theme.window_text_color+"; font-size: 16")

        self.layout = QGridLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(2)
        self.setLayout(self.layout)
        
        self.counts = {"base":0,"hair":0, "scars":0, "freckles":0, "jewelry":0, "masks":0,"eyes":0,
                       "tattoos":0, "facial hair":0, "makeup":0, "tops":0, "headwear":0, "armor":0,
                       "nose":0,"mouth":0,"eyebrows":0}
        self.max_counts = {"base":1,"hair":3, "scars":6, "freckles":4, "jewelry":6, "masks":2, "tattoos":5, "eyes":1,
                           "facial hair":3,"makeup":3, "tops":3, "headwear":4, "armor":3,"nose":1,"mouth":1,"eyebrows":1}
        self.parent.total_layers = 0
    
    def initContent(self, s):
        s = s.lower()
        self.initItem(s)
            
    def initItem(self,item):
        self.counts[item] += 1
        if self.counts[item] <= self.max_counts[item]:

            t = item+" " + str(self.counts[item])
            
            self.parent.total_layers = len(self.parent.layer_orders)+1
            self.parent.layer_orders[self.parent.total_layers] = t
            self.parent.layers_box.clear()
            for g in self.parent.layer_orders:
                self.parent.layers_box.addItem(self.parent.layer_orders[g])
            #add stack widget
