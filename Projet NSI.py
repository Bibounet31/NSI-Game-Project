import pygame
import sys

# Initialize pygame
pygame.init()

# Constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GRAVITY = 0.5
JUMP_STRENGTH = 10

# Display the Moutons
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2000 Moutons")

# pour les frames rates
clock = pygame.time.Clock()

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

    def update(self):
        keys = pygame.key.get_pressed()

        # Movements
        if keys[pygame.K_q]:
            self.rect.x -= 5  # Move left
        if keys[pygame.K_d]:
            self.rect.x += 5  # Move right

        # Jump.exe
        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.velocity_y = -JUMP_STRENGTH
            self.is_jumping = True

        # Apply Mottier difficulty(gravitÃ©)
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        # No screen escaping boi
        if self.rect.y >= SCREEN_HEIGHT - PLAYER_HEIGHT:
            self.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT
            self.is_jumping = False
            self.velocity_y = 0

# Create player
player = Player()

# Sprite group
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update sprites
    all_sprites.update()

    # Draw everything
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # Update the display
    pygame.display.flip()

    # Frame rate
    clock.tick(60)

# Quit pygame
pygame.quit()
sys.exit()
