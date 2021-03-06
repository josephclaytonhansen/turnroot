from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QPalette, QIcon, QPixmap, QCursor, QFont
from src.UI_updateJSON import updateJSON
import src.UI_colorTheme
import shutil, os, pickle, json, sys
from src.game_directory import gameDirectory
from src.UI_unit_editor_more_dialogs import editUniversalWeaponTypes
from src.UI_game_editor_backend import DragListWidget
from src.UI_Dialogs import textEntryDialog
from src.UI_error_logging import errorLog

class weaponTriangle(QDialog):
    def __init__(self, parent=None):
        data = updateJSON()
        self.load_data = None
        self.active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        active_theme = self.active_theme
        super().__init__(parent)
        self.parent = parent
        self.setStyleSheet("background-color:"+active_theme.window_background_color+";color:"+active_theme.window_text_color+";")

        self.setFixedSize(1000,450)
        
        self.back = QLabel("",self)
        self.back.setPixmap(QPixmap("src/ui_images/triangle.png"))
        self.back.show()
        self.back.move(0,0)
        self.back.raise_()
        
        self.ok = QPushButton(QIcon(), "Save and Close", self)
        self.ok.setFont(parent.body_font)
        self.ok.setMinimumHeight(48)
        self.ok.setStyleSheet("background-color: "+active_theme.button_alt_color+";color:"+active_theme.button_alt_text_color+";")
        self.ok.clicked.connect(self.ok_clicked)
        
        self.wt = QPushButton(QIcon(), "Edit Weapon Types", self)
        self.wt.setFont(parent.body_font)
        self.wt.setMinimumHeight(48)
        self.wt.setMinimumWidth(280)
        self.wt.setStyleSheet("background-color: "+active_theme.list_background_color+";color:"+active_theme.window_text_color+";")
        self.wt.clicked.connect(self.wt_clicked)
        
        self.top_1 = QComboBox(self)
        self.top_1.name = "top_1"
        self.top_1.setFont(parent.body_font)
        self.top_1.setStyleSheet("background-color: "+active_theme.list_background_color+";color:"+active_theme.window_text_color+";")
        
        self.top_2 = QComboBox(self)
        self.top_2.name = "top_2"
        self.top_2.setFont(parent.body_font)
        self.top_2.setStyleSheet("background-color: "+active_theme.node_grid_background_color+";color:"+active_theme.window_text_color+";")
        
        self.right_1 = QComboBox(self)
        self.right_1.name = "right_1"
        self.right_1.setFont(parent.body_font)
        self.right_1.setStyleSheet("background-color: "+active_theme.list_background_color+";color:"+active_theme.window_text_color+";")
        
        self.right_2 = QComboBox(self)
        self.right_2.name = "right_2"
        self.right_2.setFont(parent.body_font)
        self.right_2.setStyleSheet("background-color: "+active_theme.node_grid_background_color+";color:"+active_theme.window_text_color+";")
        
        self.left_1 = QComboBox(self)
        self.left_1.name = "left_1"
        self.left_1.setFont(parent.body_font)
        self.left_1.setStyleSheet("background-color: "+active_theme.list_background_color+";color:"+active_theme.window_text_color+";")
        
        self.left_2 = QComboBox(self)
        self.left_2.name = "left_2"
        self.left_2.setFont(parent.body_font)
        self.left_2.setStyleSheet("background-color: "+active_theme.node_grid_background_color+";color:"+active_theme.window_text_color+";")
        
        self.outliers_list = QListWidget(self)
        self.outliers_list.name = "outliers_list"
        self.outliers_list.setFont(parent.body_font)
        self.outliers_list.setMaximumWidth(200)
        self.outliers_list.setStyleSheet("background-color: "+active_theme.list_background_color+";color:"+active_theme.window_text_color+";")
        
        self.lists = [self.top_1,self.top_2,self.right_1,self.right_2,self.left_1,self.left_2]
        for k in self.lists:
            k.currentTextChanged.connect(self.assign)
        
        self.outliers_label = QLabel(self)
        self.outliers_label.setText("Outliers (No Advantage)")
        self.outliers_label.setFont(parent.body_font)
        
        self.triangle_label = QLabel(self)
        self.triangle_label.setText("Weapon Advantages (Physical: Left, Magic: Right)")
        self.triangle_label.setToolTip("Physical weapons and magic have different triangles. Keep physical weapons in the left triangle and magic on the right.")
        self.triangle_label.setFont(parent.body_font)
        
        self.reset_button = QPushButton(QIcon(), "Reset", self)
        self.reset_button.setFont(parent.body_font)
        self.reset_button.setMinimumHeight(48)
        self.reset_button.setStyleSheet("background-color: "+active_theme.list_background_color+";color:"+active_theme.window_text_color+";")
        self.reset_button.clicked.connect(self.reset_clicked)
        
        self.use_magic_triangle = QCheckBox(self)
        self.use_magic_triangle.stateChanged.connect(self.toggle_mt)
        self.use_magic_triangle_label = QLabel(self)
        self.use_magic_triangle_label.setText("Use magic triangle?")
        self.use_magic_triangle_label.setToolTip("If checked, both triangles are editable. Otherwise, only the left triangle is editable. Use only non-magic weapons in this triangle")
        self.use_magic_triangle_label.setFont(parent.body_font)
        
        self.ok.show()
        self.ok.move(860, 380)
        self.ok.raise_()
        
        self.reset_button.show()
        self.reset_button.move(770, 380)
        self.reset_button.raise_()
        
        self.wt.show()
        self.wt.move(70, 380)
        self.wt.raise_()
        
        self.top_1.show()
        self.top_1.move(270, 50)
        self.top_1.raise_()
        
        self.top_2.show()
        self.top_2.move(360, 50)
        self.top_2.raise_()
        
        self.right_1.show()
        self.right_1.move(480, 300)
        self.right_1.raise_()
        
        self.right_2.show()
        self.right_2.move(570, 300)
        self.right_2.raise_()
        
        self.left_1.show()
        self.left_1.move(70, 300)
        self.left_1.raise_()
        
        self.left_2.show()
        self.left_2.move(160, 300)
        self.left_2.raise_()
        
        self.outliers_list.show()
        self.outliers_list.move(770, 50)
        self.outliers_list.raise_()
        
        self.outliers_label.show()
        self.outliers_label.move(770,20)
        self.outliers_label.raise_()
        
        self.triangle_label.show()
        self.triangle_label.move(220,20)
        self.triangle_label.raise_()
        
        self.use_magic_triangle_label.show()
        self.use_magic_triangle_label.move(34,20)
        self.use_magic_triangle_label.raise_()
        
        self.use_magic_triangle.show()
        self.use_magic_triangle.move(180,20)
        self.use_magic_triangle.raise_()
        
        self.loadWT()
        self.populateDD()
        self.Load()
        self.toggle_mt()
        self.show()
    
    def loadWT(self):
        with open("src/skeletons/universal_weapon_types.json", "r") as weapons_file:
            self.wt_list = []
            weapon_types = []
            weapon_types = json.load(weapons_file)
            self.wt_list = weapon_types.copy()
            self.outliers_list.addItems(weapon_types)
    
    def toggle_mt(self):
        assigns = [self.left_2,self.top_2,self.right_2]
        if self.use_magic_triangle.isChecked():
            for k in assigns:
                k.setVisible(True)
        else:
            for k in assigns:
                k.setVisible(False)
    
    def populateDD(self):
        with open("src/skeletons/universal_weapon_types.json", "r") as weapons_file:
            weapon_types = ["--Select--"]
            for x in json.load(weapons_file):
                if x not in weapon_types:
                    weapon_types.append(x)
            for k in self.lists:
                k.addItems(weapon_types)
                    
    def assign(self, s):
        if s != "--Select--":
            for l in self.lists:
                if l.name != self.sender().name:
                    try:
                        l.removeItem(l.findText(s))
                        self.wt_list.remove(s)
                        self.outliers_list.clear()
                        self.outliers_list.addItems(self.wt_list)
                        
                    except Exception as e:
                        errorLog(e)
    
    def ok_clicked(self):
        self.return_confirm = True
        self.Save()
        self.close()
        
    def wt_clicked(self):
        y = editUniversalWeaponTypes(self,self.parent.body_font)
        y.exec_()
        
    def reset_clicked(self):
        for l in self.lists:
            l.clear()
            self.outliers_list.clear()
        self.populateDD()
        self.loadWT()
    
    def Load(self):
        g = gameDirectory(self)
        g.getPath()
        try:
            with open(g.path+"/game_options/weapon_triangle.trsl", "r") as f:
                self.load_data = json.load(f)
            assigns = [self.left_1, self.left_2,
                     self.top_1, self.top_2,
                     self.right_1,self.right_2]
            for i in self.load_data:
                    assigns[self.load_data.index(i)].setCurrentText(i)
            if self.load_data[len(self.load_data)-1] == True:
                self.use_magic_triangle.setChecked(True)
            else:
                self.use_magic_triangle.setChecked(False)
        except Exception as e:
            errorLog(e)
    
    def Save(self):
        order = [self.left_1.currentText(), self.left_2.currentText(),
                 self.top_1.currentText(), self.top_2.currentText(),
                 self.right_1.currentText(),self.right_2.currentText(), self.use_magic_triangle.isChecked()]
        g = gameDirectory(self)
        g.getPath()
        with open(g.path+"/game_options/weapon_triangle.trsl", "w") as f:
            json.dump(order, f)
            
class creditsDialog(QDialog):
    def __init__(self,parent=None,font=None):
        data = updateJSON()
        self.active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        active_theme = self.active_theme
        super().__init__(parent)
        self.setStyleSheet("background-color:"+active_theme.window_background_color+";color:"+active_theme.window_text_color+";")
        
        layout = QVBoxLayout()
        layout.setContentsMargins( 8,8,8,8)
        layout.setSpacing(0)
        
        self.rows = {}
        self.roles = {}
        self.names = {}
        for x in range(0,13):
            self.rows[x] = QWidget()
            row_l = QHBoxLayout()
            self.rows[x].setLayout(row_l)
            title = QLineEdit()
            self.roles[x] = title
            title_label = QLabel("Role")
            name = QTextEdit()
            self.names[x] = name
            name_label = QLabel("Name(s)")
            for k in [title,name]:
                k.setFont(parent.body_font)
                k.setMaximumHeight(48)
                k.setStyleSheet("background-color:"+active_theme.list_background_color+";color:"+active_theme.window_text_color+";")
            row_l.addWidget(title_label)
            row_l.addWidget(title)
            row_l.addWidget(name_label)
            row_l.addWidget(name)
            layout.addWidget(self.rows[x])
        
        
        self.ok = QPushButton(QIcon(), "Save and Close", self)
        self.ok.setFont(parent.body_font)
        self.ok.setMinimumHeight(48)
        self.ok.setStyleSheet("background-color: "+active_theme.button_alt_color+";color:"+active_theme.button_alt_text_color+";")
        self.ok.clicked.connect(self.ok_clicked)
        layout.addWidget(self.ok)
        
        self.setLayout(layout)
        self.Load()
        self.show()
    
    def Load(self):
        g = gameDirectory(self)
        g.getPath()
        try:
            with open(g.path+"/game_options/end_credits.trsl", "r") as f:
                order = json.load(f)
                for k in self.roles:
                    self.roles[k].setText(order[0][k])
                for h in self.names:
                    self.names[h].setPlainText(order[1][h])
        except Exception as e:
            errorLog(e)
    
    def Save(self):
        order = [[],[]]
        for k in self.roles:
            order[0].append(self.roles[k].text())
        for h in self.names:
            order[1].append(self.names[h].toPlainText())
        g = gameDirectory(self)
        g.getPath()
        with open(g.path+"/game_options/end_credits.trsl", "w") as f:
            json.dump(order, f)
        
    def ok_clicked(self):
        self.return_confirm = True
        self.Save()
        self.close()

class uploadGameArtDialog(QDialog):
    def __init__(self,parent=None,font=None):
        data = updateJSON()
        self.active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        active_theme = self.active_theme
        super().__init__(parent)
        self.setStyleSheet("background-color:"+active_theme.window_background_color+";color:"+active_theme.window_text_color+";")
        
        layout = QVBoxLayout()
        layout.setContentsMargins( 8,8,8,8)
        layout.setSpacing(0)
                
        self.preview = QLabel()
        self.preview.setMinimumHeight(400)
        self.preview.setMaximumHeight(400)
        self.preview.setMinimumWidth(400)
        self.preview.setMaximumWidth(400)
        layout.addWidget(self.preview)
        
        self.ok = QPushButton(QIcon(), "Save and Close", self)
        self.ok.setFont(parent.body_font)
        self.ok.setMinimumHeight(48)
        self.ok.setStyleSheet("background-color: "+active_theme.button_alt_color+";color:"+active_theme.button_alt_text_color+";")
        self.ok.clicked.connect(self.ok_clicked)
        
        self.upload = QPushButton(QIcon(), "Upload Image", self)
        self.upload.setFont(parent.body_font)
        self.upload.setMinimumHeight(48)
        self.upload.setStyleSheet("background-color: "+active_theme.list_background_color+";color:"+active_theme.window_text_color+";")
        self.upload.clicked.connect(self.upload_image)
        layout.addWidget(self.upload)
        layout.addWidget(self.ok)
        
        self.setLayout(layout)
        self.Load()
        self.show()
        
    def Load(self):
        g = gameDirectory(self)
        g.getPath()
        try:
            with open(g.path+"/game_options/cover_art.trsl", "r") as f:
                self.image_path = json.load(f)
                self.preview.setPixmap(QPixmap(self.image_path))
        except Exception as e:
            errorLog(e)
    
    def upload_image(self):
        q = QFileDialog(self)
        options = q.Options()
        options |= q.DontUseNativeDialog
        fileName, _ = q.getOpenFileName(None,"Open","","Image (*.png)", options=options)
        if fileName:
            if fileName.endswith(".png"):
                self.image_path = fileName
            else:
                self.image_path = fileName+".png"
            self.preview.setPixmap(QPixmap(self.image_path))
        self.Save()
    
    def Save(self):
        g = gameDirectory(self)
        g.getPath()
        try:
            with open(g.path+"/game_options/cover_art.trsl", "w") as f:
                json.dump(self.image_path, f)
        except:
            pass
        
    def ok_clicked(self):
        self.return_confirm = True
        self.Save()
        self.close()
        
class magicExperienceDialog(QDialog):
    def __init__(self,parent=None,font=None):
        data = updateJSON()
        self.active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        active_theme = self.active_theme
        super().__init__(parent)
        self.setStyleSheet("background-color:"+active_theme.window_background_color+";color:"+active_theme.window_text_color+";")
        
        self.parent = parent
        self.body_font = self.parent.body_font
        
        layout = QVBoxLayout()
        layout.setContentsMargins(8,8,8,8)
        layout.setSpacing(0)
        
        self.setLayout(layout)
        self.show()
        
        self.middle = QWidget()
        self.top = QWidget()
        self.base = QWidget()
        self.middle_layout = QHBoxLayout()
        self.top_layout = QHBoxLayout()
        self.base_layout = QHBoxLayout()
        self.middle.setLayout(self.middle_layout)
        self.top.setLayout(self.top_layout)
        self.base.setLayout(self.base_layout)
        
        self.m_l = QLabel("Magic")
        self.m_l.setFont(self.body_font)
        self.e_m_n = QPushButton()
        self.e_m_n.clicked.connect(self.Rename)
        self.e_m_n.name = "Magic"
        self.e_m_n.setStyleSheet("background-color:"+active_theme.list_background_color+";color:"+active_theme.window_text_color+";")
        self.e_m_n.setFont(self.body_font)
        self.e_m_n.setIcon(QIcon(QPixmap("src/ui_icons/white/edit.png")))
        self.e_m_n.setIconSize(QSize(48,48))
        self.e_m_n.setMaximumWidth(48)
        self.e_m_n.setMinimumHeight(48)
        self.e_m_n.setMaximumHeight(48)
        
        self.dm_l = QLabel("Dark Magic")
        self.dm_l.setFont(self.body_font)
        self.e_dm_n = QPushButton()
        self.e_dm_n.clicked.connect(self.Rename)
        self.e_dm_n.name = "Dark Magic"
        self.e_dm_n.setFont(self.body_font)
        self.e_dm_n.setStyleSheet("background-color:"+active_theme.list_background_color+";color:"+active_theme.window_text_color+";")
        self.e_dm_n.setIcon(QIcon(QPixmap("src/ui_icons/white/edit.png")))
        self.e_dm_n.setIconSize(QSize(48,48))
        self.e_dm_n.setMaximumWidth(48)
        self.e_dm_n.setMinimumHeight(48)
        self.e_dm_n.setMaximumHeight(48)
        
        self.top_layout.addWidget(self.m_l)
        self.top_layout.addWidget(self.e_m_n)
        self.top_layout.addWidget(self.dm_l)
        self.top_layout.addWidget(self.e_dm_n)
        
        self.m_list = DragListWidget()
        self.m_list.setStyleSheet("background-color:"+active_theme.list_background_color+";color:"+active_theme.window_text_color+";")
        self.m_list.setFont(self.body_font)
        self.middle_layout.addWidget(self.m_list)
        
        self.dm_list = DragListWidget()
        self.dm_list.setStyleSheet("background-color:"+active_theme.list_background_color+";color:"+active_theme.window_text_color+";")
        self.dm_list.setFont(self.body_font)
        self.middle_layout.addWidget(self.dm_list)
        
        self.a_list = DragListWidget()
        self.a_list.setStyleSheet("background-color:"+active_theme.list_background_color+";color:"+active_theme.window_text_color+";")
        self.a_list.setFont(self.body_font)
        self.middle_layout.addWidget(self.a_list)
        
        self.a_l = QLabel("All Weapon Types (Drag and Drop Magic Types)")
        self.a_l.setFont(self.body_font)
        
        self.ok = QPushButton("Save and Close")
        self.ok.clicked.connect(self.Save)
        self.ok.setFont(self.body_font)
        self.ok.setStyleSheet("background-color:"+active_theme.list_background_color+";color:"+active_theme.window_text_color+";")
        self.ok.setMinimumHeight(48)
        self.ok.setMaximumHeight(48)
        
        self.reset = QPushButton("Reset")
        self.reset.clicked.connect(self.Reset)
        self.reset.setFont(self.body_font)
        self.reset.setStyleSheet("background-color:"+active_theme.list_background_color+";color:"+active_theme.window_text_color+";")
        self.reset.setMinimumHeight(48)
        self.reset.setMaximumHeight(48)
        
        self.base_layout.addWidget(self.reset)
        self.base_layout.addWidget(self.ok)
        
        layout.addWidget(self.top)
        layout.addWidget(self.middle)
        layout.addWidget(self.a_l)
        layout.addWidget(self.a_list)
        layout.addWidget(self.base)
        
        self.loadWT()
        self.Load()
        if self.getFromList(self.a_list) == []:
            self.loadWT()
        
    def loadWT(self):
        with open("src/skeletons/universal_weapon_types.json", "r") as weapons_file:
            self.wt_list = []
            weapon_types = []
            weapon_types = json.load(weapons_file)
            self.wt_list = weapon_types.copy()
            self.a_list.clear()
            self.a_list.addItems(weapon_types)
    
    def Reset(self):
        self.m_list.clear()
        self.dm_list.clear()
        self.a_list.clear()
        self.loadWT()
    
    def Rename(self):
        g = gameDirectory(self)
        g.getPath()
        h = textEntryDialog(self)
        h.exec_()
        result = h.data
        data = [self.m_l.text(), self.dm_l.text()]
        if self.sender().name == self.m_l.text():
            data = [result, self.dm_l.text()]
        elif self.sender().name == self.dm_l.text():
            data = [self.m_l.text(), result]
        print(data)
        try:
            with open(g.path+"/game_options/magic_triangle_labels.trsl", "w") as f:
                    json.dump(data,f)
        except:
            data = ["Magic", "Dark Magic"]
            with open(g.path+"/game_options/magic_triangle_labels.trsl", "w") as f:
                    json.dump(data,f)
                    
        self.Load()
    
    def Save(self):
        g = gameDirectory(self)
        g.getPath()
        try:
            data = [self.getFromList(self.m_list),self.getFromList(self.dm_list),self.getFromList(self.a_list)]
            with open(g.path+"/game_options/magic_triangle.trsl", "w") as f:
                json.dump(data, f)
            self.close()
        except Exception as e:
            errorLog(e)
    
    def Load(self):
        g = gameDirectory(self)
        g.getPath()
        try:
            with open(g.path+"/game_options/magic_triangle.trsl", "r") as f:
                self.load_data = json.load(f)
            lists = [self.m_list, self.dm_list, self.a_list]
            count = -1
            for i in self.load_data:
                count +=1
                lists[count].clear()
                lists[count].addItems(i)  
        except:
            self.loadWT()
        try:
            with open(g.path+"/game_options/magic_triangle_labels.trsl", "r") as f:
                self.load_data = json.load(f)
            self.e_m_n.name = self.load_data[0]
            self.m_l.setText(self.load_data[0])
            self.e_dm_n.name = self.load_data[1]
            self.dm_l.setText(self.load_data[1])
        except Exception as e:
            errorLog(e)
    
    def getFromList(self, l):
        try:
            count = l.count()
            items = []
            for x in range(0,count):
                items.append(l.item(x).text())
            return items
        except Exception as e:
            errorLog(e)
            return []
        
        