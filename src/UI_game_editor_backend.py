from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import src.UI_colorTheme as UI_colorTheme
from src.UI_updateJSON import updateJSON
import fnmatch, os, json

from src.node_backend import getFiles, GET_FILES
from src.skeletons.unit_class import unitClass
from src.skeletons.unit import Unit

TOTAL_TASKS = 10

FATAL_ERROR = "Fatal Error"
WARNING = "Warning"
CAUTION = "Caution"
NO_ERROR = "No Error"

TEXT = ["#fc8dad", "#fab491", "#d7f09e"]
BACKGROUND = ["#520219", "#612508", "#384220"]
EC = ["Fatal Error", "Warning", "Caution"]

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
    query_box.setFont(parent.body_font)
    row_layout.addWidget(query_box)
    
    for o in options:
        option = QPushButton(o)
        option.setFont(parent.body_font)
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
    help_button.h = helpt 
    help_button.clicked.connect(parent.help_text)
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
        for x in EC:
            self.columns[x] = QListWidget()
            self.columns[x].setStyleSheet("background-color: "+BACKGROUND[EC.index(x)]+";color: "+TEXT[EC.index(x)])
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
        layout.addWidget(QLabel("'Fatal Errors' prevent your game from being playable.\n 'Warnings' won't make your game unplayable, but they may seriously affect the final game.\n 'Caution' warnings may be safely disregarded sometimes.")) 

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
                return [FATAL_ERROR, "Game folder not set"]
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
                return [FATAL_ERROR, "Game folder not set"]
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
                return [FATAL_ERROR, "Game folder not set"]
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
                return [FATAL_ERROR, "Game folder not set"]
        #test items folder
        elif n == 4:
            try:
                dirpath = self.parent.game_path+"/items"
                return[NO_ERROR]
            except:
                return [FATAL_ERROR, "Game folder not set"]
        #check game options
        elif n == 5:
            try:
                dirpath = self.parent.game_path+"/dat.trsl"
                with open(dirpath, "r") as f:
                    td = json.load(f)
                    if len(td) == 0 :
                        return[FATAL_ERROR, "No game options set"]
                    elif len(td) < 30:
                        return[FATAL_ERROR, "Many game options not set"]
                    elif len(td) < 35:
                        return [WARNING, "Some game options not set"]
                    elif len(td) < 46:
                        return [CAUTION, "Some game options may not be set"]
                    else:
                        return[NO_ERROR]
            except:
                return [FATAL_ERROR, "Game folder not set"]
           
        #check base classes assigned to units
        elif n == 6:
            try:
                count = 0
                dirpath = self.parent.game_path+"/classes"
                file_list = getFiles(dirpath)[GET_FILES]
                cla = {}
                for f in file_list:
                    tmp_class = unitClass()
                    try:
                        tmp_class.selfFromJSON(f.path)
                        cla[tmp_class.unit_class_name] = tmp_class
                    except:
                        pass
                dirpath2 = self.parent.game_path+"/units"
                file_list = getFiles(dirpath2)[GET_FILES]
                uni = {}
                for f in file_list:
                    tmp_unit = Unit()
                    try:
                        tmp_unit.selfFromJSON(f.path)
                        uni[tmp_unit.name] = tmp_unit
                    except:
                        pass
                for u in uni:
                    for c in cla:
                        if c in uni[u].past_classes:
                            count +=1
                if count == 0:
                    return[FATAL_ERROR, "No base classes are assigned to units"]
                elif count < len(cla):
                    return[CAUTION, "Some base classes are not assigned to units,\n they will need an item to be usable in-game"]

            except Exception as e:
                print(e)
                return [FATAL_ERROR, "Game folder not set"]
        
        #check end credits
        elif n == 7:
            try:
                dirpath = self.parent.game_path+"/game_options/end_credits.trsl"
                with open(dirpath, "r") as f:
                    td = json.load(f)
                    null_count = 0
                    for k in td:
                        for j in k:
                            if j == "":
                                null_count += 1
                if null_count == 0:
                    return [NO_ERROR]
                else:
                    return [CAUTION, "The end credits have "+str(null_count)+" blank spaces (this may be intentional)"]
            except Exception as e:
                print(e)
                return [CAUTION, "No end credits file"]
            
        #check cover art
        elif n == 8:
            try:
                dirpath = self.parent.game_path+"/game_options/cover_art.trsl"
                with open(dirpath, "r") as f:
                    td = json.load(f)
                    if os.path.exists(td) == False:
                        return [WARNING, "Assigned cover art image could not be found"]
            except Exception as e:
                print(e)
                return [CAUTION, "No cover art assigned (will be auto-generated)"]
        
        #check unit files for portraits
        #check unit files for names
        #check unit files for pronouns
        #check unit files for classes
        #check skills for connections
        #check skills for event flow
        #check weapons for weapon type
        #check weapons combat stats
        #check weapon pricing stats
                    
        else:
            return[NO_ERROR]

    
    def runTest(self):
        self.completed = 0
        self.added_errors = []
        task_index = -1
        for y in self.columns:
            self.columns[y].clear()
            qApp.processEvents()
        while task_index < TOTAL_TASKS:
            task_index += 1
            self.errors[task_index] = self.ERROR_CHECK(task_index)
            self.completed += (100 / TOTAL_TASKS)
            self.progress.setValue(self.completed)
            for k in self.errors:
                try:
                    if self.errors[k][0] != "No Error":
                        if self.errors[k][1] not in self.added_errors:
                            self.columns[self.errors[k][0]].addItem(self.errors[k][1])
                            self.added_errors.append(self.errors[k][1])
                except: #no error
                    pass
            qApp.processEvents()