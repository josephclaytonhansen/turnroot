import pygame, sys, random, json
from src.GAME_battle_map_graphics_backend import cursorOver, gridOver, moveOver, damageOver, C, overlayOver
GRID_COLOR = "white"
#Overhaul later
TILE_TYPES = {0:"Neutral terrain", 1:"Neutral terrain",2:"Neutral terrain", 3:"Adds health each turn",
              30:"Raises avoidance except for flyers", 31:"Slows movement",32:"Neutral terrain",33:"Neutral terrain"}
TILE_TYPE_NAMES = {0:"Floor", 1:"Floor",2:"Floor", 3:"Heal",
              30:"Forest", 31:"Shallow Water",32:"Floor",33:"Floor"}

class Fader(object):
    instances = []
    def __init__(self, fname,parent):
        self.parent = parent
        super(Fader, self).__init__()
        assert isinstance(fname, str)
        self.sound = pygame.mixer.Sound(fname)
        self.increment = 0.03 # tweak for speed of effect!!
        self.next_vol = 1 # fade to 100 on start
        Fader.instances.append(self)

    def fade_to(self, new_vol):
            self.next_vol = new_vol

    def update(self):
        if self.parent.music_fade[0] == True:
            curr_volume = self.sound.get_volume()
            if self.next_vol > curr_volume:
                self.sound.set_volume(curr_volume + self.increment)
            elif self.next_vol < curr_volume:
                self.sound.set_volume(curr_volume - self.increment)

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
        pygame.display.init()
        pygame.mixer.init()
        pygame.font.init()
        self.initMainWindow(dimensions, title, initial_bg, icon, bar_bg, cursor_speed)
    
    def Fade(self):
        d = self.music_fade[1]
        if d == "in":
            rain_s = self.music_max_volume
            thunder_s = 0.0
            now = pygame.time.get_ticks()
            self.music_fade[0] = True
            #PULL UP NEW SCREEN
            increment = int(1.5 * self.music_max_volume)
            while thunder_s < self.music_max_volume:
                if pygame.time.get_ticks() - now > increment:
                    rain_s -=.01
                    thunder_s += .01
                    self.rain.sound.set_volume(rain_s)
                    self.thunder.sound.set_volume(thunder_s)
                    now = pygame.time.get_ticks()
        elif d == "out":
            thunder_s = self.music_max_volume
            rain_s = 0.0
            now = pygame.time.get_ticks()
            self.music_fade[0] = True
            #PULL UP NEW SCREEN
            increment = int(1.5 * self.music_max_volume)
            while rain_s < self.music_max_volume:
                if pygame.time.get_ticks() - now > increment:
                    thunder_s -=.01
                    rain_s += .01
                    self.rain.sound.set_volume(rain_s)
                    self.thunder.sound.set_volume(thunder_s)
                    now = pygame.time.get_ticks()
        elif d == "init":
            rain_s = 0.0
            now = pygame.time.get_ticks()
            self.music_fade[0] = True
            increment = int(1.5 * self.music_max_volume)
            while rain_s < self.music_max_volume:
                if pygame.time.get_ticks() - now > increment:
                    rain_s += .01
                    self.rain.sound.set_volume(rain_s)
                    now = pygame.time.get_ticks()
            
    def initInitialValues(self, dimensions, cursor_speed):
        self.scales=[1.8,2.3,3]
        self.scale = 1
        self.show_grid_at_scale = True
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
        #get from unit
        self.xp_amount = 0
        self.level_number = 1
        
        self.colors = {"CREAM":(238,238,230),"BLACK":(0,0,0),"WHITE":(255,255,255)}
         
        self.toggle_full_key = "Q"
        self.toggle_full_key_text = "Basic overlay"
        
        self.toggle_menu_key = "Z"
        self.toggle_menu_text = "Menu"
        
        self.toggle_danger_key = "W"
        self.toggle_danger_text = "Show danger area"
        
        self.dimensions = dimensions
        self.last_cursor_move = pygame.time.get_ticks()
        self.last_input = pygame.time.get_ticks()
        self.idle = False
        
        self.tiles = {}
        
        self.tile_group = pygame.sprite.Group()
        self.move_over_group = pygame.sprite.Group()
        self.graphics = pygame.sprite.Group()
        
        self.cursor_move_cooldown = cursor_speed
        self.idle_cooldown = 1400
        self.clock = pygame.time.Clock()
        self.clock.tick(C.fps)
        
        self.music_fade = [False, "init"]
        self.music_max_volume = .7
    
    def initMusic(self,s):
        self.rain = Fader("app/app_sounds/"+s+"_rain"+".mp3",self)
        self.thunder = Fader("app/app_sounds/"+s+"_thunder"+".mp3",self)
        self.rain.sound.play()
        self.thunder.sound.play()
        self.rain.sound.set_volume(0)
        self.thunder.sound.set_volume(0)

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
        
        self.fake_rect = self.fake_screen.get_rect()
        self.screen_rect = self.screen.get_rect()
        
        self.initMusic("fw")
        self.Fade()
        
        pygame.display.set_caption(title)
        #i = pygame.image.load(icon)
        #pygame.display.set_icon(i)

        #Game loop
        while running:

            #idle timer
            now = pygame.time.get_ticks()
            if now - self.last_input >= self.idle_cooldown:
                self.idle = True   

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    sys.exit()
                
                #Key press
                if event.type == pygame.KEYDOWN:
                    self.last_input = pygame.time.get_ticks()
                    self.idle = False
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
                        #if unit selected AND combat selected
                        if self.unit_selected:
                            #pull up battle screen and then self.Fade()
                            self.music_fade[1] = "in"
                            self.Fade()
                        self.Select()
                        

                    #scale map
                    elif event.key == pygame.K_x:
                        self.scale +=1
                        if self.scale == 3:
                            self.scale = 0
                        if self.scale < 2:
                            self.show_grid_at_scale = False
                        else:
                            self.show_grid_at_scale = True
                    #'B' key
                    elif event.key == pygame.K_s:
                        if self.unit_selected:
                            self.Deselect()
                        #replace else with elif for different selection cases
                        else:
                            print("nothing selected")
                    
                    #Shoulder, maybe? Toggle overlay mode
                    elif event.key == pygame.K_q:
                        if self.unit_selected:
                            if C.SELECTION_OVERLAY_TYPE == "full":
                                C.SELECTION_OVERLAY_TYPE = "small"
                                self.toggle_full_key_text = "Full overlay"
                            else:
                                C.SELECTION_OVERLAY_TYPE = "full"
                                self.toggle_full_key_text = "Basic overlay"

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
            self.fullmap_scaled = pygame.transform.scale(self.fullmap, (int(self.scales[self.scale] * self.fake_screen.get_width()), int(self.scales[self.scale] * self.fake_screen.get_height())))
            self.fake_screen.blit(self.fullmap_scaled, (0,0), self.camera)
            #draw overlays and overlay text
            self.showOverlays()
            if C.scale == 64:
                self.showTileTexts64()
            
            #fit screen to screen
            if self.screen_rect.size != self.dimensions:
                fit_to_rect = self.fake_rect.fit(self.screen_rect)
                fit_to_rect.center = self.screen_rect.center
                scaled = pygame.transform.scale(self.fake_screen, fit_to_rect.size)
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
                
        if C.GRID_OVER:
            self.grid = gridOver(0,0,GRID_COLOR)
            self.grid.image.set_alpha(C.GRID_OPACITY*(255/100))
    
    #load fonts- runs once
    def initFont(self):
        self.fonts = {}
        for font in [C.SANS_GAME_FONT, C.SERIF_GAME_FONT]:
            if font == C.SANS_GAME_FONT:
                n = "SANS"
            else:
                n = "SERIF"
            font_path = "app/app_fonts/"+font
            for size in [8,10,12,14,16,20,22,24,28,32,48]:
                font_size = size
                fontObj = pygame.font.Font(font_path, font_size)
                self.fonts[n+"_"+str(font_size)] = fontObj

    def showOverlays(self):
        ground_desc = overlayOver(image64="app/app_imgs/overlays/64tile_desc_001.png",image32="app/app_imgs/overlays/32tile_desc_001.png")
        tile_name = overlayOver(image64="app/app_imgs/overlays/64tile_name_001.png",image32="app/app_imgs/overlays/32tile_name_001.png")

        self.fake_screen.blit(ground_desc.image, C.OVERLAY_PLACEMENTS64[0])
        self.fake_screen.blit(tile_name.image, C.OVERLAY_PLACEMENTS64[1])

        guard = overlayOver(image64=C.GUARD_ICON,image32=C.GUARD_ICON32)
        avoid = overlayOver(image64=C.AVOID_ICON,image32=C.AVOID_ICON32)
        heal = overlayOver(image64=C.HEAL_ICON,image32=C.HEAL_ICON32)
        
        self.fake_screen.blit(guard.image, C.OVERLAY_PLACEMENTS64[3])
        self.fake_screen.blit(avoid.image, C.OVERLAY_PLACEMENTS64[4])
        self.fake_screen.blit(heal.image, C.OVERLAY_PLACEMENTS64[5])
        
        if self.idle:
            toggle_full_selection = overlayOver(image64=C.KEY_OVER,image32=C.KEY_OVER32)
            toggle_damage = overlayOver(image64=C.KEY_OVER,image32=C.KEY_OVER32)
            show_menu = overlayOver(image64=C.KEY_OVER_WIDE,image32=C.KEY_OVER32)

            self.fake_screen.blit(toggle_full_selection.image, C.OVERLAY_PLACEMENTS64[22])
            self.fake_screen.blit(toggle_damage.image, C.OVERLAY_PLACEMENTS64[23])
            self.fake_screen.blit(show_menu.image, C.OVERLAY_PLACEMENTS64[24])
            
        if self.unit_selected:
            if C.SELECTION_OVERLAY_TYPE == "full":
                unit_info = overlayOver(image64="app/app_imgs/overlays/unit_info_001.png", image32="app/app_imgs/overlays/32unit_info_001.png")

                self.fake_screen.blit(unit_info.image, C.OVERLAY_PLACEMENTS64[10])

                xp_bar = overlayOver(image64="app/app_imgs/overlays/xp_bar_001.png", image32="app/app_imgs/overlays/32xp_bar_001.png")
                xp_crest = overlayOver(image64="app/app_imgs/overlays/xp_crest_001.png", image32="app/app_imgs/overlays/32xp_crest_001.png")
                xp_count = 0
                for x in range(int(((2*self.xp_amount)*(148/244)))):
                    xp_count +=1
                    xp_amount = overlayOver(image64="app/app_imgs/overlays/xp_bar_progress_001.png", image32="app/app_imgs/overlays/32xp_bar_progress_001.png")
                    self.fake_screen.blit(xp_amount.image, (C.OVERLAY_PLACEMENTS64[21][0]+(2*xp_count),C.OVERLAY_PLACEMENTS64[21][1]))
                    self.fake_screen.blit(xp_bar.image, C.OVERLAY_PLACEMENTS64[11])
                    self.fake_screen.blit(xp_crest.image, C.OVERLAY_PLACEMENTS64[11])
            else:
                unit_info = overlayOver(image64="app/app_imgs/overlays/unit_info_small_001.png", image32="app/app_imgs/overlays/32unit_info_small_001.png")
                self.fake_screen.blit(unit_info.image, C.OVERLAY_PLACEMENTS64[17])
        
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
                self.cursor_pos[0] = int((C.grid_dimensions[0]-1)*C.scale/(self.scales[self.scale]/2))
            if self.cursor_pos[1] < 0:
                self.cursor_pos[1] = 0
            if self.tile_pos[1] >= C.grid_dimensions[1]-1:
                self.cursor_pos[1] = int((C.grid_dimensions[1]-1)*C.scale/(self.scales[self.scale]/2))
                
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
        if C.CURSOR_OVER:
            self.fullmap.blit(self.c_over.image, (self.cursor_pos[0]-(C.scale*3), self.cursor_pos[1]-(C.scale*3)))
        if C.GRID_OVER:
            if self.show_grid_at_scale:
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
        self.idle = True
        
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
                
    def showTileTexts64(self):
        #Get actual values from tile
        self.avoid_amount = self.tile_pos[0]
        self.guard_amount = self.tile_pos[1]
        self.heal_amount = 0
        color = self.colors["BLACK"]
        heal_text = self.fonts["SERIF_20"].render(str(self.heal_amount), 1, color)
        avoid_text = self.fonts["SERIF_20"].render(str(self.avoid_amount), 1, color)
        guard_text = self.fonts["SERIF_20"].render(str(self.guard_amount), 1, color)

        self.fake_screen.blit(guard_text, C.OVERLAY_PLACEMENTS64[6])
        self.fake_screen.blit(avoid_text, C.OVERLAY_PLACEMENTS64[7])
        self.fake_screen.blit(heal_text, C.OVERLAY_PLACEMENTS64[8])
        
        if self.idle:
            toggle_full_key_label_key = self.fonts["SERIF_24"].render(self.toggle_full_key, 1, self.colors["WHITE"])
            toggle_full_key_label_text = self.fonts["SANS_16"].render(self.toggle_full_key_text, 1, self.colors["BLACK"])
            self.fake_screen.blit(toggle_full_key_label_key, C.OVERLAY_PLACEMENTS64[25])
            self.fake_screen.blit(toggle_full_key_label_text, C.OVERLAY_PLACEMENTS64[26])
            
            toggle_menu_key_label_key = self.fonts["SERIF_24"].render(self.toggle_menu_key, 1, self.colors["WHITE"])
            toggle_menu_label_text = self.fonts["SANS_16"].render(self.toggle_menu_text, 1, self.colors["BLACK"])
            self.fake_screen.blit(toggle_menu_key_label_key, C.OVERLAY_PLACEMENTS64[27])
            self.fake_screen.blit(toggle_menu_label_text, C.OVERLAY_PLACEMENTS64[28])
            
            toggle_danger_label_key = self.fonts["SERIF_24"].render(self.toggle_danger_key, 1, self.colors["WHITE"])
            toggle_danger_label_text = self.fonts["SANS_16"].render(self.toggle_danger_text, 1, self.colors["BLACK"])
            self.fake_screen.blit(toggle_danger_label_key, C.OVERLAY_PLACEMENTS64[29])
            self.fake_screen.blit(toggle_danger_label_text, C.OVERLAY_PLACEMENTS64[30])
        
        #Remove these if statements- a real level will have data for all tiles
        if self.current_tile_index in TILE_TYPE_NAMES:
            label = self.fonts["SERIF_22"].render(str(TILE_TYPE_NAMES[self.current_tile_index]), 1, self.colors["CREAM"])
            self.fake_screen.blit(label, (C.OVERLAY_PLACEMENTS64[1][0]+C.OVERLAY_PLACEMENTS64[2][0], C.OVERLAY_PLACEMENTS64[1][1]+C.OVERLAY_PLACEMENTS64[2][1]))
        if self.current_tile_index in TILE_TYPES:
            tile_type_text = self.fonts["SANS_16"].render(str(TILE_TYPES[self.current_tile_index]), 1, color)
            self.fake_screen.blit(tile_type_text, C.OVERLAY_PLACEMENTS64[9])
    
        if self.unit_selected:
            if C.SELECTION_OVERLAY_TYPE == "full":
            #get actual values from unit
                class_text = self.fonts["SERIF_16"].render("Soldier", 1, self.colors["CREAM"])
                self.fake_screen.blit(class_text, C.OVERLAY_PLACEMENTS64[13])
                unit_name = self.fonts["SERIF_28"].render("Talculí", 1, self.colors["CREAM"])
                self.fake_screen.blit(unit_name, C.OVERLAY_PLACEMENTS64[14])
                hp_label = self.fonts["SERIF_12"].render("HP", 1, self.colors["CREAM"])
                self.fake_screen.blit(hp_label, C.OVERLAY_PLACEMENTS64[15])
                hp_text = self.fonts["SERIF_28"].render("10/10", 1, self.colors["CREAM"])
                self.fake_screen.blit(hp_text, C.OVERLAY_PLACEMENTS64[16])
                level_text = self.fonts["SERIF_20"].render("Lvl "+str(self.level_number), 1, color)
                self.fake_screen.blit(level_text, C.OVERLAY_PLACEMENTS64[12])
            else:
                unit_name = self.fonts["SERIF_20"].render("Talculí", 1, self.colors["CREAM"])
                self.fake_screen.blit(unit_name, C.OVERLAY_PLACEMENTS64[18])
                hp_label = self.fonts["SERIF_12"].render("HP", 1, self.colors["CREAM"])
                self.fake_screen.blit(hp_label, C.OVERLAY_PLACEMENTS64[19])
                hp_text = self.fonts["SERIF_20"].render("10/10", 1, self.colors["CREAM"])
                self.fake_screen.blit(hp_text, C.OVERLAY_PLACEMENTS64[20])
            
m = sandbox((21*C.scale,13*C.scale), "Sandbox", "#000000", "icon.png", "#000000", C.cursor_speed)