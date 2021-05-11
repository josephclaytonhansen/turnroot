from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from src.UI_node_graphics_scene import QDMGraphicsView, QDMGraphicsScene
from src.UI_TableModel import TableModel
from src.node_backend import getFiles, File

import json, math, random

import src.UI_colorTheme as UI_colorTheme
from src.UI_updateJSON import updateJSON
data = updateJSON()
active_theme = getattr(UI_colorTheme, data["active_theme"])

from src.skeletons.unit import Unit
from src.skeletons.identities import orientations, genders, pronouns

from src.UI_Dialogs import confirmAction, popupInfo, infoClose, AIHelpDialog

with open("src/skeletons/universal_stats.json", "r") as stats_file:
    universal_stats =  json.load(stats_file)

GET_FILES = 1
GET_FOLDERS = 0

all_units = {}
team_units = {}
enemy_units = {}

class ValuedSpinBox(QSpinBox):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.index = 0

class UnitEditorWnd(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        
    def initUI(self):
        self.path = None
        
        self.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        
        self.tabs = QTabWidget()
        self.tabs_font = self.tabs.font()
        self.tabs_font.setPointSize(12)
        self.tabs.setFont(self.tabs_font)
        
        self.tabs.setTabPosition(QTabWidget.South)
        
        self.tscroll = QScrollArea()
        self.tscroll.setWidget(self.tabs)
        self.tscroll.setWidgetResizable(True)
        
        self.tab_names = ["Basic", "AI", "Attacks", "Actions", "Classes", "Skills", "Objects", "Relationships", "Graphics/Sounds"]
        
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
        self.basic_left.setMaximumWidth(580)
        
        self.basic_center = QWidget()
        self.basic_center_layout = QVBoxLayout()
        self.basic_center_layout.setSpacing(0)
        self.basic_center.setLayout(self.basic_center_layout)
        self.basic_layout.addWidget(self.basic_center, 60)
        
        image = QPushButton()
        image.setMaximumHeight(390)
        image.setMaximumWidth(285)
        pixmap = QPixmap(270,375)
        pixmap.fill(QColor("white"))
        pixmap = QIcon(pixmap)
        image.setIcon(pixmap)
        image.setIconSize(QSize(270,375))
        image.setToolTip("Edit portraits in the Graphics/Sounds tab")
        
        img_container = QWidget()
        img_container_layout = QHBoxLayout()
        img_container.setLayout(img_container_layout)
        img_container_layout.addWidget(image)
        
        self.basic_left_layout.addWidget(img_container)
        
        name_row = QWidget()
        name_row_layout = QHBoxLayout()
        name_row.setLayout(name_row_layout)
        
        self.name_edit = QLineEdit()
        self.name_edit.returnPressed.connect(self.nameChange)
        self.name_edit.setAlignment(Qt.AlignCenter)
        self.name_edit.setPlaceholderText("Name")
        self.name_edit.setStyleSheet("background-color: "+active_theme.window_background_color+";")
        name_font = self.name_edit.font()
        name_font.setPointSize(16)
        
        header_font = self.name_edit.font()
        header_font.setPointSize(21)
        body_font = self.name_edit.font()
        body_font.setPointSize(16)
        small_font = self.name_edit.font()
        small_font.setPointSize(12)
        
        self.name_edit.setFont(name_font)
        name_row_layout.addWidget(self.name_edit)
        
        self.title_edit = QPushButton()
        self.title_edit.clicked.connect(self.classChange)
        self.title_edit.setText("Soldier")
        self.title_edit.setToolTip("Go to Classes tab")
        self.title_edit.setFont(body_font)
        name_row_layout.addWidget(self.title_edit)
        
        self.basic_left_layout.addWidget(name_row)
        
        identity_row = QWidget()
        identity_row_layout = QHBoxLayout()
        identity_row.setLayout(identity_row_layout)
        
        self.gender_edit = QComboBox()
        self.gender_edit.currentTextChanged.connect(self.genderChange)
        self.gender_edit.addItems(["Male", "Female", "Non-Binary", "Custom"])
        self.gender_edit.setFont(small_font)
        identity_row_layout.addWidget(self.gender_edit)
        
        self.pronouns_edit = QLabel("He/Him/His")
        self.pronouns_edit.setToolTip("Will change based on gender selection")
        self.pronouns_edit.setFont(small_font)
        identity_row_layout.addWidget(self.pronouns_edit)
        
        self.basic_left_layout.addWidget(identity_row)
        
        checkbox_row = QWidget()
        checkbox_row_layout = QHBoxLayout()
        checkbox_row.setLayout(checkbox_row_layout)
        
        protag_label = QLabel("Protagonist")
        self.protag = QCheckBox()
        
        generic_label = QLabel("Generic")
        generic_label.setToolTip("If checked, there can be copies of this unit- i.e., a basic soldier. If unchecked, unit is unique and cannot be copied")
        self.generic = QCheckBox()
        
        checkbox_font = protag_label.font()
        checkbox_font.setPointSize(12)
        protag_label.setFont(checkbox_font)
        self.protag.setFont(checkbox_font)
        generic_label.setFont(checkbox_font)
        self.generic.setFont(checkbox_font)
        
        self.status = QComboBox()
        self.status.currentTextChanged.connect(self.statusChange)
        self.status.addItems(["Enemy", "Team", "Ally", "Protagonist", "Recruitable Enemy", "Recruitable Ally"])
        self.status.setFont(checkbox_font)
        
        checkbox_row_layout.addWidget(generic_label)
        checkbox_row_layout.addWidget(self.generic)
        self.generic.stateChanged.connect(self.genericChange)
        
        self.basic_left_layout.addWidget(checkbox_row)
        
        status_row = QWidget()
        status_row_layout = QHBoxLayout()
        status_row.setLayout(status_row_layout)
        status_row_layout.addWidget(self.status)
        
        self.basic_left_layout.addWidget(status_row)
        
        self.working_tab_layout.addWidget(self.basic_left)
        
        stat_label = QPushButton("Stats")
        stat_label.setToolTip("Edit universal stats")
        stat_label.setFont(body_font)
        self.basic_center_layout.addWidget(stat_label)
        
        self.stat_row = {}
        self.stat_values = {}
        self.stat_spins = {}
        for s in universal_stats:
            self.stat_row[s] = QWidget()
            self.stat_row_layout = QHBoxLayout()
            self.stat_row[s].setLayout(self.stat_row_layout)
            
            stat_label = QLabel(s[0].upper()+s[1:])
            stat_label.setFont(small_font)
            self.stat_row_layout.addWidget(stat_label)
            self.stat_values[s] = getattr(self.unit, s)
            stat_value = ValuedSpinBox()
            self.stat_spins[s] = stat_value
            stat_value.setStyleSheet("background-color: "+active_theme.window_background_color+";")
            stat_value.setRange(0,900)
            stat_value.index = universal_stats.index(s)
            stat_value.valueChanged.connect(self.statChange)
            stat_value.setFont(small_font)
            stat_value.setValue(int(self.stat_values[s]))
            self.stat_row_layout.addWidget(stat_value)
            
            self.basic_center_layout.addWidget(self.stat_row[s])
        
        text_row = QWidget()
        text_row_layout = QHBoxLayout()
        text_row.setLayout(text_row_layout)
        
        notes_column = QWidget()
        notes_column_layout = QVBoxLayout()
        notes_column.setLayout(notes_column_layout)
        
        desc_column = QWidget()
        desc_column_layout = QVBoxLayout()
        desc_column.setLayout(desc_column_layout)
        
        self.notes = QTextEdit()
        self.notes.setStyleSheet("background-color: "+active_theme.window_background_color+";")
        self.notes.textChanged.connect(self.notesChange)
        self.notes.setFont(small_font)
        notes_label = QLabel("Notes")
        notes_label.setToolTip("only seen by you")
        notes_label.setFont(body_font)
        
        self.description = QTextEdit()
        self.description.setStyleSheet("background-color: "+active_theme.window_background_color+";")
        self.description.textChanged.connect(self.descriptionChange)
        self.description.setFont(small_font)
        description_label = QLabel("Description")
        description_label.setToolTip("Added to game")
        description_label.setFont(body_font)
        
        notes_column_layout.addWidget(notes_label)
        notes_column_layout.addWidget(self.notes)
        
        desc_column_layout.addWidget(description_label)
        desc_column_layout.addWidget(self.description)
        
        text_row_layout.addWidget(notes_column)
        text_row_layout.addWidget(desc_column)
        
        self.basic_center_layout.addWidget(text_row)
        
        self.working_tab_layout.addWidget(self.basic_center)
        
        #name, title, gender, pronouns, friendly/enemy, recruitable, protagonist, mounted, stats, portraits
        
    def initAI(self):
        self.sheets = {}
        self.sheetsFromJSON()

        self.working_tab = self.tabs_dict["AI"]
        self.working_tab_layout = self.working_tab.layout()
        
        self.basic_layout = QVBoxLayout()
        self.basic_layout_widget = QWidget()
        self.basic_layout_widget.setLayout(self.basic_layout)
        
        self.tables = {}
        
        #default values- basic foot soldier
        self.table_data = self.sheets["Foot Soldier"]
        self.dv_slider_dv = [15,35,40]
        
        self.basic_table_categories = ["Move Towards", "Move Goals", "Targeting", "Targeting Change", "Avoid", "Tiles"]
        self.column_colors_dict = [["#d4f59e", "black"],
                                   ["#92c47f", "black"],
                                   ["#609480", "white"],
                                   ["#527554", "white"],
                                   ["#334f3d", "white"],
                                   ["##4a5c6d", "white"]]
        
        for t in self.basic_table_categories:
            table = QTableView()
            table_font = QFont("Menlo")
            table_font.setPointSize(14)
            table_font.setStyleHint(QFont.TypeWriter)
            table.setFont(table_font)
            table.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            table.horizontalHeader().setVisible(False)
            table.verticalHeader().setVisible(False)
            self.tables[t] = table
            
            table_data = self.table_data[self.basic_table_categories.index(t)]

            model = TableModel(table_data)
            self.tables[t].setModel(model)
            self.tables[t].model().column_colors = self.column_colors_dict[self.basic_table_categories.index(t)]
        
        personality_slider_row_1 = QWidget()
        personality_slider_row_1_layout = QHBoxLayout()
        personality_slider_row_1.setLayout(personality_slider_row_1_layout)
        
        personality_slider_row_2 = QWidget()
        personality_slider_row_layout_2 = QHBoxLayout()
        personality_slider_row_2.setLayout(personality_slider_row_layout_2)
        
        personality_slider_row_3 = QWidget()
        personality_slider_row_layout_3 = QHBoxLayout()
        personality_slider_row_3.setLayout(personality_slider_row_layout_3)
        
        self.solider_lone_wolf_slider= QSlider(Qt.Horizontal)
        self.solider_lone_wolf_slider.name = 1
        self.solider_lone_wolf_slider.setFixedWidth(750)
        self.solider_lone_wolf_slider.valueChanged.connect(self.colorizeSlider)
        self.solider_lone_wolf_slider.setValue(50)
        self.solider_lone_wolf_slider.setRange(0,100)
        self.solider_lone_wolf_slider.setSingleStep(1)
        
        soldier_label = QLabel("Soldier")
        lonewolf_label = QLabel("Lone Wolf")
        
        personality_slider_row_1_layout.addWidget(soldier_label)
        personality_slider_row_1_layout.addWidget(self.solider_lone_wolf_slider)
        personality_slider_row_1_layout.addWidget(lonewolf_label)
        
        self.strategic_mindless_slider= QSlider(Qt.Horizontal)
        self.strategic_mindless_slider.name = 2
        self.strategic_mindless_slider.setFixedWidth(750)
        self.strategic_mindless_slider.valueChanged.connect(self.colorizeSlider)
        self.strategic_mindless_slider.setValue(50)
        self.strategic_mindless_slider.setRange(0,100)
        self.strategic_mindless_slider.setSingleStep(1)
        
        strategic_label = QLabel("Strategic")
        mindless_label = QLabel("Mindless")
        
        personality_slider_row_layout_2.addWidget(strategic_label)
        personality_slider_row_layout_2.addWidget(self.strategic_mindless_slider)
        personality_slider_row_layout_2.addWidget(mindless_label)
        
        self.cautious_brash_slider= QSlider(Qt.Horizontal)
        self.cautious_brash_slider.name = 3
        self.cautious_brash_slider.setFixedWidth(750)
        self.cautious_brash_slider.valueChanged.connect(self.colorizeSlider)
        self.cautious_brash_slider.setValue(50)
        self.cautious_brash_slider.setRange(0,100)
        self.cautious_brash_slider.setSingleStep(1)
        
        cautious_label = QLabel("Cautious")
        brash_label = QLabel("Brash")
        
        personality_slider_row_layout_3.addWidget(cautious_label)
        personality_slider_row_layout_3.addWidget(self.cautious_brash_slider)
        personality_slider_row_layout_3.addWidget(brash_label)

        self.basic_layout.addWidget(personality_slider_row_1)
        self.basic_layout.addWidget(personality_slider_row_2)
        self.basic_layout.addWidget(personality_slider_row_3)

        basic_table_tabs = QTabWidget()
        
        basic_table_tabs.setFont(self.tabs_font)
        
        basic_table_tabs.setTabPosition(QTabWidget.South)

        for tab in self.basic_table_categories:
            tab_title = tab
            c_tab = self.tables[tab]
            basic_table_tabs.addTab(c_tab, tab_title)
        
        self.basic_layout.addWidget(basic_table_tabs)
        
        rules_row = QWidget()
        rules_row_layout = QHBoxLayout()
        rules_row.setLayout(rules_row_layout)
        
        basic_principles = QPushButton("Overview")
        basic_principles.clicked.connect(self.AIOverviewDialog)
        
        detailed_help = QPushButton("Rule Guidelines")
        detailed_help.clicked.connect(self.AIHelpDialog)

        
        rules_row_layout.addWidget(basic_principles)
        rules_row_layout.addWidget(detailed_help)
        
        self.basic_layout.addWidget(rules_row)
        
        default_values_row = QWidget()
        default_values_row_layout = QHBoxLayout()
        default_values_row.setLayout(default_values_row_layout)
        
        self.default_values = QComboBox()
        with open("src/skeletons/sheets/default_slider_values.json", "r") as file:
            self.dv_slider_from_sheet = json.load(file)

        self.solider_lone_wolf_slider.setValue(self.dv_slider_dv[0])
        self.strategic_mindless_slider.setValue(self.dv_slider_dv[1])
        self.cautious_brash_slider.setValue(self.dv_slider_dv[2])
        
        self.default_values.addItems(["--Select--", "Foot Soldier", "Pegasus (Flying) Knight", "Mindless Creature", "Cautious Healer", "Assassin", "Sniper", "Vengeful Demon",
                                      "Strategic Leader", "Armored Tank"])
        default_values_button = QPushButton("Load Preset")
        default_values_button.clicked.connect(self.AILoadSheets)
        
        save_values_button = QPushButton("Save")
        save_values_button.clicked.connect(self.unitToJSON)
        
        default_values_row_layout.addWidget(self.default_values)
        default_values_row_layout.addWidget(default_values_button)
        default_values_row_layout.addWidget(save_values_button)
        
        self.basic_layout.addWidget(default_values_row)

        self.working_tab_layout.addWidget(self.basic_layout_widget)
        
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
        
    def initObjects(self):
        working_tab = self.tabs_dict["Objects"]
        working_tab_layout = working_tab.layout
    
    def initRelationships(self):
        working_tab = self.tabs_dict["Relationships"]
        working_tab_layout = working_tab.layout()
        
        team_supports = QWidget()
        team_supports_layout = QHBoxLayout()
        team_supports.setLayout(team_supports_layout)
        
        team_supports_list = QWidget()
        team_supports_list_layout = QVBoxLayout()
        team_supports_list.setLayout(team_supports_list_layout)
        
        team_member_list_label = QLabel("Team Members")
        
        self.team_member_list = QListWidget()
        self.team_member_list.setMinimumWidth(160)
        self.team_member_list.setMaximumWidth(260)
        self.team_member_list.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: "+active_theme.window_background_color)
        self.team_member_list.currentTextChanged.connect(self.team_member_change)
        
        team_supports_list_layout.addWidget(team_member_list_label)
        team_supports_list_layout.addWidget(self.team_member_list)
        
        team_supports_layout.addWidget(team_supports_list)
        
        working_tab_layout.addWidget(team_supports)
        
    def genderChange(self, s):
        if s == "Male":
            self.unit.gender = genders().MALE
        elif s == "Female":
            self.unit.gender = genders().FEMALE
        elif s == "Other/Non-Binary":
            self.unit.gender = genders().OTHER
        else:
            #custom gender
            pass
        self.unit.pronoun_string = ""
        for k in (self.unit.pronouns):
            self.unit.pronoun_string += k[0].upper()+k[1:]
            if self.unit.pronouns.index(k) != 2:
                self.unit.pronoun_string += "/"
        try:
            self.pronouns_edit.setText(self.unit.pronoun_string)
        except:
            pass
        
        if self.path != None:
            self.unit.selfToJSON(self.path)
    
    def nameChange(self):
        s = self.sender().text()
        self.unit.name = s
        
        if self.path != None:
            self.unit.selfToJSON(self.path)
            
    def classChange(self):
        pass
    
    def statusChange(self, s):
        if s == "Enemy":
            self.unit.is_friendly = False
        elif s == "Team":
            self.unit.is_friendly = True
            self.has_dialogue = True
        elif s == "Ally":
            self.unit.is_friendly = False
            self.unit.is_ally = True
        elif s == "Protagonist":
            k = confirmAction("#You can only have one!\nThis will clear the existing protagonist.\nContinue?")
            k.exec_()
            if k.return_confirm:
                self.unit.is_friendly = True
                self.unit.is_ally = False
                self.unit.is_lord = True
                #clear other units of lord flag
        elif s == "Recruitable Enemy":
            self.unit.is_friendly = False
            self.unit.is_recruitable = True
        elif s == "Recruitable Ally":
            self.unit.is_friendly = False
            self.unit.is_ally = True
            self.unit.is_recruitable = True
        
        if self.path != None:
            self.unit.selfToJSON(self.path)
            
    def genericChange(self, s):
        if s == 0:
            self.unit.unique = True
        else:
            self.unit.unique = False
            
        if self.path != None:
            self.unit.selfToJSON(self.path)
            
    def statChange(self, i):
        setattr(self.unit,universal_stats[self.sender().index],i)
        
        if self.path != None:
            self.unit.selfToJSON(self.path)
    
    def notesChange(self):
        self.unit.notes=self.notes.toPlainText()
        if self.path != None:
            self.unit.selfToJSON(self.path)
    
    def descriptionChange(self):
        self.unit.description=self.description.toPlainText()
        if self.path != None:
            self.unit.selfToJSON(self.path)      
    
    def colorizeSlider(self, v):
        for tab in self.basic_table_categories:
            c_tab = self.tables[tab]
            if self.sender().name == 1:
                c_tab.model().slider_value1 = v
                self.unit.AI_soldier = v
                self.dv_slider_dv[0] = v
                c_tab.viewport().repaint()
            elif self.sender().name == 2:
                c_tab.model().slider_value2 = v
                self.unit.AI_strategic = v
                self.dv_slider_dv[1] = v
                c_tab.viewport().repaint()
            elif self.sender().name == 3:
                c_tab.model().slider_value3 = v
                self.unit.AI_cautious = v
                self.dv_slider_dv[2] = v
                c_tab.viewport().repaint()
        
        if self.path != None:
            self.unitToJSON()
        
        v = v / 100
        color_left = QColor(active_theme.node_outliner_label_0)
        color_right = QColor(active_theme.node_outliner_label_1)
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
        if self.path != None:
            self.unit.selfToJSON(self.path)
        
    def AIOverviewDialog(self):
        instructions_text = ["\nRule 1 in a set has more weight towards the final decision than 2.\n",
        "\nOrder of Importance: Avoid > Target > Target Change > Movement Goal > Move Towards > Random\n\n",
        "With attributes such as SOLDIER, the more to that side the slider is, the more weight the rule carries.\n",
        "These attributes may mean that rule2 in a set has more weight than rule1, based on slider positions."]
        a = popupInfo(instructions_text[0]+instructions_text[1]+instructions_text[2]+instructions_text[3],self)
        a.exec_()
        
    def AILoadSheets(self, ca=True):
        p = confirmAction("#Your changes will be lost if not saved, continue?")
        p.exec_()
        if p.return_confirm:
            sheet = self.default_values.currentText()
            if sheet != "--Select--":
                self.sheetsFromJSON()
                self.table_data = self.sheets[sheet]
                
                self.dv_slider_dv = self.dv_slider_from_sheet[sheet]
                    
                self.solider_lone_wolf_slider.setValue(self.dv_slider_dv[0])
                self.strategic_mindless_slider.setValue(self.dv_slider_dv[1])
                self.cautious_brash_slider.setValue(self.dv_slider_dv[2])
                
                for t in self.basic_table_categories:
                    
                    table_data = self.table_data[self.basic_table_categories.index(t)]
                    model = TableModel(table_data)
                    self.tables[t].setModel(model)
                    
                    self.tables[t].model().column_colors = self.column_colors_dict[self.basic_table_categories.index(t)]
                
                    self.tables[t].model().slider_value1 = self.solider_lone_wolf_slider.value()
                    self.tables[t].model().slider_value2 = self.strategic_mindless_slider.value()
                    self.tables[t].model().slider_value3 = self.cautious_brash_slider.value()
                    self.tables[t].viewport().repaint()

    def loadSheet(self):
        with open(self.path+".trui", "r") as r:
                self.table_data = json.load(r)
                
        self.dv_slider_dv = self.table_data[len(self.table_data)-1]
                
        self.solider_lone_wolf_slider.setValue(self.dv_slider_dv[0])
        self.strategic_mindless_slider.setValue(self.dv_slider_dv[1])
        self.cautious_brash_slider.setValue(self.dv_slider_dv[2])
            
        for t in self.basic_table_categories:
                
            table_data = self.table_data[self.basic_table_categories.index(t)]
            model = TableModel(table_data)
            self.tables[t].setModel(model)
                
            self.tables[t].model().column_colors = self.column_colors_dict[self.basic_table_categories.index(t)]
            
            self.tables[t].model().slider_value1 = self.solider_lone_wolf_slider.value()
            self.tables[t].model().slider_value2 = self.strategic_mindless_slider.value()
            self.tables[t].model().slider_value3 = self.cautious_brash_slider.value()
            self.tables[t].viewport().repaint()

    def sheetsFromJSON(self):
        with open("src/skeletons/sheets/basic_foot_soldier.json", "r") as rf:
            self.sheets["Foot Soldier"] = json.load(rf)
        with open("src/skeletons/sheets/basic_pegasus_knight.json", "r") as rf:
            self.sheets["Pegasus (Flying) Knight"] = json.load(rf)
        with open("src/skeletons/sheets/basic_mindless_creature.json", "r") as rf:
            self.sheets["Mindless Creature"] = json.load(rf)
        with open("src/skeletons/sheets/basic_healer.json", "r") as rf:
            self.sheets["Cautious Healer"] = json.load(rf)
        with open("src/skeletons/sheets/basic_assassin.json", "r") as rf:
            self.sheets["Assassin"] = json.load(rf)
        with open("src/skeletons/sheets/basic_ranged_fighter.json", "r") as rf:
            self.sheets["Sniper"] = json.load(rf)
        with open("src/skeletons/sheets/basic_wrath_fighter.json", "r") as rf:
            self.sheets["Vengeful Demon"] = json.load(rf)
        with open("src/skeletons/sheets/basic_leader.json", "r") as rf:
            self.sheets["Strategic Leader"] = json.load(rf)
        with open("src/skeletons/sheets/basic_tank.json", "r") as rf:
            self.sheets["Armored Tank"] = json.load(rf)
            
    def saveFileDialog(self):
        q = QFileDialog(self)
        options = q.Options()
        options |= q.DontUseNativeDialog
        fileName, _ = q.getSaveFileName(None,"Save","","Turnroot Unit (*.truf)", options=options)
        if fileName:
            self.path = fileName+".truf"
            g = infoClose("Saved unit as "+self.path+"\nAll changes to this unit will now autosave")
            g.exec_()
            
    def unitToJSON(self):
        self.unit.AI_sheets = self.table_data
        if self.unit.AI_sheets[len(self.unit.AI_sheets)-1] == (self.dv_slider_dv):
            pass
        else:
            self.unit.AI_sheets.append(self.dv_slider_dv)

        if self.path == None or self.path == '':
            self.saveFileDialog()
            if self.path == None or self.path == '':
                c = infoClose("No file selected")
                c.exec_()
            else:
                with open(self.path+".trui", "w") as w:
                    json.dump(self.unit.AI_sheets, w)
                self.unit.parent = self
                self.unit.selfToJSON(self.path)
                self.parent().nameChange()

        else:
            with open(self.path+".trui", "w") as w:
                json.dump(self.unit.AI_sheets, w)
            self.unit.selfToJSON(self.path)
            self.parent().nameChange()

    
    def openFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None,"Open", "","Turnroot Unit File (*.truf)", options=options)
        if fileName:
            self.path = fileName

    def loadFromFile(self, p=True):
        self.openFileDialog()
        if self.path == None:
            c = infoClose("No file selected")
            c.exec_()
        else:
            self.unit.selfFromJSON(self.path)
            self.unit.parent = self
            #update graphics
            self.name_edit.setText(self.unit.name)

            if self.unit.gender == genders().MALE:
                self.gender_edit.setCurrentText("Male")
            elif self.unit.gender == genders().FEMALE:
                self.gender_edit.setCurrentText("Female")
            elif self.unit.gender == genders().OTHER:
                self.gender_edit.setCurrentText("Non-Binary")
            
            if self.unit.is_lord:
                self.protag.setCheckState(2)
            
            if self.unit.unique != True:
                self.generic.setCheckState(2)
            
            for s in universal_stats:
                self.stat_spins[s].setValue(getattr(self.unit,s))
            
            self.notes.setPlainText(self.unit.notes)
            
            self.description.setPlainText(self.unit.description)
            
            self.loadSheet()
            
            if self.unit.is_friendly == False and self.unit.is_recruitable == False and self.unit.is_ally == False:
                self.status.setCurrentText("Enemy")
            elif self.unit.is_friendly == False and self.unit.is_recruitable == True and self.unit.is_ally == False:
                self.status.setCurrentText("Recruitable Enemy")
            elif self.unit.is_friendly == False and self.unit.is_recruitable == True and self.unit.is_ally == True:
                self.status.setCurrentText("Recruitable Ally")
            elif self.unit.is_friendly == False and self.unit.is_recruitable == False and self.unit.is_ally == True:
                self.status.setCurrentText("Ally")
            elif self.unit.is_friendly == True and self.unit.is_lord == False and self.unit.has_dialogue == True:
                self.status.setCurrentText("Team")
            else:
                self.status.setCurrentText("Protagonist")

    def AIHelpDialog(self):
        a = AIHelpDialog()
        a.exec_()
        
    def getUnitsInFolder(self):
        file_list = getFiles(self.path[0:self.path.rfind("/") + 1])[GET_FILES]
        c = 0
        all_unit_names = []
        for f in file_list:
            if f.ext.strip() == ".truf":
                c += 100
                tmp_unit = Unit()
                tmp_unit.selfFromJSON(f.fullPath)
                tmp_unit.folder_index = c
                #self.loadFromFile
                if tmp_unit.unique:
                    if tmp_unit.name+"."+str(c) not in all_units:
                        all_units[tmp_unit.name+"."+str(c)] = tmp_unit
                        if tmp_unit.name != "":
                            all_unit_names.append(tmp_unit.name)
                        else:
                            all_unit_names.append("NamelessUniqueUnit"+str(c))
                tmp_unit.selfToJSON(f.fullPath, p = False)
                
        self.team_member_list.clear()
        team_units = {}
                
        for l in all_units:
            if self.unit.is_friendly == all_units[l].is_friendly:
                team_units[l] = all_units[l]
            else:
                enemy_units[l] = all_units[l]
        self.team_member_list.addItems(team_units)

    
    def team_member_change(self):
        pass


        