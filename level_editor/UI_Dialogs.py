import sys
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QPalette, QIcon, QPixmap, QCursor, QFont
import json
from UI_updateJSON import updateJSON
import UI_colorTheme
return_confirm = False
chosen_object = None
resource_pack_path = "resource_packs"
current_resource_pack_path = ""

class confirmAction(QDialog):
    def __init__(self, s, parent=None):
        data = updateJSON()
        self.s = s
        self.return_confirm = return_confirm
        self.active_theme = getattr(UI_colorTheme, data["active_theme"])
        super().__init__(parent)
        self.setStyleSheet("font-size: "+str(data["font_size"]+3)+"px; background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        
        layout = QVBoxLayout()
        layout.setContentsMargins( 8,8,8,8)
        layout.setSpacing(0)
        self.setFixedSize((data["font_size"] * 22)+40, data["font_size"] * 7.4)
        
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
        self.active_theme = getattr(UI_colorTheme, data["active_theme"])
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
        self.active_theme = getattr(UI_colorTheme, data["active_theme"])
        super().__init__(parent)
        self.setStyleSheet("font-size: "+str(data["font_size"]+3)+"px; background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        
        layout = QVBoxLayout()
        layout.setContentsMargins( 8,8,8,8)
        layout.setSpacing(0)
        self.setFixedSize((data["font_size"] * len(info))-60, data["font_size"] * 7.4)
        
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
        self.active_theme = getattr(UI_colorTheme, data["active_theme"])
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
    def __init__(self, parent=None):
        data = updateJSON()
        self.return_confirm = return_confirm
        self.active_theme = getattr(UI_colorTheme, data["active_theme"])
        super().__init__(parent)
        self.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        
        global resource_pack_path, current_resource_pack_path
        self.pack_infos = {}
        
        with open(resource_pack_path+"/packs.txt", "r") as read_file:
            r = read_file.read().split("\n")
            read_file.close()
        
        for x in r:
            with open(resource_pack_path+"/"+x+"/info.txt", "r") as read_file:
                self.pack_infos[x] = read_file.read()
                read_file.close()
        
        self.folder_select = QLineEdit()
        
        self.reset_path_to_default = QPushButton("Reset path to default")
        self.reset_path_to_default.clicked.connect(self.reset)
        self.reset_path_to_default.clicked.connect(self.folder_select.clear)
        
        self.folder_select_label = QLabel("Pack folder path")
        self.folder_select.setPlaceholderText("/"+resource_pack_path)
        self.folder_select.returnPressed.connect(self.return_pressed)
        
        self.folder_select_submit = QPushButton("Set path")
        self.folder_select_submit.clicked.connect(self.return_pressed)
        
        self.current_pack_label = QLabel("Current pack")
        self.switch_pack = QComboBox()
        self.switch_pack.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: "+self.active_theme.list_background_color+";color: "+self.active_theme.window_text_color)
        self.switch_pack.addItems(r)
        self.switch_pack.currentTextChanged.connect(self.text_changed)
        
        self.install_pack = QPushButton("Install new pack")
        self.pack_info = QWidget()

        self.font = QFont('Monaco', 6, QFont.Light)
        self.font.setKerning(False)
        self.font.setFixedPitch(True)
        
        self.pack_info.setFont(self.font)
        
        for x in r:
            self.pack_text_info = QLabel(self.pack_infos[x])
            self.pack_img_info = QLabel()
            self.pack_img_info.setPixmap(QPixmap(resource_pack_path+"/"+x+"/pack_img.png"))
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
        self.layout.addWidget(self.install_pack,2,0,1,1)
        self.layout.addWidget(self.pack_info,1,1,1,1)
        
        self.show()
    
    def text_changed(self):
        pass
    
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

    
