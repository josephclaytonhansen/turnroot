from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import src.UI_colorTheme as UI_colorTheme
from src.UI_updateJSON import updateJSON
data = updateJSON()
active_theme = getattr(UI_colorTheme, data["active_theme"])

from src.UI_game_editor_backend import selectionRow

class GameEditorWnd(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.active_theme = active_theme
        self.initUI()
        
        
    def initUI(self):
        self.getColors()

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        
        self.tabs = QTabWidget()
        self.tabs_font = self.tabs.font()
        self.tabs_font.setPointSize(12)
        self.tabs.setFont(self.tabs_font)
        
        self.tabs.setTabPosition(QTabWidget.South)
        
        self.tscroll = QScrollArea()
        self.tscroll.setWidget(self.tabs)
        self.tscroll.setWidgetResizable(True)
        
        self.tab_names = ["Essential Game Settings", "Misc", "Weapons", "Combat", "Units/Classes", "Map/Hub", "Relationships"]
        
        self.tabs_dict = {}
        for tab in self.tab_names:
            self.tab_title = tab
            self.c_tab = QWidget()
            self.c_tab_layout = QVBoxLayout()
            self.c_tab.setLayout(self.c_tab_layout)
            self.tabs_dict[tab] = self.c_tab
            self.tabs.addTab(self.c_tab, self.tab_title)
            
        self.tabs.tabBar().setEnabled(False)
        #until there's a name and a directory, you can't change tabs
        
        #self.tabs.currentChanged.connect(self.ctab_changed)
        
        self.layout.addWidget(self.tscroll)
        
        self.initEsen()
        #init rest
    
    def initEsen(self):
        self.working_tab = self.tabs_dict["Essential Game Settings"]
        self.working_tab_layout = self.working_tab.layout()
        
        q_list = ["What is your game called?","Set game folder", "What genres apply to your game?", "What should the end credits say?", "Supply your own cover art or have one auto-generated?"]
        o_list = [["Edit"], ["Choose folder"], ["Edit"], ["Edit"], ["Supply my own", "Auto-generate"]]
        colors = [[self.active_theme.window_background_color],[self.active_theme.window_background_color],[self.active_theme.window_background_color],[self.active_theme.window_background_color],
                  [self.active_theme.window_background_color,self.active_theme.window_background_color]]
        helpts = ["","","","","",""]
        
        for q in q_list:
            self.working_tab_layout.addWidget(selectionRow(self, q,
                                                           o_list[q_list.index(q)],
                                                           colors[q_list.index(q)],
                                                           helpts[q_list.index(q)]))
            
    def getColors(self):
        blue = "#3372b0"
        red = "#f15f2a"
        purple = "#7F55c7"
        self.colors = {"BLUE":blue,"RED":red,"PURPLE":purple}
        




