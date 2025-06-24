import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Water Sort Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLOR_MAP = {
    'red': (255, 0, 0),
    'blue': (0, 0, 255),
    'green': (0, 255, 0),
    'yellow': (255, 255, 0),
    'purple': (128, 0, 128),
    'orange': (255, 165, 0),
    'pink': (255, 105, 180),
    'cyan': (0, 255, 255)
}

TUBE_WIDTH = 50
TUBE_HEIGHT = 120
GAP = 20
BASE_Y = HEIGHT // 2
BLOCK_HEIGHT = TUBE_HEIGHT // 4

def generate_random_level(colors, total_tubes):
    balls = colors * 4
    random.shuffle(balls)
    tubes = [[] for _ in range(total_tubes)]
    for i, color in enumerate(balls):
        tubes[i % (total_tubes - 2)].append(color)
    return tubes

LEVELS = [
    {'colors': ['red', 'blue'], 'tubes': 4},
    {'colors': ['red', 'blue', 'green'], 'tubes': 5},
    {'colors': ['red', 'blue', 'green', 'yellow'], 'tubes': 6},
]

current_level = 0
TUBE_COLORS = generate_random_level(LEVELS[current_level]['colors'], LEVELS[current_level]['tubes'])

running = True
selected = None
game_won = False
show_popup = False
clock = pygame.time.Clock()
popup_font = pygame.font.SysFont(None, 36)
popup_options = ["Next Level", "Quit"]
popup_rects = []

def draw_tubes():
    screen.fill(WHITE)
    for i, tube in enumerate(TUBE_COLORS):
        x = GAP + i * (TUBE_WIDTH + GAP)
        y = BASE_Y - TUBE_HEIGHT
        pygame.draw.rect(screen, BLACK, (x, y, TUBE_WIDTH, TUBE_HEIGHT), 2)
        for j, color in enumerate(reversed(tube)):
            block_y = y + TUBE_HEIGHT - (j + 1) * BLOCK_HEIGHT
            pygame.draw.rect(screen, COLOR_MAP[color], (x + 2, block_y + 2, TUBE_WIDTH - 4, BLOCK_HEIGHT - 4))

def draw_popup():
    msg = popup_font.render("You Win! 🎉", True, (0, 128, 0))
    screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 40))
    popup_rects.clear()
    for i, option in enumerate(popup_options):
        rect = pygame.Rect(WIDTH // 2 - 60, 100 + i * 50, 120, 40)
        pygame.draw.rect(screen, (200, 200, 200), rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        text = popup_font.render(option, True, BLACK)
        screen.blit(text, (rect.x + 10, rect.y + 5))
        popup_rects.append((rect, option))

def get_clicked_tube(mouse_pos):
    mx, my = mouse_pos
    for i in range(len(TUBE_COLORS)):
        x = GAP + i * (TUBE_WIDTH + GAP)
        y = BASE_Y - TUBE_HEIGHT
        if x <= mx <= x + TUBE_WIDTH and y <= my <= y + TUBE_HEIGHT:
            return i
    return None

def get_top_color(tube):
    return tube[0] if tube else None

def count_top_color(tube):
    if not tube:
        return 0
    top = tube[0]
    return sum(1 for color in tube if color == top)

def check_win(tubes):
    for tube in tubes:
        if not tube:
            continue
        if len(tube) != 4 or not all(color == tube[0] for color in tube):
            return False
    return True

def check_pouring(tube1, tube2):
    return bool(tube1) and (len(tube2) < 4) and (not tube2 or tube1[0] == tube2[0])

def pour_colors(tube1, tube2):
    if not check_pouring(tube1, tube2):
        return False
    top_color = tube1[0]
    count = count_top_color(tube1)
    space = 4 - len(tube2)
    pour_amount = min(count, space)
    for _ in range(pour_amount):
        tube1.pop(0)
        tube2.insert(0, top_color)
    return True

while running:
    draw_tubes()

    if show_popup:
        draw_popup()

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if show_popup:
                for rect, option in popup_rects:
                    if rect.collidepoint(event.pos):
                        if option == "Next Level":
                            current_level += 1
                            if current_level < len(LEVELS):
                                TUBE_COLORS = generate_random_level(LEVELS[current_level]['colors'], LEVELS[current_level]['tubes'])
                                game_won = False
                                show_popup = False
                                selected = None
                        elif option == "Quit":
                            running = False
            elif not game_won:
                idx = get_clicked_tube(pygame.mouse.get_pos())
                if idx is not None:
                    if selected is None:
                        selected = idx
                    else:
                        if selected != idx:
                            poured = pour_colors(TUBE_COLORS[selected], TUBE_COLORS[idx])
                            if poured and check_win(TUBE_COLORS):
                                game_won = True
                                pygame.time.set_timer(pygame.USEREVENT, 1000)
                        selected = None

        elif event.type == pygame.USEREVENT and game_won:
            show_popup = True
            pygame.time.set_timer(pygame.USEREVENT, 0)

    clock.tick(30)

pygame.quit()
sys.exit()
