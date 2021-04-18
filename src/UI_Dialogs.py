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
        self.setFixedSize((data["font_size"] * 22)+40, data["font_size"] * 7.7)
        
        self.label =QLabel("Do you want to "+str(s)+"?")
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
        self.active_theme = getattr(UI_colorTheme, data["active_theme"])
        
        self.new_theme = UI_colorTheme.colorTheme()
        
        self.values = {}
        self.color_blocks = {}

        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.South)

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
        
        self.layout.addWidget(QLabel("To change, type in hex color and press Enter"))
        self.layout.addWidget(self.tabs)
        
        self.show()
        
    def updateValue(self):
        self.update_id = self.sender().color_block_id
        self.c_block = self.color_blocks[self.update_id]
        self.c_block_pixmap = QPixmap(70,30)
        
        self.update_value = self.sender().text()
        if self.update_value.startswith("#") == False:
            self.update_value = "#"+self.update_value
            self.sender().setText(self.update_value)
            
        setattr(self.new_theme, self.update_id, self.update_value)
        self.values[self.update_id] = self.update_value
        
        try:
            self.c_block_pixmap.fill(QColor(self.update_value))
        except:
            self.c_block_pixmap.fill(QColor("black"))
        
        self.c_block.setPixmap(self.c_block_pixmap)
