import pygame as pg
from random import randint


# константы - глобальные переменные которые не будут меняться
WIDTH = 1000
HEIGHT = 800
SIZE = (WIDTH, HEIGHT)
CELL_HEIGHT = 10


# основная функция
def main():
    running = True
    screen = create_window()
    # заполнять словарь
    cells = {}
    for y in range(HEIGHT // CELL_HEIGHT):
        for x in range(WIDTH // CELL_HEIGHT):
            # Каждой клетке присваиваем квадрат
            #                             позиц. х         позиц. у     ширина        высота
            cells[(x, y)] = pg.Rect(x * CELL_HEIGHT, y * CELL_HEIGHT, CELL_HEIGHT, CELL_HEIGHT)
    # создаем змейку
    snake = [(50, 40), (50, 41), (50, 42), (50, 43)]
    draw_snake(screen, cells, snake)
    pg.display.flip()
    # направление змеи
    direction = "up"
    # яблоко
    apple = random_apple(snake)
    # время ожидания между кадрами
    wait_time = 100
    time_change = 2
    # съеденные яблоки
    apples = 0
    # активируем шрифты
    pg.font.init()
    # создаем шрифт
    font = pg.font.SysFont('comicsansms', 30, False, True)
    text_image = font.render(f"яблоки: {apples}", False, (255, 255, 255))
    # игровой цикл while
    while running:
        # проверяем не касается ли голова тела
        if snake[0] in snake[1: ]:
            break
        changed_direction = False
        # ждем
        pg.time.wait(wait_time)
        # обработка событий
        events = pg.event.get()  # получаем список событий
        for event in events:
            if event.type == pg.QUIT:  # если тип события - нажатие на крестик
                running = False
            elif event.type == pg.KEYDOWN and not changed_direction: # если тип события нажатие на клавишу
                # на какую клавишу нажали
                if event.key == pg.K_w and direction != "down":
                    direction = "up"
                elif event.key == pg.K_s and direction != "up":
                    direction = "down"
                elif event.key == pg.K_d and direction != "left":
                    direction = "right"
                elif event.key == pg.K_a and direction != "right":
                    direction = "left"
                changed_direction = True
        # перемещаем змею
        move_snake(snake, direction)
        # если съели яблоко
        if snake[0] == apple:
            apples += 1
            apple = random_apple(snake)
            wait_time -= time_change
            text_image = font.render(f"яблоки: {apples}", False, (255, 255, 255))
            if wait_time < 0:
                wait_time = 0
            # дз добавить хвост
            move_snake(snake, direction, grow=True)
        # перерисовать экран
        screen.fill("black")
        draw_apple(screen, cells, apple)
        draw_snake(screen, cells, snake)
        # рисуем текст
        screen.blit(text_image, (850, 0))
        pg.display.flip()
    game_over(screen)


def draw_snake(screen, cells, snake):
    try:
        pg.draw.rect(screen, (255, 0, 0), cells[snake[0]], 10)
    except KeyError:
        game_over(screen)
        quit()
    for cord_snake in snake[1:]:
        pg.draw.rect(screen, (255, 120, 0), cells[cord_snake], 10)


def draw_apple(screen, cells, apple):
    pg.draw.rect(screen, (0, 255, 0), cells[apple], 10)


def move_snake(snake, direction, grow=False):
    last_pos = snake[0]
    for i in range(1, len(snake)):
        snake[i], last_pos = last_pos, snake[i]
    if direction == "up":
        snake[0] = (snake[0][0], snake[0][1] - 1)
    elif direction == "left":
        snake[0] = (snake[0][0] - 1, snake[0][1])
    elif direction == "right":
        snake[0] = (snake[0][0] + 1, snake[0][1])
    elif direction == "down":
        snake[0] = (snake[0][0], snake[0][1] + 1)

    if grow:
        snake.append(last_pos)


# возвращает координаты яблока
def random_apple(snake) -> tuple[int,int]:
    # случайный x
    x = randint(0, 99)
    # случайный y
    y = randint(0,79)
    # если на месте змеи
    while (x, y) in snake:
        # зарандомим другую точку
        x = randint(0, 99)
        y = randint(0, 79)
    return (x, y)


def create_window():
    # создать окно
    screen = pg.display.set_mode(SIZE)
    # изменить название окна
    pg.display.set_caption("Змейка версия 0.0.1")
    # изменить иконку
    icon = pg.image.load("картинки для змейки/snake.jpeg")
    pg.display.set_icon(icon)
    return screen


def game_over(screen):
    # создать шрифт
    font = pg.font.SysFont("comicsansms", 40, False, False)
    # создать картинку по шрифту
    text_image = font.render("Игра окончена", True, (255, 255, 255))
    # нарисовать картинку
    screen.blit(text_image, (350, 300))
    pg.display.flip()
    running = True
    while running:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                running = False


# точка входа в программу
if __name__ == '__main__':
    main()
