from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import src.UI_colorTheme as UI_colorTheme
from src.UI_updateJSON import updateJSON
from src.UI_game_editor_dialogs import weaponTriangle, creditsDialog, uploadGameArtDialog
data = updateJSON()
active_theme = getattr(UI_colorTheme, data["active_theme"])

from src.game_directory import gameDirectory
from src.UI_game_editor_tabs import (initEsen,
        initMisc,
        initWeapons,
        initCombat,
        initUC,
        initR,
        initM,
        initD)
from src.UI_Dialogs import textEntryDialog, infoClose, stackedInfoImgDialog
from src.UI_game_editor_backend import checkDialog, gameArtGenerate
from src.UI_game_editor_dialogs import magicExperienceDialog
import json, os
game_options = {}

class GameEditorWnd(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.active_theme = active_theme
        self.check_tb = True
        #when loading, this also needs to change
        self.weapon_rows = {}
        self.initUI()
        
        
    def initUI(self):
        self.getColors()
        self.body_font = self.parent.unit_editor.body_font

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
        
        self.tab_names = ["Essential Game Settings", "Misc", "Display", "Weapons", "Combat", "Units/Classes", "Map/Hub", "Relationships"]
        
        self.tabs_dict = {}
        for tab in self.tab_names:
            self.tab_title = tab
            self.c_tab = QWidget()
            self.c_tab_layout = QVBoxLayout()
            self.c_tab.setLayout(self.c_tab_layout)
            self.tabs_dict[tab] = self.c_tab
            self.tabs.addTab(self.c_tab, self.tab_title)
            
        self.tabs.tabBar().setEnabled(False)
        self.tabs.currentChanged.connect(self.tab_change)
        #until there's a name and a directory, you can't change tabs
        
        #self.tabs.currentChanged.connect(self.ctab_changed)
        
        self.layout.addWidget(self.tscroll)
        
        initEsen(self)
        initMisc(self)
        initWeapons(self)
        initCombat(self)
        initUC(self)
        initR(self)
        initM(self)
        initD(self)
        
        g = gameDirectory(self)
        g.getPath()
        print(g.path)

        if g.path != "" and os.path.exists(g.path):
            self.parent.backButton.setEnabled(True)
            self.tabs.tabBar().setEnabled(True)
            self.check_tb = False
            self.es_instr.setVisible(False)
            self.game_path = g.path
            self.Load()
           
    def getColors(self):
        blue = "#3372b0"
        red = "#f15f2a"
        purple = "#7F55c7"
        grey = "#555555"
        self.colors = {"BLUE":blue,"RED":red,"PURPLE":purple,"GREY":grey}
    
    def Load(self):
        self.weapon_rows["What is your game called?"].dL.setPixmap(QPixmap("src/ui_icons/on.png"))
        self.weapon_rows["Set game folder"].dL.setPixmap(QPixmap("src/ui_icons/on.png"))
        with open(self.game_path+"/dat.trsl", "r") as g:
            data = json.load(g)
        for item in self.weapon_rows:
            try:
                if item in data:
                    self.weapon_rows[item].options[data[item]].setChecked(True)
                    self.weapon_rows[item].dL.setPixmap(QPixmap("src/ui_icons/on.png"))
            except:
                pass
    
    def tab_change(self):
        global game_options
        with open(self.game_path+"/dat.trsl", "r") as g:
            game_options = game_options | json.load(g)
            for item in self.weapon_rows:
                try:
                    if item in data:
                        self.weapon_rows[item].options[data[item]].setChecked(True)
                        self.weapon_rows[item].dL.setPixmap(QPixmap("src/ui_icons/on.png"))
                except:
                    pass
    
    def toggleOption(self):
        global game_options
        self.sender().row.dL.setPixmap(QPixmap("src/ui_icons/on.png"))
        for o in self.sender().row.options:
            if self.sender().row.options[o] != self.sender():
                self.sender().row.options[o].setChecked(False)
            if self.sender().row.options[o].text() == self.sender().name:
                self.sender().setChecked(True)
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
                if os.path.exists(g.path):
                    self.sender().setText(g.path)
                    game_options[self.sender().row_name] = g.path
                    self.game_path = g.path
                    self.parent.backButton.setEnabled(True)
                else:
                    g = infoClose(info = "Invalid path", parent = self)
                    g.exec_()
                
        #set game name        
        elif self.sender().row_name == "What is your game called?":
            h = textEntryDialog(self)
            h.exec_()
            if h.data != None and h.data != "":
                self.sender().setText(h.data)
                game_options[self.sender().row_name] = h.data
                self.game_name = h.data
                g = gameDirectory(self)
                g.nameSrl()
        
        #show item forging specifics
        elif self.sender().row_name == "Is item forging enabled?":
            game_options[self.sender().row_name] = self.sender().text()
            if self.sender().text() == "Yes":
                self.weapon_rows["What does item forging do?"].setVisible(True)
            else:
                self.weapon_rows["What does item forging do?"].setVisible(False)
        
        #show children paralogues
        elif self.sender().row_name == "Can S level supports produce children?":
            game_options[self.sender().row_name] = self.sender().text()
            if self.sender().text() == "Yes":
                self.weapon_rows["Do children units have paralogues?"].setVisible(True)
                self.parent.unit_editor.bio.setVisible(True)
            else:
                self.weapon_rows["Do children units have paralogues?"].setVisible(False)
                self.parent.unit_editor.bio.setVisible(False)
        
        #show encumbrance options
        elif self.sender().row_name == "Do units have encumbrance (weapon weight affecting movement/speed)?":
            game_options[self.sender().row_name] = self.sender().text()
            if self.sender().text() == "Yes":
                self.weapon_rows["Does encumbrance affect movement or speed?"].setVisible(True)
            else:
                self.weapon_rows["Does encumbrance affect movement or speed?"].setVisible(False)
        
        #weapons triangle
        elif self.sender().row_name == "Use weapon triangle?":
            game_options[self.sender().row_name] = self.sender().text()
            g = weaponTriangle(self)
            g.exec_()
        
        #credits
        elif self.sender().row_name == "What should the end credits say?":
            game_options[self.sender().row_name] = self.sender().text()
            g = creditsDialog(self)
            g.exec_()
            
        #game art
        elif self.sender().row_name == "Supply your own cover art or have one auto-generated?":
            if self.sender().text() == "Supply my own":
                game_options[self.sender().row_name] = self.sender().text()
                g = uploadGameArtDialog(self)
                g.exec_()
            else:
                gameArtGenerate(self) #Doesn't do anything (yet)
        
        #magic weapon experience handling
        elif self.sender().row_name == "Are magic weapon experience types combined or separate?":
            if self.sender().text() == "Combined":
                game_options[self.sender().row_name] = self.sender().text()
                s = magicExperienceDialog(self)
                s.exec_()
        
        #change map/hub options/visiblity based on choice( this is a big one)
        elif self.sender().row_name == "Does game have hub, map, or both?":
            game_options[self.sender().row_name] = self.sender().text()
            if self.sender().text() == "Hub":
                self.weapon_rows["Can player shop in the hub?"].setVisible(True)
                self.weapon_rows["Does player have 'free time'?"].setVisible(True)
                
                self.weapon_rows["Can player use items on map?"].setVisible(False)
                self.weapon_rows["Do completed levels become shops?"].setVisible(False)
                self.weapon_rows["Are there travelling merchants?"].setVisible(False)
                
            elif self.sender().text() == "Map":
                self.weapon_rows["Can player shop in the hub?"].setVisible(False)
                self.weapon_rows["Does player have 'free time'?"].setVisible(False)
                
                self.weapon_rows["Can player use items on map?"].setVisible(True)
                self.weapon_rows["Do completed levels become shops?"].setVisible(True)
                self.weapon_rows["Are there travelling merchants?"].setVisible(True)
                
            else: #both
                self.weapon_rows["Does player choose missions from the hub or the map?"].setVisible(True)
                self.weapon_rows["Does player have 'free time'?"].setVisible(False)
                self.weapon_rows["Is hub accessed from map menu, or is map accessed from hub?"].setVisible(True)
                self.weapon_rows["Can player use items on map?"].setVisible(True)
                self.weapon_rows["Do completed levels become shops?"].setVisible(True)
                self.weapon_rows["Are there travelling merchants?"].setVisible(True)
                self.weapon_rows["Can player shop in the hub?"].setVisible(True)
                self.weapon_rows["Does player have 'free time'?"].setVisible(True)
        try:
            with open(self.game_path+"/dat.trsl", "w") as g:
                json.dump(game_options, g)
        except Exception as e:
            print(e)
    
    def checkErrors(self):
        c = checkDialog(self)
        c.exec_()
        
    def help_text(self):
        img = self.sender().h[0]
        info = self.sender().h[1]
        row_styles = self.sender().h[2]
        o = stackedInfoImgDialog(img, info, row_styles, parent=self)