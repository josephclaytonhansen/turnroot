from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

def selectionRow(parent, query, options, colors, helpt):
    row = QWidget()
    row_layout = QHBoxLayout()
    row.setLayout(row_layout)

    query_box = QLabel(query)
    row_layout.addWidget(query_box)
    
    for o in options:
        option = QPushButton(o)
        if len(options) > 1:
            option.setCheckable(True)
        option.setStyleSheet("background-color: "+colors[options.index(o)])
        row_layout.addWidget(option)
        
    help_button = QPushButton()
    help_button.setIcon(QIcon("src/ui_icons/white/question-mark-4-32.png"))
    help_button.setIconSize(QSize(48,48))
    help_button.setMaximumWidth(48)
    help_button.setStyleSheet("background-color: "+parent.active_theme.window_background_color+"; color:"+parent.active_theme.window_text_color)
    
    row_layout.addWidget(help_button)
    
    return row