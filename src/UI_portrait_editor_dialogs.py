import sys, json, os
import src.UI_colorTheme as UI_colorTheme
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from src.UI_updateJSON import updateJSON
from src.game_directory import gameDirectory
from src.UI_Dialogs import confirmAction, infoClose, switchEditorDialog, REPLACE_WINDOW, NEW_WINDOW
import qtmodern.styles
import qtmodern.windows

data = updateJSON()
active_theme = getattr(UI_colorTheme, data["active_theme"])

class portraitStackWidget(QWidget):
    def __init__(self, parent=None,font=None,stack=None):
        super().__init__(parent)
        self.body_font = font
        self.parent = parent
        self.stack = stack
        self.initUI()
        
    def initUI(self):
        self.path = None
        self.active_color = "#000000"
        
        self.setStyleSheet("background-color: "+active_theme.window_background_color+"; color:"+active_theme.window_text_color+"; font-size: 16")

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(2)
        self.setLayout(self.layout)
        
        self.counts = {"base":0,"hair":0, "scars":0, "freckles":0, "jewelry":0, "masks":0,"eyes":0,
                       "tattoos":0, "facial hair":0, "makeup":0, "tops":0, "headwear":0, "armor":0,
                       "nose":0,"mouth":0,"eyebrows":0}
        self.max_counts = {"base":1,"hair":3, "scars":6, "freckles":4, "jewelry":6, "masks":2, "tattoos":5, "eyes":1,
                           "facial hair":3,"makeup":3, "tops":3, "headwear":4, "armor":3,"nose":1,"mouth":1,"eyebrows":1}
        self.parent.total_layers = 0
        
        with open("src/tmp/pech.trch", "r") as f:
            self.color_history = json.load(f)
        
        with open("src/tmp/pecp.trch", "r") as f:
            self.saved_palette = json.load(f)
        
        color_edit = QWidget()
        color_edit_layout = QGridLayout()
        color_edit.setLayout(color_edit_layout)
        
        img_edit = QWidget()
        img_edit_layout = QVBoxLayout()
        img_edit.setLayout(img_edit_layout)
        
        self.layout.addWidget(color_edit)
        self.layout.addWidget(img_edit)
        
        self.img_choices_list = QListWidget()
        self.img_choices_list.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+";")
        img_edit_layout.addWidget(self.img_choices_list)
        
        self.expand_choices = QPushButton()
        self.expand_choices.setIcon(QIcon(QPixmap("src/ui_icons/white/expand.png")))
        self.expand_choices.setMinimumWidth(42)
        self.expand_choices.setMinimumHeight(42)
        self.expand_choices.setMaximumHeight(42)
        self.expand_choices.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+";")
        self.expand_choices.setIconSize(QSize(40,40))
        img_edit_layout.addWidget(self.expand_choices)
        
        self.color_preview = QWidget()
        self.color_preview.setStyleSheet("background-color: #000000")
        self.color_preview.setMinimumHeight(60)
        color_edit_layout.addWidget(self.color_preview,0,0,1,2)
        
        self.color_hex = QLineEdit()
        self.color_hex.returnPressed.connect(self.color_update)
        self.color_hex.setFont(self.body_font)
        self.color_hex.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+";")
        self.color_hex.setPlaceholderText("#000000")
        color_edit_layout.addWidget(self.color_hex,1,0,1,1)
        
        save_fav_color = QPushButton()
        save_fav_color.setIcon(QIcon(QPixmap("src/ui_icons/white/star.png")))
        save_fav_color.setMaximumWidth(24)
        save_fav_color.setMinimumWidth(24)
        save_fav_color.setMinimumHeight(24)
        save_fav_color.setMaximumHeight(24)
        save_fav_color.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+";")
        save_fav_color.setIconSize(QSize(22,22))
        save_fav_color.clicked.connect(self.save_color)
        color_edit_layout.addWidget(save_fav_color,1,1,1,1)
        
        color_history_row = QWidget()
        color_history_row.setMaximumHeight(60)
        color_history_row_layout = QHBoxLayout()
        color_history_row_layout.setSpacing(2)
        color_history_row.setLayout(color_history_row_layout)
        
        self.color_history_buttons = {}
        
        history_label = QLabel("History")
        history_label.setFont(self.body_font)
        color_history_row_layout.addWidget(history_label)
        
        for x in range(0,6):
            color_ = QPushButton()
            self.color_history_buttons[x] = color_
            color_.setMaximumHeight(20)
            color_.setMaximumWidth(20)
            color_.setMinimumWidth(20)
            color_.setMaximumWidth(20)
            try:
                color_.setStyleSheet("background-color:"+self.color_history[x])
                color_.value = self.saved_palette[x]
            except:
                color_.setStyleSheet("background-color: #000000")
                color_.value = "#000000"
            color_history_row_layout.addWidget(color_)
            color_.clicked.connect(self.color_from_palette)
            
        color_edit_layout.addWidget(color_history_row,2,0,1,2)
        
        palette_row = QWidget()
        palette_row.setMaximumHeight(60)
        palette_row_layout = QHBoxLayout()
        palette_row_layout.setSpacing(2)
        palette_row.setLayout(palette_row_layout)
        
        self.palette_buttons = {}
        
        palette_label = QLabel("Saved")
        palette_label.setFont(self.body_font)
        palette_row_layout.addWidget(palette_label)
        
        for x in range(0,6):
            color_ = QPushButton()
            self.palette_buttons[x] = color_
            color_.setMaximumHeight(20)
            color_.setMaximumWidth(20)
            color_.setMinimumWidth(20)
            color_.setMaximumWidth(20)
            try:
                color_.setStyleSheet("background-color:"+self.saved_palette[x])
                color_.value = self.saved_palette[x]
            except:
                color_.setStyleSheet("background-color: #000000")
                color_.value = "#000000"
                
            palette_row_layout.addWidget(color_)
            color_.clicked.connect(self.color_from_palette)
            
        color_edit_layout.addWidget(palette_row,3,0,1,2)
        
        self.history_index = 6
        self.palette_index = 6
            
    def initContent(self, s):
        s = s.lower()
        self.initItem(s)
            
    def initItem(self,item):
        print(item)
        self.counts[item] += 1
        if self.counts[item] <= self.max_counts[item]:

            t = item+" " + str(self.counts[item])
            
            self.parent.total_layers = len(self.parent.layer_orders)+1
            self.parent.layer_orders[self.parent.total_layers] = t
            self.parent.layers_box.clear()
            for g in self.parent.layer_orders:
                self.parent.layers_box.addItem(self.parent.layer_orders[g])
            #add stack widget
                
    def color_from_palette(self):
        color = self.sender().value
        self.active_color = color
        self.color_preview.setStyleSheet("background-color: "+self.active_color)
        self.color_hex.setText(self.active_color)
    
    def color_update(self):
        color = self.color_hex.text()
        if color == "":
            color = "#000000"
        if color.startswith("#") == False:
            color = "#" + color
        self.active_color = color
        self.color_preview.setStyleSheet("background-color: "+self.active_color)
        self.color_hex.setText(self.active_color)
        
        self.history_index -= 1
        if self.history_index == -1:
            self.history_index = 5
        self.color_history[self.history_index] = self.active_color
        self.color_history_buttons[self.history_index].value = self.active_color
        self.color_history_buttons[self.history_index].setStyleSheet("background-color: "+self.active_color)
        
        #set pixmap to color using mask
        
    def save_color(self):
        if self.color_hex.text() != "":
            self.palette_index -= 1
            if self.palette_index == -1:
                self.palette_index = 5
            self.saved_palette[self.palette_index] = self.color_hex.text()
            self.palette_buttons[self.palette_index].value = self.color_hex.text()
            self.palette_buttons[self.palette_index].setStyleSheet("background-color: "+self.color_hex.text())
            with open("src/tmp/pecp.trch", "w") as f:
                json.dump(self.saved_palette, f)
