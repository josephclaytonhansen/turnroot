from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QPalette, QIcon, QPixmap, QCursor, QFont
from src.UI_updateJSON import updateJSON
import src.UI_colorTheme
import shutil, os, pickle, json, sys

return_confirm = False
chosen_object = None
resource_pack_path = "src/resource_packs"
current_resource_pack_path = ""
with open("src/tmp/rsp.tmp", "r") as read_file:
    current_pack = read_file.read().strip()
pack_infos = {}
installer = None

class confirmAction(QDialog):
    def __init__(self, s, parent=None):
        data = updateJSON()
        self.s = s

        self.return_confirm = return_confirm
        self.active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        super().__init__(parent)
        self.setStyleSheet("font-size: "+str(data["font_size"]+3)+"px; background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        
        layout = QVBoxLayout()
        layout.setContentsMargins( 8,8,8,8)
        layout.setSpacing(0)
        self.setMinimumSize((data["font_size"] * 22)+40, data["font_size"] * 7.7)
        
        if self.s.startswith("#") == False:
            self.label =QLabel("Do you want to "+str(s)+"?")
        else:
            self.label = QLabel(str(s[1:]))
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        layout.addWidget(self.label, 1)
        self.yes = QPushButton(QIcon(), "Yes", self)
        self.yes.setMinimumHeight(data["font_size"] * 2)
        self.no = QPushButton(QIcon(), "No", self)
        self.no.setMinimumHeight(data["font_size"] * 2)
        
        boxes = QWidget()
        boxes_layout = QHBoxLayout()
        boxes_layout.addWidget(self.yes, 50)
        boxes_layout.addWidget(self.no, 50)
        boxes.setLayout(boxes_layout)
        layout.addWidget(boxes, 2)
        
        self.yes.clicked.connect(self.yes_clicked)
        self.no.clicked.connect(self.no_clicked)
        self.setLayout(layout)
        self.show()

    def yes_clicked(self):
        self.return_confirm = True
        self.close()
    def no_clicked(self):
        self.return_confirm = False
        self.close()

class stackedInfoImgDialog(QDialog):
    def __init__(self, img, info, row_styles, parent=None):
        data = updateJSON()
        self.img = img
        self.info = info
        self.rows = len(info)
        self.row_styles = row_styles
        self.active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        super().__init__(parent)
        self.setStyleSheet("font-size: "+str(data["font_size"]+3)+"px; background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(8,8,8,8)
        self.layout.setSpacing(4)
        
        self.img_label = QLabel()
        self.img_label.setPixmap(QPixmap(img))
        self.img_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        
        self.layout.addWidget(self.img_label)
        self.setLayout(self.layout)
        self.layout.setSizeConstraint( QLayout.SetFixedSize)
        self.show()
        self.labels = {}
        
        for x in range(0, self.rows):
            self.labels[x] = QLabel(self.info[x])
            self.labels[x].setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.labels[x].setStyleSheet(self.row_styles[x]+"background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
            self.layout.addWidget(self.labels[x])

class infoClose(QDialog):
    def __init__(self, info, parent=None):
        data = updateJSON()
        self.return_confirm = return_confirm
        self.info = info
        self.active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        super().__init__(parent)
        self.setStyleSheet("font-size: "+str(data["font_size"]+3)+"px; background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        
        layout = QVBoxLayout()
        layout.setContentsMargins( 8,8,8,8)
        layout.setSpacing(0)
        self.setFixedSize((data["font_size"] * len(info)/1.6), data["font_size"] * 7.4)
        
        self.label =QLabel(self.info)
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        layout.addWidget(self.label, 1)
        self.ok = QPushButton(QIcon(), "Ok", self)    
        self.ok.clicked.connect(self.ok_clicked)
        layout.addWidget(self.ok, 2)
        self.setLayout(layout)
        self.show()
        
    def ok_clicked(self):
        self.return_confirm = True
        self.close()
     
class addObject(QDialog):
    def __init__(self, parent=None):
        global chosen_object
        self.chosen_object = chosen_object
        data = updateJSON()
        self.active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        super().__init__(parent)
        
        self.setWindowFlags(Qt.Popup)
        
        self.setStyleSheet("font-size: "+str(data["font_size"]+3)+"px; background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(8,8,8,8)
        self.layout.addWidget(QLabel("Add object: "))
        
        self.add_options = ["Enemy Unit", "Ally Unit", "Door", "Barred Gate", "Breakable Wall", "Chest", "Emplacement", "Switch", "Trap", "Heal", "Warp", "Fortress"]
        self.add_dd = QComboBox()
        self.add_dd.currentTextChanged.connect(self.add_dd_changed)
        self.add_dd.setStyleSheet("background-color: "+self.active_theme.list_background_color+"; selection-background-color:"+self.active_theme.window_background_color)

        self.add_dd.addItems(self.add_options)
        self.layout.addWidget(self.add_dd)
        self.setLayout(self.layout)
        
        self.show()
    
    def add_dd_changed(self, s):
        global chosen_object
        chosen_object = s
        self.chosen_object = chosen_object
        
    def showEvent(self, event):
        geom = self.frameGeometry()
        geom.moveCenter(QCursor.pos())
        self.setGeometry(geom)
        self.position = self.pos()
        self.move(self.position.x()+0,self.position.y()+48)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        super().showEvent(event)
        
class resourcePackDialog(QDialog): 
    def openFileDialog(self):
        global installer
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Open", "","Turnroot Resource Pack Install File (*.trpi)", options=options)
        if fileName:
            installer = fileName
            
    def __init__(self, parent=None):
        data = updateJSON()
        self.return_confirm = return_confirm
        self.active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        super().__init__(parent)
        self.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        
        global resource_pack_path, current_resource_pack_path, pack_infos
        
        with open(resource_pack_path+"/packs.txt", "r") as read_file:
            r = read_file.read().split("\n")
            read_file.close()
        
        self.folder_select = QLineEdit()
        
        self.reset_path_to_default = QPushButton("Reset path to default")
        self.reset_path_to_default.clicked.connect(self.reset)
        self.reset_path_to_default.clicked.connect(self.folder_select.clear)
        
        self.folder_select_label = QLabel("Pack folder path")
        self.folder_select.setPlaceholderText("src/"+resource_pack_path)
        self.folder_select.returnPressed.connect(self.return_pressed)
        
        self.folder_select_submit = QPushButton("Set path")
        self.folder_select_submit.clicked.connect(self.return_pressed)
        
        self.current_pack_label = QLabel("Current pack")
        self.switch_pack = QComboBox()
        self.switch_pack.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: "+self.active_theme.list_background_color+";color: "+self.active_theme.window_text_color)
        self.switch_pack.addItems(r)
        self.switch_pack.currentTextChanged.connect(self.text_changed)
        
        self.install_pack = QPushButton("Install new pack")
        self.install_pack.clicked.connect(self.installPack)
        self.pack_info = QWidget()

        self.font = QFont('Monaco', 6, QFont.Light)
        self.font.setKerning(False)
        self.font.setFixedPitch(True)
        
        self.pack_info.setFont(self.font)
        self.pack_img_info = QLabel()

        with open(resource_pack_path+"/"+r[0]+"/info.txt", "r") as read_file:
                pack_infos[r[0]] = read_file.read()
                read_file.close()
                
        self.pack_text_info = QLabel(pack_infos[r[0]])
        self.pack_img_info.setPixmap(QPixmap(resource_pack_path+"/"+r[0]+"/pack_img.png"))
        self.pack_img_info.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        
        self.pack_info_layout = QVBoxLayout()
        self.pack_info_layout.addWidget(self.pack_img_info)
        self.pack_info_layout.addWidget(self.pack_text_info)
        self.pack_info.setLayout(self.pack_info_layout)
        
        self.layout.addWidget(self.folder_select_label,0,0,1,1)
        self.layout.addWidget(self.reset_path_to_default,0,4,1,1)
        self.layout.addWidget(self.folder_select,0,1,1,2)
        self.layout.addWidget(self.folder_select_submit,0,3,1,1)
        self.layout.addWidget(self.current_pack_label,1,0,1,1)
        self.layout.addWidget(self.switch_pack,1,2,1,1)
        self.layout.addWidget(self.install_pack,2,0,1,3)
        self.layout.addWidget(self.pack_info,1,1,1,1)
        
        self.show()
    
    def text_changed(self, s):
        global current_pack, pack_infos
        current_pack = s
        with open(resource_pack_path+"/"+s+"/info.txt", "r") as read_file:
                self.info = read_file.read()
                read_file.close()
        self.c = infoClose("You'll need to restart the level editor for this change to take effect")
        self.c.exec_()
        if self.c.return_confirm:
            with open("src/tmp/rsp.tmp", "w") as write_file:
                write_file.write(current_pack)
            self.pack_text_info.setText(self.info)
            self.pack_img_info.setPixmap(QPixmap(resource_pack_path+"/"+s+"/pack_img.png"))
    
    def return_pressed(self):
        global resource_pack_path
        self.temp_path = resource_pack_path
        resource_pack_path = self.folder_select.text()
        try:
            open(resource_pack_path+"/packs.txt", "r")
        except:
            infoClose("Invalid folder path or missing packs.txt file",self)
            resource_pack_path = self.temp_path
            self.folder_select.clear()         
    
    def reset(self):
        global resource_pack_path, current_resource_pack_path
        resource_pack_path = "resource_packs"
    
    def installPack(self):
        self.openFileDialog()
        global installer, resource_pack_path
        if installer != None:
            with open(installer, "rb") as read_file:
                self.install_directions = pickle.load()
                self.orig_path = installer[:installer.find("INSTALLER.trpi")]
                print(self.orig_path)
                if "#$c*" in self.install_directions:
                    self.pack_name = self.install_directions[self.install_directions.find("*$cNAME")+7:self.install_directions.find("*$cVERSION")]
                    #check
                    with open(resource_pack_path+"/packs.txt", "r") as read_file:
                        r = read_file.read().split("\n")
                        read_file.close()
                    if self.pack_name not in r:
                        if "#$i*" in self.install_directions:
                            self.install_path = resource_pack_path
                            self.install_directions = self.install_directions[self.install_directions.find("#$i*")+4:]
                            self.install_directions = self.install_directions.split("*$i")
                            if self.install_directions[0] == "$i'tiles'":
                                self.install_path_t = self.install_path+ "/"+self.pack_name+"/tiles"
                                self.install_path = self.install_path+ "/"+self.pack_name+"/"
                                os.makedirs(self.install_path_t)
                                #shutil.move(self.orig_path+"/tiles/", self.install_path+"/tiles/")
                            shutil.move(self.orig_path+"info.txt", self.install_path+"info.txt")
                            shutil.move(self.orig_path+"pack_img.png", self.install_path+"pack_img.png")
                        with open(resource_pack_path+"/packs.txt", "a") as write_file:
                            write_file.write("\n"+self.pack_name)
                            write_file.close()

class activeResourcePack():
    def __init__(self):
        global resource_pack_path, current_pack
        self.path = resource_pack_path
        self.pack = current_pack
        
class ColorBlock(QLabel):
    def __init__(self, color, w, h, parent=None):
        super().__init__(parent)
        self.color = color
        self.pixmap = QPixmap(w,h)
        self.pixmap.fill(QColor(self.color))
        self.setPixmap(self.pixmap)
        
class colorThemeEdit(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        data = updateJSON()

        self.active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        
        self.new_theme = src.UI_colorTheme.colorTheme()
        
        self.values = {}
        self.color_blocks = {}
        
        self.setMaximumHeight(750)

        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)
        
        self.tscroll = QScrollArea()
        self.tscroll.setMaximumHeight(900)
        self.tscroll.setWidget(self.tabs)
        self.tscroll.setWidgetResizable(True)
        self.tscroll.setHorizontalScrollBarPolicy( Qt.ScrollBarAlwaysOff )
        self.tscroll.setVerticalScrollBarPolicy( Qt.ScrollBarAlwaysOn )

        self.theme_groups = self.active_theme.groups
        for tab in (self.theme_groups):
            self.tab_title = tab[0]
            self.c_tab = QWidget()
            self.c_tab_layout = QVBoxLayout()
            self.c_tab.setLayout(self.c_tab_layout)

            self.c_colors = getattr(self.active_theme, self.tab_title)
            self.c_colors_labels = getattr(self.active_theme, self.tab_title+"_labels")

            for l in range(1, len(self.c_colors)):
                self.color_block = QWidget()
                self.color_block_layout = QHBoxLayout()
                self.color_block.setLayout(self.color_block_layout)

                self.color_label = QLabel(self.c_colors_labels[l])
                self.color_block_color = ColorBlock(self.c_colors[l],70,20)
                self.color_blocks[self.c_colors_labels[l]] = self.color_block_color
                self.color_value = QLineEdit()
                self.color_value.color_block_id = self.c_colors_labels[l]
                self.color_value.returnPressed.connect(self.updateValue)
                self.color_value.setPlaceholderText(self.c_colors[l])
                
                self.color_block_layout.addWidget(self.color_label, 0)
                self.color_block_layout.addWidget(self.color_block_color, 1)
                self.color_block_layout.addWidget(self.color_value, 2)
                
                self.values[self.c_colors_labels[l]] = self.c_colors[l]
                
                self.c_tab_layout.addWidget(self.color_block)
                
            self.tabs.addTab(self.c_tab, self.tab_title)
            
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        self.in_ok = QWidget()
        self.in_ok.setMaximumHeight(70)
        self.in_ok_layout = QHBoxLayout()
        self.in_ok_layout.addWidget(QLabel("To change, type in hex color and press Enter\n(changes save automatically)"))
        self.in_ok.setLayout(self.in_ok_layout)
        
        self.layout.addWidget(self.in_ok)
        self.layout.addWidget(self.tscroll)
        
        self.show()
    
    def updateValue(self):
        self.update_id = self.sender().color_block_id
        self.c_block = self.color_blocks[self.update_id]
        self.c_block_pixmap = QPixmap(70,20)
        
        self.update_value = self.sender().text()
        if self.update_value.startswith("#") == False:
            self.update_value = "#"+self.update_value
            if self.update_value.endswith("#"):
                self.update_value = "#000000"
            self.sender().setText(self.update_value)
            
        setattr(self.new_theme, self.update_id, self.update_value)
        self.values[self.update_id] = self.update_value
        
        with open("src/UI_ColorTheme.py", "r") as readfile:
            color_theme_file = readfile.read()
            color_theme_file = color_theme_file.split("\n")
            color_theme_file_hold = color_theme_file
            readfile.close()

            color_theme_start = None
            counter = 0
            while color_theme_start == None:
                counter += 1
                line = color_theme_file[counter]
                if "tag" in line and self.active_theme.tag in line:
                    color_theme_start = color_theme_file.index(line)
                    
            if color_theme_start is not None:
                color_theme_file = color_theme_file[color_theme_start:color_theme_start+51]
                
                counter = -1
                edit_line = None
                while edit_line == None:
                    counter +=1
                    if self.update_id in color_theme_file[counter]:
                        edit_line = counter + color_theme_start
            
            with open("src/tmp/uctp.tmp", "w") as tmp_color_file:
                theme_edit_line = color_theme_file_hold[edit_line]
                theme_edit_line_start = theme_edit_line.find("#")
                theme_edit_line_portion = theme_edit_line[theme_edit_line_start:len(theme_edit_line)-1]
                new_line = theme_edit_line[:theme_edit_line_start] + self.update_value + "\""
                color_theme_file_hold[edit_line] = new_line
                
                for x in color_theme_file_hold:
                    tmp_color_file.write(x)
                    tmp_color_file.write("\n")
                
            shutil.copyfile("src/tmp/uctp.tmp", "src/UI_ColorTheme.py")
        
        try:
            self.c_block_pixmap.fill(QColor(self.update_value))
        except:
            self.c_block_pixmap.fill(QColor("black"))
        
        self.c_block.setPixmap(self.c_block_pixmap)

NEW_WINDOW = 0
REPLACE_WINDOW = 1

class editorDialogItem(QWidget):
    def __init__(self,icon,text,editor,parent=None):
        data = updateJSON()
        super().__init__(parent)
        self.icon = icon
        self.text = text
        self.editor = editor
        self.parent = parent
        
        self.layout = QVBoxLayout()
        self.layout.setSpacing(2)
        self.setLayout(self.layout)
        self.icon_widget = QLabel()
        self.icon_widget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.icon_widget.setPixmap(QPixmap(self.icon))
        self.label_widget = QPushButton(self.text)
        self.label_widget.clicked.connect(self.changeEditor)
        
        self.layout.addWidget(self.icon_widget)
        self.layout.addWidget(self.label_widget)
    
    def changeEditor(self):
        self.parent.editor = self.editor
        self.parent.close()

TILE_EDITOR = 0
NODE_EDITOR = 1
WORLD_EDITOR = 2
HUB_EDITOR = 3
UNIT_EDITOR = 4
OBJECT_EDITOR = 5
PORTRAIT_EDITOR = 6
CLASS_EDITOR = 7
MENU_EDITOR = 8
STORE_EDITOR = 9
GAME_EDITOR = 10

EDITORS = [TILE_EDITOR,NODE_EDITOR,WORLD_EDITOR,HUB_EDITOR,UNIT_EDITOR,OBJECT_EDITOR,PORTRAIT_EDITOR,CLASS_EDITOR,MENU_EDITOR,STORE_EDITOR,GAME_EDITOR]

class switchEditorDialog(QDialog):
    def __init__(self,parent=None):
        data = updateJSON()
        self.active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        super().__init__(parent)
        self.setWindowFlags(Qt.Popup)
        self.mode = NEW_WINDOW
        self.setStyleSheet("font-size: "+str(data["font_size"]+3)+"px; background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        
        self.editor = None
        
        self.layout = QVBoxLayout()

        self.radioGroup = QWidget()
        self.radioGroup_layout = QHBoxLayout()
        self.radioGroup.setLayout(self.radioGroup_layout)
        
        self.radio_new = QRadioButton("Open new window")
        self.radio_new.setChecked(True)
        self.radio_new.toggled.connect(self.newWindow)
        
        self.radio_replace = QRadioButton("Replace current window")
        self.radio_new.setChecked(False)
        self.radio_new.toggled.connect(self.replaceWindow)
        
        self.radioGroup_layout.addWidget(self.radio_new)
        self.radioGroup_layout.addWidget(self.radio_replace)
        
        self.row_1 = QWidget()
        self.row_2 = QWidget()
        self.row_3 = QWidget()
        
        self.row_1_layout = QHBoxLayout()
        self.row_2_layout = QHBoxLayout()
        self.row_3_layout = QHBoxLayout()
        
        self.row_1.setLayout(self.row_1_layout)
        self.row_2.setLayout(self.row_2_layout)
        self.row_3.setLayout(self.row_3_layout)
        
        self.layout.addWidget(self.row_1)
        self.layout.addWidget(self.row_2)
        self.layout.addWidget(self.row_3)
        
        self.icons = [["src/ui_icons/white/e_tile.png", "src/ui_icons/white/e_node.png", "src/ui_icons/white/e_world.png","src/ui_icons/white/e_hub.png"],
                      ["src/ui_icons/white/e_unit.png","src/ui_icons/white/e_object.png","src/ui_icons/white/e_portrait.png", "src/ui_icons/white/e_class.png"],
                      ["src/ui_icons/white/e_menu.png", "src/ui_icons/white/e_store.png", "src/ui_icons/white/e_game.png"]]
        self.labels = [["Tiles (level)", "Nodes (dialogue/actions)", "Tiles (world)", "Hub"],
                       ["Units", "Objects", "Portraits", "Classes"],
                       ["Menus", "Stores", "Game"]]
        self.widgets = [[0,1,2,3],[0,1,2,3],[0,1,2]]
        self.rows = [self.row_1_layout, self.row_2_layout, self.row_3_layout]
        
        e = -1
        current_row = -1
        for row in self.widgets:
            current_row  += 1
            for item in row:
                e += 1
                current_icon = self.icons[current_row][item]
                current_label = self.labels[current_row][item]
                w = editorDialogItem(current_icon, current_label, EDITORS[e], parent=self)
                self.rows[current_row].addWidget(w)

        #self.layout.addWidget(self.radioGroup)
        
        self.setLayout(self.layout)
        
        self.show()
    
    def newWindow(self):
        self.mode = NEW_WINDOW
    
    def replaceWindow(self):
        self.mode = REPLACE_WINDOW

class popupInfo(QDialog):
    def __init__(self,s,parent=None):
        data = updateJSON()
        self.active_theme = getattr(src.UI_colorTheme, data["active_theme"])
        super().__init__(parent)
        self.setWindowFlags(Qt.Popup)
        self.setStyleSheet("font-size: "+str(data["font_size"]+3)+"px; background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        
        self.info = s
        
        layout = QVBoxLayout()
        layout.setContentsMargins( 8,8,8,8)
        layout.setSpacing(0)
        
        self.label =QLabel(self.info)
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        layout.addWidget(self.label, 1)
        self.setLayout(layout)
        self.show()

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
