import pygame
import sys

# Initialisztion pygame
pygame.init()

# Constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
GOOMBA_WIDTH = 40
GOOMBA_HEIGHT = 40
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255,0,0)
GRAVITY = 0.5
JUMP_STRENGTH = 10
PLAYER_SPEED = 5
GOOMBA_SPEED = 3

# Displaying
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
        self.health = 3 # Player starts with 3 Health Points
        
    def update(self):
        keys = pygame.key.get_pressed()

        # Mouvements
        if keys[pygame.K_q]:
            self.rect.x -= 5  # Move left
        if keys[pygame.K_d]:
            self.rect.x += 5  # Move right

        # Jump.exe
        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.velocity_y = -JUMP_STRENGTH
            self.is_jumping = True

        # Apply Gravity
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y
        
        if self.rect.x < 0 :
            self.rect.x = 0
        if self.rect.x > SCREEN_WIDTH - PLAYER_WIDTH :
            self.rect.x = SCREEN_WIDTH - PLAYER_WIDTH

        # No screen escaping ( marche pas )
        if self.rect.y >= SCREEN_HEIGHT - PLAYER_HEIGHT:
            self.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT
            self.is_jumping = False
            self.velocity_y = 0

    def take_damage(self):
        if self.health > 0 :
            self.health -= 1
            
# Class Goomba
class Goomba(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((GOOMBA_WIDTH,GOOMBA_HEIGHT))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - GOOMBA_HEIGHT
        self.direction = 1 # start by moving to the right
        self.alive = True # Goomba débute en vie ( c'est un peu mieux qu'il soit vivant a la base)
        
    def update(self):
        if self.alive:
            self.rect.x += self.direction*GOOMBA_SPEED # retourne le goomba si mange un mur ( marche pas )
        if self.rect.right >= SCREEN_WIDTH or self.rect.left <= 0:
            self.direction *= -1 # change la direction ( marche pas )
            
    def die(self):
        self.alive = False
        self.kill() # delete goomba when dead ( ne sait pas si sa marche )
        
# Create player and Goomba
player = Player()
goomba = Goomba()

# Sprite group
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(goomba)

# Game
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update sprites
    all_sprites.update()
    
    if pygame.sprite.collide_rect(player,goomba) and goomba.alive :
        if player.rect.bottom <= goomba.rect.top + 10 and player.velocity_y > 0 :
            goomba.die() # A mort le goomba
            player.velocity_y = -JUMP_STRENGTH # player rebondit surle goomba ( ne sait pas si sa marche )
        elif  player.rect.bottom > goomba.rect.top + 10 :
            player.take_damage()
            
    # Draw everything
    screen.fill(WHITE)
    all_sprites.draw(screen)
    
    # Update the display
    pygame.display.flip()

    # Frame rate
    clock.tick(60)

    # Game Over
    if player.health <= 0 :
        print("Game Over !")
        running = False

# Quit pygame
pygame.quit()
sys.exit()
