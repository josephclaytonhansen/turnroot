from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from src.skeletons.weapon_types import weaponTypes
from src.skeletons.unit_class import unitClass
from src.UI_TableModel import TableModel
from src.node_backend import getFiles, File

import json, math, random, os

import src.UI_colorTheme as UI_colorTheme
from src.UI_updateJSON import updateJSON
data = updateJSON()
active_theme = getattr(UI_colorTheme, data["active_theme"])

from src.skeletons.unit import Unit, universal_classifications

from src.UI_Dialogs import confirmAction, popupInfo, infoClose
from src.game_directory import gameDirectory
from src.UI_unit_editor_tabs import (initUnit, initBasic, initAI, initWeaponAffinities, initClasses, initUnique, initRelationships, initActions)
from src.UI_unit_editor_dialogs import (growthRateDialog, statBonusDialog, AIHelpDialog, editUniversalStats,
                                        classSkillDialog, loadSavedClass,
                                        instanceStatDialog, tileChangesDialog, unitGrowthRateDialog,
                                        classCriteriaDialog)
from src.UI_unit_editor_more_dialogs import (weakAgainstDialog, expTypesDialog, nextClassesDialog,
                                             classGraphicDialog,editUniversalWeaponTypes, editClassifications, statCapDialog,
                                             baseClassesDialog)

with open("src/skeletons/universal_stats.json", "r") as stats_file:
    universal_stats =  json.load(stats_file)

GET_FILES = 1
GET_FOLDERS = 0

all_units = {}
team_units = {}
enemy_units = {}
classes = {}

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
        
        initUnit(self)
        
        initBasic(self)
        initAI(self)
        initWeaponAffinities(self)
        initActions(self)
        initClasses(self)
        initUnique(self)
        initRelationships(self)
        
        self.layout.addWidget(self.tscroll)
        
        self.show()
    
    def genderChange(self, s):
        self.unit.pronouns = s
        
        if self.path != None:
            self.unit.selfToJSON(self.path)
    
    def nameChange(self):
        s = self.sender().text()
        self.unit.name = s
        
        if self.path != None:
            self.unit.selfToJSON(self.path)
        
    def classificationChange(self):
        s = self.sender().currentText()
        self.unit.classification = s
        
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
            
            self.classification.setCurrentText(self.unit.classification)
            
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
    
    def editClassifications(self):
        e = editClassifications(parent=self,font=self.body_font)
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
        if os.sep == "/":
            self.loaded_class.selfToJSON("src/skeletons/classes/"+s+".tructf")
        else:
            self.loaded_class.selfToJSON("src\\skeletons\\classes\\"+s+".tructf")
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
    
    def stat_cap_change(self):
        p = statCapDialog(parent=self,font=self.body_font)
        p.exec_()
        if self.path != None:
            self.unit.selfToJSON(self.path)
    
    def baseClassPopup(self):
        p = baseClassesDialog(parent=self,font=self.body_font)
        p.exec_()
        if self.path != None:
            self.unit.selfToJSON(self.path)
