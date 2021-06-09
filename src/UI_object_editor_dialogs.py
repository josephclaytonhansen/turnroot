from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QPalette, QIcon, QPixmap, QCursor, QFont
from src.UI_updateJSON import updateJSON
import src.UI_colorTheme
import shutil, os, pickle, json, sys, random
from src.UI_Dialogs import confirmAction, popupInfo, numberEntryDialog
from src.node_backend import getFiles, GET_FILES
from src.img_overlay import overlayTile
from src.skeletons.unit_class import unitClass
from src.skeletons.unit import Unit
from src.skeletons.weapon_types import weaponTypes, expTypes
from src.skeletons.Object import (Object,usableItem,Key,healItem,statIncreaseItem,expIncreaseItem,
                                  classChangeItem,summoningItem,levelEffectItem,equippableItem,Weapon,Shield)
from src.UI_object_editor_more_dialogs import chooseUnitStatDialog

class combatDialog(QDialog):
    def __init__(self, parent=None,font=None):
        data = updateJSON()
        self.parent = parent
        self.restart = False
        self.body_font = font
        self.h_font = QFont(self.body_font)
        self.h_font.setPointSize(20)
        self.active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        active_theme = self.active_theme
        super().__init__(parent)
        
        self.setStyleSheet("background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.layout = QGridLayout()
        self.layout.setContentsMargins(12,12,12,12)
        self.setLayout(self.layout)
        
        self.values = {}
        
        q = QLabel("Combat Statistics")
        q.setFont(self.h_font)
        self.layout.addWidget(q, 0, 0, 1,1)
        
        self.help = QPushButton()
        self.help.clicked.connect(self.combatInfo)
        self.help.setIcon(QIcon(QPixmap("src/ui_icons/white/question-mark-4-32.png")))
        self.help.setIconSize(QSize(36,36))
        self.help.setMaximumWidth(36)
        self.layout.addWidget(self.help, 0, 1, 1,1)
        
        r = 0
        s = ["durability", "avoidance", "attack speed"]
        for x in ["might", "hit", "crit", "weight", "full_durability", "avo", "asm"]:
            r +=1
            if r <= 4:
                stat_label = QLabel(x)
            else:
                stat_label = QLabel(s[r-5])
            stat_label.setFont(self.body_font)
            
            stat_value = QSpinBox()
            stat_value.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
            stat_value.name = x
            stat_value.setFont(self.body_font)
            self.values[x] = stat_value
            if stat_value.name != "avo" and stat_value.name != "asm":
                stat_value.setRange(0,100)
            else:
                stat_value.setRange(-50,50)

            try:
                stat_value.setValue(getattr(self.parent.weapon, x))
            except:
                pass

            stat_value.valueChanged.connect(self.change_value)
                
            self.layout.addWidget(stat_label, r, 0, 1, 1)
            self.layout.addWidget(stat_value, r,1,1,1)
            
        range_row = QWidget()
        range_row_layout = QHBoxLayout()
        range_row.setLayout(range_row_layout)
        
        ranges = getattr(self.parent.weapon, "range")
        self.new_ranges = [1,1]
        self.range_spinners = {}
        
        lrange = QSpinBox()
        self.range_spinners[0] = lrange
        lrange.valueChanged.connect(self.change_range)
        lrange.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
        lrange.name = 0
        lrange.setFont(self.body_font)
        self.values[x] = lrange
        lrange.setRange(1,5)
        try:
            lrange.setValue(ranges[0])
        except:
            pass
        lrange_label = QLabel("Range (Lower Limit)")
        lrange_label.setFont(self.body_font)
        range_row_layout.addWidget(lrange_label)
        range_row_layout.addWidget(lrange)
        
        frange = QSpinBox()
        self.range_spinners[1] = frange
        frange.valueChanged.connect(self.change_range)
        frange.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
        frange.name = 1
        frange.setFont(self.body_font)
        self.values[x] = lrange
        frange.setRange(1,5)
        try:
            frange.setValue(ranges[1])
        except:
            pass
        frange_label = QLabel("Range (Upper Limit)")
        frange_label.setFont(self.body_font)
        range_row_layout.addWidget(frange_label)
        range_row_layout.addWidget(frange)
        
        damage_type = QComboBox()
        damage_type.currentTextChanged.connect(self.change_damage_type)
        damage_type_label = QLabel("Damage Type")
        damage_type.addItems(["Physical", "Magical"])
        damage_type.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
        damage_type.setFont(self.body_font)
        damage_type_label.setFont(self.body_font)
        
        min_level = QComboBox()
        min_level.currentTextChanged.connect(self.change_min_level)
        min_level_label = QLabel("Minimum Usable Level")
        min_level.addItems(["--Select--", "E", "D", "C", "B","A", "S"])
        min_level.setCurrentText(self.parent.weapon.minimum_experience_level)

        min_level.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
        min_level.setFont(self.body_font)
        min_level_label.setFont(self.body_font)
        
        self.layout.addWidget(damage_type_label, r+1,0,1,1)
        self.layout.addWidget(damage_type,r+1,1,1,1)
        self.layout.addWidget(min_level_label, r+2,0,1,1)
        self.layout.addWidget(min_level,r+2,1,1,1)
        
        self.layout.addWidget(range_row, r+3,0,1,2)
            
    def change_value(self):
        setattr(self.parent.weapon, self.sender().name, self.sender().value()) 
        if self.parent.weapon.path != None:
            self.parent.weapon.selfToJSON()
    
    def change_damage_type(self):
        self.parent.weapon.damage_type = self.sender().currentText()
        if self.parent.weapon.path != None:
            self.parent.weapon.selfToJSON()
    
    def change_min_level(self):
        if self.sender().currentText() != "--Select--":
            self.parent.weapon.minimum_experience_level = self.sender().currentText()
            if self.parent.weapon.path != None:
                self.parent.weapon.selfToJSON()
            
    def combatInfo(self):
        g = popupInfo("<b><br>How do I create a weapon that recovers health, inflicts a status, or has some other ability?</b><br>"+
                      "Once you've set the stats here, close this pop-up and click 'Abilities'.<br>"+
                      "<br><b>How do I create magic that can warp, heals based on unit Mag stat, or other cases where these stats aren't applicable?</b><br>"+
                      "'Weapons' of this nature are classified as Actions, and can be set up through the Actions tab in the Unit Editor.<br>"+
                      "<br><b>Why can't I change the 'Lower Limit' of the weapon range?</b><br>"+
                      "The lower limit must be the same or less than the upper limit, so if the upper limit is 1, the lower limit must be 1."
                      ,self,self.body_font)
    
    def change_range(self):
        self.new_ranges[self.sender().name] = self.sender().value()
        if self.new_ranges[0] > self.new_ranges[1]:
            self.new_ranges[0] = self.new_ranges[1]
            self.range_spinners[0].setValue(self.new_ranges[0])
        setattr(self.parent.weapon, "range", self.new_ranges)
        if self.parent.weapon.path != None:
            self.parent.weapon.selfToJSON()

class loadSavedWeapon(QDialog):
    def __init__(self, parent=None,font=None):
        data = updateJSON()
        self.parent = parent
        self.restart = False
        self.active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        super().__init__(parent)
        self.body_font = font
        self.h_font = QFont(self.body_font)
        self.h_font.setPointSize(20)
        
        self.setStyleSheet("background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(12,12,12,12)
        self.setLayout(self.layout)
        
        label = QLabel("Choose Weapon")
        label.setFont(self.h_font)
        self.layout.addWidget(label)
        
        self.search = QLineEdit()
        self.search.setFont(self.body_font)
        self.search.setStyleSheet("background-color: "+self.active_theme.list_background_color+";color: "+self.active_theme.window_text_color)
        self.search.setPlaceholderText("Search")
        self.layout.addWidget(self.search)
        self.search.textChanged.connect(self.filterList)
        self.class_list = QListWidget()
        self.class_list.setStyleSheet("background-color: "+self.active_theme.list_background_color+";color: "+self.active_theme.window_text_color)
        self.class_list.setFont(self.body_font)
        self.layout.addWidget(self.class_list)
        self.class_list.itemClicked.connect(self.change)
        self.getWeaponsInFolder()
        self.show()
        
    def getWeaponsInFolder(self):
        file_list = getFiles("src/skeletons/weapons")[GET_FILES]
        class_names = []
        global classes
        classes = {}
        self.paths = {}
        for f in file_list:
            f.fullPath = f.fullPath.replace("\\", "/")
            if f.ext.strip() == ".trwof":
                tmp_class = Weapon()
                tmp_class.selfFromJSON(f.fullPath)
                name = getattr(tmp_class, "name")
                self.paths[name] = f.fullPath
                if name not in class_names:
                    class_names.append(name)
                    classes[name] = tmp_class
            self.classesToDropDown(class_names)
                
    def classesToDropDown(self, class_names):
        self.class_list.clear()
        self.class_list.addItems(class_names)
        self.class_list.update()
        self.full_list = []
        for x in range(self.class_list.count()):
            self.full_list.append(self.class_list.item(x).text())
    
    def change(self,s):
        self.returns = self.paths[self.sender().currentItem().text()]
        self.close()
    
    def filterList(self):
        try:
            self.class_list.clear()
            self.class_list.addItems(self.full_list)
            if len(self.sender().text()) > 0:
                tmp_list = []
                for x in self.class_list.findItems(self.sender().text(), Qt.MatchContains):
                    tmp_list.append(x.text())
                self.class_list.clear()
                self.class_list.addItems(tmp_list)
        except:
            pass
    
class pricingDialog(QDialog):
    def __init__(self, parent=None,font=None):
        data = updateJSON()
        self.parent = parent
        self.restart = False
        self.body_font = font
        self.h_font = QFont(self.body_font)
        self.h_font.setPointSize(20)
        self.active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        active_theme = self.active_theme
        super().__init__(parent)
        
        self.setStyleSheet("background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.layout = QGridLayout()
        self.layout.setContentsMargins(12,12,12,12)
        self.setLayout(self.layout)
        
        price_sold = QSpinBox()
        price_buy = QSpinBox()
        buyable = QSpinBox()
        cost_per_durability = QSpinBox()
        self.spinners = [price_sold,price_buy,buyable,cost_per_durability]
        self.att = ["price_if_sold","price","sell_cost_per","buyable_quantity"]
        labels = ["Price if Sold (Unused)", "Price to Buy", "Sell Price Deducted Per Use", "Maximum Buyable at a Time*"]
        r = 0
        for x in self.spinners:
            r+=1
            x.setFont(self.body_font)
            x.setRange(0,10000)
            x.name = self.att[self.spinners.index(x)]
            try:
                x.setValue(getattr(self.parent.weapon, self.att[self.spinners.index(x)]))
            except:
                pass
            x.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
            x.valueChanged.connect(self.change_value)
            self.layout.addWidget(x, r, 1, 1, 1)
            label = QLabel(labels[r-1])
            label.setFont(self.body_font)
            self.layout.addWidget(label,r,0,1,1)
        
        self.layout.addWidget(QLabel("*Set to 0 for no maximum"), r+1,0,1,2)
        
        self.rate_slider = QSlider(Qt.Horizontal)
        self.rate_slider.name = 1
        self.rate_slider.valueChanged.connect(self.colorizeSlider)

        self.rate_slider.setValue(int(self.parent.weapon.full_durability/2))
        self.rate_slider.setRange(0,self.parent.weapon.full_durability)
        self.rate_slider.setSingleStep(1)
        
        self.layout.addWidget(self.rate_slider,r+4,0,1,2)
        
        h = QLabel("Used, this weapon would sell for...")
        h.setFont(self.h_font)
        self.layout.addWidget(h,r+2,0,1,2)
        t = QLabel("Change used amount")
        t.setToolTip("Durability must be greater than 0. Set with the Combat button")
        t.setFont(self.body_font)
        self.layout.addWidget(t,r+3,0,1,2)
        
        self.used_uses = QLabel("Remaining Uses: ")
        self.used_uses.setFont(self.body_font)
        self.cost = QLabel(" Price: ")
        self.cost.setFont(self.body_font)
        self.layout.addWidget(self.used_uses, r+5, 0, 1,1)
        self.layout.addWidget(self.cost,r+5,1,1,1)
        
    def change_value(self):
        self.cost.setText(" Price: ")
        setattr(self.parent.weapon, self.sender().name, self.sender().value()) 
        if self.parent.weapon.path != None:
            self.parent.weapon.selfToJSON()
    
    def colorizeSlider(self, v):
        try:
            self.cost_at_use = self.parent.weapon.price_if_sold - ((self.parent.weapon.full_durability - v) * self.parent.weapon.sell_cost_per)
            self.used_uses.setText("Remaining Uses: "+str(v))
            self.cost.setText(" Price: "+str(self.cost_at_use))
        except:
            pass
            
        v = v / self.parent.weapon.full_durability
        color_left = QColor(self.active_theme.unit_editor_slider_color_0)
        color_right = QColor(self.active_theme.unit_editor_slider_color_1)
        color_left_c = [color_left.red(), color_left.green(), color_left.blue()]
        color_right_c = [color_right.red(), color_right.green(), color_right.blue()]
        
        distances = [(color_right.red() - color_left.red()),
                     (color_right.green() - color_left.green()),
                     (color_right.blue() - color_left.blue())]
        
        
        new_color = [int(color_left.red() + v * distances[0]),
                     int(color_left.green() + v * distances[1]),
                     int(color_left.blue()+ v * distances[2])]
        
        self.sender().setStyleSheet(
            "QSlider::handle:horizontal {\nbackground-color: "+str(QColor(new_color[0],new_color[1],new_color[2]).name())+";border-radius: 2px;width:40px;height:40px;}"
            )
        
class abilitiesDialog(QDialog):
    def __init__(self, parent=None,font=None):
        data = updateJSON()
        self.parent = parent
        self.restart = False
        self.body_font = font
        self.h_font = QFont(self.body_font)
        self.h_font.setPointSize(20)
        self.active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        active_theme = self.active_theme
        super().__init__(parent)
        
        try:
            with open("src/tmp/universal_weapon_abilities.json", "r") as f:
                self.abilities = json.load(f)
        except:
            with open("src/tmp/uwad.tdndf", "r") as f:
                self.abilities = json.load(f)
        
        self.setStyleSheet("background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.layout = QGridLayout()
        self.layout.setContentsMargins(12,12,12,12)
        self.setLayout(self.layout)
        
        h = QLabel("This weapon...")
        h.setFont(self.h_font)
        self.layout.addWidget(h,0,0,1,6)
        
        r = 0
        self.entries1 = {}
        self.entries2 = {}
        self.ability_checks = {}
        
        for x in self.abilities:
            r+=1
            ability_split = x.split("&")
            ability_check = QCheckBox()
            ability_check.row = r
            ability_check.stateChanged.connect(self.toggle_ability)
            self.layout.addWidget(ability_check, r, 0, 1, 1)
            ability_check.name = x
            self.ability_checks[x] = ability_check
            ability_len = len(ability_split)
            
            if ability_len == 1:
                label = QLabel(x)
                label.setFont(self.body_font)
                self.layout.addWidget(label,r,1,1,6)
                
            elif ability_len == 2:
                label = QLabel(ability_split[0])
                label.setFont(self.body_font)
                self.layout.addWidget(label,r,1,1,4)
                
                midentry = QPushButton()
                midentry.row = r
                midentry.setIcon(QIcon(QPixmap("src/ui_icons/white/edit.png")))
                midentry.name = x
                midentry.clicked.connect(self.edit_mid)
                
                entry1 = QComboBox()
                self.entries1[r] = entry1
                entry1.addItems(["Number", "Unit Stat"])
                label2 = QLabel(ability_split[1])
                label2.setFont(self.body_font)
                
                self.layout.addWidget(entry1,r,4,1,1)
                self.layout.addWidget(midentry,r,5,1,1)
                self.layout.addWidget(label2,r,6,1,1)
                
                for g in [midentry, entry1]:
                    g.setStyleSheet("background-color: "+self.active_theme.list_background_color+";color: "+self.active_theme.window_text_color)
                
            elif ability_len == 3:
                label1 = QLabel(ability_split[0])
                midentry = QPushButton()
                midentry.row = r
                midentry.setIcon(QIcon(QPixmap("src/ui_icons/white/edit.png")))
                midentry.name = x
                midentry.clicked.connect(self.edit_mid)
                
                if x.startswith("Inflicts"):
                    entry1 = QComboBox()
                    self.entries1[r] = entry1
                    entry1.addItems(["Poisoned", "On Fire", "Frozen", "Shocked"])
                    midentry.setIcon(QIcon(QPixmap("src/ui_icons/white/question-mark-4-32.png")))
                    midentry.name = x
                    midentry.clicked.disconnect()
                    midentry.clicked.connect(self.define_status)
                elif x.startswith("Foe"):
                    entry1 = QComboBox()
                    self.entries1[r] = entry1
                    entry1.addItems(["Unit Stat"])
                else:
                    entry1 = QComboBox()
                    self.entries1[r] = entry1
                    entry1.addItems(["Number", "Unit Stat"])
                
                label2 = QLabel(ability_split[1])
                entry2 = QSpinBox()
                self.entries2[r] = entry2
                label3 = QLabel(ability_split[2])
                
                for y in [label1,entry1,label2,entry2,label3,midentry]:
                    y.setFont(self.body_font)
                
                for g in [midentry, entry1, entry2]:
                    g.setStyleSheet("background-color: "+self.active_theme.list_background_color+";color: "+self.active_theme.window_text_color)
                    
                self.layout.addWidget(label1, r,1,1,1)
                self.layout.addWidget(entry1, r,2,1,1)
                self.layout.addWidget(midentry,r,3,1,1)
                self.layout.addWidget(label2, r,4,1,1)
                self.layout.addWidget(entry2, r,5,1,1)
                self.layout.addWidget(label3, r,6,1,1)
                
        self.current_abilities = QTextEdit()
        self.current_abilities.setMaximumHeight(140)
        self.tfont = QFont('Monaco', 14, QFont.Light)
        self.tfont.setKerning(False)
        self.tfont.setFixedPitch(True)
        self.current_abilities.setFont(self.tfont)
        self.current_abilities.setStyleSheet("background-color: "+self.active_theme.list_background_color+";color: "+self.active_theme.window_text_color)
        try:
            self.current_abilities.setPlainText(str(self.parent.weapon.special_abilities))
        except:
            pass
        self.layout.addWidget(self.current_abilities, r+1,0,1,6)
        
        self.clear_all  = QPushButton("Reset")
        self.clear_all.setMinimumHeight(40)
        self.clear_all.setStyleSheet("background-color: "+self.active_theme.list_background_color+";color: "+self.active_theme.window_text_color)
        self.clear_all.setFont(self.body_font)
        self.clear_all.clicked.connect(self.reset)
        self.layout.addWidget(self.clear_all,r+1,6,1,1)
        
        self.ins = QLabel("This shows the current abilities on the weapon. If no weapon is loaded, this will be  blank. Click 'Reset' to clear abilities")
        self.ins.setFont(self.body_font)
        self.layout.addWidget(self.ins,r+2,0,1,7)
            
    def edit_mid(self):
        if self.entries1[self.sender().row].currentText() == "Unit Stat":
            g = chooseUnitStatDialog(parent=self,font=self.body_font)
            g.exec_()
            self.entries1[self.sender().row].clear()
            if self.sender().row != 12:
                self.entries1[self.sender().row].addItem("Number")
            self.entries1[self.sender().row].addItem("Unit Stat")
            self.entries1[self.sender().row].addItem(g.data)
            self.entries1[self.sender().row].setCurrentText(g.data)
        else:
            g = numberEntryDialog(parent=self,font=self.body_font)
            g.exec_()
            self.entries1[self.sender().row].clear()
            if self.sender().row != 12:
                self.entries1[self.sender().row].addItem("Number")
            self.entries1[self.sender().row].addItem("Unit Stat")
            self.entries1[self.sender().row].addItem(g.data)
            self.entries1[self.sender().row].setCurrentText(g.data)
        string = self.sender().name.split("&")
        try:
            string = string[0] + self.entries1[self.sender().row].currentText() + string[1] + str(self.entries2[self.sender().row].value()) + string[2]
        except:
            string = string[0] + self.entries1[self.sender().row].currentText() + string[1]
        
    def define_status(self):
        g = popupInfo("\nA poisoned unit takes damage every turn until they take an antidote or it wears off\n"+
"\nAn on fire unit takes damage every turn unless in water\n"+
"\nA frozen enemy has movement / 2 for the next turn(s)\n"+
"\nA shocked unit has a 25% chance to ignore AI and move somewhere random for the next turn(s)\n"
                      ,self,self.body_font)
        g.exec_()
    
    def toggle_ability(self):
        if self.sender().row <= 2:
            if self.entries1[self.sender().row].currentText() == "Unit Stat":
                g = chooseUnitStatDialog(parent=self,font=self.body_font)
                g.exec_()
                self.entries1[self.sender().row].clear()
                if self.sender().row != 12:
                    self.entries1[self.sender().row].addItem("Number")
                self.entries1[self.sender().row].addItem("Unit Stat")
                self.entries1[self.sender().row].addItem(g.data)
                self.entries1[self.sender().row].setCurrentText(g.data)
            string = self.sender().name.split("&")
            string = string[0] + self.entries1[self.sender().row].currentText() + string[1] + str(self.entries2[self.sender().row].value()) + string[2]
            self.toggle_save(string, self.sender(), self)
            
        elif self.sender().row == 3 or self.sender().row == 12:
            string = self.sender().name.split("&")
            string = string[0] + self.entries1[self.sender().row].currentText() + string[1] + str(self.entries2[self.sender().row].value()) + string[2]
            self.toggle_save(string, self.sender(), self)
            
        elif self.sender().row > 3 and self.sender().row <= 10:
            string = self.sender().name
            self.toggle_save(string, self.sender(), self)
        
        elif self.sender().row == 11:
            string = self.sender().name.split("&")
            string = string[0] + self.entries1[self.sender().row].currentText() + string[1]
            self.toggle_save(string, self.sender(), self)

    def toggle_save(self,string, sender, parent):
        self.parent = parent.parent
        self.p = parent
        if sender.isChecked():
            if string not in self.parent.weapon.special_abilities:
                self.parent.weapon.special_abilities.append(string)
                if self.parent.weapon.path != None:
                    self.parent.weapon.selfToJSON()
                    self.p.current_abilities.setPlainText(str(self.parent.weapon.special_abilities))
        else:
            if string in self.parent.weapon.special_abilities:
                self.parent.weapon.special_abilities.remove(string)
                if self.parent.weapon.path != None:
                    self.parent.weapon.selfToJSON()
                    self.p.current_abilities.setPlainText(str(self.parent.weapon.special_abilities))
    
    def reset(self):
        self.parent.weapon.special_abilities = []
        self.current_abilities.setPlainText(str(self.parent.weapon.special_abilities))
        
        for x in self.ability_checks:
            self.ability_checks[x].setChecked(False)
        
        if self.parent.weapon.path != None:
            self.parent.weapon.selfToJSON()
            
            
                    
               
            