from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QPalette, QIcon, QPixmap, QCursor, QFont
from src.UI_updateJSON import updateJSON
import src.UI_colorTheme
import shutil, os, pickle, json, sys, random
from src.UI_Dialogs import confirmAction, popupInfo
from src.node_backend import getFiles, GET_FILES
from src.img_overlay import overlayTile
from src.skeletons.unit_class import unitClass
from src.skeletons.unit import Unit
from src.skeletons.weapon_types import weaponTypes, expTypes
from src.skeletons.Object import (Object,usableItem,Key,healItem,statIncreaseItem,expIncreaseItem,Healing,
                                  classChangeItem,summoningItem,levelEffectItem,equippableItem,Weapon,Shield)

FORGED_WEAPONS_INDEX = 0
FORGED_WEAPONS = {}

class chooseUnitStatDialog(QDialog):
    def __init__(self, parent=None,font=None):
        data = updateJSON()
        self.parent = parent
        self.restart = False
        self.active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        super().__init__(parent)
        self.setMinimumWidth(200)
        self.body_font = font
        
        self.setStyleSheet("background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(12,12,12,12)
        self.setLayout(self.layout)
        
        with open("src/skeletons/universal_stats.json", "r") as stats_file:
            universal_stats =  json.load(stats_file)
        
        self.list = QListWidget()
        self.list.currentTextChanged.connect(self.returnData)
        self.list.setFont(self.body_font)
        self.list.setStyleSheet("background-color: "+self.active_theme.list_background_color+";color: "+self.active_theme.window_text_color)
        self.list.addItems(universal_stats)
        self.layout.addWidget(self.list)
                
        self.close_button = QPushButton("Close")
        self.close_button.setFont(self.body_font)
        self.layout.addWidget(self.close_button)
        self.close_button.clicked.connect(self.close)
    
    def returnData(self):
        self.data = self.sender().currentItem().text()

class forgingDialog(QDialog):
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
        self.setMinimumWidth(400)
        
        self.setStyleSheet("background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(12,12,12,12)
        self.setLayout(self.layout)
        
        self.tabs = QTabWidget()
        self.tabs_font = self.tabs.font()
        self.tabs_font.setPointSize(12)
        self.tabs.setFont(self.tabs_font)
        
        self.tabs.setTabPosition(QTabWidget.South)
        
        self.layout.addWidget(self.tabs)
        
        self.tab_names = ["Repair", "Forging"]
        self.tabs_dict = {}
        
        for tab in self.tab_names:
            self.tab_title = tab
            self.c_tab = QWidget()
            self.c_tab_layout = QGridLayout()
            self.c_tab.setLayout(self.c_tab_layout)
            self.tabs_dict[tab] = self.c_tab
            self.tabs.addTab(self.c_tab, self.tab_title)
        
        self.initRepair()
        self.initForging()
        
    def initRepair(self):
        self.working_tab = self.tabs_dict["Repair"]
        self.working_tab_layout = self.working_tab.layout()
        active_theme = self.active_theme
        data = updateJSON()
        
        repair_cost_per = QSpinBox()
        repair_items_amounts = QSpinBox()
        self.spinners = [repair_cost_per,repair_items_amounts]
        self.att = ["repair_cost_per","repair_items_amounts"]
        labels = ["Repair Price Per Use","Repair Item Quantity Per 10 Uses*"]
        r = 0
        for x in self.spinners:
            r+=1
            x.setFont(self.body_font)
            x.setRange(0,1000)
            x.name = self.att[self.spinners.index(x)]
            try:
                x.setValue(getattr(self.parent.weapon, self.att[self.spinners.index(x)]))
            except:
                pass
            x.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
            x.valueChanged.connect(self.change_value)
            self.working_tab_layout.addWidget(x, r, 1, 1, 2)
            label = QLabel(labels[r-1])
            label.setFont(self.body_font)
            self.working_tab_layout.addWidget(label,r,0,1,1)
        
        self.rate_slider = QSlider(Qt.Horizontal)
        self.rate_slider.name = 1
        self.rate_slider.valueChanged.connect(self.colorizeSlider)
        self.rate_slider.setValue(int(self.parent.weapon.full_durability/2))
        self.rate_slider.setRange(0,self.parent.weapon.full_durability)
        self.rate_slider.setSingleStep(1)
        
        self.working_tab_layout.addWidget(self.rate_slider,r+6,0,1,3)
        
        h = QLabel("Used, this item would cost X to repair...")
        h.setFont(self.h_font)
        self.working_tab_layout.addWidget(h,r+4,0,1,2)
        t = QLabel("Change used amount")
        t.setToolTip("Durability must be greater than 0. Set with the Combat button")
        t.setFont(self.body_font)
        self.working_tab_layout.addWidget(t,r+5,0,1,2)
        
        self.used_uses = QLabel("Remaining Uses: ")
        self.used_uses.setFont(self.body_font)
        self.cost = QLabel(" Cost: ")
        self.cost.setFont(self.body_font)
        self.working_tab_layout.addWidget(self.used_uses, r+7, 0, 1,1)
        self.working_tab_layout.addWidget(self.cost,r+7,1,1,1)
        self.item_cost = QLabel(" Item Cost: ")
        self.item_cost.setFont(self.body_font)
        self.working_tab_layout.addWidget(self.item_cost,r+7,2,1,1)
        
        i = QLabel("*Set to 0 if this weapon doesn't require items to repair")
        self.working_tab_layout.addWidget(i,r+3,0,1,1)
        
        forging_item_label = QLabel("Item Used for Repairs")
        forging_item_label.setFont(self.body_font)
        self.working_tab_layout.addWidget(forging_item_label, r+2,0,1,1)
        
        self.class_list = QComboBox()
        self.class_list.setStyleSheet("background-color: "+self.active_theme.list_background_color+";color: "+self.active_theme.window_text_color)
        self.class_list.setFont(self.body_font)
        self.working_tab_layout.addWidget(self.class_list, r+2,1,1,2)
        self.class_list.currentTextChanged.connect(self.change)
        self.getWeaponsInFolder()
        self.show()
    
    def initForging(self):
        self.working_tab = self.tabs_dict["Forging"]
        self.working_tab_layout = self.working_tab.layout()
        active_theme = self.active_theme
        data = updateJSON()
        
        self.list = QListWidget()
        self.list.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
        self.list.currentTextChanged.connect(self.change_active_item)
        
        if len(self.parent.weapon.forge_into) > 0:
            pass
            #populate list with forge intos
        
        else:
            pass
        
        self.tscroll = QScrollArea()
        self.tscroll.setWidget(self.list)
        self.tscroll.setWidgetResizable(True)
        
        self.working_tab_layout.addWidget(self.tscroll,0,0,4,4)
        
        self.add = QPushButton()
        self.add.clicked.connect(self.add_forged)
        self.add.setMaximumWidth(40)
        self.add.setIcon(QIcon(QPixmap("src/ui_icons/white/add.png")))
        self.add.setIconSize(QSize(38,38))
        self.add.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
        self.remove = QPushButton()
        self.remove.setMaximumWidth(40)
        self.remove.setIcon(QIcon(QPixmap("src/ui_icons/white/dl.png")))
        self.remove.setIconSize(QSize(34,34))
        self.remove.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
        self.edit = QPushButton()
        self.edit.clicked.connect(self.edit_active_item)
        self.edit.setMaximumWidth(40)
        self.edit.setIcon(QIcon(QPixmap("src/ui_icons/white/edit.png")))
        self.edit.setIconSize(QSize(34,34))
        self.edit.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
        
        for w in [self.list, self.add, self.remove,self.edit]:
            w.setFont(self.body_font)
            w.setMinimumHeight(40)
        
        self.working_tab_layout.addWidget(self.add,4,1,1,1)
        self.working_tab_layout.addWidget(self.remove,4,2,1,1)
        self.working_tab_layout.addWidget(self.edit,4,3,1,1)

    def add_forged(self):
        pass
    
    def change_active_item(self):
        self.active_item = self.sender().currentItem()
    
    def edit_active_item(self):
        pass
 
    def getWeaponsInFolder(self):
        file_list = getFiles("src/skeletons/items/forging_items")[GET_FILES]
        class_names = []
        global classes
        classes = {}
        self.paths = {}
        for f in file_list:
            f.fullPath = f.fullPath.replace("\\", "/")
            if f.ext.strip() == ".trfof":
                tmp_class = usableItem()
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
            self.full_list.append(self.class_list.itemText(x))
    
    def change(self,s):
        self.parent.weapon.repair_items = self.sender().currentText()
        if self.parent.weapon.path != None:
            self.parent.weapon.selfToJSON()
        
    def change_value(self):
        self.cost.setText(" Cost: ")
        self.item_cost.setText(" Item Cost: ")
        setattr(self.parent.weapon, self.sender().name, self.sender().value()) 
        if self.parent.weapon.path != None:
            self.parent.weapon.selfToJSON()
    
    def colorizeSlider(self, v):
        try:
            self.cost_at_use = ((v) * self.parent.weapon.repair_cost_per)
            self.used_uses.setText("Remaining Uses: "+str(self.parent.weapon.full_durability-v))
            self.cost.setText(" Price: "+str(self.cost_at_use))
            self.item_cost.setText(" Item Cost: "+str(round(v/10) * self.parent.weapon.repair_items_amounts))
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
    
class forgeWeaponDialog(QDialog):
    def __init__(self, parent=None,font=None):
        data = updateJSON()
        self.parent = parent
        self.active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        active_theme = self.active_theme
        super().__init__(parent)
        self.body_font = font
        self.h_font = QFont(self.body_font)
        self.h_font.setPointSize(20)
        
        self.setStyleSheet("background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(12,12,12,12)
        self.setLayout(self.layout)
        
        label = QLabel("Choose Weapon to Forge Into")
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
        self.class_list.itemClicked.connect(self.change_into)
        
        self.grid = QWidget()
        self.grid_layout = QGridLayout()
        self.grid.setLayout(self.grid_layout)
        self.layout.addWidget(self.grid)
        
        forge_items_amounts = QSpinBox()
        forge_costs = QSpinBox()
        self.spinners = [forge_items_amounts,forge_costs]
        self.att = ["forge_items_amounts","forge_costs"]
        labels = ["Number of Items Needed to Forge","Cost to Forge"]
        r = 1
        
        self.fi_label = QLabel("Item Used for Forging")
        self.fi_label.setFont(self.body_font)
        self.item_list = QComboBox()
        self.item_list.setStyleSheet("background-color: "+self.active_theme.list_background_color+";color: "+self.active_theme.window_text_color)
        self.item_list.setFont(self.body_font)

        self.grid_layout.addWidget(self.fi_label,0,0,1,1)
        self.grid_layout.addWidget(self.item_list,0,1,1,1)
        
        for x in self.spinners:
            r+=1
            x.setFont(self.body_font)
            x.setRange(0,2000)
            x.name = self.att[self.spinners.index(x)]
            
            try:
                x.setValue(getattr(self.parent.parent.weapon, self.att[self.spinners.index(x)]))
            except:
                pass
            
            x.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))

            label = QLabel(labels[r-2])
            label.setFont(self.body_font)
            
            self.grid_layout.addWidget(label, r, 0, 1, 1)
            self.grid_layout.addWidget(x, r, 1, 1, 1)
        
        self.show()
        
class loadSavedHealing(QDialog):
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
        
        label = QLabel("Choose Item")
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
        file_list = getFiles("src/skeletons/items/equippable_healing_items")[GET_FILES]
        class_names = []
        global classes
        classes = {}
        self.paths = {}
        for f in file_list:
            f.fullPath = f.fullPath.replace("\\", "/")
            if f.ext.strip() == ".trhof":
                tmp_class = Healing()
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

class healingAbilitiesDialog(QDialog):
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
            with open("src/tmp/universal_healing_item_abilities.json", "r") as f:
                self.abilities = json.load(f)
        except:
            with open("src/tmp/uhiad.tdndf", "r") as f:
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
        
    def toggle_ability(self):
        pass

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