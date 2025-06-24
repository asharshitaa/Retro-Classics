import pygame
import random
import os

pygame.init()

WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Egg Catcher Deluxe")
clock = pygame.time.Clock()
FPS = 60

SKY = (135, 206, 235)
GRASS = (34, 139, 34)
BROWN = (139, 69, 19)
GOLD = (255, 215, 0)
RED = (220, 20, 60)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
BASKET_COLOR = (160, 82, 45)

font = pygame.font.SysFont("Verdana", 36)
big_font = pygame.font.SysFont("Verdana", 72)

basket_width, basket_height = 100, 50
basket_x = WIDTH // 2 - basket_width // 2
basket_y = HEIGHT - 80
basket_speed = 10

num_chickens = 5
chicken_positions = [i * (WIDTH // num_chickens) + 20 for i in range(num_chickens)]

falling_objects = []
object_speed = 4
spawn_delay = 45
spawn_counter = 0

score = 0
lives = 3
game_over = False
high_score = 0

if os.path.exists("highscore.txt"):
    with open("highscore.txt", "r") as f:
        high_score = int(f.read())

def save_high_score():
    with open("highscore.txt", "w") as f:
        f.write(str(high_score))

def spawn_object():
    obj_type = random.choices(['egg', 'golden', 'bomb'], weights=[70, 20, 10])[0]
    x = random.choice(chicken_positions) + 20
    falling_objects.append({'x': x, 'y': 60, 'type': obj_type})

def draw_objects():
    for obj in falling_objects:
        if obj['type'] == 'egg':
            pygame.draw.ellipse(screen, YELLOW, (obj['x'], obj['y'], 20, 25))
        elif obj['type'] == 'golden':
            pygame.draw.ellipse(screen, GOLD, (obj['x'], obj['y'], 20, 25))
        elif obj['type'] == 'bomb':
            pygame.draw.circle(screen, RED, (obj['x'] + 10, obj['y'] + 12), 12)

def draw_chickens():
    for cx in chicken_positions:
        body_y = 80
        pygame.draw.ellipse(screen, WHITE, (cx, body_y, 40, 30))  # chicken body
        pygame.draw.circle(screen, BLACK, (cx + 10, body_y + 10), 3)   # eye
        pygame.draw.polygon(screen, RED, [(cx + 20, body_y), (cx + 25, body_y - 5), (cx + 30, body_y)])  # beak

def check_collision(obj):
    return (basket_x < obj['x'] + 10 < basket_x + basket_width) and (basket_y < obj['y'] + 20 < basket_y + basket_height)

def reset_game():
    global score, lives, falling_objects, object_speed, game_over
    score = 0
    lives = 5
    falling_objects.clear()
    object_speed = 4
    game_over = False

running = True
while running:
    screen.fill(SKY)
    pygame.draw.rect(screen, GRASS, (0, HEIGHT - 40, WIDTH, 40))  

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            if game_over and event.key == pygame.K_r:
                reset_game()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and basket_x > 0:
        basket_x -= basket_speed
    if keys[pygame.K_RIGHT] and basket_x < WIDTH - basket_width:
        basket_x += basket_speed

    if not game_over:
        spawn_counter += 1
        if spawn_counter >= spawn_delay:
            spawn_object()
            spawn_counter = 0

        object_speed = 4 + (score // 10)  # difficulty increase

        for obj in falling_objects[:]:
            obj['y'] += object_speed

            if check_collision(obj):
                if obj['type'] == 'egg':
                    score += 1
                elif obj['type'] == 'golden':
                    score += 5
                elif obj['type'] == 'bomb':
                    lives -= 1
                falling_objects.remove(obj)

            elif obj['y'] > HEIGHT:
                if obj['type'] != 'bomb':
                    lives -= 1
                falling_objects.remove(obj)

        draw_objects()

    pygame.draw.rect(screen, BASKET_COLOR, (basket_x, basket_y, basket_width, basket_height), border_radius=12)

    if score > high_score:
        high_score = score
        save_high_score()

    score_line = f"Score: {score}   High Score: {high_score}"
    lives_line = f"Lives: {lives}"

    score_text = font.render(score_line, True, BLACK)
    lives_text = font.render(lives_line, True, RED)

    score_rect = score_text.get_rect(center=(WIDTH // 2, 10 + score_text.get_height() // 2))
    lives_rect = lives_text.get_rect(center=(WIDTH // 2, score_rect.bottom + 10))

    screen.blit(score_text, score_rect)
    screen.blit(lives_text, lives_rect)

    draw_chickens()

    if lives <= 0:
        game_over = True

    if game_over:
        game_text = big_font.render("GAME OVER", True, RED)
        retry_text = font.render("Press 'R' to Restart", True, BLACK)
        quit_text = font.render("Press 'Q' to Quit", True, BLACK)
        screen.blit(game_text, game_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80)))
        screen.blit(retry_text, retry_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        screen.blit(quit_text, quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50)))

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
