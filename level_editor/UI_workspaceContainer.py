from PyQt5.QtCore import QSize, Qt, pyqtSignal, QObject
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QPalette, QIcon, QPixmap, QCursor
import qtmodern.styles
import qtmodern.windows
from UI_updateJSON import updateJSON
from UI_ProxyStyle import ProxyStyle
from UI_Dialogs import confirmAction
import UI_colorTheme
from UI_color_test_widget import Color
from tasks_backend import getFillSquares
import json, math, re, sys, os

#don't edit these
current_tile = None
previous_sender = None
current_sender = None
tiles = {0:{}, 1:{}, 2:{}, 3:{}, 4:{}, 5:{}, 6:{}}
ttype = ""

#these can be edited
tile_stack = ["simple_grasslands_jungle", "simple_grasslands", "simple_grasslands_jungle_walls"]
task_categories = ["Tiles", "Tile Effects", "Level Events"]

#don't edit these
tile_set = tile_stack[0]
ttype_label = None
ttype_pix = None
ttype_img = None
p_ttype_pix = None
p_ttype_label = None
current_stack = tile_set
playout = None
level_data = {}
current_name = None
highlighted_tile = None
ht = None
lpt = None
task_history = [None,None,None,None]
current_task = None
tile_preview_fwt = None
tile_ratio = 0
global_squares = {}
global_open_settings = 0
tile_preview_rwt_to = None
tile_preview_rwt_from = None

class LevelData():
    def __init__(self):
        global level_data
        self.level_data = level_data

class TileSets():
    def __init__(self):
        self.tile_stack = tile_stack

with open("tiles/"+tile_set+".json", "r") as read_file:
    read_file.seek(0)
    tile_data = json.load(read_file)
    read_file.close()
    
class workspaceContainer(QWidget):
        def __init__(self, workspace, layout):
            super().__init__()
            self.setAutoFillBackground(True)
            data = updateJSON()
            self.active_theme = getattr(UI_colorTheme, data["active_theme"])
            self.setStyleSheet("font-size: "+str(data["font_size"])+"px;color: "+self.active_theme.window_text_color)
            palette = self.palette()
            self.background_color = QColor(self.active_theme.workspace_background_color)
            palette.setColor(QPalette.Window, self.background_color)
            self.setPalette(palette)
            self.layout = QVBoxLayout()
            self.layout.setContentsMargins(2,2,2,2)
            self.layout.setSpacing(4)
            self.label = QLabel("Label")
            font = self.label.font()
            font.setPointSize(int(data["icon_size"])/2)
            self.label.setFont(font)
            self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

            self.layout.addWidget(self.label)
            self.layout.addWidget(Color(self.active_theme.window_background_color))
            self.layout.addWidget(Color(self.active_theme.list_background_color))
            self.setLayout(self.layout)

class showWorkspace(QPushButton):
    def __init__(self, workspace, layout):
        super().__init__()
        data = updateJSON()
        self.workspace = workspace
        self.layout = layout
        self.active_theme = getattr(UI_colorTheme, data["active_theme"])
        self.setText("+")
        self.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.setFixedSize((int(data["icon_size"]) -3), (int(data["icon_size"]) -3))
        
class hideWorkspace(QPushButton):
    def __init__(self, workspace, layout):
        super().__init__()
        data = updateJSON()
        self.workspace = workspace
        self.layout = layout
        self.active_theme = getattr(UI_colorTheme, data["active_theme"])
        self.setText("—")
        self.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.setFixedSize((int(data["icon_size"])-3), (int(data["icon_size"])-3))

class tileGridWorkspace(QWidget):
    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)
        self.squares = {}
        self.count = 0
        self.checker = 0
        self.layout = QGridLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)
        self.width = self.geometry().width()
        self.height = self.geometry().height()
        
        self.setMinimumWidth(self.width)
        self.setMaximumHeight(self.height)
        self.ratio = self.width/self.height
        #each square is ratio width/1 height
        global tile_ratio
        for x in range(0,int(int(self.height/(50*self.ratio))*4.4)):
            self.checker = self.checker + 1
            for y in range(0,int(int(self.width/50)*4.4)):
                
                self.count = self.count + 1
                level_data[self.count] = 'e'
                self.checker = self.checker + 1
                self.squares[self.count] = ClickableQLabel_t()
                self.squares[self.count].setMouseTracking(True)
                self.squares[self.count].gridIndex = self.count
                self.squares[self.count].setScaledContents( True )
                self.squares[self.count].clicked.connect(self.change_color)
                self.squares[self.count].right_clicked.connect(self.reset_color)
                self.squares[self.count].setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.layout.addWidget(self.squares[self.count], x, y)
                if self.checker % 2 == 0:
                    self.squares[self.count].setStyleSheet("color: white; background-color: black;")
                else:
                    self.squares[self.count].setStyleSheet("color: white; background-color: #222222;")
                if x % 3 == 0 and y % 3 == 0:
                    self.squares[self.count].setText(str(self.squares[self.count].gridIndex))
        tile_ratio = y + 1
        global global_squares
        global_squares = self.squares
        self.setLayout(self.layout)
    
    def change_color(self):
        global current_tile
        global level_data
        global current_name
        try:
            self.sender().setPixmap(current_tile)
            level_data[self.sender().gridIndex] = current_name
        except:
            pass
   
    def reset_color(self):
        self.sender().clear()
    
class ClickableQLabel_t(QLabel):
    clicked=pyqtSignal()
    global highlighted_tile
    right_clicked=pyqtSignal()
    def mousePressEvent(self, ev):
        if ev.button() == Qt.LeftButton:
            global ht
            ht.setText("Current grid space: "+str(highlighted_tile))
            self.clicked.emit()
        elif ev.button() == Qt.RightButton:
            self.right_clicked.emit()
            
    def mouseMoveEvent(self, ev):
        highlighted_tile=self.gridIndex
        global ht
        ht.setText("Current grid space: "+str(highlighted_tile))

class ClickableQLabel(QLabel):
    clicked=pyqtSignal()
    global highlighted_tile
    right_clicked=pyqtSignal()
    QLabel.gridIndex = 0
    def mousePressEvent(self, ev):
        if ev.button() == Qt.LeftButton:
            self.clicked.emit()
        elif ev.button() == Qt.RightButton:
            self.right_clicked.emit()

class toolsWorkspace(QWidget):
        def __init__(self, workspace, layout, labels):
            super().__init__()
            self.setAutoFillBackground(True)
            data = updateJSON()
            self.active_theme = getattr(UI_colorTheme, data["active_theme"])
            self.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
            
            self.layout = QVBoxLayout()
            self.layout.setContentsMargins(0,0,0,0)
            self.layout.setSpacing(0)
            self.k = QWidget()
            self.k.setMinimumHeight(0)
            self.k.setMinimumWidth(int(data["icon_size"])+6)
            self.layout.addWidget(self.k)
            for x in range(0, len(labels)):
                self.layout.addWidget(labels[x])
                labels[x].setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                labels[x].setMinimumHeight(int(data["icon_size"]))
                labels[x].setMinimumWidth(int(data["icon_size"]))
            self.setLayout(self.layout)
            
class TilesInfo(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)
        data = updateJSON()
        self.setTabPosition(QTabWidget.South)
        global tiles
        global ttype
        global ttype_label
        global ttype_pix
        global p_ttype_label
        global p_ttype_pix
        global ttype_name
        global tile_stack
        global highlighted_tile
        global ht
       
        ttype_label = QLabel("tile type")
        ttype_pix = QLabel()
        p_ttype_label = ClickableQLabel()
        p_ttype_label.clicked.connect(self.assignLastTile)
        pr_label = QLabel("  Previous tile (click to select)  ")
        
        ht = QLabel()
       
        p_ttype_label.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        pr_label.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        ttype_label.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        ttype_pix.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        ht.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        self.layout.addWidget(ttype_pix)
        self.layout.addWidget(ttype_label)
        self.layout.addWidget(pr_label)
        self.layout.addWidget(p_ttype_label)
        self.layout.addWidget(ht)
        
        ttype_label.setMaximumHeight(40)
        pr_label.setMaximumHeight(40)
        
        self.active_theme = getattr(UI_colorTheme, data["active_theme"])
        p_ttype_label.setStyleSheet("font-size: "+str(data["font_size"]-2)+"px; background-color: "+self.active_theme.list_background_color+";color: "+self.active_theme.window_text_color)
        ttype_label.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        ttype_pix.setStyleSheet("font-size: "+str(data["font_size"]-2)+"px; background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        pr_label.setStyleSheet("font-size: "+str(data["font_size"]-2)+"px; background-color: "+self.active_theme.list_background_color+";color: "+self.active_theme.window_text_color)
        ht.setStyleSheet("font-size: "+str(data["font_size"]-2)+"px; background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        self.wi = QWidget()
        self.wi.setLayout(self.layout)
        self.addTab(self.wi, "Selections")
        
        self.select_tilesheet_layout = QVBoxLayout()
        self.select_tilesheet_layout.setContentsMargins(0,0,0,0)
        self.select_tilesheet_layout.setSpacing(0)
        self.tile_list = QListWidget()
        self.tile_list.addItems(tile_stack)
        self.tile_list.currentTextChanged.connect(self.text_changed)
        self.select_tilesheet_layout.addWidget(self.tile_list)
        self.twi = QWidget()
        self.twi.setStyleSheet("font-size: "+str(data["font_size"]-2)+"px; background-color: "+self.active_theme.list_background_color+";color: "+self.active_theme.window_text_color)
        self.twi.setLayout(self.select_tilesheet_layout)
        self.addTab(self.twi, "Sheets")
        
    def text_changed(self, s):
        global playout
        global tile_stack
        playout.setCurrentIndex(tile_stack.index(s))
        pass
            
    def assignLastTile(self):
        global current_tile
        global previous_sender
        global current_sender
        global p_ttype_label
        global ttype_pix
        global ttype
        try:
            ttype = previous_sender.ttype
            ttype_img = previous_sender.pixmap()
            ttype_label.setText(ttype)
            ttype_pix.setPixmap(ttype_img.scaled(int(64), int(64), Qt.KeepAspectRatio))
            current_sender = previous_sender
            current_tile = current_sender.pixmap()
        except:
            pass
        
class Tiles(QWidget):
    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)
        data = updateJSON()
        
        global tiles
        global ttype
        global p_ttype_label
        global tile_stack
        global playout
        self.w = TilesInfo()
        self.stacks = {}
        self.active_theme = getattr(UI_colorTheme, data["active_theme"])
        self.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: black;color: "+self.active_theme.window_text_color)
        
        for x in range(0, len(tile_stack)):
            self.stacks[x] = QWidget()
            self.pixmap = QPixmap("tiles/"+tile_stack[x]+".png")
            with open("tiles/"+tile_stack[x]+".json", "r") as read_file:
                read_file.seek(0)
                tile_data = json.load(read_file)
                read_file.close()
            
            self.label = QLabel()
            self.label.setPixmap(self.pixmap)
            
            self.layout = QGridLayout()
            self.layout.setSpacing(1)
            self.layout.setContentsMargins(0,0,0,0)
            self.stacks[x].setLayout(self.layout)
            
            self.count = 0
                
            for x in range(0,int(self.pixmap.width()/32)):
                for y in range(0,int(self.pixmap.height()/32)):
                    self.count +=1
                    tiles[y][x] = ClickableQLabel_t()
                    tiles[y][x].count = self.count
                    tiles[y][x].clicked.connect(self.assignCurrentTile)

                    tiles[y][x].setPixmap(self.pixmap.copy(x*32, y*32, 32, 32).scaled(int(64), int(64), Qt.KeepAspectRatio))
                    tiles[y][x].setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
                    td = tile_data[str(y)][str(x)]
                    tiles[y][x].ttype = tile_data["6"][str(td[1])]
                    tiles[y][x].ttype_name_s = td[0]
                    ttype = tile_data["6"][str(td[1])]
                    
                    self.layout.addWidget(tiles[y][x], y+1, x+1)
        
        playout = QStackedLayout()
        for x in range(0, len(tile_stack)):
            playout.addWidget(self.stacks[x])
        self.setLayout(playout)
        playout.setCurrentIndex(0)
    
    def assignCurrentTile(self):
        global current_tile
        global previous_sender
        global current_sender
        previous_sender = current_sender
        global tiles
        global ttype_pix
        global p_ttype_label
        global level_data
        global current_name
        global tile_preview_rwt_to
        global tile_preview_rwt_from
     
        try:
            previous_sender.setStyleSheet("background-color: black;")
            p_ttype_label.setPixmap(previous_sender.pixmap())
        except:
            pass
        
        current_sender = self.sender()
        current_tile = self.sender().pixmap()
        current_name = current_sender.ttype_name_s

        ttype = current_sender.ttype
        ttype_img = current_sender.pixmap()
        ttype_label.setText(ttype)
        ttype_pix.setPixmap(ttype_img.scaled(int(64), int(64), Qt.KeepAspectRatio))
        
        #connect to fwt task, rwt task
        tile_preview_fwt.setPixmap(ttype_img.scaled(int(64), int(64), Qt.KeepAspectRatio))
        try:
            tile_preview_rwt_from.setPixmap(previous_sender.pixmap().scaled(int(64), int(64), Qt.KeepAspectRatio))
            tile_preview_rwt_to.setPixmap(ttype_img.scaled(int(64), int(64), Qt.KeepAspectRatio))
        except:
            pass
        
        self.sender().setStyleSheet("background-color: "+self.active_theme.window_background_color+";")

class taskInList(object):
    def __init__(self, name, category):
        global task_categories
        self.task_categories = task_categories
        self.name = name
        self.category = self.task_categories[category]
        
class TaskSelection(QWidget):
    def __init__(self):
            super().__init__()
            self.setAutoFillBackground(True)
            data = updateJSON()
            self.active_theme = getattr(UI_colorTheme, data["active_theme"])
            self.setStyleSheet("font-size: "+str(data["font_size"]-2)+"px; background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
   
            self.layout = QVBoxLayout()
            self.layout.setContentsMargins(0,0,0,0)
            self.layout.setSpacing(0)
            
            self.tasks_box = QWidget()
            self.tb_layout = QGridLayout()

            self.tasks = [taskInList("Fill Area with Tile", 0),
                          taskInList("Replace Tile with Tile", 0),
                          taskInList("Random Decorations Collection", 0),
                          taskInList("Blend Water Depth Edges", 0),
                          taskInList("Add Trap", 1),
                          taskInList("Add Fire", 1),
                          taskInList("Add Door", 1),
                          taskInList("Add Chest", 1),
                          taskInList("Add Warp", 1),
                          taskInList("Add Switch", 1),
                          taskInList("Add Heal", 1),
                          taskInList("Add Emplacement", 1),
                          taskInList("Set Start Tiles", 2),
                          taskInList("Level Turn Options", 2),
                          taskInList("Win/Lose Conditions", 2),
                          taskInList("Add Event Trigger", 2),
                          taskInList("Spawn Point", 2),
                          taskInList("Reach Point", 2),
                          taskInList("Defend Point", 2),
                          taskInList("Seize Point", 2),
                          taskInList("Fog and Mist", 2),
                          ]
            
            self.task_strings = []
            self.search = QComboBox()

            for x in range(0, len(self.tasks)):
                if len(self.tasks[x].name) > 16:
                    self.space_count = 0
                    self.s = self.tasks[x].name
                    for m in re.finditer(' ', self.tasks[x].name):
                        self.space_count += 1
                        if self.space_count % 2 == 0:
                            self.s = self.s[:m.start()] + "\n" + self.s[m.start() + 1:]
                            self.tasks[x].name = self.s
                self.task_strings.append(self.tasks[x].name)
            self.search.addItems(self.task_strings)
                
            self.filter = QLabel("Filter tasks:")
            self.search_label = QLabel("Choose task from dropdown")
            self.buttons_label = QLabel("Choose from all tasks")
            
            global task_categories
            
            self.sh_0 = QCheckBox(task_categories[0])
            self.sh_1 = QCheckBox(task_categories[1])
            self.sh_2 = QCheckBox(task_categories[2])
            
            self.sh_0.setCheckState(Qt.Checked)
            self.sh_1.setCheckState(Qt.Checked)
            self.sh_2.setCheckState(Qt.Checked)
            
            self.sh_0.stateChanged.connect(self.toggleCategoryTiles)
            self.sh_1.stateChanged.connect(self.toggleCategoryTilesEffects)
            self.sh_2.stateChanged.connect(self.toggleCategoryLevelEvents)
            
            self.search.setMinimumHeight(data["font_size"] * 3.5)
            self.buttons_label.setMinimumHeight(data["font_size"] * 2.5)
            self.buttons_label.setMaximumHeight(data["font_size"] * 2.5)
            self.search.setStyleSheet("background-color: "+self.active_theme.list_background_color+"; selection-background-color:"+self.active_theme.window_background_color)
            self.search_label.setMaximumHeight(data["font_size"] * 3.5)
            self.search_label.setMinimumHeight(data["font_size"] * 3.5)
            self.filter.setMaximumHeight(data["font_size"] * 3.5)
            self.filter.setMinimumHeight(data["font_size"] * 3.5)
            self.sh_0.setMaximumHeight(data["font_size"] * 1.4)
            self.sh_1.setMaximumHeight(data["font_size"] * 1.4)
            self.sh_2.setMaximumHeight(data["font_size"] * 1.4)

            self.rows = 0
            self.tb_layout.addWidget(self.search_label, self.rows, 0)
            self.tb_layout.addWidget(self.search, self.rows+1, 0)
            self.tb_layout.addWidget(self.filter, self.rows+2,0)
            self.tb_layout.addWidget(self.sh_0, self.rows+3,0)
            self.tb_layout.addWidget(self.sh_1, self.rows+3,1)
            self.tb_layout.addWidget(self.sh_2, self.rows+4,0)
            self.tb_layout.addWidget(self.buttons_label, self.rows+5,0)
            
            self.setContextMenuPolicy(Qt.CustomContextMenu)
            self.customContextMenuRequested.connect(self.context_menu)
            
            self.task_buttons = {}
            self.ccolumn = 1
            self.crow = self.rows+6
            for x in range(0, len(self.tasks)):
                self.task_buttons[x] = QPushButton(self.tasks[x].name)
                self.task_buttons[x].clicked.connect(self.TaskFromButton)
                self.tb_layout.addWidget(self.task_buttons[x], x+self.crow, self.ccolumn)
                self.ccolumn += 1
                if self.ccolumn == 2:
                    self.ccolumn = 0
                    self.crow -=1
                if task_categories.index(self.tasks[x].category) % 2 == 0:
                    self.task_buttons[x].setStyleSheet("background-color:"+self.active_theme.button_alt_color+"; color:"+self.active_theme.button_alt_text_color)
            
            self.search.currentTextChanged.connect(self.TaskFromComboBox)
            
            self.tasks_box.setLayout(self.tb_layout)
            self.layout.addWidget(self.tasks_box)
            
            self.tb_layout.setSpacing(8)
            self.tb_layout.setContentsMargins(2,2,2,2)
            
            self.setLayout(self.layout)
        
    def toggleCategoryTiles(self, s):
        if s==0:
            for x in range(0, len(self.tasks)):
                if self.tasks[x].category == "Tiles":
                    self.task_buttons[x].hide()
        else:
            for x in range(0, len(self.tasks)):
                if self.tasks[x].category == "Tiles":
                    self.task_buttons[x].show()
    
    def toggleCategoryTilesEffects(self, s):
        if s==0:
            for x in range(0, len(self.tasks)):
                if self.tasks[x].category == "Tile Effects":
                    self.task_buttons[x].hide()
        else:
            for x in range(0, len(self.tasks)):
                if self.tasks[x].category == "Tile Effects":
                    self.task_buttons[x].show()
    
    def toggleCategoryLevelEvents(self, s):
        if s==0:
            for x in range(0, len(self.tasks)):
                if self.tasks[x].category == "Level Events":
                    self.task_buttons[x].hide()
        else:
            for x in range(0, len(self.tasks)):
                if self.tasks[x].category == "Level Events":
                    self.task_buttons[x].show()
                    
    def context_menu(self, pos):
        global task_history
        self.context = QMenu(self)
        self.context.addAction(QAction(task_history[0], self))
        self.context.addAction(QAction(task_history[1], self))
        self.context.addAction(QAction(task_history[2], self))
        self.context.exec_(self.mapToGlobal(pos))

    def TaskFromButton(self):
        global current_task, global_open_settings
        s = self.sender().text()
        for task in range(0, len(self.tasks)):
            if s == self.tasks[task].name:
                current_task = self.tasks[task]
                current_task = self.tasks.index(current_task)
                global_open_settings.setCurrentIndex(current_task)
    
    def TaskFromComboBox(self,s):
        global current_task, global_open_settings
        for task in range(0, len(self.tasks)):
            if s == self.tasks[task].name:
                current_task = self.tasks[task]
                current_task = self.tasks.index(current_task)
                global_open_settings.setCurrentIndex(current_task)

class TaskSettings(QWidget):
    def __init__(self):
            super().__init__()
            self.setAutoFillBackground(True)
            data = updateJSON()
            self.active_theme = getattr(UI_colorTheme, data["active_theme"])
            self.setStyleSheet("font-size: "+str(data["font_size"]-2)+"px; background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
            self.stacks = []
            
            #task: Fill Area with Tiles
            self.fill_with_tiles_widget = QWidget()
            self.fill_with_tiles_widget.setStyleSheet("font-size: "+str(data["font_size"]-2)+"px; background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
            self.fill_with_tiles_widget_layout = QVBoxLayout()
            
            global current_sender, global_open_settings, tile_preview_fwt
             
            tile_preview_fwt = QLabel()
            tile_preview_fwt.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            self.fwt_label = QLabel("Fill Area With Tile")
            self.fwt_label.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            
            self.fwt_corners_layout = QHBoxLayout()
            self.fwt_corners = QWidget()
            self.fwt_tl_corner = QSpinBox()
            self.fwt_br_corner = QSpinBox()
            global tile_ratio
            self.fwt_tl_corner.setRange(1,2560)
            self.fwt_br_corner.setRange(1,2560)
            
            self.fwt_corners_labels = QWidget()
            self.fwt_corners_labels_layout = QHBoxLayout()
            self.fwt_corners_labels_layout.addWidget(QLabel("Top left corner"))
            self.fwt_corners_labels_layout.addWidget(QLabel("Bottom right corner"))
            self.fwt_corners_labels.setLayout(self.fwt_corners_labels_layout)
            
            self.fwt_corners_layout.addWidget(self.fwt_tl_corner)
            self.fwt_corners_layout.addWidget(self.fwt_br_corner)
            self.fwt_corners.setLayout(self.fwt_corners_layout)
            
            self.go_button = QPushButton("Fill area")
            self.go_button.clicked.connect(self.fwt_fill)

            self.fill_with_tiles_widget_layout.addWidget(self.fwt_label)
            self.fill_with_tiles_widget_layout.addWidget(tile_preview_fwt)
            self.fill_with_tiles_widget_layout.addWidget(self.fwt_corners_labels)
            self.fill_with_tiles_widget_layout.addWidget(self.fwt_corners)
            self.fill_with_tiles_widget_layout.addWidget(self.go_button)
            #end stack
            #task: Replace Tile With Tile
            global tile_preview_rwt_to, tile_preview_rwt_from

            self.replace_tile_with_tile_widget = QWidget()
            self.replace_tile_with_tile_widget.setStyleSheet("font-size: "+str(data["font_size"]-2)+"px; background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
            self.replace_tile_with_tile_widget_layout = QVBoxLayout()
            self.replace_tile_with_tile_widget.setLayout(self.replace_tile_with_tile_widget_layout)
            
            self.rwt_label = QLabel("Replace Tile With Tile")
            self.rwt_label.setMaximumHeight(data["font_size"]*2)
            self.rwt_label.setAlignment(Qt.AlignHCenter)
            
            self.rwt_boxes_layout = QHBoxLayout()
            self.rwt_boxes = QWidget()
            tile_preview_rwt_from = QLabel()
            tile_preview_rwt_from.setAlignment( Qt.AlignHCenter)
            tile_preview_rwt_to = QLabel()
            tile_preview_rwt_to.setAlignment(Qt.AlignHCenter)

            self.rwt_boxes_labels = QWidget()
            self.rwt_boxes_labels_layout = QHBoxLayout()
            self.rwt_cf_label = QLabel("Change from")
            self.rwt_cf_label.setMaximumHeight(data["font_size"]*2)
            self.rwt_ct_label = QLabel("Change to")
            self.rwt_ct_label.setMaximumHeight(data["font_size"]*2)
            self.rwt_boxes_labels_layout.addWidget(self.rwt_cf_label)
            self.rwt_boxes_labels_layout.addWidget(self.rwt_ct_label)
            self.rwt_cf_label.setAlignment(Qt.AlignHCenter)
            self.rwt_ct_label.setAlignment(Qt.AlignHCenter)
            self.rwt_boxes_labels.setLayout(self.rwt_boxes_labels_layout)
            
            self.rwt_boxes_layout.addWidget(tile_preview_rwt_from)
            self.rwt_boxes_layout.addWidget(tile_preview_rwt_to)
            self.rwt_boxes.setLayout(self.rwt_boxes_layout)
            
            self.rwt_go_button = QPushButton("Replace")
            self.rwt_go_button.clicked.connect(self.rwt_replace)

            self.replace_tile_with_tile_widget_layout.addWidget(self.rwt_label)
            self.replace_tile_with_tile_widget_layout.addWidget(self.rwt_boxes_labels)
            self.replace_tile_with_tile_widget_layout.addWidget(self.rwt_boxes)
            self.replace_tile_with_tile_widget_layout.addWidget(self.rwt_go_button)
            
            #add stacks
            self.fill_with_tiles_widget.setLayout(self.fill_with_tiles_widget_layout)
            self.stacks.append(self.fill_with_tiles_widget)
            self.stacks.append(self.replace_tile_with_tile_widget)
            
            #finalize layout
            global_open_settings = QStackedLayout()
            self.setLayout(global_open_settings)
            
            for x in self.stacks:
                global_open_settings.addWidget(self.stacks[self.stacks.index(x)])
    
    def fwt_fill(self):
        global tile_ratio, global_squares, current_tile, level_data 
        if current_tile != None:
            k = getFillSquares(self.fwt_tl_corner.value(), self.fwt_br_corner.value(), tile_ratio)
            for x in k:
                global_squares[x].setPixmap(current_tile)
                level_data[x] = current_name

    def rwt_replace(self):
        global level_data, previous_sender, global_squares
        for x in range(1, len(level_data)):
            if level_data[x] == previous_sender.ttype_name_s:
                global_squares[x].setPixmap(current_tile)
                level_data[x] = current_name
                


        

