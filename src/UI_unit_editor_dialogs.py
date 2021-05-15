from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QPalette, QIcon, QPixmap, QCursor, QFont
from src.UI_updateJSON import updateJSON
import src.UI_colorTheme
import shutil, os, pickle, json, sys
from src.UI_Dialogs import confirmAction

class growthRateDialog(QDialog):
    def __init__(self, parent=None):
        data = updateJSON()
        self.parent = parent
        self.restart = False
        self.active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        super().__init__(parent)
        self.setMinimumWidth(500)
        
        self.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(8,8,8,8)
        
        with open("src/skeletons/universal_stats.json", "r") as stats_file:
            universal_stats =  json.load(stats_file)
        
        for s in universal_stats:
            self.parent.unit.unit_class.growth_rates[s] = 60
        
        self.list = QListWidget()
        self.list.currentTextChanged.connect(self.list_change)
        self.list.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: "+self.active_theme.list_background_color+";color: "+self.active_theme.window_text_color)
        self.list.addItems(universal_stats)
        
        self.layout.addWidget(self.list)
        
        row = QWidget()
        row_layout = QHBoxLayout()
        row.setLayout(row_layout)
        
        row_layout.addWidget(QLabel("0%\n(never increase)"))
        
        self.rate_slider = QSlider(Qt.Horizontal)
        self.rate_slider.name = 1
        self.rate_slider.valueChanged.connect(self.colorizeSlider)
        self.rate_slider.setValue(50)
        self.rate_slider.setRange(0,99)
        self.rate_slider.setSingleStep(1)
        
        row_layout.addWidget(self.rate_slider)
        
        row_layout.addWidget(QLabel("100%\n(always increase)"))
        
        self.layout.addWidget(row)
        
        self.setLayout(self.layout)
    
    def colorizeSlider(self, v):
        try:
            self.parent.unit.unit_class.growth_rates[self.list.currentItem().text()] = v
            self.parent.unit.unit_class.selfToJSON("src/skeletons/classes/"+self.class_name.currentText()+".tructf")
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
        self.rate_slider.setValue(self.parent.unit.unit_class.growth_rates[self.list.currentItem().text()])
        
class statBonusDialog(QDialog):
    def __init__(self, parent=None):
        data = updateJSON()
        self.parent = parent
        self.restart = False
        self.active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        super().__init__(parent)
        self.setMinimumWidth(200)
        
        self.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(8,8,8,8)
        
        with open("src/skeletons/universal_stats.json", "r") as stats_file:
            universal_stats =  json.load(stats_file)
        
        self.rows = {}
        self.labels = {}
        self.values = {}
        
        for s in universal_stats:
            if s not in self.parent.unit.unit_class.stat_bonuses:
                self.parent.unit.unit_class.stat_bonuses[s] = 0
            row = QWidget()
            row_layout = QHBoxLayout()
            row.setLayout(row_layout)
            
            self.rows[s] = row
            
            label = QLabel(s)
            self.labels[s] = label
            row_layout.addWidget(label)
            
            value = QSpinBox()
            value.name = s
            value.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: "+self.active_theme.list_background_color+";color: "+self.active_theme.window_text_color)
            value.setRange(0,10)
            value.setValue(self.parent.unit.unit_class.stat_bonuses[s])
            value.valueChanged.connect(self.value_changed)
            self.values[s] = value
            row_layout.addWidget(value)
            
            self.layout.addWidget(row)
            
        self.setLayout(self.layout)
        
    def value_changed(self):
        try:
            self.parent.unit.unit_class.stat_bonuses[self.sender().name] = self.sender().value()
            self.parent.unit.unit_class.selfToJSON("src/skeletons/classes/"+self.class_name.currentText()+".tructf")
        except:
            pass

class AIHelpDialog(QDialog):
    def __init__(self, parent=None):
        data = updateJSON()

        self.active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        super().__init__(parent)
        
        self.setMinimumWidth(1080)
        self.setMinimumHeight(600)
        self.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
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
            
class editUniversalWeaponTypes(QDialog):
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
        
        with open("src/skeletons/universal_weapon_types.json", "r") as weapons_file:
            weapon_types = json.load(weapons_file)
        
        self.list = QListWidget()
        self.list.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: "+self.active_theme.list_background_color+";color: "+self.active_theme.window_text_color)
        self.list.addItems(weapon_types)
    
        row_layout.addWidget(self.list)
        
        row2 = QWidget()
        row2_layout = QHBoxLayout()
        row2.setLayout(row2_layout)
        
        self.add_stat_name = QLineEdit()
        self.add_stat_name.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.add_stat_name.setPlaceholderText("New weapon type name")
        
        self.add_stat = QPushButton("+Add Weapon Type")
        self.add_stat.clicked.connect(self.addType)
        
        self.remove_stat = QPushButton("-Remove Selected Weapon Type")
        self.remove_stat.clicked.connect(self.removeType)
        
        row2_layout.addWidget(self.add_stat_name)
        row2_layout.addWidget(self.add_stat)
        row2_layout.addWidget(self.remove_stat)
        
        self.layout.addWidget(row)
        self.layout.addWidget(row2)
        
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
            self.parent.unit.removeUniversalWeaponsType(self.list.currentItem().text())
            self.close()
            self.restart = True
        