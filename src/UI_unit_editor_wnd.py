from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from src.UI_node_graphics_scene import QDMGraphicsView, QDMGraphicsScene

import json

import src.UI_colorTheme as UI_colorTheme
from src.UI_updateJSON import updateJSON
data = updateJSON()
active_theme = getattr(UI_colorTheme, data["active_theme"])

from src.skeletons.unit import Unit

with open("src/skeletons/universal_stats.json", "r") as stats_file:
    universal_stats =  json.load(stats_file)

class UnitEditorWnd(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        
    def initUI(self):
        self.setStyleSheet("background-color: "+active_theme.window_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.South)
        
        self.tscroll = QScrollArea()
        self.tscroll.setWidget(self.tabs)
        self.tscroll.setWidgetResizable(True)
        
        self.tab_names = ["Basic", "AI", "Attacks", "Actions", "Classes", "Skills",
                          "Tactics", "Skilled Blows", "Objects", "Relationships"]
        
        self.tabs_dict = {}
        for tab in self.tab_names:
            self.tab_title = tab
            self.c_tab = QWidget()
            self.c_tab_layout = QHBoxLayout()
            self.c_tab.setLayout(self.c_tab_layout)
            self.tabs_dict[tab] = self.c_tab
            self.tabs.addTab(self.c_tab, self.tab_title)
        
        self.initUnit()
        
        self.initBasic()
        self.initAI()
        self.initAttacks()
        self.initActions()
        self.initClasses()
        self.initSkills()
        self.initTactics()
        self.initSkilledBlows()
        self.initObjects()
        self.initRelationships()
        
        self.layout.addWidget(self.tscroll)
        
        self.show()
    
    def initUnit(self):
        #get unit from file
        self.unit = Unit()
        
    def initBasic(self):
        self.working_tab = self.tabs_dict["Basic"]
        self.working_tab_layout = self.working_tab.layout()
        
        #split in thirds
        self.basic_layout = QHBoxLayout()
        self.basic_layout_widget = QWidget()
        self.basic_layout_widget.setLayout(self.basic_layout)
        
        self.basic_left = QWidget()
        self.basic_left_layout = QVBoxLayout()
        self.basic_left_layout.setSpacing(0)
        self.basic_left.setLayout(self.basic_left_layout)
        self.basic_layout.addWidget(self.basic_left, 40)
        self.basic_left.setMaximumWidth(350)
        
        self.basic_center = QWidget()
        self.basic_center_layout = QVBoxLayout()
        self.basic_center_layout.setSpacing(0)
        self.basic_center.setLayout(self.basic_center_layout)
        self.basic_layout.addWidget(self.basic_center, 60)
        
        image = QLabel()
        pixmap = QPixmap(270,375)
        image.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        pixmap.fill(QColor("white"))
        image.setPixmap(pixmap)
        self.basic_left_layout.addWidget(image)
        
        name_row = QWidget()
        name_row_layout = QHBoxLayout()
        name_row.setLayout(name_row_layout)
        
        self.name_edit = QLineEdit()
        self.name_edit .setAlignment(Qt.AlignCenter)
        self.name_edit .setPlaceholderText("Name")
        name_font = self.name_edit.font()
        name_font.setPointSize(18)
        self.name_edit.setFont(name_font)
        name_row_layout.addWidget(self.name_edit)
        
        name_row_layout.addWidget(QLabel(" - "))
        
        self.title_edit = QLabel()
        self.title_edit.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.title_edit.setText("Soldier")
        title_font = self.title_edit.font()
        title_font.setPointSize(18)
        self.title_edit.setFont(title_font)
        name_row_layout.addWidget(self.title_edit)
        
        self.basic_left_layout.addWidget(name_row)
        
        identity_row = QWidget()
        identity_row_layout = QHBoxLayout()
        identity_row.setLayout(identity_row_layout)
        
        self.gender_edit = QComboBox()
        self.gender_edit.addItems(["Male", "Female", "Non-Binary", "Custom"])
        gender_font = self.gender_edit.font()
        gender_font.setPointSize(16)
        self.gender_edit.setFont(title_font)
        identity_row_layout.addWidget(self.gender_edit)
        
        self.pronouns_edit = QComboBox()
        self.pronouns_edit.addItems(["He/Him/His", "She/Her/Hers", "They/Them/Theirs", "Custom"])
        gender_font = self.pronouns_edit.font()
        gender_font.setPointSize(16)
        self.pronouns_edit.setFont(title_font)
        identity_row_layout.addWidget(self.pronouns_edit)
        
        self.basic_left_layout.addWidget(identity_row)
        
        checkbox_row = QWidget()
        checkbox_row_layout = QHBoxLayout()
        checkbox_row.setLayout(checkbox_row_layout)
        
        protag_label = QLabel("Protagonist")
        self.protag = QCheckBox()
        
        generic_label = QLabel("Generic")
        self.generic = QCheckBox()
        
        checkbox_font = protag_label.font()
        checkbox_font.setPointSize(16)
        protag_label.setFont(checkbox_font)
        self.protag.setFont(checkbox_font)
        generic_label.setFont(checkbox_font)
        self.generic.setFont(checkbox_font)
        
        self.friendly_toggle = QPushButton("Friendly")
        self.friendly_toggle.setFont(checkbox_font)
        checkbox_row_layout.addWidget(self.friendly_toggle)
        
        checkbox_row_layout.addWidget(protag_label)
        checkbox_row_layout.addWidget(self.protag)
        
        checkbox_row_layout.addWidget(generic_label)
        checkbox_row_layout.addWidget(self.generic)
        
        self.basic_left_layout.addWidget(checkbox_row)
        
        self.working_tab_layout.addWidget(self.basic_left)
        
        stat_label = QLabel("Stats")
        stat_label.setFont(name_font)
        stat_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.basic_center_layout.addWidget(stat_label)
        
        self.stat_row = {}
        self.stat_values = {}
        for s in universal_stats:
            self.stat_row[s] = QWidget()
            stat_row_layout = QHBoxLayout()
            self.stat_row[s].setLayout(stat_row_layout)
            
            stat_row_layout.addWidget(QLabel(s))
            self.stat_values[s] = getattr(self.unit, s)
            stat_value = QSpinBox()
            stat_value.setValue(int(self.stat_values[s]))
            stat_row_layout.addWidget(stat_value)
            
            self.basic_center_layout.addWidget(self.stat_row[s])
        
        self.working_tab_layout.addWidget(self.basic_center)
        
        #name, title, gender, pronouns, friendly/enemy, recruitable, protagonist, mounted, stats, portraits
        
    def initAI(self):
        working_tab = self.tabs_dict["AI"]
        working_tab_layout = working_tab.layout
        
    def initAttacks(self):
        working_tab = self.tabs_dict["Attacks"]
        working_tab_layout = working_tab.layout
        
    def initActions(self):
        working_tab = self.tabs_dict["Actions"]
        working_tab_layout = working_tab.layout
    
    def initClasses(self):
        working_tab = self.tabs_dict["Classes"]
        working_tab_layout = working_tab.layout
        
    def initSkills(self):
        working_tab = self.tabs_dict["Skills"]
        working_tab_layout = working_tab.layout
        
    def initTactics(self):
        working_tab = self.tabs_dict["Tactics"]
        working_tab_layout = working_tab.layout

    def initSkilledBlows(self):
        working_tab = self.tabs_dict["Skilled Blows"]
        working_tab_layout = working_tab.layout
        
    def initObjects(self):
        working_tab = self.tabs_dict["Objects"]
        working_tab_layout = working_tab.layout
    
    def initRelationships(self):
        working_tab = self.tabs_dict["Relationships"]
        working_tab_layout = working_tab.layout