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
        
        self.counts = {"hair":0, "scars":0, "freckles":0, "jewelry":0}
        self.max_counts = {"hair":3, "scars":6, "freckles":4, "jewelry":6}
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
            
            self.parent.layers_box.clear()
            self.parent.layers_box.addItems(self.parent.active_layers)
    
    def initEyes(self):
        ###REPLACE THIS###
        eyes = "temp eyes"
        
        self.parent.active_layers["eyes"] = eyes
        
        self.total_layers = len(self.parent.active_layers)
        self.parent.layer_orders[self.total_layers] = eyes
        
        self.parent.layers_box.clear()
        self.parent.layers_box.addItems(self.parent.active_layers)
    
    def initNose(self):
        ###REPLACE THIS###
        nose = "temp nose"
        
        self.parent.active_layers["nose"] = nose
        
        self.total_layers = len(self.parent.active_layers)
        self.parent.layer_orders[self.total_layers] = nose
        
        self.parent.layers_box.clear()
        self.parent.layers_box.addItems(self.parent.active_layers)
    
    def initMouth(self):
        ###REPLACE THIS###
        mouth = "temp mouth"
        
        self.parent.active_layers["mouth"] = mouth
        
        self.total_layers = len(self.parent.active_layers)
        self.parent.layer_orders[self.total_layers] = mouth
        
        self.parent.layers_box.clear()
        self.parent.layers_box.addItems(self.parent.active_layers)
    
    def initScars(self):
        self.counts["scars"] += 1
        if self.counts["scars"] <= self.max_counts["scars"]:
        
            ###REPLACE THIS###
            scar = "temp scar " + str(self.counts["scars"])
            
            self.parent.active_layers["scar " + str(self.counts["scars"])] = scar
            
            self.total_layers = len(self.parent.active_layers)
            self.parent.layer_orders[self.total_layers] = scar
            
            self.parent.layers_box.clear()
            self.parent.layers_box.addItems(self.parent.active_layers)
    
    def initFreckles(self):
        self.counts["freckles"] += 1
        if self.counts["freckles"] <= self.max_counts["freckles"]:
        
            ###REPLACE THIS###
            freckle = "temp freckle " + str(self.counts["freckles"])
            
            self.parent.active_layers["freckle " + str(self.counts["freckles"])] = freckle
            
            self.total_layers = len(self.parent.active_layers)
            self.parent.layer_orders[self.total_layers] = freckle
            
            self.parent.layers_box.clear()
            self.parent.layers_box.addItems(self.parent.active_layers)
    
    def initJewelry(self):
        self.counts["jewelry"] += 1
        if self.counts["jewelry"] <= self.max_counts["jewelry"]:
        
            ###REPLACE THIS###
            jewelry = "temp jewelry " + str(self.counts["jewelry"])
            
            self.parent.active_layers["jewelry " + str(self.counts["jewelry"])] = jewelry
            
            self.total_layers = len(self.parent.active_layers)
            self.parent.layer_orders[self.total_layers] = jewelry
            
            self.parent.layers_box.clear()
            self.parent.layers_box.addItems(self.parent.active_layers)
    
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
