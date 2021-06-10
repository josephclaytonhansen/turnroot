from src.img_overlay import overlayTileWithoutScaling
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from src.node_backend import getFiles, File

import json, math, os, random

import src.UI_colorTheme as UI_colorTheme
from src.UI_updateJSON import updateJSON
data = updateJSON()
active_theme = getattr(UI_colorTheme, data["active_theme"])

from src.UI_Dialogs import confirmAction, popupInfo, infoClose
from src.game_directory import gameDirectory

class imageOverlayCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        
        self.setStyleSheet("background-color: "+active_theme.window_background_color+"; color:"+active_theme.window_text_color+"; font-size: 16")
        
        self.left = QWidget()
        self.left_layout = QVBoxLayout()
        self.left.setLayout(self.left_layout)
        
        self.right = QWidget()
        self.right.setMinimumWidth(170)
        self.right.setMaximumWidth(170)
        self.right_layout = QVBoxLayout()
        self.right.setLayout(self.right_layout)
        
        self.center = QWidget()
        self.center.setMaximumWidth(520)
        self.center.setMinimumWidth(520)
        self.center_layout = QHBoxLayout()
        self.center.setLayout(self.center_layout)
        
        self.layout.addWidget(self.left)
        self.layout.addWidget(self.center)
        self.layout.addWidget(self.right)
        
        self.canvas = QLabel()
        self.canvas.setAlignment(Qt.AlignCenter)
        self.canvas.setStyleSheet("background-color: white; border: 4px solid black; border-radius: 3px;")
        self.canvas.setMinimumWidth(512)
        self.canvas.setMaximumWidth(512)
        self.canvas.setMinimumHeight(512)
        self.canvas.setMaximumHeight(512)
        
        self.center_layout.addWidget(self.canvas)
        
        self.transform_pad = QWidget()
        self.transform_pad.setMaximumHeight(150)
        self.transform_pad_layout = QGridLayout()
        self.transform_pad_layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        self.transform_pad.setLayout(self.transform_pad_layout)
        
        self.transform_pad_buttons = {}
        self.tpb_locs = [[0,1],[1,2],[2,1],[1,0]]
        index = -1
        
        self.timer = QTimer()
        
        for button in ["up", "right", "down", "left"]:
            index += 1
            self.transform_pad_buttons[button] = QPushButton()
            self.transform_pad_buttons[button].setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+";")
            self.transform_pad_buttons[button].direction = button

            self.transform_pad_buttons[button].pressed.connect(self.on_press)
            self.transform_pad_buttons[button].released.connect(self.on_release)
            self.timer.timeout.connect(self.while_pressed)
            
            self.transform_pad_buttons[button].setMaximumWidth(50)
            self.transform_pad_buttons[button].setMaximumHeight(50)
            self.transform_pad_buttons[button].setIcon(QIcon(QPixmap("src/ui_icons/white/"+button+".png")))
            self.transform_pad_buttons[button].setIconSize(QSize(48,48))
            self.transform_pad_layout.addWidget(self.transform_pad_buttons[button], self.tpb_locs[index][0], self.tpb_locs[index][1], 1, 1)
        
        self.layers_label = QLabel("Layers")
        self.layers_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        
        self.layers_box = QListWidget()
        self.layers_box.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+";")
        
        self.edit_layers_row = QWidget()
        self.edit_layers_row_layout = QHBoxLayout()
        self.edit_layers_row.setLayout(self.edit_layers_row_layout)
        
        self.edit_layer_name = QPushButton()
        self.edit_layer_name.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+";")
        self.edit_layer_name.setMaximumWidth(40)
        self.edit_layer_name.setMinimumWidth(40)
        self.edit_layer_name.setMaximumHeight(40)
        self.edit_layer_name.setMinimumHeight(40)
        self.edit_layer_name.setIcon(QIcon(QPixmap("src/ui_icons/white/edit.png")))
        self.edit_layer_name.setIconSize(QSize(38,38))
        
        self.delete_layer = QPushButton()
        self.delete_layer.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+";")
        self.delete_layer.setMaximumWidth(40)
        self.delete_layer.setMinimumWidth(40)
        self.delete_layer.setMaximumHeight(40)
        self.delete_layer.setMinimumHeight(40)
        self.delete_layer.setIcon(QIcon(QPixmap("src/ui_icons/white/delete.png")))
        self.delete_layer.setIconSize(QSize(38,38))
        
        self.edit_layers_row_layout.addWidget(self.edit_layer_name)
        self.edit_layers_row_layout.addWidget(self.delete_layer)
        
        self.right_layout.addWidget(self.layers_label)
        self.right_layout.addWidget(self.layers_box)
        self.right_layout.addWidget(self.edit_layers_row)
        self.right_layout.addWidget(self.transform_pad)
        
        self.current_layer_options_container = QWidget()
        self.current_layer_options_container.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+";")
        self.current_layer_options_container.setMinimumHeight(300)
        self.current_layer_options_container_layout = QStackedLayout()
        self.current_layer_options_container.setLayout(self.current_layer_options_container_layout)
        
        self.add_options = QWidget()
        self.add_options_layout = QGridLayout()
        self.add_options.setLayout(self.add_options_layout)
        
        self.add_options_buttons = {}
        self.aob_row = -1
        self.aob_column = 0
        
        for button in ["Base", "Hair", "Eyes", "Nose", "Mouth", "Scars", "Freckles", "Jewelry", "Tattoos", "Facial Hair", "Eyebrows", "Makeup", "Headwear", "Bodywear"]:
            self.aob_row +=1
            if self.aob_row == 4:
                self.aob_row = 0
                self.aob_column += 1
                
            self.add_options_buttons[button] = QPushButton(button)
            self.add_options_buttons[button].setMinimumHeight(40)
            self.add_options_buttons[button].setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+";")
            self.add_options_buttons[button].name = button
            
            self.add_options_layout.addWidget(self.add_options_buttons[button], self.aob_column, self.aob_row,1,1)
        
        self.left_layout.addWidget(self.add_options)
        self.left_layout.addWidget(self.current_layer_options_container)
            
        ###TESTING ONLY###
        self.image1 = QPixmap("src/portrait_graphics/blue.png")
        self.image2 = QPixmap("src/portrait_graphics/yellow.png")
        self.overlay_dimensions = [self.image2.width(), self.image2.height()]
        self.pos = [256,256]
        composite = overlayTileWithoutScaling(self.image1, self.image2, 512, self.pos)
        self.canvas.setPixmap(composite)
        #self.canvas.setPixmap(composite).scaled(self.canvas_size, self.canvas_size, Qt.KeepAspectRatio, Qt.FastTransformation)
        
    def on_release(self):
        self.timer.stop()

    def on_press(self):
        self.timer.start(25)
        self.tmp_direction = self.sender().direction

    def while_pressed(self):
        self.move_overlay(self.tmp_direction)

    def move_overlay(self,direction):
        if direction == "up":
            self.pos[1] -= 1
            self.actually_move_overlay()
        elif direction == "right":
            self.pos[0] += 1
            self.actually_move_overlay()
        elif direction == "down":
            self.pos[1] += 1
            self.actually_move_overlay()
        elif direction == "left":
            self.pos[0] -= 1
            self.actually_move_overlay()
    
    def actually_move_overlay(self):
        if self.pos[0] > 512-self.overlay_dimensions[0]:
            self.pos[0] = 512-self.overlay_dimensions[0]
        if self.pos[0] < 0:
            self.pos[0] = 0
        if self.pos[1] > 512-self.overlay_dimensions[1]:
            self.pos[1] = 512-self.overlay_dimensions[1]
        if self.pos[1] < 0:
            self.pos[1] = 0
        composite = overlayTileWithoutScaling(self.image1, self.image2, 512, self.pos)
        self.canvas.setPixmap(composite)