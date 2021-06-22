import pygame, sys, random, json

class Constants():
    def __init__(self,data):
        super().__init__()
        with open(data, "r") as f:
            d = json.load(f)
        self.scale = d[0]
        self.fps = d[1]
        self.cursor_speed = d[2]

C = Constants("src/tmp/sc.trecd")
C.scale = 64

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
        self.cursor_x_change = 0
        self.cursor_y_change = 0
        
        self.dimensions = dimensions
        self.last_cursor_move = pygame.time.get_ticks()
        
        self.tiles = {}
        
        self.tile_group = pygame.sprite.Group()
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
        self.fake_screen = fake_screen
        self.screen = screen
        self.icon = icon
        running = True
        
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
                        self.cursor_y_change = -C.scale
                    elif event.key == pygame.K_DOWN:
                        self.cursor_y_change = C.scale
                    elif event.key == pygame.K_LEFT:
                        self.cursor_x_change = -C.scale
                    elif event.key == pygame.K_RIGHT:
                        self.cursor_x_change = C.scale
                    elif event.key == pygame.K_RETURN:
                        t = self.tiles[self.tile_pos[0]][self.tile_pos[1]]
                        print(t.x, t.y, t)

                #Key release
                elif event.type == pygame.KEYUP:
                    if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                        self.cursor_x_change = 0
                        self.cursor_y_change = 0
                        
                #Handle screen size
                elif event.type == pygame.VIDEORESIZE:
                    screen = pygame.display.set_mode((int(event.size[0]), int(event.size[1])), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
                    self.screen_rect = self.screen.get_rect()
            
            screen.fill(bar_bg)
            self.fake_screen.fill(initial_bg)
            
            #self.show...
            self.graphics.draw(self.fake_screen)
                
                
            self.showCursor()
            
            #screen.blit(pygame.transform.scale(self.fake_screen, screen.get_rect().size), (0, 0))
            if self.screen_rect.size != self.dimensions:
                fit_to_rect = self.fake_rect.fit(self.screen_rect)
                fit_to_rect.center = self.screen_rect.center
                scaled = pygame.transform.smoothscale(self.fake_screen, fit_to_rect.size)
                self.screen.blit(scaled, fit_to_rect)
            else:
                self.screen.blit(self.fake_screen, (0,0))
            
            pygame.display.update()
            
    def initGrid(self):
        max_x = int(self.dimensions[0] / C.scale)
        max_y = int(self.dimensions[1] / C.scale)
        for x in range(0,max_x+1):
            self.tiles[x] = {}
            
            for y in range(0,max_y+1):
                self.tiles[x][y] = Tile(x,y,0,"ground")
                self.tile_group.add(self.tiles[x][y])
                self.graphics.add(self.tiles[x][y])
    
    def showCursor(self):
        if C.scale == 64:
            img = pygame.image.load("app/app_imgs/64cursor.png")
        elif C.scale == 32:
            img = pygame.image.load("app/app_imgs/32cursor.png")
        now = pygame.time.get_ticks()
        if now - self.last_cursor_move >= self.cursor_move_cooldown:
            self.cursor_pos[0] += self.cursor_x_change
            self.cursor_pos[1] += self.cursor_y_change
            if self.cursor_pos[0] < 0:
                self.cursor_pos[0] = 0
            if self.cursor_pos[0] >= self.dimensions[0] - C.scale:
                self.cursor_pos[0] = self.dimensions[0] - C.scale
            if self.cursor_pos[1] < 0:
                self.cursor_pos[1] = 0
            if self.cursor_pos[1] >= self.dimensions[1] - C.scale:
                self.cursor_pos[1] = self.dimensions[1] - C.scale
            
            self.tile_pos[0] = int(self.cursor_pos[0] / C.scale) + self.tile_offset[0]
            self.tile_pos[1] = int(self.cursor_pos[1] / C.scale) + self.tile_offset[1]
            
            self.last_cursor_move = now
            
        imgX = self.cursor_pos[0]
        imgY = self.cursor_pos[1]
        self.fake_screen.blit(img, (imgX,imgY))

m = sandbox((15*C.scale,13*C.scale), "Sandbox", "#FfFfFf", "icon.png", "#000000", C.cursor_speed)
