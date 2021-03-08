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
        
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        fileMenu = menubar.addMenu('&File')
        bar = self.menuBar()

        menubar.setStyleSheet("background-color: "+active_theme.window_background_color+"; color: "+active_theme.window_text_color+"; padding: 2px; font:bold;")
        editMenu = bar.addMenu("&Edit")
        viewMenu = bar.addMenu( "&View")
        
        toolbar = QToolBar("")
        toolbar.setStyleSheet("background-color: "+active_theme.window_background_color+"; color: #ffffff; font-size: 15px;" )
        toolbar.setIconSize(QSize(int(icon_size), int(icon_size)))
        toolbar.setToolButtonStyle(Qt.ToolButtonIconOnly)
              
        resourcesButton = QAction(QIcon("ui_icons/package-2-32.png"), "Resources", self)
        optionsButton = QAction(QIcon("ui_icons/settings-17-32.png"),"Options", self)
        helpButton = QAction(QIcon("ui_icons/question-mark-4-32.png"),"Read docs", self)
        backButton = QAction(QIcon("ui_icons/grid-three-up-32.png"),"Return to editor selection", self)
        playAnimationButton = QAction(QIcon("ui_icons/play-2-32.png"),"Play animations", self)
        playSoundButton = QAction(QIcon("ui_icons/mute-2-32.png"),"Play sounds", self)
        justTilesButton = QAction(QIcon("ui_icons/fit-to-width-32.png"),"Show just tiles", self)
        forumButton = QAction(QIcon("ui_icons/speech-bubble-2-32.png"),"Access forum", self)
        
        optionsButton.triggered.connect(self.OptionsMenu)
        
        toolbar.addAction(backButton)
        toolbar.addAction(optionsButton)
        toolbar.addSeparator()
        toolbar.addSeparator()
        toolbar.addSeparator()
        toolbar.addAction(resourcesButton)
        toolbar.addSeparator()
        toolbar.addSeparator()
        toolbar.addSeparator()
        toolbar.addAction(playSoundButton)
        toolbar.addAction(playAnimationButton)
        toolbar.addAction(justTilesButton)
        toolbar.addSeparator()
        toolbar.addSeparator()
        toolbar.addSeparator()
        toolbar.addAction(helpButton)
        toolbar.addAction(forumButton)
        
        self.addToolBar(toolbar)

        widget = QWidget()

        widget.setLayout(layout)

        self.setCentralWidget(widget)
        
    def OptionsMenu(self):
        p = PreferencesDialog()
        p.exec_()
              
window = main()

window.show()
sys.exit(app.exec_())
