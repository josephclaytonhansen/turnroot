
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

from src.skeletons.unit import Unit, universal_classifications

from src.UI_Dialogs import confirmAction, popupInfo, infoClose
from src.game_directory import gameDirectory
from src.UI_unit_editor_dialogs import (growthRateDialog, statBonusDialog, AIHelpDialog, editUniversalStats,
                                        classSkillDialog, loadSavedClass,
                                        instanceStatDialog, tileChangesDialog, unitGrowthRateDialog,
                                        classCriteriaDialog)
from src.UI_unit_editor_more_dialogs import (weakAgainstDialog, expTypesDialog, nextClassesDialog,
                                             classGraphicDialog,editUniversalWeaponTypes, editClassifications, statCapDialog)

from src.game_directory import gameDirectory
directory = gameDirectory(None)
directory.getPath()
game_options = directory.getGameOptions()
print(game_options)

with open("src/skeletons/universal_stats.json", "r") as stats_file:
    universal_stats =  json.load(stats_file)

GET_FILES = 1
GET_FOLDERS = 0

class ValuedSpinBox(QSpinBox):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.index = 0

def initUnit(parent):
    #get unit from file
    parent.unit = Unit()
    parent.unit.unit_class = unitClass()
        
def initBasic(parent):
    parent.working_tab = parent.tabs_dict["Basic"]
    parent.working_tab_layout = parent.working_tab.layout()
    
    #split in thirds
    parent.basic_layout = QHBoxLayout()
    parent.basic_layout_widget = QWidget()
    parent.basic_layout_widget.setLayout(parent.basic_layout)
    
    parent.basic_left = QWidget()
    parent.basic_left_layout = QVBoxLayout()
    parent.basic_left_layout.setSpacing(0)
    parent.basic_left.setLayout(parent.basic_left_layout)
    parent.basic_layout.addWidget(parent.basic_left, 40)
    parent.basic_left.setMaximumWidth(580)
    
    parent.basic_center = QWidget()
    parent.basic_center_layout = QVBoxLayout()
    parent.basic_center_layout.setSpacing(0)
    parent.basic_center.setLayout(parent.basic_center_layout)
    parent.basic_layout.addWidget(parent.basic_center, 60)
    
    image = QPushButton()
    image.setMaximumHeight(522)
    image.setMaximumWidth(362)
    pixmap = QPixmap(360,520)
    pixmap.fill(QColor("white"))
    pixmap = QIcon(pixmap)
    image.setIcon(pixmap)
    image.setIconSize(QSize(360,520))
    image.setToolTip("Edit portraits in the Portrait Editor")
    
    img_container = QWidget()
    img_container_layout = QHBoxLayout()
    img_container.setLayout(img_container_layout)
    img_container_layout.addWidget(image)
    
    parent.basic_left_layout.addWidget(img_container)
    
    name_row = QWidget()
    name_row_layout = QHBoxLayout()
    name_row.setLayout(name_row_layout)
    
    parent.name_edit = QLineEdit()
    parent.name_edit.returnPressed.connect(parent.nameChange)
    parent.name_edit.setAlignment(Qt.AlignCenter)
    parent.name_edit.setPlaceholderText("Name")
    parent.name_edit.setToolTip("Change unit name.\nIf unit is Generic, name should also be generic.\nProtagonist name is the default if player doesn't change it.")
    parent.name_edit.setStyleSheet("background-color: "+active_theme.list_background_color+";")
    name_font = parent.name_edit.font()
    name_font.setPointSize(21)
    
    header_font = parent.name_edit.font()
    header_font.setPointSize(18)
    body_font = parent.name_edit.font()
    body_font.setPointSize(int(data["font_size"]))
    parent.body_font = body_font
    small_font = parent.name_edit.font()
    small_font.setPointSize(12)
    
    parent.name_edit.setFont(name_font)
    name_row_layout.addWidget(parent.name_edit)
    
    parent.title_edit = QComboBox()
    parent.title_edit.setStyleSheet("background-color: "+active_theme.list_background_color+";")
    parent.title_edit.currentTextChanged.connect(parent.classChange)
    parent.title_edit.setToolTip("Choose starting/current class from existing classes\n(edit or create new in the Classes tab)")
    parent.title_edit.setFont(header_font)
    name_row_layout.addWidget(parent.title_edit)
    
    parent.class_popup = QPushButton()
    parent.class_popup.setIcon(QIcon("src/ui_icons/white/edit.png"))
    parent.class_popup.setIconSize(QSize(48,48))
    parent.class_popup.setStyleSheet("background-color: "+active_theme.list_background_color+";")
    parent.class_popup.clicked.connect(parent.baseClassPopup)
    parent.class_popup.setToolTip("Set other base class choices, for re-classing")
    parent.class_popup.setFont(header_font)
    name_row_layout.addWidget(parent.class_popup)
    
    try:
        parent.getClassesInFolder()
    except: #game folder is invalid
        pass
    
    parent.basic_left_layout.addWidget(name_row)
    
    identity_row = QWidget()
    identity_row_layout = QHBoxLayout()
    identity_row.setLayout(identity_row_layout)
    
    parent.pronouns_edit = QComboBox()
    parent.pronouns_edit.currentTextChanged.connect(parent.genderChange)
    parent.pronouns_edit.addItems(["He/Him", "She/Her", "They/Them"])
    parent.pronouns_edit.setToolTip("Set unit pronouns")
    parent.pronouns_edit.setFont(small_font)
    identity_row_layout.addWidget(parent.pronouns_edit)
    
    parent.basic_left_layout.addWidget(identity_row)
    
    checkbox_row = QWidget()
    checkbox_row_layout = QHBoxLayout()
    checkbox_row.setLayout(checkbox_row_layout)
    
    protag_label = QLabel("Protagonist")
    protag_label.setToolTip("The protagonist, or avatar, is the unit that stands in for the player.\nIf protagonist is enabled in game settings, player can customize this unit")
    parent.protag = QCheckBox()
    
    parent.generic_label = QPushButton("Generic")
    parent.generic_label.setStyleSheet("background-color: "+active_theme.list_background_color+";")
    parent.generic_label.setToolTip("If checked, there can be instances of this unit- i.e., a basic soldier.\n If unchecked, unit is unique and cannot be instanced\nClick to edit instance randomness")
    parent.generic_label.clicked.connect(parent.instance_stat_edit)
    parent.generic_label.setEnabled(False)
    parent.generic = QCheckBox()
    
    checkbox_font = protag_label.font()
    checkbox_font.setPointSize(12)
    protag_label.setFont(checkbox_font)
    parent.protag.setFont(checkbox_font)
    parent.generic_label.setFont(checkbox_font)
    parent.generic.setFont(checkbox_font)
    
    parent.status = QComboBox()
    parent.status.setStyleSheet("background-color: "+active_theme.list_background_color+";")
    parent.status.setToolTip("Change status. You can only have one protagonist.\nEnemies and Allies can be generic, Recruitable Enemies/Allies or Team members cannot")
    parent.status.currentTextChanged.connect(parent.statusChange)
    parent.status.addItems(["Enemy", "Team", "Ally", "Protagonist", "Recruitable Enemy", "Recruitable Ally"])
    parent.status.setFont(checkbox_font)
    
    checkbox_row_layout.addWidget(parent.generic_label)
    checkbox_row_layout.addWidget(parent.generic)
    parent.generic.stateChanged.connect(parent.genericChange)
    
    parent.basic_left_layout.addWidget(checkbox_row)
    
    status_row = QWidget()
    status_row_layout = QHBoxLayout()
    status_row.setLayout(status_row_layout)
    status_row_layout.addWidget(parent.status)
    
    parent.basic_left_layout.addWidget(status_row)
    
    c_row = QWidget()
    c_row_layout = QHBoxLayout()
    c_row.setLayout(c_row_layout)
    
    parent.classification = QComboBox()
    parent.classification.setStyleSheet("background-color: "+active_theme.list_background_color+";")
    parent.classification.setToolTip("Set unit classification. Mainly affects weapon abilities")
    parent.classification.addItems(universal_classifications)
    edit_c = QPushButton("Edit")
    edit_c.clicked.connect(parent.editClassifications)
    edit_c.setToolTip("Change universal classifications. For example, if you're making a sci-fi game, you could remove 'dragon' and replace with 'cyborg'")
    edit_c.setStyleSheet("background-color: "+active_theme.list_background_color+";")
    edit_c.setFont(parent.body_font)
    parent.classification.setFont(parent.body_font)
    c_row_layout.addWidget(parent.classification)
    parent.classification.currentTextChanged.connect(parent.classificationChange)
    c_row_layout.addWidget(edit_c)
    
    parent.basic_left_layout.addWidget(c_row)
    
    parent.working_tab_layout.addWidget(parent.basic_left)
    
    stats_header_growth = QWidget()
    shg_layout = QHBoxLayout()
    stats_header_growth.setLayout(shg_layout)
    
    stat_label = QLabel("Base Stats")
    stat_label.setToolTip("How much of each universal stat unit has at level 1\nStat growth rate = (unit growth rate + class growth rate / 2)")
    stat_label.setFont(header_font)
    
    growth_rates = QPushButton("Stat Growth Rates")
    growth_rates.clicked.connect(parent.unit_growth_rates_dialog)
    growth_rates.setToolTip("Set natural affinity for different stats.\nYou can also test growth rates here.\nNote that unit growth rate are always enabled, but class growth rates can be disabled in the Game Editor.\nIf growth chance for Strength for a unit is 60, and the class growth rate is 80, the actual growth rate is 70")
    growth_rates.setFont(parent.body_font)
    
    shg_layout.addWidget(stat_label)
    shg_layout.addWidget(growth_rates)
    
    parent.basic_center_layout.addWidget(stats_header_growth)
    
    parent.stat_row = {}
    parent.stat_values = {}
    parent.stat_spins = {}
    parent.stat_tooltips = [
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
        parent.stat_row[s] = QWidget()
        parent.stat_row[s].setToolTip(parent.stat_tooltips[universal_stats.index(s)])
        parent.stat_row_layout = QHBoxLayout()
        parent.stat_row[s].setLayout(parent.stat_row_layout)
        
        stat_label = QLabel(s[0].upper()+s[1:])
        stat_label.setFont(small_font)
        parent.stat_row_layout.addWidget(stat_label)
        parent.stat_values[s] = getattr(parent.unit, s)
        stat_value = ValuedSpinBox()
        parent.stat_spins[s] = stat_value
        stat_value.setStyleSheet("background-color: "+active_theme.list_background_color+";")
        stat_value.setRange(0,900)
        stat_value.index = universal_stats.index(s)
        stat_value.valueChanged.connect(parent.statChange)
        stat_value.setFont(small_font)
        stat_value.setValue(int(parent.stat_values[s]))
        parent.stat_row_layout.addWidget(stat_value)
        
        parent.basic_center_layout.addWidget(parent.stat_row[s])
    
    text_row = QWidget()
    text_row_layout = QHBoxLayout()
    text_row.setLayout(text_row_layout)
    
    notes_column = QWidget()
    notes_column_layout = QVBoxLayout()
    notes_column.setLayout(notes_column_layout)
    
    desc_column = QWidget()
    desc_column_layout = QVBoxLayout()
    desc_column.setLayout(desc_column_layout)
    
    parent.notes = QTextEdit()
    parent.notes.setStyleSheet("background-color: "+active_theme.list_background_color+";")
    parent.notes.textChanged.connect(parent.notesChange)
    parent.notes.setFont(small_font)
    notes_label = QLabel("Notes")
    notes_label.setToolTip("only seen by you")
    notes_label.setFont(header_font)
    
    parent.description = QTextEdit()
    parent.description.setStyleSheet("background-color: "+active_theme.list_background_color+";")
    parent.description.textChanged.connect(parent.descriptionChange)
    parent.description.setFont(small_font)
    description_label = QLabel("Description")
    description_label.setToolTip("Added to game")
    description_label.setFont(header_font)
    
    notes_column_layout.addWidget(notes_label)
    notes_column_layout.addWidget(parent.notes)
    
    desc_column_layout.addWidget(description_label)
    desc_column_layout.addWidget(parent.description)
    
    text_row_layout.addWidget(notes_column)
    text_row_layout.addWidget(desc_column)
    
    stat_cap = QPushButton("Stat Caps (if enabled)")
    stat_cap.setFont(parent.body_font)
    stat_cap.setToolTip("If Stat Caps are enabled in the Game Editor, set the maximum amount this unit can reach for each stat. Otherwise, ignore")
    stat_cap.clicked.connect(parent.stat_cap_change)
    parent.basic_center_layout.addWidget(stat_cap)
    
    parent.basic_center_layout.addWidget(text_row)
    
    parent.working_tab_layout.addWidget(parent.basic_center)
    parent.generic_label.setEnabled(False)
    
def initAI(parent):
    parent.sheets = {}
    parent.sheetsFromJSON()

    parent.working_tab = parent.tabs_dict["AI"]
    parent.working_tab_layout = parent.working_tab.layout()
    
    parent.basic_layout = QVBoxLayout()
    parent.basic_layout_widget = QWidget()
    parent.basic_layout_widget.setLayout(parent.basic_layout)
    
    parent.tables = {}
    
    #default values- basic foot soldier
    parent.table_data = parent.sheets["Foot Soldier"]
    parent.dv_slider_dv = [15,35,40]
    
    parent.basic_table_categories = ["Move Towards", "Move Goals", "Targeting", "Targeting Change", "Avoid", "Tiles"]
    parent.column_colors_dict = [[active_theme.unit_editor_rule_0, "black"],
                               [active_theme.unit_editor_rule_1, "black"],
                               [active_theme.unit_editor_rule_2, "white"],
                               [active_theme.unit_editor_rule_3, "white"],
                               [active_theme.unit_editor_rule_4, "white"],
                               [active_theme.unit_editor_rule_5, "white"]]
    
    for t in parent.basic_table_categories:
        table = QTableView()
        table_font = QFont("Menlo")
        table_font.setPointSize(14)
        table_font.setStyleHint(QFont.TypeWriter)
        table.setFont(table_font)
        table.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.horizontalHeader().setVisible(False)
        table.verticalHeader().setVisible(False)
        parent.tables[t] = table
        
        table_data = parent.table_data[parent.basic_table_categories.index(t)]

        model = TableModel(table_data)
        parent.tables[t].setModel(model)
        parent.tables[t].model().column_colors = parent.column_colors_dict[parent.basic_table_categories.index(t)]
    
    personality_slider_row_1 = QWidget()
    personality_slider_row_1_layout = QHBoxLayout()
    personality_slider_row_1.setLayout(personality_slider_row_1_layout)
    
    personality_slider_row_2 = QWidget()
    personality_slider_row_layout_2 = QHBoxLayout()
    personality_slider_row_2.setLayout(personality_slider_row_layout_2)
    
    personality_slider_row_3 = QWidget()
    personality_slider_row_layout_3 = QHBoxLayout()
    personality_slider_row_3.setLayout(personality_slider_row_layout_3)
    
    parent.solider_lone_wolf_slider= QSlider(Qt.Horizontal)
    parent.solider_lone_wolf_slider.name = 1
    parent.solider_lone_wolf_slider.setFixedWidth(750)
    parent.solider_lone_wolf_slider.valueChanged.connect(parent.colorizeSlider)
    parent.solider_lone_wolf_slider.setValue(50)
    parent.solider_lone_wolf_slider.setRange(0,100)
    parent.solider_lone_wolf_slider.setSingleStep(1)
    
    soldier_label = QLabel("Soldier")
    soldier_label.setFont(parent.body_font)
    lonewolf_label = QLabel("Lone Wolf")
    lonewolf_label.setFont(parent.body_font)
    
    personality_slider_row_1_layout.addWidget(soldier_label)
    personality_slider_row_1_layout.addWidget(parent.solider_lone_wolf_slider)
    personality_slider_row_1_layout.addWidget(lonewolf_label)
    
    parent.strategic_mindless_slider= QSlider(Qt.Horizontal)
    parent.strategic_mindless_slider.name = 2
    parent.strategic_mindless_slider.setFixedWidth(750)
    parent.strategic_mindless_slider.valueChanged.connect(parent.colorizeSlider)
    parent.strategic_mindless_slider.setValue(50)
    parent.strategic_mindless_slider.setRange(0,100)
    parent.strategic_mindless_slider.setSingleStep(1)
    
    strategic_label = QLabel("Strategic")
    strategic_label.setFont(parent.body_font)
    mindless_label = QLabel("Mindless")
    mindless_label.setFont(parent.body_font)
    
    personality_slider_row_layout_2.addWidget(strategic_label)
    personality_slider_row_layout_2.addWidget(parent.strategic_mindless_slider)
    personality_slider_row_layout_2.addWidget(mindless_label)
    
    parent.cautious_brash_slider= QSlider(Qt.Horizontal)
    parent.cautious_brash_slider.name = 3
    parent.cautious_brash_slider.setFixedWidth(750)
    parent.cautious_brash_slider.valueChanged.connect(parent.colorizeSlider)
    parent.cautious_brash_slider.setValue(50)
    parent.cautious_brash_slider.setRange(0,100)
    parent.cautious_brash_slider.setSingleStep(1)
    
    cautious_label = QLabel("Cautious")
    cautious_label.setFont(parent.body_font)
    brash_label = QLabel("Brash")
    brash_label.setFont(parent.body_font)
    
    personality_slider_row_layout_3.addWidget(cautious_label)
    personality_slider_row_layout_3.addWidget(parent.cautious_brash_slider)
    personality_slider_row_layout_3.addWidget(brash_label)

    parent.basic_layout.addWidget(personality_slider_row_1)
    parent.basic_layout.addWidget(personality_slider_row_2)
    parent.basic_layout.addWidget(personality_slider_row_3)

    basic_table_tabs = QTabWidget()
    
    basic_table_tabs.setFont(parent.tabs_font)
    
    basic_table_tabs.setTabPosition(QTabWidget.South)

    for tab in parent.basic_table_categories:
        tab_title = tab
        c_tab = parent.tables[tab]
        c_tab.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
        basic_table_tabs.addTab(c_tab, tab_title)
    
    parent.basic_layout.addWidget(basic_table_tabs)
    
    rules_row = QWidget()
    rules_row_layout = QHBoxLayout()
    rules_row.setLayout(rules_row_layout)
    
    basic_principles = QPushButton("Overview")
    basic_principles.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
    basic_principles.setFont(parent.body_font)
    basic_principles.clicked.connect(parent.AIOverviewDialog)
    
    detailed_help = QPushButton("Rule Guidelines")
    detailed_help.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
    detailed_help.setFont(parent.body_font)
    detailed_help.clicked.connect(parent.AIHelpDialog)

    
    rules_row_layout.addWidget(basic_principles)
    rules_row_layout.addWidget(detailed_help)
    
    parent.basic_layout.addWidget(rules_row)
    
    default_values_row = QWidget()
    default_values_row_layout = QHBoxLayout()
    default_values_row.setLayout(default_values_row_layout)
    
    parent.default_values = QComboBox()
    parent.default_values.setFont(parent.body_font)
    with open("src/skeletons/sheets/default_slider_values.json", "r") as file:
        parent.dv_slider_from_sheet = json.load(file)

    parent.solider_lone_wolf_slider.setValue(parent.dv_slider_dv[0])
    parent.strategic_mindless_slider.setValue(parent.dv_slider_dv[1])
    parent.cautious_brash_slider.setValue(parent.dv_slider_dv[2])
    
    parent.default_values.addItems(["--Select--", "Foot Soldier", "Pegasus (Flying) Knight", "Mindless Creature", "Cautious Healer", "Assassin", "Sniper", "Vengeful Demon",
                                  "Strategic Leader", "Armored Tank"])
    parent.default_values.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
    default_values_button = QPushButton("Load Preset")
    default_values_button.setStyleSheet("background-color: "+active_theme.button_alt_color+"; color:"+active_theme.button_alt_text_color+"; font-size: "+str(data["font_size"]))
    default_values_button.setFont(parent.body_font)
    default_values_button.clicked.connect(parent.AILoadSheets)
    
    default_values_row_layout.addWidget(parent.default_values)
    default_values_row_layout.addWidget(default_values_button)
    
    parent.basic_layout.addWidget(default_values_row)

    parent.working_tab_layout.addWidget(parent.basic_layout_widget)
    
def initWeaponAffinities(parent):
    working_tab = parent.tabs_dict["Weapon Affinities"]
    working_tab_layout = working_tab.layout()
    
    parent.starting_level_labels = {}
    parent.weapon_type_widgets = {}
    parent.starting_type_sliders = {}
    parent.growth_multipliers_widgets = {}
    growth_multiplier_labels = {}
    
    parent.wascroll = QScrollArea()
    parent.wascroll.setWidgetResizable(True)
    working_tab_layout.addWidget(parent.wascroll)
    
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
        
        parent.weapon_type_widgets[weapon_type] = weapon_type_widget
        
        parent.starting_level_labels[weapon_type] = QLabel("D")
        parent.starting_level_labels[weapon_type].setToolTip("At level one, unit's proficiency with weapon")
        parent.starting_level_labels[weapon_type].setFont(parent.body_font)
        lab = QLabel("<b>"+weapon_type.upper()+"</b><br>Starting level")
        lab.setFont(parent.body_font)
        weapon_type_layout.addWidget(lab)
        weapon_type_layout.addWidget(parent.starting_level_labels[weapon_type])
        
        parent.starting_type_sliders[weapon_type] = QSlider(Qt.Vertical)
        parent.starting_type_sliders[weapon_type].name = weapon_type
        parent.starting_type_sliders[weapon_type].valueChanged.connect(parent.colorizeSliderC)
        parent.starting_type_sliders[weapon_type].valueChanged.connect(parent.weapon_starting_level_changed)
        parent.starting_type_sliders[weapon_type].setValue(2)
        parent.starting_type_sliders[weapon_type].setValue(0)
        parent.starting_type_sliders[weapon_type].setRange(0,10)
        parent.starting_type_sliders[weapon_type].setSingleStep(1)
        
        weapon_type_layout.addWidget(parent.starting_type_sliders[weapon_type])
        
        growth_multiplier_labels[weapon_type] = QLabel("Growth Rate")
        growth_multiplier_labels[weapon_type].setFont(parent.body_font)
        growth_multiplier_labels[weapon_type].setToolTip("How quickly/slowly unit gains weapon experience.\nFor instance, values less than 1 are a weakness- unit will learn slowly.")
        weapon_type_layout.addWidget(growth_multiplier_labels[weapon_type])
        
        parent.growth_multipliers_widgets[weapon_type] = QDoubleSpinBox()
        parent.growth_multipliers_widgets[weapon_type].setFont(parent.body_font)
        parent.growth_multipliers_widgets[weapon_type].name = weapon_type
        parent.growth_multipliers_widgets[weapon_type].setRange(0.5,2)
        parent.growth_multipliers_widgets[weapon_type].setValue(1.0)
        parent.growth_multipliers_widgets[weapon_type].setSingleStep(0.1)
        parent.growth_multipliers_widgets[weapon_type].valueChanged.connect(parent.growth_multiplier_changed)
        
        weapon_type_layout.addWidget(parent.growth_multipliers_widgets[weapon_type])
        
        column_inner_layout.addWidget(weapon_type_widget)
        
    column_layout.addWidget(column_inner)
        
    parent.edit_weapon_types = QPushButton("Edit Weapon Types")
    parent.edit_weapon_types.setToolTip("Edit universal weapon types.")
    parent.edit_weapon_types.setFont(parent.body_font)
    parent.edit_weapon_types.clicked.connect(parent.weaponTypesChange)
    column_layout.addWidget(parent.edit_weapon_types)
        
    parent.wascroll.setWidget(column)

def initActions(parent):
    working_tab = parent.tabs_dict["Actions"]
    working_tab_layout = working_tab.layout

def initClasses(parent):
    parent.loaded_class = unitClass()
    parent.d_tile_changes = {}
    parent.m_tile_changes = {}
    working_tab = parent.tabs_dict["Classes"]
    working_tab_layout = working_tab.layout()
    
    working_tab_layout.setContentsMargins(20,20,20,20)
    working_tab_layout.setSpacing(2)
    
    wt = weaponTypes().data
    lenwt = len(wt)
    if lenwt < 10:
        lenwt = 10

    parent.class_name = QLineEdit()
    parent.class_name.setFont(parent.body_font)
    parent.class_name.setPlaceholderText("Class name")
    parent.class_name.setToolTip("Press enter to save class as 'class name.tructf' in game folder.\nOnce a class is named, changes will autosave.")
    parent.class_name.returnPressed.connect(parent.class_name_change)
    working_tab_layout.addWidget(parent.class_name, 0,0,1,1)
    
    parent.class_desc = QLineEdit()
    parent.class_desc.setFont(parent.body_font)
    parent.class_desc.setPlaceholderText("Class description")
    parent.class_desc.setToolTip("In-game class description.")
    parent.class_desc.textChanged.connect(parent.class_desc_change)
    working_tab_layout.addWidget(parent.class_desc, 0,1,1,1)
    
    parent.new_class = QPushButton("New Class")
    parent.new_class.setStyleSheet("background-color: "+active_theme.button_alt_color+"; color:"+active_theme.button_alt_text_color+"; font-size: "+str(data["font_size"]))
    parent.new_class.setToolTip("Create a new, blank, class (will not save until named)")
    parent.new_class.setFont(parent.body_font)
    parent.new_class.clicked.connect(parent.createClass)
    working_tab_layout.addWidget(parent.new_class, 0,3,1,1)
    
    parent.load_class = QPushButton("Load Class")
    parent.load_class.setToolTip("Load a saved class for editing")
    parent.load_class.setFont(parent.body_font)
    parent.load_class.setStyleSheet("background-color: "+active_theme.button_alt_color+"; color:"+active_theme.button_alt_text_color+"; font-size: "+str(data["font_size"]))
    parent.load_class.clicked.connect(parent.loadClassDialog)
    working_tab_layout.addWidget(parent.load_class, 0,2,1,1)

    allowed_weapons_label = QLabel("Can use")
    allowed_weapons_label.setFont(parent.body_font)
    working_tab_layout.addWidget(allowed_weapons_label, 1,1,1,1)

    minimum_level_label = QLabel("Minimum level")
    minimum_level_label.setFont(parent.body_font)
    working_tab_layout.addWidget(minimum_level_label, 1,2,1,1)
    minimum_level_label.setToolTip("Minimum unit level to have this class.\n If classes are criteria based, set this to 0.\nCriteria vs Level can be set in the Game Editor")

    parent.minimum_level = QSpinBox()
    parent.minimum_level.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
    parent.minimum_level.setFont(parent.body_font)
    parent.minimum_level.setRange(0,40)
    parent.minimum_level.valueChanged.connect(parent.minimum_level_change)
    working_tab_layout.addWidget(parent.minimum_level, 1,3,1,1)

    is_mounted_label = QLabel("Mounted?")
    is_mounted_label.setToolTip("If unit is mounted, they gain increased movement.\nTile changes such as stairs can be added with the Tile Changes button.\nUnit will have the option to Dismount/Mount")
    is_mounted_label.setFont(parent.body_font)
    working_tab_layout.addWidget(is_mounted_label, 2,2,1,1)

    parent.is_mounted = QCheckBox()
    parent.is_mounted.stateChanged.connect(parent.is_mounted_change)
    working_tab_layout.addWidget(parent.is_mounted, 2,3,1,1)

    mounted_m_label = QLabel("Mounted movement+")
    mounted_m_label.setToolTip("How many more tiles are added to movement radius when mounted")
    mounted_m_label.setFont(parent.body_font)
    working_tab_layout.addWidget(mounted_m_label, 3,2,1,1)

    parent.mounted_m = QSpinBox()
    parent.mounted_m.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
    parent.mounted_m.setFont(parent.body_font)
    parent.mounted_m.setRange(0,10)
    parent.mounted_m.valueChanged.connect(parent.mounted_m_change)
    working_tab_layout.addWidget(parent.mounted_m, 3,3,1,1)

    exp_m_label = QLabel("EXP growth X")
    exp_m_label.setToolTip("How quickly this class levels up.\n Low level classes should have a value higher than 1, advanced classes should be lower.")
    exp_m_label.setFont(parent.body_font)
    working_tab_layout.addWidget(exp_m_label, 4,2,1,1)

    parent.exp_m = QDoubleSpinBox()
    parent.exp_m.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
    parent.exp_m.setFont(parent.body_font)
    parent.exp_m.setRange(0.1,3.0)
    parent.exp_m.setSingleStep(0.1)
    parent.exp_m.setValue(1.25)
    parent.exp_m.valueChanged.connect(parent.exp_m_change)
    working_tab_layout.addWidget(parent.exp_m, 4,3,1,1)

    class_type_label = QLabel("Item growth type")
    class_type_label.setToolTip("If using items such as seals for class growth, set type needed.\nYou can set these in the Game Editor")
    class_type_label.setFont(parent.body_font)
    working_tab_layout.addWidget(class_type_label, 5,2,1,1)

    parent.class_type = QComboBox()
    parent.class_type.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
    parent.class_type.setFont(parent.body_font)
    parent.class_type.currentTextChanged.connect(parent.class_type_change)
    working_tab_layout.addWidget(parent.class_type, 5,3,1,1)
    
    is_flying_label = QLabel("Flying?")
    is_flying_label.setToolTip("If unit can fly, they have the same options as a mounted unit (including Movement+), but they are weak to arrows/projectiles")
    is_flying_label.setFont(parent.body_font)
    working_tab_layout.addWidget(is_flying_label, 6,2,1,1)

    parent.is_flying = QCheckBox()
    parent.is_flying.stateChanged.connect(parent.is_flying_change)
    working_tab_layout.addWidget(parent.is_flying, 6,3,1,1)
    
#     is_unique_label = QLabel("Unique to unit?")
#     is_unique_label.setToolTip("If class is unique to unit, minimum level/criteria will be ignored\nIf a unit has a unique class set (from the drop-down on the Basic tab), unit will start with that class")
#     is_unique_label.setFont(parent.body_font)
#     working_tab_layout.addWidget(is_unique_label, 7,2,1,1)
# 
#     parent.is_unique = QCheckBox()
#     parent.is_unique.stateChanged.connect(parent.is_unique_change)
#     working_tab_layout.addWidget(parent.is_unique, 7,3,1,1)
    class_type_label = QLabel("Class type/tier?")
    class_type_label.setToolTip("Choose whether this is a Basic class or a higher tier (set tiers in the Game Editor)")
    class_type_label.setFont(parent.body_font)
    working_tab_layout.addWidget(class_type_label, 7, 2, 1, 1)
    
    parent.class_type = QComboBox()
    parent.class_type.currentTextChanged.connect(parent.class_type_changed)
    parent.class_type.setFont(parent.body_font)
    working_tab_layout.addWidget(parent.class_type, 7, 3, 1,1)
    try:
        if "How many levels of classes are there?" not in game_options:
            parent.class_type.addItem("Basic")
        else:
            if game_options["How many levels of classes are there?"] == '2 (Basic, Advanced)':
                parent.class_type.addItems(["Basic",'Advanced'])
            else:
                parent.class_type.addItems(["Basic", "Advanced", "Master"])
    except:
        parent.class_type.addItem("Basic")
    
    is_visible_label = QLabel("Secret class?")
    is_visible_label.setToolTip("If class is secret, it can't be normally achieved (level/criteria, if using), nor will it show up in class grid (if using).\nA secret class is given through a game event or item.\nFor example, a Lord could become a Great Lord at the right time.")
    is_visible_label.setFont(parent.body_font)
    working_tab_layout.addWidget(is_visible_label, 8,2,1,1)

    parent.is_visible = QCheckBox()
    parent.is_visible.stateChanged.connect(parent.is_visible_change)
    working_tab_layout.addWidget(parent.is_visible, 8,3,1,1)
    
    class_worth_label = QLabel("Class Value EXP X")
    class_worth_label.setToolTip("How much EXP this class gives when defeated.\nAdvanced classes could give more EXP- bosses and thieves often do as well.")
    class_worth_label.setFont(parent.body_font)
    working_tab_layout.addWidget(class_worth_label, 9,2,1,1)

    parent.class_worth = QDoubleSpinBox()
    parent.class_worth.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
    parent.class_worth.setFont(parent.body_font)
    parent.class_worth.setRange(0.1,3.0)
    parent.class_worth.setSingleStep(0.1)
    parent.class_worth.setValue(1.0)
    parent.class_worth.valueChanged.connect(parent.class_worth_change)
    working_tab_layout.addWidget(parent.class_worth, 9,3,1,1)
    
    exp_types_button = QPushButton("EXP Types Gained")
    exp_types_button.setMinimumHeight(40)
    exp_types_button.setToolTip("What knowledge types will gain experience during all combat, regardless of equipped weapon.\nFor example, a mounted cavalier might always gain lance, sword, and riding experience, even if using a sword only.\nIn that case, the unit would gain extra sword experience from the weapon as well.\nAdditional EXP types- such as Riding and Flying- can be set (or turned off) in the Game Editor")
    exp_types_button.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
    exp_types_button.clicked.connect(parent.exp_types_edit)
    exp_types_button.setFont(parent.body_font)
    working_tab_layout.addWidget(exp_types_button, len(wt)+4,3,1,1)

    parent.tactics = QPushButton("Tactics")
    parent.tactics.setMinimumHeight(40)
    parent.tactics.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
    parent.tactics.setToolTip("Tactics are limited use attacks with special effects that can target multiple tiles.\nThis allows Tactics to be class-specific")
    parent.tactics.setFont(parent.body_font)
    parent.tactics.clicked.connect(parent.tactics_dialog)
    working_tab_layout.addWidget(parent.tactics, lenwt+2,0,1,1)

    parent.skills = QPushButton("Skills")
    parent.skills.setMinimumHeight(40)
    parent.skills.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
    parent.skills.setToolTip("Skills are unique abilities that incur bonuses or penalties.\nThis allows Skills to be class-specific")
    parent.skills.setFont(parent.body_font)
    parent.skills.clicked.connect(parent.skills_dialog)
    working_tab_layout.addWidget(parent.skills, lenwt+2,1,1,1)

    parent.skilled_blows = QPushButton("Skilled Blows")
    parent.skilled_blows.setMinimumHeight(40)
    parent.skilled_blows.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
    parent.skilled_blows.setToolTip("Skilled Blows are special attacks that use extra weapon durability (\nor, if weapon durability is disabled, have a set number of uses).\nThis allows Skilled Blows to be class-specific")
    parent.skilled_blows.setFont(parent.body_font)
    parent.skilled_blows.clicked.connect(parent.skilled_blows_dialog)
    working_tab_layout.addWidget(parent.skilled_blows, lenwt+2,2,1,1)

    parent.growth_rates = QPushButton("Growth Rates")
    parent.growth_rates.setMinimumHeight(40)
    parent.growth_rates.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
    parent.growth_rates.setToolTip("When a unit of this class levels up, their stats increase randomly.\n This allows the % growth chance to be changed for each stat.\nActual growth rate = (unit growth rate + class growth rate) / 2")
    parent.growth_rates.setFont(parent.body_font)
    parent.growth_rates.clicked.connect(parent.growth_rates_dialog)
    working_tab_layout.addWidget(parent.growth_rates, lenwt+2,3,1,1)

    parent.tile_changes = QPushButton("Universal Tile Changes")
    parent.tile_changes.setMinimumHeight(40)
    parent.tile_changes.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
    parent.tile_changes.setToolTip("If this class interacts with tiles in a unique way, set those rules.\nFor example, a magic unit may not take damage from terrain.")
    parent.tile_changes.setFont(parent.body_font)
    parent.tile_changes.clicked.connect(parent.tile_changes_dialog)
    working_tab_layout.addWidget(parent.tile_changes, lenwt+3,0,1,1)
    
    parent.mtile_changes = QPushButton("Mounted Tile Changes")
    parent.mtile_changes.setMinimumHeight(40)
    parent.mtile_changes.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
    parent.mtile_changes.setToolTip("If this class interacts with tiles in a unique way when mounted, set those rules.\nFor example, a mounted unit will move slowly (or not at all) on stairs.")
    parent.mtile_changes.setFont(parent.body_font)
    parent.mtile_changes.clicked.connect(parent.mtile_changes_dialog)
    working_tab_layout.addWidget(parent.mtile_changes, lenwt+3,1,1,1)

    parent.weak_against = QPushButton("Weakness")
    parent.weak_against.setMinimumHeight(40)
    parent.weak_against.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
    parent.weak_against.setToolTip("Allows for unit weaknesses- for example, armored knights are often weak against magic.\nNote that Flying units already are weak against arrows.")
    parent.weak_against.setFont(parent.body_font)
    parent.weak_against.clicked.connect(parent.weak_against_dialog)
    working_tab_layout.addWidget(parent.weak_against, lenwt+3,2,1,1)
    
    parent.class_criteria = QPushButton("Class Criteria")
    parent.class_criteria.setMinimumHeight(40)
    parent.class_criteria.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
    parent.class_criteria.setToolTip("If classes are criteria based (%) instead of level based, set Minimum Level to 0 and use this instead.")
    parent.class_criteria.setFont(parent.body_font)
    parent.class_criteria.clicked.connect(parent.criteria_dialog)
    working_tab_layout.addWidget(parent.class_criteria, lenwt+3,3,1,1)

    parent.stat_bonuses = QPushButton("Stats+")
    parent.stat_bonuses.setMinimumHeight(40)
    parent.stat_bonuses.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
    parent.stat_bonuses.setToolTip("When a unit switches to this class, they can gain a set stat bonus.")
    parent.stat_bonuses.setFont(parent.body_font)
    parent.stat_bonuses.clicked.connect(parent.stat_bonuses_dialog)
    working_tab_layout.addWidget(parent.stat_bonuses, lenwt+4,0,1,1)

    parent.next_classes = QPushButton("Next Classes")
    parent.next_classes.setMinimumHeight(40)
    parent.next_classes.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
    parent.next_classes.setToolTip("If using Branching Classes, set what classes come after this one.\nOtherwise, this can be ignored.\n(Set Branching Classes in the Game Editor)")
    parent.next_classes.setFont(parent.body_font)
    parent.next_classes.clicked.connect(parent.next_classes_dialog)
    working_tab_layout.addWidget(parent.next_classes, len(wt)+4,1,1,1)
    
    parent.graphics = QPushButton("Graphics")
    parent.graphics.setMinimumHeight(40)
    parent.graphics.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
    parent.graphics.setToolTip("Change sprites/portraits for this class")
    parent.graphics.setFont(parent.body_font)
    parent.graphics.clicked.connect(parent.class_graphics_dialog)
    working_tab_layout.addWidget(parent.graphics, len(wt)+4,2,1,1)

    parent.wt_checkboxes = {}
    parent.wt_checkboxes_right = {}
    count = 1

    for w in wt:
        count += 1
        parent.wt_checkboxes[w] = QCheckBox()
        parent.wt_checkboxes[w].setToolTip("Click to toggle type "+w)
        parent.wt_checkboxes[w].name = w
        parent.wt_checkboxes[w].stateChanged.connect(parent.weapon_type_toggle)
        
        parent.loaded_class.disallowed_weapon_types.append(w)
        label = QLabel(w)
        label.setFont(parent.body_font)
        
        working_tab_layout.addWidget(label, count, 0, 1, 1)
        working_tab_layout.addWidget(parent.wt_checkboxes[w], count, 1, 1, 1)
        
        working_tab_layout.setColumnStretch(0, 3)
        working_tab_layout.setColumnStretch(1, 3)
        working_tab_layout.setColumnStretch(2, 3)
        working_tab_layout.setColumnStretch(3, 3)
    
    parent.createClass()
   
def initUnique(parent):
    working_tab = parent.tabs_dict["Unique Skills/Tactics/Objects"]
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

def initRelationships(parent):
    working_tab = parent.tabs_dict["Relationships"]
    working_tab_layout = working_tab.layout()
    
    team_supports = QWidget()
    team_supports_layout = QHBoxLayout()
    team_supports.setLayout(team_supports_layout)
    
    team_supports_list = QWidget()
    team_supports_list_layout = QVBoxLayout()
    team_supports_list.setLayout(team_supports_list_layout)
    
    team_member_list_label = QLabel("Team Members")
    team_member_list_label.setFont(parent.body_font)
    
    parent.team_member_list = QListWidget()
    parent.team_member_list.setFont(parent.body_font)
    parent.team_member_list.setMinimumWidth(160)
    parent.team_member_list.setMaximumWidth(260)
    parent.team_member_list.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: "+active_theme.list_background_color)
    parent.team_member_list.currentTextChanged.connect(parent.team_member_change)
    
    team_supports_list_layout.addWidget(team_member_list_label)
    team_supports_list_layout.addWidget(parent.team_member_list)
    
    team_supports_layout.addWidget(team_supports_list)
    
    supports_setup = QWidget()
    supports_setup.setMinimumWidth(400)
    parent.supports_setup_layout = QVBoxLayout()
    
    parent.relationship_label = QLabel("Relationship with team member")
    parent.relationship_label.setFont(parent.body_font)
    parent.relationship_label.setAlignment(Qt.AlignCenter)
    parent.supports_setup_layout.addWidget(parent.relationship_label)
    
    parent.max_support_level_label = QLabel("Max support level")
    parent.max_support_level_label.setFont(parent.body_font)
    parent.max_support_level_label.setAlignment(Qt.AlignCenter)
    parent.supports_setup_layout.addWidget(parent.max_support_level_label)
    
    parent.max_support_level_widget = QWidget()
    parent.max_support_level_widget_layout = QHBoxLayout()
    parent.max_support_level_widget.setLayout(parent.max_support_level_widget_layout)
    
    parent.max_support_level_D = QRadioButton("D")
    parent.max_support_level_C = QRadioButton("C")
    parent.max_support_level_B = QRadioButton("B")
    parent.max_support_level_A = QRadioButton("A")
    parent.max_support_level_S = QRadioButton("S")
    
    parent.max_support_radio_buttons = [parent.max_support_level_D, parent.max_support_level_C,
                                      parent.max_support_level_B, parent.max_support_level_A,
                                      parent.max_support_level_S]
    
    
    for rb in parent.max_support_radio_buttons:
        rb.clicked.connect(parent.max_support_changed)
        rb.setFont(parent.body_font)
    
    parent.max_support_level_widget_layout.addWidget(parent.max_support_level_D)
    parent.max_support_level_widget_layout.addWidget(parent.max_support_level_C)
    parent.max_support_level_widget_layout.addWidget(parent.max_support_level_B)
    parent.max_support_level_widget_layout.addWidget(parent.max_support_level_A)
    parent.max_support_level_widget_layout.addWidget(parent.max_support_level_S)
    
    parent.supports_setup_layout.addWidget(parent.max_support_level_widget)
    
    parent.support_difficulty_slider = QSlider(Qt.Horizontal)
    parent.support_difficulty_slider.setFixedWidth(300)
    parent.support_difficulty_slider.valueChanged.connect(parent.colorizeSliderB)
    parent.support_difficulty_slider.setValue(5)
    parent.support_difficulty_slider.setRange(0,10)
    parent.support_difficulty_slider.setSingleStep(1)
    
    support_difficulty_widget = QWidget()
    support_difficulty_layout = QHBoxLayout()
    support_difficulty_widget.setLayout(support_difficulty_layout)
    
    hate_label = QLabel("Intensely Dislikes \n(Builds support very slowly)")
    love_label = QLabel("Intensely Likes \n(Builds support very quickly)")
    hate_label.setFont(parent.body_font)
    love_label.setFont(parent.body_font)
    
    support_difficulty_layout.addWidget(hate_label)
    support_difficulty_layout.addWidget(parent.support_difficulty_slider)
    support_difficulty_layout.addWidget(love_label)
    
    parent.supports_setup_layout.addWidget(support_difficulty_widget)
    
    parent.supports_setup_layout.addSpacerItem(QSpacerItem(1, 200))
    
    spacer_label = QLabel("--------------------------------------------------------------------------------")
    d_color = QColor(active_theme.window_background_color).darker(125).name()

    spacer_label.setStyleSheet("font-size: "+str(data["font_size"])+"px; color: "+str(d_color))
    spacer_label.setAlignment(Qt.AlignCenter)
    parent.supports_setup_layout.addWidget(spacer_label)
    
    parent.supports_setup_layout.addSpacerItem(QSpacerItem(1, 200))
    
    personal_enemy_widget = QWidget()
    personal_enemy_layout = QHBoxLayout()
    personal_enemy_widget.setLayout(personal_enemy_layout)
    
    parent.personal_enemy_label = QLabel("Personal enemy\n--None--")
    parent.personal_enemy_label.setFont(parent.body_font)
    parent.personal_enemy = QListWidget()
    parent.personal_enemy.setFont(parent.body_font)
    parent.personal_enemy.setFixedWidth(300)
    parent.personal_enemy.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: "+active_theme.list_background_color)
    parent.personal_enemy.currentTextChanged.connect(parent.personal_enemy_changed)
    
    personal_enemy_layout.addWidget(parent.personal_enemy_label)
    personal_enemy_layout.addWidget(parent.personal_enemy)
    
    parent.supports_setup_layout.addWidget(personal_enemy_widget)
    
    supports_setup.setLayout(parent.supports_setup_layout)
    
    working_tab_layout.addWidget(team_supports)
    working_tab_layout.addWidget(supports_setup)
