#thanks to janbodnar

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
import json

ind = 0
entries = ["Help Topic 1", "Help Topic 2", "Help Topic 3"]
data = {"font_size": 15, "rfont_size": 15,
        "active_theme": "midnight_spark_yellow",
        "active_layout": "right_lower", "icon_size": "26",
        "ah_rte": True, "ah_tasks": True, "ah_taskss": True,
        "ah_overlays": False, "theme_changed": False}

with open("preferences.json", "r") as read_file:
    data = json.load(read_file)
    font_size = data["font_size"]
    icon_size = data["icon_size"]
    rfont_size = data["rfont_size"]
    active_theme = data["active_theme"]
    active_layout = data["active_layout"]
    ah_rte = ["ah_rte"]
    ah_tasks = data["ah_tasks"]
    ah_taskss = data["ah_taskss"]
    ah_overlays = data["ah_overlays"]
    theme_changed = False
    data["theme_changed"] = False
    read_file.close()

from UI_updateJSON import updateJSON
import UI_colorTheme

active_theme = getattr(UI_colorTheme, active_theme)


class webView(QDialog):
    
    def __init__(self, parent=None):
        super().__init__()
        updateJSON()
        self.ind = ind
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
        self.help.setMinimumWidth(400)
        
        #options are stacked
        self.help_layout = QStackedLayout()
        self.aes = QWidget()

        self.loadPage()
        self.help_layout.addWidget(self.help)
        self.aes.setLayout(self.help_layout)
        self.layout.addWidget(self.aes)
        self.show()

    def loadPage(self):
        with open('help_docs/help_'+str(self.ind)+'.html', 'r') as f:
 
             html = f.read()
             self.help.setHtml(html)

    def category_change(self, s):
        for x in range(0, len(entries)):
            if (s == entries[x]):
                self.ind = x
                print(ind)
                self.help_layout.setCurrentIndex(self.ind)