#                             Пинг-Понг — компьютерная игра.

import pygame
import sys

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BALL_SPEED = 5
PADDLE_SPEED = 5

# Создаем окно
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Пинг-Понг')

# Шрифт для отображения текста
font = pygame.font.Font(None, 74)

# Класс для мяча
class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, 15, 15)
        self.vx = BALL_SPEED
        self.vy = BALL_SPEED

    def move(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

        # Отскок от верхней и нижней границы
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.vy = -self.vy

    def draw(self):
        pygame.draw.ellipse(screen, WHITE, self.rect)

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.vx = BALL_SPEED * (-1 if self.vx > 0 else 1)
        self.vy = BALL_SPEED

# Класс для ракеток
class Paddle:
    def __init__(self, x):
        self.rect = pygame.Rect(x, HEIGHT // 2 - 60, 10, 120)

    def move(self, up, down):
        if up and self.rect.top > 0:
            self.rect.y -= PADDLE_SPEED
        if down and self.rect.bottom < HEIGHT:
            self.rect.y += PADDLE_SPEED

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

# Функция для отрисовки, обновления и обработки событий
def main():
    clock = pygame.time.Clock()

    ball = Ball()
    left_paddle = Paddle(30)
    right_paddle = Paddle(WIDTH - 40)

    left_up = left_down = right_up = right_down = False
    left_score = 0
    right_score = 0
    game_started = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Управление клавишами
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    left_up = True
                if event.key == pygame.K_s:
                    left_down = True
                if event.key == pygame.K_UP:
                    right_up = True
                if event.key == pygame.K_DOWN:
                    right_down = True
                if event.key == pygame.K_SPACE:
                    game_started = not game_started
                if event.key == pygame.K_r:
                    left_score = 0
                    right_score = 0
                    ball.reset()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    left_up = False
                if event.key == pygame.K_s:
                    left_down = False
                if event.key == pygame.K_UP:
                    right_up = False
                if event.key == pygame.K_DOWN:
                    right_down = False

        if game_started:
            # Обновление состояния игры
            ball.move()
            left_paddle.move(left_up, left_down)
            right_paddle.move(right_up, right_down)

            # Проверка столкновений с ракетками
            if ball.rect.colliderect(left_paddle.rect) or ball.rect.colliderect(right_paddle.rect):
                ball.vx = -ball.vx

            # Обновление счета
            if ball.rect.left <= 0:
                right_score += 1
                ball.reset()
                game_started = False
            if ball.rect.right >= WIDTH:
                left_score += 1
                ball.reset()
                game_started = False

        # Отрисовка
        screen.fill(BLACK)
        ball.draw()
        left_paddle.draw()
        right_paddle.draw()

        # Отображение счета
        score_text = font.render(f"{left_score} : {right_score}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))

        # Обновление экрана
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
