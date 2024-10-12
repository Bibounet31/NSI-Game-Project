import pygame
import sys

# Initialize pygame
pygame.init()

# Constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
GOOMBA_WIDTH = 40
GOOMBA_HEIGHT = 40
PLATFORM_WIDTH = 200
PLATFORM_HEIGHT = 20
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BROWN = (139, 69, 19)
GRAVITY = 0.5
JUMP_STRENGTH = 11
PLAYER_SPEED = 5
GOOMBA_SPEED = 3

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("mario.wish")

# Clock for FPS
clock = pygame.time.Clock()

# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Player class
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
        self.health = 3  
        self.on_ground = False

    def update(self, platforms):
        keys = pygame.key.get_pressed()

        # Movement controls
        if keys[pygame.K_q]:
            self.rect.x -= PLAYER_SPEED  # left
        if keys[pygame.K_d]:
            self.rect.x += PLAYER_SPEED  # right

        # Jump.exe
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = -JUMP_STRENGTH
            self.is_jumping = True
            self.on_ground = False

        # Mottier difficulty
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        # collisions with platforms
        self.handle_platform_collisions(platforms)

        # Prevent falling off the screen
        if self.rect.y >= SCREEN_HEIGHT - PLAYER_HEIGHT:
            self.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT
            self.on_ground = True
            self.velocity_y = 0

    def handle_platform_collisions(self, platforms):
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0 and self.rect.bottom <= platform.rect.top + 11:
                    self.rect.bottom = platform.rect.top  
                    self.velocity_y = 0 
                    self.on_ground = True  

    def take_damage(self):
        if self.health > 0:
            self.health -= 1

# Goomba class
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
            # Move left or right
            self.rect.x += self.direction * GOOMBA_SPEED

            if self.rect.right >= SCREEN_WIDTH or self.rect.left <= 0:
                self.direction *= -1  # Change direction

            self.velocity_y += GRAVITY
            self.rect.y += self.velocity_y

            # Check for collision with platforms
            for platform in platforms:
                if self.rect.colliderect(platform.rect):
                    # If Goomba is falling and its feet hit the platform
                    if self.rect.bottom <= platform.rect.top + 10:
                        self.rect.bottom = platform.rect.top
                        self.velocity_y = 0

            # Prevent Goomba from falling off the screen
            if self.rect.y >= SCREEN_HEIGHT - GOOMBA_HEIGHT:
                self.rect.y = SCREEN_HEIGHT - GOOMBA_HEIGHT
                self.velocity_y = 0

    def die(self):
        self.alive = False
        self.kill()  # kill yourself

# Create player and Goomba
player = Player()
goomba = Goomba()

# Create platforms
platforms = pygame.sprite.Group()
platform1 = Platform(100, 400, PLATFORM_WIDTH, PLATFORM_HEIGHT)
platform2 = Platform(400, 300, PLATFORM_WIDTH, PLATFORM_HEIGHT)
platform3 = Platform(600, 500, PLATFORM_WIDTH, PLATFORM_HEIGHT)
platforms.add(platform1, platform2, platform3)

# Sprite group
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(goomba)
all_sprites.add(platform1, platform2, platform3)

# Game
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    player.update(platforms)
    goomba.update(platforms)

    if pygame.sprite.collide_rect(player, goomba) and goomba.alive:
        # stomp
        if player.rect.bottom <= goomba.rect.top + 10 and player.velocity_y > 0:
            goomba.die()  # A mort le goomba
            player.velocity_y = -JUMP_STRENGTH  # Player bounces up after stomping

        elif player.rect.bottom > goomba.rect.top + 10:
            player.take_damage()

    # Draw
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # Display player's health
    font = pygame.font.SysFont(None, 36)
    health_text = font.render(f"Health: {player.health}", True, (0, 0, 0))
    screen.blit(health_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # FPS
    clock.tick(60)

    # End the game if player health is 0
    if player.health <= 0:
        print("Game Over!")
        running = False

# Quit pygame
pygame.quit()
sys.exit()
