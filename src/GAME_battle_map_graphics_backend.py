import pygame, sys, random, json
#Overhaul later
TILE_TYPES = {0:"Neutral terrain", 1:"Neutral terrain",2:"Neutral terrain", 3:"Adds health each turn",
              30:"Raises avoidance except for flyers", 31:"Slows movement",32:"Neutral terrain",33:"Neutral terrain"}
TILE_TYPE_NAMES = {0:"Floor", 1:"Floor",2:"Floor", 3:"Heal",
              30:"Forest", 31:"Shallow Water",32:"Floor",33:"Floor"}
TILE_CONTENTS = {64:"friendly_unit", 122:"enemy_unit"}

FRIEND = 0
ENEMY = 1
ALLY = 2
TILE = 3

ALL_MENU_TILES = ["*Attack","*Assist","*Rally","Wait",
"Items","*Mount/Dismount","*Trade","*Convoy",
 "*Rescue","*Units","*Options","*End"]

class Constants():
    def __init__(self):
        super().__init__()
        with open("src/tmp/sc.trecd", "r") as f:
            d = json.load(f)
        self.scale = d[0]
        self.fps = d[1]
        self.cursor_speed = d[2]
        self.grid_dimensions = d[3]
        with open("src/tmp/sc2.trecd", "r") as da:
            g = json.load(da)
        self.CURSOR_OVER = g[0]
        self.GRID_OVER = g[1]
        self.GRID_OPACITY = g[2]
        self.SANS_GAME_FONT= g[3]
        self.SERIF_GAME_FONT = g[4]
        self.OVERLAY_PLACEMENTS64 = g[5]
        self.OVERLAY_PLACEMENTS32 = g[6]
        self.GUARD_ICON = g[7]
        self.AVOID_ICON = g[8]
        self.HEAL_ICON = g[9]
        self.GUARD_ICON32 = g[10]
        self.AVOID_ICON32 = g[11]
        self.HEAL_ICON32 = g[12]
        self.KEY_OVER = g[13]
        self.KEY_OVER_WIDE = g[14]
        self.KEY_OVER32 = g[15]
        self.KEY_OVER_WIDE32 = g[16]
        self.SELECTION_OVERLAY_TYPE = g[17]

C = Constants()
print(C.grid_dimensions)

class cursorOver(pygame.sprite.Sprite):
    def __init__(self,x,y,color):
        super().__init__()
        self.sprites = []
        self.x = x
        self.y = y 
        if C.scale == 64:
            if color == "white":
                self.sprites.append(pygame.image.load('app/app_imgs/64_cursor_over_white.png'))
            if color == "black":
                self.sprites.append(pygame.image.load('app/app_imgs/64_cursor_over_black.png'))
        elif C.scale == 32:
            if color == "white":
                self.sprites.append(pygame.image.load('app/app_imgs/32_cursor_over_white.png'))
            if color == "black":
                self.sprites.append(pygame.image.load('app/app_imgs/32_cursor_over_black.png'))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x*C.scale,self.y*C.scale]

class overlayOver(pygame.sprite.Sprite):
    def __init__(self,image64,image32):
        super().__init__()
        self.sprites = []
        if C.scale == 64:
            self.sprites.append(pygame.image.load(image64))
        elif C.scale == 32:
            self.sprites.append(pygame.image.load(image32))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

class gridOver(pygame.sprite.Sprite):
    def __init__(self,x,y,color):
        super().__init__()
        self.sprites = []
        self.x = x
        self.y = y 
        if C.scale == 64:
            if color == "white":
                self.sprites.append(pygame.image.load('app/app_imgs/64_grid_white.png'))
            elif color == "black":
                self.sprites.append(pygame.image.load('app/app_imgs/64_grid_black.png'))
        elif C.scale == 32:
            pass
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x*C.scale,self.y*C.scale]
        
class moveOver(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.sprites = []
        self.x = x
        self.y = y 
        if C.scale == 64:
            self.sprites.append(pygame.image.load('app/app_imgs/64move.png'))
        elif C.scale == 32:
            self.sprites.append(pygame.image.load('app/app_imgs/32move.png'))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x*C.scale,self.y*C.scale]
    
class damageOver(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.sprites = []
        self.x = x
        self.y = y 
        if C.scale == 64:
            self.sprites.append(pygame.image.load('app/app_imgs/64damage.png'))
        elif C.scale == 32:
            self.sprites.append(pygame.image.load('app/app_imgs/32damage.png'))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x*C.scale,self.y*C.scale]

def showMenuTiles(parent):
    start_pos = [860,0]
    for item in ALL_MENU_TILES:
        start_pos[1] += 55
        img = overlayOver(image64="app/app_imgs/overlays/menu_tile.png",image32="app/app_imgs/overlays/menu_tile.png")
        text = parent.fonts["SERIF_20"].render(item, 1, parent.colors["CREAM"])
        parent.fake_screen.blit(img.image, start_pos)
        parent.fake_screen.blit(text, (start_pos[0]+5,start_pos[1]+5))

def showTileTexts64(parent):
    #Get actual values from tile
    parent.avoid_amount = parent.tile_pos[0]
    parent.guard_amount = parent.tile_pos[1]
    parent.heal_amount = 0
    color = parent.colors["BLACK"]
    heal_text = parent.fonts["SERIF_20"].render(str(parent.heal_amount), 1, color)
    avoid_text = parent.fonts["SERIF_20"].render(str(parent.avoid_amount), 1, color)
    guard_text = parent.fonts["SERIF_20"].render(str(parent.guard_amount), 1, color)

    parent.fake_screen.blit(guard_text, C.OVERLAY_PLACEMENTS64[6])
    parent.fake_screen.blit(avoid_text, C.OVERLAY_PLACEMENTS64[7])
    parent.fake_screen.blit(heal_text, C.OVERLAY_PLACEMENTS64[8])
    
    if parent.idle:
        toggle_full_key_label_key = parent.fonts["SERIF_24"].render(parent.toggle_full_key, 1, parent.colors["WHITE"])
        toggle_full_key_label_text = parent.fonts["SANS_16"].render(parent.toggle_full_key_text, 1, parent.colors["BLACK"])
        parent.fake_screen.blit(toggle_full_key_label_key, C.OVERLAY_PLACEMENTS64[25])
        parent.fake_screen.blit(toggle_full_key_label_text, C.OVERLAY_PLACEMENTS64[26])
        
        toggle_menu_key_label_key = parent.fonts["SERIF_24"].render(parent.toggle_menu_key, 1, parent.colors["WHITE"])
        toggle_menu_label_text = parent.fonts["SANS_16"].render(parent.toggle_menu_text, 1, parent.colors["BLACK"])
        parent.fake_screen.blit(toggle_menu_key_label_key, C.OVERLAY_PLACEMENTS64[27])
        parent.fake_screen.blit(toggle_menu_label_text, C.OVERLAY_PLACEMENTS64[28])
        
        toggle_danger_label_key = parent.fonts["SERIF_24"].render(parent.toggle_danger_key, 1, parent.colors["WHITE"])
        toggle_danger_label_text = parent.fonts["SANS_16"].render(parent.toggle_danger_text, 1, parent.colors["BLACK"])
        parent.fake_screen.blit(toggle_danger_label_key, C.OVERLAY_PLACEMENTS64[29])
        parent.fake_screen.blit(toggle_danger_label_text, C.OVERLAY_PLACEMENTS64[30])
    
    #Remove these if statements- a real level will have data for all tiles
    if parent.current_tile_index in TILE_TYPE_NAMES:
        label = parent.fonts["SERIF_22"].render(str(TILE_TYPE_NAMES[parent.current_tile_index]), 1, parent.colors["CREAM"])
        parent.fake_screen.blit(label, (C.OVERLAY_PLACEMENTS64[1][0]+C.OVERLAY_PLACEMENTS64[2][0], C.OVERLAY_PLACEMENTS64[1][1]+C.OVERLAY_PLACEMENTS64[2][1]))
    if parent.current_tile_index in TILE_TYPES:
        tile_type_text = parent.fonts["SANS_16"].render(str(TILE_TYPES[parent.current_tile_index]), 1, color)
        parent.fake_screen.blit(tile_type_text, C.OVERLAY_PLACEMENTS64[9])

    if parent.unit_selected:
        if C.SELECTION_OVERLAY_TYPE == "full":
        #get actual values from unit
            class_text = parent.fonts["SERIF_16"].render("Soldier", 1, parent.colors["CREAM"])
            parent.fake_screen.blit(class_text, C.OVERLAY_PLACEMENTS64[13])
            unit_name = parent.fonts["SERIF_28"].render("Talculí", 1, parent.colors["CREAM"])
            parent.fake_screen.blit(unit_name, C.OVERLAY_PLACEMENTS64[14])
            hp_label = parent.fonts["SERIF_12"].render("HP", 1, parent.colors["CREAM"])
            parent.fake_screen.blit(hp_label, C.OVERLAY_PLACEMENTS64[15])
            hp_text = parent.fonts["SERIF_28"].render("10/10", 1, parent.colors["CREAM"])
            parent.fake_screen.blit(hp_text, C.OVERLAY_PLACEMENTS64[16])
            level_text = parent.fonts["SERIF_20"].render("Lvl "+str(parent.level_number), 1, color)
            parent.fake_screen.blit(level_text, C.OVERLAY_PLACEMENTS64[12])
        else:
            unit_name = parent.fonts["SERIF_20"].render("Talculí", 1, parent.colors["CREAM"])
            parent.fake_screen.blit(unit_name, C.OVERLAY_PLACEMENTS64[18])
            hp_label = parent.fonts["SERIF_12"].render("HP", 1, parent.colors["CREAM"])
            parent.fake_screen.blit(hp_label, C.OVERLAY_PLACEMENTS64[19])
            hp_text = parent.fonts["SERIF_20"].render("10/10", 1, parent.colors["CREAM"])
            parent.fake_screen.blit(hp_text, C.OVERLAY_PLACEMENTS64[20])

class Tile(pygame.sprite.Sprite):
    def __init__(self,x,y,tile_graphic_index,tile_type):
        super().__init__()
        self.x = x
        self.y = y
        self.grid_pos = [x,y]
        self.tile_graphic_index = tile_graphic_index
        self.tile_type = tile_type
        
        self.animateSprites()
        
    def animateSprites(self):
        self.sprites = []
        self.sprites.append(pygame.image.load('app/app_imgs/grass_test.png'))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x*C.scale,self.y*C.scale]

class gUnit(pygame.sprite.Sprite):
    #rework
    def __init__(self,x,y,unit):
        super().__init__()
        self.x = x
        self.y = y
        self.grid_pos = (x*C.grid_dimensions[0])+y
        self.unit = unit
        self.animateSprites()
        
    def animateSprites(self):
        self.sprites = []
        if self.unit == "friendly_unit":
            self.sprites.append(pygame.image.load('app/app_imgs/tmp/friendly_unit.png'))
            self.status = FRIEND
        elif self.unit == "enemy_unit":
            self.sprites.append(pygame.image.load('app/app_imgs/tmp/enemy_unit.png'))
            self.status = ENEMY
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x*C.scale,self.y*C.scale]
