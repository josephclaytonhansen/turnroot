#thanks to janbodnar for the skeleton

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
import json
from src.UI_updateJSON import updateJSON

ind = 0
entries = ["Keyboard Shortcuts", "Quickstart", "Creation Checklists", "Turnroot Documentation (Read the Docs)", "Turnroot Forums"]
data = {"font_size": 15, "rfont_size": 15,
        "active_theme": "midnight_spark_yellow",
        "active_layout": "right_lower", "icon_size": "26",
        "ah_rte": True, "ah_tasks": True, "ah_taskss": True,
        "ah_overlays": False, "theme_changed": False}

data = updateJSON()
import src.UI_colorTheme

active_theme = getattr(src.UI_colorTheme, data["active_theme"])


class webView(QDialog):
    
    def __init__(self, page, parent=None):
        super().__init__()
        updateJSON()
        self.ind = ind
        self.page = page
        self.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: "+active_theme.window_background_color+";color: "+active_theme.window_text_color)
        self.setWindowTitle("Help")
        self.setMinimumHeight(600)
        #the overall layout is a grid
        self.layout = QHBoxLayout()
        self.help_categories = QListWidget()
        self.layout.addWidget(self.help_categories)
        self.setLayout(self.layout)
        #list categories on the left
        self.help_categories.addItems(entries)
        self.help_categories.setMinimumWidth(200)
        self.help_categories.setMaximumWidth(300)
        self.help_categories.setStyleSheet("font-size: "+str(data["font_size"])+"px; background-color: "+active_theme.list_background_color)
        self.help_categories.currentTextChanged.connect(self.category_change)
        self.help_categories.currentTextChanged.connect(self.loadPage)
        
        #options on the right
        self.help = QWebEngineView()
        self.help.setMinimumWidth(950)
        
        #options are stacked
        self.help_layout = QStackedLayout()
        self.aes = QWidget()
        
        self.ind = self.page
        self.loadPage()
        self.help_layout.addWidget(self.help)
        self.aes.setLayout(self.help_layout)
        self.layout.addWidget(self.aes)
        self.show()

    def loadPage(self):
        if (self.ind < 3):
            with open('src/help_docs/help_'+str(self.ind)+'.html', 'r') as f:
                html = f.read()
                self.help.setHtml(html)
        elif self.ind == 3:
            self.help.setUrl(QUrl("https://turnroot.readthedocs.io/en/latest/"))
        elif self.ind == 4:
            self.help.setUrl(QUrl("http://forums.turnroot.com/"))

    def category_change(self, s):
        for x in range(0, len(entries)):
            if (s == entries[x]):
                self.ind = x
                self.help_layout.setCurrentIndex(self.ind)
