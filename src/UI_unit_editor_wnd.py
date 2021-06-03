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
from src.UI_unit_editor_dialogs import (growthRateDialog, statBonusDialog, AIHelpDialog, editUniversalStats,
                                        classSkillDialog, loadSavedClass,
                                        instanceStatDialog, tileChangesDialog, unitGrowthRateDialog,
                                        classCriteriaDialog)
from src.UI_unit_editor_more_dialogs import (weakAgainstDialog, expTypesDialog, nextClassesDialog,
                                             classGraphicDialog,editUniversalWeaponTypes)

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
        
        self.setStyleSheet("background-color: "+active_theme.window_background_color+"; color:"+active_theme.window_text_color+"; font-size: 16")

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
        self.tts = ["Edit unit identity, stats, and test growth rates", "Edit unit behavior when controlled by computer",
                    "Edit unit weapon growth and experience. Also edit universal weapon types",
                    "Edit unit actions such as rallying, mounting/dismounting, and summoning", "Create and edit classes",
                    "Assign unique skills/tactics/objects to a unit", "Define how this unit interacts with teammates and set personal enemy",
                    "Customize unit graphics and sounds"]
        
        self.tabs_dict = {}
        for tab in self.tab_names:
            self.tab_title = tab
            self.c_tab = QWidget()
            self.c_tab.setToolTip(self.tts[self.tab_names.index(tab)])
            if tab == "Classes":
                self.c_tab_layout = QGridLayout()
            else:
                self.c_tab_layout = QHBoxLayout()
            self.c_tab.setLayout(self.c_tab_layout)
            self.tabs_dict[tab] = self.c_tab
            self.tabs.addTab(self.c_tab, self.tab_title)
        
        self.tabs.currentChanged.connect(self.ctab_changed)
        
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
        self.name_edit.setToolTip("Change unit name.\nIf unit is Generic, name should also be generic.\nProtagonist name is the default if player doesn't change it.")
        self.name_edit.setStyleSheet("background-color: "+active_theme.list_background_color+";")
        name_font = self.name_edit.font()
        name_font.setPointSize(21)
        
        header_font = self.name_edit.font()
        header_font.setPointSize(18)
        body_font = self.name_edit.font()
        body_font.setPointSize(int(data["font_size"]))
        self.body_font = body_font
        small_font = self.name_edit.font()
        small_font.setPointSize(12)
        
        self.name_edit.setFont(name_font)
        name_row_layout.addWidget(self.name_edit)
        
        self.title_edit = QComboBox()
        self.title_edit.currentTextChanged.connect(self.classChange)
        self.title_edit.setToolTip("Choose assigned class from existing classes (edit or create new in the Classes tab)")
        self.title_edit.setFont(header_font)
        name_row_layout.addWidget(self.title_edit)
        
        self.getClassesInFolder()
        
        self.basic_left_layout.addWidget(name_row)
        
        identity_row = QWidget()
        identity_row_layout = QHBoxLayout()
        identity_row.setLayout(identity_row_layout)
        
        self.gender_edit = QComboBox()
        self.gender_edit.setToolTip("Set unit gender. This will also change pronouns for dialogue")
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
        protag_label.setToolTip("The protagonist, or avatar, is the unit that stands in for the player.\nIf protagonist is enabled in game settings, player can customize this unit")
        self.protag = QCheckBox()
        
        self.generic_label = QPushButton("Generic")
        self.generic_label.setToolTip("If checked, there can be instances of this unit- i.e., a basic soldier.\n If unchecked, unit is unique and cannot be instanced\nClick to edit instance randomness")
        self.generic_label.clicked.connect(self.instance_stat_edit)
        self.generic_label.setEnabled(False)
        self.generic = QCheckBox()
        
        checkbox_font = protag_label.font()
        checkbox_font.setPointSize(12)
        protag_label.setFont(checkbox_font)
        self.protag.setFont(checkbox_font)
        self.generic_label.setFont(checkbox_font)
        self.generic.setFont(checkbox_font)
        
        self.status = QComboBox()
        self.status.setToolTip("Change status. You can only have one protagonist.\nEnemies and Allies can be generic, Recruitable Enemies/Allies or Team members cannot")
        self.status.currentTextChanged.connect(self.statusChange)
        self.status.addItems(["Enemy", "Team", "Ally", "Protagonist", "Recruitable Enemy", "Recruitable Ally"])
        self.status.setFont(checkbox_font)
        
        checkbox_row_layout.addWidget(self.generic_label)
        checkbox_row_layout.addWidget(self.generic)
        self.generic.stateChanged.connect(self.genericChange)
        
        self.basic_left_layout.addWidget(checkbox_row)
        
        status_row = QWidget()
        status_row_layout = QHBoxLayout()
        status_row.setLayout(status_row_layout)
        status_row_layout.addWidget(self.status)
        
        self.basic_left_layout.addWidget(status_row)
        
        self.working_tab_layout.addWidget(self.basic_left)
        
        stats_header_growth = QWidget()
        shg_layout = QHBoxLayout()
        stats_header_growth.setLayout(shg_layout)
        
        stat_label = QLabel("Base Stats")
        stat_label.setToolTip("How much of each universal stat unit has at level 1\nStat growth rate = (unit growth rate + class growth rate / 2)")
        stat_label.setFont(header_font)
        
        growth_rates = QPushButton("Stat Growth Rates")
        growth_rates.clicked.connect(self.unit_growth_rates_dialog)
        growth_rates.setToolTip("Set natural affinity for different stats.\nYou can also test growth rates here.\nIf growth chance for Strength for a unit is 60, and the class growth rate is 80, the actual growth rate is 70")
        growth_rates.setFont(self.body_font)
        
        shg_layout.addWidget(stat_label)
        shg_layout.addWidget(growth_rates)
        
        self.basic_center_layout.addWidget(stats_header_growth)
        
        self.stat_row = {}
        self.stat_values = {}
        self.stat_spins = {}
        self.stat_tooltips = [
            "Damage dealt in physical attacks\nActual damage = (strength + weapon damage) minus foe‘s defense",
            "Unit‘s health points",
            "Determines chance of attacking twice, and affects evasion (Avo)\nIf speed minus weapon speed penalty (if enabled for game) is 5 more than foe‘s speed, unit attacks twice. \nEvasion = (luck + dexterity) / 2 + speed",
            "Defense against physical attack\nSee Strength for damage formula",
            "Depending on game settings, this may be ignored, or it may affect tactics‘ durability and ability to learn new tactics/skilled blows\nMay also affect ability to use emplacements",
            "Damage dealt in magical attacks\nActual damage = (magic + weapon damage) minus foe‘s resistance",
            "Defense against magical attack\nSee Magic for damage formula",
            "Affects evasion and critical chance.\nIf class growth is learned, also affects success.\nSee Speed for evasion formula.\nCritical = luck + weapon critical",
            "Affects support building and tactics‘ effectiveness.",
            "Depending on game settings, this may be ignored.\n If enabled, affects weapon speed penalties.",
            "Affects evasion and weapon hit chance.\nSee Speed for evasion formula.\nHit chance = dexterity + weapon hit"
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
            stat_value.setStyleSheet("background-color: "+active_theme.list_background_color+";")
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
        self.notes.setStyleSheet("background-color: "+active_theme.list_background_color+";")
        self.notes.textChanged.connect(self.notesChange)
        self.notes.setFont(small_font)
        notes_label = QLabel("Notes")
        notes_label.setToolTip("only seen by you")
        notes_label.setFont(header_font)
        
        self.description = QTextEdit()
        self.description.setStyleSheet("background-color: "+active_theme.list_background_color+";")
        self.description.textChanged.connect(self.descriptionChange)
        self.description.setFont(small_font)
        description_label = QLabel("Description")
        description_label.setToolTip("Added to game")
        description_label.setFont(header_font)
        
        notes_column_layout.addWidget(notes_label)
        notes_column_layout.addWidget(self.notes)
        
        desc_column_layout.addWidget(description_label)
        desc_column_layout.addWidget(self.description)
        
        text_row_layout.addWidget(notes_column)
        text_row_layout.addWidget(desc_column)
        
        self.basic_center_layout.addWidget(text_row)
        
        self.working_tab_layout.addWidget(self.basic_center)
        self.generic_label.setEnabled(False)
        
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
            c_tab.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
            basic_table_tabs.addTab(c_tab, tab_title)
        
        self.basic_layout.addWidget(basic_table_tabs)
        
        rules_row = QWidget()
        rules_row_layout = QHBoxLayout()
        rules_row.setLayout(rules_row_layout)
        
        basic_principles = QPushButton("Overview")
        basic_principles.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
        basic_principles.setFont(self.body_font)
        basic_principles.clicked.connect(self.AIOverviewDialog)
        
        detailed_help = QPushButton("Rule Guidelines")
        detailed_help.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
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
        self.default_values.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
        default_values_button = QPushButton("Load Preset")
        default_values_button.setStyleSheet("background-color: "+active_theme.button_alt_color+"; color:"+active_theme.button_alt_text_color+"; font-size: "+str(data["font_size"]))
        default_values_button.setFont(self.body_font)
        default_values_button.clicked.connect(self.AILoadSheets)
        
        default_values_row_layout.addWidget(self.default_values)
        default_values_row_layout.addWidget(default_values_button)
        
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
        
        self.wascroll = QScrollArea()
        self.wascroll.setWidgetResizable(True)
        working_tab_layout.addWidget(self.wascroll)
        
        column = QWidget()
        column_layout = QVBoxLayout()
        column.setLayout(column_layout)
        
        column_inner = QWidget()
        column_inner.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
        column_inner_layout = QHBoxLayout()
        column_inner.setLayout(column_inner_layout)
        
        for weapon_type in weaponTypes().data:
            weapon_type_widget = QWidget()
            weapon_type_layout  = QVBoxLayout()
            weapon_type_widget.setLayout(weapon_type_layout)
            
            self.weapon_type_widgets[weapon_type] = weapon_type_widget
            
            self.starting_level_labels[weapon_type] = QLabel("D")
            self.starting_level_labels[weapon_type].setToolTip("At level one, unit's proficiency with weapon")
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
            self.starting_type_sliders[weapon_type].setRange(0,10)
            self.starting_type_sliders[weapon_type].setSingleStep(1)
            
            weapon_type_layout.addWidget(self.starting_type_sliders[weapon_type])
            
            growth_multiplier_labels[weapon_type] = QLabel("Growth Rate")
            growth_multiplier_labels[weapon_type].setFont(self.body_font)
            growth_multiplier_labels[weapon_type].setToolTip("How quickly/slowly unit gains weapon experience.\nFor instance, values less than 1 are a weakness- unit will learn slowly.")
            weapon_type_layout.addWidget(growth_multiplier_labels[weapon_type])
            
            self.growth_multipliers_widgets[weapon_type] = QDoubleSpinBox()
            self.growth_multipliers_widgets[weapon_type].setFont(self.body_font)
            self.growth_multipliers_widgets[weapon_type].name = weapon_type
            self.growth_multipliers_widgets[weapon_type].setRange(0.5,2)
            self.growth_multipliers_widgets[weapon_type].setValue(1.0)
            self.growth_multipliers_widgets[weapon_type].setSingleStep(0.1)
            self.growth_multipliers_widgets[weapon_type].valueChanged.connect(self.growth_multiplier_changed)
            
            weapon_type_layout.addWidget(self.growth_multipliers_widgets[weapon_type])
            
            column_inner_layout.addWidget(weapon_type_widget)
            
        column_layout.addWidget(column_inner)
            
        self.edit_weapon_types = QPushButton("Edit Weapon Types")
        self.edit_weapon_types.setToolTip("Edit universal weapon types.")
        self.edit_weapon_types.setFont(self.body_font)
        self.edit_weapon_types.clicked.connect(self.weaponTypesChange)
        column_layout.addWidget(self.edit_weapon_types)
            
        self.wascroll.setWidget(column)
 
    def initActions(self):
        working_tab = self.tabs_dict["Actions"]
        working_tab_layout = working_tab.layout
    
    def initClasses(self):
        self.loaded_class = unitClass()
        self.d_tile_changes = {}
        self.m_tile_changes = {}
        working_tab = self.tabs_dict["Classes"]
        working_tab_layout = working_tab.layout()
        
        working_tab_layout.setContentsMargins(20,20,20,20)
        working_tab_layout.setSpacing(2)
        
        wt = weaponTypes().data
        lenwt = len(wt)
        if lenwt < 10:
            lenwt = 10

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
        working_tab_layout.addWidget(self.class_desc, 0,1,1,1)
        
        self.new_class = QPushButton("New Class")
        self.new_class.setStyleSheet("background-color: "+active_theme.button_alt_color+"; color:"+active_theme.button_alt_text_color+"; font-size: "+str(data["font_size"]))
        self.new_class.setToolTip("Create a new, blank, class (will not save until named)")
        self.new_class.setFont(self.body_font)
        self.new_class.clicked.connect(self.createClass)
        working_tab_layout.addWidget(self.new_class, 0,3,1,1)
        
        self.load_class = QPushButton("Load Class")
        self.load_class.setToolTip("Load a saved class for editing")
        self.load_class.setFont(self.body_font)
        self.load_class.setStyleSheet("background-color: "+active_theme.button_alt_color+"; color:"+active_theme.button_alt_text_color+"; font-size: "+str(data["font_size"]))
        self.load_class.clicked.connect(self.loadClassDialog)
        working_tab_layout.addWidget(self.load_class, 0,2,1,1)

        allowed_weapons_label = QLabel("Can use")
        allowed_weapons_label.setFont(self.body_font)
        working_tab_layout.addWidget(allowed_weapons_label, 1,1,1,1)

        minimum_level_label = QLabel("Minimum level")
        minimum_level_label.setFont(self.body_font)
        working_tab_layout.addWidget(minimum_level_label, 1,2,1,1)
        minimum_level_label.setToolTip("Minimum unit level to have this class.\n If classes are criteria based, set this to 0.\nCriteria vs Level can be set in the Game Editor")

        self.minimum_level = QSpinBox()
        self.minimum_level.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
        self.minimum_level.setFont(self.body_font)
        self.minimum_level.setRange(0,40)
        self.minimum_level.valueChanged.connect(self.minimum_level_change)
        working_tab_layout.addWidget(self.minimum_level, 1,3,1,1)

        is_mounted_label = QLabel("Mounted?")
        is_mounted_label.setToolTip("If unit is mounted, they gain increased movement.\nTile changes such as stairs can be added with the Tile Changes button.\nUnit will have the option to Dismount/Mount")
        is_mounted_label.setFont(self.body_font)
        working_tab_layout.addWidget(is_mounted_label, 2,2,1,1)

        self.is_mounted = QCheckBox()
        self.is_mounted.stateChanged.connect(self.is_mounted_change)
        working_tab_layout.addWidget(self.is_mounted, 2,3,1,1)

        mounted_m_label = QLabel("Mounted movement+")
        mounted_m_label.setToolTip("How many more tiles are added to movement radius when mounted")
        mounted_m_label.setFont(self.body_font)
        working_tab_layout.addWidget(mounted_m_label, 3,2,1,1)

        self.mounted_m = QSpinBox()
        self.mounted_m.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
        self.mounted_m.setFont(self.body_font)
        self.mounted_m.setRange(0,10)
        self.mounted_m.valueChanged.connect(self.mounted_m_change)
        working_tab_layout.addWidget(self.mounted_m, 3,3,1,1)

        exp_m_label = QLabel("EXP growth X")
        exp_m_label.setToolTip("How quickly this class levels up.\n Low level classes should have a value higher than 1, advanced classes should be lower.")
        exp_m_label.setFont(self.body_font)
        working_tab_layout.addWidget(exp_m_label, 4,2,1,1)

        self.exp_m = QDoubleSpinBox()
        self.exp_m.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
        self.exp_m.setFont(self.body_font)
        self.exp_m.setRange(0.1,3.0)
        self.exp_m.setSingleStep(0.1)
        self.exp_m.setValue(1.25)
        self.exp_m.valueChanged.connect(self.exp_m_change)
        working_tab_layout.addWidget(self.exp_m, 4,3,1,1)

        class_type_label = QLabel("Item growth type")
        class_type_label.setToolTip("If using items such as seals for class growth, set type needed.\nYou can set these in the Game Editor")
        class_type_label.setFont(self.body_font)
        working_tab_layout.addWidget(class_type_label, 5,2,1,1)

        self.class_type = QComboBox()
        self.class_type.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
        self.class_type.setFont(self.body_font)
        self.class_type.currentTextChanged.connect(self.class_type_change)
        working_tab_layout.addWidget(self.class_type, 5,3,1,1)
        
        is_flying_label = QLabel("Flying?")
        is_flying_label.setToolTip("If unit can fly, they have the same options as a mounted unit (including Movement+), but they are weak to arrows/projectiles")
        is_flying_label.setFont(self.body_font)
        working_tab_layout.addWidget(is_flying_label, 6,2,1,1)

        self.is_flying = QCheckBox()
        self.is_flying.stateChanged.connect(self.is_flying_change)
        working_tab_layout.addWidget(self.is_flying, 6,3,1,1)
        
        is_unique_label = QLabel("Unique to unit?")
        is_unique_label.setToolTip("If class is unique to unit, minimum level/criteria will be ignored\nIf a unit has a unique class set (from the drop-down on the Basic tab), unit will start with that class")
        is_unique_label.setFont(self.body_font)
        working_tab_layout.addWidget(is_unique_label, 7,2,1,1)

        self.is_unique = QCheckBox()
        self.is_unique.stateChanged.connect(self.is_unique_change)
        working_tab_layout.addWidget(self.is_unique, 7,3,1,1)
        
        is_visible_label = QLabel("Secret class?")
        is_visible_label.setToolTip("If class is secret, it can't be normally achieved (level/criteria), nor will it show up in class grid (if using).\nA secret class is given through a game event.\nFor example, a Lord could become a Great Lord at the right time.")
        is_visible_label.setFont(self.body_font)
        working_tab_layout.addWidget(is_visible_label, 8,2,1,1)

        self.is_visible = QCheckBox()
        self.is_visible.stateChanged.connect(self.is_visible_change)
        working_tab_layout.addWidget(self.is_visible, 8,3,1,1)
        
        class_worth_label = QLabel("Class Value EXP X")
        class_worth_label.setToolTip("How much EXP this class gives when defeated.\nAdvanced classes could give more EXP- bosses and thieves often do as well.")
        class_worth_label.setFont(self.body_font)
        working_tab_layout.addWidget(class_worth_label, 9,2,1,1)

        self.class_worth = QDoubleSpinBox()
        self.class_worth.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
        self.class_worth.setFont(self.body_font)
        self.class_worth.setRange(0.1,3.0)
        self.class_worth.setSingleStep(0.1)
        self.class_worth.setValue(1.0)
        self.class_worth.valueChanged.connect(self.class_worth_change)
        working_tab_layout.addWidget(self.class_worth, 9,3,1,1)
        
        exp_types_button = QPushButton("EXP Types Gained")
        exp_types_button.setMinimumHeight(40)
        exp_types_button.setToolTip("What knowledge types will gain experience during all combat, regardless of equipped weapon.\nFor example, a mounted cavalier might always gain lance, sword, and riding experience, even if using a sword only.\nIn that case, the unit would gain extra sword experience from the weapon as well.\nAdditional EXP types- such as Riding and Flying- can be set (or turned off) in the Game Editor")
        exp_types_button.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
        exp_types_button.clicked.connect(self.exp_types_edit)
        exp_types_button.setFont(self.body_font)
        working_tab_layout.addWidget(exp_types_button, len(wt)+4,3,1,1)

        self.tactics = QPushButton("Tactics")
        self.tactics.setMinimumHeight(40)
        self.tactics.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
        self.tactics.setToolTip("Tactics are limited use attacks with special effects that can target multiple tiles.\nThis allows Tactics to be class-specific")
        self.tactics.setFont(self.body_font)
        self.tactics.clicked.connect(self.tactics_dialog)
        working_tab_layout.addWidget(self.tactics, lenwt+2,0,1,1)

        self.skills = QPushButton("Skills")
        self.skills.setMinimumHeight(40)
        self.skills.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
        self.skills.setToolTip("Skills are unique abilities that incur bonuses or penalties.\nThis allows Skills to be class-specific")
        self.skills.setFont(self.body_font)
        self.skills.clicked.connect(self.skills_dialog)
        working_tab_layout.addWidget(self.skills, lenwt+2,1,1,1)

        self.skilled_blows = QPushButton("Skilled Blows")
        self.skilled_blows.setMinimumHeight(40)
        self.skilled_blows.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
        self.skilled_blows.setToolTip("Skilled Blows are special attacks that use extra weapon durability (\nor, if weapon durability is disabled, have a set number of uses).\nThis allows Skilled Blows to be class-specific")
        self.skilled_blows.setFont(self.body_font)
        self.skilled_blows.clicked.connect(self.skilled_blows_dialog)
        working_tab_layout.addWidget(self.skilled_blows, lenwt+2,2,1,1)

        self.growth_rates = QPushButton("Growth Rates")
        self.growth_rates.setMinimumHeight(40)
        self.growth_rates.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
        self.growth_rates.setToolTip("When a unit of this class levels up, their stats increase randomly.\n This allows the % growth chance to be changed for each stat.\nActual growth rate = (unit growth rate + class growth rate) / 2")
        self.growth_rates.setFont(self.body_font)
        self.growth_rates.clicked.connect(self.growth_rates_dialog)
        working_tab_layout.addWidget(self.growth_rates, lenwt+2,3,1,1)

        self.tile_changes = QPushButton("Universal Tile Changes")
        self.tile_changes.setMinimumHeight(40)
        self.tile_changes.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
        self.tile_changes.setToolTip("If this class interacts with tiles in a unique way, set those rules.\nFor example, a magic unit may not take damage from terrain.")
        self.tile_changes.setFont(self.body_font)
        self.tile_changes.clicked.connect(self.tile_changes_dialog)
        working_tab_layout.addWidget(self.tile_changes, lenwt+3,0,1,1)
        
        self.mtile_changes = QPushButton("Mounted Tile Changes")
        self.mtile_changes.setMinimumHeight(40)
        self.mtile_changes.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
        self.mtile_changes.setToolTip("If this class interacts with tiles in a unique way when mounted, set those rules.\nFor example, a mounted unit will move slowly (or not at all) on stairs.")
        self.mtile_changes.setFont(self.body_font)
        self.mtile_changes.clicked.connect(self.mtile_changes_dialog)
        working_tab_layout.addWidget(self.mtile_changes, lenwt+3,1,1,1)

        self.weak_against = QPushButton("Weakness")
        self.weak_against.setMinimumHeight(40)
        self.weak_against.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
        self.weak_against.setToolTip("Allows for unit weaknesses- for example, armored knights are often weak against magic.\nNote that Flying units already are weak against arrows.")
        self.weak_against.setFont(self.body_font)
        self.weak_against.clicked.connect(self.weak_against_dialog)
        working_tab_layout.addWidget(self.weak_against, lenwt+3,2,1,1)
        
        self.class_criteria = QPushButton("Class Criteria")
        self.class_criteria.setMinimumHeight(40)
        self.class_criteria.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
        self.class_criteria.setToolTip("If classes are criteria based (%) instead of level based, set Minimum Level to 0 and use this instead.")
        self.class_criteria.setFont(self.body_font)
        self.class_criteria.clicked.connect(self.criteria_dialog)
        working_tab_layout.addWidget(self.class_criteria, lenwt+3,3,1,1)

        self.stat_bonuses = QPushButton("Stats+")
        self.stat_bonuses.setMinimumHeight(40)
        self.stat_bonuses.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
        self.stat_bonuses.setToolTip("When a unit switches to this class, they can gain a set stat bonus.")
        self.stat_bonuses.setFont(self.body_font)
        self.stat_bonuses.clicked.connect(self.stat_bonuses_dialog)
        working_tab_layout.addWidget(self.stat_bonuses, lenwt+4,0,1,1)

        self.next_classes = QPushButton("Next Classes")
        self.next_classes.setMinimumHeight(40)
        self.next_classes.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
        self.next_classes.setToolTip("If using Branching Classes, set what classes come after this one.\nOtherwise, this can be ignored.\n(Set Branching Classes in the Game Editor)")
        self.next_classes.setFont(self.body_font)
        self.next_classes.clicked.connect(self.next_classes_dialog)
        working_tab_layout.addWidget(self.next_classes, len(wt)+4,1,1,1)
        
        self.graphics = QPushButton("Graphics")
        self.graphics.setMinimumHeight(40)
        self.graphics.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
        self.graphics.setToolTip("Change sprites/portraits for this class")
        self.graphics.setFont(self.body_font)
        self.graphics.clicked.connect(self.class_graphics_dialog)
        working_tab_layout.addWidget(self.graphics, len(wt)+4,2,1,1)

        self.wt_checkboxes = {}
        self.wt_checkboxes_right = {}
        count = 1

        for w in wt:
            count += 1
            self.wt_checkboxes[w] = QCheckBox()
            self.wt_checkboxes[w].setToolTip("Click to toggle type "+w)
            self.wt_checkboxes[w].name = w
            self.wt_checkboxes[w].stateChanged.connect(self.weapon_type_toggle)
            
            self.loaded_class.disallowed_weapon_types.append(w)
            label = QLabel(w)
            label.setFont(self.body_font)
            
            working_tab_layout.addWidget(label, count, 0, 1, 1)
            working_tab_layout.addWidget(self.wt_checkboxes[w], count, 1, 1, 1)
            
            working_tab_layout.setColumnStretch(0, 3)
            working_tab_layout.setColumnStretch(1, 3)
            working_tab_layout.setColumnStretch(2, 3)
            working_tab_layout.setColumnStretch(3, 3)
        
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
        self.team_member_list.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: "+active_theme.list_background_color)
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
        d_color = QColor(active_theme.window_background_color).darker(125).name()

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
        self.personal_enemy.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: "+active_theme.list_background_color)
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
            self.generic.setEnabled(True)
            self.generic_label.setEnabled(True)
            
        elif s == "Team":
            self.unit.is_friendly = True
            self.has_dialogue = True
            self.generic.setEnabled(False)
            self.generic_label.setEnabled(False)
            self.generic.setChecked(False)
        elif s == "Ally":
            self.unit.is_friendly = False
            self.unit.is_ally = True
            self.generic.setEnabled(True)
            self.generic_label.setEnabled(True)
        elif s == "Protagonist":
            k = confirmAction("#You can only have one!\nThis will clear the existing protagonist.\nContinue?")
            k.exec_()
            if k.return_confirm:
                self.unit.is_friendly = True
                self.unit.is_ally = False
                self.unit.is_lord = True
                self.generic.setEnabled(False)
                self.generic_label.setEnabled(False)
                self.generic.setChecked(False)
                #clear other units of lord flag
        elif s == "Recruitable Enemy":
            self.unit.is_friendly = False
            self.unit.is_recruitable = True
            self.generic.setEnabled(False)
            self.generic_label.setEnabled(False)
            self.generic.setChecked(False)
        elif s == "Recruitable Ally":
            self.unit.is_friendly = False
            self.unit.is_ally = True
            self.unit.is_recruitable = True
            self.generic.setEnabled(False)
            self.generic_label.setEnabled(False)
            self.generic.setChecked(False)
        
        if self.path != None:
            self.unit.selfToJSON(self.path)
            
    def genericChange(self, s):
        if s == 0:
            self.unit.unique = True
            self.generic_label.setEnabled(False)
        else:
            self.unit.unique = False
            self.generic_label.setEnabled(True)
            
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
        self.parent().parent().save_status.setPixmap(QPixmap("src/ui_icons/white/file_saving.png").scaled(int(int(data["icon_size"])/1.5),int(int(data["icon_size"])/1.5), Qt.KeepAspectRatio))
        self.parent().parent().save_status.setToolTip("Unit file saving")
        options = q.Options()
        options |= q.DontUseNativeDialog
        fileName, _ = q.getSaveFileName(None,"Save","","Turnroot Unit (*.truf)", options=options)
        if fileName:
            self.path = fileName+".truf"
            g = infoClose("Saved unit as "+self.path+"\nAll changes to this unit will now autosave")
            self.parent().parent().save_status.setPixmap(QPixmap("src/ui_icons/white/file_saved.png").scaled(int(int(data["icon_size"])/1.5),int(int(data["icon_size"])/1.5), Qt.KeepAspectRatio))
            self.parent().parent().save_status.setToolTip("Unit file saved")
            g.exec_()
            
    def unitToJSON(self):
        self.parent().parent().save_status.setPixmap(QPixmap("src/ui_icons/white/file_saving.png").scaled(int(int(data["icon_size"])/1.5),int(int(data["icon_size"])/1.5), Qt.KeepAspectRatio))
        self.parent().parent().save_status.setToolTip("Unit file saving")
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
                self.parent().parent().save_status.setPixmap(QPixmap("src/ui_icons/white/file_saved.png").scaled(int(int(data["icon_size"])/1.5),int(int(data["icon_size"])/1.5), Qt.KeepAspectRatio))
                self.parent().parent().save_status.setToolTip("Unit file saved")

        else:
            with open(self.path+".trui", "w") as w:
                json.dump(self.unit.AI_sheets, w)
            self.unit.selfToJSON(self.path)
            self.parent().parent().save_status.setPixmap(QPixmap("src/ui_icons/white/file_saved.png").scaled(int(int(data["icon_size"])/1.5),int(int(data["icon_size"])/1.5), Qt.KeepAspectRatio))
            self.parent().parent().save_status.setToolTip("Unit file saved")

    
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
            self.parent().parent().save_status.setPixmap(QPixmap("src/ui_icons/white/file_saving.png").scaled(int(int(data["icon_size"])/1.5),int(int(data["icon_size"])/1.5), Qt.KeepAspectRatio))
            self.parent().parent().save_status.setToolTip("Unit file saving")
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
                self.generic_label.setEnabled(True)
            else:
                self.generic_label.setEnabled(False)
            
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
                
            self.parent().parent().save_status.setPixmap(QPixmap("src/ui_icons/white/file_saved.png").scaled(int(int(data["icon_size"])/1.5),int(int(data["icon_size"])/1.5), Qt.KeepAspectRatio))
            self.parent().parent().save_status.setToolTip("Unit file saved")
        
                

    def AIHelpDialog(self):
        a = AIHelpDialog(parent=self,font=self.body_font)
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
        v = v / 11
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
        
        number_to_value = ["E", "E+","D", "D+", "C", "C+", "B", "B+", "A", "A+", "S"]
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
        f =editUniversalWeaponTypes(parent=self,font=self.body_font)
        f.exec_()
        if f.restart:
            self.parent().parent().restart()
    
    def class_name_change(self):
        tmp_data = self.loaded_class
        self.loaded_class = unitClass() 
        self.class_desc.setText("")
        self.minimum_level.setValue(0)
        self.is_mounted.setChecked(False)
        self.mounted_m.setValue(0)
        self.exp_m.setValue(0)
        self.class_type.setCurrentText("")
        self.is_flying.setChecked(False)
        
        for w in weaponTypes().data:
            self.wt_checkboxes[w].setChecked(False)
            
        s = self.class_name.text()
        self.loaded_class.unit_class_name = self.class_name.text()
        self.loaded_class.selfToJSON("src/skeletons/classes/"+s+".tructf")
        self.getClassesInFolder()
        self.loadClass(s)

    def minimum_level_change(self):
        self.loaded_class.minimum_level = self.minimum_level.value()
        self.loaded_class.selfToJSON("src/skeletons/classes/"+self.class_name.text()+".tructf")

    def is_mounted_change(self):
        self.loaded_class.is_mounted = self.is_mounted.isChecked()
        self.loaded_class.selfToJSON("src/skeletons/classes/"+self.class_name.text()+".tructf")
        
    def is_flying_change(self):
        self.loaded_class.is_flying = self.is_flying.isChecked()
        self.loaded_class.selfToJSON("src/skeletons/classes/"+self.class_name.text()+".tructf")

    def mounted_m_change(self):
        self.loaded_class.mounted_move_change = self.mounted_m.value()
        self.loaded_class.selfToJSON("src/skeletons/classes/"+self.class_name.text()+".tructf")

    def exp_m_change(self):
        self.loaded_class.exp_gained_multiplier = self.exp_m.value()
        self.loaded_class.selfToJSON("src/skeletons/classes/"+self.class_name.text()+".tructf")
    
    def class_worth_change(self):
        self.loaded_class.class_worth = self.class_worth.value()
        self.loaded_class.selfToJSON("src/skeletons/classes/"+self.class_name.text()+".tructf")

    def class_type_change(self):
        self.loaded_class.class_type = self.class_type.value()
        self.loaded_class.selfToJSON("src/skeletons/classes/"+self.class_name.text()+".tructf")
    
    def is_unique_change(self):
        self.loaded_class.unique_to_unit = self.is_unique.isChecked()
        self.loaded_class.selfToJSON("src/skeletons/classes/"+self.class_name.text()+".tructf")
    
    def is_visible_change(self):
        self.loaded_class.secret = self.is_unique.isChecked()
        self.loaded_class.selfToJSON("src/skeletons/classes/"+self.class_name.text()+".tructf")

    def growth_rates_dialog(self):
        u = growthRateDialog(parent=self,font=self.body_font)
        u.exec_()
        self.loaded_class.selfToJSON("src/skeletons/classes/"+self.class_name.text()+".tructf")
        
    def unit_growth_rates_dialog(self):
        u = unitGrowthRateDialog(parent=self,font=self.body_font)
        u.exec_()
        if self.path != None:
            self.unit.selfToJSON(self.path)

    def tile_changes_dialog(self):
        o = tileChangesDialog(parent=self,font=self.body_font)
        o.exec_()
        self.d_tile_changes = o.table_data[5]
        self.loaded_class.dismounted_tile_changes = self.d_tile_changes
        self.loaded_class.selfToJSON("src/skeletons/classes/"+self.class_name.text()+".tructf")

    def weak_against_dialog(self):
        w = weakAgainstDialog(parent=self,font=self.body_font)
        w.exec_()
        self.loaded_class.selfToJSON("src/skeletons/classes/"+self.class_name.text()+".tructf")

    def stat_bonuses_dialog(self):
        i = statBonusDialog(parent=self,font=self.body_font)
        i.exec_()
        self.loaded_class.selfToJSON("src/skeletons/classes/"+self.class_name.text()+".tructf")
    
    def class_graphics_dialog(self):
        l = classGraphicDialog(parent=self,font=self.body_font)
        l.exec_()
        self.loaded_class.selfToJSON("src/skeletons/classes/"+self.class_name.text()+".tructf")

    def weapon_type_toggle(self):
        w = self.sender().name
        s = self.sender().isChecked()
        if not s:
            self.wt_checkboxes[w].setChecked(False)
            if w not in self.loaded_class.disallowed_weapon_types:
                self.loaded_class.disallowed_weapon_types.append(w)
            if w in self.loaded_class.allowed_weapon_types:
                self.loaded_class.allowed_weapon_types.remove(w)
            
        else:
            self.wt_checkboxes[w].setChecked(True)
            if w not in self.loaded_class.allowed_weapon_types:
                self.loaded_class.allowed_weapon_types.append(w)
            if w in self.loaded_class.disallowed_weapon_types:
                self.loaded_class.disallowed_weapon_types.remove(w)

        self.loaded_class.selfToJSON("src/skeletons/classes/"+self.class_name.text()+".tructf")

    def tactics_dialog(self):
        pass
    
    def skills_dialog(self):
        y = classSkillDialog(parent=self,font=self.body_font)
        y.exec_()
        self.loaded_class.selfToJSON("src/skeletons/classes/"+self.class_name.text()+".tructf")

    def skilled_blows_dialog(self):
        pass
    
    def next_classes_dialog(self):
        n = nextClassesDialog(parent=self,font=self.body_font)
        n.exec_()
        self.loaded_class.selfToJSON("src/skeletons/classes/"+self.class_name.text()+".tructf")
            
    def getClassesInFolder(self, b = True):
        file_list = getFiles("src/skeletons/classes")[GET_FILES]
        class_names = []
        if hasattr(self.unit, "unit_class_name"):
            tmp_class_name = self.loaded_class_name
        global classes
        classes = {}
        self.paths = {}
        self.title_edit.clear()
        for f in file_list:
            if f.ext.strip() == ".tructf":
                tmp_class = unitClass()
                tmp_class.selfFromJSON(f.fullPath)
                self.paths[tmp_class.unit_class_name] = f.fullPath
                if tmp_class.unit_class_name not in class_names:
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
        try:
            self.class_name.setEnabled(False)
        except:
            pass
        if name == None:
            try:
                ac = self.loaded_class
                ac.selfFromJSON(self.paths[ac.unit_class_name])
            except:
                pass
        else:
            ac = unitClass()
            ac.selfFromJSON(self.paths[name])
            self.loaded_class = ac
        try:
            self.class_name.setText(ac.unit_class_name)
            self.class_name.setToolTip("Class will autosave as "+self.loaded_class.unit_class_name+".tructf")
            self.class_desc.setText(ac.desc)
            self.minimum_level.setValue(ac.minimum_level)
            self.is_mounted.setChecked(ac.is_mounted)
            self.mounted_m.setValue(ac.mounted_move_change)
            self.exp_m.setValue(ac.exp_gained_multiplier)
            self.class_type.setCurrentText(ac.class_type)
            self.is_flying.setChecked(ac.is_flying)
            self.class_worth.setValue(ac.class_worth)
            self.is_visible.setChecked(ac.secret)
            self.is_unique.setChecked(ac.unique_to_unit)
            
            for w in weaponTypes().data:
                if w in ac.allowed_weapon_types:
                    self.wt_checkboxes[w].setChecked(True)
                else:
                    self.wt_checkboxes[w].setChecked(False)
                if w in ac.disallowed_weapon_types:
                    self.wt_checkboxes[w].setChecked(False)
        except:
            pass
    
    def loadClassDialog(self):
        y = loadSavedClass(parent=self,font=self.body_font)
        y.exec_()
        if hasattr(y,"returns"):
            self.loadClass(name = y.returns)
            self.parent().parent().save_status.setPixmap(QPixmap("src/ui_icons/white/file_saved.png").scaled(int(int(data["icon_size"])/1.5),int(int(data["icon_size"])/1.5), Qt.KeepAspectRatio))
            self.parent().parent().save_status.setToolTip("Class file saved")
        else:
            c = infoClose("No class selected")
            c.exec_()
            self.parent().parent().save_status.setPixmap(QPixmap("src/ui_icons/white/file_not_saved.png").scaled(int(int(data["icon_size"])/1.5),int(int(data["icon_size"])/1.5), Qt.KeepAspectRatio))
            self.parent().parent().save_status.setToolTip("Class file not saved")

    
    def createClass(self):
        self.class_name.setEnabled(True)
        self.class_name.setToolTip("Press enter to save class as 'class name.tructf' in game folder.\nOnce a class is named, changes will autosave.")
        try:
            self.parent().parent().save_status.setPixmap(QPixmap("src/ui_icons/white/file_not_saved.png").scaled(int(int(data["icon_size"])/1.5),int(int(data["icon_size"])/1.5), Qt.KeepAspectRatio))
            self.parent().parent().save_status.setToolTip("Class file not saved")
        except:
            pass
        self.loaded_class = None
        self.loaded_class = unitClass()
        ac = self.loaded_class
        
        self.class_name.setText("")
        self.class_desc.setText("")
        self.minimum_level.setValue(0)
        self.is_mounted.setChecked(False)
        self.mounted_m.setValue(0)
        self.exp_m.setValue(1)
        self.class_type.setCurrentText("")
        self.is_flying.setChecked(False)
        self.class_worth.setValue(1)
        self.is_visible.setChecked(False)
        self.is_unique.setChecked(False)
        
        for w in weaponTypes().data:
            self.wt_checkboxes[w].setChecked(False)
    
    def class_desc_change(self):
        self.loaded_class.desc = self.sender().text()
        self.loaded_class.selfToJSON("src/skeletons/classes/"+self.class_name.text()+".tructf")
    
    def instance_stat_edit(self):
        u = instanceStatDialog(parent=self,font=self.body_font)
        u.exec_()
    
    def ctab_changed(self,s):
        if s == 4:
            self.parent().parent().menubar.setVisible(False)
            if self.loaded_class.unit_class_name == None:
                self.parent().parent().save_status.setPixmap(QPixmap("src/ui_icons/white/file_not_saved.png").scaled(int(int(data["icon_size"])/1.5),int(int(data["icon_size"])/1.5), Qt.KeepAspectRatio))
                self.parent().parent().save_status.setToolTip("Class file not saved")
            else:
                self.parent().parent().save_status.setPixmap(QPixmap("src/ui_icons/white/file_saved.png").scaled(int(int(data["icon_size"])/1.5),int(int(data["icon_size"])/1.5), Qt.KeepAspectRatio))
                self.parent().parent().save_status.setToolTip("Class file saved")
        else:
            self.parent().parent().menubar.setVisible(True)
            if self.path == None:
                self.parent().parent().save_status.setPixmap(QPixmap("src/ui_icons/white/file_not_saved.png").scaled(int(int(data["icon_size"])/1.5),int(int(data["icon_size"])/1.5), Qt.KeepAspectRatio))
                self.parent().parent().save_status.setToolTip("Unit file not saved")
            else:
                self.parent().parent().save_status.setPixmap(QPixmap("src/ui_icons/white/file_saved.png").scaled(int(int(data["icon_size"])/1.5),int(int(data["icon_size"])/1.5), Qt.KeepAspectRatio))
                self.parent().parent().save_status.setToolTip("Unit file saved")
    
    def mtile_changes_dialog(self):
        o = tileChangesDialog(parent=self,font=self.body_font)
        o.exec_()
        self.m_tile_changes = o.table_data[5]
        self.loaded_class.mounted_tile_changes = self.m_tile_changes
        self.loaded_class.selfToJSON("src/skeletons/classes/"+self.class_name.text()+".tructf")
    
    def criteria_dialog(self):
        c = classCriteriaDialog(parent=self,font=self.body_font)
        c.exec_()
        self.loaded_class.selfToJSON("src/skeletons/classes/"+self.class_name.text()+".tructf")
    
    def exp_types_edit(self):
        e = expTypesDialog(parent=self,font=self.body_font)
        e.exec_()
        self.loaded_class.selfToJSON("src/skeletons/classes/"+self.class_name.text()+".tructf")
