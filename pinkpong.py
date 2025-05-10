import pygame
import random

# Параметры окна
WIDTH, HEIGHT = 800, 600
FPS = 60

# Цвета
WHITE = (255, 255, 255)
WHIT = (255, 255, 125)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Размеры и начальные позиции
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
BALL_SIZE = 20

PLAYER_SPEED = 7
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

WIN_SCORE = 10  # Количество очков для победы

# Рендеринг текста
def draw_text(surf, text, size, x, y):
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

# Класс для теннисного мяча
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2
        self.speed_x = random.choice([BALL_SPEED_X, -BALL_SPEED_X])
        self.speed_y = random.choice([BALL_SPEED_Y, -BALL_SPEED_Y])

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Отскок от верха и низа
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1

        # Вышел за левый край — очко игроку 2
        if self.rect.left < 0:
            global score_player2
            score_player2 += 1
            self.reset()

        # Вышел за правый край — очко игроку 1
        if self.rect.right > WIDTH:
            global score_player1
            score_player1 += 1
            self.reset()

    def reset(self):
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2
        self.speed_x = random.choice([BALL_SPEED_X, -BALL_SPEED_X])
        self.speed_y = random.choice([BALL_SPEED_Y, -BALL_SPEED_Y])

# Класс для игровой ракетки
class Paddle(pygame.sprite.Sprite):
    def __init__(self, x_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT))
        self.image.fill(WHIT)
        self.rect = self.image.get_rect()
        self.rect.centerx = x_pos
        self.rect.centery = HEIGHT / 2
        self.speed = PLAYER_SPEED

    def move_up(self):
        if self.rect.top > 0:
            self.rect.y -= self.speed

    def move_down(self):
        if self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

# Главная функция игры
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = True

    # Глобальные переменные счета
    global score_player1, score_player2
    score_player1 = 0
    score_player2 = 0

    all_sprites = pygame.sprite.Group()
    paddle_left = Paddle(PADDLE_WIDTH)      # Левый игрок
    paddle_right = Paddle(WIDTH - PADDLE_WIDTH)  # Правый игрок
    ball = Ball()

    all_sprites.add(paddle_left, paddle_right, ball)

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Управление первой ракеткой (игрок 1): клавиши W и S
        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_w]:  # Вверх
            paddle_left.move_up()
        if key_state[pygame.K_s]:  # Вниз
            paddle_left.move_down()

        # Управление второй ракеткой (игрок 2): стрелочки вверх и вниз
        if key_state[pygame.K_UP]:  # Вверх
            paddle_right.move_up()
        if key_state[pygame.K_DOWN]:  # Вниз
            paddle_right.move_down()

        # Обновление состояния всех спрайтов
        all_sprites.update()

        # Проверка попадания мяча в ракетку
        hits = pygame.sprite.spritecollide(ball, [paddle_left, paddle_right], False)
        if len(hits) > 0:
            ball.speed_x *= -1  # Меняется горизонтальное направление мяча

        # Завершение игры при наборе нужного количества очков
        if score_player1 >= WIN_SCORE or score_player2 >= WIN_SCORE:
            running = False

        # Отрисовка всего
        screen.fill(BLACK)
        all_sprites.draw(screen)

        # Вывод текущего счёта
        draw_text(screen, str(score_player1), 36, WIDTH // 4, 10)
        draw_text(screen, str(score_player2), 36, WIDTH * 3 // 4, 10)

        pygame.display.flip()

    # Окончание игры
    result_text = "YOU WIN" if score_player1 >= WIN_SCORE else "YOU LOSE"
    final_screen = pygame.display.set_mode((WIDTH, HEIGHT))
    final_screen.fill(BLACK)
    draw_text(final_screen, result_text, 72, WIDTH // 2, HEIGHT // 2)
    pygame.display.flip()
    pygame.time.delay(3000)  # Пауза перед закрытием окна

    pygame.quit()

if __name__ == '__main__':
    main()
