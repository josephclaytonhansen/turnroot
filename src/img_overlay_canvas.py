from src.img_overlay import overlayTileWithoutScaling, createClippingMask
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from src.node_backend import getFiles, File
from src.pixmap_to_data import StoreQPixmap

import json, math, os, random, pickle

import src.UI_colorTheme as UI_colorTheme
from src.UI_updateJSON import updateJSON
data = updateJSON()
active_theme = getattr(UI_colorTheme, data["active_theme"])

from src.UI_Dialogs import confirmAction, popupInfo, infoClose
from src.game_directory import gameDirectory
from src.UI_portrait_editor_dialogs import portraitStackWidget
from src.portrait_editor_backend import layerDown, layerUp, layerDelete

class imageOverlayCanvas(QWidget):
    def __init__(self, parent=None,font=None):
        super().__init__(parent)
        
        self.path_no_ext = None
        self.path = None
        
        self.composites = {}
        
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
        self.center.setMaximumWidth(400)
        self.center.setMinimumWidth(400)
        self.center_layout = QVBoxLayout()
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
        
        self.sl_row = QWidget()
        self.sl_row_layout = QHBoxLayout()
        self.sl_row.setLayout(self.sl_row_layout)
        self.center_layout.addWidget(self.sl_row)
        
        for b in ["Save", "Load"]:
            slb = QPushButton(b)
            slb.setMaximumWidth(190)
            slb.setFont(self.body_font)
            slb.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+";")
            self.sl_row_layout.addWidget(slb)
            slb.what = b
            slb.clicked.connect(self.b_save_load)
        
        
        self.center_layout.addWidget(self.canvas)
        
        self.transform_pad = QWidget()
        self.transform_pad.setMaximumHeight(150)
        self.transform_pad_layout = QGridLayout()
        self.transform_pad_layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        self.transform_pad.setLayout(self.transform_pad_layout)
        
        self.transform_pad_buttons = {}
        self.tpb_locs = [[0,1],[1,2],[2,1],[1,0],[1,1]]
        index = -1
        
        self.timer = QTimer()
        
        for button in ["up", "right", "down", "left", "reset"]:
            index += 1
            self.transform_pad_buttons[button] = QPushButton()
            self.transform_pad_buttons[button].setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+";")
            self.transform_pad_buttons[button].direction = button
            
            if button != "reset":
                self.transform_pad_buttons[button].pressed.connect(self.on_press)
                self.transform_pad_buttons[button].released.connect(self.on_release)
                self.timer.timeout.connect(self.while_pressed)
            else:
                self.transform_pad_buttons[button].clicked.connect(self.reset_transform)
            
            self.transform_pad_buttons[button].setMaximumWidth(50)
            self.transform_pad_buttons[button].setMaximumHeight(50)
            self.transform_pad_buttons[button].setIcon(QIcon(QPixmap("src/ui_icons/white/"+button+".png")))
            self.transform_pad_buttons[button].setIconSize(QSize(48,48))
            self.transform_pad_layout.addWidget(self.transform_pad_buttons[button], self.tpb_locs[index][0], self.tpb_locs[index][1], 1, 1)
        
        self.layers_label = QLabel("Layers")
        self.layers_label.setFont(self.body_font)
        self.layers_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        
        self.layers_box = QListWidget()
        self.layers_box.currentRowChanged.connect(self.list_index_change)
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
        
        for b in [self.layer_up, self.layer_down, self.delete_layer]:
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
        
        self.current_layer_options_container = portraitStackWidget(parent=self,font=self.body_font)
        self.current_layer_options_container.setStyleSheet("background-color: "+active_theme.window_background_color+"; color:"+active_theme.window_text_color+";")
        self.current_layer_options_container.setMinimumHeight(300)
        
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

            self.add_options_layout.addWidget(self.add_options_buttons[button], self.aob_column, self.aob_row,1,1)
            
        self.left_buttons_row = QWidget()
        self.left_buttons_row_layout = QHBoxLayout()
        self.left_buttons_row.setLayout(self.left_buttons_row_layout)
        
        self.left_buttons= {}
        
        for button in ["add_image", "help"]:
            self.left_buttons[button] = QPushButton()
            self.left_buttons[button].setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+";")
            self.left_buttons[button].what = button
            
            self.left_buttons[button].clicked.connect(self.left_button_clicked)
            
            self.left_buttons[button].setMaximumWidth(58)
            self.left_buttons[button].setMaximumHeight(58)
            self.left_buttons[button].setIcon(QIcon(QPixmap("src/ui_icons/white/"+button+".png")))
            self.left_buttons[button].setIconSize(QSize(56,56))
            
            self.left_buttons_row_layout.addWidget(self.left_buttons[button])
        
        self.left_layout.addWidget(self.add_options)
        self.left_layout.addWidget(self.current_layer_options_container)
        self.left_layout.addWidget(self.left_buttons_row)
        
    def on_release(self):
        self.timer.stop()

    def on_press(self):
        self.timer.start(44)
        self.tmp_direction = self.sender().direction

    def while_pressed(self):
        self.move_overlay(self.tmp_direction)

    def move_overlay(self,direction):
        if direction == "up":
            self.layer_positions[self.layers_box.currentRow()][1] -= 1
            self.actually_move_overlay()
        elif direction == "right":
            self.layer_positions[self.layers_box.currentRow()][0] += 1
            self.actually_move_overlay()
        elif direction == "down":
            self.layer_positions[self.layers_box.currentRow()][1] += 1
            self.actually_move_overlay()
        elif direction == "left":
            self.layer_positions[self.layers_box.currentRow()][0] -= 1
            self.actually_move_overlay()
    
    def reset_transform(self):
        self.layer_positions[self.layers_box.currentRow()] = [0,0]
        self.render()
    
    def actually_move_overlay(self):
        self.overlay_dimensions = [360,520]
        if self.pos[0] > 360-self.overlay_dimensions[0]:
            self.pos[0] = 360-self.overlay_dimensions[0]
        if self.pos[0] < 0:
            self.pos[0] = 0
        if self.pos[1] > 520-self.overlay_dimensions[1]:
            self.pos[1] = 520-self.overlay_dimensions[1]
        if self.pos[1] < 0:
            self.pos[1] = 0
        self.render()
        self.main_up.save_status.setPixmap(QPixmap("src/ui_icons/white/file_not_saved.png").scaled(int(int(data["icon_size"])/1.5),int(int(data["icon_size"])/1.5), Qt.KeepAspectRatio))
        self.main_up.save_status.setToolTip("Portrait file not saved")
    
    def color_mask(self, bottom, color):
        if isinstance(bottom, str):
            mask = bottom.strip(".png")+"cm.png"
        else:
            mask = bottom
        self.img_bottom = QPixmap(bottom).scaled(360,520, Qt.KeepAspectRatio)
        self.img_mask = QPixmap(mask).scaled(360,520, Qt.KeepAspectRatio)
        self.img_top = QPixmap(bottom).scaled(360,520, Qt.KeepAspectRatio)
        self.overlay_dimensions = [self.img_mask.width(), self.img_mask.height()]
        composite = createClippingMask(self.img_bottom, self.img_mask, color, 360, 520)
        composite = overlayTileWithoutScaling(composite, self.img_top, 360, 520, [0,0])
        self.composites[self.layers_box.currentRow()] = composite
        self.render()
    
    def render(self):
        number = self.layers_box.count()-1
        painter = QPainter()
        result = QPixmap(360,520)
        result.fill(Qt.transparent)
        painter.begin(result)
        try:
            painter.drawPixmap(self.layer_positions[-1][0], self.layer_positions[-1][1],self.composites[-1].scaled(360,520, Qt.KeepAspectRatio))
        except:
            painter.drawPixmap(self.layer_positions[0][0], self.layer_positions[0][1],self.composites[0].scaled(360,520, Qt.KeepAspectRatio))
        for x in range(0, number+1):
            painter.drawPixmap(self.layer_positions[x][0], self.layer_positions[x][1], self.composites[x].scaled(360,520, Qt.KeepAspectRatio))
        self.canvas.setPixmap(result)
    
    def canvas_edit_change(self):
        self.current_layer_options_container.addRow(self.sender().name)
    
    def list_index_change(self,i):
        self.current_layer_options_container.refreshData(i)
        self.pos = [0,0]
        
    def move_layer_down(self):
        if self.layers_box.currentRow() < self.layers_box.count() - 1:
            layerDown(self)
    
    def move_layer_up(self):
        if self.layers_box.currentRow() > 0:
            layerUp(self)
    
    def layer_delete(self):
        if self.layers_box.currentRow() != -1:
            t = self.layers_box.currentRow()
            s = self.layers_box.currentItem().text()
            layerDelete(self, t, s)
    
    def left_button_clicked(self):
        print(self.sender().what)
    
    def b_save_load(self):
        if self.sender().what == "Save":
            self.save()
    
    def canvasToJSON(self):
        with open(self.path, "wb") as f:
            p = StoreQPixmap()
            pixmap_data = {}
            for img in self.composites:
                p._qpixmap[img] = self.composites[img]
            pixmap_data = p.to_data()
            data = {"poss":self.layer_positions,"orders":self.layer_orders,"attrs":self.layer_attributes,"imgs":pixmap_data}
            pickle.dump(data,f)
        #editable canvas
    
    def canvasToPNG(self):
        f = QFile(self.path+".png")
        f.open(QIODevice.ReadOnly)
        self.canvas.pixmap().save(f, "PNG")
        #flat image used for actual game
           
    def saveFileDialog(self):
        q = QFileDialog(self)
        self.main_up.save_status.setPixmap(QPixmap("src/ui_icons/white/file_saving.png").scaled(int(int(data["icon_size"])/1.5),int(int(data["icon_size"])/1.5), Qt.KeepAspectRatio))
        self.main_up.save_status.setToolTip("Portrait file saving")
        options = q.Options()
        options |= q.DontUseNativeDialog
        fileName, _ = q.getSaveFileName(None,"Save","","Turnroot Portrait (*.trsp)", options=options)
        if fileName:
            self.path = fileName+".trsp"
            g = infoClose("Saved portrait as "+self.path+"\nPlease note that changes will not auto-save")
            
            self.main_up.save_status.setPixmap(QPixmap("src/ui_icons/white/file_saved.png").scaled(int(int(data["icon_size"])/1.5),int(int(data["icon_size"])/1.5), Qt.KeepAspectRatio))
            self.main_up.save_status.setToolTip("Portrait file saved")
            g.exec_()
            
    def save(self):
        self.main_up.save_status.setPixmap(QPixmap("src/ui_icons/white/file_saving.png").scaled(int(int(data["icon_size"])/1.5),int(int(data["icon_size"])/1.5), Qt.KeepAspectRatio))
        self.main_up.save_status.setToolTip("Portrait file saving")
        
        if self.path == None or self.path == '':
            self.saveFileDialog()
            if self.path == None or self.path == '':
                c = infoClose("No file selected")
                c.exec_()
            else:
                self.canvasToJSON()
                self.canvasToPNG()
                    
                self.main_up.save_status.setPixmap(QPixmap("src/ui_icons/white/file_saved.png").scaled(int(int(data["icon_size"])/1.5),int(int(data["icon_size"])/1.5), Qt.KeepAspectRatio))
                self.main_up.save_status.setToolTip("Portrait file saved")

        else:
            self.canvasToJSON()
            self.canvasToPNG()
            
            self.main_up.save_status.setPixmap(QPixmap("src/ui_icons/white/file_saved.png").scaled(int(int(data["icon_size"])/1.5),int(int(data["icon_size"])/1.5), Qt.KeepAspectRatio))
            self.main_up.save_status.setToolTip("Portrait file saved")