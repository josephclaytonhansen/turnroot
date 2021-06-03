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
from src.UI_TableModel import TableModel
from src.skeletons.weapon_types import weaponTypes, expTypes
from src.UI_unit_editor_more_dialogs import testGrowthDialog

class growthRateDialog(QDialog):
    def __init__(self, parent=None,font=None):
        data = updateJSON()
        self.parent = parent
        self.restart = False
        self.body_font = font
        self.active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        super().__init__(parent)
        self.setMinimumWidth(600)
        
        self.setStyleSheet("background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(8,8,8,8)
        
        with open("src/skeletons/universal_stats.json", "r") as stats_file:
            universal_stats =  json.load(stats_file)
        
        for s in universal_stats:
            try:
                self.parent.loaded_class.growth_rates[s] = self.parent.loaded_class.growth_rates[s]
            except:
                with open("src/tmp/dugc.tsgr") as f:
                    f_data = json.load(f)
                self.parent.unit.growth_rates[s] = f_data[s]
        
        self.list = QListWidget()
        self.list.setFont(self.body_font)
        self.list.currentTextChanged.connect(self.list_change)
        self.list.setStyleSheet("background-color: "+self.active_theme.list_background_color+";color: "+self.active_theme.window_text_color)
        self.list.addItems(universal_stats)
        
        self.layout.addWidget(self.list)
        
        row = QWidget()
        row_layout = QHBoxLayout()
        row.setLayout(row_layout)
        
        r0 = QLabel("0%\n(never increase)")
        r0.setFont(self.body_font)
        row_layout.addWidget(r0)
        
        self.rate_slider = QSlider(Qt.Horizontal)
        self.rate_slider.setTickPosition(3)
        self.rate_slider.setTickInterval(10)
        self.rate_slider.name = 1
        self.rate_slider.valueChanged.connect(self.colorizeSlider)
        self.rate_slider.setValue(50)
        self.rate_slider.setRange(0,99)
        self.rate_slider.setSingleStep(1)
        
        row_layout.addWidget(self.rate_slider)
        
        r1 = QLabel("100%\n(always increase)")
        r1.setFont(self.body_font)
        row_layout.addWidget(r1)
        
        self.layout.addWidget(row)

        self.setLayout(self.layout)
    
    def colorizeSlider(self, v):
        try:
            self.parent.loaded_class.growth_rates[self.list.currentItem().text()] = v
            self.parent.loaded_class.selfToJSON("src/skeletons/classes/"+self.class_name.text()+".tructf")
        except:
            pass
            
        v = v / 100
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
    
    def list_change(self):
        try:
            self.rate_slider.setValue(self.parent.loaded_class.growth_rates[self.list.currentItem().text()])
        except:
            self.rate_slider.setValue(50)
        
class statBonusDialog(QDialog):
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
        self.layout.setContentsMargins(8,8,8,8)
        
        with open("src/skeletons/universal_stats.json", "r") as stats_file:
            universal_stats =  json.load(stats_file)
        
        self.rows = {}
        self.labels = {}
        self.values = {}
        
        for s in universal_stats:
            if s not in self.parent.loaded_class.stat_bonuses:
                self.parent.loaded_class.stat_bonuses[s] = 0
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
            value.setRange(0,10)
            value.setValue(self.parent.loaded_class.stat_bonuses[s])
            value.valueChanged.connect(self.value_changed)
            self.values[s] = value
            row_layout.addWidget(value)
            
            self.layout.addWidget(row)
            
        self.setLayout(self.layout)
        
    def value_changed(self):
        try:
            self.parent.loaded_class.stat_bonuses[self.sender().name] = self.sender().value()
            self.parent.loaded_class.selfToJSON("src/skeletons/classes/"+self.class_name.text()+".tructf")
        except:
            pass

class AIHelpDialog(QDialog):
    def __init__(self, parent=None,font=None):
        data = updateJSON()
        self.font=font

        self.active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        super().__init__(parent)
        
        self.setMinimumWidth(1080)
        self.setMinimumHeight(600)
        self.setStyleSheet("background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.layout = QVBoxLayout()

        self.setLayout(self.layout)
        
        self.tabs = QTabWidget()
        
        self.tabs.setTabPosition(QTabWidget.North)
        
        self.tscroll = QScrollArea()
        self.tscroll.setWidget(self.tabs)
        self.tscroll.setWidgetResizable(True)
        
        self.layout.addWidget(self.tscroll)
        
        self.tab_names = ["Move Towards", "Move Goals", "Targeting", "Target Change", "Avoid", "Tiles"]
        
        self.tabs_dict = {}
        for tab in self.tab_names:
            self.tab_title = tab
            self.c_tab = QWidget()
            self.c_tab_layout = QVBoxLayout()
            self.c_tab.setLayout(self.c_tab_layout)
            self.tabs_dict[tab] = self.c_tab
            self.tabs.addTab(self.c_tab, self.tab_title)
        
        self.initMT()
        self.initMG()
        self.initT()
        self.initTC()
        self.initA()
        self.initTi()
        
    def initMT(self):
        self.working_tab = self.tabs_dict["Move Towards"]
        self.working_tab_layout = self.working_tab.layout()
        self.working_tab_layout.setSpacing(0)
        
        img_label = QLabel()
        img_label.setPixmap(QPixmap("src/ui_images/move_towards.png"))
        img_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.working_tab_layout.addWidget(img_label)
        instructions = [
            "A move towards rule influences what object, state, or unit this unit moves towards.\n",
            "As the chart shows, each rule can only move towards one of the above (object, state, or unit.)\n",
            "Units are the simplest. For a foe, describe the foe with an adjective and  add \"foe\" to the end.",
            "For an ally/team member, choose an adjective and add \"ally\". for example- \"injured ally\".",
            "For example, \"nearest foe\" would be the nearest enemy unit. The chart shows the allowed unit descriptions.\n",
            "State describes the state the unit will be in if they move. States can either be \"safety\" or \"in/not in range of\".",
            "\"safety\" means the unit is out of danger. As for range: \"not in range of arrows\" means the unit is avoiding as many arrows as possible.\n",
            "Lastly, units can move towards objects. The format for this is object + \"if can/ if can not\" + take action.",
            "For example, \"chest if can open\" will move towards chests, if they can be opened by the unit."
            ]
        for t in instructions:
            v = instructions.index(t) / len(instructions)
            color_left = QColor(self.active_theme.node_outliner_label_0)
            color_right = QColor(self.active_theme.node_outliner_label_1)
            color_left_c = [color_left.red(), color_left.green(), color_left.blue()]
            color_right_c = [color_right.red(), color_right.green(), color_right.blue()]
        
            distances = [(color_right.red() - color_left.red()),
                     (color_right.green() - color_left.green()),
                     (color_right.blue() - color_left.blue())]
        
            new_color = [int(color_left.red() + v * distances[0]),
                     int(color_left.green() + v * distances[1]),
                     int(color_left.blue()+ v * distances[2])]
            
            g = QLabel(t)
            g.setFont(self.font)
            g.setStyleSheet("color: "+str(QColor(new_color[0],new_color[1],new_color[2]).name()))
            self.working_tab_layout.addWidget(g)

    def initMG(self):
        self.working_tab = self.tabs_dict["Move Goals"]
        self.working_tab_layout = self.working_tab.layout()
        self.working_tab_layout.setSpacing(0)
        
        instructions = [
            "A move towards rule influence what the unit wants to accomplish by moving.\n",
            "Movement goals are very simple- there's only a few.\n",
            "\"stay in group\" means the unit will try to stay close to its allies.",
            "\"alone\" is the direct opposite, where the unit will try to stay alone.\n",
            "After those two, the movement goals follow the format of \"maximize/minimize\" + \"given damage/received damage/movement/visibility\".",
            "For example, \"maximize movement\" means the unit wants to move as much as it can every turn.",
            "Another example- \"minimize received damage\" means the unit wants to take as little damage as possible.",
            "\"minimize visibility\" means the unit will try to be targeted as little as possible, and \"maximize visiblity\" means they are front and center.",
            ]
        for t in instructions:
            v = instructions.index(t) / len(instructions)
            color_left = QColor(self.active_theme.node_outliner_label_0)
            color_right = QColor(self.active_theme.node_outliner_label_1)
            color_left_c = [color_left.red(), color_left.green(), color_left.blue()]
            color_right_c = [color_right.red(), color_right.green(), color_right.blue()]
        
            distances = [(color_right.red() - color_left.red()),
                     (color_right.green() - color_left.green()),
                     (color_right.blue() - color_left.blue())]
        
            new_color = [int(color_left.red() + v * distances[0]),
                     int(color_left.green() + v * distances[1]),
                     int(color_left.blue()+ v * distances[2])]
            
            g = QLabel(t)
            g.setFont(self.font)
            g.setStyleSheet("color: "+str(QColor(new_color[0],new_color[1],new_color[2]).name()))
            self.working_tab_layout.addWidget(g)
    
    def initTC(self):
        self.working_tab = self.tabs_dict["Target Change"]
        self.working_tab_layout = self.working_tab.layout()
        self.working_tab_layout.setSpacing(0)
        
        img_label = QLabel()
        img_label.setPixmap(QPixmap("src/ui_images/target_change.png"))
        img_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.working_tab_layout.addWidget(img_label)
        instructions = [
            "A target change rule shifts focus from an enemy to a different one. If attacking isn't the final decision, this may have no apparent effect.\n",
            "These rules start with \"new target\" or \"last target\", followed by \"is/is not\", than a condition. ",
            "\"new target\" refers to a potential new enemy to shift focus to, \"last target\" is the enemy current focused on.",
            "For example, \"new target is disadvantaged\" means that this unit will switch focus if they can gain the upper hand on a new enemy.",
            "Or \"last target is killable\" would keep focus on the current enemy if this unit has a good chance of killing them with the next attack.",
            "\"personal enemy\" allows a unit to target especially hated foes- these can be defined in the Relationships tab of the Unit Editor.",
            ]
        for t in instructions:
            v = instructions.index(t) / len(instructions)
            color_left = QColor(self.active_theme.node_outliner_label_0)
            color_right = QColor(self.active_theme.node_outliner_label_1)
            color_left_c = [color_left.red(), color_left.green(), color_left.blue()]
            color_right_c = [color_right.red(), color_right.green(), color_right.blue()]
        
            distances = [(color_right.red() - color_left.red()),
                     (color_right.green() - color_left.green()),
                     (color_right.blue() - color_left.blue())]
        
            new_color = [int(color_left.red() + v * distances[0]),
                     int(color_left.green() + v * distances[1]),
                     int(color_left.blue()+ v * distances[2])]
            
            g = QLabel(t)
            g.setFont(self.font)
            g.setStyleSheet("color: "+str(QColor(new_color[0],new_color[1],new_color[2]).name()))
            self.working_tab_layout.addWidget(g)

    def initT(self):
        self.working_tab = self.tabs_dict["Targeting"]
        self.working_tab_layout = self.working_tab.layout()
        self.working_tab_layout.setSpacing(0)
        
        instructions = [
            "A targeting rule influences who to focus attacks on. If attacking isn't the final decision, this may have no apparent effect.\n",
            "These rules are very simple: the possible options are \"disadvantaged foe\", \"visible foe\", \"killable foe\",\n \"protagonist\", \"nearest foe\", \"furthest foe\", and \"personal enemy\".",
            "See Target Change guidelines for more info on these.\n",
            "What's the difference between Targeting and Target Change? In practice, not much- both influence targeting decisions.",
            "They are very similar and work very closely together. It's generally a good idea to have similar Targeting and Target Change rules."
            ]
        for t in instructions:
            v = instructions.index(t) / len(instructions)
            color_left = QColor(self.active_theme.node_outliner_label_0)
            color_right = QColor(self.active_theme.node_outliner_label_1)
            color_left_c = [color_left.red(), color_left.green(), color_left.blue()]
            color_right_c = [color_right.red(), color_right.green(), color_right.blue()]
        
            distances = [(color_right.red() - color_left.red()),
                     (color_right.green() - color_left.green()),
                     (color_right.blue() - color_left.blue())]
        
            new_color = [int(color_left.red() + v * distances[0]),
                     int(color_left.green() + v * distances[1]),
                     int(color_left.blue()+ v * distances[2])]
            
            g = QLabel(t)
            g.setFont(self.font)
            g.setStyleSheet("color: "+str(QColor(new_color[0],new_color[1],new_color[2]).name()))
            self.working_tab_layout.addWidget(g)
            
    def initA(self):
        self.working_tab = self.tabs_dict["Avoid"]
        self.working_tab_layout = self.working_tab.layout()
        self.working_tab_layout.setSpacing(0)
        
        img_label = QLabel()
        img_label.setPixmap(QPixmap("src/ui_images/avoid.png"))
        img_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.working_tab_layout.addWidget(img_label)
        instructions = [
            "An avoid rule tells units which tiles to move away from.\n",
            "These rules start with \"tile\" or \"door\", then \"if\", then the condition\n",
            "Doors have one rule- \"door if shut\". This means closed doors will be avoided.",
            "Another essential rule is \"tile if stop\". This means that tiles that stop movement- like chasms- will be avoided.",
            "\nNote that by default, \"tile if stop\" is set to ALWAYS!, but \"door if shut\" is not.",
            "This is because a closed door can be opened by the unit, but a stop tile can't change.",
            "So avoiding closed doors always would mean that doors could never be opened.",
            "\n\"slow\" indicates tiles that slow the unit down, and \"hurt\" indicates tiles that hurt the unit.",
            ]
        for t in instructions:
            v = instructions.index(t) / len(instructions)
            color_left = QColor(self.active_theme.node_outliner_label_0)
            color_right = QColor(self.active_theme.node_outliner_label_1)
            color_left_c = [color_left.red(), color_left.green(), color_left.blue()]
            color_right_c = [color_right.red(), color_right.green(), color_right.blue()]
        
            distances = [(color_right.red() - color_left.red()),
                     (color_right.green() - color_left.green()),
                     (color_right.blue() - color_left.blue())]
        
            new_color = [int(color_left.red() + v * distances[0]),
                     int(color_left.green() + v * distances[1]),
                     int(color_left.blue()+ v * distances[2])]
            
            g = QLabel(t)
            g.setFont(self.font)
            g.setStyleSheet("color: "+str(QColor(new_color[0],new_color[1],new_color[2]).name()))
            self.working_tab_layout.addWidget(g)
            
    def initTi(self):
        self.working_tab = self.tabs_dict["Tiles"]
        self.working_tab_layout = self.working_tab.layout()
        self.working_tab_layout.setSpacing(0)
        
        instructions = [
            "Tile rules determine how the unit interacts with tiles.\n",
            "These rules take the tile type and set a status or result. To set multiple, use a comma: \"stop,blind\".",
            "You can change the amount of attributes \"slow\", \"hurt\", \"avoid\", \"guard\", and \"heal\" by adding \"*\" and a number.",
            "For example, \"slow * .5\" means this tile type slows half as much as a tile type set to \"slow\".\n",
            "\"move\" means the unit can move on this tile type.",
            "\"stop\" means the unit cannot move on this tile type.",
            "\"blind\" means that visibility is cut off by this tile type.",
            "\"hurt_if_enter\" means the unit takes immediate damage when moving to this tile type.",
            "\"hurt_if_stay\" means the unit takes damage at the beginning of each turn standing on ",
            "\"shut\" means the unit can't move onto the tile unless the item (door/chest) is opened.",
            "\"open_if_item\" and \"open_if_skilled\" allow shut tiles to be opened.",
            "\"teleport\" is for warp tiles- stepping onto the tile will move the unit to a different tile.",
            "\"use_if_skilled\" is for emplacements- tiles that can do damage to enemies.",
            "\"heal\" heals the unit at the beginning of each turn standing on the tile.",
            "\"use_if_safe\" is for switches or levers- the unit will use the switch if they're not on a trap tile.",
            "\"guard\" raises defense when standing on this tile.",
            "\"avoid\" raises dodge change (dexterity) when standing on this tile.",
            "\"empower\" raises strength and magic when standing on this tile type."
            ]
        for t in instructions:
            v = instructions.index(t) / len(instructions)
            color_left = QColor(self.active_theme.node_outliner_label_0)
            color_right = QColor(self.active_theme.node_outliner_label_1)
            color_left_c = [color_left.red(), color_left.green(), color_left.blue()]
            color_right_c = [color_right.red(), color_right.green(), color_right.blue()]
        
            distances = [(color_right.red() - color_left.red()),
                     (color_right.green() - color_left.green()),
                     (color_right.blue() - color_left.blue())]
        
            new_color = [int(color_left.red() + v * distances[0]),
                     int(color_left.green() + v * distances[1]),
                     int(color_left.blue()+ v * distances[2])]
            
            g = QLabel(t)
            g.setFont(self.font)
            g.setStyleSheet("color: "+str(QColor(new_color[0],new_color[1],new_color[2]).name()))
            self.working_tab_layout.addWidget(g)


class editUniversalStats(QDialog):
    def __init__(self, parent=None):
        data = updateJSON()
        self.parent = parent
        self.restart = False
        self.active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        super().__init__(parent)
        
        self.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(8,8,8,8)
        
        row = QWidget()
        row_layout = QHBoxLayout()
        row.setLayout(row_layout)
        
        with open("src/skeletons/universal_stats.json", "r") as stats_file:
            universal_stats =  json.load(stats_file)
        
        self.list = QListWidget()
        self.list.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: "+self.active_theme.list_background_color+";color: "+self.active_theme.window_text_color)
        self.list.addItems(universal_stats)
    
        row_layout.addWidget(self.list)
        
        row2 = QWidget()
        row2_layout = QHBoxLayout()
        row2.setLayout(row2_layout)
        
        self.add_stat_name = QLineEdit()
        self.add_stat_name.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.add_stat_name.setPlaceholderText("New stat name")
        
        self.add_stat = QPushButton("+Add Stat")
        self.add_stat.clicked.connect(self.addStat)
        
        self.remove_stat = QPushButton("-Remove Selected Stat")
        self.remove_stat.clicked.connect(self.removeStat)
        
        row2_layout.addWidget(self.add_stat_name)
        row2_layout.addWidget(self.add_stat)
        row2_layout.addWidget(self.remove_stat)
        
        self.layout.addWidget(row)
        self.layout.addWidget(row2)
        
        self.setLayout(self.layout)
    
    def addStat(self):
        c = confirmAction("#This will add this stat to all units in the game, do you want to continue?", parent=self)
        c.exec_()
        if(c.return_confirm):
            self.parent.unit.createUniversalStat(self.add_stat_name.text())
            self.restart = True
            self.close()
    
    def removeStat(self):
        c = confirmAction("#This will remove this stat from all units in the game, do you want to continue?",parent=self)
        c.exec_()
        if(c.return_confirm):
            self.parent.unit.removeUniversalStat(self.list.currentItem().text())
            self.restart = True
            self.close()

class classSkillDialog(QDialog):
    def __init__(self, parent=None,font=None):
        data = updateJSON()
        self.parent = parent
        self.restart = False
        self.active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        super().__init__(parent)
        self.body_font = font
        
        self.setStyleSheet("background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.layout = QGridLayout()
        self.layout.setContentsMargins(8,8,8,8)
        self.setLayout(self.layout)
        
        #fromRow, int fromColumn, int rowSpan, int columnSpan
        
        self.skill_list = QListWidget()
        self.skill_list.currentTextChanged.connect(self.row_changed)
        self.skill_list.setFont(self.body_font)
        self.skill_list.setIconSize(QSize(56,56))
        self.layout.addWidget(self.skill_list, 0,0,2,2)
        
        self.all_skills = self.getSkillsInFolder()
        
        with open("src/skill_graphics/skill_graphics.txt", "r") as f:
            g_data = json.load(f)
        
        self.outer = g_data[0]
        self.inner = g_data[1]
        self.inner2 = g_data[2]
        self.level_values = {}
        self.level = QSpinBox()
        self.level.setValue(0)
        self.fillList()
            
        if len(self.parent.loaded_class.skills) == 0:
            self.skill_list.addItem("No skills connected to class")
            self.level_values["No skills connected to class"] = 0
        
        self.level_label = QLabel("Unlock Level")
        self.level_label.setFont(self.body_font)
        
        self.level.setFont(self.body_font)
        self.level.valueChanged.connect(self.skill_changed)
        self.level.setRange(0,30)

        
        self.layout.addWidget(self.level_label, 2, 0, 1, 1)
        self.layout.addWidget(self.level, 2,1,1,1)
        
        self.remove = QPushButton()
        self.remove.setToolTip("Unlink skill from class")
        self.remove.setIcon(QIcon(QPixmap("src/ui_icons/white/dl.png").scaled(48,48, Qt.KeepAspectRatio)))
        self.remove.setIconSize(QSize(32,32))
        self.remove.setMinimumWidth(52)
        self.remove.setMinimumHeight(52)
        self.remove.setMaximumHeight(52)
        self.remove.clicked.connect(self.remove_skill)
        
        self.layout.addWidget(self.remove, 3, 0, 1,1)
        
        self.add = QPushButton()
        self.add.setToolTip("Create/Edit Skills")
        self.add.setIcon(QIcon(QPixmap("src/ui_icons/white/add.png").scaled(48,48, Qt.KeepAspectRatio)))
        self.add.setIconSize(QSize(32,32))
        self.add.setMinimumWidth(52)
        self.add.setMinimumHeight(52)
        self.add.setMaximumHeight(52)
        self.add.clicked.connect(self.add_skill)
        
        self.layout.addWidget(self.add, 3, 1, 1,1)
         
    def skill_changed(self, i):
        try:
            self.parent.loaded_class.skill_criteria[self.skill_list.currentItem().text()] = i
            self.level_values[self.skill_list.currentItem().text()] = self.level.value()
            self.parent.loaded_class.selfToJSON("src/skeletons/classes/"+self.parent.loaded_class.unit_class_name+".tructf")
        except:
            print("no skills in list")
    
    def row_changed(self,s):
        self.level.setValue(self.level_values[self.skill_list.currentItem().text()])
        
    def remove_skill(self):
        try:
            self.parent.loaded_class.skills.remove(self.skill_list.currentItem().text())
            self.parent.loaded_class.selfToJSON("src/skeletons/classes/"+self.parent.loaded_class.unit_class_name+".tructf")
            self.fillList()
        except:
            pass
    
    def add_skill(self):
       self.parent.parent().setCurrentWidget(self.parent.parent().parent().skills_editor)
       self.close()
        

    def getSkillsInFolder(self):
        file_list = getFiles("src/")[GET_FILES]
        skills = {}
        for f in file_list:
            if f.ext.strip() == ".trnep":
                skills[f.path[f.path.rfind("/")+1:f.path.find(".trnep")]] = f.path
        return skills

    def fillList(self):
        self.skill_list.clear()
        count = 0
        for d in self.parent.loaded_class.skills:
            count +=1
            if d in self.parent.loaded_class.skill_criteria:
                self.level_values[d] = self.parent.loaded_class.skill_criteria[d]
            else:
                self.level_values[d] = 0
            if count == 1:
                self.level_values[count] = self.level_values[d]
            list_item = QListWidgetItem()

            with open(self.all_skills[d], "r") as f:
                s = json.load(f)
            or_index = s["icon"][0]
            ir_index= s["icon"][1]
            ic_index= s["icon"][2]
            
            pixmap = QPixmap(56,56)
            pixmap.fill(Qt.transparent)
            p = overlayTile(pixmap, self.outer[or_index], 56)
            g = overlayTile(p, self.inner[ir_index], 56)
            r = overlayTile(g, self.inner2[ic_index], 56)
            pixmap = QIcon(r)
            list_item.setIcon(pixmap)
            
            self.skill_list.addItem(list_item)
            
            list_item.setText(d)
        try:
            self.level.setValue(self.level_values[1])
        except:
            pass
        self.level.update()
        
class loadSavedClass(QDialog):
    def __init__(self, parent=None,font=None):
        data = updateJSON()
        self.parent = parent
        self.restart = False
        self.active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        super().__init__(parent)
        self.body_font = font
        
        self.setStyleSheet("background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(8,8,8,8)
        self.setLayout(self.layout)
        
        label = QLabel("Choose Class")
        label.setFont(self.body_font)
        self.layout.addWidget(label)
            
        self.class_list = QListWidget()
        self.class_list.setFont(self.body_font)
        self.layout.addWidget(self.class_list)
        self.class_list.itemClicked.connect(self.change)
        self.getClassesInFolder()
        self.show()
        
    def getClassesInFolder(self):
        file_list = getFiles("src/skeletons/classes")[GET_FILES]
        class_names = []
        global classes
        classes = {}
        self.class_list.clear()
        for f in file_list:
            if f.ext.strip() == ".tructf":
                tmp_class = unitClass()
                tmp_class.selfFromJSON(f.fullPath)
                if tmp_class.unit_class_name not in class_names:
                    class_names.append(tmp_class.unit_class_name)
                    classes[tmp_class.unit_class_name] = tmp_class
            self.classesToDropDown(class_names)
                
    def classesToDropDown(self, class_names):
        self.class_list.clear()
        self.class_list.addItems(class_names)
        self.class_list.update()
    
    def change(self,s):
        self.returns = self.sender().currentItem().text()
        self.close()

class instanceStatDialog(QDialog):
    def __init__(self, parent=None,font=None):
        data = updateJSON()
        self.parent = parent
        self.restart = False
        self.active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        super().__init__(parent)
        self.body_font = font
        
        self.setStyleSheet("background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(8,8,8,8)
        self.setLayout(self.layout)
        self.setMinimumWidth(700)
        
        with open("src/skeletons/universal_stats.json", "r") as stats_file:
            universal_stats =  json.load(stats_file)
        
        for s in universal_stats:
            try:
                self.parent.unit.generic_stat_randomness[s] = self.parent.unit.generic_stat_randomness[s]
                self.parent.unit.generic_stat_randomness_amount[s] = self.parent.unit.generic_stat_randomness_amount[s]
            except:
                self.parent.unit.generic_stat_randomness[s] = 4.5
                self.parent.unit.generic_stat_randomness_amount[s] = 0
        
        self.list = QListWidget()
        self.list.setFont(self.body_font)
        self.list.currentTextChanged.connect(self.list_change)
        self.list.setStyleSheet("background-color: "+self.active_theme.list_background_color+";color: "+self.active_theme.window_text_color)
        self.list.addItems(universal_stats)
        
        self.layout.addWidget(self.list)
        
        row = QWidget()
        row_layout = QHBoxLayout()
        row.setLayout(row_layout)
        
        r0 = QLabel("0%\n(never change from base stat)")
        r0.setFont(self.body_font)
        row_layout.addWidget(r0)
        
        self.rate_slider = QSlider(Qt.Horizontal)
        self.rate_slider.name = 1
        self.rate_slider.valueChanged.connect(self.colorizeSlider)
        self.rate_slider.setValue(4.5)
        self.rate_slider.setRange(0,9)
        self.rate_slider.setSingleStep(0.5)
        
        row_layout.addWidget(self.rate_slider)
        
        r1 = QLabel("100%\n(always change from base stat)")
        r1.setFont(self.body_font)
        row_layout.addWidget(r1)
        
        self.layout.addWidget(row)
        
        row2 = QWidget()
        row2_layout = QHBoxLayout()
        row2.setLayout(row2_layout)
        
        r3 = QLabel("Maximum amount stat can vary by (+/-)")
        r3.setFont(self.body_font)
        r3.setToolTip("For example: If the base stat is 5, and this is set to 2, an instance could have between 3 and 6 (+/-2)")
        self.amount = QSpinBox()
        self.amount.valueChanged.connect(self.changeAmount)
        r3.setFont(self.body_font)
        self.amount.setValue(0)
        self.amount.setRange(0,5)
        
        row2_layout.addWidget(r3)
        row2_layout.addWidget(self.amount)
        
        self.layout.addWidget(row2)
        
        self.setLayout(self.layout)
    
    def colorizeSlider(self, v):
        try:
            self.parent.unit.generic_stat_randomness[self.list.currentItem().text()] = v
            self.parent.unit.selfToJSON(self.parent.path)
        except:
            pass
        v = v / 10
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
    
    def list_change(self):
        self.rate_slider.setValue(self.parent.unit.generic_stat_randomness[self.list.currentItem().text()])
        self.amount.setValue(self.parent.unit.generic_stat_randomness_amount[self.list.currentItem().text()])
    
    def changeAmount(self):
        try:
            self.parent.unit.generic_stat_randomness_amount[self.list.currentItem().text()] = self.amount.value()
            self.parent.unit.selfToJSON(self.parent.path)
        except:
            pass
        
class tileChangesDialog(QDialog):
    def __init__(self, parent=None,font=None,r="dismounted"):
        data = updateJSON()
        self.parent = parent
        self.restart = False
        self.active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        active_theme = self.active_theme
        super().__init__(parent)
        self.body_font = font
        
        self.setMinimumWidth(600)
        self.setMinimumHeight(300)
        self.resize(780,800)
        
        self.setStyleSheet("background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(8,8,8,8)
        self.setLayout(self.layout)
        
        self.sheets = {}
        self.sheetsFromJSON()

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
        
        self.tables = {}

        for t in self.basic_table_categories:
            if t == "Tiles":
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
                
                self.layout.addWidget(table)
            
    def sheetsFromJSON(self):
            with open("src/skeletons/sheets/basic_foot_soldier.json", "r") as rf:
                self.sheets["Foot Soldier"] = json.load(rf)

class unitGrowthRateDialog(QDialog):
    def __init__(self, parent=None,font=None):
        data = updateJSON()
        self.parent = parent
        self.restart = False
        self.body_font = font
        self.active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        super().__init__(parent)
        self.setMinimumWidth(600)
        
        self.setStyleSheet("background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(8,8,8,8)
        
        with open("src/skeletons/universal_stats.json", "r") as stats_file:
            universal_stats =  json.load(stats_file)
        
        for s in universal_stats:
            try:
                self.parent.unit.growth_rates[s] = self.parent.unit.growth_rates[s]
            except:
                with open("src/tmp/dugc.tsgr") as f:
                    f_data = json.load(f)
                self.parent.unit.growth_rates[s] = f_data[s]
        
        self.list = QListWidget()
        self.list.setFont(self.body_font)
        self.list.currentTextChanged.connect(self.list_change)
        self.list.setStyleSheet("background-color: "+self.active_theme.list_background_color+";color: "+self.active_theme.window_text_color)
        self.list.addItems(universal_stats)
        
        self.layout.addWidget(self.list)
        
        row = QWidget()
        row_layout = QHBoxLayout()
        row.setLayout(row_layout)
        
        r0 = QLabel("0%\n(never increase)")
        r0.setFont(self.body_font)
        row_layout.addWidget(r0)
        
        self.rate_slider = QSlider(Qt.Horizontal)
        self.rate_slider.setTickPosition(3)
        self.rate_slider.setTickInterval(10)
        self.rate_slider.name = 1
        self.rate_slider.valueChanged.connect(self.colorizeSlider)
        self.rate_slider.setValue(50)
        self.rate_slider.setRange(0,99)
        self.rate_slider.setSingleStep(1)
        
        row_layout.addWidget(self.rate_slider)
        
        r1 = QLabel("100%\n(always increase)")
        r1.setFont(self.body_font)
        row_layout.addWidget(r1)
        
        self.layout.addWidget(row)
        
        test_rates = QPushButton("Test")
        test_rates.setToolTip("Test growth rates using selected class.\nIf no class is selected, only unit growth rates will be factored in.")
        test_rates.setFont(self.body_font)
        test_rates.clicked.connect(self.test_growth)
        self.layout.addWidget(test_rates)
        
        self.setLayout(self.layout)
    
    def test_growth(self):
        h = testGrowthDialog(parent=self,font=self.body_font)
        h.exec_()
    
    def colorizeSlider(self, v):
        try:
            self.parent.unit.growth_rates[self.list.currentItem().text()] = v
            if self.parent.path != None:
                self.unit.selfToJSON(self.parent.path)
        except:
            pass
            
        v = v / 100
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
    
    def list_change(self):
        self.rate_slider.setValue(self.parent.unit.growth_rates[self.list.currentItem().text()])
        
class classCriteriaDialog(QDialog):
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
        self.setMinimumWidth(600)
        
        self.setStyleSheet("background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.layout = QVBoxLayout()
        
        inner = QWidget()
        inner_layout = QHBoxLayout()
        inner.setLayout(inner_layout)
        
        header = QLabel("To have a 100% chance of gaining class, unit must have:")
        self.layout.addWidget(header)
        header.setFont(self.h_font)
        
        self.layout.addWidget(inner)
        
        self.layout.setContentsMargins(8,8,8,8)
        
        with open("src/skeletons/universal_stats.json", "r") as stats_file:
            universal_stats =  json.load(stats_file)
        
        weapon_types = weaponTypes().data
        exp_types = expTypes().data
        
        stats_column = QWidget()
        stats_column_layout = QVBoxLayout()
        stats_column.setLayout(stats_column_layout)
        
        weapons_column = QWidget()
        weapons_column_layout = QVBoxLayout()
        weapons_column.setLayout(weapons_column_layout)
        
        self.stat_spinners = {}
        self.weapon_spinners = {}
        
        for s in universal_stats:
            stats_row = QWidget()
            stats_row_layout = QHBoxLayout()
            stats_row.setLayout(stats_row_layout)
            
            label = QLabel(s)
            label.setToolTip("Leave at 0 if unrelated to class or if stat is not being used (i.e. endurance)")
            label.setFont(self.body_font)
            stat_amount = QSpinBox()
            stat_amount.name = s
            stat_amount.valueChanged.connect(self.stat_criteria)
            stat_amount.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
            stat_amount.setFont(self.body_font)
            stat_amount.setRange(0,40)
            stat_amount.setValue(0)
            self.stat_spinners[s] = stat_amount
            
            stats_row_layout.addWidget(label)
            stats_row_layout.addWidget(stat_amount)
            
            stats_column_layout.addWidget(stats_row)
        
        for w in weapon_types+exp_types:
            weapons_row = QWidget()
            weapons_row_layout = QHBoxLayout()
            weapons_row.setLayout(weapons_row_layout)
            
            label = QLabel(w)
            label.setToolTip("Leave at E if unrelated to class")
            label.setFont(self.body_font)
            weapon_amount = QComboBox()
            weapon_amount.name = w
            weapon_amount.currentTextChanged.connect(self.weapon_criteria)
            weapon_amount.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
            weapon_amount.setFont(self.body_font)
            weapon_amount.addItems(["E", "E+", "D", "D+", "C", "C+", "B", "B+", "A", "A+", "S"])
            self.weapon_spinners[s] = weapon_amount
            
            weapons_row_layout.addWidget(label)
            weapons_row_layout.addWidget(weapon_amount)
            
            weapons_column_layout.addWidget(weapons_row)
        
        inner_layout.addWidget(stats_column)
        inner_layout.addWidget(weapons_column)
        
        self.setLayout(self.layout)
    
    def stat_criteria(self):
        try:
            self.parent.loaded_class.class_criteria_stats[self.sender().name] = self.sender().value()
            self.parent.loaded_class.selfToJSON("src/skeletons/classes/"+self.parent.loaded_class.unit_class_name+".tructf")
        except:
            pass

    
    def weapon_criteria(self):
        try:
            self.parent.loaded_class.class_criteria_weapon_levels[self.sender().name] = self.sender().currentText()
            self.parent.loaded_class.selfToJSON("src/skeletons/classes/"+self.parent.loaded_class.unit_class_name+".tructf")
        except:
            pass

        