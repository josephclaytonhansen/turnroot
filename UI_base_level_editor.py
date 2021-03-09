import sys
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QPalette, QIcon
import qtmodern.styles
import qtmodern.windows
import json
from UI_preferencesDialog import PreferencesDialog
from UI_color_test_widget import Color
from UI_ProxyStyle import ProxyStyle

with open("preferences.json", "r") as read_file:
            data = json.load(read_file)
            font_size = data["font_size"]
            icon_size = data["icon_size"]
            rfont_size = data["rfont_size"]
            active_theme = data["active_theme"]
            active_layout = data["active_layout"]
            ah_rte = ["ah_rte"]
            ah_tasks = data["ah_tasks"]
            ah_taskss = data["ah_taskss"]
            ah_overlays = data["ah_overlays"]
            read_file.close()
            
def updateJSON():
    with open("preferences.json", "r") as read_file:
        read_file.seek(0)
        data = json.load(read_file)
        font_size = data["font_size"]
        icon_size = data["icon_size"]
        rfont_size = data["rfont_size"]
        active_theme = data["active_theme"]
        active_layout = data["active_layout"]
        ah_rte = ["ah_rte"]
        ah_tasks = data["ah_tasks"]
        ah_taskss = data["ah_taskss"]
        ah_overlays = data["ah_overlays"]
        read_file.close()
        return data

import UI_colorTheme

active_theme = getattr(UI_colorTheme, active_theme)
print(active_theme)
        

app = QApplication([])

myStyle = ProxyStyle('Fusion')    
app.setStyle(myStyle)
    
screen = app.primaryScreen()
size = screen.size()
title = "Window"

class main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(title)
        self.setMinimumSize(QSize(int(size.width()/3), int(size.height()/3)))
        self.setMaximumSize(QSize(int(size.width()), int(size.height())))
        self.resize(QSize(int(size.width()*.9), int(size.height()*.9)))

        layout = QGridLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        
        self.rte = Color("#f9cb9c")
        self.tiles = Color("#d9ead3")
        self.tasks = Color("#fdf2cc")
        self.task_settings = Color("#ea9999")
        self.tile_grid = Color("#222222")
        self.tools = Color("#d5a6be")

        layout.addWidget(self.tile_grid, 0, 0, 26, 48)
        layout.addWidget(self.rte, 17, 0, 9, 17)
        layout.addWidget(self.tiles, 20, 17, 6, 23)
        layout.addWidget(self.tasks, 14, 40, 12, 8)
        layout.addWidget(self.task_settings, 4, 40, 10, 8)
        layout.addWidget(self.tools, 2, 0, 13, 1)
        
        self.menubar = self.menuBar()
        font = self.menubar.font()
        font.setPointSize(font_size)
        self.menubar.setNativeMenuBar(False)
        fileMenu = self.menubar.addMenu('&File')
        self.bar = self.menuBar()

        self.menubar.setStyleSheet("background-color: "+active_theme.window_background_color+"; color: "+active_theme.window_text_color+"; padding: 2px; font:bold;font-size: "+str(font_size))
        editMenu = self.bar.addMenu("&Edit")
        viewMenu = self.bar.addMenu( "&View")
        
        self.toolbar = QToolBar("")
        self.toolbar.setStyleSheet("background-color: "+active_theme.window_background_color+"; color: #ffffff; font-size: "+str(font_size))
        self.toolbar.setIconSize(QSize(int(icon_size), int(icon_size)))
        self.toolbar.setToolButtonStyle(Qt.ToolButtonIconOnly)
        
        icon_string = ""
        if (active_theme.tag == "midnight_spark"):
            icon_string = "teal/"
        elif (active_theme.tag == "midnight_spark_yellow"):
            icon_string = "yellow/"
        elif (active_theme.tag == "coral_reef"):
            icon_string = "pink/"
        elif (active_theme.tag == "sand_dunes" or active_theme.tag == "chocolate"):
            icon_string = "brown/"
        elif (active_theme.tag == "rainforest"):
            icon_string = "green/"
        elif (active_theme.tag == "charcoal" or active_theme.tag == "ocean_waves"  or active_theme.tag == "garden_morning"):
            icon_string = "white/"
        elif (active_theme.tag == "system_light" or active_theme.tag == "clouds"):
            icon_string = "blue/"
        elif (active_theme.tag == "chili_pepper"):
            icon_string = "red/"
              
        resourcesButton = QAction(QIcon("ui_icons/"+icon_string+"package-2-32.png"), "Resources", self)
        optionsButton = QAction(QIcon("ui_icons/"+icon_string+"settings-17-32.png"),"Options", self)
        helpButton = QAction(QIcon("ui_icons/"+icon_string+"question-mark-4-32.png"),"Read docs", self)
        backButton = QAction(QIcon("ui_icons/"+icon_string+"grid-three-up-32.png"),"Return to editor selection", self)
        playAnimationButton = QAction(QIcon("ui_icons/"+icon_string+"play-2-32.png"),"Play animations", self)
        playSoundButton = QAction(QIcon("ui_icons/"+icon_string+"mute-2-32.png"),"Play sounds", self)
        justTilesButton = QAction(QIcon("ui_icons/"+icon_string+"fit-to-width-32.png"),"Show just tiles", self)
        forumButton = QAction(QIcon("ui_icons/"+icon_string+"speech-bubble-2-32.png"),"Access forum", self)
        
        optionsButton.triggered.connect(self.OptionsMenu)
        
        self.toolbar.addAction(backButton)
        self.toolbar.addAction(optionsButton)
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addAction(resourcesButton)
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addAction(playSoundButton)
        self.toolbar.addAction(playAnimationButton)
        self.toolbar.addAction(justTilesButton)
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addAction(helpButton)
        self.toolbar.addAction(forumButton)
        
        self.addToolBar(self.toolbar)

        widget = QWidget()

        widget.setLayout(layout)

        self.setCentralWidget(widget)
        
    def OptionsMenu(self):
        p = PreferencesDialog()
        p.exec_()
        data = updateJSON()
        self.menubar.style().unpolish(self.menubar)
        self.menubar.style().polish(self.menubar)
        self.menubar.update()
        self.toolbar.style().unpolish(self.toolbar)
        self.toolbar.style().polish(self.toolbar)
        self.toolbar.update()
        active_theme = getattr(UI_colorTheme, data["active_theme"])
        self.menubar.setStyleSheet("background-color: "+active_theme.window_background_color+"; color: "+active_theme.window_text_color+"; padding: 2px; font:bold; font-size: "+str(data["font_size"]))
        self.toolbar.setStyleSheet("background-color: "+active_theme.window_background_color+"; color: #ffffff; font-size: "+str(data["font_size"]))
        font = self.menubar.font()
        font.setPointSize(data["font_size"])
        self.toolbar.setIconSize(QSize(int(data["icon_size"]), int(data["icon_size"])))

              
window = main()

window.show()
sys.exit(app.exec_())
