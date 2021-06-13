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
from src.UI_portrait_editor_dialogs import portraitStackWidget
from src.portrait_editor_backend import layerDown, layerUp, layerDelete, layerRename

class imageOverlayCanvas(QWidget):
    def __init__(self, parent=None,font=None):
        super().__init__(parent)
        
        self.path_no_ext = None
        self.path = None
        
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        self.body_font = font
        
        self.setStyleSheet("background-color: "+active_theme.window_background_color+"; color:"+active_theme.window_text_color+"; font-size: 16")
        
        self.left = QWidget()
        self.left_layout = QVBoxLayout()
        self.left.setLayout(self.left_layout)
        
        self.right = QWidget()
        self.right.setMinimumWidth(210)
        self.right.setMaximumWidth(210)
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
        self.canvas.setStyleSheet("background-color: white; border: 2px solid black; border-radius: 3px;")
        self.canvas.setMinimumWidth(360)
        self.canvas.setMaximumWidth(360)
        self.canvas.setMinimumHeight(520)
        self.canvas.setMaximumHeight(520)
        
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
        self.layers_label.setFont(self.body_font)
        self.layers_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        
        self.layers_box = QListWidget()
        self.layers_box.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+";")
        
        self.layer_positions = {}
        self.layer_orders = {}
        self.layer_attributes = {}
        self.layer_images = {}
        
        self.edit_layers_row = QWidget()
        self.edit_layers_row_layout = QHBoxLayout()
        self.edit_layers_row.setLayout(self.edit_layers_row_layout)
        
        self.layer_up = QPushButton()
        self.layer_up.clicked.connect(self.move_layer_up)
        self.layer_up.setIcon(QIcon(QPixmap("src/ui_icons/white/layer_up.png")))
        
        self.layer_down = QPushButton()
        self.layer_down.clicked.connect(self.move_layer_down)
        self.layer_down.setIcon(QIcon(QPixmap("src/ui_icons/white/layer_down.png")))
        
        self.delete_layer = QPushButton()
        self.delete_layer.clicked.connect(self.layer_delete)
        self.delete_layer.setIcon(QIcon(QPixmap("src/ui_icons/white/delete.png")))
        
        self.rename_layer = QPushButton()
        self.rename_layer.clicked.connect(self.layer_rename)
        self.rename_layer.setIcon(QIcon(QPixmap("src/ui_icons/white/rename.png")))
        
        for b in [self.layer_up, self.layer_down, self.delete_layer, self.rename_layer]:
            b.setMaximumWidth(42)
            b.setMinimumWidth(42)
            b.setMinimumHeight(42)
            b.setMaximumHeight(42)
            b.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+";")
            b.setIconSize(QSize(40,40))
            self.edit_layers_row_layout.addWidget(b)
        
        self.right_layout.addWidget(self.layers_label)
        self.right_layout.addWidget(self.layers_box)
        self.right_layout.addWidget(self.edit_layers_row)
        self.right_layout.addWidget(self.transform_pad)
        
        self.current_layer_options_container = QWidget()
        self.current_layer_options_container.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+";")
        self.current_layer_options_container.setMinimumHeight(300)
        self.current_layer_options_container_layout = QStackedLayout()
        self.current_layer_options_container.setLayout(self.current_layer_options_container_layout)
        
        self.stacks = {}
        
        self.add_options = QWidget()
        self.add_options_layout = QGridLayout()
        self.add_options.setLayout(self.add_options_layout)
        
        self.add_options_buttons = {}
        self.aob_row = -1
        self.aob_column = 0
        self.buttons =  ["Base", "Hair", "Eyes", "Nose", "Mouth", "Scars", "Freckles", "Jewelry",
                       "Masks", "Tattoos", "Facial Hair", "Eyebrows", "Makeup", "Headwear", "Tops", "Armor"]
        
        #"Bottoms", "Shoes", "Belts", "Gloves"
        for button in self.buttons:
            self.aob_row +=1
            if self.aob_row == 4:
                self.aob_row = 0
                self.aob_column += 1
                
            self.add_options_buttons[button] = QPushButton(button)
            self.add_options_buttons[button].setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+";")
            self.add_options_buttons[button].clicked.connect(self.canvas_edit_change)
            self.add_options_buttons[button].setMinimumHeight(40)
            self.add_options_buttons[button].name = button
            self.add_options_buttons[button].setFont(self.body_font)
            
            widget = portraitStackWidget(parent=self,font=self.body_font,stack=button)
            self.stacks[button] = widget
            
            self.current_layer_options_container_layout.addWidget(widget)
            self.add_options_layout.addWidget(self.add_options_buttons[button], self.aob_column, self.aob_row,1,1)
        
        self.left_layout.addWidget(self.add_options)
        self.left_layout.addWidget(self.current_layer_options_container)
            
        ###TESTING ONLY###
        self.image1 = QPixmap("src/portrait_graphics/blue.png")
        self.image2 = QPixmap("src/portrait_graphics/yellow.png")
        self.image3 = QPixmap("src/portrait_graphics/pink.png")
        self.overlay_dimensions = [self.image2.width(), self.image2.height()]
        self.pos = [135,188]
        composite = overlayTileWithoutScaling(self.image1, self.image2, 336, 468, self.pos)
        composite = overlayTileWithoutScaling(composite, self.image3, 336, 468, self.pos)
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
        if self.pos[0] > 336-self.overlay_dimensions[0]:
            self.pos[0] = 336-self.overlay_dimensions[0]
        if self.pos[0] < 0:
            self.pos[0] = 0
        if self.pos[1] > 468-self.overlay_dimensions[1]:
            self.pos[1] = 468-self.overlay_dimensions[1]
        if self.pos[1] < 0:
            self.pos[1] = 0
        composite = overlayTileWithoutScaling(self.image1, self.image2, 336, 468, self.pos)
        composite = overlayTileWithoutScaling(composite, self.image3, 336, 468, [135,188])
        self.canvas.setPixmap(composite)
    
    def canvas_edit_change(self):
        self.stacks[self.sender().name].initContent(self.sender().name)
        for x in range(0, len(self.buttons)):
            if (self.sender().name == self.buttons[x]):
                ind = x
                self.current_layer_options_container_layout.setCurrentIndex(ind)

    def move_layer_down(self):
        layerDown(self)
    
    def move_layer_up(self):
        layerUp(self)
    
    def layer_delete(self):
        if self.layers_box.currentRow() != -1:
            t = self.layers_box.currentRow()
            layerDelete(self, t)
    
    def layer_rename(self):
        if self.layers_box.currentRow() != -1:
            t = self.layers_box.currentRow()
            layerRename(self, t)
    
    def canvasToJSON(self):
        with open("src/skeletons/portraits/"+self.path) as f:
            data = {"poss":self.layer_positions,"orders":self.layer_orders,"attrs":self.layer_attributes,"imgs":self.layer_images}
            json.load(data,f)
        #editable canvas
    
    def canvasToPNG(self):
        self.canvas.pixmap.save("src/skeletons/portrait_images/"+self.path_no_ext, "PNG")
        #flat image used for actual game