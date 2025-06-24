import pygame
import random

pygame.init()

# consts
WIDTH, HEIGHT = 800, 400
WHITE = (255, 255, 255)
FPS = 60
GRAVITY = 1

# screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Game")
clock = pygame.time.Clock()

# load assets
dino_img = pygame.image.load("OneDrive\Desktop\my_games\dino_game\dino.png")
cactus_img = pygame.image.load("OneDrive\Desktop\my_games\dino_game\cactus.png")

class Dino:
    def __init__(self):
        self.image = dino_img
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = HEIGHT - self.rect.height - 20
        self.is_jumping = False
        self.velocity = 0

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity = -15

    def update(self):
        if self.is_jumping:
            self.rect.y += self.velocity
            self.velocity += GRAVITY
            if self.rect.y >= HEIGHT - self.rect.height - 20:
                self.rect.y = HEIGHT - self.rect.height - 20
                self.is_jumping = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Cactus:
    def __init__(self):
        self.image = cactus_img
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = HEIGHT - self.rect.height - 20

    def update(self):
        self.rect.x -= 10

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# main game 
def main():
    run = True
    dino = Dino()
    cactus = Cactus()
    font = pygame.font.SysFont(None, 36)
    score = 0

    while run:
        clock.tick(FPS)
        screen.fill(WHITE)

        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dino.jump()

        dino.update()
        cactus.update()

        if dino.rect.colliderect(cactus.rect):
            run = False

        if cactus.rect.x < -cactus.rect.width:
            cactus = Cactus()
            score += 1

        dino.draw(screen)
        cactus.draw(screen)

        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
