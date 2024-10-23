
import pygame
import sys

pygame.init()

# Initialisation des constantes
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1000
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
GOOMBA_WIDTH = 40
GOOMBA_HEIGHT = 40
PLATFORM_WIDTH = 200
PLATFORM_HEIGHT = 20
TRAMPOLINE_HEIGHT = 10  
KEY_WIDTH = 30
KEY_HEIGHT = 30
DOOR_WIDTH = 50
DOOR_HEIGHT = 100
SPIKE_WIDTH = 30
SPIKE_HEIGHT = 30
WHITE = (255,255,255)
BLUE = (0,0,255)
RED = (255,0,0)
BROWN = (60,0,60)
YELLOW = (255,255,0)
LIGHT_GRAY = (169,169,169)
GRAY = (70,64,64)
BLACK = (0,0,0)
GRAVITY = 0.5
JUMP_STRENGTH = 11
PLAYER_SPEED = 5
GOOMBA_SPEED = 3

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mario_De_Wish.exe")

# Pour les images par secondes
clock = pygame.time.Clock()

# Class Platforme
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image = pygame.image.load('texture2.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Class Trampoline
class Trampoline(Platform): 
    def __init__(self, x, y):
        super().__init__(x, y, PLATFORM_WIDTH, TRAMPOLINE_HEIGHT)  
        self.image.fill(BLUE)  

# Class Spike        
class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((SPIKE_WIDTH, SPIKE_HEIGHT), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, BLACK, [(0, SPIKE_HEIGHT), (SPIKE_WIDTH // 2, 0), (SPIKE_WIDTH, SPIKE_HEIGHT)])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Class Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image = pygame.image.load("texture.png")
        self.image= pygame.transform.scale(self.image,(PLAYER_WIDTH, PLAYER_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT
        self.velocity_y = 0
        self.is_jumping = False
        self.health = 1
        self.on_ground = False
        self.has_key = False

    # Update mouvements Player selon la situation
    def update(self, platforms):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q] and self.rect.x > 0:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_d] and self.rect.x < SCREEN_WIDTH - PLAYER_WIDTH:
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = -JUMP_STRENGTH
            self.is_jumping = True
            self.on_ground = False
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y
        self.handle_platform_collisions(platforms)
        if self.rect.y >= SCREEN_HEIGHT - PLAYER_HEIGHT:
            self.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT
            self.on_ground = True
            self.velocity_y = 0

    # J'ai passé beaucoup trop de temps sur des platformes en bois
    def handle_platform_collisions(self, platforms):
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0 and self.rect.bottom <= platform.rect.top + 50:
                    if isinstance(platform, Trampoline):
                        self.velocity_y = -JUMP_STRENGTH - 20  
                    else:
                        self.rect.bottom = platform.rect.top
                        self.velocity_y = 0
                        self.on_ground = True

    # Player peut mourir
    def take_damage(self):
        if self.health > 0:
            self.health -= 1

    def collect_key(self, key):
        if key is not None and pygame.sprite.collide_rect(self, key):
            self.has_key = True
            key.kill()

    # def collect_key(self, key):
    #     if pygame.sprite.collide_rect(self, key):
    #         self.has_key = True
    #         key.kill()

# Class Goomba
class Goomba(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((GOOMBA_WIDTH, GOOMBA_HEIGHT))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - GOOMBA_HEIGHT
        self.direction = 1
        self.alive = True
        self.velocity_y = 0

    # Update mouvements Goomba selon la situation
    def update(self, platforms):
        if self.alive:
            self.rect.x += self.direction * GOOMBA_SPEED
            if self.rect.right >= SCREEN_WIDTH or self.rect.left <= 0:
                self.direction *= -1
            self.velocity_y += GRAVITY
            self.rect.y += self.velocity_y
            for platform in platforms:
                if self.rect.colliderect(platform.rect):
                    if self.rect.bottom <= platform.rect.top + 50:
                        self.rect.bottom = platform.rect.top
                        self.velocity_y = 0
            if self.rect.y >= SCREEN_HEIGHT - GOOMBA_HEIGHT:
                self.rect.y = SCREEN_HEIGHT - GOOMBA_HEIGHT
                self.velocity_y = 0

    def die(self):
        self.alive = False
        self.kill()

# Class Clé
class Key(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((KEY_WIDTH, KEY_HEIGHT))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def key_alive(self):
        self.alive = True


# Class Porte
class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((DOOR_WIDTH, DOOR_HEIGHT))
        self.image.fill(GRAY)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.locked = True

    # ouverture de la porte fermée
    def unlock(self, player):
        if self.locked and pygame.sprite.collide_rect(self, player) and player.has_key:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_e]:
                self.locked = False
                self.image.fill((0, 255, 0))
                return True
        return False

    def check_locked(self, player):
        if self.locked and pygame.sprite.collide_rect(self, player):
            if player.rect.right > self.rect.left:
                player.rect.right = self.rect.left

# Creation Player, Goomba, Key and Door
player = Player()
goomba = Goomba()
key = Key(380, 200)
door = Door(1550, SCREEN_HEIGHT - DOOR_HEIGHT)

platforms = pygame.sprite.Group()
spikes = pygame.sprite.Group()
trampolines = pygame.sprite.Group()
goombas = pygame.sprite.Group()

# Creation des Platforms
platform1 = Platform(0, 900, PLATFORM_WIDTH, PLATFORM_HEIGHT)
platform2 = Platform(0, 800, PLATFORM_WIDTH, PLATFORM_HEIGHT)
platform3 = Platform(200, 800, PLATFORM_WIDTH, PLATFORM_HEIGHT)
platform4 = Platform(500, 825, PLATFORM_WIDTH, PLATFORM_HEIGHT)
platform5 = Platform(800, 800, PLATFORM_WIDTH, PLATFORM_HEIGHT)
platform6 = Platform(1200, 700, PLATFORM_WIDTH, PLATFORM_HEIGHT)
platform7 = Platform(1400, 700, PLATFORM_WIDTH, PLATFORM_HEIGHT)
platform8 = Platform(1500, 600, PLATFORM_WIDTH, PLATFORM_HEIGHT)
platform9 = Platform(1500, 500, PLATFORM_WIDTH, PLATFORM_HEIGHT)
platform10 = Platform(1400, 400, PLATFORM_WIDTH, PLATFORM_HEIGHT)
platform11 = Platform(1000,300, PLATFORM_WIDTH, PLATFORM_HEIGHT)
platform12 = Platform(1200, 400, PLATFORM_WIDTH, PLATFORM_HEIGHT)
platform13 = Platform(1000, 800, PLATFORM_WIDTH, PLATFORM_HEIGHT)
platform14 = Platform(600, 150, PLATFORM_WIDTH, PLATFORM_HEIGHT)
platform15 = Platform(400, 250, PLATFORM_WIDTH, PLATFORM_HEIGHT)
platform16 = Platform(200, 250, PLATFORM_WIDTH, PLATFORM_HEIGHT)
platform17 =  Platform(800, 610, PLATFORM_WIDTH, PLATFORM_HEIGHT)

platforms.add(platform1, platform2, platform3, platform4, platform5, platform6, platform7, platform8, platform9, platform10, platform11, platform12, platform13, platform14, platform15, platform16, platform17)

# Creation des Spikes
spike1 = Spike(500, 795)
spike2 = Spike(670, 795)
spike3 = Spike(1000, 770)
spike4 = Spike(970, 770)
spike5 = Spike(1030, 770)
spike6 = Spike(1410, 370)
spike7 = Spike(1150, 970)
spike8 = Spike(1170, 770)
spike9 = Spike(1320, 670)
spike10 = Spike(1350, 670)
spike11 = Spike(1380, 670)
spike12 = Spike(570, 220)
spike13 = Spike(1380, 370)
spike14 = Spike(1350, 370)
spike15 = Spike(1180, 970 )
spike16 = Spike(0, 770)
spike17 = Spike(30, 770)
spike18 = Spike(0, 870)

spikes.add(spike1, spike2, spike3, spike4, spike5, spike6, spike7, spike8, spike9, spike10, spike11, spike12, spike13, spike14, spike15, spike16, spike17, spike18)

# Creation trampolines + add to sprites
trampoline1 = Trampoline(800, 600)

trampolines.add(trampoline1)

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(goomba)
all_sprites.add(key)
all_sprites.add(door)
all_sprites.add(platforms)
all_sprites.add(spikes)
all_sprites.add(trampolines)  

running = True
scene_changed = False

# Changement de scene
def create_new_scene():
    global scene_changed
    global key2
    global door2
    all_sprites.empty()
    platforms.empty()
    spikes.empty()
    trampolines.empty()


    # Réinitialisation de la position du joueur et du Goomba
    player.rect.x = 250
    player.rect.y = 990
    goomba.rect.x = 50
    goomba.rect.y = 50
    goomba.velocity_y = 0
    platform1 = Platform(0, 900, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platform2 = Platform(0, 800, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platform3 = Platform(0, 700, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platform4 = Platform(0, 600, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platform5 = Platform(0, 500, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platform6 = Platform(0, 400, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platform7 = Platform(0, 300, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platform8 = Platform(1400,910,PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platform10 = Platform(1400, 400, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platform11 = Platform(900,600, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platform12 = Platform(1200, 400, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platform13 = Platform(600, 100, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platform14 = Platform(600, 925, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platform15 = Platform(400, 200, PLATFORM_WIDTH, PLATFORM_HEIGHT) 
    platform16 = Platform(200, 200, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platforms.add(platform1, platform2, platform3, platform4, platform5, platform6, platform7,platform8, platform10, platform11, platform12, platform13, platform14, platform15, platform16)
    new_spike1 = Spike(170, 270)
    new_spike2 = Spike(430, 970)
    new_spike3 = Spike(460, 970)
    new_spike4 = Spike(490, 970)
    new_spike5 = Spike(520, 970)
    new_spike6 = Spike(550, 970)
    new_spike7 = Spike(580, 970)
    new_spike8 = Spike(820, 970)
    new_spike9 = Spike(850, 970)
    new_spike10 = Spike(880, 970)
    new_spike11 = Spike(910, 970)
    new_spike12 = Spike(940, 970)
    new_spike13 = Spike(970, 970)
    new_spike14 = Spike(1000, 970)
    new_spike15 = Spike(1030, 970)
    new_spike16 = Spike(1060, 970)
    new_spike17 = Spike(1090, 970)
    new_spike18 = Spike(1120, 970)
    new_spike19 = Spike(1150, 970)
    new_spike20 = Spike(1180, 970)
    new_spike21 = Spike(1210, 970)
    new_spike22 = Spike(1240, 970)
    new_spike23 = Spike(1270, 970)
    new_spike24 = Spike(1300, 970)
    new_spike25 = Spike(1330, 970)
    new_spike26 = Spike(1360, 970)
    new_spike27 = Spike(1390, 970)
    new_spike28 = Spike(1420, 970)
    new_spike29 = Spike(1450, 970)
    new_spike30 = Spike(1480, 970)
    new_spike31 = Spike(1510, 970)
    new_spike32 = Spike(1540, 970)
    new_spike33 = Spike(1570, 970)
    new_spike34 = Spike(790, 970)
    new_spike35 = Spike(760, 970)
    new_spike36 = Spike(730, 970)
    new_spike37 = Spike(700, 970)
    new_spike38 = Spike(670, 970)
    new_spike39 = Spike(640, 970)
    new_spike40 = Spike(610, 970)
    new_spike41 = Spike(0, 370)
    new_spike42 = Spike(170, 570)
    new_spike43 = Spike(170, 770)
    new_spike44 = Spike(0, 770)
    new_spike45 = Spike(0, 570)
    new_spike46 = Spike(170, 370)
    new_spike47 = Spike(1200, 370)
    new_spike48 = Spike(1230, 370)
    new_spike49 = Spike(50, 470)
    new_spike50 = Spike(120, 670)
    new_spike51 = Spike(380, 170)
    new_spike52 = Spike(410, 170)
    new_spike53 = Spike(570, 170)
    new_spike54 = Spike(770, 70)
    spikes.add(new_spike1, new_spike2, new_spike3, new_spike4, new_spike5, new_spike6, new_spike7, new_spike8, new_spike9, new_spike10, new_spike11, new_spike12, new_spike13, new_spike14, new_spike15, new_spike16, new_spike17, new_spike18, new_spike19, new_spike20, new_spike21, new_spike22, new_spike23, new_spike24, new_spike25, new_spike26, new_spike27, new_spike28, new_spike29, new_spike30, new_spike31, new_spike32, new_spike33, new_spike34, new_spike35, new_spike36, new_spike37, new_spike38, new_spike39, new_spike40, new_spike41, new_spike42, new_spike43, new_spike44, new_spike45, new_spike46, new_spike47, new_spike48, new_spike49, new_spike50, new_spike51, new_spike52, new_spike53, new_spike54)
    new_trampoline1 = Trampoline(1400,900)
    key2 = Key(680,870)
    door2 = Door(1550,300)
    trampolines.add(new_trampoline1)
    all_sprites.add(player, goomba, platforms, spikes, trampolines)
    all_sprites.add(key2)
    all_sprites.add(door2)
    scene_changed = Trueq


def create_new_scene2():
        global key3
        global door3
        global scene_changed
        all_sprites.empty()
        platforms.empty()
        spikes.empty()
        trampolines.empty()
    
        player.rect.x = 100
        player.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT
        goomba3 = Goomba()
        

        platform1 = Platform(200, 900, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        platform2 = Platform(600, 800, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        platform3 = Platform(1000, 700, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        platforms.add(platform1, platform2, platform3)
    
        spike1 = Spike(300, 870)
        spikes.add(spike1)
    
        new_trampoline = Trampoline(1200, 850)
        trampolines.add(new_trampoline)

        key3 = Key(400, 500)
        door3 = Door(1550, 900)

        goombas.add(goomba3)
        all_sprites.add(player, platforms, spikes, trampolines, key3, door3, goomba3)
        scene_changed = False  
	

# Game Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    player.update(platforms)
    goomba.update(platforms)
    player.collect_key(key if not scene_changed else key2)
    if door.unlock(player) and not scene_changed:
        create_new_scene()
    door.check_locked(player)

    if not scene_changed:
        if door.unlock(player):
            create_new_scene()
    else:
        if door2.unlock(player):
            create_new_scene2()

    if not scene_changed:
        door.check_locked(player)
    else:
        door2.check_locked(player)
        door.check_locked(player)

    if pygame.sprite.collide_rect(player, goomba) and goomba.alive:
        if player.rect.bottom <= goomba.rect.top + 50 and player.velocity_y > 0:
            goomba.die()
            player.velocity_y = -JUMP_STRENGTH + 2
        elif player.rect.bottom > goomba.rect.top + 10:
            player.take_damage()

    if pygame.sprite.spritecollideany(player, spikes):
        player.take_damage()
    fond = pygame.image.load("fond.png")
    # Trampoline Bounce power
    for trampoline in trampolines:
        if pygame.sprite.collide_rect(player, trampoline) and player.velocity_y > 0:
            player.velocity_y = -JUMP_STRENGTH - 12  
    screen.blit(fond,(0,0))
    all_sprites.draw(screen)

    # Display
    font = pygame.font.SysFont(None, 36)
    health_text = font.render(f"Health: {player.health}", True, (0, 0, 0))
    screen.blit(health_text, (10, 10))
    pygame.display.flip()
    clock.tick(60)

    # End the game if dead
    if player.health <= 0:
        print("Game Over!")
        running = False

pygame.quit()
sys.exit()
