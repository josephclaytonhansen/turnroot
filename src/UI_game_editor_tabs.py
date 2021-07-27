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
    helpts = [[None,["The game will show up in the player's game list as this", "This is one of two required settings to access other editors"],["font-size:24px;",None]],
              [None,["The game folder contains all the files in the game.","The necessary sub-folders are created automatically.","This is one of two required settings to access other editors","Note that changing the game folder will reset all game options"],["font-size:24px;",None,None, None]],
              [None, ["Who are you/your team?", "This will allow you to show your team's names or aliases in the credits of the game"],["font-size:24px;",None]],
              [None, ["What is the cover of your game?", "If you have your own cover artwork, you can upload it- otherwise, your cover will just be text"],["font-size:24px;",None]],
              [],[],[]]
    
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
    self.package.setFont(self.body_font)
    self.check_for_errors.setFont(self.body_font)
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
    helpts = [[None,["If enabled, player has customization options at the start of game", "This includes hair color, skin color, and hair style by default.","You can change this in the Flow Editor"],["font-size:24px;",None,None]],
              [None,["If enabled, player can type in their own name and change pronouns","You can edit those settings in the Unit Editor, when editing the protagonist"],["font-size:24px;",None]],
              [None,["Music can fade to combat music in combat", "Make sure to add both version in the Music folder","You can learn more in the Level Editor"],["font-size:24px;",None,None]],
              [None,["'Yes' means each map has at least 3 tracks", "Player turn (map), player turn (combat), and enemy turn"],["font-size:24px;",None]],
              [None,["Video based will require you to create your own videos", "Because of the work involved in this, POB is generally recommended.","Fire Emblem: Sacred Stones is a great example of POB"],["font-size:24px;",None, None]],
              [None,["'Yes' means you provide voice tracks for dialogue.", "No doesn't mean game doesn't have voices- you can use our generic sounds or provide your own.","Rather, No means that dialogue isn't being read word for word.","No is highly recommended"],["font-size:24px;",None,None,None]],
              ]
    
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
    helpts = [[None,["Set a cap on equipped skills", "Player can switch out equipped skills, this just limits how many can be equipped at a time"],["font-size:24px;",None]],
              [None,["Set a cap on items", "Based on Game Editor settings, magic weapons may not be counted towards this total"],["font-size:24px;",None]],
              [None,["Note that 'grid' will be a more compact display ", "Specifically, the player will be able to see unit information all in one place"],["font-size:24px;",None]],
              [None,["This relates to skill display", "If 'List' and 'One Page' are both selected, the view will actually be two pages"],["font-size:24px;",None]]]
    
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
              "Use prowess skills (as weapon experience levels up, prowess skill levels up)?",
              "Do skill levels have midpoints (i.e.: E goes to E+) or not (E goes to D)?"
              ]
    o_list = [["Yes", "No"], ["Yes", "No"],
              ["Bought like other items", "Learned with classes/experience level"],
              ["Yes", "No"],
              ["Create new weapons", "Enhance existing weapon"],
              ["Yes", "No"],
              ["Yes", "No"],
              ["Movement", "Speed"],
              ["Yes", "No"],
              ["Use +", "Don't Use +"]]
    colors = [[self.colors["BLUE"],self.colors["PURPLE"]],
              [self.colors["BLUE"],self.colors["GREY"]],
              [self.colors["BLUE"],self.colors["PURPLE"]],
              [self.colors["BLUE"],self.colors["RED"]],
              [self.colors["PURPLE"],self.colors["BLUE"]],
              [self.colors["PURPLE"],self.colors["BLUE"]],
              [self.colors["PURPLE"],self.colors["BLUE"]],
              [self.colors["GREY"],self.colors["GREY"]],
              [self.colors["PURPLE"],self.colors["BLUE"]],
               [self.colors["PURPLE"],self.colors["BLUE"]]
              ]
    helpts = ["","","","","","","","","",""]
    
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
              "Can units have linked attacks when adjacent?",
              "Do relationship levels have midpoints (i.e.: E goes to E+) or not (E goes to D)?"
              ]
    
    o_list = [["Immediately once support is high enough", "Not until a game event"],
              ["Yes", "No"],
              ["Yes", "No"],
              ["Pair up", "Adjutants","Neither"],
              ["Yes", "No"],
              ["Yes", "No"],
              ["Use +", "Don't Use +"]]
    
    colors = [[self.colors["BLUE"],self.colors["PURPLE"]],
              [self.colors["BLUE"],self.colors["PURPLE"]],
              [self.colors["BLUE"],self.colors["GREY"]],
              [self.colors["BLUE"],self.colors["PURPLE"],self.colors["RED"]],
              [self.colors["RED"],self.colors["BLUE"]],
              [self.colors["PURPLE"],self.colors["BLUE"]],
               [self.colors["PURPLE"],self.colors["BLUE"]]
              ]
    helpts = ["","","","","","",""]
    
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
    