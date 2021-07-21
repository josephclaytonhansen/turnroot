from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import src.UI_colorTheme as UI_colorTheme
from src.UI_updateJSON import updateJSON
data = updateJSON()
active_theme = getattr(UI_colorTheme, data["active_theme"])

from src.UI_game_editor_backend import selectionRow
from src.game_directory import gameDirectory
from src.UI_Dialogs import textEntryDialog

game_options = {}

class GameEditorWnd(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.active_theme = active_theme
        self.check_tb = True
        #when loading, this also needs to change
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
        
        self.tabs.setTabPosition(QTabWidget.North)
        
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
        self.initMisc()
        self.initWeapons()
        self.initCombat()
        self.initUC()
        #init rest
    
    def initEsen(self):
        self.working_tab = self.tabs_dict["Essential Game Settings"]
        self.working_tab_layout = self.working_tab.layout()
        
        self.es_instr = QLabel("Before you can edit most of the game settings, you need to set the game name and game folder. \nAll the files you create going forward are in the game folder.\nPlease make sure the folder you choose for the game folder is empty.")
        self.working_tab_layout.addWidget(self.es_instr)
            
        q_list = ["What is your game called?","Set game folder", "What genres apply to your game?", "What should the end credits say?", "Supply your own cover art or have one auto-generated?"]
        o_list = [["Edit"], ["Choose folder"], ["Edit"], ["Edit"], ["Supply my own", "Auto-generate"]]
        colors = [[self.colors["GREY"]],[self.colors["GREY"]],[self.colors["GREY"]],[self.colors["GREY"]],
                  [self.colors["GREY"],self.colors["GREY"]]]
        helpts = ["","","","","",""]
        
        for q in q_list:
            self.working_tab_layout.addWidget(selectionRow(self, q,
                                                           o_list[q_list.index(q)],
                                                           colors[q_list.index(q)],
                                                           helpts[q_list.index(q)]))
    def initMisc(self):
        self.working_tab = self.tabs_dict["Misc"]
        self.working_tab_layout = self.working_tab.layout()
        
        q_list = ["Can protagonist appearance be customized?","Can protagonist name/pronouns be customized?",
                  "Is map music and combat music the same, or is there a version of map music for combat?",
                  "Does enemy turn have unique music?",
                  "Are cutscenes portrait against background based or video based?",
                  "Does game have voice acting?"
                  ]
        o_list = [["Yes", "No"], ["Yes", "No"], ["The same", "Different"], ["Yes", "No"], ["Portraits", "Videos"],["Yes", "No"]]
        colors = [[self.colors["BLUE"],self.colors["RED"]],
                  [self.colors["PURPLE"],self.colors["RED"]],
                  [self.colors["RED"],self.colors["BLUE"]],
                  [self.colors["BLUE"],self.colors["PURPLE"]],
                  [self.colors["RED"],self.colors["BLUE"]],
                  [self.colors["BLUE"],self.colors["RED"]]
                  ]
        helpts = ["","","","","",""]
        
        for q in q_list:
            self.working_tab_layout.addWidget(selectionRow(self, q,
                                                           o_list[q_list.index(q)],
                                                           colors[q_list.index(q)],
                                                           helpts[q_list.index(q)]))
    
    def initWeapons(self):
        self.weapon_rows = {}
        self.working_tab = self.tabs_dict["Weapons"]
        self.working_tab_layout = self.working_tab.layout()
        
        q_list = ["Use weapon triangle?", "Use weapon durability?", "How are magic weapons gained?",
                  "Is item forging enabled?", "What does item forging do?",
                  "Do magic weapons gain full durability at the beginning of each battle?",
                  "Do units have encumbrance (weapon weight affecting movement/speed)?",
                  "Does encumbrance affect movement or speed?",
                  "Use prowess skills (as weapon experience levels up, prowess skill levels up)?"
                  ]
        o_list = [["Yes", "No"], ["Yes", "No"],
                  ["Bought like other items", "Learned with classes/experience level"],
                  ["Yes", "No"],
                  ["Create new weapons", "Enhance existing weapon"],
                  ["Yes", "No"],
                  ["Yes", "No"],
                  ["Movement", "Speed"],
                  ["Yes", "No"]]
        colors = [[self.colors["BLUE"],self.colors["PURPLE"]],
                  [self.colors["BLUE"],self.colors["GREY"]],
                  [self.colors["BLUE"],self.colors["PURPLE"]],
                  [self.colors["BLUE"],self.colors["RED"]],
                  [self.colors["PURPLE"],self.colors["BLUE"]],
                  [self.colors["PURPLE"],self.colors["BLUE"]],
                  [self.colors["PURPLE"],self.colors["BLUE"]],
                  [self.colors["GREY"],self.colors["GREY"]],
                  [self.colors["PURPLE"],self.colors["BLUE"]]
                  ]
        helpts = ["","","","","","","","",""]
        
        for q in q_list:
            w = selectionRow(self, q,
                                                           o_list[q_list.index(q)],
                                                           colors[q_list.index(q)],
                                                           helpts[q_list.index(q)])
            self.working_tab_layout.addWidget(w)
            self.weapon_rows[q] = w
            if q == "What does item forging do?":
                self.weapon_rows[q].setVisible(False)
                
    def initCombat(self):
        self.working_tab = self.tabs_dict["Combat"]
        self.working_tab_layout = self.working_tab.layout()
        
        q_list = ["Use tactics? (similar to gambits)",
                  "Use skilled blows? (similar to combat arts)",
                  "Enable 'extra' experience types in addition to weapon types (i.e. riding/flying)?",
                  "Can game map have random encounters?",
                  "Is the difficulty of random encounters calculated by map location or team level?",
                  "Can time be turned back?"
                  ]
        o_list = [["Yes", "No"], ["Yes", "No"],["Yes", "No"],["Yes", "No"],
                  ["Map location", "Team level"],
                  ["Yes", "No"]
                  ]
        colors = [[self.colors["PURPLE"],self.colors["BLUE"]],
                  [self.colors["PURPLE"],self.colors["BLUE"]],
                  [self.colors["PURPLE"],self.colors["BLUE"]],
                  [self.colors["BLUE"],self.colors["PURPLE"]],
                  [self.colors["BLUE"],self.colors["RED"]],
                  [self.colors["PURPLE"],self.colors["RED"]],
                  ]
        helpts = ["","","","","",""]
        
        for q in q_list:
            self.working_tab_layout.addWidget(selectionRow(self, q,
                                                           o_list[q_list.index(q)],
                                                           colors[q_list.index(q)],
                                                           helpts[q_list.index(q)]))
    def initUC(self):
        self.working_tab = self.tabs_dict["Units/Classes"]
        self.working_tab_layout = self.working_tab.layout()
        
        q_list = ["Do units have stat caps?",
                  "Do classes have stat growth rates, or is stat growth just by unit?",
                  "Do units reset to level 1 when changing class?",
                  "Are classes solely level based, criteria based, or both?",
                  "Does reclassing require items?",
                  "How many levels of classes are there?",
                  "Are classes limited by previous class?",
                  "When reclassing, is there a grid of options or a list?",
                  "Can units reclass during combat, or only out of combat?",
                  "Units can have how many skills equipped?",
                  "Units can have how many items in inventory?",
                  "How do skills display?",
                  "How do units display?"
                  ]
        o_list = [["Yes", "No"],
                  ["Classes have stat growth rates", "Stat growth is just by unit rates"],
                  ["Yes", "No"],
                  ["Level based", "Criteria based", "Both"],
                  ["Yes", "No"],
                  ["2 (Basic, Advanced)", "3 (Basic, Advanced, Master)"],
                  ["Yes", "No (units can reclass to any class)"],
                  ["List", "Grid"],
                  ["In combat", "Only out of combat"],
                  ["5", "6", "7"],
                  ["5", "6","7","8"],
                  ["In grid as icons", "In list as icons + name"],
                  ["One page", "Multiple pages"],
                  ]
        colors = [[self.colors["GREY"],self.colors["GREY"]],
                  [self.colors["GREY"],self.colors["GREY"]],
                  [self.colors["BLUE"],self.colors["PURPLE"]],
                  [self.colors["BLUE"],self.colors["GREY"],self.colors["PURPLE"]],
                  [self.colors["BLUE"],self.colors["RED"]],
                  [self.colors["BLUE"],self.colors["PURPLE"]],
                  [self.colors["BLUE"],self.colors["PURPLE"]],
                  [self.colors["BLUE"],self.colors["PURPLE"]],
                  [self.colors["BLUE"],self.colors["PURPLE"]],
                  [self.colors["GREY"],self.colors["GREY"],self.colors["GREY"]],
                  [self.colors["GREY"],self.colors["GREY"],self.colors["GREY"],self.colors["GREY"]],
                  [self.colors["BLUE"],self.colors["PURPLE"]],
                  [self.colors["BLUE"],self.colors["PURPLE"]]
                  ]
        helpts = ["","","","","","","","","","","","",""]
        
        for q in q_list:
            self.working_tab_layout.addWidget(selectionRow(self, q,
                                                           o_list[q_list.index(q)],
                                                           colors[q_list.index(q)],
                                                           helpts[q_list.index(q)]))  
    def getColors(self):
        blue = "#3372b0"
        red = "#f15f2a"
        purple = "#7F55c7"
        grey = "#555555"
        self.colors = {"BLUE":blue,"RED":red,"PURPLE":purple,"GREY":grey}
        
    def toggleOption(self):
        global game_options
        for o in self.sender().row.options:
            if self.sender().row.options[o] != self.sender():
                self.sender().row.options[o].setChecked(False)
        game_options[self.sender().row_name] = self.sender().name
        if self.check_tb:
            if 'What is your game called?' in game_options:
                if 'Set game folder' in game_options:
                    self.tabs.tabBar().setEnabled(True)
                    self.check_tb = False
                    self.es_instr.setVisible(False)
                    
        #set game folder            
        if self.sender().row_name == "Set game folder":
            g = gameDirectory(self)
            g.changePath(g.pathDialog())
            if g.path != None:
                self.sender().setText(g.path)
                game_options[self.sender().row_name] = g.path
                
        #set game name        
        elif self.sender().row_name == "What is your game called?":
            h = textEntryDialog(self)
            h.exec_()
            if h.data != None:
                self.sender().setText(h.data)
                game_options[self.sender().row_name] = h.data
        
        #show item forging specifics
        elif self.sender().row_name == "Is item forging enabled?":
            if self.sender().text() == "Yes":
                self.weapon_rows["What does item forging do?"].setVisible(True)
            else:
                self.weapon_rows["What does item forging do?"].setVisible(False)
                
        print(game_options)



