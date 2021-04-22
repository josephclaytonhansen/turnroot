import sys, os, json, pickle
from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QPalette, QIcon, QPixmap
import qtmodern.styles
import qtmodern.windows
from src.UI_preferencesDialog import PreferencesDialog
from src.UI_ProxyStyle import ProxyStyle
from src.UI_Dialogs import (confirmAction,
                        stackedInfoImgDialog,
                        infoClose,
                        addObject,
                        resourcePackDialog,
                        activeResourcePack)
from src.UI_updateJSON import updateJSON
from src.UI_workspaceContainer import (showWorkspace,
                                   hideWorkspace,
                                   tileGridWorkspace,
                                   ClickableQLabel,
                                   toolsWorkspace,
                                   Tiles,
                                   TilesInfo,
                                   LevelData,
                                   TileSets,
                                   TaskSelection,
                                   TaskSettings,
                                   overlayTile,
                                   DeleteMode)
from src.UI_WebViewer import webView

data = updateJSON()
            
import src.UI_colorTheme

active_theme = getattr(src.UI_colorTheme, data["active_theme"])

app = QApplication([])

myStyle = ProxyStyle('Fusion')    
app.setStyle(myStyle)
    
screen = app.primaryScreen()
size = screen.size()
version = "0.0.0d"
title = "Turnroot " +version+ "- Level Editor - "
icon_loc = ""
icon_string = ""

warning_text = "This software was downloaded from an unverified source, and may be compromised. Please download an official release of Turnroot"

fullscreen = False
zoom_level = 1.75
mode_highlight = 0

with open("src/tmp/rsp.tmp", "r") as read_file:
    tmp = read_file.read().strip()

class main(QMainWindow):
    def __init__(self):       
        #create, title, and size mainwindow
        super().__init__()
        self.setWindowTitle(title)
        self.setMinimumSize(QSize(int(size.width()/3), int(size.height()/2)))
        self.setMaximumSize(QSize(int(size.width()), int(size.height())))
        self.resize(QSize(int(size.width()*.98), int(size.height()*.9)))
        
        #set up some variables
        self.fullscreen = fullscreen
        self.zoom_level = zoom_level
        self.path = None
        global icon_string
        self.setFocusPolicy(Qt.ClickFocus)
        
        #pull data from other files
        self.level_data = LevelData().level_data
        self.decor_data = LevelData().decor_data
        self.type_data = LevelData().type_data
        self.object_data = LevelData().object_data
        self.delete_mode = DeleteMode().delete_mode
        self.active_pack = activeResourcePack().pack
        self.tilesets = TileSets().tile_stack

        #set main layout to grid
        self.layout = QGridLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
             
        #color toolbar icons based on theme
        icon_string = ""
        self.icon_loc = icon_loc
        icon_string = "white/"
        self.icon_loc = "ui_icons/logo-white.png"

        
        #add workspaces
        #tiles (in scroll area)        
        self.tiles = Tiles()
        self.tiles_info = TilesInfo()
        self.tscroll = QScrollArea()
        self.tscroll.setMaximumHeight((size.height()/4))
        self.tscroll.setWidget(self.tiles)
        self.tscroll.setWidgetResizable(True)
        self.tscroll.setHorizontalScrollBarPolicy( Qt.ScrollBarAlwaysOn )
        self.tscroll.setVerticalScrollBarPolicy( Qt.ScrollBarAlwaysOn )
        
        #tasks (in scroll area)
        self.tasks = TaskSelection()
        self.tasks_scroll = QScrollArea()
        self.tasks_scroll.setMaximumWidth((size.width()/3))
        self.tasks_scroll.setWidget(self.tasks)
        self.tasks_scroll.setWidgetResizable(True)
        self.tasks_scroll.setVerticalScrollBarPolicy( Qt.ScrollBarAlwaysOn )
        
        #task settings (in scroll area)
        self.task_setting = TaskSettings()
        self.task_settings = QScrollArea()
        self.task_settings.setWidget(self.task_setting)
        self.task_settings.setWidgetResizable(True)
        
        #tile grid (in scroll area)
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
        self.z_in.setPixmap(QPixmap(("src/ui_icons/"+icon_string+"zoom-in.png")).scaled(int(data["icon_size"]), int(data["icon_size"]), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.z_in.setToolTip("Zoom in (I)")
        self.z_out = ClickableQLabel()
        self.z_out.setToolTip("Zoom out (O)")
        self.z_out.setPixmap(QPixmap(("src/ui_icons/"+icon_string+"zoom-out.png")).scaled(int(data["icon_size"]), int(data["icon_size"]), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.goto_00 = ClickableQLabel()
        self.goto_00.setToolTip("Go to top left (L)")
        self.goto_00.setPixmap(QPixmap(("src/ui_icons/"+icon_string+"goto-00.png")).scaled(int(data["icon_size"]), int(data["icon_size"]), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.z_in.clicked.connect(self.zoom_in)
        self.z_out.clicked.connect(self.zoom_out)
        self.goto_00.clicked.connect(self.scrollReset)
        self.goto_fr = ClickableQLabel()
        self.goto_fr.setToolTip("Go to bottom right (.)")
        self.goto_fr.setPixmap(QPixmap(("src/ui_icons/"+icon_string+"goto-fr.png")).scaled(int(data["icon_size"]), int(data["icon_size"]), Qt.KeepAspectRatio,Qt.SmoothTransformation))
        self.goto_fr.clicked.connect(self.scrollFr)
     
        self.tools = toolsWorkspace("tools", data["active_layout"], [self.z_in, self.z_out, self.goto_00, self.goto_fr], "v")

        #add workspaces to main layout
        self.layout.addWidget(self.scroll, 0, 0, 26, 48)
        self.layout.addWidget(self.tscroll, 20, 0, 6, 37)
        self.layout.addWidget(self.tiles_info, 20, 37, 6, 3)
        self.layout.addWidget(self.tasks_scroll, 14, 40, 12, 8)
        self.layout.addWidget(self.task_settings, 4, 40, 10, 8)
        self.layout.addWidget(self.tools, 2, 0, 7, 1)
        
        #add show workspace buttons
        self.tiles_show = showWorkspace("tiles", data["active_layout"])
        self.tasks_show = showWorkspace("tasks", data["active_layout"])
        self.task_settings_show = showWorkspace("task_settings", data["active_layout"])
        self.tools_show = showWorkspace("tools", data["active_layout"])
        
        #add Tiles workspace show/hide toggle to main layout
        self.tiles_show = showWorkspace("tiles", data["active_layout"])
        self.layout.addWidget(self.tiles_show, 25, 0, 1, 1)
        self.tiles_show.clicked.connect(self.show_tiles)
        self.tiles_hide = hideWorkspace("tiles", data["active_layout"])
        self.layout.addWidget(self.tiles_hide, 25, 0, 1, 1)
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
        self.resourcesButton = QAction(QIcon("src/ui_icons/"+icon_string+"package-2-32.png"), "Resources (R)", self)
        self.optionsButton = QAction(QIcon("src/ui_icons/"+icon_string+"settings-17-32.png"),"Options (S)", self)
        self.helpButton = QAction(QIcon("src/ui_icons/"+icon_string+"question-mark-4-32.png"),"Read docs (H)", self)
        self.backButton = QAction(QIcon("src/ui_icons/"+icon_string+"grid-three-up-32.png"),"Return to editor selection (Esc)", self)
        self.justTilesButton = QAction(QIcon("src/ui_icons/"+icon_string+"fit-to-width-32.png"),"Show just tiles (F)", self)
        self.edit_mode = QAction(QIcon("src/ui_icons/"+icon_string+"tile_edit.png"), "Delete tiles", self)
        self.forumButton = QAction(QIcon("src/ui_icons/"+icon_string+"speech-bubble-2-32.png"),"Access forum (Q)", self)
        
        #connect toolbar buttons to actions
        self.optionsButton.triggered.connect(self.OptionsMenu)
        self.helpButton.triggered.connect(self.helpView)
        self.forumButton.triggered.connect(self.forumView)
        self.edit_mode.triggered.connect(self.tileEditMode)
        self.justTilesButton.triggered.connect(self.full_screen)
        self.resourcesButton.triggered.connect(self.resourcesDialog)
        
        #add toolbar buttons to toolbar
        self.toolbar.addAction(self.backButton)
        self.toolbar.addAction(self.optionsButton)
        self.toolbar.addAction(self.resourcesButton)
        self.toolbar.addAction(self.justTilesButton)
        self.toolbar.addAction(self.edit_mode)
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
        self.saveAsButton = QAction("Save As", self)
        self.saveAsButton.triggered.connect(self.saveFileDialog)
        self.SaveButton = QAction("Save", self)
        self.SaveButton.triggered.connect(self.Save)
        self.OpenButton = QAction("Open", self)
        self.OpenButton.triggered.connect(self.openFileDialog)
        
        #file menu items
        fileMenu.addAction(self.OpenButton)
        fileMenu.addAction(self.SaveButton)
        fileMenu.addAction(self.saveAsButton)
        fileMenu.addAction(self.aboutButton)
        fileMenu.addAction(self.checkUpdatesButton)
        fileMenu.addAction(self.quitButton)
        editMenu.addAction(self.optionsButton)

        #put everything together
        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)
        
        #honor autohide
        if(data["ah_tasks"]):
            self.hide_tasks()
        if(data["ah_taskss"]):
            self.hide_tasks_settings()
            
        #keyboard shortcuts
        self.keyboard_shortcuts = {}
        self.pickle_cuts = {}
        with open('src/tmp/kybs.trkp', 'rb') as fh:
            self.pickle_cuts = pickle.load(fh)

        for x in self.pickle_cuts:
            if self.pickle_cuts[x].startswith("self.") and len(self.pickle_cuts[x]) < 32 and "(" not in self.pickle_cuts[x] and ")" not in self.pickle_cuts[x]:
                self.keyboard_shortcuts[x] = eval(self.pickle_cuts[x])
        with open('src/tmp/kybs.trkp', 'wb') as fh:
            pickle.dump(self.pickle_cuts, fh)
    
    #actions- save
    def Save(self):
        if self.path == None:
            self.saveFileDialog()
        else:
            self.setWindowTitle(title+self.path)
            with open(self.path+"f", "w") as write_file:
                json.dump(self.level_data, write_file)
                write_file.close()
            with open(self.path+"d", "w") as write_decor_file:
                json.dump(self.decor_data, write_decor_file)
                write_decor_file.close()
            with open(self.path+"t", "w") as write_type_file:
                json.dump(self.type_data, write_type_file)
                write_type_file.close()
            with open(self.path+"o", "w") as write_object_file:
                json.dump(self.object_data, write_object_file)
                write_object_file.close()
                
    #keyboard events
    def keyPressEvent(self, e):
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.ControlModifier:
            if e.key() == Qt.Key_Q:
                self.quitWindow()
            elif e.key() == Qt.Key_O:
                self.openFileDialog()
            elif e.key() == Qt.Key_S:
                self.Save()                
        else:
            try:
                self.keyboard_shortcuts[e.key()]()
            except:
                pass

    #quick add pop up
    def quickAdd(self):
        t = addObject(parent=self)
        t.exec_()
    #resource pack dialog
    def resourcePack(self):
        r = resourcePackDialog(parent=self)
        r.exec_()
    #options menu dialog
    def OptionsMenu(self):
        p = PreferencesDialog(parent=self)
        theme = p.exec_()
        data = updateJSON()
        
        #apply data from preferences
        if (theme != 0):
            self.menubar.style().unpolish(self.menubar)
            self.menubar.style().polish(self.menubar)
            self.menubar.update()
            self.toolbar.style().unpolish(self.toolbar)
            self.toolbar.style().polish(self.toolbar)
            self.toolbar.update()
            
            active_theme = getattr(src.UI_colorTheme, data["active_theme"])
            self.menubar.setStyleSheet("background-color: "+active_theme.window_background_color+"; color: "+active_theme.window_text_color+"; padding: 2px; font:bold; font-size: "+str(data["font_size"]))
            self.toolbar.setStyleSheet("background-color: "+active_theme.window_background_color+"; color: #ffffff; font-size: "+str(data["font_size"]))
            self.setStyleSheet("font: bold; font-size: "+str(data["font_size"]))
            font = self.menubar.font()
            font.setPointSize(data["font_size"])
            self.toolbar.setIconSize(QSize(int(data["icon_size"]), int(data["icon_size"])))

            if (data["theme_changed"] == True):
                os.execl(sys.executable, sys.executable, *sys.argv)
            
    #help/forums view
    def helpView(self):
        h = webView(page = 3, parent=self)
        h.exec_()
    
    def forumView(self):
        h = webView(page = 4, parent=self)
        h.exec_()
    
    #close (and confirm)
    def closeEvent(self, event):
        c = confirmAction(parent=self, s="quit the level editor")
        c.exec_()
        if(c.return_confirm):
            event.accept()
            sys.exit()
        else:
            event.ignore()
    #quit    
    def quitWindow(self):
        c = confirmAction(parent=self, s="quit the level editor")
        c.exec_()
        if(c.return_confirm):
            sys.exit()
            
    #show and hide workspaces     
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
        self.tasks_scroll.setVisible(True)
        self.task_settings.setVisible(True)
        self.tasks_hide.setVisible(True)
        self.tasks_show.setVisible(False)
        self.tasks_settings_hide.setVisible(True)
        self.tasks_settings_show.setVisible(False)
    
    def hide_tasks(self):
        self.tasks_scroll.setVisible(False)
        self.task_settings.setVisible(False)
        self.tasks_hide.setVisible(False)
        self.tasks_show.setVisible(True)
        self.tasks_settings_hide.setVisible(False)
        self.tasks_settings_show.setVisible(True)
        
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
    
    #full screen toggles ALL hide/show buttons
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
        elif self.fullscreen == False:
            self.show_tiles()
            self.show_tasks()
            self.show_tools()
            self.show_tasks_settings()
    
    #about dialog
    def about(self):
        a = stackedInfoImgDialog(str(self.icon_loc),
                                 ["Turnroot "+version,
                                  "Copyright 2021 - Joseph Hansen",],
                                 ["font-size: 30px; font: bold;", "font-size:15px;"],
                                 parent=self)
        a.exec_()
    
    #check for updates
    def checkUpdates(self):
        u = infoClose("Turnroot is up to date")
        u.exec_()
    
    #resources dialog
    def resourcesDialog(self):
        r = resourcePackDialog(parent=self)
        r.exec_()
    
    #zoom in/out
    def zoom_in(self):
        if self.zoom_level < 3:
            self.zoom_level += .1
        else:
            self.zoom_level = 3
        self.tile_grid.setFixedSize(size.width()*self.zoom_level, int(size.height()/size.width()*size.width())*self.zoom_level)
        self.tile_grid.update()
    
    def zoom_out(self):
        if self.zoom_level >= 1.76:
            self.zoom_level -= .1
        else:
            self.zoom_level = 1.7
        self.tile_grid.setFixedSize(size.width()*self.zoom_level, int(size.height()/size.width()*size.width())*self.zoom_level)
        self.tile_grid.update()
    
    #goto TL/BR corners of tile grid
    def scrollReset(self):
        self.scroll.horizontalScrollBar().setValue(0)
        self.scroll.verticalScrollBar().setValue(0)

    def scrollFr(self):
        self.scroll.horizontalScrollBar().setValue(2200)
        self.scroll.verticalScrollBar().setValue(2200)
    
    #toggle delete mode
    def tileEditMode(self):
        global icon_string
        if self.delete_mode == 0:
            self.edit_mode.setIcon(QIcon("src/ui_icons/"+icon_string+"decor_edit.png"))
            self.delete_mode = 1
            self.edit_mode.setToolTip("src/Delete Objects")
        else:
            self.edit_mode.setIcon(QIcon("ui_icons/"+icon_string+"tile_edit.png"))
            self.delete_mode = 0
            self.edit_mode.setToolTip("Delete tiles")
            
        self.tile_grid.setDeleteMode(self.delete_mode)

    #thanks to pythonspot for the open / save dialog skeletons
    def openFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Open", "","Turnroot Level File (*.trlf)", options=options)
        if fileName:
            self.path = fileName
            self.setWindowTitle(title+self.path)
            
            with open(self.path, "r") as read_file:
                level_data = json.load(read_file)
                read_file.close()
                tile_data = {}
                
            with open(self.path+"d", "r") as read_decor_file:
                decor_data = json.load(read_decor_file)
                read_decor_file.close()
            
            with open(self.path+"t", "r") as read_type_file:
                type_data = json.load(read_type_file)
                read_type_file.close()
            
            with open(self.path+"o", "r") as read_object_file:
                self.type_data = json.load(read_object_file)
                read_object_file.close()
                
                for x in range(0, len(self.tilesets)):
                    with open("src/resource_packs/ClassicVerdant/tiles/"+self.tilesets[x]+".json", "r") as read_file:
                        read_file.seek(0)
                        tile_data[x] = json.load(read_file)
                        
                for g in range(1, self.tile_grid.count+1):
                    self.tile_grid.squares[g].clear()
                    if level_data[str(g)] != 'e':
                        for x in range(0, len(tile_data)):
                            #open tiles
                            for k in range(0, 6):
                                for y in range(0, 27):
                                    tile = tile_data[x][str(k)][str(y)]
                                    if (level_data[str(g)] ) == tile[0]:
                                        self.image = QPixmap("src/resource_packs/ClassicVerdant/tiles/"+self.tilesets[x]+".png")
                                        self.tile_grid.squares[g].setPixmap(self.image.copy(y*32, k*32, 32, 32).scaled(int(64), int(64), Qt.KeepAspectRatio))
                                        self.level_data[g] = level_data[str(g)]
                                            
                    for l in decor_data:
                        self.decor_tile_index = l[:l.index("-")]
                        self.decor_index = l[l.index("-")+1:]
                        if level_data[str(g)] != "e":
                            if str(self.tile_grid.squares[g].gridIndex) == self.decor_tile_index:
                                for x in range(0, len(tile_data)):
                                    for k in range(0, 6):
                                        for y in range(0, 27):
                                            self.decor_tile = tile_data[x][str(k)][str(y)][0]
                                            self.decor_image = image = QPixmap("src/resource_packs/ClassicVerdant/tiles/"+self.tilesets[x]+".png")
                                            if str(self.decor_tile) == self.decor_index:
                                                self.tile_grid.squares[g].setPixmap(
                                                    overlayTile(self.tile_grid.squares[g].pixmap().scaled(int(32), int(32), Qt.KeepAspectRatio),
                                                                self.decor_image.copy(y*32, k*32, 32, 32).scaled(int(32), int(32), Qt.KeepAspectRatio)))
                                           
    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"Save","","Turnroot Level File (*.trlf)", options=options)
        if fileName:
            self.path = fileName+".trl"
            self.setWindowTitle(title+self.path)
            with open(self.path+"f", "w") as write_file:
                json.dump(self.level_data, write_file)
                write_file.close()
            with open(self.path+"d", "w") as write_decor_file:
                json.dump(self.decor_data, write_decor_file)
                write_decor_file.close()
            with open(self.path+"t", "w") as write_type_file:
                json.dump(self.type_data, write_type_file)
                write_type_file.close()
            with open(self.path+"o", "w") as write_object_file:
                json.dump(self.object_data, write_object_file)
                write_object_file.close()
                
window = main()
window.show()
a = app.exec_()
