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
        self.layout.setContentsMargins(8,8,8,8)
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
        self.total_likely.setFont(self.h_font)
        
        self.good_bad = QLabel()
        self.good_bad.setPixmap(QPixmap("src/ui_icons/white/bad.png"))
        
        self.layout.addWidget(test, row_count+1,  0)
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
            self.good_bad.setToolTip("This variation score means level ups will be unique.\nMore variance is not needed")
        
        elif self.total_l >= 45 and self.total_l < 65:
            self.good_bad.setPixmap(QPixmap("src/ui_icons/white/medium.png"))
            self.good_bad.setToolTip("This variation score means many level ups will be similar.\nIf this is unwanted, consider adding more variance to your growth rates")
        
        else:
            self.good_bad.setPixmap(QPixmap("src/ui_icons/white/bad.png"))
            self.good_bad.setToolTip("This variation score means that most level ups will be the same.\nIf your score is low after repeated testing, add more variance to your growth rates")
        
        self.likely.setText("This level up is ~"+str(self.l)+"% likely")
        self.total_likely.setText("Variation score: "+str(self.total_l)+"%")