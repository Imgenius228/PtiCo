import pygame
import random

# Ініціалізація модулів у pygame
pygame.init()

SCREEN = pygame.display.set_mode((500, 750))  # Налаштування дисплея

# фон
BACKGROUND_IMAGE = pygame.image.load('Image/background-day.png')
BACKGROUND_IMAGE = pygame.transform.scale2x(BACKGROUND_IMAGE)

# Птах
BIRD_IMAGE = pygame.image.load('Image/bird.png')
bird_x = 50
bird_y = 300
bird_y_change = 0

def display_bird(x, y):
    SCREEN.blit(BIRD_IMAGE, (x, y))

# Перешкоди
OBSTACLE_WIDTH = 70
OBSTACLE_HEIGHT = random.randint(100,400)
OBSTACLE_COLOR = (211, 253, 117)
OBSTACE_X_CHANGE = -2
obstacle_x = 800

def display_obstacle(height):
    pygame.draw.rect(SCREEN, OBSTACLE_COLOR, (obstacle_x, 0, OBSTACLE_WIDTH, height))
    bottom_obstacle_height = 635 - height - 150
    pygame.draw.rect(SCREEN, OBSTACLE_COLOR, (obstacle_x, 750 - bottom_obstacle_height, OBSTACLE_WIDTH, bottom_obstacle_height))

# Виявлення зіткнень
def collision_detection (bird_x, bird_y, obstacle_x, obstacle_width, obstacle_height): 
    if bird_x + 34 >= obstacle_x and bird_x <= obstacle_x + obstacle_width:
        if bird_y <= obstacle_height:
            return True
    return False

def collision_detections (bird_x, bird_y, obstacle_x, OBSTACLE_WIDTH, bottom_obstacle_height):
    if bird_x + 34 >= obstacle_x and bird_x <= obstacle_x + OBSTACLE_WIDTH:
        if bird_y <= bottom_obstacle_height:
            return True
    return False

# Бали
score = 0
SCORE_FONT = pygame.font.Font('freesansbold.ttf', 32)

def score_display(score):
    display = SCORE_FONT.render(f"Score: {score}", True, (255,255,255))
    SCREEN.blit(display, (10, 10))

# Початковий екран
startFont = pygame.font.Font('freesansbold.ttf', 32)
def start():
    display = startFont.render(f"PRESS SPACE BAR TO START", True, (255, 255, 255))
    SCREEN.blit(display, (20, 200))
    pygame.display.update()

# Екран коли програв
score_list = [0]

game_over_font1 = pygame.font.Font('freesansbold.ttf', 64)
game_over_font2 = pygame.font.Font('freesansbold.ttf', 32)

def game_over():
    # перевірити максимальний бал
    maximum = max(score_list)
    #  "Гра закінчена"
    display1 = game_over_font1.render(f"GAME OVER", True, (200,35,35))
    SCREEN.blit(display1, (50, 300))
    # показує ваш поточний і максимальний бал
    display2 = game_over_font2.render(f"SCORE: {score} MAX SCORE: {maximum}", True, (255, 255, 255))
    SCREEN.blit(display2, (50, 400))
    #  Якщо ваш новий бал такий самий, як максимальний, ви досягли нового найвищого балу
    if score == maximum:
        display3 = game_over_font2.render(f"NEW HIGH SCORE!!", True, (200,35,35))
        SCREEN.blit(display3, (80, 100))

running = True
# очікування посилатиметься на наш кінцевий або початковий екран
waiting = True
# встановіть зіткнення на false на початку, щоб ми бачили лише початковий екран на початку
collision = False

while running:

    SCREEN.fill((0, 0, 0))

    # відобразити фонове зображення
    SCREEN.blit(BACKGROUND_IMAGE, (0, 0))

    # нас буде відправлено в цей цикл while на початку та в кінці кожної гри
    while waiting:
        if collision:
            # Якщо зіткнення має значення True (з другого разу і далі), ми побачимо і кінцевий, і початковий екрани
            game_over()
            start()
        else:
            # Це стосується першого разу, коли гравець починає гру
            start()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Якщо ми натиснемо пробіл, ми вийдемо з циклу очікування та почнемо грати в гру
                    # ми також скинемо деякі змінні, такі як оцінка, позиція птаха Y і початкова позиція перешкоди
                    score = 0
                    bird_y = 300
                    obstacle_x = 500
                    # щоб вийти з циклу while
                    waiting = False

            if event.type == pygame.QUIT:
                # у випадку, якщо ми виходимо, зробити як запуск, так і очікування помилковими
                waiting = False
                running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Якщо ви натиснете exit, ви вийдете з циклу while і pygame завершить роботу
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                #  якщо ви натиснете пробіл, ви переміститесь вгору
                bird_y_change = -6

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                # коли ви відпускаєте пробіл, ви автоматично рухатиметеся вниз
                bird_y_change = 3

    # переміщення птаха вертикально
    bird_y += bird_y_change
    # встановлення меж руху птахів
    if bird_y <= 0:
        bird_y = 0
    if bird_y >= 571:
        bird_y = 571

    # Переміщення перешкоди
    obstacle_x += OBSTACE_X_CHANGE

    # Зіткнення
    collision = collision_detection(bird_x, bird_y, obstacle_x, OBSTACLE_WIDTH, OBSTACLE_HEIGHT) 
    collision = collision_detections(bird_x, bird_y, obstacle_x, OBSTACLE_WIDTH, bottom_obstacle_height=OBSTACLE_HEIGHT)
    
    if collision:
        # якщо зіткнення все-таки станеться, ми додамо цю оцінку до нашого списку оцінок і зробимо очікування True
        score_list.append(score)
        waiting = True

    # створення нових перешкод
    if obstacle_x <= -10:
        obstacle_x = 500
        OBSTACLE_HEIGHT = random.randint(200, 400)
        score += 1
    # відображення перешкоди
    display_obstacle(OBSTACLE_HEIGHT)

    # показ птаха
    display_bird(bird_x, bird_y)

    # відобразити рахунок
    score_display(score)

    # Оновлюйте відображення після кожної ітерації циклу while
    pygame.display.update()

pygame.quit()