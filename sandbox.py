import pygame, sys, random, json
from src.GAME_battle_map_graphics_backend import cursorOver, gridOver, moveOver, damageOver, C, overlayOver

CURSOR_OVER = True
GRID_OVER = True
GRID_COLOR = "white"
GRID_OPACITY = 30
SANS_GAME_FONT = "FiraSans-Light.ttf"
SERIF_GAME_FONT = "Martel-Bold.ttf"
OVERLAY_PLACEMENTS = [(3,80),(4,23),(11,9),(10,90),(70,92),(130,92),(38,88),(100,88),(160,88),(10,124), (10,515)]
GUARD_ICON = "app/app_imgs/overlays/guard_001.png"
AVOID_ICON = "app/app_imgs/overlays/avoid_001.png"
HEAL_ICON = "app/app_imgs/overlays/heal_001.png"

#Overhaul later
TILE_TYPES = {0:"Neutral terrain", 1:"Neutral terrain",2:"Neutral terrain", 3:"Adds health each turn",
              30:"Raises avoidance except for flyers", 31:"Slows movement",32:"Neutral terrain",33:"Neutral terrain"}
TILE_TYPE_NAMES = {0:"Floor", 1:"Floor",2:"Floor", 3:"Heal",
              30:"Forest", 31:"Shallow Water",32:"Floor",33:"Floor"}

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
        if C.scale == 64:
            self.sprites.append(pygame.image.load('app/app_imgs/grass_test.png'))
        elif C.scale == 32:
            self.sprites.append(pygame.image.load('app/app_imgs/32grass_test.png'))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x*C.scale,self.y*C.scale]

class sandbox():
    def __init__(self, dimensions, title, initial_bg, icon, bar_bg, cursor_speed):
        super().__init__()
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()
        self.initMainWindow(dimensions, title, initial_bg, icon, bar_bg, cursor_speed)
    
    def initInitialValues(self, dimensions, cursor_speed):
        self.cursor_pos = [0,0]
        self.tile_pos = [0,0]
        self.tile_offset = [0,0]
        self.current_tile = [0,0]
        self.cursor_x_change = 0
        self.cursor_y_change = 0
        self.cursor_history = []
        self.moved = False
        self.unit_selected = False
        self.tmp_cursor = [0,0]
        
        self.dimensions = dimensions
        self.last_cursor_move = pygame.time.get_ticks()
        
        self.tiles = {}
        
        self.tile_group = pygame.sprite.Group()
        self.move_over_group = pygame.sprite.Group()
        self.graphics = pygame.sprite.Group()
        
        self.cursor_move_cooldown = cursor_speed
        clock = pygame.time.Clock()
        clock.tick(C.fps)
        
    def initMainWindow(self, dimensions, title, initial_bg, icon, bar_bg, cursor_speed):
        #load variables and constants
        self.initInitialValues(dimensions, cursor_speed)
        self.initGrid()
        self.initFont()
        
        #init screen
        screen = pygame.display.set_mode(self.dimensions, flags=(pygame.RESIZABLE))
        fake_screen = screen.copy()
        self.camera = fake_screen.get_rect()
        self.fake_screen = fake_screen
        self.screen = screen
        self.icon = icon
        running = True
        
        self.c_over = cursorOver(192,192,GRID_COLOR)
        
        if C.scale == 64:
            self.c_img = pygame.image.load("app/app_imgs/64cursor.png")
        elif C.scale == 32:
            self.c_img = pygame.image.load("app/app_imgs/32cursor.png")
        
        self.fake_rect = self.fake_screen.get_rect()
        self.screen_rect = self.screen.get_rect()
        
        pygame.display.set_caption(title)
        #i = pygame.image.load(icon)
        #pygame.display.set_icon(i)

        #Game loop
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    sys.exit()
                
                #Key press
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.moved = True
                        self.cursor_y_change = -C.scale
                    elif event.key == pygame.K_DOWN:
                        self.cursor_y_change = C.scale
                        self.moved = True
                    elif event.key == pygame.K_LEFT:
                        self.cursor_x_change = -C.scale
                        self.moved = True
                    elif event.key == pygame.K_RIGHT:
                        self.cursor_x_change = C.scale
                        self.moved = True
                    #A key
                    elif event.key == pygame.K_a:
                        t = self.tiles[self.tile_pos[0]][self.tile_pos[1]]
                        print(t.x, t.y, t)
                        self.Select()
                    #'B' key
                    elif event.key == pygame.K_s:
                        if self.unit_selected:
                            self.Deselect()
                        #replace else with elif for different selection cases
                        else:
                            print("nothing selected")

                #Key release
                elif event.type == pygame.KEYUP:
                    if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                        self.cursor_history = []
                        self.moved = False
                        self.cursor_x_change = 0
                        self.cursor_y_change = 0
                        
                #Handle screen size
                elif event.type == pygame.VIDEORESIZE:
                    screen = pygame.display.set_mode((int(event.size[0]), int(event.size[1])), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
                    self.screen_rect = self.screen.get_rect()
            
            screen.fill(bar_bg)
            self.fake_screen.fill(initial_bg)
            
            #draw grid
            self.tile_group.draw(self.fullmap)
            
            #draw cursor and map from camera
            self.showCursor()
            self.fake_screen.blit(self.fullmap, (0,0), self.camera)
            #draw overlays and overlay text
            self.showOverlays()
            self.showTileTexts()
            
            #fit screen to screen
            if self.screen_rect.size != self.dimensions:
                fit_to_rect = self.fake_rect.fit(self.screen_rect)
                fit_to_rect.center = self.screen_rect.center
                scaled = pygame.transform.smoothscale(self.fake_screen, fit_to_rect.size)
                self.screen.blit(scaled, fit_to_rect)
            else:
                self.screen.blit(self.fake_screen, (0,0))
            
            pygame.display.update()
    
    #init tile grid- runs once
    def initGrid(self):
        self.fullmap = pygame.Surface((C.grid_dimensions[0]*C.scale, C.grid_dimensions[1]*C.scale))
        self.fullmap_rect = self.fullmap.get_rect()
        max_x = int(self.dimensions[0] / C.scale)
        max_y = int(self.dimensions[1] / C.scale)
        for x in range(0,C.grid_dimensions[0]+1):
            self.tiles[x] = {}
            for y in range(0,C.grid_dimensions[1]+1):
                self.tiles[x][y] = Tile(x,y,0,"ground")
                self.tile_group.add(self.tiles[x][y])
                self.graphics.add(self. tiles[x][y])
                
        global GRID_OVER, GRID_OPACITY, GRID_COLOR
        if GRID_OVER:
            self.grid = gridOver(0,0,GRID_COLOR)
            self.grid.image.set_alpha(GRID_OPACITY*(255/100))
    
    #load fonts- runs once
    def initFont(self):
        global SANS_GAME_FONT, SERIF_GAME_FONT
        self.fonts = {}
        for font in [SANS_GAME_FONT, SERIF_GAME_FONT]:
            if font == SANS_GAME_FONT:
                n = "SANS"
            else:
                n = "SERIF"
            font_path = "app/app_fonts/"+font
            for size in [12,14,16,20,22,24,28,32,48]:
                font_size = size
                fontObj = pygame.font.Font(font_path, font_size)
                self.fonts[n+"_"+str(font_size)] = fontObj

    def showOverlays(self):
        ground_desc = overlayOver(image64="app/app_imgs/overlays/tile_desc_001.png",image32=None)
        tile_name = overlayOver(image64="app/app_imgs/overlays/tile_name_001.png",image32=None)
        unit_info = overlayOver(image64="app/app_imgs/overlays/unit_info_001.png", image32=None)
        
        global OVERLAY_PLACEMENTS, GUARD_ICON, AVOID_ICON, HEAL_ICON
        self.fake_screen.blit(ground_desc.image, OVERLAY_PLACEMENTS[0])
        self.fake_screen.blit(tile_name.image, OVERLAY_PLACEMENTS[1])
        
        guard = overlayOver(image64=GUARD_ICON,image32=None)
        avoid = overlayOver(image64=AVOID_ICON,image32=None)
        heal = overlayOver(image64=HEAL_ICON,image32=None)
        
        self.fake_screen.blit(guard.image, OVERLAY_PLACEMENTS[3])
        self.fake_screen.blit(avoid.image, OVERLAY_PLACEMENTS[4])
        self.fake_screen.blit(heal.image, OVERLAY_PLACEMENTS[5])
        self.fake_screen.blit(unit_info.image, OVERLAY_PLACEMENTS[10])
        
    #update cursor/selected overlays
    def showCursor(self):
        now = pygame.time.get_ticks()
        self.current_tile_index = self.tile_pos[0]+(self.tile_pos[1]*C.grid_dimensions[1])
        self.tile_pos[0] = int(self.cursor_pos[0] / C.scale) + self.tile_offset[0]
        self.tile_pos[1] = int(self.cursor_pos[1] / C.scale) + self.tile_offset[1]
        self.tmp_cursor = self.cursor_pos.copy()
        
        for j in self.move_over_group:
            self.fullmap.blit(j.image,(j.x,j.y))
        
        if now - self.last_cursor_move >= self.cursor_move_cooldown:
            self.cursor_pos[0] += self.cursor_x_change
            self.cursor_pos[1] += self.cursor_y_change
            
            if self.moved:
                self.cursor_history.append([self.cursor_x_change,self.cursor_y_change])
        
            self.tile_pos[0] = int(self.cursor_pos[0] / C.scale) + self.tile_offset[0]
            self.tile_pos[1] = int(self.cursor_pos[1] / C.scale) + self.tile_offset[1]

            if self.cursor_pos[0] < 0:
                self.cursor_pos[0] = 0
            if self.tile_pos[0] >= C.grid_dimensions[0]-1:
                self.cursor_pos[0] = (C.grid_dimensions[0]-1)*C.scale
            if self.cursor_pos[1] < 0:
                self.cursor_pos[1] = 0
            if self.tile_pos[1] >= C.grid_dimensions[1]-1:
                self.cursor_pos[1] = (C.grid_dimensions[1]-1)*C.scale
                
            if self.unit_selected:
                t = (self.tile_pos[0], self.tile_pos[1])
                if t not in self.move_tiles:
                    self.cursor_pos = self.tmp_cursor
            
            if len(self.cursor_history) > 3:
                camera_pan_direction = self.cursor_history[0]
                h_speed = C.scale
                v_speed = C.scale
                if camera_pan_direction[0] == -C.scale:
                    self.camera.x -=h_speed
                elif camera_pan_direction[0] == C.scale:
                    self.camera.x +=h_speed
                if camera_pan_direction[1] == C.scale:
                    self.camera.y +=v_speed
                elif camera_pan_direction[1] == -C.scale:
                    self.camera.y -=v_speed

            self.last_cursor_move = now
            
        imgX = self.cursor_pos[0]
        imgY = self.cursor_pos[1]
        global CURSOR_OVER, GRID_OVER
        if CURSOR_OVER:
            self.fullmap.blit(self.c_over.image, (self.cursor_pos[0]-192, self.cursor_pos[1]-192))
        if GRID_OVER:
            self.fullmap.blit(self.grid.image, (self.camera.x, self.camera.y))
        self.fullmap.blit(self.c_img, (imgX,imgY))
    
    def Select(self):
        #currently selects tile- get unit from tile contents
        self.move_over_group.empty()
        #get move and damage from tile contents
        start = self.tile_pos
        s = start.copy()

        move = 3
        damage = 1
        
        #use these to limit cursor movement
        self.move_tiles = [(s[0],s[1])]
        self.damage_tiles = []
        self.unit_selected = True
        
        rows = (move* 2) + 1
        for x in range(-move+self.tile_pos[0]-damage,move+1+self.tile_pos[0]+damage):
            for y in range(-move+self.tile_pos[1]-damage, move+1+self.tile_pos[1]+damage):
                distance = abs(self.tile_pos[0] - x) + abs(self.tile_pos[1] - y)
                if distance <= move:
                    #and if tile is movable by unit/tile is empty
                    m = moveOver(x*C.scale, y*C.scale)
                    self.move_tiles.append((x,y))
                    self.move_over_group.add(m)
                elif distance > move and distance <= damage + move:
                    d = damageOver(x*C.scale, y*C.scale)
                    self.damage_tiles.append((x,y))
                    self.move_over_group.add(d)
    
    def Deselect(self):
        self.move_over_group.empty()
        self.unit_selected = False
                
    def showTileTexts(self):
        #Get actual values from tile
        self.avoid_amount = self.tile_pos[0]
        self.guard_amount = self.tile_pos[1]
        self.heal_amount = 0
        color = (0,0,0)
        heal_text = self.fonts["SERIF_20"].render(str(self.heal_amount), 1, color)
        avoid_text = self.fonts["SERIF_20"].render(str(self.avoid_amount), 1, color)
        guard_text = self.fonts["SERIF_20"].render(str(self.guard_amount), 1, color)
        self.fake_screen.blit(guard_text, OVERLAY_PLACEMENTS[6])
        self.fake_screen.blit(avoid_text, OVERLAY_PLACEMENTS[7])
        self.fake_screen.blit(heal_text, OVERLAY_PLACEMENTS[8])
        
        global TILE_TYPES, TILE_TYPE_NAMES
        #Remove these if statements- a real level will have data for all tiles
        if self.current_tile_index in TILE_TYPE_NAMES:
            label = self.fonts["SERIF_22"].render(str(TILE_TYPE_NAMES[self.current_tile_index]), 1, (238,238,230))
            self.fake_screen.blit(label, (OVERLAY_PLACEMENTS[1][0]+OVERLAY_PLACEMENTS[2][0], OVERLAY_PLACEMENTS[1][1]+OVERLAY_PLACEMENTS[2][1]))
        if self.current_tile_index in TILE_TYPES:
            tile_type_text = self.fonts["SANS_16"].render(str(TILE_TYPES[self.current_tile_index]), 1, color)
            self.fake_screen.blit(tile_type_text, OVERLAY_PLACEMENTS[9])

m = sandbox((21*C.scale,13*C.scale), "Sandbox", "#000000", "icon.png", "#000000", C.cursor_speed)