import sys
import os
from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QPalette, QIcon, QPixmap
import qtmodern.styles
import qtmodern.windows
import json
from UI_preferencesDialog import PreferencesDialog
from UI_color_test_widget import Color
from UI_ProxyStyle import ProxyStyle
from UI_Dialogs import confirmAction, stackedInfoImgDialog, infoClose
from UI_updateJSON import updateJSON
from UI_workspaceContainer import workspaceContainer, showWorkspace, hideWorkspace, tileGridWorkspace, ClickableQLabel, toolsWorkspace, Tiles
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
zoom_level = 1.75

class main(QMainWindow):
    def __init__(self):
        
        #create, title, and size mainwindow
        super().__init__()
        self.setWindowTitle(title)
        self.setMinimumSize(QSize(int(size.width()/3), int(size.height()/3)))
        self.setMaximumSize(QSize(int(size.width()), int(size.height())))
        self.resize(QSize(int(size.width()*.9), int(size.height()*.9)))
        self.fullscreen = fullscreen
        self.zoom_level = zoom_level
        self.setFocusPolicy(Qt.ClickFocus)

        #set main layout to grid
        self.layout = QGridLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
             
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
        elif (active_theme.tag == "system_light"):
            icon_string = "blue/"
        elif (active_theme.tag == "chili_pepper"):
            icon_string = "red/"
            self.icon_loc = "ui_icons/logo-white.png"
        
        #add workspaces
        self.rte = workspaceContainer("rte", data["active_layout"])
        
        self.tiles = Tiles()
        self.tiles_info = workspaceContainer("tasks", data["active_layout"])
        self.tscroll = QScrollArea()
        self.tscroll.setMaximumHeight(212)
        self.tscroll.setWidget(self.tiles)
        self.tscroll.setWidgetResizable(True)
        self.tscroll.setHorizontalScrollBarPolicy( Qt.ScrollBarAlwaysOn )
        self.tscroll.setVerticalScrollBarPolicy( Qt.ScrollBarAlwaysOn )
        
        self.tasks = workspaceContainer("tasks", data["active_layout"])
        self.task_settings = workspaceContainer("task_settings", data["active_layout"])
        
        self.tile_grid = tileGridWorkspace()
        self.tile_grid.setMinimumWidth(size.width())
        self.tile_grid.setMaximumHeight(size.height()) 
        self.scroll = QScrollArea()
        self.scroll.setWidget(self.tile_grid)
        self.tile_grid.setFixedSize(int(size.width())*self.zoom_level, int(size.height()/size.width()*size.width())*self.zoom_level)
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy( Qt.ScrollBarAlwaysOff )
        self.scroll.setVerticalScrollBarPolicy( Qt.ScrollBarAlwaysOff )
        
        self.setStyleSheet("font: bold; font-size: "+str(data["font_size"]))
        
        #tools workspace
        self.z_in = ClickableQLabel()
        self.z_in.setPixmap(QPixmap(("ui_icons/"+icon_string+"zoom_in.png")).scaled(int(data["icon_size"]), int(data["icon_size"]), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.z_in.setToolTip("Zoom in (I)")
        self.z_out = ClickableQLabel()
        self.z_out.setToolTip("Zoom out (O)")
        self.z_out.setPixmap(QPixmap(("ui_icons/"+icon_string+"zoom_out.png")).scaled(int(data["icon_size"]), int(data["icon_size"]), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.goto_00 = ClickableQLabel()
        self.goto_00.setToolTip("Go to top left (L)")
        self.goto_00.setPixmap(QPixmap(("ui_icons/"+icon_string+"goto_00.png")).scaled(int(data["icon_size"]), int(data["icon_size"]), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.z_in.clicked.connect(self.zoom_in)
        self.z_out.clicked.connect(self.zoom_out)
        self.goto_00.clicked.connect(self.scrollReset)
        self.goto_fr = ClickableQLabel()
        self.goto_fr.setToolTip("Go to bottom right (.)")
        self.goto_fr.setPixmap(QPixmap(("ui_icons/"+icon_string+"goto_fr.png")).scaled(int(data["icon_size"]), int(data["icon_size"]), Qt.KeepAspectRatio,Qt.SmoothTransformation))
        self.goto_fr.clicked.connect(self.scrollFr)

        
        self.remove_above = ClickableQLabel()
        self.remove_above.setToolTip("Remove above (Right Click)")
        self.remove_above.setPixmap(QPixmap(("ui_icons/"+icon_string+"remove_above.png")).scaled(int(data["icon_size"]), int(data["icon_size"]), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.remove_above.clicked.connect(self.removeAbove)

        
        self.remove_below = ClickableQLabel()
        self.remove_below.setToolTip("Remove below (Shift+Right Click)")
        self.remove_below.setPixmap(QPixmap(("ui_icons/"+icon_string+"remove_below.png")).scaled(int(data["icon_size"]), int(data["icon_size"]), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.remove_below.clicked.connect(self.removeBelow)
        
        self.remove_effect = ClickableQLabel()
        self.remove_effect.setToolTip("Remove tile effects (Alt+Right Click)")
        self.remove_effect.setPixmap(QPixmap(("ui_icons/"+icon_string+"remove_effect.png")).scaled(int(data["icon_size"]), int(data["icon_size"]), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.remove_effect.clicked.connect(self.removeEffect)
        
        self.random_decoration_add = ClickableQLabel()
        self.random_decoration_add.setToolTip("Add random decoration (Shift+Left Click)")
        self.random_decoration_add.setPixmap(QPixmap(("ui_icons/"+icon_string+"random_decoration_add.png")).scaled(int(data["icon_size"]), int(data["icon_size"]), Qt.KeepAspectRatio))
        self.random_decoration_add.clicked.connect(self.randomDecorationAdd)
        
        self.tools = toolsWorkspace("tools", data["active_layout"], [self.z_in, self.z_out, self.goto_00, self.goto_fr, self.remove_above, self.remove_below, self.remove_effect, self.random_decoration_add])

        #add workspaces to main layout
        self.layout.addWidget(self.scroll, 0, 0, 26, 48)
        self.layout.addWidget(self.rte, 17, 0, 9, 14)
        self.layout.addWidget(self.tscroll, 20, 14, 6, 23)
        self.layout.addWidget(self.tiles_info, 20, 37, 6, 3)
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
        self.layout.addWidget(self.tiles_show, 25, 15, 1, 1)
        self.tiles_show.clicked.connect(self.show_tiles)
        self.tiles_hide = hideWorkspace("tiles", data["active_layout"])
        self.layout.addWidget(self.tiles_hide, 25, 15, 1, 1)
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

        #add actions for toolbar
        self.resourcesButton = QAction(QIcon("ui_icons/"+icon_string+"package-2-32.png"), "Resources (R)", self)
        self.optionsButton = QAction(QIcon("ui_icons/"+icon_string+"settings-17-32.png"),"Options (S)", self)
        self.helpButton = QAction(QIcon("ui_icons/"+icon_string+"question-mark-4-32.png"),"Read docs (H)", self)
        self.backButton = QAction(QIcon("ui_icons/"+icon_string+"grid-three-up-32.png"),"Return to editor selection (Esc)", self)
        self.playAnimationButton = QAction(QIcon("ui_icons/"+icon_string+"play-2-32.png"),"Play animations (Spacebar)", self)
        self.playSoundButton = QAction(QIcon("ui_icons/"+icon_string+"mute-2-32.png"),"Play sounds (Shift+Spacebar)", self)
        self.justTilesButton = QAction(QIcon("ui_icons/"+icon_string+"fit-to-width-32.png"),"Show just tiles (F)", self)
        self.forumButton = QAction(QIcon("ui_icons/"+icon_string+"speech-bubble-2-32.png"),"Access forum (Q)", self)
        
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
        self.checkUpdatesButton = QAction("Check for updates", self)
        self.checkUpdatesButton.triggered.connect(self.checkUpdates)
        fileMenu.addAction(self.aboutButton)
        fileMenu.addAction(self.checkUpdatesButton)
        fileMenu.addAction(self.quitButton)
        editMenu.addAction(self.optionsButton)

        #put everything together
        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)
        
        #honor autohide
        if(data["ah_rte"]):
            self.hideRTE()
        if(data["ah_tasks"]):
            self.hide_tasks()
        if(data["ah_taskss"]):
            self.hide_tasks_settings()
    
    #keyboard events
    def keyPressEvent(self, e):
        modifiers = QApplication.keyboardModifiers()
        if e.key() == Qt.Key_F:
            self.full_screen()
        elif e.key() == Qt.Key_S:
            self.OptionsMenu()
        elif e.key() == Qt.Key_H:
            self.helpView()
        elif e.key() == Qt.Key_I:
            self.zoom_in()
        elif e.key() == Qt.Key_O:
            self.zoom_out()
        elif e.key() == Qt.Key_L:
            self.scrollReset()
        elif e.key() == Qt.Key_Period:
            self.scrollFr()

        if modifiers == Qt.ControlModifier:
            if e.key() == Qt.Key_Q:
                self.quitWindow()

    #custom events
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
        self.tscroll.setVisible(True)
        self.tiles_info.setVisible(True)
        self.tiles_hide.setVisible(True)
        self.tiles_show.setVisible(False)
    
    def hide_tiles(self):
        self.tscroll.setVisible(False)
        self.tiles_info.setVisible(False)
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
    
    def checkUpdates(self):
        #check updates
        u = infoClose("Turnroot is up to date")
        u.exec_()
    
    def zoom_in(self):
        if self.zoom_level < 3.25:
            self.zoom_level += .25
        else:
            self.zoom_level = 3.25
        self.tile_grid.setFixedSize(size.width()*self.zoom_level, int(size.height()/size.width()*size.width())*self.zoom_level)
        self.tile_grid.update()
    
    def zoom_out(self):
        if self.zoom_level >= 1.76:
            self.zoom_level -= .25
        else:
            self.zoom_level = 1.75
        self.tile_grid.setFixedSize(size.width()*self.zoom_level, int(size.height()/size.width()*size.width())*self.zoom_level)
        self.tile_grid.update()
    
    def scrollReset(self):
        self.scroll.horizontalScrollBar().setValue(0)
        self.scroll.verticalScrollBar().setValue(0)

    def scrollFr(self):
        self.scroll.horizontalScrollBar().setValue(2200)
        self.scroll.verticalScrollBar().setValue(2200)
    
    def removeAbove(self):
        pass
       
    def removeBelow(self):
        pass
    
    def randomDecorationAdd(self):
        pass
    
    def removeEffect(self):
        pass
            
window = main()
window.show()
a = app.exec_()