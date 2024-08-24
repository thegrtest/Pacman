import pygame
import random

# Initialize pygame
pygame.init()

# Set up display
screen_width = 448
screen_height = 576
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pac-Man')

# Colors
black = (0, 0, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
white = (255, 255, 255)

# Load images
pacman = pygame.image.load('pacman.png')
pacman = pygame.transform.scale(pacman, (32, 32))

ghost_image = pygame.image.load('ghost.png')
ghost_image = pygame.transform.scale(ghost_image, (32, 32))

heart_image = pygame.image.load('heart.png')
heart_image = pygame.transform.scale(heart_image, (24, 24))

coin_image = pygame.Surface((8, 8))
coin_image.fill(yellow)

# Pac-Man's position (starting near the bottom left corner)
pacman_x = 32
pacman_y = 512
pacman_speed = 2
pacman_direction = 'right'

# Player's lives and coin counter
lives = 3
coins_collected = 0

# More complex wall layout (vertical walls stop at the first horizontal wall)
walls = [
    # Outer boundaries
    pygame.Rect(0, 0, 448, 16),
    pygame.Rect(0, 0, 16, 576),
    pygame.Rect(432, 0, 16, 576),
    pygame.Rect(0, 560, 448, 16),

    # Horizontal inner walls
    pygame.Rect(64, 64, 320, 16),
    pygame.Rect(64, 496, 320, 16),
    pygame.Rect(64, 128, 64, 16),
    pygame.Rect(320, 128, 64, 16),
    pygame.Rect(64, 192, 128, 16),
    pygame.Rect(256, 192, 128, 16),
    pygame.Rect(192, 256, 64, 16),
    pygame.Rect(192, 320, 64, 16),
    pygame.Rect(64, 256, 64, 16),
    pygame.Rect(320, 256, 64, 16),
    pygame.Rect(64, 384, 128, 16),
    pygame.Rect(256, 384, 128, 16),
    pygame.Rect(192, 448, 64, 16),

    # Vertical inner walls stopping at the first horizontal wall
    pygame.Rect(128, 64, 16, 64),   # Stops at horizontal wall at y=128
    pygame.Rect(304, 64, 16, 64),   # Stops at horizontal wall at y=128
    pygame.Rect(128, 192, 16, 64),  # Stops at horizontal wall at y=256
    pygame.Rect(304, 192, 16, 64),  # Stops at horizontal wall at y=256
    pygame.Rect(192, 320, 16, 64),  # Stops at horizontal wall at y=384
    pygame.Rect(240, 320, 16, 64),  # Stops at horizontal wall at y=384
]

def is_valid_spawn(x, y):
    """Check if the spawn location is valid (not on a wall)."""
    spawn_rect = pygame.Rect(x, y, 32, 32)
    for wall in walls:
        if spawn_rect.colliderect(wall):
            return False
    return True

# Coin positions ensuring they don't spawn on walls
coins = []
potential_coin_positions = [
    (x, y) for x in range(80, 400, 48) for y in range(80, 520, 48)
]
for pos in potential_coin_positions:
    if is_valid_spawn(pos[0], pos[1]):
        coins.append(pos)

# Ghosts' initial positions ensuring they don't spawn on walls
ghosts = []
potential_ghost_positions = [
    (224, 224), (224, 256), (224, 288), (224, 320), (192, 160), (160, 192)
]
for pos in potential_ghost_positions:
    if is_valid_spawn(pos[0], pos[1]):
        ghosts.append({'x': pos[0], 'y': pos[1], 'direction': random.choice(['left', 'right', 'up', 'down'])})

ghost_speed = 2

def draw_walls():
    for wall in walls:
        pygame.draw.rect(screen, blue, wall)

def draw_coins():
    for coin in coins:
        screen.blit(coin_image, coin)

def draw_lives_and_coins():
    # Draw hearts (lives)
    for i in range(lives):
        screen.blit(heart_image, (10 + 30 * i, 10))
    
    # Draw coin counter
    font = pygame.font.Font(None, 36)
    text = font.render(f"Coins: {coins_collected}", True, white)
    screen.blit(text, (screen_width - 120, 10))

def move_pacman(direction, speed):
    global pacman_x, pacman_y, coins_collected
    if direction == 'left':
        pacman_x -= speed
    if direction == 'right':
        pacman_x += speed
    if direction == 'up':
        pacman_y -= speed
    if direction == 'down':
        pacman_y += speed

    # Collision detection with walls
    pacman_rect = pygame.Rect(pacman_x, pacman_y, 32, 32)
    for wall in walls:
        if pacman_rect.colliderect(wall):
            if direction == 'left':
                pacman_x += speed
            if direction == 'right':
                pacman_x -= speed
            if direction == 'up':
                pacman_y += speed
            if direction == 'down':
                pacman_y -= speed

    # Coin collection
    global coins
    pacman_rect = pygame.Rect(pacman_x, pacman_y, 32, 32)
    collected_coins = [coin for coin in coins if pacman_rect.colliderect(pygame.Rect(coin[0], coin[1], 8, 8))]
    coins_collected += len(collected_coins)
    coins = [coin for coin in coins if coin not in collected_coins]

def move_ghosts():
    for ghost in ghosts:
        ghost_x, ghost_y = ghost['x'], ghost['y']
        direction = ghost['direction']

        # Move ghost in the current direction
        if direction == 'left':
            ghost_x -= ghost_speed
        if direction == 'right':
            ghost_x += ghost_speed
        if direction == 'up':
            ghost_y -= ghost_speed
        if direction == 'down':
            ghost_y += ghost_speed

        # Collision detection with walls
        ghost_rect = pygame.Rect(ghost_x, ghost_y, 32, 32)
        collided = False
        for wall in walls:
            if ghost_rect.colliderect(wall):
                collided = True
                break

        if collided:
            # Revert movement and change direction
            if direction == 'left':
                ghost_x += ghost_speed
                ghost['direction'] = random.choice(['right', 'up', 'down'])
            if direction == 'right':
                ghost_x -= ghost_speed
                ghost['direction'] = random.choice(['left', 'up', 'down'])
            if direction == 'up':
                ghost_y += ghost_speed
                ghost['direction'] = random.choice(['left', 'right', 'down'])
            if direction == 'down':
                ghost_y -= ghost_speed
                ghost['direction'] = random.choice(['left', 'right', 'up'])
        else:
            ghost['x'], ghost['y'] = ghost_x, ghost_y

def check_collision():
    pacman_rect = pygame.Rect(pacman_x, pacman_y, 32, 32)
    for ghost in ghosts:
        ghost_rect = pygame.Rect(ghost['x'], ghost['y'], 32, 32)
        if pacman_rect.colliderect(ghost_rect):
            return True
    return False

# Main loop
running = True
while running:
    screen.fill(black)
    
    # Draw walls, coins, characters, and UI elements
    draw_walls()
    draw_coins()
    draw_lives_and_coins()
    screen.blit(pacman, (pacman_x, pacman_y))
    for ghost in ghosts:
        screen.blit(ghost_image, (ghost['x'], ghost['y']))
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Key handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        pacman_direction = 'left'
    if keys[pygame.K_RIGHT]:
        pacman_direction = 'right'
    if keys[pygame.K_UP]:
        pacman_direction = 'up'
    if keys[pygame.K_DOWN]:
        pacman_direction = 'down'
    
    # Move Pac-Man
    move_pacman(pacman_direction, pacman_speed)
    
    # Move Ghosts
    move_ghosts()
    
    # Check for collisions with ghosts
    if check_collision():
        lives -= 1
        if lives <= 0:
            print("Game Over!")
            running = False
        else:
            pacman_x, pacman_y = 32, 512  # Reset Pac-Man's position to the bottom left corner
    
    # Update the display
    pygame.display.flip()
    pygame.time.Clock().tick(30)

# Quit pygame
pygame.quit()
