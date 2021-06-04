from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from src.UI_node_graphics_scene import QDMGraphicsView, QDMGraphicsScene

from src.skeletons.Object import (Object,usableItem,Key,healItem,statIncreaseItem,expIncreaseItem,
                                  classChangeItem,summoningItem,levelEffectItem,equippableItem,Weapon,Shield)

import src.UI_colorTheme as UI_colorTheme
from src.UI_updateJSON import updateJSON
from src.game_directory import gameDirectory
data = updateJSON()
active_theme = getattr(UI_colorTheme, data["active_theme"])

class ObjectEditorWnd(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        
    def initUI(self):
        self.path = None
        self.item_templates = {"Basic Object":Object,
                               "Usable Item":usableItem,
                               "Key":Key,
                               "Heal Item":healItem,
                               "Stat+ Item":statIncreaseItem,
                               "EXP/Knowledge+ Item":expIncreaseItem,
                               "Class Change Item":classChangeItem,
                               "Unit Summoning Item":summoningItem,
                               "Level Effect Item":levelEffectItem,
                               "Equippable Item":equippableItem,
                               "Weapon":Weapon,
                               "Shield":Shield}
        
        self.setStyleSheet("background-color: "+active_theme.window_background_color+"; color:"+active_theme.window_text_color+"; font-size: 16")
        
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
        
        self.tab_names = ["Weapons", "Equippable Items", "Usable Items", "Non-Combat Items"]
        self.tts = ["Edit weapon objects","Edit equippable items such as shields",
                    "Edit usable items (healing items, seals, keys, torches, etc)",
                    "Edit non-combat items (cooking, tea, gifts, forging items, unit summoning items)"]
        
        self.tabs_dict = {}
        for tab in self.tab_names:
            self.tab_title = tab
            self.c_tab = QWidget()
            self.c_tab.setToolTip(self.tts[self.tab_names.index(tab)])
            self.c_tab_layout = QGridLayout()
            self.c_tab.setLayout(self.c_tab_layout)
            self.tabs_dict[tab] = self.c_tab
            self.tabs.addTab(self.c_tab, self.tab_title)
        
        self.tabs.currentChanged.connect(self.ctab_changed)
        
        self.initObject()
        
        self.initWeapons()
        self.initEquippable()
        self.initUsable()
        self.initNonCombat()
        
        self.layout.addWidget(self.tscroll)
        
        self.show()
    
    def initObject(self):
        pass

    def initWeapons(self):
        pass
    
    def initEquippable(self):
        pass
    
    def initUsable(self):
        pass
    
    def initNonCombat(self):
        pass
    
    def ctab_changed(self):
        pass
    
    def objectFromJSON(self):
        pass
    
    def objectToJSON(self):
        pass
    
    def newObject(self):
        pass
    
    def loadObject(self):
        pass

