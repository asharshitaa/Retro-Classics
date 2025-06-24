import pygame 
import sys
import random 

pygame.init() 

width = 600
height = 400
cell = 20 

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("My Snake Game!") 

clock = pygame.time.Clock()

white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)
direction = 'right'
snake = [(100, 100), (80, 100), (60, 100)]

food = (random.randint(0, (width - cell) // cell) * cell,
        random.randint(0, (height - cell) // cell) * cell)
score = 0

font = pygame.font.SysFont(None, 35)  

def game_over(Score):
    while True:
        screen.fill(black)
        msg1 = font.render(f"Game Over! Your score: {Score}", True, red)
        msg2 = font.render("Press R to restart or Q to quit", True, white)

        screen.blit(msg1, (width // 2 - 150, height // 2 - 30))
        screen.blit(msg2, (width // 2 - 180, height // 2 + 10))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r:
                    main() 


def main():
    global score, direction, snake, food

    direction = 'right'
    snake = [(100, 100), (80, 100), (60, 100)]
    score = 0
    food = (random.randint(0, (width - cell) // cell) * cell,
            random.randint(0, (height - cell) // cell) * cell)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over(score)  
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'down':
                    direction = 'up'
                elif event.key == pygame.K_DOWN and direction != "up":
                    direction = 'down'
                elif event.key == pygame.K_LEFT and direction != 'right':
                    direction = 'left'
                elif event.key == pygame.K_RIGHT and direction != 'left':
                    direction = 'right'

        screen.fill(black)

        score_text = font.render(f"Score: {score}", True, white)
        screen.blit(score_text, (10, 10))

        head_x, head_y = snake[0]
        if direction == 'up':
            head_y -= cell
        if direction == 'down':
            head_y += cell
        if direction == 'right':
            head_x += cell
        if direction == 'left':
            head_x -= cell

        new_head = (head_x, head_y)

        if head_x < 0 or head_x >= width or head_y < 0 or head_y >= height:
            game_over(score)

        if new_head in snake:
            game_over(score)

        snake.insert(0, new_head)

        if new_head == food:
            score += 1
            food = (random.randint(0, (width - cell) // cell) * cell,
                    random.randint(0, (height - cell) // cell) * cell)
        else:
            snake.pop() 

        gap = 2  

        for i, seg in enumerate(snake):
            x, y = seg
            rect = pygame.Rect(x + gap, y + gap, cell - 2 * gap, cell - 2 * gap)

            if i == 0:
                pygame.draw.rect(screen, green, rect)

                eye_radius = 2
                eye_offset_x = 4
                eye_offset_y = 4

                if direction == 'right':
                    eye1 = (x + cell - eye_offset_x, y + eye_offset_y)
                    eye2 = (x + cell - eye_offset_x, y + cell - eye_offset_y)
                elif direction == 'left':
                    eye1 = (x + eye_offset_x, y + eye_offset_y)
                    eye2 = (x + eye_offset_x, y + cell - eye_offset_y)
                elif direction == 'up':
                    eye1 = (x + eye_offset_x, y + eye_offset_y)
                    eye2 = (x + cell - eye_offset_x, y + eye_offset_y)
                elif direction == 'down':
                    eye1 = (x + eye_offset_x, y + cell - eye_offset_y)
                    eye2 = (x + cell - eye_offset_x, y + cell - eye_offset_y)

                pygame.draw.circle(screen, white, eye1, eye_radius)
                pygame.draw.circle(screen, white, eye2, eye_radius)
            else:
                pygame.draw.rect(screen, green, rect)


        pygame.draw.circle(screen, red, (food[0] + cell // 2, food[1] + cell // 2), cell // 2)
        pygame.draw.rect(screen, (0, 200, 0), (food[0] + cell // 2 - 2, food[1] + 2, 4, 5))

        pygame.display.update()
        clock.tick(10) 

main()
