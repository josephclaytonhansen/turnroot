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
        row_count = 0
        
        self.rt = 0
        self.l = 0
        
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
        
        self.test_runs = QLabel("Levelled Up "+str(self.rt)+" Times")
        self.test_runs.setFont(self.body_font)
        self.likely = QLabel("Based on current rates, "+str(self.l)+"% of level ups\nwill have the same stat gain as this level up")
        self.likely.setFont(self.body_font)
        
        self.layout.addWidget(test, row_count+1,  0)
        self.layout.addWidget(clear,row_count+3,0)
        self.layout.addWidget(self.test_runs,row_count+1,1)
        self.layout.addWidget(self.likely,row_count+2,0,1,2)
    
    def reset(self):
        self.stat_amounts = {}
        for s in self.universal_stats:
            self.stat_amounts[s] = 0
            self.amounts[s].setText("+"+str(self.stat_amounts[s]))
            self.amounts[s].setStyleSheet("background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
            self.rt= 0
            self.test_runs.setText("Levelled Up "+str(self.rt)+" Times")
            self.l = 0
            self.likely.setText("Based on current rates, this level up is "+str(self.l)+"% likely")
    
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
            expected_outcomes[s] = ugr[s]
            actual_outcomes[s] = 0
            rate = int(random.random() * 100)
            if rate <= actual_rate:
                self.stat_amounts[s] +=1
                actual_outcomes[s] = ugr[s]
                self.amounts[s].setText("+"+str(self.stat_amounts[s]))
                self.amounts[s].setStyleSheet("background-color: "+self.active_theme.list_background_color+";color: "+self.active_theme.window_text_color)
            else:
                self.amounts[s].setStyleSheet("background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.rt += 1
        self.test_runs.setText("Levelled Up "+str(self.rt)+" Times")
        
        prob = 0
        for s in actual_outcomes:
            if actual_outcomes[s] == expected_outcomes[s]:
                prob += 1
        
        prob = prob / len(actual_outcomes)
        prob = int(prob * 100)
        self.l = prob
        
        self.likely.setText("Based on current rates, this level up is "+str(self.l)+"% likely")
                
            
            
        