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
BROWN = (139,69,19)
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
        self.image.fill(BROWN)
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
        self.image.fill(BLUE)
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

# Create Player, Goomba, Key and Door
player = Player()
goomba = Goomba()
key = Key(380, 200)
door = Door(1550, SCREEN_HEIGHT - DOOR_HEIGHT)

platforms = pygame.sprite.Group()
spikes = pygame.sprite.Group()
trampolines = pygame.sprite.Group()

# Creation des Platforms
platform1 = Platform(0, 900, PLATFORM_WIDTH, PLATFORM_HEIGHT)#
platform2 = Platform(0, 800, PLATFORM_WIDTH, PLATFORM_HEIGHT)#
platform3 = Platform(200, 800, PLATFORM_WIDTH, PLATFORM_HEIGHT)#
platform4 = Platform(500, 825, PLATFORM_WIDTH, PLATFORM_HEIGHT)#
platform5 = Platform(800, 800, PLATFORM_WIDTH, PLATFORM_HEIGHT)#
platform6 = Platform(1200, 700, PLATFORM_WIDTH, PLATFORM_HEIGHT)#
platform7 = Platform(1400, 700, PLATFORM_WIDTH, PLATFORM_HEIGHT)#
platform8 = Platform(1500, 600, PLATFORM_WIDTH, PLATFORM_HEIGHT)#
platform9 = Platform(1500, 500, PLATFORM_WIDTH, PLATFORM_HEIGHT)#
platform10 = Platform(1400, 400, PLATFORM_WIDTH, PLATFORM_HEIGHT)#
platform11 = Platform(1000,300, PLATFORM_WIDTH, PLATFORM_HEIGHT)#
platform12 = Platform(1200, 400, PLATFORM_WIDTH, PLATFORM_HEIGHT)#
platform13 = Platform(1000, 800, PLATFORM_WIDTH, PLATFORM_HEIGHT)#
platform14 = Platform(600, 150, PLATFORM_WIDTH, PLATFORM_HEIGHT)#
platform15 = Platform(400, 250, PLATFORM_WIDTH, PLATFORM_HEIGHT)#
platform16 = Platform(200, 250, PLATFORM_WIDTH, PLATFORM_HEIGHT)#

platforms.add(platform1, platform2, platform3, platform4, platform5, platform6, platform7, platform8, platform9, platform10, platform11, platform12, platform13, platform14, platform15, platform16)

# Creation des Spikes
spike1 = Spike(500, 795)#
spike2 = Spike(670, 795)#
spike3 = Spike(1000, 770)#
spike4 = Spike(970, 770)#
spike5 = Spike(1030, 770)#
spike6 = Spike(1410, 370)#
spike7 = Spike(1150, 970)
spike8 = Spike(1170, 770)#
spike9 = Spike(1320, 670)#
spike10 = Spike(1350, 670)#
spike11 = Spike(1380, 670)#
spike12 = Spike(570, 220)#
spike13 = Spike(1380, 370)#
spike14 = Spike(1350, 370)#
spike15 = Spike(1180, 970 )#

spikes.add(spike1, spike2, spike3, spike4, spike5, spike6, spike7, spike8, spike9, spike10, spike11, spike12, spike13, spike14, spike15)

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

# Changement de scene ( qui marche pas ) 
def create_new_scene():
    global scene_changed
    all_sprites.empty()
    platforms.empty()
    spikes.empty()
    trampolines.empty()

    # Réinitialisation de la position du joueur et du Goomba
    player.rect.x = SCREEN_WIDTH // 2
    player.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT
    goomba.rect.x = 50
    goomba.rect.y = 50
    goomba.velocity_y = 0
    platform1 = Platform(200, 1000, PLATFORM_WIDTH, PLATFORM_HEIGHT)    # A CHANGER !! 
    platform2 = Platform(400, 800, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platform3 = Platform(600, 600, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platform4 = Platform(800, 400, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platform5 = Platform(1000, 200, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platforms.add(platform1, platform2, platform3, platform4, platform5)
    new_spike1 = Spike(250, 970)
    new_spike2 = Spike(450, 770)
    new_spike3 = Spike(650, 570)
    spikes.add(new_spike1, new_spike2, new_spike3)
    new_trampoline1 = Trampoline(500, 300)
    trampolines.add(new_trampoline1)
    all_sprites.add(player, goomba, platforms, spikes, trampolines)
    scene_changed = True


# Game Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    player.update(platforms)
    goomba.update(platforms)
    player.collect_key(key if not scene_changed else None)
    if door.unlock(player) and not scene_changed:
        create_new_scene()
    door.check_locked(player)
    if pygame.sprite.collide_rect(player, goomba) and goomba.alive:
        if player.rect.bottom <= goomba.rect.top + 50 and player.velocity_y > 0:
            goomba.die()
            player.velocity_y = -JUMP_STRENGTH
        elif player.rect.bottom > goomba.rect.top + 10:
            player.take_damage()

    if pygame.sprite.spritecollideany(player, spikes):
        player.take_damage()
    
    # Trampoline Bounce power
    for trampoline in trampolines:
        if pygame.sprite.collide_rect(player, trampoline) and player.velocity_y > 0:
            player.velocity_y = -JUMP_STRENGTH - 12  
    screen.fill(LIGHT_GRAY)
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
