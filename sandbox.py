import pygame, sys, random, json

class Constants():
    def __init__(self,constants):
        super().__init__()
        with open(constants, "r") as f:
            d = json.load(f)
        self.scale = d[0]
        self.fps = d[1]
        self.cursor_speed = d[2]
        self.grid_dimensions = d[3]

C = Constants("src/tmp/sc.trecd")

CURSOR_OVER = True
GRID_OVER = False
GRID_OPACITY = 50

class cursorOver(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.sprites = []
        self.x = x
        self.y = y 
        if C.scale == 64:
            self.sprites.append(pygame.image.load('app/app_imgs/64_cursor_over.png'))
        elif C.scale == 32:
            pass
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x*C.scale,self.y*C.scale]

class gridOver(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.sprites = []
        self.x = x
        self.y = y 
        if C.scale == 64:
            self.sprites.append(pygame.image.load('app/app_imgs/64_grid.png'))
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
            pass
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x*C.scale,self.y*C.scale]
        
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
        
        #init screen
        screen = pygame.display.set_mode(self.dimensions, flags=(pygame.RESIZABLE))
        fake_screen = screen.copy()
        self.camera = fake_screen.get_rect()
        self.fake_screen = fake_screen
        self.screen = screen
        self.icon = icon
        running = True
        
        self.c_over = cursorOver(192,192)
        
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
                    elif event.key == pygame.K_RETURN:
                        t = self.tiles[self.tile_pos[0]][self.tile_pos[1]]
                        print(t.x, t.y, t)
                        self.Select()

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
            
            #draw cursor and map from camera)
            self.showCursor()
            self.fake_screen.blit(self.fullmap, (0,0), self.camera)

            if self.screen_rect.size != self.dimensions:
                fit_to_rect = self.fake_rect.fit(self.screen_rect)
                fit_to_rect.center = self.screen_rect.center
                scaled = pygame.transform.smoothscale(self.fake_screen, fit_to_rect.size)
                self.screen.blit(scaled, fit_to_rect)
            else:
                self.screen.blit(self.fake_screen, (0,0))
            
            pygame.display.update()
            
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
                
                global GRID_OVER, GRID_OPACITY
                if GRID_OVER:
                    self.grid = gridOver(0,0)
                    self.grid.image.set_alpha(GRID_OPACITY)
    
    def showCursor(self):
        now = pygame.time.get_ticks()
        
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
        self.move_over_group.empty()
        #get move and damage from tile contents
        start = self.tile_pos
        move = 2
        damage = 1
        rows = (move* 2) + 1
        for x in range(-move+self.tile_pos[0],move+1+self.tile_pos[0]):
            for y in range(-move+self.tile_pos[1], move+1+self.tile_pos[1]):
                distance = abs(self.tile_pos[0] - x) + abs(self.tile_pos[1] - y)
                if distance <= move:
                    m = moveOver(x*C.scale, y*C.scale)
                    self.move_over_group.add(m)

m = sandbox((21*C.scale,13*C.scale), "Sandbox", "#FfFfFf", "icon.png", "#000000", C.cursor_speed)
