from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QPalette, QIcon, QPixmap, QCursor, QFont
from src.UI_updateJSON import updateJSON
import src.UI_colorTheme
import shutil, os, pickle, json, sys
from src.node_presets import NODE_KEYS, NODES, Nodes
from src.skeletons.unit_class import unitClass
from src.UI_nodes_backend import getFiles, GET_FILES
from src.skeletons.weapon_types import weaponType

class addNodePreset(QDialog):
    def __init__(self, parent=None,font=None):
        self.chosen_node = None
        self.parent = parent
        self.add = False
        data = updateJSON()
        self.active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        super().__init__(parent)
        self.body_font = font
        
        self.setWindowFlags(Qt.Popup)
        
        self.setStyleSheet("background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(8,8,8,8)
        l = QLabel("Add node: ")
        l.setFont(self.body_font)
        self.layout.addWidget(l)
        
        self.add_options = NODE_KEYS
        self.add_dd = QComboBox()
        self.add_dd.setFont(self.body_font)
        self.add_dd.setMaxVisibleItems(10)
        self.add_dd.textHighlighted.connect(self.add_enable)
        self.add_dd.currentTextChanged.connect(self.add_dd_changed)
        self.add_dd.setStyleSheet("QComboBox { combobox-popup: 0; };"+"background-color: "+self.active_theme.list_background_color+"; selection-background-color:"+self.active_theme.window_background_color)
        
        self.add_dd.addItem("--Select--")
        self.add_dd.addItems(self.add_options)
        self.layout.addWidget(self.add_dd)
        self.setLayout(self.layout)
        
        self.show()
    
    def add_enable(self,t):
        self.add = True
    
    def add_dd_changed(self, s):
        if self.add:
            self.chosen_node = NODES[s]
            g = Nodes(self.parent.grScene.NodeEditorWnd.scene, s).node
            self.parent.grScene.NodeEditorWnd.scene.added_nodes.append(g)
            i = self.parent.grScene.NodeEditorWnd.view.mapFromGlobal(self.position)
            h = self.parent.grScene.NodeEditorWnd.view.mapToScene(i.x(), i.y())
            g.setPos(h.x(), h.y())
            
        self.close()
        
    def showEvent(self, event):
        geom = self.frameGeometry()
        geom.moveCenter(QCursor.pos())
        self.setGeometry(geom)
        self.position = self.pos()
        self.move(self.position.x()+0,self.position.y()+48)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        super().showEvent(event)

class setSkillToClass(QDialog):
    def __init__(self, parent=None,font=None):
        data = updateJSON()
        self.parent = parent
        self.active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        super().__init__(parent)
        self.body_font = font
        
        self.setStyleSheet("background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(8,8,8,8)
        
        g = QLabel("Choose new class: ")
        g.setToolTip("Ignore and close this dialog if there's already a class assigned")
        g.setFont(self.body_font)
        self.layout.addWidget(g)
        self.list = QComboBox()
        self.list.setFont(self.body_font)
        self.list.addItem("--Select--")
        self.list.addItems(self.getClassesInFolder())
        self.list.currentTextChanged.connect(self.connect_class)
        self.layout.addWidget(self.list)
        
        self.setLayout(self.layout)
        
    def connect_class(self, s):
        file_list = getFiles("src/skeletons/classes")[GET_FILES]
        for f in file_list:
            if f.ext.strip() == ".tructf":
                f.path = f.path.replace("\\", "/") 
                tmp_class = unitClass()
                tmp_class.selfFromJSON(f.path)
                if tmp_class.unit_class_name == s:
                    if self.parent.skill_name not in tmp_class.skills:
                        tmp_class.skills.append(self.parent.skill_name.text())
                    tmp_class.selfToJSON(f.path)
                    self.close()                        
                    
    def getClassesInFolder(self):
        file_list = getFiles("src/skeletons/classes")[GET_FILES]
        class_names = []
        for f in file_list:
            tmp_class = unitClass()
            tmp_class.selfFromJSON(f.path)
            class_names.append(tmp_class.unit_class_name)
        print(class_names)
        return class_names

class setSkillToWeapon(QDialog):
    def __init__(self, parent=None,font=None,n=None):
        data = updateJSON()
        self.parent = parent
        self.active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        super().__init__(parent)
        self.body_font = font
        self.n = n
        
        self.setStyleSheet("background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(8,8,8,8)
        
        g = QLabel("Choose new weapon type: ")
        g.setToolTip("Ignore and close this dialog if there's already a weapon type assigned")
        g.setFont(self.body_font)
        self.layout.addWidget(g)
        self.list = QComboBox()
        self.list.setFont(self.body_font)
        self.list.addItem("--Select--")
        self.list.addItems(self.getWeaponsInFolder())
        self.list.currentTextChanged.connect(self.connect_weapon)
        self.layout.addWidget(self.list)
        
        self.setLayout(self.layout)
        
    def connect_weapon(self, s):
        file_list = getFiles("src/skeletons/weapon_types")[GET_FILES]
        for f in file_list:
            f.path = f.path.replace("\\", "/") 
            tmp_weapon = weaponType(f.path[f.path.rfind("/")+1:f.path.find(".json")])
            tmp_weapon.Load()
            if tmp_weapon.name == s:
                if self.parent.skill_name not in tmp_weapon.skills:
                    print("not in skills!")
                    tmp_weapon.addSkill(self.parent.skill_name.text(), self.n)
                tmp_weapon.Save()
                self.close()
                    
    def getWeaponsInFolder(self):
        file_list = getFiles("src/skeletons/weapon_types")[GET_FILES]
        weapons = []
        for f in file_list:
            tmp_weapon = weaponType(f.path[f.path.rfind(os.sep)+1:f.path.find(".json")])
            tmp_weapon.Load()
            weapons.append(tmp_weapon.name)
        print(weapons)
        return weapons