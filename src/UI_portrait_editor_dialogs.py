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
        
        self.counts = {"hair":0}
        self.max_counts = {"hair":3}
        self.total_layers = 0
    
    def initContent(self, s):
        if s == "Base":
            self.initBase()
        elif s == "Hair":
            self.initHair()
        elif s == "Eyes":
            self.initEyes()
        elif s== "Nose":
            self.initNose()
        elif s == "Mouth":
            self.initMouth()
        elif s == "Scars":
            self.initScars()
        elif s == "Freckles":
            self.initFreckles()
        elif s == "Jewelry":
            self.initJewelry()
        elif s == "Masks":
            self.initMasks()
        elif s == "Tattoos":
            self.initTattoos()
        elif s == "Facial Hair":
            self.initFacialHair()
        elif s == "Eyebrows":
            self.initEyebrows()
        elif s == "Makeup":
            self.initMakeup()
        elif s == "Headwear":
            self.initHeadwear()
        elif s == "Tops":
            self.initTops()
        elif s == "Armor":
            self.initArmor()
    
    def initBase(self):
        ###REPLACE THIS###
        base = "temp base"
        
        self.parent.active_layers["base"] = base
        
        self.total_layers = len(self.parent.active_layers)
        self.parent.layer_orders[self.total_layers] = base
        
        print(self.parent.layer_orders, self.parent.active_layers)
        
        self.parent.layers_box.clear()
        self.parent.layers_box.addItems(self.parent.active_layers)
    
    def initHair(self):
        self.counts["hair"] += 1
        if self.counts["hair"] <= self.max_counts["hair"]:
        
            ###REPLACE THIS###
            hair = "temp hair " + str(self.counts["hair"])
            
            self.parent.active_layers["hair " + str(self.counts["hair"])] = hair
            
            self.total_layers = len(self.parent.active_layers)
            self.parent.layer_orders[self.total_layers] = hair
            
            print(self.parent.layer_orders, self.parent.active_layers)
            
            self.parent.layers_box.clear()
            self.parent.layers_box.addItems(self.parent.active_layers)
            
            
    
    def initEyes(self):
        pass
    
    def initNose(self):
        pass
    
    def initMouth(self):
        pass
    
    def initScars(self):
        pass
    
    def initFreckles(self):
        pass
    
    def initJewelry(self):
        pass
    
    def initMasks(self):
        pass
    
    def initTattoos(self):
        pass
    
    def initFacialHair(self):
        pass
    
    def initEyebrows(self):
        pass
    
    def initMakeup(self):
        pass
    
    def initHeadwear(self):
        pass
    
    def initTops(self):
        pass
    
    def initArmor(self):
        pass
