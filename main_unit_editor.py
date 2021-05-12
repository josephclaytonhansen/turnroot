import sys, json, os
import src.UI_colorTheme as UI_colorTheme
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QPalette, QIcon, QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView
from src.UI_updateJSON import updateJSON
from src.UI_Dialogs import confirmAction, infoClose, switchEditorDialog, REPLACE_WINDOW, NEW_WINDOW
from src. UI_unitPreferencesDialog import unitOptionsDialog
from src.UI_ProxyStyle import ProxyStyle
from src.UI_unit_editor_wnd import UnitEditorWnd
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

class mainN(UnitEditorWnd):
    def __init__(self, parent):
        super().__init__(parent)
        self.setMinimumSize(QSize(int(size.width()/1.7), int(size.height()*.7)))
        self.setMaximumSize(QSize(int(size.width()), int(size.height())))

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
        
        self.addToolBar(self.toolbar)
        
        self.menubar = self.menuBar()
        font = self.menubar.font()
        font.setPointSize(data["font_size"])
        self.menubar.setNativeMenuBar(False)
        self.bar = self.menuBar()
        
        self.m = mainN(parent=self)
        
        self.openButton = QAction("&Open", self)
        self.openButton.triggered.connect(self.m.loadFromFile)
        self.openButton.triggered.connect(self.nameChange)
        self.menubar.addAction(self.openButton)
        
        self.saveButton = QAction("&Save", self)
        self.saveButton.triggered.connect(self.m.unitToJSON)
        self.saveButton.triggered.connect(self.nameChange)
        self.menubar.addAction(self.saveButton)
        
        self.setCentralWidget(self.m)
        
    def nameChange(self):
        if self.m.path is not None:
            self.setWindowTitle(title + " - "+self.m.path)
    
    def editorSelect(self):
        e = switchEditorDialog(parent=self)
        e.exec_()
        new_editor = e.editor
        if e.mode == REPLACE_WINDOW:
            pass
        elif e.mode == NEW_WINDOW:
            if new_editor == 0:
                from main_level_editor import main
            elif new_editor == 1:
                pass
            elif new_editor == 2:
                from main_world_editor import main
            elif new_editor == 3:
                from main_hub_editor import main
            elif new_editor == 4:
                from main_unit_editor import main
            elif new_editor == 5:
                from main_object_editor import main
            elif new_editor == 6:
                from main_portrait_editor import main
            elif new_editor == 7:
                from main_class_editor import main
            elif new_editor == 8:
                from main_menu_editor import main
            elif new_editor == 9:
                from main_stores_editor import main
            elif new_editor == 10:
                from main_game_editor import main
            
    def OptionsMenu(self):
        p = unitOptionsDialog(parent=self)
        theme = p.exec_()
        data = updateJSON()
        
        #apply data from preferences
        if (theme != 0):
            active_theme = getattr(UI_colorTheme, data["active_theme"])
            if (data["theme_changed"] == True):
                self.m.unitToJSON()
                    
                with open("src/tmp/wer.taic", "w") as tmp_reason:
                    tmp_reason.write(OPEN_LAST_FILE)
                with open("src/tmp/lsf.taic", "w") as next_open_file:
                    try:
                        next_open_file.write(self.m.path)
                    except:
                        with open("src/tmp/wer.taic", "w") as tmp_reason:
                            tmp_reason.write(OPEN_NEW_FILE)
                    
                os.execl(sys.executable, sys.executable, *sys.argv)
                        
window = main()
window.show()
a = app.exec_()