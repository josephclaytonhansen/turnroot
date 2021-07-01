import pygame, sys, random, json
#Overhaul later
TILE_TYPES = {0:"Neutral terrain", 1:"Neutral terrain",2:"Neutral terrain", 3:"Adds health each turn",
              30:"Raises avoidance except for flyers", 31:"Slows movement",32:"Neutral terrain",33:"Neutral terrain"}
TILE_TYPE_NAMES = {0:"Floor", 1:"Floor",2:"Floor", 3:"Heal",
              30:"Forest", 31:"Shallow Water",32:"Floor",33:"Floor"}
TILE_CONTENTS = {64:"friendly_unit", 162:"enemy_unit"}

FRIEND = 0
ENEMY = 1
ALLY = 2
TILE = 3

ALL_MENU_TILES = ["*Attack","*Assist","*Rally","Wait",
"Items","*Mount/Dismount","*Trade","*Convoy",
 "*Rescue","*Units","*Options","*End"]
CURRENT_MENU_TILES = ALL_MENU_TILES.copy()
#No, it doesn't, but it does for now. Get from unit later
#To be exact- if enemy units in danger area or move area (or max_range for weird stuff like Meteor), show attack
#If allied units in assist max_radius, show assist
#If allied unit adjacent, show rally/trade/rescue (if can be rescued, figure that out later)
#If unit is mounted, show mount/dismount
#If protagonist adjacent, or selected unit is protagonist, show convoy
#Wait/options/units/end always show
#So the only way there's ACTUALLY all items is if a mounted healer protagonist is adjacent to another unit

MENU_ITEMS = {}

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
        with open ("app/preferences.json", "r") as h:
            l = json.load(h)
        self.sfx_max_volume = l[0]
        self.music_max_volume = l[1]
        self.max_voices_volume = l[2]
        self.subtitles = l[3]
        self.smart_end = l[4]
        self.cursor_memory = l[5]
        self.hp_gauge_type = l[6]
        self.x_axis = l[7]
        self.y_axis = l[8]
        self.axis_changed = False
        
    def pack(self):
        with open("src/tmp/sc.trecd", "w") as f:
            d = [self.scale, self.fps, self.cursor_speed, self.grid_dimensions]
            json.dump(d,f)
        with open("src/tmp/sc2.trecd", "w") as da:
            g = [self.CURSOR_OVER, self.GRID_OVER, self.GRID_OPACITY, self.SANS_GAME_FONT,self.SERIF_GAME_FONT,
                 self.OVERLAY_PLACEMENTS64,self.OVERLAY_PLACEMENTS32,self.GUARD_ICON,self.AVOID_ICON,self.HEAL_ICON,
                 self.GUARD_ICON32,self.AVOID_ICON32,self.HEAL_ICON32,self.KEY_OVER,self.KEY_OVER_WIDE,self.KEY_OVER32,self.KEY_OVER_WIDE32,self.SELECTION_OVERLAY_TYPE]
            json.dump(g,da)
        with open ("app/preferences.json", "w") as h:
            l = [self.sfx_max_volume,self.music_max_volume,self.max_voices_volume,self.subtitles,self.smart_end,self.cursor_memory,self.hp_gauge_type,self.x_axis,self.y_axis]
            json.dump(l,h)
            
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

def initMenuItems(parent):
    menu_index = -1
    #rework to only include relevant menu items
    for item in CURRENT_MENU_TILES:
        menu_index += 1
        MENU_ITEMS[menu_index] = item
        #below- no it doesn't, but it works for now
        parent.current_menu_length = len(CURRENT_MENU_TILES)-1

def showMenuTiles(parent):
    start_pos = [860,0]
    for item in CURRENT_MENU_TILES:
        start_pos[1] += 55
        img = overlayOver(image64="app/app_imgs/overlays/menu_tile.png",image32="app/app_imgs/overlays/menu_tile.png")
        text = parent.fonts["SERIF_20"].render(item, 1, parent.colors["CREAM"])
        parent.fake_screen.blit(img.image, start_pos)
        parent.fake_screen.blit(text, (start_pos[0]+5,start_pos[1]+5))

def showMenuCursor(parent):
    item = MENU_ITEMS[parent.active_menu_index]
    text = parent.fonts["SERIF_20"].render(item, 1, parent.colors["CREAM"])
    img = overlayOver(image64="app/app_imgs/overlays/menu_tile_selected.png",image32="app/app_imgs/overlays/menu_tile_selected.png")
    pos = [860,55*(parent.active_menu_index+1)]
    parent.fake_screen.blit(img.image, pos)
    parent.fake_screen.blit(text, (pos[0]+5,pos[1]+5))
    
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
        
#init tile grid- runs once
def initGrid(parent):
    parent.fullmap = pygame.Surface((C.grid_dimensions[0]*C.scale, C.grid_dimensions[1]*C.scale))
    parent.fullmap_rect = parent.fullmap.get_rect()
    max_x = int(parent.dimensions[0] / C.scale)
    max_y = int(parent.dimensions[1] / C.scale)
    for x in range(0,C.grid_dimensions[0]+1):
        parent.tiles[x] = {}
        parent.units_pos[x]  = {}
        for y in range(0,C.grid_dimensions[1]+1):
            parent.units_pos[x][y] = None
            parent.tiles[x][y] = Tile(x,y,0,"ground")
            parent.tile_group.add(parent.tiles[x][y])
            parent.graphics.add(parent. tiles[x][y])
            if (x+(y*C.grid_dimensions[1])) in TILE_CONTENTS:
                parent.units_pos[x][y] = gUnit(x,y,TILE_CONTENTS[(x+(y*C.grid_dimensions[1]))])
                parent.on_screen_units.add(parent.units_pos[x][y])
            
    if C.GRID_OVER:
        parent.grid = gridOver(0,0,GRID_COLOR)
        parent.grid.image.set_alpha(C.GRID_OPACITY*(255/100))

#load fonts- runs once
def initFont(parent):
    parent.fonts = {}
    for font in [C.SANS_GAME_FONT, C.SERIF_GAME_FONT]:
        if font == C.SANS_GAME_FONT:
            n = "SANS"
        else:
            n = "SERIF"
        font_path = "app/app_fonts/"+font
        for size in [10,12,14,16,18,20,22,24,28,32,48]:
            font_size = size
            fontObj = pygame.font.Font(font_path, font_size)
            parent.fonts[n+"_"+str(font_size)] = fontObj

def centerCursor(parent):
    parent.camera.x = parent.cursor_pos[0] - 640
    parent.camera.y = parent.cursor_pos[1] - 384

        