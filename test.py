import pygame
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
GOOMBA_WIDTH = 40
GOOMBA_HEIGHT = 40
PLATFORM_WIDTH = 200
PLATFORM_HEIGHT = 20
KEY_WIDTH = 30
KEY_HEIGHT = 30
DOOR_WIDTH = 50
DOOR_HEIGHT = 100
WHITE = (255,255,255)
BLUE = (0,0,255)
RED = (255,0,0)
BROWN = (139,69,19)
YELLOW = (255,255,0)
GRAY = (70,64,64)
LIGHT_GRAY = (179,179,179)
GRAVITY = 0.5
JUMP_STRENGTH = 11
PLAYER_SPEED = 5
GOOMBA_SPEED = 3

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Moveable Character with Key and Door")

clock = pygame.time.Clock()

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

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

    def handle_platform_collisions(self, platforms):
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0 and self.rect.bottom <= platform.rect.top + 50:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True

    def take_damage(self):
        if self.health > 0:
            self.health -= 1

    def collect_key(self, key):
        if pygame.sprite.collide_rect(self, key):
            self.has_key = True
            key.kill()

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

    def reset(self):
        self.alive = True
        self.rect.x = 50
        self.rect.y = 50
        self.direction = 1
        self.velocity_y = 0
        all_sprites.add(self)

class Key(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((KEY_WIDTH, KEY_HEIGHT))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((DOOR_WIDTH, DOOR_HEIGHT))
        self.image.fill(GRAY)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.locked = True

    def unlock(self, player):
        if self.locked and pygame.sprite.collide_rect(self, player) and player.has_key:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_e]:
                self.locked = False
                print("Door unlocked!")
                self.image.fill((0, 255, 0))
                return True
        return False

    def check_locked(self, player):
        if self.locked and pygame.sprite.collide_rect(self, player):
            if player.rect.right > self.rect.left:
                player.rect.right = self.rect.left

player = Player()
goomba = Goomba()
key = Key(350, 250)
door = Door(700, SCREEN_HEIGHT - DOOR_HEIGHT)

platforms = pygame.sprite.Group()
platform1 = Platform(300, 400, PLATFORM_WIDTH, PLATFORM_HEIGHT)
platform2 = Platform(400, 300, PLATFORM_WIDTH, PLATFORM_HEIGHT)
platform3 = Platform(600, 500, PLATFORM_WIDTH, PLATFORM_HEIGHT)
platforms.add(platform1, platform2, platform3)

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(goomba)
all_sprites.add(key)
all_sprites.add(door)
all_sprites.add(platform1, platform2, platform3)

running = True
scene_changed = False
new_key = None
new_door = None

def create_new_scene():
    global scene_changed, new_key, new_door
    all_sprites.empty()
    platforms.empty()
    player.rect.x = SCREEN_WIDTH // 2
    player.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT
    goomba.reset()
    platform1 = Platform(350, 375, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platform2 = Platform(500, 275, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platform3 = Platform(600, 480, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platform4 = Platform(700, 220, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platform5 = Platform(200, 200, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platform_roof = Platform(700, 110, PLATFORM_WIDTH, 20)
    new_key = Key(275, 150)
    new_door = Door(725, 125)
    platforms.add(platform1, platform2, platform3, platform4, platform5, platform_roof)
    all_sprites.add(player, platform1, platform2, platform3, platform4, platform5, platform_roof, new_key, new_door)

    scene_changed = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.update(platforms)
    goomba.update(platforms)
    player.collect_key(new_key if scene_changed else key)
    if (new_door if scene_changed else door).unlock(player) and not scene_changed:
        create_new_scene()
    (new_door if scene_changed else door).check_locked(player)

    if pygame.sprite.collide_rect(player, goomba) and goomba.alive:
        if player.rect.bottom <= goomba.rect.top + 50 and player.velocity_y > 0:
            goomba.die()
            player.velocity_y = -JUMP_STRENGTH
        elif player.rect.bottom > goomba.rect.top + 10:
            player.take_damage()

    screen.fill(LIGHT_GRAY)
    all_sprites.draw(screen)
    font = pygame.font.SysFont(None, 36)
    health_text = font.render(f"Health: {player.health}", True, (0, 0, 0))
    screen.blit(health_text, (10, 10))
    pygame.display.flip()
    clock.tick(60)

    if player.health <= 0:
        print("Game Over!")
        running = False

pygame.quit()
sys.exit()
