from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QPalette, QIcon, QPixmap, QCursor, QFont
from src.UI_updateJSON import updateJSON
import src.UI_colorTheme
import shutil, os, pickle, json, sys, random
from src.UI_Dialogs import confirmAction
from src.node_backend import getFiles, GET_FILES
from src.img_overlay import overlayTile
from src.skeletons.unit_class import unitClass
from src.skeletons.unit import Unit
from src.skeletons.weapon_types import weaponTypes, expTypes
from src.skeletons.Object import (Object,usableItem,Key,healItem,statIncreaseItem,expIncreaseItem,
                                  classChangeItem,summoningItem,levelEffectItem,equippableItem,Weapon,Shield)

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
        self.layout.addWidget(q, 0, 0, 1,2)
        
        r = 0
        for x in ["might", "hit", "crit", "weight", "full_durability"]:
            r +=1
            if x != "full_durability":
                stat_label = QLabel(x)
            else:
                stat_label = QLabel("durability")
            stat_label.setFont(self.body_font)
            
            stat_value = QSpinBox()
            stat_value.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
            stat_value.name = x
            stat_value.setFont(self.body_font)
            self.values[x] = stat_value
            stat_value.setRange(0,100)

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
            
            self.layout.addWidget(range_row, r+1,0,1,2)
            
    def change_value(self):
        setattr(self.parent.weapon, self.sender().name, self.sender().value()) 
        if self.parent.weapon.path != None:
            self.parent.weapon.selfToJSON()
    
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
        
        self.setStyleSheet("background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(12,12,12,12)
        self.setLayout(self.layout)
        
        label = QLabel("Choose Weapon")
        label.setFont(self.body_font)
        self.layout.addWidget(label)
            
        self.class_list = QListWidget()
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
    
    def change(self,s):
        self.returns = self.paths[self.sender().currentItem().text()]
        self.close()
        
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
        self.att = ["price_if_sold","price","repair_cost_per","buyable_quantity"]
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
        print(self.parent.weapon.full_durability)
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
            self.cost_at_use = self.parent.weapon.price_if_sold - ((self.parent.weapon.full_durability - v) * self.parent.weapon.repair_cost_per)
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