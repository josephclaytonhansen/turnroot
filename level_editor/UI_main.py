import sys
import os
from PyQt5.QtCore import QSize, Qt 
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QPalette, QIcon
import qtmodern.styles
import qtmodern.windows
import json
from UI_preferencesDialog import PreferencesDialog
from UI_color_test_widget import Color
from UI_ProxyStyle import ProxyStyle
from UI_Dialogs import confirmAction, stackedInfoImgDialog
from UI_updateJSON import updateJSON
from UI_workspaceContainer import workspaceContainer, showWorkspace, hideWorkspace
from UI_WebViewer import webView

data = updateJSON()
            
import UI_colorTheme

active_theme = getattr(UI_colorTheme, data["active_theme"])

app = QApplication([])

myStyle = ProxyStyle('Fusion')    
app.setStyle(myStyle)
    
screen = app.primaryScreen()
size = screen.size()
version = "0.0.0d"
title = "Turnroot" +version+ "- Level Editor"
icon_loc = ""

warning_text = "This software was downloaded from an unverified source, and may be compromised. Please download an official release of Turnroot"

fullscreen = False

class main(QMainWindow):
    def __init__(self):
        
        #create, title, and size mainwindow
        super().__init__()
        self.setWindowTitle(title)
        self.setMinimumSize(QSize(int(size.width()/3), int(size.height()/3)))
        self.setMaximumSize(QSize(int(size.width()), int(size.height())))
        self.resize(QSize(int(size.width()*.9), int(size.height()*.9)))
        self.fullscreen = fullscreen

        #set main layout to grid
        self.layout = QGridLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        
        #add workspaces
        self.rte = workspaceContainer("rte", data["active_layout"])
        self.tiles = workspaceContainer("tiles", data["active_layout"])
        self.tasks = workspaceContainer("tasks", data["active_layout"])
        self.task_settings = workspaceContainer("task_settings", data["active_layout"])
        self.tile_grid = Color("black")
        self.tools = workspaceContainer("tools", data["active_layout"])
        self.setStyleSheet("font: bold; font-size: "+str(data["font_size"]))

        #add workspaces to main layout
        self.layout.addWidget(self.tile_grid, 0, 0, 26, 48)
        self.layout.addWidget(self.rte, 17, 0, 9, 17)
        self.layout.addWidget(self.tiles, 20, 17, 6, 23)
        self.layout.addWidget(self.tasks, 14, 40, 12, 8)
        self.layout.addWidget(self.task_settings, 4, 40, 10, 8)
        self.layout.addWidget(self.tools, 2, 0, 13, 1)
        
        #add show workspace buttons
        self.tiles_show = showWorkspace("tiles", data["active_layout"])
        self.tasks_show = showWorkspace("tasks", data["active_layout"])
        self.task_settings_show = showWorkspace("task_settings", data["active_layout"])
        self.tools_show = showWorkspace("tools", data["active_layout"])
        self.rte_show = showWorkspace("rte", data["active_layout"])
        
        #add RTE workspace show/hide toggle to main layout
        self.layout.addWidget(self.rte_show, 25, 0, 1, 1)
        self.rte_show.clicked.connect(self.showRTE)
        self.rte_hide = hideWorkspace("rte", data["active_layout"])
        self.layout.addWidget(self.rte_hide, 25, 0, 1, 1)
        self.rte_hide.clicked.connect(self.hideRTE)
        self.rte_show.setVisible(False)
        
        #add Tiles workspace show/hide toggle to main layout
        self.tiles_show = showWorkspace("tiles", data["active_layout"])
        self.layout.addWidget(self.tiles_show, 25, 17, 1, 1)
        self.tiles_show.clicked.connect(self.show_tiles)
        self.tiles_hide = hideWorkspace("tiles", data["active_layout"])
        self.layout.addWidget(self.tiles_hide, 25, 17, 1, 1)
        self.tiles_hide.clicked.connect(self.hide_tiles)
        self.tiles_show.setVisible(False)

        #add Tasks workspace show/hide toggle to main layout
        self.tasks_show = showWorkspace("tasks", data["active_layout"])
        self.layout.addWidget(self.tasks_show, 14, 47, 1, 1)
        self.tasks_show.clicked.connect(self.show_tasks)
        self.tasks_hide = hideWorkspace("tasks", data["active_layout"])
        self.layout.addWidget(self.tasks_hide, 14, 47, 1, 1)
        self.tasks_hide.clicked.connect(self.hide_tasks)
        self.tasks_show.setVisible(False)

        #add Task Settings workspace show/hide toggle to main layout
        self.tasks_settings_show = showWorkspace("tasks_settings", data["active_layout"])
        self.layout.addWidget(self.tasks_settings_show, 4, 47, 1, 1)
        self.tasks_settings_show.clicked.connect(self.show_tasks_settings)
        self.tasks_settings_hide = hideWorkspace("tasks_settings", data["active_layout"])
        self.layout.addWidget(self.tasks_settings_hide, 4, 47, 1, 1)
        self.tasks_settings_hide.clicked.connect(self.hide_tasks_settings)
        self.tasks_settings_show.setVisible(False)

        #add Tools workspace show/hide toggle to main layout
        self.tools_show = showWorkspace("tools", data["active_layout"])
        self.layout.addWidget(self.tools_show, 2, 0, 1, 1)
        self.tools_show.clicked.connect(self.show_tools)
        self.tools_hide = hideWorkspace("tools", data["active_layout"])
        self.layout.addWidget(self.tools_hide, 2, 0, 1, 1)
        self.tools_hide.clicked.connect(self.hide_tools)
        self.tools_show.setVisible(False)

        #add Menu, File
        self.menubar = self.menuBar()
        font = self.menubar.font()
        font.setPointSize(data["font_size"])
        self.menubar.setNativeMenuBar(False)
        fileMenu = self.menubar.addMenu('&File')
        self.bar = self.menuBar()
        
        #add Edit and View to menu
        self.menubar.setStyleSheet("background-color: "+active_theme.window_background_color+"; color: "+active_theme.window_text_color+"; padding: 2px; font:bold;font-size: "+str(data["font_size"]))
        editMenu = self.bar.addMenu("&Edit")
        viewMenu = self.bar.addMenu( "&View")

        #add toolbar
        self.toolbar = QToolBar("")
        self.toolbar.setStyleSheet("background-color: "+active_theme.window_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
        self.toolbar.setIconSize(QSize(int(data["icon_size"]), int(data["icon_size"])))
        self.toolbar.setToolButtonStyle(Qt.ToolButtonIconOnly)
        
        #color toolbar icons based on theme
        icon_string = ""
        self.icon_loc = icon_loc
        self.icon_loc = "ui_icons/logo-color.png"
        if (active_theme.tag == "midnight_spark"):
            icon_string = "teal/"
        elif (active_theme.tag == "midnight_spark_yellow"):
            icon_string = "yellow/"
        elif (active_theme.tag == "sand_dunes" or active_theme.tag == "chocolate"):
            icon_string = "brown/"
            self.icon_loc = "ui_icons/logo-white.png"
        elif (active_theme.tag == "rainforest"):
            icon_string = "green/"
        elif (active_theme.tag == "charcoal" or active_theme.tag == "ocean_waves"  or active_theme.tag == "garden_morning" or  active_theme.tag == "coral_reef"):
            icon_string = "white/"
            self.icon_loc = "ui_icons/logo-white.png"
        elif (active_theme.tag == "system_light" or active_theme.tag == "clouds"):
            icon_string = "blue/"
        elif (active_theme.tag == "chili_pepper"):
            icon_string = "red/"
            self.icon_loc = "ui_icons/logo-white.png"

        #add actions for toolbar
        self.resourcesButton = QAction(QIcon("ui_icons/"+icon_string+"package-2-32.png"), "Resources", self)
        self.optionsButton = QAction(QIcon("ui_icons/"+icon_string+"settings-17-32.png"),"Options", self)
        self.helpButton = QAction(QIcon("ui_icons/"+icon_string+"question-mark-4-32.png"),"Read docs", self)
        self.backButton = QAction(QIcon("ui_icons/"+icon_string+"grid-three-up-32.png"),"Return to editor selection", self)
        self.playAnimationButton = QAction(QIcon("ui_icons/"+icon_string+"play-2-32.png"),"Play animations", self)
        self.playSoundButton = QAction(QIcon("ui_icons/"+icon_string+"mute-2-32.png"),"Play sounds", self)
        self.justTilesButton = QAction(QIcon("ui_icons/"+icon_string+"fit-to-width-32.png"),"Show just tiles", self)
        self.forumButton = QAction(QIcon("ui_icons/"+icon_string+"speech-bubble-2-32.png"),"Access forum", self)
        
        #connect toolbar buttons to actions
        self.optionsButton.triggered.connect(self.OptionsMenu)
        self.helpButton.triggered.connect(self.helpView)
        self.justTilesButton.triggered.connect(self.full_screen)
        
        #add toolbar buttons to toolbar
        self.toolbar.addAction(self.backButton)
        self.toolbar.addAction(self.optionsButton)
        self.toolbar.addAction(self.resourcesButton)
        self.toolbar.addAction(self.playSoundButton)
        self.toolbar.addAction(self.playAnimationButton)
        self.toolbar.addAction(self.justTilesButton)
        self.toolbar.addAction(self.helpButton)
        self.toolbar.addAction(self.forumButton)
        
        self.addToolBar(self.toolbar)
        
        #add menu actions
        self.quitButton = QAction("Quit", self)
        self.quitButton.triggered.connect(self.quitWindow)
        self.aboutButton = QAction("About", self)
        self.aboutButton.triggered.connect(self.about)
        fileMenu.addAction(self.aboutButton)
        fileMenu.addAction(self.quitButton)
        editMenu.addAction(self.optionsButton)

        #put everything together
        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)
        
    def OptionsMenu(self):
        p = PreferencesDialog(parent=self)
        theme = p.exec_()
        data = updateJSON()
        if (theme != 0):
            self.menubar.style().unpolish(self.menubar)
            self.menubar.style().polish(self.menubar)
            self.menubar.update()
            self.toolbar.style().unpolish(self.toolbar)
            self.toolbar.style().polish(self.toolbar)
            self.toolbar.update()
            active_theme = getattr(UI_colorTheme, data["active_theme"])
            self.menubar.setStyleSheet("background-color: "+active_theme.window_background_color+"; color: "+active_theme.window_text_color+"; padding: 2px; font:bold; font-size: "+str(data["font_size"]))
            self.toolbar.setStyleSheet("background-color: "+active_theme.window_background_color+"; color: #ffffff; font-size: "+str(data["font_size"]))
            self.setStyleSheet("font: bold; font-size: "+str(data["font_size"]))
            font = self.menubar.font()
            font.setPointSize(data["font_size"])
            self.toolbar.setIconSize(QSize(int(data["icon_size"]), int(data["icon_size"])))
            if (data["theme_changed"] == True):
                os.execl(sys.executable, sys.executable, *sys.argv)
        
    def helpView(self):
        h = webView(parent=self)
        h.exec_()
    
    def closeEvent(self, event):
        c = confirmAction(parent=self, s="quit the level editor")
        c.exec_()
        print(c.return_confirm)
        if(c.return_confirm):
            event.accept()
            sys.exit()
        else:
            event.ignore()
        
    def quitWindow(self):
        c = confirmAction(parent=self, s="quit the level editor")
        c.exec_()
        if(c.return_confirm):
            sys.exit()
    
    def showRTE(self):
        self.rte.setVisible(True)
        self.rte_hide.setVisible(True)
        self.rte_show.setVisible(False)
    
    def hideRTE(self):
        self.rte.setVisible(False)
        self.rte_hide.setVisible(False)
        self.rte_show.setVisible(True)
        
    def show_tiles(self):
        self.tiles.setVisible(True)
        self.tiles_hide.setVisible(True)
        self.tiles_show.setVisible(False)
    
    def hide_tiles(self):
        self.tiles.setVisible(False)
        self.tiles_hide.setVisible(False)
        self.tiles_show.setVisible(True)
        
    def show_tasks(self):
        self.tasks.setVisible(True)
        self.tasks_hide.setVisible(True)
        self.tasks_show.setVisible(False)
    
    def hide_tasks(self):
        self.tasks.setVisible(False)
        self.tasks_hide.setVisible(False)
        self.tasks_show.setVisible(True)
        
    def show_tasks_settings(self):
        self.task_settings.setVisible(True)
        self.tasks_settings_hide.setVisible(True)
        self.tasks_settings_show.setVisible(False)
    
    def hide_tasks_settings(self):
        self.task_settings.setVisible(False)
        self.tasks_settings_hide.setVisible(False)
        self.tasks_settings_show.setVisible(True)
    
    def show_tools(self):
        self.tools.setVisible(True)
        self.tools_hide.setVisible(True)
        self.tools_show.setVisible(False)
    
    def hide_tools(self):
        self.tools.setVisible(False)
        self.tools_hide.setVisible(False)
        self.tools_show.setVisible(True)
    
    def full_screen(self):
        if self.fullscreen == True:
            self.fullscreen = False
        elif self.fullscreen == False:
            self.fullscreen = True
        if self.fullscreen == True:
            self.hide_tiles()
            self.hide_tasks()
            self.hide_tools()
            self.hide_tasks_settings()
            self.hideRTE()
        elif self.fullscreen == False:
            self.show_tiles()
            self.show_tasks()
            self.show_tools()
            self.show_tasks_settings()
            self.showRTE()
            
    def about(self):
        a = stackedInfoImgDialog(str(self.icon_loc),
                                 ["Turnroot "+version,
                                  "Copyright 2021 - Joseph Hansen",],
                                 ["font-size: 30px; font: bold;", "font-size:15px;"],
                                 parent=self)
        a.exec_()

window = main()
window.show()
a = app.exec_()