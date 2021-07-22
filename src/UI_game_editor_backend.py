from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

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