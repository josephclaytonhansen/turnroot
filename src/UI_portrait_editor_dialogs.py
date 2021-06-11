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
        
        self.counts = {"hair":0, "scars":0, "freckles":0, "jewelry":0, "masks":0, "tattoos":0, "facial hair":0, "makeup":0, "tops":0, "headwear":0, "armor":0}
        self.max_counts = {"hair":3, "scars":6, "freckles":4, "jewelry":6, "masks":2, "tattoos":5, "facial hair":3,"makeup":3, "tops":3, "headwear":4, "armor":3}
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
        base = "base"
        
        self.parent.active_layers["base"] = base
        
        self.total_layers = len(self.parent.active_layers)
        self.parent.layer_orders[self.total_layers] = base
        
        self.parent.layers_box.clear()
        self.parent.layers_box.addItems(self.parent.active_layers)
    
    def initHair(self):
        self.counts["hair"] += 1
        if self.counts["hair"] <= self.max_counts["hair"]:
        
            ###REPLACE THIS###
            hair = "hair " + str(self.counts["hair"])
            
            self.parent.active_layers["hair " + str(self.counts["hair"])] = hair
            
            self.total_layers = len(self.parent.active_layers)
            self.parent.layer_orders[self.total_layers] = hair
            
            self.parent.layers_box.clear()
            self.parent.layers_box.addItems(self.parent.active_layers)
    
    def initEyes(self):
        ###REPLACE THIS###
        eyes = "eyes"
        
        self.parent.active_layers["eyes"] = eyes
        
        self.total_layers = len(self.parent.active_layers)
        self.parent.layer_orders[self.total_layers] = eyes
        
        self.parent.layers_box.clear()
        self.parent.layers_box.addItems(self.parent.active_layers)
    
    def initNose(self):
        ###REPLACE THIS###
        nose = "nose"
        
        self.parent.active_layers["nose"] = nose
        
        self.total_layers = len(self.parent.active_layers)
        self.parent.layer_orders[self.total_layers] = nose
        
        self.parent.layers_box.clear()
        self.parent.layers_box.addItems(self.parent.active_layers)
    
    def initMouth(self):
        ###REPLACE THIS###
        mouth = "mouth"
        
        self.parent.active_layers["mouth"] = mouth
        
        self.total_layers = len(self.parent.active_layers)
        self.parent.layer_orders[self.total_layers] = mouth
        
        self.parent.layers_box.clear()
        self.parent.layers_box.addItems(self.parent.active_layers)
    
    def initScars(self):
        self.counts["scars"] += 1
        if self.counts["scars"] <= self.max_counts["scars"]:
        
            ###REPLACE THIS###
            scar = "scar " + str(self.counts["scars"])
            
            self.parent.active_layers["scar " + str(self.counts["scars"])] = scar
            
            self.total_layers = len(self.parent.active_layers)
            self.parent.layer_orders[self.total_layers] = scar
            
            self.parent.layers_box.clear()
            self.parent.layers_box.addItems(self.parent.active_layers)
    
    def initFreckles(self):
        self.counts["freckles"] += 1
        if self.counts["freckles"] <= self.max_counts["freckles"]:
        
            ###REPLACE THIS###
            freckle = "freckle " + str(self.counts["freckles"])
            
            self.parent.active_layers["freckle " + str(self.counts["freckles"])] = freckle
            
            self.total_layers = len(self.parent.active_layers)
            self.parent.layer_orders[self.total_layers] = freckle
            
            self.parent.layers_box.clear()
            self.parent.layers_box.addItems(self.parent.active_layers)
    
    def initJewelry(self):
        self.counts["jewelry"] += 1
        if self.counts["jewelry"] <= self.max_counts["jewelry"]:
        
            ###REPLACE THIS###
            jewelry = "jewelry " + str(self.counts["jewelry"])
            
            self.parent.active_layers["jewelry " + str(self.counts["jewelry"])] = jewelry
            
            self.total_layers = len(self.parent.active_layers)
            self.parent.layer_orders[self.total_layers] = jewelry
            
            self.parent.layers_box.clear()
            self.parent.layers_box.addItems(self.parent.active_layers)
    
    def initMasks(self):
        self.counts["masks"] += 1
        if self.counts["masks"] <= self.max_counts["masks"]:
        
            ###REPLACE THIS###
            mask = "mask " + str(self.counts["masks"])
            
            self.parent.active_layers["mask " + str(self.counts["masks"])] = mask
            
            self.total_layers = len(self.parent.active_layers)
            self.parent.layer_orders[self.total_layers] = mask
            
            self.parent.layers_box.clear()
            self.parent.layers_box.addItems(self.parent.active_layers)
    
    def initTattoos(self):
        self.counts["tattoos"] += 1
        if self.counts["tattoos"] <= self.max_counts["tattoos"]:
        
            ###REPLACE THIS###
            tattoo = "tattoo " + str(self.counts["tattoos"])
            
            self.parent.active_layers["tattoo " + str(self.counts["tattoos"])] = tattoo
            
            self.total_layers = len(self.parent.active_layers)
            self.parent.layer_orders[self.total_layers] = tattoo
            
            self.parent.layers_box.clear()
            self.parent.layers_box.addItems(self.parent.active_layers)
    
    def initFacialHair(self):
        self.counts["facial hair"] += 1
        if self.counts["facial hair"] <= self.max_counts["facial hair"]:
        
            ###REPLACE THIS###
            facial_hair = "facial hair " + str(self.counts["facial hair"])
            
            self.parent.active_layers["facial hair " + str(self.counts["facial hair"])] = facial_hair
            
            self.total_layers = len(self.parent.active_layers)
            self.parent.layer_orders[self.total_layers] = facial_hair
            
            self.parent.layers_box.clear()
            self.parent.layers_box.addItems(self.parent.active_layers)
    
    def initEyebrows(self):
        ###REPLACE THIS###
        eyebrows = "eyebrows"
        
        self.parent.active_layers["eyebrows"] = eyebrows
        
        self.total_layers = len(self.parent.active_layers)
        self.parent.layer_orders[self.total_layers] = eyebrows
        
        self.parent.layers_box.clear()
        self.parent.layers_box.addItems(self.parent.active_layers)
    
    def initMakeup(self):
        self.counts["makeup"] += 1
        if self.counts["makeup"] <= self.max_counts["makeup"]:
        
            ###REPLACE THIS###
            makeup = "makeup " + str(self.counts["makeup"])
            
            self.parent.active_layers["makeup " + str(self.counts["makeup"])] = makeup
            
            self.total_layers = len(self.parent.active_layers)
            self.parent.layer_orders[self.total_layers] = makeup
            
            self.parent.layers_box.clear()
            self.parent.layers_box.addItems(self.parent.active_layers)
    
    def initHeadwear(self):
        self.counts["headwear"] += 1
        if self.counts["headwear"] <= self.max_counts["headwear"]:
        
            ###REPLACE THIS###
            headwear = "headwear " + str(self.counts["headwear"])
            
            self.parent.active_layers["headwear " + str(self.counts["headwear"])] = headwear
            
            self.total_layers = len(self.parent.active_layers)
            self.parent.layer_orders[self.total_layers] = headwear
            
            self.parent.layers_box.clear()
            self.parent.layers_box.addItems(self.parent.active_layers)
    
    def initTops(self):
        self.counts["tops"] += 1
        if self.counts["tops"] <= self.max_counts["tops"]:
        
            ###REPLACE THIS###
            tops = "tops " + str(self.counts["tops"])
            
            self.parent.active_layers["tops " + str(self.counts["tops"])] = tops
            
            self.total_layers = len(self.parent.active_layers)
            self.parent.layer_orders[self.total_layers] = tops
            
            self.parent.layers_box.clear()
            self.parent.layers_box.addItems(self.parent.active_layers)
    
    def initArmor(self):
        self.counts["armor"] += 1
        if self.counts["armor"] <= self.max_counts["armor"]:
        
            ###REPLACE THIS###
            armor = "armor " + str(self.counts["armor"])
            
            self.parent.active_layers["armor " + str(self.counts["armor"])] = armor
            
            self.total_layers = len(self.parent.active_layers)
            self.parent.layer_orders[self.total_layers] = armor
            
            self.parent.layers_box.clear()
            self.parent.layers_box.addItems(self.parent.active_layers)
