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
from src.game_directory import gameDirectory

g = gameDirectory(None)
PATH = g.getPath()
if PATH == None:
    PATH = "/"

class testGrowthDialog(QDialog):
    def __init__(self, parent=None,font=None):
        data = updateJSON()
        self.parent = parent
        self.restart = False
        self.body_font = font
        self.h_font = QFont(self.body_font)
        self.h_font.setPointSize(20)
        self.active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        super().__init__(parent)
        
        self.setStyleSheet("background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.layout = QGridLayout()
        self.layout.setContentsMargins(12,12,12,12)
        self.setLayout(self.layout)
        
        with open("src/skeletons/universal_stats.json", "r") as stats_file:
            self.universal_stats =  json.load(stats_file)
            universal_stats = self.universal_stats
        
        self.amounts = {}
        self.stat_amounts = {}
        row_count = 1
        
        self.rt = 0
        self.l = 0
        self.total_l = 0
        self.rolls = 0
        
        h = QLabel("Given unit growth rates and class growth rates:")
        h.setToolTip("If no class is selected, only unit growth rates will be factored in.")
        h.setFont(self.h_font)
        self.layout.addWidget(h,0,0,1,2)
        
        for s in universal_stats:
            self.stat_amounts[s] = 0
            row_count +=1
            label = QLabel(s)
            label.setFont(self.body_font)
            amount = QLabel("+0")
            amount.setFont(self.body_font)
            self.amounts[s] = amount
            self.layout.addWidget(label, row_count, 0)
            self.layout.addWidget(amount, row_count, 1)
        
        test = QPushButton("Level Up")
        test.clicked.connect(self.run_test)
        test.setFont(self.body_font)
        
        clear = QPushButton("Reset")
        clear.clicked.connect(self.reset)
        clear.setFont(self.body_font)
        
        self.test_runs = QLabel("Leveled Up "+str(self.rt)+" Times")
        self.test_runs.setFont(self.body_font)
        self.likely = QLabel("This level up is ~"+str(self.l)+"% likely")
        self.likely.setFont(self.body_font)
        
        self.total_likely = QLabel("Variation score: "+str(self.total_l)+"%")
        self.total_likely.setToolTip("You should run a test 10+ times (without resetting) to get an accurate variation score.\nVariation score will fluctuate too much to be useful until that point")
        self.total_likely.setFont(self.h_font)
        
        self.good_bad = QLabel()
        self.good_bad.setPixmap(QPixmap("src/ui_icons/white/bad.png"))
        self.good_bad.setToolTip("This variation score means that most level ups will be similar or the same.\nIf your score is low after repeated testing, add more variance to your growth rates")
        
        self.layout.addWidget(test, row_count+1,0)
        self.layout.addWidget(clear,row_count+4,0)
        self.layout.addWidget(self.test_runs,row_count+1,1)
        self.layout.addWidget(self.likely,row_count+2,0,1,2)
        self.layout.addWidget(self.total_likely,row_count+3,0,1,1)
        self.layout.addWidget(self.good_bad,row_count+3,1,1,1)
    
    def reset(self):
        self.stat_amounts = {}
        for s in self.universal_stats:
            self.stat_amounts[s] = 0
            self.amounts[s].setText("+"+str(self.stat_amounts[s]))
            self.amounts[s].setStyleSheet("background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
            self.rt= 0
            self.test_runs.setText("Leveled Up "+str(self.rt)+" Times")
            self.l = 0
            self.rolls = 0
            self.total_l = 0
            self.likely.setText("This level up is ~"+str(self.l)+"% likely")
            self.total_likely.setText("Variation score: "+str(self.total_l)+"%")
            self.good_bad.setPixmap(QPixmap("src/ui_icons/white/bad.png"))
            self.good_bad.setToolTip("This variation score means that most level ups will be the same.\nIf your score is low after repeated testing, add more variance to your growth rates")
    
    def run_test(self):
        self.unit = self.parent.parent.unit
        ugr = self.unit.growth_rates
        cgr = self.unit.unit_class.growth_rates
        if len(cgr) == 0:
            self.unit.unit_class = self.parent.parent.loaded_class
            cgr = self.unit.unit_class.growth_rates
        
        expected_outcomes = {}
        actual_outcomes = {}
        
        with open("src/skeletons/universal_stats.json", "r") as stats_file:
            universal_stats =  json.load(stats_file)
        
        for s in universal_stats:
            try:
                actual_rate = (ugr[s] + cgr[s]) / 2
            except:
                actual_rate = ugr[s]

            expected_outcomes[s] = actual_rate / 100
            actual_outcomes[s] = 0
            rate = int(random.random() * 99)+1
            if rate <= actual_rate:
                self.stat_amounts[s] +=1
                actual_outcomes[s] = 1
                self.amounts[s].setText("+"+str(self.stat_amounts[s]))
                self.amounts[s].setStyleSheet("background-color: "+self.active_theme.list_background_color+";color: "+self.active_theme.window_text_color)
            else:
                self.amounts[s].setStyleSheet("background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.rt += 1
        self.test_runs.setText("Leveled Up "+str(self.rt)+" Times")
        
        prob = 0
        for s in actual_outcomes:
            if actual_outcomes[s] >= expected_outcomes[s]:
                prob += 1
                self.rolls += 1
        
        prob = prob / len(actual_outcomes)
        prob = int(prob * 100)
        self.l = prob
        self.total_l = int((self.rolls / self.rt*len(actual_outcomes)))
        self.total_l = 100  - self.total_l
        
        if self.total_l >= 65:
            self.good_bad.setPixmap(QPixmap("src/ui_icons/white/good.png"))
            self.good_bad.setToolTip("This variation score means level ups will be unique.\nIf this persists after repeated testing, more variance is not needed")
        
        elif self.total_l >= 45 and self.total_l < 65:
            self.good_bad.setPixmap(QPixmap("src/ui_icons/white/medium.png"))
            self.good_bad.setToolTip("This variation score means many level ups will be similar.\nIf this persists after repeated testing, consider adding more variance to your growth rates")
        
        else:
            self.good_bad.setPixmap(QPixmap("src/ui_icons/white/bad.png"))
            self.good_bad.setToolTip("This variation score means that most level ups will be similar or the same.\nIf your score is low after repeated testing, add more variance to your growth rates")
        
        self.likely.setText("This level up is ~"+str(self.l)+"% likely")
        self.total_likely.setText("Variation score: "+str(self.total_l)+"%")

class weakAgainstDialog(QDialog):
    def __init__(self, parent=None,font=None):
        data = updateJSON()
        self.parent = parent
        self.restart = False
        self.body_font = font
        self.h_font = QFont(self.body_font)
        self.h_font.setPointSize(20)
        self.active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        super().__init__(parent)
        
        self.setStyleSheet("background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.layout = QGridLayout()
        self.layout.setContentsMargins(12,12,12,12)
        self.setLayout(self.layout)
        
        weapon_types = weaponTypes().data

        self.loaded = self.parent.loaded_class
        if self.loaded.unit_class_name == None:
            self.load_data = False
        else:
            self.load_data = True
        
        amount_label = QLabel("Effective damage multiplier")
        amount_label.setFont(self.body_font)
        amount_label.setToolTip("Usual values are double (2) or triple (3)")
        self.layout.addWidget(amount_label,1,0,1,1)
        
        amount = QDoubleSpinBox()
        amount.setRange(1.0,3.0)
        amount.setSingleStep(1.0)
        amount.setValue(2.0)
        if self.load_data:
            amount.setValue(self.loaded.weak_against_amount)
        amount.valueChanged.connect(self.value_changed)
        amount.setFont(self.body_font)
        self.layout.addWidget(amount,1,1,1,1)
        
        self.rows = {}
        self.checks = {}
        row_count = 1
        
        info = QLabel("Effective damage types (this class is weak against)")
        info.setFont(self.h_font)
        self.layout.addWidget(info,0,0,1,2)
        
        for w in weapon_types:
            row_count+=1
            l = QLabel(w)
            l.setFont(self.body_font)
            self.layout.addWidget(l,row_count,0,1,1)
            
            r = QCheckBox()
            if self.load_data:
                if w in self.loaded.weak_against:
                    r.setChecked(True)
            r.name = w
            r.stateChanged.connect(self.check)
            self.layout.addWidget(r,row_count,1,1,1)
            
    def check(self):
        if self.sender().name not in self.loaded.weak_against:
            self.loaded.weak_against.append(self.sender().name)
    
    def value_changed(self):
        self.loaded.weak_against_amount = self.sender().value()
    
class expTypesDialog(QDialog):
    def __init__(self, parent=None,font=None):
        data = updateJSON()
        self.parent = parent
        self.restart = False
        self.body_font = font
        self.h_font = QFont(self.body_font)
        self.h_font.setPointSize(20)
        self.active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        super().__init__(parent)
        
        self.setStyleSheet("background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.layout = QGridLayout()
        self.layout.setContentsMargins(12,12,12,12)
        self.setLayout(self.layout)
        
        weapon_types = weaponTypes().data
        extra_exp_types = expTypes().data

        self.loaded = self.parent.loaded_class
        if self.loaded.unit_class_name == None:
            self.load_data = False
        else:
            self.load_data = True
        
        self.rows = {}
        self.checks = {}
        row_count = 0
        
        info = QLabel("EXP Types Gained")
        info.setFont(self.h_font)
        self.layout.addWidget(info,0,0,1,2)
        
        for w in weapon_types+extra_exp_types:
            row_count+=1
            l = QLabel(w)
            l.setFont(self.body_font)
            self.layout.addWidget(l,row_count,0,1,1)
            
            r = QCheckBox()
            if self.load_data:
                if w in self.loaded.experience_types_gained:
                    r.setChecked(True)
            r.name = w
            r.stateChanged.connect(self.check)
            self.layout.addWidget(r,row_count,1,1,1)
            
    def check(self):
        if self.sender().name not in self.loaded.experience_types_gained:
            self.loaded.weak_against.append(self.sender().name)

class nextClassesDialog(QDialog):
    def __init__(self, parent=None,font=None):
        data = updateJSON()
        self.parent = parent
        self.restart = False
        self.body_font = font
        self.h_font = QFont(self.body_font)
        self.h_font.setPointSize(20)
        self.active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        super().__init__(parent)
        
        self.setStyleSheet("background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.layout = QGridLayout()
        self.layout.setContentsMargins(12,12,12,12)
        self.setLayout(self.layout)

        self.loaded = self.parent.loaded_class
        
        classes = self.getClassesInFolder()
        if self.loaded.unit_class_name in classes:
            classes.remove(self.loaded.unit_class_name)
        
        if len(classes) == 0:
            classes = ["No saved classes"]
        
        self.rows = {}
        self.checks = {}
        row_count = 0
        
        info = QLabel("Next Classes")
        info.setToolTip("Applicable only for branching classes")
        info.setFont(self.h_font)
        self.layout.addWidget(info,0,0,1,2)
        
        for w in classes:
            row_count+=1
            l = QLabel(w)
            l.setFont(self.body_font)
            self.layout.addWidget(l,row_count,0,1,1)
            
            r = QCheckBox()
            if w in self.loaded.next_classes:
                r.setChecked(True)
            r.name = w
            r.stateChanged.connect(self.check)
            if w != "No saved classes":
                self.layout.addWidget(r,row_count,1,1,1)
            
    def check(self):
        if self.sender().name not in self.loaded.next_classes:
            self.loaded.next_classes.append(self.sender().name)
    
    def getClassesInFolder(self):
        file_list = getFiles(PATH+"/classes")[GET_FILES]
        class_names = []
        for f in file_list:
            tmp_class = unitClass()
            try:
                tmp_class.selfFromJSON(f.path)
                class_names.append(tmp_class.unit_class_name)
            except:
                print(f.path," failed to load")
        return class_names

class classGraphicDialog(QDialog):
    def __init__(self, parent=None,font=None):
        data = updateJSON()
        self.parent = parent
        self.restart = False
        self.body_font = font
        self.h_font = QFont(self.body_font)
        self.h_font.setPointSize(20)
        self.active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        super().__init__(parent)
        
        self.setStyleSheet("background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.layout = QGridLayout()
        self.layout.setContentsMargins(12,12,12,12)
        self.setLayout(self.layout)

        self.loaded = self.parent.loaded_class
        
            
class editUniversalWeaponTypes(QDialog):
    def __init__(self, parent=None,font=None):
        data = updateJSON()
        self.parent = parent
        self.restart = False
        self.active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        super().__init__(parent)
        self.font = font
        self.body_font = self.font
        
        self.setStyleSheet("background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(12,12,12,12)
        
        row = QWidget()
        row_layout = QHBoxLayout()
        row.setLayout(row_layout)
        
        with open("src/skeletons/universal_weapon_types.json", "r") as weapons_file:
            weapon_types = json.load(weapons_file)
        
        self.list = QListWidget()
        self.list.setFont(self.font)
        self.list.setStyleSheet("background-color: "+self.active_theme.list_background_color+";color: "+self.active_theme.window_text_color)
        self.list.addItems(weapon_types)
    
        row_layout.addWidget(self.list)
        
        row2 = QWidget()
        row2_layout = QHBoxLayout()
        row2.setLayout(row2_layout)
        
        self.add_stat_name = QLineEdit()
        self.add_stat_name.setFont(self.font)
        self.add_stat_name.setStyleSheet("background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.add_stat_name.setPlaceholderText("New weapon type name")
        
        self.add_stat = QPushButton("+Add Weapon Type")
        self.add_stat.setFont(self.font)
        self.add_stat.clicked.connect(self.addType)
        
        self.remove_stat = QPushButton("-Remove Selected Weapon Type")
        self.remove_stat.setFont(self.font)
        self.remove_stat.clicked.connect(self.removeType)
        
        row2_layout.addWidget(self.add_stat_name)
        row2_layout.addWidget(self.add_stat)
        row2_layout.addWidget(self.remove_stat)
        
        row3 = QWidget()
        row3_layout = QHBoxLayout()
        row3.setLayout(row3_layout)
        
        self.change_desc = QLineEdit()
        self.change_desc.setFont(self.font)
        self.change_desc.textChanged.connect(self.desc_change)
        self.change_desc_label = QLabel("Change selected weapon type's description")
        self.change_desc_label.setFont(self.font)
        self.change_desc_label.setToolTip("This will show in game")
        
        self.change_icon = QPushButton()
        self.change_icon.clicked.connect(self.icon_change)
        self.change_icon.setIcon(QIcon(QPixmap("src/ui_icons/white/image.png")))
        self.change_icon.setIconSize(QSize(40,40))
        self.change_icon.setToolTip("Change in-game icon")
        
        row3_layout.addWidget(self.change_desc_label)
        row3_layout.addWidget(self.change_desc)
        row3_layout.addWidget(self.change_icon)
        
        self.layout.addWidget(row)
        self.layout.addWidget(row2)
        self.layout.addWidget(row3)
        
        self.close_button = QPushButton("Close")
        self.close_button.setFont(self.body_font)
        self.layout.addWidget(self.close_button)
        self.close_button.clicked.connect(self.close)
        
        self.setLayout(self.layout)
    
    def addType(self):
        c = confirmAction("#This will add this weapon type to all units in the game, do you want to continue?", parent=self)
        c.exec_()
        if(c.return_confirm):
            self.parent.unit.createUniversalWeaponsType(self.add_stat_name.text())
            self.restart = True
            self.close()
    
    def removeType(self):
        c = confirmAction("#This will remove this weapon type from all units in the game, do you want to continue?",parent=self)
        c.exec_()
        if(c.return_confirm):
            y = self.list.currentItem().text()
            self.parent.unit.removeUniversalWeaponsType(y)
            
            if os.path.exists("src/skeletons/weapon_types/"+y+".json"):
                os.remove("src/skeletons/weapon_types/"+y+".json")
            
            self.close()
            self.restart = True
        
    def icon_change(self):
        pass

    def desc_change(self):
        pass
        
class editClassifications(QDialog):
    def __init__(self, parent=None, font =None):
        data = updateJSON()
        self.parent = parent
        self.restart = False
        self.active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        super().__init__(parent)
        self.body_font = font
        
        self.setStyleSheet("background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(12,12,12,12)
        self.setMinimumWidth(620)
        
        row = QWidget()
        row_layout = QHBoxLayout()
        row.setLayout(row_layout)
        
        with open("src/skeletons/universal_classifications.json", "r") as stats_file:
            universal_stats =  json.load(stats_file)
        
        self.list = QListWidget()
        self.list.setFont(self.body_font)
        self.list.setStyleSheet("background-color: "+self.active_theme.list_background_color+";color: "+self.active_theme.window_text_color)
        self.list.addItems(universal_stats)
    
        row_layout.addWidget(self.list)
        
        row2 = QWidget()
        row2_layout = QHBoxLayout()
        row2.setLayout(row2_layout)
        
        self.add_stat_name = QLineEdit()
        self.add_stat_name.setFont(self.body_font)
        self.add_stat_name.setStyleSheet("background-color: "+self.active_theme.list_background_color+";color: "+self.active_theme.window_text_color)
        self.add_stat_name.setPlaceholderText("New classification name")
        
        self.add_stat = QPushButton("+Add Classification")
        self.add_stat.setStyleSheet("background-color: "+self.active_theme.list_background_color+";color: "+self.active_theme.window_text_color)
        self.add_stat.setFont(self.body_font)
        self.add_stat.clicked.connect(self.addStat)
        
        self.remove_stat = QPushButton("-Remove Selected Classification")
        self.remove_stat.setStyleSheet("background-color: "+self.active_theme.list_background_color+";color: "+self.active_theme.window_text_color)
        self.remove_stat.setFont(self.body_font)
        self.remove_stat.clicked.connect(self.removeStat)
        
        row2_layout.addWidget(self.add_stat_name)
        row2_layout.addWidget(self.add_stat)
        row2_layout.addWidget(self.remove_stat)
        
        self.layout.addWidget(row)
        self.layout.addWidget(row2)
        
        self.setLayout(self.layout)
    
    def addStat(self):
        c = confirmAction("#This will add this classification to the game, do you want to continue?", parent=self)
        c.exec_()
        if(c.return_confirm):
            self.parent.unit.createUniversalClassification(self.add_stat_name.text())
            self.restart = True
            self.close()
    
    def removeStat(self):
        c = confirmAction("#This will remove this classification from the game, do you want to continue?",parent=self)
        c.exec_()
        if(c.return_confirm):
            self.parent.unit.removeUniversalClassification(self.list.currentItem().text())
            self.restart = True
            self.close()
            
class statCapDialog(QDialog):
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
        
        with open("src/skeletons/universal_stats.json", "r") as stats_file:
            universal_stats =  json.load(stats_file)
        
        self.rows = {}
        self.labels = {}
        self.values = {}
        
        for s in universal_stats:
            if s not in self.parent.unit.stat_caps:
                self.parent.unit.stat_caps[s] = 0
            row = QWidget()
            row_layout = QHBoxLayout()
            row.setLayout(row_layout)
            
            self.rows[s] = row
            
            label = QLabel(s)
            label.setFont(self.body_font)
            self.labels[s] = label
            row_layout.addWidget(label)
            
            value = QSpinBox()
            value.setFont(self.body_font)
            value.name = s
            value.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: "+self.active_theme.list_background_color+";color: "+self.active_theme.window_text_color)
            value.setRange(0,100)
            value.setValue(self.parent.unit.stat_caps[s])
            value.valueChanged.connect(self.value_changed)
            self.values[s] = value
            row_layout.addWidget(value)
            
            self.layout.addWidget(row)
            
        self.setLayout(self.layout)
        
    def value_changed(self):
        try:
            self.parent.unit.stat_caps[self.sender().name] = self.sender().value()
        except:
            pass

class baseClassesDialog(QDialog):
    def __init__(self, parent=None,font=None):
        data = updateJSON()
        self.parent = parent
        self.restart = False
        self.body_font = font
        self.h_font = QFont(self.body_font)
        self.h_font.setPointSize(20)
        self.active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        super().__init__(parent)
        
        self.setStyleSheet("background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.inner = QWidget()
        self.layout = QGridLayout()
        self.inner.setLayout(self.layout)
        
        self.outer_layout = QVBoxLayout()
        self.layout.setContentsMargins(12,12,12,12)
        self.tscroll = QScrollArea()
        self.tscroll.setWidget(self.inner)
        self.tscroll.setWidgetResizable(True)
        info = QLabel("Base classes this unit can re-class to")
        info.setToolTip("Applicable only for branching classes")
        info.setFont(self.h_font)
        self.outer_layout.addWidget(info)
        self.outer_layout.addWidget(self.tscroll)
        self.setLayout(self.outer_layout)
       
        c = self.getClassesInFolder()
        classes = c[0]
        for k in classes:
            #THIS NEEDS TO CHANGE! Base classes are the ONLY kind that should show up
            if c[1][k].class_type == "basic":
                classes.remove(c[1][k].unit_class_name)
        
        if len(classes) == 0:
            classes = ["No saved classes"]
        
        self.rows = {}
        self.checks = {}
        row_count = 0
        
        for w in classes:
            row_count+=1
            l = QLabel(w)
            l.setFont(self.body_font)
            self.layout.addWidget(l,row_count,0,1,1)
            
            r = QCheckBox()
            if w in self.parent.unit.past_classes:
                r.setChecked(True)
            r.name = w
            r.stateChanged.connect(self.check)
            if w != "No saved classes":
                self.layout.addWidget(r,row_count,1,1,1)
            
    def check(self):
        if self.sender().isChecked() == False:
            self.parent.unit.past_classes.remove(self.sender().name)
        else:
            if self.sender().name not in self.parent.unit.past_classes:
                self.parent.unit.past_classes.append(self.sender().name)
    
    def getClassesInFolder(self):
        file_list = getFiles(PATH+"/classes")[GET_FILES]
        class_names = []
        cla = {}
        for f in file_list:
            tmp_class = unitClass()
            try:
                tmp_class.selfFromJSON(f.path)
                class_names.append(tmp_class.unit_class_name)
                cla[tmp_class.unit_class_name] = tmp_class
            except:
                print(f.path," failed to load")
        return [class_names, cla]