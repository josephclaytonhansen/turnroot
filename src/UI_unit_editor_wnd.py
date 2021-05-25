from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from src.skeletons.weapon_types import weaponTypes
from src.skeletons.unit_class import unitClass
from src.UI_TableModel import TableModel
from src.node_backend import getFiles, File

import json, math, random

import src.UI_colorTheme as UI_colorTheme
from src.UI_updateJSON import updateJSON
data = updateJSON()
active_theme = getattr(UI_colorTheme, data["active_theme"])

from src.skeletons.unit import Unit
from src.skeletons.identities import orientations, genders, pronouns

from src.UI_Dialogs import confirmAction, popupInfo, infoClose
from src.UI_unit_editor_dialogs import growthRateDialog, statBonusDialog, AIHelpDialog, editUniversalStats, editUniversalWeaponTypes, classSkillDialog,loadSavedClass

with open("src/skeletons/universal_stats.json", "r") as stats_file:
    universal_stats =  json.load(stats_file)

GET_FILES = 1
GET_FOLDERS = 0

all_units = {}
team_units = {}
enemy_units = {}
classes = {}

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
        
        self.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: 16")

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
        
        self.tab_names = ["Basic", "AI", "Weapon Affinities", "Actions", "Classes", "Unique Skills/Tactics/Objects", "Relationships", "Graphics/Sounds"]
        
        self.tabs_dict = {}
        for tab in self.tab_names:
            self.tab_title = tab
            self.c_tab = QWidget()
            if tab == "Classes":
                self.c_tab_layout = QGridLayout()
            else:
                self.c_tab_layout = QHBoxLayout()
            self.c_tab.setLayout(self.c_tab_layout)
            self.tabs_dict[tab] = self.c_tab
            self.tabs.addTab(self.c_tab, self.tab_title)
        
        self.initUnit()
        
        self.initBasic()
        self.initAI()
        self.initWeaponAffinities()
        self.initActions()
        self.initClasses()
        self.initUnique()
        self.initRelationships()
        
        self.layout.addWidget(self.tscroll)
        
        self.show()
    
    def initUnit(self):
        #get unit from file
        self.unit = Unit()
        self.unit.unit_class = unitClass()
        
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
        name_font.setPointSize(21)
        
        header_font = self.name_edit.font()
        header_font.setPointSize(21)
        body_font = self.name_edit.font()
        body_font.setPointSize(int(data["font_size"]))
        self.body_font = body_font
        small_font = self.name_edit.font()
        small_font.setPointSize(12)
        
        self.name_edit.setFont(name_font)
        name_row_layout.addWidget(self.name_edit)
        
        self.title_edit = QComboBox()
        self.title_edit.currentTextChanged.connect(self.classChange)
        self.title_edit.setToolTip("Choose from existing classes (edit or create new in the Classes tab)")
        self.title_edit.setFont(body_font)
        name_row_layout.addWidget(self.title_edit)
        
        self.getClassesInFolder()
        
        self.basic_left_layout.addWidget(name_row)
        
        identity_row = QWidget()
        identity_row_layout = QHBoxLayout()
        identity_row.setLayout(identity_row_layout)
        
        self.gender_edit = QComboBox()
        self.gender_edit.currentTextChanged.connect(self.genderChange)
        self.gender_edit.addItems(["Male", "Female", "Non-Binary"])
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
        
        stat_label = QLabel("Stats")
        stat_label.setToolTip("How much of each universal stat unit has at level 1")
        stat_label.setFont(body_font)
        self.basic_center_layout.addWidget(stat_label)
        
        self.stat_row = {}
        self.stat_values = {}
        self.stat_spins = {}
        self.stat_tooltips = [
            "Damage dealt in physical attacks\nActual damage = (strength + weapon damage) minus foe‘s defense",
            "Unit‘s health points",
            "Determines chance of attacking twice, and affects evasion (Avo)\nIf speed minus weapon speed penalty (if enabled for game) is 5 more than foe‘s speed, unit attacks twice. \nEvasion = (.5 x luck) + speed + bonuses",
            "Defense against physical attack\nSee Strength for damage formula",
            "Depending on game settings, this may be ignored, or it may affect tactics‘ durability and ability to learn new tactics/skilled blows\nMay also affect ability to use emplacements",
            "Damage dealt in magical attacks\nActual damage = (magic + weapon damage) minus foe‘s resistance",
            "Defense against magical attack\nSee Magic for damage formula",
            "Affects evasion and critical chance.\nIf class growth is learned, also affects success.\nSee Speed for evasion formula.\nCritical = luck + weapon critical",
            "Affects support building and tactics‘ effectiveness.",
            "Depending on game settings, this may be ignored.\n If enabled, affects weapon speed penalties."
            ]
        
        for s in universal_stats:
            self.stat_row[s] = QWidget()
            self.stat_row[s].setToolTip(self.stat_tooltips[universal_stats.index(s)])
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
        self.column_colors_dict = [[active_theme.unit_editor_rule_0, "black"],
                                   [active_theme.unit_editor_rule_1, "black"],
                                   [active_theme.unit_editor_rule_2, "white"],
                                   [active_theme.unit_editor_rule_3, "white"],
                                   [active_theme.unit_editor_rule_4, "white"],
                                   [active_theme.unit_editor_rule_5, "white"]]
        
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
        soldier_label.setFont(self.body_font)
        lonewolf_label = QLabel("Lone Wolf")
        lonewolf_label.setFont(self.body_font)
        
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
        strategic_label.setFont(self.body_font)
        mindless_label = QLabel("Mindless")
        mindless_label.setFont(self.body_font)
        
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
        cautious_label.setFont(self.body_font)
        brash_label = QLabel("Brash")
        brash_label.setFont(self.body_font)
        
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
        basic_principles.setFont(self.body_font)
        basic_principles.clicked.connect(self.AIOverviewDialog)
        
        detailed_help = QPushButton("Rule Guidelines")
        detailed_help.setFont(self.body_font)
        detailed_help.clicked.connect(self.AIHelpDialog)

        
        rules_row_layout.addWidget(basic_principles)
        rules_row_layout.addWidget(detailed_help)
        
        self.basic_layout.addWidget(rules_row)
        
        default_values_row = QWidget()
        default_values_row_layout = QHBoxLayout()
        default_values_row.setLayout(default_values_row_layout)
        
        self.default_values = QComboBox()
        self.default_values.setFont(self.body_font)
        with open("src/skeletons/sheets/default_slider_values.json", "r") as file:
            self.dv_slider_from_sheet = json.load(file)

        self.solider_lone_wolf_slider.setValue(self.dv_slider_dv[0])
        self.strategic_mindless_slider.setValue(self.dv_slider_dv[1])
        self.cautious_brash_slider.setValue(self.dv_slider_dv[2])
        
        self.default_values.addItems(["--Select--", "Foot Soldier", "Pegasus (Flying) Knight", "Mindless Creature", "Cautious Healer", "Assassin", "Sniper", "Vengeful Demon",
                                      "Strategic Leader", "Armored Tank"])
        default_values_button = QPushButton("Load Preset")
        default_values_button.setFont(self.body_font)
        default_values_button.clicked.connect(self.AILoadSheets)
        
        save_values_button = QPushButton("Save Unit")
        save_values_button.setFont(self.body_font)
        save_values_button.clicked.connect(self.unitToJSON)
        
        default_values_row_layout.addWidget(self.default_values)
        default_values_row_layout.addWidget(default_values_button)
        default_values_row_layout.addWidget(save_values_button)
        
        self.basic_layout.addWidget(default_values_row)

        self.working_tab_layout.addWidget(self.basic_layout_widget)
        
    def initWeaponAffinities(self):
        working_tab = self.tabs_dict["Weapon Affinities"]
        working_tab_layout = working_tab.layout()
        
        self.starting_level_labels = {}
        self.weapon_type_widgets = {}
        self.starting_type_sliders = {}
        self.growth_multipliers_widgets = {}
        growth_multiplier_labels = {}
        
        column = QWidget()
        column_layout = QVBoxLayout()
        column.setLayout(column_layout)
        
        column_inner = QWidget()
        column_inner_layout = QHBoxLayout()
        column_inner.setLayout(column_inner_layout)
        
        for weapon_type in weaponTypes().data:
            weapon_type_widget = QWidget()
            weapon_type_layout  = QVBoxLayout()
            weapon_type_widget.setLayout(weapon_type_layout)
            
            self.weapon_type_widgets[weapon_type] = weapon_type_widget
            
            self.starting_level_labels[weapon_type] = QLabel("D")
            self.starting_level_labels[weapon_type].setFont(self.body_font)
            lab = QLabel("<b>"+weapon_type.upper()+"</b><br>Starting level")
            lab.setFont(self.body_font)
            weapon_type_layout.addWidget(lab)
            weapon_type_layout.addWidget(self.starting_level_labels[weapon_type])
            
            self.starting_type_sliders[weapon_type] = QSlider(Qt.Vertical)
            self.starting_type_sliders[weapon_type].name = weapon_type
            self.starting_type_sliders[weapon_type].valueChanged.connect(self.colorizeSliderC)
            self.starting_type_sliders[weapon_type].valueChanged.connect(self.weapon_starting_level_changed)
            self.starting_type_sliders[weapon_type].setValue(2)
            self.starting_type_sliders[weapon_type].setValue(0)
            self.starting_type_sliders[weapon_type].setRange(0,8)
            self.starting_type_sliders[weapon_type].setSingleStep(1)
            
            weapon_type_layout.addWidget(self.starting_type_sliders[weapon_type])
            
            growth_multiplier_labels[weapon_type] = QLabel("Growth Rate")
            growth_multiplier_labels[weapon_type].setFont(self.body_font)
            weapon_type_layout.addWidget(growth_multiplier_labels[weapon_type])
            
            self.growth_multipliers_widgets[weapon_type] = QDoubleSpinBox()
            self.growth_multipliers_widgets[weapon_type].setFont(self.body_font)
            self.growth_multipliers_widgets[weapon_type].name = weapon_type
            self.growth_multipliers_widgets[weapon_type].setRange(0.5,1.5)
            self.growth_multipliers_widgets[weapon_type].setValue(1.0)
            self.growth_multipliers_widgets[weapon_type].setSingleStep(0.1)
            self.growth_multipliers_widgets[weapon_type].valueChanged.connect(self.growth_multiplier_changed)
            
            weapon_type_layout.addWidget(self.growth_multipliers_widgets[weapon_type])
            
            column_inner_layout.addWidget(weapon_type_widget)
            
        column_layout.addWidget(column_inner)
            
        self.edit_weapon_types = QPushButton("Edit Weapon Types")
        self.edit_weapon_types.setToolTip("Edit universal weapon types. \nCAUTION: This may break existing files.\nDo this first when making a game with new weapon types.")
        self.edit_weapon_types.setFont(self.body_font)
        self.edit_weapon_types.clicked.connect(self.weaponTypesChange)
        column_layout.addWidget(self.edit_weapon_types)
            
        working_tab_layout.addWidget(column)
 
    def initActions(self):
        working_tab = self.tabs_dict["Actions"]
        working_tab_layout = working_tab.layout
    
    def initClasses(self):
        working_tab = self.tabs_dict["Classes"]
        working_tab_layout = working_tab.layout()
        
        working_tab_layout.setSpacing(2)
        
        wt = weaponTypes().data

        self.class_name = QLineEdit()
        self.class_name.setFont(self.body_font)
        self.class_name.setPlaceholderText("Class name")
        self.class_name.setToolTip("Press enter to save class as 'class name.tructf' in game folder.\nOnce a class is named, changes will autosave.")
        self.class_name.returnPressed.connect(self.class_name_change)
        working_tab_layout.addWidget(self.class_name, 0,0,1,1)
        
        self.class_desc = QLineEdit()
        self.class_desc.setFont(self.body_font)
        self.class_desc.setPlaceholderText("Class description")
        self.class_desc.setToolTip("In-game class description.")
        self.class_desc.textChanged.connect(self.class_desc_change)
        working_tab_layout.addWidget(self.class_desc, 0,1,1,2)
        
        self.new_class = QPushButton("New Class")
        self.new_class.setToolTip("Create a new, blank, class (will not save until named)")
        self.new_class.setFont(self.body_font)
        self.new_class.clicked.connect(self.createClass)
        working_tab_layout.addWidget(self.new_class, 0,4,1,2)
        
        self.new_class = QPushButton("Load Class")
        self.new_class.setToolTip("Load a saved class for editing")
        self.new_class.setFont(self.body_font)
        self.new_class.clicked.connect(self.loadClassDialog)
        working_tab_layout.addWidget(self.new_class, 0,3,1,1)

        allowed_weapons_label = QLabel("Can use")
        allowed_weapons_label.setFont(self.body_font)
        working_tab_layout.addWidget(allowed_weapons_label, 1,1,1,1)

        not_allowed_weapons_label = QLabel("Can't use")
        not_allowed_weapons_label.setFont(self.body_font)
        working_tab_layout.addWidget(not_allowed_weapons_label, 1,2,1,1)

        minimum_level_label = QLabel("Minimum level")
        minimum_level_label.setFont(self.body_font)
        working_tab_layout.addWidget(minimum_level_label, 1,3,1,1)
        minimum_level_label.setToolTip("Minimum unit level to have this class.\n If classes reset to level 1, this should be low (10,20), whereas if growth is continous, this can be high (30,40)")

        self.minimum_level = QSpinBox()
        self.minimum_level.setFont(self.body_font)
        self.minimum_level.setRange(0,40)
        self.minimum_level.valueChanged.connect(self.minimum_level_change)
        working_tab_layout.addWidget(self.minimum_level, 1,4,1,1)

        is_mounted_label = QLabel("Mounted?")
        is_mounted_label.setToolTip("If unit is mounted, they gain increased movement.\nTile changes such as stairs can be added with the Tile Changes button.\nUnit will have the option to Dismount/Mount")
        is_mounted_label.setFont(self.body_font)
        working_tab_layout.addWidget(is_mounted_label, 2,3,1,1)

        self.is_mounted = QCheckBox()
        self.is_mounted.stateChanged.connect(self.is_mounted_change)
        working_tab_layout.addWidget(self.is_mounted, 2,4,1,1)

        mounted_m_label = QLabel("Mounted movement+")
        mounted_m_label.setToolTip("How many more tiles are added to movement radius when mounted")
        mounted_m_label.setFont(self.body_font)
        working_tab_layout.addWidget(mounted_m_label, 3,3,1,1)

        self.mounted_m = QSpinBox()
        self.mounted_m.setFont(self.body_font)
        self.mounted_m.setRange(0,10)
        self.mounted_m.valueChanged.connect(self.mounted_m_change)
        working_tab_layout.addWidget(self.mounted_m, 3,4,1,1)

        exp_m_label = QLabel("EXP growth X")
        exp_m_label.setToolTip("How quickly this class levels up.\n Low level classes should have a value higher than 1, advanced classes should be lower.")
        exp_m_label.setFont(self.body_font)
        working_tab_layout.addWidget(exp_m_label, 4,3,1,1)

        self.exp_m = QDoubleSpinBox()
        self.exp_m.setFont(self.body_font)
        self.exp_m.setRange(0.1,2.0)
        self.exp_m.setSingleStep(0.1)
        self.exp_m.valueChanged.connect(self.exp_m_change)
        working_tab_layout.addWidget(self.exp_m, 4,4,1,1)

        class_type_label = QLabel("Item growth type")
        class_type_label.setToolTip("If using items such as seals for class growth, set type needed.\nYou can set these in the Game Editor")
        class_type_label.setFont(self.body_font)
        working_tab_layout.addWidget(class_type_label, 5,3,1,1)

        self.class_type = QComboBox()
        self.class_type.setFont(self.body_font)
        self.class_type.currentTextChanged.connect(self.class_type_change)
        working_tab_layout.addWidget(self.class_type, 5,4,1,1)
        
        is_flying_label = QLabel("Flying?")
        is_flying_label.setToolTip("If unit can fly, they have the same options as a mounted unit (including Movement+), but they are weak to arrows/projectiles")
        is_flying_label.setFont(self.body_font)
        working_tab_layout.addWidget(is_flying_label, 6,3,1,1)

        self.is_flying = QCheckBox()
        self.is_flying.stateChanged.connect(self.is_flying_change)
        working_tab_layout.addWidget(self.is_flying, 6,4,1,1)

        self.tactics = QPushButton("Tactics")
        self.tactics.setToolTip("Tactics are limited use attacks with special effects that can target multiple tiles.\nThis allows Tactics to be class-specific")
        self.tactics.setFont(self.body_font)
        self.tactics.clicked.connect(self.tactics_dialog)
        working_tab_layout.addWidget(self.tactics, len(wt)+2,0,1,1)

        self.skills = QPushButton("Skills")
        self.skills.setToolTip("Skills are unique abilities that incur bonuses or penalties.\nThis allows Skills to be class-specific")
        self.skills.setFont(self.body_font)
        self.skills.clicked.connect(self.skills_dialog)
        working_tab_layout.addWidget(self.skills, len(wt)+2,1,1,1)

        self.skilled_blows = QPushButton("Skilled Blows")
        self.skilled_blows.setToolTip("Skilled Blows are special attacks that use extra weapon durability (\nor, if weapon durability is disabled, have a set number of uses).\nThis allows Skilled Blows to be class-specific")
        self.skilled_blows.setFont(self.body_font)
        self.skilled_blows.clicked.connect(self.skilled_blows_dialog)
        working_tab_layout.addWidget(self.skilled_blows, len(wt)+2,2,1,1)

        self.growth_rates = QPushButton("Growth Rates")
        self.growth_rates.setToolTip("When a unit of this class levels up, their stats increase randomly.\n This allows the \% growth chance to be changed for each stat.")
        self.growth_rates.setFont(self.body_font)
        self.growth_rates.clicked.connect(self.growth_rates_dialog)
        working_tab_layout.addWidget(self.growth_rates, len(wt)+2,3,1,1)

        self.tile_changes = QPushButton("Tile Changes")
        self.tile_changes.setToolTip("If this class interacts with tiles in a unique way, set those rules.\nFor example, a mounted unit will move slowly (or not at all) on stairs.")
        self.tile_changes.setFont(self.body_font)
        self.tile_changes.clicked.connect(self.tile_changes_dialog)
        working_tab_layout.addWidget(self.tile_changes, len(wt)+3,0,1,2)

        self.weak_against = QPushButton("Weakness")
        self.weak_against.setToolTip("Allows for unit weaknesses- for example, armored knights are often weak against magic.\nNote that Flying units already are weak against arrows.")
        self.weak_against.setFont(self.body_font)
        self.weak_against.clicked.connect(self.weak_against_dialog)
        working_tab_layout.addWidget(self.weak_against, len(wt)+3,2,1,2)

        self.stat_bonuses = QPushButton("Stats+")
        self.stat_bonuses.setToolTip("When a unit switches to this class, they can gain a set stat bonus.")
        self.stat_bonuses.setFont(self.body_font)
        self.stat_bonuses.clicked.connect(self.stat_bonuses_dialog)
        working_tab_layout.addWidget(self.stat_bonuses, len(wt)+4,0,1,4)

        self.next_classes = QPushButton("Next Classes")
        self.next_classes.setToolTip("If using Branching Classes, set what classes come after this one.\nOtherwise, this can be ignored.\n(Set Branching Classes in the Game Editor)")
        self.next_classes.setFont(self.body_font)
        self.next_classes.clicked.connect(self.next_classes_dialog)
        working_tab_layout.addWidget(self.next_classes, len(wt)+5,0,1,4)

        self.wt_checkboxes_left = {}
        self.wt_checkboxes_right = {}
        count = 1

        for w in wt:
            count += 1
            self.wt_checkboxes_left[w] = QCheckBox()
            self.wt_checkboxes_left[w].setToolTip("Click to toggle (both for type "+w+" cannot be checked)")
            self.wt_checkboxes_left[w].name = w
            self.wt_checkboxes_left[w].stateChanged.connect(self.left_weapon_type_toggle)
            self.wt_checkboxes_right[w] = QCheckBox()
            self.wt_checkboxes_right[w].name = w
            self.wt_checkboxes_right[w].setToolTip("Click to toggle (both for type "+w+" cannot be checked)")
            self.wt_checkboxes_right[w].setChecked(True)
            self.unit.unit_class.disallowed_weapon_types.append(w)
            self.wt_checkboxes_right[w].stateChanged.connect(self.right_weapon_type_toggle)
            label = QLabel(w)
            label.setFont(self.body_font)
            
            working_tab_layout.addWidget(label, count, 0, 1, 1)
            working_tab_layout.addWidget(self.wt_checkboxes_left[w], count, 1, 1, 1)
            working_tab_layout.addWidget(self.wt_checkboxes_right[w], count, 2, 1, 1)
            
            working_tab_layout.setColumnStretch(0, 3)
            working_tab_layout.setColumnStretch(1, 3)
            working_tab_layout.setColumnStretch(2, 3)
            working_tab_layout.setColumnStretch(3, 3)
            working_tab_layout.setColumnStretch(4, 1)
        
        self.createClass()
       
    def initUnique(self):
        working_tab = self.tabs_dict["Unique Skills/Tactics/Objects"]
        working_tab_layout = working_tab.layout()
        
        columns = QWidget()
        columns_layout = QHBoxLayout()
        columns.setLayout(columns_layout)

        skills_tactics_column = QWidget()
        skills_tactics_layout = QVBoxLayout()
        skills_tactics_column.setLayout(skills_tactics_layout)

        skills_row = QWidget()
        skills_layout = QHBoxLayout()
        skills_row.setLayout(skills_layout)
        skills_tactics_layout.addWidget(skills_row)

        tactics_row = QWidget()
        tactics_layout = QHBoxLayout()
        tactics_row.setLayout(tactics_layout)
        skills_tactics_layout.addWidget(tactics_row)

        objects_column = QWidget()
        objects_layout = QHBoxLayout()
        objects_column.setLayout(objects_layout)

        columns_layout.addWidget(skills_tactics_column)
        columns_layout.addWidget(objects_column)

        working_tab_layout.addWidget(columns)
    
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
        team_member_list_label.setFont(self.body_font)
        
        self.team_member_list = QListWidget()
        self.team_member_list.setFont(self.body_font)
        self.team_member_list.setMinimumWidth(160)
        self.team_member_list.setMaximumWidth(260)
        self.team_member_list.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: "+active_theme.window_background_color)
        self.team_member_list.currentTextChanged.connect(self.team_member_change)
        
        team_supports_list_layout.addWidget(team_member_list_label)
        team_supports_list_layout.addWidget(self.team_member_list)
        
        team_supports_layout.addWidget(team_supports_list)
        
        supports_setup = QWidget()
        supports_setup.setMinimumWidth(400)
        self.supports_setup_layout = QVBoxLayout()
        
        self.relationship_label = QLabel("Relationship with team member")
        self.relationship_label.setFont(self.body_font)
        self.relationship_label.setAlignment(Qt.AlignCenter)
        self.supports_setup_layout.addWidget(self.relationship_label)
        
        self.max_support_level_label = QLabel("Max support level")
        self.max_support_level_label.setFont(self.body_font)
        self.max_support_level_label.setAlignment(Qt.AlignCenter)
        self.supports_setup_layout.addWidget(self.max_support_level_label)
        
        self.max_support_level_widget = QWidget()
        self.max_support_level_widget_layout = QHBoxLayout()
        self.max_support_level_widget.setLayout(self.max_support_level_widget_layout)
        
        self.max_support_level_D = QRadioButton("D")
        self.max_support_level_C = QRadioButton("C")
        self.max_support_level_B = QRadioButton("B")
        self.max_support_level_A = QRadioButton("A")
        self.max_support_level_S = QRadioButton("S")
        
        self.max_support_radio_buttons = [self.max_support_level_D, self.max_support_level_C,
                                          self.max_support_level_B, self.max_support_level_A,
                                          self.max_support_level_S]
        
        
        for rb in self.max_support_radio_buttons:
            rb.clicked.connect(self.max_support_changed)
            rb.setFont(self.body_font)
        
        self.max_support_level_widget_layout.addWidget(self.max_support_level_D)
        self.max_support_level_widget_layout.addWidget(self.max_support_level_C)
        self.max_support_level_widget_layout.addWidget(self.max_support_level_B)
        self.max_support_level_widget_layout.addWidget(self.max_support_level_A)
        self.max_support_level_widget_layout.addWidget(self.max_support_level_S)
        
        self.supports_setup_layout.addWidget(self.max_support_level_widget)
        
        self.support_difficulty_slider = QSlider(Qt.Horizontal)
        self.support_difficulty_slider.setFixedWidth(300)
        self.support_difficulty_slider.valueChanged.connect(self.colorizeSliderB)
        self.support_difficulty_slider.setValue(5)
        self.support_difficulty_slider.setRange(0,10)
        self.support_difficulty_slider.setSingleStep(1)
        
        support_difficulty_widget = QWidget()
        support_difficulty_layout = QHBoxLayout()
        support_difficulty_widget.setLayout(support_difficulty_layout)
        
        hate_label = QLabel("Intensely Dislikes \n(Builds support very slowly)")
        love_label = QLabel("Intensely Likes \n(Builds support very quickly)")
        hate_label.setFont(self.body_font)
        love_label.setFont(self.body_font)
        
        support_difficulty_layout.addWidget(hate_label)
        support_difficulty_layout.addWidget(self.support_difficulty_slider)
        support_difficulty_layout.addWidget(love_label)
        
        self.supports_setup_layout.addWidget(support_difficulty_widget)
        
        self.supports_setup_layout.addSpacerItem(QSpacerItem(1, 200))
        
        spacer_label = QLabel("--------------------------------------------------------------------------------")
        d_color = QColor(active_theme.list_background_color).darker(125).name()

        spacer_label.setStyleSheet("font-size: "+str(data["font_size"])+"px; color: "+str(d_color))
        spacer_label.setAlignment(Qt.AlignCenter)
        self.supports_setup_layout.addWidget(spacer_label)
        
        self.supports_setup_layout.addSpacerItem(QSpacerItem(1, 200))
        
        personal_enemy_widget = QWidget()
        personal_enemy_layout = QHBoxLayout()
        personal_enemy_widget.setLayout(personal_enemy_layout)
        
        self.personal_enemy_label = QLabel("Personal enemy\n--None--")
        self.personal_enemy_label.setFont(self.body_font)
        self.personal_enemy = QListWidget()
        self.personal_enemy.setFont(self.body_font)
        self.personal_enemy.setFixedWidth(300)
        self.personal_enemy.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: "+active_theme.window_background_color)
        self.personal_enemy.currentTextChanged.connect(self.personal_enemy_changed)
        
        personal_enemy_layout.addWidget(self.personal_enemy_label)
        personal_enemy_layout.addWidget(self.personal_enemy)
        
        self.supports_setup_layout.addWidget(personal_enemy_widget)
        
        supports_setup.setLayout(self.supports_setup_layout)
        
        working_tab_layout.addWidget(team_supports)
        working_tab_layout.addWidget(supports_setup)
        
    def genderChange(self, s):
        if s == "Male":
            self.unit.gender = genders().MALE
        elif s == "Female":
            self.unit.gender = genders().FEMALE
        elif s == "Non-Binary":
            self.unit.gender = genders().OTHER
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
            
    def classChange(self, s):
        global classes
        if s != "":
            self.unit.unit_class = classes[s]
            self.loadClass()
    
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
        color_left = QColor(active_theme.unit_editor_slider_color_0)
        color_right = QColor(active_theme.unit_editor_slider_color_1)
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

        else:
            with open(self.path+".trui", "w") as w:
                json.dump(self.unit.AI_sheets, w)
            self.unit.selfToJSON(self.path)

    
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
        
            if self.unit.personal_enemy != None:
                self.personal_enemy_label.setText("Personal enemy\nCurrent: "+self.unit.personal_enemy.name)
            
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
                
            for weapon_type in weaponTypes().data:
                if weapon_type in self.unit.affinities:
                    self.growth_multipliers_widgets[weapon_type].setValue(round(self.unit.affinities[weapon_type],1))
                
                number_to_value = ["D", "D+", "C", "C+", "B", "B+", "A", "A+", "S"]
                
                self.starting_type_sliders[weapon_type].setValue(number_to_value.index(self.unit.current_weapon_levels[weapon_type]))
            
            self.loadClass()
                

    def AIHelpDialog(self):
        a = AIHelpDialog()
        a.exec_()
        
    def getUnitsInFolder(self):
        file_list = getFiles(self.path[0:self.path.rfind("/") + 1])[GET_FILES]
        c = 1000
        all_unit_names = []
        for f in file_list:
            if f.ext.strip() == ".truf":
                c += 10
                tmp_unit = Unit()
                tmp_unit.selfFromJSON(f.fullPath)
                tmp_unit.folder_index = c
                #self.loadFromFile
                if tmp_unit.unique:
                    if tmp_unit.name not in all_units:
                        all_units[tmp_unit.name] = tmp_unit
                        if tmp_unit.name != "":
                            all_unit_names.append(tmp_unit.name)
                        else:
                            all_unit_names.append("NamelessUniqueUnit")
                    
                tmp_unit.selfToJSON(f.fullPath, p = False)
                
        self.team_member_list.clear()
        self.personal_enemy.clear()
        team_units = {}
        enemy_units = {}
                
        for l in all_units:
            if self.unit.name+str(self.unit.folder_index) == all_units[l].name+str(all_units[l].folder_index):
                continue
            if self.unit.is_friendly == all_units[l].is_friendly:
                team_units[l] = all_units[l]
            else:
                enemy_units[l] = all_units[l]
        self.team_member_list.addItems(team_units)
        self.personal_enemy.addItems(enemy_units)

    
    def team_member_change(self, s):
        #selected unit, support_difficulty, max_support_levels
        if s != "":
            self.selected_unit = all_units[s]
            try:
                self.support_difficulty_slider.setValue(self.unit.support_difficulty[self.selected_unit.name])
            except:
                pass
            try:
                for rb in self.max_support_radio_buttons:
                    if rb.text() == self.unit.max_support_levels[self.selected_unit.name]:
                        rb.setChecked()
            except:
                pass

    
    def personal_enemy_changed(self, s):
        if s != "":
            self.unit.personal_enemy = all_units[s]
        if self.path != None:
            self.unit.selfToJSON(self.path)
        
    def max_support_changed(self):
        try:
            self.unit.max_support_levels[self.selected_unit.name] = self.sender().text()
            if self.path != None:
                self.unit.selfToJSON(self.path)
        except:
            pass
    
    def colorizeSliderB(self, v):
        try:
            self.unit.support_difficulty[self.selected_unit.name] = v
            if self.path != None:
                self.unit.selfToJSON(self.path)
        except:
            pass
            
        v = v / 10
        color_left = QColor(active_theme.unit_editor_slider_color_0)
        color_right = QColor(active_theme.unit_editor_slider_color_1)
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
        
    def colorizeSliderC(self, v):
        n = v
        v = v / 9
        color_left = QColor(active_theme.unit_editor_slider_color_0)
        color_right = QColor(active_theme.unit_editor_slider_color_1)
        color_left_c = [color_left.red(), color_left.green(), color_left.blue()]
        color_right_c = [color_right.red(), color_right.green(), color_right.blue()]
        
        distances = [(color_right.red() - color_left.red()),
                     (color_right.green() - color_left.green()),
                     (color_right.blue() - color_left.blue())]
        
        
        new_color = [int(color_left.red() + v * distances[0]),
                     int(color_left.green() + v * distances[1]),
                     int(color_left.blue()+ v * distances[2])]
        
        self.sender().setStyleSheet(
            "QSlider::handle:vertical {\nbackground-color: "+str(QColor(new_color[0],new_color[1],new_color[2]).name())+";border-radius: 2px;width:40px;height:40px;}"
            )
        
        number_to_value = ["D", "D+", "C", "C+", "B", "B+", "A", "A+", "S"]
        self.starting_level_labels[self.sender().name].setText(number_to_value[n])
        self.unit.current_weapon_levels[self.sender().name] = number_to_value[n]
        
        if self.path != None:
            self.unit.selfToJSON(self.path)
        
    def growth_multiplier_changed(self, i):
        self.unit.affinities[self.sender().name] = self.sender().value()
        if self.path != None:
            self.unit.selfToJSON(self.path)
    
    def weapon_starting_level_changed(self):
        pass
    
    def universalStats(self):
        e = editUniversalStats(parent=self)
        e.exec_()
        if e.restart:
            self.parent().parent().restart()

    def weaponTypesChange(self):
        f =editUniversalWeaponTypes(parent=self)
        f.exec_()
        if f.restart:
            self.parent().parent().restart()
    
    def class_name_change(self):
        self.unit.unit_class.unit_class_name = self.class_name.text()
        self.unit.unit_class.selfToJSON("src/skeletons/classes/"+self.class_name.text()+".tructf")
        self.getClassesInFolder()

    def minimum_level_change(self):
        self.unit.unit_class.minimum_level = self.minimum_level.value()
        self.unit.unit_class.selfToJSON("src/skeletons/classes/"+self.class_name.text()+".tructf")

    def is_mounted_change(self):
        self.unit.unit_class.is_mounted = self.is_mounted.isChecked()
        self.unit.unit_class.selfToJSON("src/skeletons/classes/"+self.class_name.text()+".tructf")
        
    def is_flying_change(self):
        self.unit.unit_class.is_flying = self.is_flying.isChecked()
        self.unit.unit_class.selfToJSON("src/skeletons/classes/"+self.class_name.text()+".tructf")

    def mounted_m_change(self):
        self.unit.unit_class.mounted_move_change = self.mounted_m.value()
        self.unit.unit_class.selfToJSON("src/skeletons/classes/"+self.class_name.text()+".tructf")

    def exp_m_change(self):
        self.unit.unit_class.exp_gained_multiplier = self.exp_m.value()
        self.unit.unit_class.selfToJSON("src/skeletons/classes/"+self.class_name.text()+".tructf")

    def class_type_change(self):
        self.unit.unit_class.class_type = self.class_type.value()
        self.unit.unit_class.selfToJSON("src/skeletons/classes/"+self.class_name.text()+".tructf")

    def growth_rates_dialog(self):
        u = growthRateDialog(parent=self,font=self.body_font)
        u.exec_()
        self.unit.unit_class.selfToJSON("src/skeletons/classes/"+self.class_name.text()+".tructf")

    def tile_changes_dialog(self):
        pass

    def weak_against_dialog(self):
        pass

    def stat_bonuses_dialog(self):
        i = statBonusDialog(parent=self,font=self.body_font)
        i.exec_()
        self.unit.unit_class.selfToJSON("src/skeletons/classes/"+self.class_name.text()+".tructf")

    def left_weapon_type_toggle(self):
        w = self.sender().name
        s = self.sender().isChecked()
        if s:
            self.wt_checkboxes_right[w].setChecked(False)
        else:
            self.wt_checkboxes_right[w].setChecked(True)
        if w in self.unit.unit_class.disallowed_weapon_types:
            self.unit.unit_class.disallowed_weapon_types.remove(w)
        self.unit.unit_class.allowed_weapon_types.append(w)
        
        for t in self.unit.unit_class.allowed_weapon_types:
            if t in self.unit.unit_class.disallowed_weapon_types:
                self.unit.unit_class.disallowed_weapon_types.remove(t)

        self.unit.unit_class.selfToJSON("src/skeletons/classes/"+self.class_name.text()+".tructf")
            
    def right_weapon_type_toggle(self):
        w = self.sender().name
        s = self.sender().isChecked()
        if s:
            self.wt_checkboxes_left[w].setChecked(False)
        else:
            self.wt_checkboxes_left[w].setChecked(True)
        if w in self.unit.unit_class.allowed_weapon_types:
            self.unit.unit_class.allowed_weapon_types.remove(w)
        self.unit.unit_class.disallowed_weapon_types.append(w)
        
        for t in self.unit.unit_class.allowed_weapon_types:
            if t in self.unit.unit_class.disallowed_weapon_types:
                self.unit.unit_class.disallowed_weapon_types.remove(t)

        self.unit.unit_class.selfToJSON("src/skeletons/classes/"+self.class_name.text()+".tructf")

    def tactics_dialog(self):
        pass
    
    def skills_dialog(self):
        y = classSkillDialog(parent=self,font=self.body_font)
        y.exec_()
        self.unit.unit_class.selfToJSON("src/skeletons/classes/"+self.class_name.text()+".tructf")

    def skilled_blows_dialog(self):
        pass
    
    def next_classes_dialog(self):
        pass
            
    def getClassesInFolder(self, b = True):
        file_list = getFiles("src/skeletons/classes")[GET_FILES]
        class_names = []
        if hasattr(self.unit, "unit_class_name"):
            tmp_class_name = self.unit.unit_class_name
        global classes
        classes = {}
        self.paths = {}
        self.title_edit.clear()
        for f in file_list:
            if f.ext.strip() == ".tructf":
                tmp_class = unitClass()
                tmp_class.selfFromJSON(f.fullPath)
                self.paths[tmp_class.unit_class_name] = f.fullPath
                class_names.append(tmp_class.unit_class_name)
                classes[tmp_class.unit_class_name] = tmp_class
                
        if b:
            self.classesToDropDown(class_names)
                
    def classesToDropDown(self, class_names):
        self.title_edit.addItems(class_names)
        self.title_edit.update()
        try:
            self.title_edit.setCurrentText(tmp_class_name)
        except:
            pass
    
    def loadClass(self,name = None):
        if name == None:
            ac = self.unit.unit_class
            ac.selfFromJSON(self.paths[ac.unit_class_name])
        else:
            ac = unitClass()
            ac.selfFromJSON(self.paths[name])
        try:
            self.class_name.setText(ac.unit_class_name)
            self.class_desc.setText(ac.desc)
            self.minimum_level.setValue(ac.minimum_level)
            self.is_mounted.setChecked(ac.is_mounted)
            self.mounted_m.setValue(ac.mounted_move_change)
            self.exp_m.setValue(ac.exp_gained_multiplier)
            self.class_type.setCurrentText(ac.class_type)
            self.is_flying.setChecked(ac.is_flying)
            
            for w in weaponTypes().data:
                if w in ac.allowed_weapon_types:
                    self.wt_checkboxes_left[w].setChecked(True)
                elif w in ac.disallowed_weapon_types:
                    self.wt_checkboxes_right[w].setChecked(True)
        except:
            pass
    
    def loadClassDialog(self):
        y = loadSavedClass(parent=self,font=self.body_font)
        y.exec_()
        if hasattr(y,"returns"):
            self.loadClass(name = y.returns)
        else:
            c = infoClose("No class selected")
            c.exec_()

    
    def createClass(self):
        self.unit.unit_class = None
        self.unit.unit_class = unitClass()
        ac = self.unit.unit_class
        
        self.class_name.setText("")
        self.class_desc.setText("")
        self.minimum_level.setValue(0)
        self.is_mounted.setChecked(False)
        self.mounted_m.setValue(0)
        self.exp_m.setValue(0)
        self.class_type.setCurrentText("")
        self.is_flying.setChecked(False)
        
        for w in weaponTypes().data:
            self.wt_checkboxes_left[w].setChecked(False)
            self.wt_checkboxes_right[w].setChecked(True)
    
    def class_desc_change(self):
        self.unit.unit_class.desc = self.sender().text()
        self.unit.unit_class.selfToJSON("src/skeletons/classes/"+self.class_name.text()+".tructf")
        
