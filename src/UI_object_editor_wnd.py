from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from src.UI_node_graphics_scene import QDMGraphicsView, QDMGraphicsScene

from src.skeletons.Object import (Object,usableItem,Key,healItem,statIncreaseItem,expIncreaseItem,
                                  classChangeItem,summoningItem,levelEffectItem,equippableItem,Weapon,Shield)

import src.UI_colorTheme as UI_colorTheme
from src.UI_updateJSON import updateJSON
from src.game_directory import gameDirectory
from src.skeletons.weapon_types import weaponTypes
from src.UI_object_editor_dialogs import combatDialog, loadSavedWeapon, pricingDialog, abilitiesDialog
from src.UI_object_editor_more_dialogs import forgingDialog
from src.UI_Dialogs import confirmAction, popupInfo, infoClose
data = updateJSON()
active_theme = getattr(UI_colorTheme, data["active_theme"])

class ObjectEditorWnd(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        
    def initUI(self):
        self.path = None
        self.item_templates = {"Basic Object":Object,
                               "Usable Item":usableItem,
                               "Key":Key,
                               "Heal Item":healItem,
                               "Stat+ Item":statIncreaseItem,
                               "EXP/Knowledge+ Item":expIncreaseItem,
                               "Class Change Item":classChangeItem,
                               "Unit Summoning Item":summoningItem,
                               "Level Effect Item":levelEffectItem,
                               "Equippable Item":equippableItem,
                               "Weapon":Weapon,
                               "Shield":Shield}
        
        self.setStyleSheet("background-color: "+active_theme.window_background_color+"; color:"+active_theme.window_text_color+"; font-size: 16")
        
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        
        self.tabs = QTabWidget()
        self.tabs_font = self.tabs.font()
        self.tabs_font.setPointSize(12)
        self.tabs.setFont(self.tabs_font)
        
        self.tabs.setTabPosition(QTabWidget.South)
        
        self.tscroll = QScrollArea()
        self.tscroll.setWidget(self.tabs)
        self.tscroll.setWidgetResizable(True)
        
        self.tab_names = ["Weapons", "Equippable Items", "Usable Items", "Non-Combat Items"]
        self.tts = ["Edit weapon objects","Edit equippable items such as shields",
                    "Edit usable items (healing items, seals, keys, torches, etc)",
                    "Edit non-combat items (cooking, tea, gifts, forging items, unit summoning items)"]
        
        self.tabs_dict = {}
        for tab in self.tab_names:
            self.tab_title = tab
            self.c_tab = QWidget()
            self.c_tab.setToolTip(self.tts[self.tab_names.index(tab)])
            self.c_tab_layout = QGridLayout()
            self.c_tab.setLayout(self.c_tab_layout)
            self.tabs_dict[tab] = self.c_tab
            self.tabs.addTab(self.c_tab, self.tab_title)
        
        self.tabs.currentChanged.connect(self.ctab_changed)
        
        self.initObject()
        
        self.initWeapons()
        self.initEquippable()
        self.initUsable()
        self.initNonCombat()
        
        self.layout.addWidget(self.tscroll)
        
        self.show()
    
    def initObject(self):
        pass

    def initWeapons(self):
        self.working_tab = self.tabs_dict["Weapons"]
        self.working_tab_layout = self.working_tab.layout()
        
        for x in [0,1,2]:
            self.working_tab_layout.setColumnStretch(x, 3)
        for x in [0,1,2,3]:
            self.working_tab_layout.setRowStretch(x, 3)
        
        self.newWeapon()
        
        self.icon = QPushButton()
        self.icon.setIcon(QIcon(QPixmap("src/ui_icons/white/image.png")))
        self.icon.setIconSize(QSize(64,64))
        self.icon.setMaximumWidth(64)
        self.icon.setMaximumHeight(64)
        
        self.name_edit = QLineEdit()
        self.name_edit.returnPressed.connect(self.nameChange)
        self.name_edit.setPlaceholderText("Weapon name")

        self.desc_edit = QLineEdit()
        self.desc_edit.returnPressed.connect(self.descChange)
        self.desc_edit.setPlaceholderText("Weapon description")
        
        self.connect = QPushButton("Connect")
        
        self.forging = QPushButton("Forge/Repair")
        self.forging.clicked.connect(self.forging_dialog)
        
        self.type = QComboBox()
        self.type.currentTextChanged.connect(self.changeWeaponType)
        
        self.abilities = QPushButton("Abilities")
        self.abilities.clicked.connect(self.abilities_dialog)
        self.abilities.setMinimumWidth(240)
        
        self.combat = QPushButton("Combat")
        self.combat.clicked.connect(self.combat_dialog)
        
        self.sprites = QPushButton("Sprites")
        
        self.pricing = QPushButton("Pricing")
        self.pricing.clicked.connect(self.pricing_dialog)
        
        self.new = QPushButton("New")
        self.new.clicked.connect(self.newWeapon)
        self.save = QPushButton("Load")
        self.save.clicked.connect(self.loadWeaponDialog)
        
        header_font = self.name_edit.font()
        header_font.setPointSize(18)
        body_font = self.name_edit.font()
        body_font.setPointSize(int(data["font_size"]))
        self.body_font = body_font
        
        r = 0
        c = -1
        widgets = [self.icon, self.name_edit, self.desc_edit, self.abilities, self.pricing, self.combat, self.connect, self.forging, self.type]
        tts = ["Change weapon icon/sprites", "change weapon name (press enter to save as name.trwof. Once saved, changes will auto-save", "change weapon description",
               "change weapon special abilities", "change weapon pricing","change weapon combat behavior",
               "change weapon in-game connections (i.e. shop menus, inventories", "change weapon forging/repair capabilities","change weapon type"]
        for w in widgets:
            c += 1
            if c == 3:
                c = 0
                r+= 1
            w.setStyleSheet("background-color: "+active_theme.list_background_color+"; color:"+active_theme.window_text_color+"; font-size: "+str(data["font_size"]))
            w.setToolTip(tts[widgets.index(w)])
            w.setFont(self.body_font)
            w.setMinimumHeight(64)
            self.working_tab_layout.addWidget(w, r, c, 1, 1)
        
        row = QWidget()
        row_layout = QHBoxLayout()
        row.setLayout(row_layout)
        
        n_widgets = [self.new, self.save]
        tts = ["new weapon", "load weapon"]
        for w in n_widgets:
            w.setStyleSheet("background-color: "+active_theme.button_alt_color+"; color:"+active_theme.button_alt_text_color+"; font-size: "+str(data["font_size"]))
            w.setToolTip(tts[n_widgets.index(w)])
            w.setFont(self.body_font)
            w.setMinimumHeight(64)
            row_layout.addWidget(w)
        
        self.working_tab_layout.addWidget(row, r+1, 0, 1, 3)
        
        self.type.addItem("--Select--")
        self.type.addItems(weaponTypes().data)
    
    def changeWeaponType(self):
        if self.sender().currentText != "--Select--":
            self.weapon.type = self.sender().currentText()
            if self.weapon.path != None:
                self.weapon.selfToJSON()
    
    def nameChange(self):
        s = self.sender().text()
        self.weapon.name = s
        self.weapon.path = "src/skeletons/weapons/"+s+".trwof"
        self.weapon.selfToJSON()
        self.parent().parent().save_status.setPixmap(QPixmap("src/ui_icons/white/file_saved.png").scaled(int(int(data["icon_size"])/1.5),int(int(data["icon_size"])/1.5), Qt.KeepAspectRatio))
        self.parent().parent().save_status.setToolTip("Object file saved")
    
    def descChange(self):
        self.weapon.desc = self.sender().text()
        if self.weapon.path != None:
            self.weapon.selfToJSON()
    
    def pricing_dialog(self):
        p = pricingDialog(parent=self,font=self.body_font)
        p.exec_()
    
    def forging_dialog(self):
        f = forgingDialog(parent=self,font=self.body_font)
        f.exec_()
        
    def abilities_dialog(self):
        a = abilitiesDialog(parent=self,font=self.body_font)
        a.exec_()
    
    def combat_dialog(self):
        d = combatDialog(parent=self,font=self.body_font)
        d.exec_()
        
    def newWeapon(self):
        self.weapon = Weapon()
        self.weapon.path = None
        try:
            self.name_edit.clear()
            self.type.clear()
            self.type.addItem("--Select--")
            self.type.addItems(weaponTypes().data)
            self.parent().parent().save_status.setPixmap(QPixmap("src/ui_icons/white/file_not_saved.png").scaled(int(int(data["icon_size"])/1.5),int(int(data["icon_size"])/1.5), Qt.KeepAspectRatio))
            self.parent().parent().save_status.setToolTip("Object file not saved")
        except:
            pass
    
    def loadWeaponDialog(self):
        y = loadSavedWeapon(parent=self,font=self.body_font)
        y.exec_()
        if hasattr(y,"returns"):
            print(y.returns)
            self.weapon.path = y.returns
            self.weapon.selfFromJSON()
            self.name_edit.setText(getattr(self.weapon, "name"))
            self.desc_edit.setText(getattr(self.weapon, "desc"))
            self.type.setCurrentText(getattr(self.weapon, "type"))
            self.parent().parent().save_status.setPixmap(QPixmap("src/ui_icons/white/file_saved.png").scaled(int(int(data["icon_size"])/1.5),int(int(data["icon_size"])/1.5), Qt.KeepAspectRatio))
            self.parent().parent().save_status.setToolTip("Object file saved")
        else:
            c = infoClose("No weapon selected")
            c.exec_()
            self.parent().parent().save_status.setPixmap(QPixmap("src/ui_icons/white/file_not_saved.png").scaled(int(int(data["icon_size"])/1.5),int(int(data["icon_size"])/1.5), Qt.KeepAspectRatio))
            self.parent().parent().save_status.setToolTip("Object file not saved")
    
    def initEquippable(self):
        pass
    
    def initUsable(self):
        pass
    
    def initNonCombat(self):
        pass
    
    def ctab_changed(self):
        pass
    
    def objectFromJSON(self):
        pass
    
    def objectToJSON(self):
        pass
    
    def newObject(self):
        pass
    
    def loadObject(self):
        pass

