from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import src.UI_colorTheme as UI_colorTheme
from src.UI_updateJSON import updateJSON

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
    
    def runTest(self):
        self.completed = 0
        task_index = -1
        while self.completed < 100:
            task_index += 1
            self.errors[ERROR_CHECK[task_index]] = ERROR_CHECK[task_index].run()
            self.completed += 0.01
            self.progress.setValue(self.completed)
            qApp.processEvents()