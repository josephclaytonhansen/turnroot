from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from src.UI_node_graphics_scene import QDMGraphicsView, QDMGraphicsScene
from src.img_overlay_canvas import imageOverlayCanvas

import src.UI_colorTheme as UI_colorTheme
from src.UI_updateJSON import updateJSON
data = updateJSON()
active_theme = getattr(UI_colorTheme, data["active_theme"])

class PortraitEditorWnd(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        
    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        
        self.setStyleSheet("background-color: "+active_theme.window_background_color+"; color:"+active_theme.window_text_color+"; font-size: 16")
        
        self.tabs = QTabWidget()
        self.tabs_font = self.tabs.font()
        self.tabs_font.setPointSize(12)
        self.tabs.setFont(self.tabs_font)
        
        self.tabs.setTabPosition(QTabWidget.South)
        
        self.tscroll = QScrollArea()
        self.tscroll.setWidget(self.tabs)
        self.tscroll.setWidgetResizable(True)
        self.layout.addWidget(self.tscroll)
        
        self.tab_names = ["Dialogue Portraits", "Map Sprites", "Instance Appearance Variation"]
        self.tts = ["Edit unit appearance in dialogue",
                    "Edit small unit icon for maps",
                    "Edit variation"]
        
        self.tabs_dict = {}
        for tab in self.tab_names:
            self.tab_title = tab
            self.c_tab = QWidget()
            self.c_tab.setToolTip(self.tts[self.tab_names.index(tab)])
            self.c_tab_layout = QVBoxLayout()
            self.c_tab.setLayout(self.c_tab_layout)
            self.tabs_dict[tab] = self.c_tab
            self.tabs.addTab(self.c_tab, self.tab_title)
        
        self.tabs.currentChanged.connect(self.ctab_changed)
        
        self.initDP()
    
    def initDP(self):
        self.working_tab = self.tabs_dict["Dialogue Portraits"]
        self.working_tab_layout = self.working_tab.layout()
        self.canvas = imageOverlayCanvas()
        self.canvas.setMaximumWidth(1150)
        self.working_tab_layout.addWidget(self.canvas)
        
    def ctab_changed(self):
        pass


