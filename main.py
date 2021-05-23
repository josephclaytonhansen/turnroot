import sys, json, os
import src.UI_colorTheme as UI_colorTheme
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from src.UI_updateJSON import updateJSON
from src.UI_Dialogs import confirmAction, infoClose, switchEditorDialog, REPLACE_WINDOW, NEW_WINDOW
from src. UI_unitPreferencesDialog import unitOptionsDialog
from src.UI_ProxyStyle import ProxyStyle
from src.UI_unit_editor_wnd import UnitEditorWnd
from src.UI_node_editor_wnd import NodeEditorWnd
from src.UI_node_preferences_dialog import NodePreferencesDialog
from src.node_presets import NODES, Nodes
from src.UI_WebViewer import webView
import qtmodern.styles
import qtmodern.windows, json

data = updateJSON()
active_theme = getattr(UI_colorTheme, data["active_theme"])

app = QApplication([])

myStyle = ProxyStyle('Fusion')    
app.setStyle(myStyle)

screen = app.primaryScreen()
size = screen.size()

title = "Turnroot Unit Editor" 

if os.sep == "\\":
    font_string = "Lucida Sans Unicode"
else:
    font_string = "Lucida Grande"
    
with open("src/tmp/aic.json", "r") as cons:
    const = json.load(cons)
    
OPEN_LAST_FILE = const[0]
OPEN_NEW_FILE = const[1]

class mainS(NodeEditorWnd):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setMaximumSize(QSize(int(size.width()), int(size.height())))
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.context_menu)
        
    def context_menu(self, pos):
        context = QMenu(self)
        self.tmp_pos = QCursor.pos()
        items_keys = self.scene.node_keys
        items = self.scene.node_presets
        context.setStyleSheet("background-color: "+active_theme.node_background_color+"; color: "+active_theme.node_text_color+"; padding: 2px;font-size: "+str(data["font_size"]))
        flow = QMenu("Events/Flow")
        con = QMenu("Conditions")
        econ = QMenu("Environment Conditions")
        nop = QMenu("Numbers/Operations")
        ub = QMenu("Unit Effects")
        ab = QMenu("Ally Effects")
        fp = QMenu("Foe Effects")
        ui = QMenu("Combat Bonus")
        se = QMenu("Special Effects")
        
        submenus = [flow,con,nop,ub,ab,fp,se]
        for y in submenus:
            y.setStyleSheet("background-color: "+active_theme.node_background_color+"; color: "+active_theme.node_text_color+"; padding: 2px;font-size: "+str(data["font_size"]))
        
        nop_actions = [QAction("Math", self),QAction("Compare Numbers", self),QAction("Convert T/F to Event", self), QAction("And", self),
                       QAction("A or B", self), QAction("Not (If A is False, True)",self)]
        for n in nop_actions:
            nop.addAction(n)
            n.triggered.connect(self.submenu_item)
            
        flow_actions = [QAction("Combat Start", self),QAction("Unit Initiates Combat", self),QAction("Foe Initiates Combat", self),
                        ]
        
        for n in flow_actions:
            flow.addAction(n)
            n.triggered.connect(self.submenu_item)
        
        econ_actions = [QAction("Level is Night", self), QAction("Level is Raining", self), QAction("Level is Foggy", self)]
        econ.setStyleSheet("background-color: "+active_theme.node_background_color+"; color: "+active_theme.node_text_color+"; padding: 2px;font-size: "+str(data["font_size"]))
        
        for n in econ_actions:
            econ.addAction(n)
            n.triggered.connect(self.submenu_item)
        
        con.addMenu(econ)
        
        con_actions = [QAction("Unit is Adjacent to Ally", self), QAction("Unit is Within N of Ally", self),
                        QAction("Unit Using Weapon Type", self), QAction("Foe Using Weapon Type", self), QAction("Unit Health Percentage", self),
                        QAction("Foe Health Percentage", self), QAction("Unit is Mounted", self), QAction("Foe is Mounted", self),
                        QAction("Foe has Bonus", self), QAction("Foe has Penalty", self), QAction("Unit has Bonus", self),
                        QAction("Unit has Penalty", self), QAction("Ally is Mounted", self), QAction("Ally is Female", self),
                        QAction("Ally is Male", self)]
        
        for n in con_actions:
            con.addAction(n)
            n.triggered.connect(self.submenu_item)
            
        ub_actions = [QAction("Unit +Bonus Strength/Magic", self),QAction("Unit +Bonus Defense", self),QAction("Unit +Bonus Resistance", self),
                        QAction("Unit +Bonus Charisma", self), QAction("Unit +Bonus Dexterity", self),QAction("Unit +Bonus Luck", self),
                      QAction("Earn Extra Weapon EXP", self), QAction("Earn Extra Level EXP", self), QAction("Unit +Bonus Critical",self)]
        ub.addMenu(ui)
        for n in ub_actions:
            ub.addAction(n)
            n.triggered.connect(self.submenu_item)
        
        ab_actions = [QAction("Ally +Bonus Strength/Magic", self),QAction("Ally +Bonus Defense", self),QAction("Ally +Bonus Resistance", self),
                        QAction("Ally +Bonus Charisma", self), QAction("Ally +Bonus Dexterity", self),QAction("Ally +Bonus Luck", self)]
        
        for n in ab_actions:
            ab.addAction(n)
            n.triggered.connect(self.submenu_item)
            
        ui_actions = [QAction("Unit +Hit Chance", self),QAction("Unit +Dodge Chance", self),QAction("Unit +Critical Chance", self),
                      QAction("Unit does Less/More Damage", self)]
        ui.setStyleSheet("background-color: "+active_theme.node_background_color+"; color: "+active_theme.node_text_color+"; padding: 2px;font-size: "+str(data["font_size"]))
        for n in ui_actions:
            ui.addAction(n)
            n.triggered.connect(self.submenu_item)
        
    
        for y in submenus:
            y.setStyleSheet("background-color: "+active_theme.node_background_color+"; color: "+active_theme.node_text_color+"; padding: 2px;font-size: "+str(data["font_size"]))
            context.addMenu(y)
            
        context.exec_(self.mapToGlobal(pos))
    
    def submenu_item(self):
        s = self.sender().text()
        self.chosen_node = NODES[s]
        g = Nodes(self.scene, s).node
        self.scene.added_nodes.append(g)
        i = self.view.mapFromGlobal(self.tmp_pos)
        h = self.view.mapToScene(i.x(), i.y())
        g.setPos(h.x(), h.y())

class mainN(UnitEditorWnd):
    def __init__(self, parent):
        super().__init__(parent)
        self.resize(QSize(1500,850))
        self.setMaximumSize(QSize(int(size.width()*2), int(size.height()*2)))

class main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(title)
        self.toolbar = QToolBar("")
        
        self.toolbar.setStyleSheet("background-color: "+active_theme.window_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
        self.toolbar.setIconSize(QSize(int(data["icon_size"]), int(data["icon_size"])))
        self.toolbar.setToolButtonStyle(Qt.ToolButtonIconOnly)
        
        self.optionsButton = QAction(QIcon("src/ui_icons/white/settings-17-32.png"),"Options (S)", self)
        self.helpButton = QAction(QIcon("src/ui_icons/white/question-mark-4-32.png"),"Read docs (H)", self)
        self.backButton = QAction(QIcon("src/ui_icons/white/grid-three-up-32.png"),"Return to editor selection (Esc)", self)
        
        self.toolbar.addAction(self.backButton)
        self.toolbar.addAction(self.optionsButton)
        self.toolbar.addAction(self.helpButton)
        
        self.optionsButton.triggered.connect(self.OptionsMenu)
        self.backButton.triggered.connect(self.editorSelect)
        self.helpButton.triggered.connect((self.helpView))
        
        self.addToolBar(self.toolbar)
        
        self.menubar = self.menuBar()
        font = self.menubar.font()
        font.setPointSize(data["font_size"])
        self.menubar.setNativeMenuBar(False)
        self.bar = self.menuBar()
        
        self.m = QStackedWidget(parent=self)
        self.unit_editor = mainN(parent=self)
        self.m.addWidget(self.unit_editor)
        self.skills_editor = mainS(parent=self)
        self.m.addWidget(self.skills_editor)
        self.m.setCurrentWidget(self.unit_editor)
        
        self.setGeometry(
    QStyle.alignedRect(
        Qt.LeftToRight,
        Qt.AlignCenter,
        self.unit_editor.size(),
        app.desktop().availableGeometry()
        ))
        
        self.newButton = QAction("&New", self)
        self.newButton.setVisible(False)
        self.menubar.addAction(self.newButton)
        
        self.openButton = QAction("&Open", self)
        self.openButton.triggered.connect(self.unit_editor.loadFromFile)
        self.openButton.triggered.connect(self.nameChange)
        self.menubar.addAction(self.openButton)
        
        self.saveButton = QAction("&Save", self)
        self.saveButton.triggered.connect(self.unit_editor.unitToJSON)
        self.saveButton.triggered.connect(self.nameChange)
        self.menubar.addAction(self.saveButton)
        
        self.deleteButton = QAction("Delete Selection", self)
        self.deleteButton.triggered.connect(self.skills_editor.view.deleteSelected)
        self.menubar.addAction(self.deleteButton)
        self.deleteButton.setVisible(False)
        
        self.quitButton = QAction("&Quit", self)
        self.quitButton.triggered.connect(self.quitWindow)
        self.menubar.addAction(self.quitButton)
        
        self.setCentralWidget(self.m)
        
    def nameChange(self):
        pass
    
    def editorSelect(self):
        e = switchEditorDialog(parent=self,font=self.unit_editor.body_font)
        e.exec_()
        new_editor = e.editor
        if e.mode == REPLACE_WINDOW:
            pass
        elif e.mode == NEW_WINDOW:
            if new_editor == 0:
                from main_level_editor import main
            elif new_editor == 1:
                self.m.setCurrentWidget(self.skills_editor)
                self.openButton.triggered.disconnect()
                self.saveButton.triggered.disconnect() 
                self.openButton.triggered.connect(self.skills_editor.scene.loadFromFile)
                self.saveButton.triggered.connect(self.skills_editor.scene.saveToFile)
                self.resize(QSize(1200,700))
                self.newButton.setVisible(True)
                self.deleteButton.setVisible(True)
                self.newButton.triggered.connect(self.skills_editor.scene.new)
                self.setGeometry(
    QStyle.alignedRect(
        Qt.LeftToRight,
        Qt.AlignCenter,
        self.size(),
        app.desktop().availableGeometry()
        ))
                self.setWindowTitle("Turnroot Skills Editor")
            elif new_editor == 2:
                from main_world_editor import main
            elif new_editor == 3:
                from main_hub_editor import main
            elif new_editor == 4:
                self.m.setCurrentWidget(self.unit_editor)
                self.openButton.triggered.disconnect()
                self.saveButton.triggered.disconnect() 
                self.openButton.triggered.connect(self.unit_editor.loadFromFile)
                self.saveButton.triggered.connect(self.unit_editor.unitToJSON)
                self.resize(QSize(1500,850))
                self.newButton.setVisible(False)
                self.deleteButton.setVisible(False)
                self.setGeometry(
    QStyle.alignedRect(
        Qt.LeftToRight,
        Qt.AlignCenter,
        self.size(),
        app.desktop().availableGeometry()
        ))
                self.setWindowTitle("Turnroot Unit/Class Editor")
            elif new_editor == 5:
                from main_object_editor import main
            elif new_editor == 6:
                from main_portrait_editor import main
            elif new_editor == 7:
                from main_menu_editor import main
            elif new_editor == 8:
                from main_stores_editor import main
            elif new_editor == 9:
                from main_game_editor import main
                
            
    def OptionsMenu(self):
        if isinstance(self.m.currentWidget(), mainN):
            p = unitOptionsDialog(parent=self,font=self.unit_editor.body_font)
            theme = p.exec_()
            data = updateJSON()
        
            #apply data from preferences
            if (theme != 0):
                active_theme = getattr(UI_colorTheme, data["active_theme"])
                if (data["theme_changed"] == True):
                    self.unit_editor.unitToJSON()
                    self.restart()
                    
        elif isinstance(self.m.currentWidget(), mainS):
            p = NodePreferencesDialog(parent=self)
            theme = p.exec_()
            data = updateJSON()
            
            #apply data from preferences
            if (theme != 0):
                active_theme = getattr(UI_colorTheme, data["active_theme"])
                if (data["theme_changed"] == True):
                    self.skills_editor.scene.saveToFile()
                        
                    with open("src/tmp/wer.taic", "w") as tmp_reason:
                        tmp_reason.write(OPEN_LAST_FILE)
                    with open("src/tmp/lsf.taic", "w") as next_open_file:
                        try:
                            next_open_file.write(self.skills_editor.scene.path)
                        except:
                            with open("src/tmp/wer.taic", "w") as tmp_reason:
                                tmp_reason.write(OPEN_NEW_FILE)
                        
                    self.restart()
                    
    def restart(self):
        with open("src/tmp/wer.taic", "w") as tmp_reason:
            tmp_reason.write(OPEN_LAST_FILE)
            with open("src/tmp/lsf.taic", "w") as next_open_file:
                try:
                    next_open_file.write(self.skills_editor.path)
                except:
                    with open("src/tmp/wer.taic", "w") as tmp_reason:
                        tmp_reason.write(OPEN_NEW_FILE)
                    
                os.execl(sys.executable, sys.executable, *sys.argv)

    def quitWindow(self):
        c = confirmAction(parent=self, s="quit the editor")
        c.exec_()
        with open("src/tmp/wer.taic", "w") as quit_reason:
            quit_reason.write(OPEN_NEW_FILE)
        if(c.return_confirm):
            sys.exit()
            
    def helpView(self):
        h = webView(page = 3, parent=self)
        h.exec_()

window = main()
window.show()
a = app.exec_()