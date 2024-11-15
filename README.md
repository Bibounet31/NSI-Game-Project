import pygame
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Chan uwu")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)  # Top paddle color
RED = (255, 0, 0)   # Bottom paddle color

# Font
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# Paddle settings
PADDLE_WIDTH, PADDLE_HEIGHT = 150, 10
PADDLE_SPEED = 12

# Ball settings
BALL_SIZE = 30
initial_ball_speed = 5  # Initial speed
ball_speed_increment = 0.5  # Speed increase on paddle hit
ball_speed_x, ball_speed_y = initial_ball_speed, initial_ball_speed

# Create paddles and ball
top_paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, 20, PADDLE_WIDTH, PADDLE_HEIGHT)
bottom_paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 30, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_SIZE, BALL_SIZE)

# Initialize scores
top_score = 0
bottom_score = 0
max_score = 3  # Winning score

# Function to display the winner screen
def display_winner(winner_text):
    screen.fill(BLACK)
    text = font.render(winner_text, True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.delay(2000)  # Display for 2 seconds before closing
    pygame.quit()
    sys.exit()

# Reset ball position and speed
def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.x, ball.y = WIDTH // 2, HEIGHT // 2  # Reset ball to center
    ball_speed_x, ball_speed_y = initial_ball_speed, initial_ball_speed  # Reset speed

# Game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Check for a win
    if top_score >= max_score:
        display_winner("Blue Wins!")
    elif bottom_score >= max_score:
        display_winner("Red Wins!")

    # Get keys pressed
    keys = pygame.key.get_pressed()

    # Top paddle movement (Q and D keys)
    if keys[pygame.K_q] and top_paddle.left > 0:
        top_paddle.x -= PADDLE_SPEED
    if keys[pygame.K_d] and top_paddle.right < WIDTH:
        top_paddle.x += PADDLE_SPEED

    # Bottom paddle movement (left and right arrow keys)
    if keys[pygame.K_LEFT] and bottom_paddle.left > 0:
        bottom_paddle.x -= PADDLE_SPEED
    if keys[pygame.K_RIGHT] and bottom_paddle.right < WIDTH:
        bottom_paddle.x += PADDLE_SPEED

    # Ball movement
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collision with walls
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed_x = -ball_speed_x  # Reverse horizontal direction

    # Ball collision with paddles
    if ball.colliderect(top_paddle) or ball.colliderect(bottom_paddle):
        ball_speed_y = -ball_speed_y  # Reverse vertical direction
        # Increase speed by increment for both X and Y direction
        if ball_speed_x > 0:
            ball_speed_x += ball_speed_increment
        else:
            ball_speed_x -= ball_speed_increment
        if ball_speed_y > 0:
            ball_speed_y += ball_speed_increment
        else:
            ball_speed_y -= ball_speed_increment

    # Check if the ball goes out of bounds (score and reset ball)
    if ball.top <= 0:  # Ball goes past the top paddle
        bottom_score += 1
        reset_ball()
    elif ball.bottom >= HEIGHT:  # Ball goes past the bottom paddle
        top_score += 1
        reset_ball()

    # Clear screen
    screen.fill(BLACK)

    # Draw paddles and ball
    pygame.draw.rect(screen, BLUE, top_paddle)
    pygame.draw.rect(screen, RED, bottom_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)

    # Display scores
    top_score_text = small_font.render(str(top_score), True, BLUE)
    bottom_score_text = small_font.render(str(bottom_score), True, RED)
    screen.blit(top_score_text, (WIDTH // 2 - 50, 50))
    screen.blit(bottom_score_text, (WIDTH // 2 - 50, HEIGHT - 70))

    # Update display
    pygame.display.flip()

    # Frame rate
    pygame.time.Clock().tick(60)
