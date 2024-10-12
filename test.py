import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
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
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)
GRAY = (169, 169, 169)
GRAVITY = 0.5
JUMP_STRENGTH = 11
PLAYER_SPEED = 5
GOOMBA_SPEED = 3

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Moveable Character with Key and Door")

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
        self.health = 3  # Player starts with 3 health points
        self.on_ground = False
        self.has_key = False  # Player starts without the key

    def update(self, platforms):
        keys = pygame.key.get_pressed()

        # Mouvements
        if keys[pygame.K_q] and self.rect.x > 0:
            self.rect.x -= PLAYER_SPEED  # Move left
        if keys[pygame.K_d] and self.rect.x < SCREEN_WIDTH - PLAYER_WIDTH:
            self.rect.x += PLAYER_SPEED  # Move right

        # Jump.exe
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = -JUMP_STRENGTH
            self.is_jumping = True
            self.on_ground = False

        # Apply Mottier difficulty
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        # collisions with platforms
        self.handle_platform_collisions(platforms)

        # No screen escaping
        if self.rect.y >= SCREEN_HEIGHT - PLAYER_HEIGHT:
            self.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT
            self.on_ground = True
            self.velocity_y = 0

    def handle_platform_collisions(self, platforms):
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # Player is falling and hits the platform
                if self.velocity_y > 0 and self.rect.bottom <= platform.rect.top + 50:
                    self.rect.bottom = platform.rect.top  
                    self.velocity_y = 0  # Stop falling
                    self.on_ground = True  # Player is now standing on the platform

    def take_damage(self):
        if self.health > 0:
            self.health -= 1

    def collect_key(self, key):
        if pygame.sprite.collide_rect(self, key):
            self.has_key = True
            key.kill()  

# Goomba class
class Goomba(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((GOOMBA_WIDTH, GOOMBA_HEIGHT))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - GOOMBA_HEIGHT
        self.direction = 1  # Start moving right
        self.alive = True   # Goomba starts alive
        self.velocity_y = 0

    def update(self, platforms):
        if self.alive:
            # Move left or right
            self.rect.x += self.direction * GOOMBA_SPEED

            # Reverse direction if it hits the edge of the screen
            if self.rect.right >= SCREEN_WIDTH or self.rect.left <= 0:
                self.direction *= -1  # Change direction

            # Apply Mottier difficulty
            self.velocity_y += GRAVITY
            self.rect.y += self.velocity_y

            # Check for collision with platforms
            for platform in platforms:
                if self.rect.colliderect(platform.rect):
                    # If Goomba is falling and hits platform
                    if self.rect.bottom <= platform.rect.top + 50:
                        self.rect.bottom = platform.rect.top
                        self.velocity_y = 0

            # Prevent Goomba from falling off the screen
            if self.rect.y >= SCREEN_HEIGHT - GOOMBA_HEIGHT:
                self.rect.y = SCREEN_HEIGHT - GOOMBA_HEIGHT
                self.velocity_y = 0

    def die(self):
        self.alive = False
        self.kill()  # kill goomba

# Key class
class Key(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((KEY_WIDTH, KEY_HEIGHT))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Door class
class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((DOOR_WIDTH, DOOR_HEIGHT))
        self.image.fill(GRAY)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.locked = True  # Door starts as locked

    def unlock(self, player):
        # If player is colliding with the door and has the key, they can press 'E' to unlock
        if self.locked and pygame.sprite.collide_rect(self, player) and player.has_key:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_e]:  # Player presses "E" to unlock the door
                self.locked = False
                print("Door unlocked!")  # Additional actions can be added here
                self.image.fill((0, 255, 0))  # Change door color to green (open)

    def check_locked(self, player):
        # Prevent player from going through the door if it's locked
        if self.locked and pygame.sprite.collide_rect(self, player):
            # Push the player back so they can't pass through
            if player.rect.right > self.rect.left:
                player.rect.right = self.rect.left

# Create player, Goomba, key, and door
player = Player()
goomba = Goomba()
key = Key(350, 250)
door = Door(700, SCREEN_HEIGHT - DOOR_HEIGHT)

# platforms
platforms = pygame.sprite.Group()
platform1 = Platform(300, 400, PLATFORM_WIDTH, PLATFORM_HEIGHT)
platform2 = Platform(400, 300, PLATFORM_WIDTH, PLATFORM_HEIGHT)
platform3 = Platform(600, 500, PLATFORM_WIDTH, PLATFORM_HEIGHT)
platforms.add(platform1, platform2, platform3)

# Sprite group
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(goomba)
all_sprites.add(key)
all_sprites.add(door)
all_sprites.add(platform1, platform2, platform3)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.update(platforms)
    goomba.update(platforms)

    player.collect_key(key)

    door.unlock(player)

    door.check_locked(player)

    # Check for collision between player and Goomba
    if pygame.sprite.collide_rect(player, goomba) and goomba.alive:
        # (stomp)
        if player.rect.bottom <= goomba.rect.top + 50 and player.velocity_y > 0:
            goomba.die()  # Goomba dies if player lands on its head
            player.velocity_y = -JUMP_STRENGTH  # Player bounces up after stomping

        elif player.rect.bottom > goomba.rect.top + 10:
            player.take_damage()

    # Draw everything
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # Display player's health
    font = pygame.font.SysFont(None, 36)
    health_text = font.render(f"Health: {player.health}", True, (0, 0, 0))
    screen.blit(health_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Frame rate
    clock.tick(60)

    # End the game if player health is 0
    if player.health <= 0:
        print("Game Over!")
        running = False

# Quit pygame
pygame.quit()
sys.exit()


