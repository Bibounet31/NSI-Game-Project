import pygame
import sys
import os

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
BROWN = (100,60,0)
YELLOW = (255,255,0)
LIGHT_GRAY = (169,169,169)
GRAY = (70,64,64)
BLACK = (0,0,0)
# Physique du jeu
GRAVITY = 0.5
JUMP_STRENGTH = 11
PLAYER_SPEED = 5
GOOMBA_SPEED = 3

# ALLER MUSIQUE
chemin_fichier = os.path.dirname(__file__) # Obtient le chemin du fichier actuel
music_path = os.path.join(chemin_fichier, "musique.mp3") # Définit le chemin de la musique
pygame.mixer.music.load(music_path) # Charge la musique
pygame.mixer.music.play(-1) # Joue la musique en boucle

# interface graphique
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # Crée la fenêtre de jeu
pygame.display.set_caption("The Very Good Game") # Définit le titre de la fenêtre

# Pour les images par secondes
clock = pygame.time.Clock() # initialisation d'une clock pour gérer les images par secondes

# Menu d'avant début du jeu
def main_menu():
    play_button_rect = pygame.Rect(700, 450, 200, 100)  # Crée le bouton "Play" sous forme de rectangle
    while True:
        path = os.path.join(chemin_fichier, "TheVeryGoodGame.png") # Chemin pour l'image de fond
        fond = pygame.image.load(path) # Charge l'image de fond
        screen.blit(fond, (0,0)) # Affiche l'image de fond sur l'écran
        pygame.draw.rect(screen, BLUE, play_button_rect) # Dessine le bouton "Play" en bleu
        font = pygame.font.Font(None, 74) # Définit la police pour le texte "Play"
        text = font.render("Play", True, WHITE) # Crée le texte "Play" en blanc
        screen.blit(text, (play_button_rect.x + 50, play_button_rect.y + 25))  # Positionne le texte "Play" au centre du bouton

        for event in pygame.event.get(): # Boucle d'événements
            if event.type == pygame.QUIT: # Vérifie si l'utilisateur ferme la fenêtre
                pygame.quit() # Quitte Pygame
                sys.exit() # Ferme le programme
            elif event.type == pygame.MOUSEBUTTONDOWN and play_button_rect.collidepoint(event.pos): # Si le bouton "Play" est cliqué
                return  # Lance le jeu

        pygame.display.flip() # Met à jour l'affichage
        clock.tick(60) # Limite le jeu à 60 images par seconde

# Class Platforme
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__() # pour pouvoir acceder aux methodes et proprietes de cette classe
        self.image = pygame.Surface((width, height)) # Crée une surface pour la plateforme
        self.image.fill(BROWN) # Remplit la surface avec la couleur marron
        self.rect = self.image.get_rect() # Obtient le rectangle de la surface
        self.rect.x = x # Définit la position x de la plateforme
        self.rect.y = y # Définit la position y de la plateforme

# Class Trampoline
class Trampoline(Platform): 
    def __init__(self, x, y):
        super().__init__(x, y, PLATFORM_WIDTH, TRAMPOLINE_HEIGHT)  # Utilise la largeur de la plateforme et la hauteur du trampoline
        self.image.fill(BLUE)  # Remplit le trampoline avec la couleur bleue

# Class Spike        
class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__() # pour pouvoir acceder aux methodes et proprietes de cette classe
        self.image = pygame.Surface((SPIKE_WIDTH, SPIKE_HEIGHT), pygame.SRCALPHA) # Crée une surface pour le spike
        pygame.draw.polygon(self.image, BLACK, [(0, SPIKE_HEIGHT), (SPIKE_WIDTH // 2, 0), (SPIKE_WIDTH, SPIKE_HEIGHT)]) # Dessine un triangle noir
        self.rect = self.image.get_rect() # Obtient le rectangle de la surface
        self.rect.x = x # Définit la position x du spike
        self.rect.y = y # Définit la position y du 


# Class Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() # pour pouvoir acceder aux methodes et proprietes de cette classe
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT)) # Crée une surface pour le joueur
        path = os.path.join(chemin_fichier, "MaRiO.png") # Chemin de l'image du joueur
        self.image = pygame.image.load(path) # Charge l'image du joueur
        self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT)) # Redimensionne l'image du joueur
        self.rect = self.image.get_rect() # Obtient le rectangle de la surface
        self.rect.x = SCREEN_WIDTH // 2 # Positionne le joueur au centre horizontalement
        self.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT # Positionne le joueur en bas de l'écran
        self.velocity_y = 0 # Initialisation de la vitesse verticale
        self.is_jumping = False # Indicateur de saut
        self.health = 1 # Points de vie du joueur
        self.on_ground = False # Indicateur de contact avec le sol
        self.has_key = False # Indique si le joueur a la clé

    # Update mouvements Player selon la situation
    def update(self, platforms):
        keys = pygame.key.get_pressed() # obtention de l'état des touches appuyées
        if keys[pygame.K_q] and self.rect.x > 0: # Aller a gauche
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_d] and self.rect.x < SCREEN_WIDTH - PLAYER_WIDTH: # aller a droite
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_SPACE] and self.on_ground: # sauter
            self.velocity_y = -JUMP_STRENGTH
            self.is_jumping = True
            self.on_ground = False
        self.velocity_y += GRAVITY # ajoute la gravité a la vitesse verticale
        self.rect.y += self.velocity_y # position y modifier on fontion de vitesse verticale
        self.handle_platform_collisions(platforms) # peut tenir sur la platforme
        if self.rect.y >= SCREEN_HEIGHT - PLAYER_HEIGHT: # si le joueur touche le bas de l'écran
            self.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT # le joueur est placé en bas de l'écran
            self.on_ground = True # il touche le sol
            self.velocity_y = 0 # s'arrete de tomber

    # collisions des platformes
    def handle_platform_collisions(self, platforms):
        self.on_ground = False  # réinitialise l'état du sol
        for platform in platforms: # pour chaque platforme
            if self.rect.colliderect(platform.rect): # check la collision
                if self.velocity_y > 0 and self.rect.bottom <= platform.rect.top + 50: # si le joueur tombe sur la platforme
                    if isinstance(platform, Trampoline): # si c'est un trampoline
                        self.velocity_y = -JUMP_STRENGTH - 20  # faire un saut puissant
                    else:
                        self.rect.bottom = platform.rect.top # sinon arrete la chute et le joueur tient sur la platforme
                        self.velocity_y = 0
                        self.on_ground = True

    # Player peut mourir
    def take_damage(self):
        if self.health > 0: # si joueur a plus de 1 pv
            self.health -= 1 # joueur perd 1 pv

    # Player peut récupérer la clé
    def collect_key(self, key):
        if key is not None and pygame.sprite.collide_rect(self, key): # si la clé n'est pas none, et que le joueur touche la clé
            self.has_key = True # le joueur a récupéré la clé
            key.kill() # fait disparaitre la clé une fois récupérée

# Class Goomba
class Goomba(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() # pour pouvoir acceder aux methodes et proprietes de cette classe
        self.image = pygame.Surface((GOOMBA_WIDTH, GOOMBA_HEIGHT)) # créer une surface pour le goomba
        path = os.path.join(chemin_fichier, "goomba.png") # chemin de l'image du goomba
        self.image = pygame.image.load(path) # charge l'image du goomba
        self.image= pygame.transform.scale(self.image,(PLAYER_WIDTH, PLAYER_HEIGHT)) # règle la taile de l'image pour match celle du goomba
        self.rect = self.image.get_rect() # get_rect() crée une image rectangulaire
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - GOOMBA_HEIGHT
        self.direction = 1 # démarre en allant a droite
        self.alive = True # goomba commence en vie ( et oui )
        self.velocity_y = 0 #  initialisation de sa vitesse verticale

    # Update mouvements Goomba selon la situation
    def update(self, platforms):
        if self.alive: # si goomba en vie
            self.rect.x += self.direction * GOOMBA_SPEED # faire avancer le goomba vers la droite
            if self.rect.right >= SCREEN_WIDTH or self.rect.left <= 0:  # si le goomba tape le mur de l'interface graphique 
                self.direction *= -1 # il fait demi tour
            self.velocity_y += GRAVITY # ajout de la gravité a sa vitesse verticale
            self.rect.y += self.velocity_y # on change son y en fonction de la vitesse verticale
            for platform in platforms: # pour chaque platforme
                if self.rect.colliderect(platform.rect): # si goomba collison avec platforme
                    if self.rect.bottom <= platform.rect.top + 50: # goomba retombe sur platforme
                        self.rect.bottom = platform.rect.top # arret de la chute
                        self.velocity_y = 0 # réinitialisation de sa vitesse verticale 
            if self.rect.y >= SCREEN_HEIGHT - GOOMBA_HEIGHT: # empeche le goomba de tomber hors de l'écran
                self.rect.y = SCREEN_HEIGHT - GOOMBA_HEIGHT
                self.velocity_y = 0

    # Tuer
    def die(self):
        self.alive = False # faire mourir le sprite 
        self.kill() # le fait disparaitre de l'interface

# Class Clé
class Key(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__() # pour pouvoir acceder aux methodes et proprietes de cette classe
        self.image = pygame.Surface((KEY_WIDTH, KEY_HEIGHT)) # crée une surface pour la clé
        self.image.fill(YELLOW) # une clé jaune
        self.rect = self.image.get_rect() # une clé rectangulaire 
        self.rect.x = x
        self.rect.y = y
    def key_alive(self):
        self.alive = True # la clé est présente sur l'interface


# Class Porte
class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__() # pour pouvoir acceder aux methodes et proprietes de cette classe
        self.image = pygame.Surface((DOOR_WIDTH, DOOR_HEIGHT)) # crée une surface pour la porte
        self.image.fill(GRAY) # une porte grise
        self.rect = self.image.get_rect() # une porte rectangulaire
        self.rect.x = x
        self.rect.y = y
        self.locked = True # la porte est fermé a sa création

    # ouverture de la porte fermée
    def unlock(self, player):
        if self.locked and pygame.sprite.collide_rect(self, player) and player.has_key: # si la porte est ferméé et le joueur colle la porte et possede la clé
            keys = pygame.key.get_pressed() # obtentions de l'état des touches appuyées
            if keys[pygame.K_e]: # si la touche "e" est appuyée
                self.locked = False # sésame ouvre toi
                return True 
        return False # et sinon ba elle s'ouvre pas

    # collisions des portes
    def check_locked(self, player):
        if self.locked and pygame.sprite.collide_rect(self, player): # si la porte est fermé et le joueur colle la porte
            if player.rect.right > self.rect.left: 
                player.rect.right = self.rect.left # le joueur ne peut pas traverser la porte et est bloqué

# Creation Player, Goomba, Key and Door
player = Player()
goomba = Goomba()
key = Key(380, 200)
door = Door(1550, SCREEN_HEIGHT - DOOR_HEIGHT)

# Groupes de sprites
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

# ajout des platformes dans le Sprite group "Platforms"
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
spike15 = Spike(1180, 970)
spike16 = Spike(0, 770)
spike17 = Spike(30, 770)
spike18 = Spike(0, 870)
spike19 = Spike(970, 570)

# ajout des spikes dans le Sprite group "Spikes"
spikes.add(spike1, spike2, spike3, spike4, spike5, spike6, spike7, spike8, spike9, spike10, spike11, spike12, spike13, spike14, spike15, spike16, spike17, spike18, spike19)

# Creation trampolines + add to sprites
trampoline1 = Trampoline(800, 600)

# ajout du trampoline dans le Sprite group "tramplines"
trampolines.add(trampoline1)

# création d'un Sprite group global
all_sprites = pygame.sprite.Group()

# rassemblement des sprites dans un seul groupe pour les dessiners sur l'écran
all_sprites.add(player,goomba,key,door,platforms,spikes,trampolines)

running = True # le jeu est actif
scene_changed = 0 # aucun changement de scene pour le moment

# Changement de scene 1
def create_new_scene():
    global scene_changed
    global key2
    global door2
    
    # réinitialisations des sprites apres changement de scene
    all_sprites.empty()
    platforms.empty()
    spikes.empty()
    trampolines.empty()

    # le joueur a utilisé sa clé sur la porte précédente
    player.has_key = False

    # réinitialisation des placements des sprites
    player.rect.x = 250
    player.rect.y = 990
    goomba.rect.x = 50
    goomba.rect.y = 50
    goomba.velocity_y = 0
    goomba.alive = True

    # configuration de la scene 2
    # création des platformes
    # platforme_exemple = Platform( x , y , PLATFORM_WIDTH, PLATFORM_HEIGHT)
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

    # ajout des platformes dans le Sprite group "platforms"
    platforms.add(platform1, platform2, platform3, platform4, platform5, platform6, platform7,platform8, platform10, platform11, platform12, platform13, platform14, platform15, platform16)

    # création des Spikes
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

    # ajout des spikes dans le Sprite group "spikes"
    spikes.add(new_spike1, new_spike2, new_spike3, new_spike4, new_spike5, new_spike6, new_spike7, new_spike8, new_spike9, new_spike10, new_spike11, new_spike12, new_spike13, new_spike14, new_spike15, new_spike16, new_spike17, new_spike18, new_spike19, new_spike20, new_spike21, new_spike22, new_spike23, new_spike24, new_spike25, new_spike26, new_spike27, new_spike28, new_spike29, new_spike30, new_spike31, new_spike32, new_spike33, new_spike34, new_spike35, new_spike36, new_spike37, new_spike38, new_spike39, new_spike40, new_spike41, new_spike42, new_spike43, new_spike44, new_spike45, new_spike46, new_spike47, new_spike48, new_spike49, new_spike50, new_spike51, new_spike52, new_spike53, new_spike54)

    # création du trampoline
    new_trampoline1 = Trampoline(1400,900)

    # ajout du trampoline dans le Sprite group "trampolines"
    trampolines.add(new_trampoline1)

    # création de clé2 et porte2
    key2 = Key(680,870)
    door2 = Door(1550,300)
    
    # ajout des sprites dans le group global
    all_sprites.add(player, goomba, platforms, spikes, trampolines)
    all_sprites.add(key2)
    all_sprites.add(door2)
    scene_changed = 1 # la scene a changé une premiere fois
def create_new_scene2():
    global scene_changed
    global door3
    global key3
    all_sprites.empty()
    platforms.empty()
    spikes.empty()
    trampolines.empty()
    player.has_key = False
    
    # réinitialisation des placements des sprites
    player.rect.x = 50
    player.rect.y = 970
    goomba.rect.x = 0
    goomba.rect.y = 590
    goomba.alive = True

    # configuration de la scene 3
    
    platform1 = Platform(1400,900,PLATFORM_WIDTH,PLATFORM_HEIGHT)
    platform2 = Platform(1150,800,PLATFORM_WIDTH,PLATFORM_HEIGHT)
    platform3 = Platform(950,800,PLATFORM_WIDTH,PLATFORM_HEIGHT)
    platform4 = Platform(550,800,PLATFORM_WIDTH,PLATFORM_HEIGHT)
    platform5 = Platform(400,800,PLATFORM_WIDTH,PLATFORM_HEIGHT)
    platform6 = Platform(200,800,PLATFORM_WIDTH,PLATFORM_HEIGHT)
    platform7 = Platform(0,820,PLATFORM_WIDTH,PLATFORM_HEIGHT)
    platform8 = Platform(0,500,PLATFORM_WIDTH,PLATFORM_HEIGHT)
    platform9 = Platform(200,500,PLATFORM_WIDTH,PLATFORM_HEIGHT)
    platform10 = Platform(500,550,PLATFORM_WIDTH,PLATFORM_HEIGHT)
    platform11 = Platform(800,500,PLATFORM_WIDTH,PLATFORM_HEIGHT)
    platform12 = Platform(1000,500,PLATFORM_WIDTH,PLATFORM_HEIGHT)
    platform13 = Platform(1200,500,PLATFORM_WIDTH,PLATFORM_HEIGHT)
    platform14 = Platform(1400,500,PLATFORM_WIDTH,PLATFORM_HEIGHT)
    platform15 = Platform(1400,400,PLATFORM_WIDTH,PLATFORM_HEIGHT)
    platform16 = Platform(1200,300,PLATFORM_WIDTH,PLATFORM_HEIGHT)
    platform17 = Platform(1000,200,PLATFORM_WIDTH,PLATFORM_HEIGHT)
    platform18 = Platform(650,200,PLATFORM_WIDTH,PLATFORM_HEIGHT)
    platform19 = Platform(300,200,PLATFORM_WIDTH,PLATFORM_HEIGHT)
    platform20 = Platform(100,200,PLATFORM_WIDTH,PLATFORM_HEIGHT)
    platform21 = Platform(0,200,PLATFORM_WIDTH,PLATFORM_HEIGHT)
    platform22 = Platform(0,100,PLATFORM_WIDTH,PLATFORM_HEIGHT)

    platforms.add(platform1, platform2, platform3,platform4, platform5, platform6, platform7, platform8, platform9, platform10, platform11, platform12, platform13, platform14, platform15, platform16, platform17, platform18, platform19, platform20, platform21, platform22)
    
    spike1 = Spike(275,170)
    spike2 = Spike(305,170)
    spike3 = Spike(335,170)
    spike4 = Spike(735,170)
    spike5 = Spike(1085,170)
    spike6 = Spike(1200,270)
    spike7 = Spike(1230,270)
    spike8 = Spike(1570,370)
    spike9 = Spike(1170,470)
    spike10 = Spike(1200,470)
    spike11 = Spike(1230,470)
    spike12 = Spike(940,470)
    spike13 = Spike(965,470)
    spike14 = Spike(990,470)
    spike15 = Spike(1015,470)
    spike16 = Spike(500,520)
    spike17 = Spike(670,520)
    spike18 = Spike(305,470)
    spike19 = Spike(280,470)
    spike20 = Spike(255,470)
    spike21 = Spike(230,470)
    spike22 = Spike(200,770)
    spike23 = Spike(230,770)
    spike24 = Spike(260,770)
    spike25 = Spike(500,770)
    spike26 = Spike(530,770)
    spike27 = Spike(560,770)
    spike28 = Spike(1080,770)
    spike29 = Spike(1105,770)
    spike30 = Spike(1130,770)
    spike31 = Spike(1155,770)
    spike32 = Spike(1570,870)
    spike33 = Spike(1540,870)
    spike34 = Spike(750,970)
    spike35 = Spike(780,970)
    spike36 = Spike(890,970)
    spike37 = Spike(920,970)
    spike38 = Spike(350,970)
    spike39 = Spike(375,970)
    spike40 = Spike(400,970)
    spike41 = Spike(425,970)
    
    spikes.add(spike1,spike2,spike3,spike4,spike5,spike6,spike7,spike8,spike9,spike10,spike11,spike12,spike13,spike14,spike15,spike16,spike17,spike18,spike19,spike20,spike21,spike22,spike23,spike24,spike25,spike26,spike27,spike28,spike29,spike30,spike31,spike32,spike33,spike34,spike35,spike36,spike37,spike38,spike39,spike40,spike41)
    
    new_trampoline = Trampoline(0,810)
    trampolines.add(new_trampoline)

    key3 = Key(800, 600)
    door3 = Door(150,0)

    all_sprites.add(player, platforms, spikes, trampolines, key3, door3, goomba)
    scene_changed = 2

# changement de scene 3
def create_new_scene3():
    global scene_changed
    global door4
    global key4

    # réinitialisation des sprites apres changement de scene
    all_sprites.empty()
    platforms.empty()
    spikes.empty()
    trampolines.empty()

    # le joueur a utilisé sa clé précédement
    player.has_key = False
    
    # réinitialisation des placements des sprites
    player.rect.x = 50
    player.rect.y = 775
    goomba.rect.x = 50
    goomba.rect.y = 590
    goomba.alive = True

    # configuration de la scene 3

    # création des platformes
    platform1 = Platform(0, 800, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platform2 = Platform(100, 800, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platform3 = Platform(500, 800, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platform4 = Platform(700, 600, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platform5 = Platform(300, 600, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platform6 = Platform(700, 990, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platform7 = Platform(100, 600, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platform8 = Platform(0, 600, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platform9 = Platform(0, 500, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platform10 = Platform(0, 400, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platform11 = Platform(0, 300, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platform12 = Platform(200, 300, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platform13 = Platform(400, 300, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platform14 = Platform(600, 300, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platform15 = Platform(800, 300, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platform16 = Platform(1000, 300, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platform17 = Platform(1200, 300, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platform18 = Platform(1500, 300, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platform19 = Platform(1250, 500, PLATFORM_WIDTH, PLATFORM_HEIGHT)#
    platform20 = Platform(1450, 900, PLATFORM_WIDTH, PLATFORM_HEIGHT)#
    platform21 = Platform(400, 200, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platform22 = Platform(900, 200, PLATFORM_WIDTH, PLATFORM_HEIGHT)

    # ajout des platformes dans le Sprite group "platforms"
    platforms.add(platform1, platform2, platform3,platform4, platform5, platform6, platform7, platform8, platform9, platform10, platform11, platform12, platform13, platform14, platform15, platform16, platform17, platform18, platform19, platform20, platform21, platform22)
    
    # création des Spikes
    spike1 = Spike(500, 770)
    spike2 = Spike(534, 770)
    spike3 = Spike(568, 770)
    spike4 = Spike(602, 770)
    spike5 = Spike(636, 770)
    spike6 = Spike(670, 770)
    spike7 = Spike(640, 970)
    spike8 = Spike(670, 970)
    spike9 = Spike(610, 970)
    spike10 = Spike(385, 570)
    spike11 = Spike(1250, 470)
    spike12 = Spike(1284, 470)
    spike13 = Spike(1318, 470)
    spike14 = Spike(1352, 470)
    spike15 = Spike(1386, 470)
    spike16 = Spike(1420, 470)
    spike17 = Spike(1450, 870)
    spike18 = Spike(1480, 870)
    spike19 = Spike(1510, 870)
    spike20 = Spike(1540, 870)
    spike21 = Spike(1570, 870)
    spike22 = Spike(1330, 970)
    spike23 = Spike(1300, 970)
    spike24 = Spike(1270, 970)
    spike25 = Spike(1240, 970)
    spike26 = Spike(1210, 970)
    spike27 = Spike(1180, 970)
    spike28 = Spike(1150, 970)
    spike29 = Spike(1120, 970)
    spike30 = Spike(1090, 970)
    spike31 = Spike(1060, 970)
    spike32 = Spike(1030, 970)
    spike33 = Spike(1000, 970)
    spike34 = Spike(975, 970)
    spike35 = Spike(950, 970)
    spike36 = Spike(925, 970)
    spike37 = Spike(900, 970)
    spike38 = Spike(270, 970)
    spike39 = Spike(240, 970)
    spike40 = Spike(210, 970)
    spike41 = Spike(180, 970)
    spike42 = Spike(150, 970)
    spike43 = Spike(120, 970)
    spike44 = Spike(90, 970)
    spike45 = Spike(60, 970)
    spike46 = Spike(30, 970)
    spike47 = Spike(0, 970)
    spike48 = Spike(0, 570)
    spike49 = Spike(30, 570)
    spike50 = Spike(340, 270)
    spike51 = Spike(370, 270)
    spike52 = Spike(570, 270)
    spike53 = Spike(600, 270)
    spike54 = Spike(485, 170)
    spike55 = Spike(810, 270)
    spike56 = Spike(780, 270)
    spike57 = Spike(750, 270)
    spike58 = Spike(1070, 170)
    spike59 = Spike(900, 170)
    
    # ajout des spikes dans le Sprite group "spikes"
    spikes.add(spike1,spike2,spike3,spike4,spike5,spike6,spike7,spike8,spike9,spike10,spike11,spike12,spike13,spike14,spike15,spike16,spike17,spike18,spike19,spike20,spike21,spike22,spike23,spike24,spike25,spike26,spike27,spike28,spike29,spike30,spike31,spike32,spike33,spike34,spike35,spike36,spike37,spike38,spike39,spike40,spike41,spike42,spike43,spike44,spike45,spike46,spike47,spike48,spike49,spike50,spike51,spike52,spike53,spike54,spike55,spike56,spike57,spike58,spike59)
    
    # création et ajout du trampoline dans le Sprite group "trampolines"
    new_trampoline = Trampoline(700,980)
    trampolines.add(new_trampoline)

    # création de clé3 et porte3
    key4 = Key(985, 100)
    door4 = Door(1550, 900)

    # ajout des Sprites dans un Sprite group global
    all_sprites.add(player, platforms, spikes, trampolines, key4, door4, goomba)
    scene_changed = 3 # la scene a changé une deuxieme fois
	
# création du End Screen
def end_game_screen():
    screen.fill(WHITE) # le fond est blanc
    path = os.path.join(chemin_fichier, "end_screen.png") # chemin vers l'image "end_screen.png"
    fond = pygame.image.load(path) # charge l'image "end_screen.png"
    screen.blit(fond,(0,0)) # dessine l'image sur le fond
    pygame.display.flip() # rend visible toutes les modifications depuis le dernier rafraichissement
    pygame.time.delay(12000) # fait apparaitre le "end_screen" pendant 12 secondes puis fermeture du jeu
    pygame.quit()
    sys.exit()

main_menu() # fait apparaitre le menu d'avant jeu

# Game Loop
while running:  
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # si l'on quitte pygame , tout s'arrete
            running = False
    player.update(platforms)
    goomba.update(platforms)

    # collection des clés selon la scene
    if scene_changed == 0 and player.has_key == False:
        player.collect_key(key)
    else:
        if scene_changed == 1 and player.has_key == False:
            player.collect_key(key2)
        else:
            if scene_changed == 2 and player.has_key == False:
                player.collect_key(key3)
            else:
                if scene_changed == 3 and player.has_key == False:
                    player.collect_key(key4)

    # changements de scenes
    if scene_changed == 0:
        if player.has_key and door.unlock(player):
            create_new_scene()
    else:
        if scene_changed == 1:
            if player.has_key and door2.unlock(player):
                create_new_scene2()
        else:
            if scene_changed == 2:
                if player.has_key and door3.unlock(player):
                    create_new_scene3()
            else:
                if scene_changed == 3:
                    if player.has_key and door4.unlock(player):
                        end_game_screen()

    # collisions des portes selon la scene
    if scene_changed ==0:
        door.check_locked(player)
    else:
        if scene_changed == 1:
            door2.check_locked(player)
        else:
            if scene_changed == 2:
                door3.check_locked(player)
            else:
                if scene_changed == 3:
                    door4.check_locked(player)

    # Mort goomba + goomba damage
    if pygame.sprite.collide_rect(player, goomba) and goomba.alive:
        if player.rect.bottom <= goomba.rect.top + 50 and player.velocity_y > 0: # si le joueur frappe le goomba venant du haut
            goomba.die() # le goomba rend l'âme 
            player.velocity_y = -JUMP_STRENGTH + 2 # le joueur rebondit sur le goomba
        elif player.rect.bottom > goomba.rect.top + 10: # dans le cas inverse
            player.take_damage() # le joueur prend un dégat et décède

    # chargement de différents fonds d'écrans selon la scene
    if scene_changed == 0:
        path = os.path.join(chemin_fichier, "font1.png")
        fond = pygame.image.load(path)
        screen.blit(fond,(0,0))
    else:
        if scene_changed == 1:
            path = os.path.join(chemin_fichier, "font2.png")
            fond = pygame.image.load(path)
            screen.blit(fond,(0,0))
        else:
            if scene_changed == 2:
                screen.fill(LIGHT_GRAY)
            else:
                if scene_changed == 3:
                    path = os.path.join(chemin_fichier, "font3.png")
                    fond = pygame.image.load(path)
                    screen.blit(fond,(0,0))

    # Spike damage
    if pygame.sprite.spritecollideany(player, spikes): # si le joueur entre entre en collision avec le spike
        player.take_damage() # il prend un dégat et décède
    
    # Trampoline Bounce power
    for trampoline in trampolines: # pour chaque trampoline
        if pygame.sprite.collide_rect(player, trampoline) and player.velocity_y > 0: #  si le joueur tombe sur le trampoline avec une vitesse verticale supérieur a 0
            player.velocity_y =- JUMP_STRENGTH - 12  # fait rebondir le joueur très haut
    all_sprites.draw(screen) # dessine les sprites sur l'écran

    # Display point de vies
    font = pygame.font.SysFont(None, 36) # None = police d'écriture , 36 = taille de la police
    health_text = font.render(f"Health: {player.health}", True, (0, 0, 0)) # fait apparaitre un texte "health = ( points de vies du joueur )"
    screen.blit(health_text, (10, 10)) # se texte se situe en haut a gauche de l'écran
    pygame.display.flip() # rafraichissement de l'écran
    clock.tick(60) # 60 images par secondes

    # End the game if dead
    if player.health <= 0: # si le joueur possede 0 au moins points de vies , il est mort , le jeu s'sarrete et "Game Over" est print dans la console
        print("Game Over!")
        running = False

# fermeture du jeu
pygame.quit()
sys.exit()
