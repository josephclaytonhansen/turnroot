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
import json

def initEsen(self):
    self.working_tab = self.tabs_dict["Essential Game Settings"]
    self.working_tab_layout = self.working_tab.layout()
    
    self.es_instr = QLabel("Before you can edit most of the game settings, you need to set the game name and game folder. \nAll the files you create going forward are in the game folder.\nPlease make sure the folder you choose for the game folder is empty.")
    self.working_tab_layout.addWidget(self.es_instr)
        
    q_list = ["What is your game called?","Set game folder", "What should the end credits say?", "Supply your own cover art or have one auto-generated?"]
    o_list = [["Edit"], ["Choose folder"], ["Edit"], ["Supply my own", "Auto-generate"]]
    colors = [[self.colors["GREY"]],
              [self.colors["GREY"]],
              [self.colors["GREY"]],
              [self.colors["GREY"],
               self.colors["GREY"]]]
    helpts = ["","","","","",""]
    
    for q in q_list:
        w = selectionRow(self, q,
                                                       o_list[q_list.index(q)],
                                                       colors[q_list.index(q)],
                                                       helpts[q_list.index(q)])
        self.working_tab_layout.addWidget(w)
        self.weapon_rows[q] = w
    
    #check and publish
    self.check_for_errors = QPushButton("Check game for errors")
    self.check_for_errors.clicked.connect(self.checkErrors)
    self.package = QPushButton("Create game package")
    self.check_for_errors.setMinimumHeight(48)
    self.package.setMinimumHeight(48)
    self.package.setStyleSheet("background-color:"+active_theme.button_alt_color+";color:"+active_theme.button_alt_text_color)
    self.check_for_errors.setStyleSheet("background-color:"+active_theme.window_background_color+";color:"+active_theme.window_text_color)
    self.go_row = QWidget()
    self.go_row_layout = QHBoxLayout()
    self.go_row.setLayout(self.go_row_layout)
    self.go_row_layout.addWidget(self.check_for_errors)
    self.go_row_layout.addWidget(self.package)
    self.working_tab_layout.addWidget(self.go_row)
        
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
        w = selectionRow(self, q,
                                                       o_list[q_list.index(q)],
                                                       colors[q_list.index(q)],
                                                       helpts[q_list.index(q)])
        self.working_tab_layout.addWidget(w)
        self.weapon_rows[q] = w
        
def initD(self):
    self.working_tab = self.tabs_dict["Display"]
    self.working_tab_layout = self.working_tab.layout()
    
    q_list = ["Units can have how many skills equipped?",
              "Units can have how many items in inventory?",
              "How do skills display?",
              "How do units display?"
              ]
    o_list = [["5", "6", "7"],
              ["5", "6","7","8"],
              ["In grid as icons", "In list as icons + name"],
              ["One page", "Multiple pages"]]
    
    colors = [[self.colors["GREY"],self.colors["GREY"],self.colors["GREY"]],
              [self.colors["GREY"],self.colors["GREY"],self.colors["GREY"],self.colors["GREY"]],
              [self.colors["BLUE"],self.colors["PURPLE"]],
              [self.colors["BLUE"],self.colors["PURPLE"]]
              ]
    helpts = ["","","",""]
    
    for q in q_list:
        w = selectionRow(self, q,
                                                       o_list[q_list.index(q)],
                                                       colors[q_list.index(q)],
                                                       helpts[q_list.index(q)])
        self.working_tab_layout.addWidget(w)
        self.weapon_rows[q] = w

def initWeapons(self):
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
        if q == "What does item forging do?" or q == "Does encumbrance affect movement or speed?":
            self.weapon_rows[q].setVisible(False)
            
def initCombat(self):
    self.working_tab = self.tabs_dict["Combat"]
    self.working_tab_layout = self.working_tab.layout()
    
    q_list = ["Use tactics? (similar to gambits)",
              "Use skilled blows? (similar to combat arts)",
              "Enable 'extra' experience types in addition to weapon types (i.e. riding/flying)?",
              "Can game map have random encounters?",
              "Is the difficulty of random encounters calculated by map location or team level?",
              "Can time be turned back?",
              "How much damage do criticals do?",
              ]
    o_list = [["Yes", "No"], ["Yes", "No"],["Yes", "No"],["Yes", "No"],
              ["Map location", "Team level"],
              ["Yes", "No"],
              ["2x", "2.5x", "3x"]
              ]
    colors = [[self.colors["PURPLE"],self.colors["BLUE"]],
              [self.colors["PURPLE"],self.colors["BLUE"]],
              [self.colors["PURPLE"],self.colors["BLUE"]],
              [self.colors["BLUE"],self.colors["PURPLE"]],
              [self.colors["BLUE"],self.colors["RED"]],
              [self.colors["PURPLE"],self.colors["RED"]],
              [self.colors["RED"],self.colors["GREY"],self.colors["BLUE"]],
              ]
    helpts = ["","","","","","",""]
    
    for q in q_list:
        w = selectionRow(self, q,
                                                       o_list[q_list.index(q)],
                                                       colors[q_list.index(q)],
                                                       helpts[q_list.index(q)])
        self.working_tab_layout.addWidget(w)
        self.weapon_rows[q] = w
        
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
              
              ]
    helpts = ["","","","","","","","",""]
    
    for q in q_list:
        w = selectionRow(self, q,
                                                       o_list[q_list.index(q)],
                                                       colors[q_list.index(q)],
                                                       helpts[q_list.index(q)])
        self.working_tab_layout.addWidget(w)
        self.weapon_rows[q] = w
        
def initR(self):
    self.working_tab = self.tabs_dict["Relationships"]
    self.working_tab_layout = self.working_tab.layout()
    
    q_list = ["When can S level supports (marriage) occur?",
              "Can S level supports produce children?",
              "Do children units have paralogues?",
              "Can units 'pair up' or be assigned as 'adjutants'?",
              "Can units pick up or 'rescue' other units?",
              "Can units have linked attacks when adjacent?"
              ]
    
    o_list = [["Immediately once support is high enough", "Not until a game event"],
              ["Yes", "No"],
              ["Yes", "No"],
              ["Pair up", "Adjutants","Neither"],
              ["Yes", "No"],
              ["Yes", "No"]]
    
    colors = [[self.colors["BLUE"],self.colors["PURPLE"]],
              [self.colors["BLUE"],self.colors["PURPLE"]],
              [self.colors["BLUE"],self.colors["GREY"]],
              [self.colors["BLUE"],self.colors["PURPLE"],self.colors["RED"]],
              [self.colors["RED"],self.colors["BLUE"]],
              [self.colors["PURPLE"],self.colors["BLUE"]]
              ]
    helpts = ["","","","","",""]
    
    for q in q_list:
        w = selectionRow(self, q,
                                                       o_list[q_list.index(q)],
                                                       colors[q_list.index(q)],
                                                       helpts[q_list.index(q)])
        self.working_tab_layout.addWidget(w)
        self.weapon_rows[q] = w
        if q == "Do children units have paralogues?":
            self.weapon_rows[q].setVisible(False)
            
def initM(self):
    self.working_tab = self.tabs_dict["Map/Hub"]
    self.working_tab_layout = self.working_tab.layout()
    
    q_list = ["Does game have hub, map, or both?",
              "Do completed levels become shops?",
              "Are there travelling merchants?",
              "Can player shop in the hub?",
              "Does player have 'free time'?",
              "Can player use items on map?",
              "Does player choose missions from the hub or the map?",
              "Is hub accessed from map menu, or is map accessed from hub?"
              ]
    
    o_list = [["Map", "Hub", "Both"],
              ["Yes", "No"],
              ["Yes", "No"],
              ["Yes", "No"],
              ["Yes", "No"],
              ["Yes", "No"],
              ["Map", "Hub"],
              ["Map goes to hub", "Hub goes to map"],]
    
    colors = [[self.colors["RED"],self.colors["PURPLE"],self.colors["BLUE"]],
              [self.colors["BLUE"],self.colors["GREY"]],
              [self.colors["BLUE"],self.colors["GREY"]],
              [self.colors["PURPLE"],self.colors["BLUE"]],
              [self.colors["PURPLE"],self.colors["GREY"]],
              [self.colors["BLUE"],self.colors["GREY"]],
              [self.colors["BLUE"],self.colors["GREY"]],
              [self.colors["BLUE"],self.colors["GREY"]]
              ]
    helpts = ["","","","","","","",""]
    
    for q in q_list:
        w = selectionRow(self, q,
                                                       o_list[q_list.index(q)],
                                                       colors[q_list.index(q)],
                                                       helpts[q_list.index(q)])
        self.working_tab_layout.addWidget(w)
        self.weapon_rows[q] = w
        if q != "Does game have hub, map, or both?":
            self.weapon_rows[q].setVisible(False)
        if q == "Does game have hub, map, or both?":
            self.weapon_rows[q].setVisible(True)

