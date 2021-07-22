from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import src.UI_colorTheme as UI_colorTheme
from src.UI_updateJSON import updateJSON
import fnmatch

TOTAL_TASKS = 10

FATAL_ERROR = "Fatal Error"
WARNING = "Warning"
CAUTION = "Caution"
NO_ERROR = "No Error"

def selectionRow(parent, query, options, colors, helpt):
    row = QWidget()
    row_layout = QHBoxLayout()
    row.setLayout(row_layout)
    row.options = {}
        
    row.dL = QLabel()
    row.dL.setMaximumWidth(10)
    row.dL.setPixmap(QPixmap("src/ui_icons/off.png"))
    row_layout.addWidget(row.dL)
    
    query_box = QLabel(query)
    row_layout.addWidget(query_box)
    
    for o in options:
        option = QPushButton(o)
        option.setMinimumHeight(48)
        option.name = o
        option.row = row
        option.row_name = query
        option.clicked.connect(parent.toggleOption)
        if len(options) > 1:
            option.setCheckable(True)
            row.options[o] = option 
        option.setStyleSheet("color:white; background-color: "+colors[options.index(o)])
        row_layout.addWidget(option)

    help_button = QPushButton()
    help_button.setIcon(QIcon("src/ui_icons/white/question-mark-4-32.png"))
    help_button.setIconSize(QSize(48,48))
    help_button.setMaximumWidth(48)
    help_button.setStyleSheet("background-color: "+parent.active_theme.window_background_color+"; color:"+parent.active_theme.window_text_color)
    
    row_layout.addWidget(help_button)

    return row

class checkDialog(QDialog):
    def __init__(self,parent=None):
        data = updateJSON()
        self.parent = parent
        self.active_theme = getattr(UI_colorTheme, data["active_theme"])
        super().__init__(parent)
        self.setStyleSheet("background-color: "+self.active_theme.window_background_color+";color: "+self.active_theme.window_text_color)
        
        self.errors = {}
        
        self.progress = QProgressBar(self)
        self.test = QPushButton("Test")
        self.test.clicked.connect(self.runTest)
        
        layout = QVBoxLayout()
        layout.setContentsMargins( 8,8,8,8)
        layout.setSpacing(0)
        
        column_widget = QWidget()
        column_widget_layout = QHBoxLayout()
        column_widget.setLayout(column_widget_layout)
        
        self.columns = {}
        for x in ["Fatal Error", "Warning", "Caution"]:
            self.columns[x] = QListWidget()
            self.columns[x].setStyleSheet("background-color: "+self.active_theme.list_background_color+";color: "+self.active_theme.window_text_color)
            label = QLabel(x)
            
            g = QWidget()
            g_layout = QVBoxLayout()
            g.setLayout(g_layout)
            g_layout.addWidget(label)
            g_layout.addWidget(self.columns[x])
            
            column_widget_layout.addWidget(g)
        
        layout.addWidget(self.test)
        layout.addWidget(self.progress)
        layout.addWidget(column_widget)
        
        self.setLayout(layout)
        self.show()
    
    def ERROR_CHECK(self, n):
        #basic errors first- counts
        #test unit count
        if n == 0:
            try:
                dirpath = self.parent.game_path+"/units"
                if len(fnmatch.filter(os.listdir(dirpath), '*.truf')) == 0:
                   return [FATAL_ERROR, "No units found"]
                elif len(fnmatch.filter(os.listdir(dirpath), '*.truf')) < 12:
                   return [WARNING, "Total units less than 12"]
                elif len(fnmatch.filter(os.listdir(dirpath), '*.truf')) < 24:
                    return [CAUTION, "Total units less than 24"]
                else:
                    return [NO_ERROR]
            except:
                return [FATAL_ERROR, "No unit folder in game folder"]
        #test class count
        elif n == 1:
            try:
                dirpath = self.parent.game_path+"/classes"
                if len(fnmatch.filter(os.listdir(dirpath), '*.tructf')) == 0:
                   return [FATAL_ERROR, "No classes found"]
                elif len(fnmatch.filter(os.listdir(dirpath), '*.tructf')) < 10:
                   return [WARNING, "Total classes less than 10"]
                elif len(fnmatch.filter(os.listdir(dirpath), '*.tructf')) < 20:
                    return [CAUTION, "Total classes less than 20"]
                else:
                    return [NO_ERROR]
            except:
                return [FATAL_ERROR, "No class folder in game folder"]
        #test weapon type count
        elif n == 2:
            try:
                dirpath = self.parent.game_path+"/weapon_types"
                if len(fnmatch.filter(os.listdir(dirpath), '*.json')) == 0:
                   return [FATAL_ERROR, "No weapon types found"]
                elif len(fnmatch.filter(os.listdir(dirpath), '*.json')) < 3:
                   return [WARNING, "Total weapon types less than 3"]
                elif len(fnmatch.filter(os.listdir(dirpath), '*.json')) < 5:
                    return [CAUTION, "Total classes less than 5"]
                else:
                    return [NO_ERROR]
            except:
                return [FATAL_ERROR, "No weapon type folder in game folder"]
        #test skills count
        elif n == 3:
            try:
                dirpath = self.parent.game_path+"/skills"
                if len(fnmatch.filter(os.listdir(dirpath), '*.trnep')) == 0:
                   return [FATAL_ERROR, "No skills found"]
                elif len(fnmatch.filter(os.listdir(dirpath), '*.trnep')) < 7:
                   return [WARNING, "Total skills less than 7"]
                elif len(fnmatch.filter(os.listdir(dirpath), '*.trnep')) < 14:
                    return [CAUTION, "Total skills less than 14"]
                else:
                    return [NO_ERROR]
            except:
                return [FATAL_ERROR, "No skills folder in game folder"]
        #test items folder
        elif n == 4:
            try:
                dirpath = self.parent.game_path+"/items"
                return[NO_ERROR]
            except:
                return [FATAL_ERROR, "No items folder in game folder"]
        else:
            return[NO_ERROR]
    
    def runTest(self):
        self.completed = 0
        self.added_errors = []
        task_index = -1
        while task_index < TOTAL_TASKS:
            task_index += 1
            self.errors[task_index] = self.ERROR_CHECK(task_index)
            self.completed += (100 / TOTAL_TASKS)
            self.progress.setValue(self.completed)
            for k in self.errors:
                print(k, self.errors[k])
                if self.errors[k][0] != "No Error":
                    if self.errors[k][1] not in self.added_errors:
                        self.columns[self.errors[k][0]].addItem(self.errors[k][1])
                        self.added_errors.append(self.errors[k][1])
            qApp.processEvents()