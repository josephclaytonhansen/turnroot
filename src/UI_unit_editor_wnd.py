from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from src.UI_node_graphics_scene import QDMGraphicsView, QDMGraphicsScene
from src.UI_TableModel import TableModel

import json, math

import src.UI_colorTheme as UI_colorTheme
from src.UI_updateJSON import updateJSON
data = updateJSON()
active_theme = getattr(UI_colorTheme, data["active_theme"])

from src.skeletons.unit import Unit
from src.skeletons.identities import orientations, genders, pronouns

from src.UI_Dialogs import confirmAction

with open("src/skeletons/universal_stats.json", "r") as stats_file:
    universal_stats =  json.load(stats_file)

class ValuedSpinBox(QSpinBox):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.index = 0

class UnitEditorWnd(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        
    def initUI(self):
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
        self.name_edit.textChanged.connect(self.nameChange)
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
        self.gender_edit.addItems(["Male", "Female", "Other/Non-Binary", "Custom"])
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
        for s in universal_stats:
            self.stat_row[s] = QWidget()
            self.stat_row_layout = QHBoxLayout()
            self.stat_row[s].setLayout(self.stat_row_layout)
            
            stat_label = QLabel(s[0].upper()+s[1:])
            stat_label.setFont(small_font)
            self.stat_row_layout.addWidget(stat_label)
            self.stat_values[s] = getattr(self.unit, s)
            stat_value = ValuedSpinBox()
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
        self.working_tab = self.tabs_dict["AI"]
        self.working_tab_layout = self.working_tab.layout()
        
        self.basic_layout = QVBoxLayout()
        self.basic_layout_widget = QWidget()
        self.basic_layout_widget.setLayout(self.basic_layout)
        
        self.table = QTableView()
        table_font = QFont("Menlo")
        table_font.setStyleHint(QFont.TypeWriter)
        self.table.setFont(table_font)
        self.table.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.table_data = [
            ["move_towards1","player or ally IS nearest","!"],
["move_towards2","player or ally IS disadvantage","STRATEGIC"],
["move_towards3","IS safe","COWARDLY"],
["move_towards4","chest IF self can open","GREED+LONE_WOLF"],
            ["","",""],
["move_goals1","self IS in group: stay in group","SOLDIER"],
["move_goals2","",""],
            ["","",""],
["target1","player or ally IS last","SOLDIER"],
["target2","player or ally IS disadvantage","STRATEGIC"],
["target3","player or ally IS leader","BRASH"],
["target4","player or ally IS nearest","MINDLESS"],
            ["","",""],
["target_change1","possible_target IS disadvantage","STRATEGIC"],
["target_change2","last_target IS NOT in vision","!"],
            ["","",""],
["avoid1","doors IF shut",""],
["avoid2","IS stop","!"],
["avoid3","space IS emplacement",""],
["avoid4","self IS alone in vision","SOLDIER"],
["avoid5","space IS hurt",""],
["avoid6","space IS last position",""],
["avoid7","IS slow ","STRATEGIC"]
            ]

        self.model = TableModel(self.table_data)
        self.table.setModel(self.model)
        
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
        self.strategic_mindless_slider.valueChanged.connect(self.colorizeSlider)
        self.strategic_mindless_slider.setValue(50)
        self.strategic_mindless_slider.setRange(0,100)
        self.strategic_mindless_slider.setSingleStep(1)
        
        strategic_label = QLabel("Strategic")
        mindless_label = QLabel("Mindless")
        
        personality_slider_row_layout_2.addWidget(strategic_label)
        personality_slider_row_layout_2.addWidget(self.strategic_mindless_slider)
        personality_slider_row_layout_2.addWidget(mindless_label)
        
        self.cowardly_brash_slider= QSlider(Qt.Horizontal)
        self.cowardly_brash_slider.valueChanged.connect(self.colorizeSlider)
        self.cowardly_brash_slider.setValue(50)
        self.cowardly_brash_slider.setRange(0,100)
        self.cowardly_brash_slider.setSingleStep(1)
        
        cowardly_label = QLabel("Cowardly")
        brash_label = QLabel("Brash")
        
        personality_slider_row_layout_3.addWidget(cowardly_label)
        personality_slider_row_layout_3.addWidget(self.cowardly_brash_slider)
        personality_slider_row_layout_3.addWidget(brash_label)

        self.basic_layout.addWidget(personality_slider_row_1)
        self.basic_layout.addWidget(personality_slider_row_2)
        self.basic_layout.addWidget(personality_slider_row_3)

        
        self.basic_layout.addWidget(self.table)

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
        working_tab_layout = working_tab.layout
        
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
    
    def nameChange(self,s):
        self.unit.name = s
        
        self.unit.selfToJSON()
            
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
            
        self.unit.selfToJSON()
            
    def genericChange(self, s):
        if s == 0:
            self.unit.unique = False
        else:
            self.unit.unique = True
            
        self.unit.selfToJSON()
            
    def statChange(self, i):
        setattr(self.unit,universal_stats[self.sender().index],i)
        
        self.unit.selfToJSON()
    
    def notesChange(self):
        self.unit.notes=self.notes.toPlainText()
        self.unit.selfToJSON()
    
    def descriptionChange(self):
        self.unit.description=self.description.toPlainText()
        self.unit.selfToJSON()
    
    def colorizeSlider(self, v):
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
        
        self.sender().setStyleSheet("QSlider::handle:horizontal {\nbackground-color: "+str(QColor(new_color[0],new_color[1],new_color[2]).name())+";border-radius: 2px;}")