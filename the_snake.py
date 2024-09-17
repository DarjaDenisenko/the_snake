from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SNAKE_SPEED = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, body_color=BOARD_BACKGROUND_COLOR):
        self.position = None
        self.body_color = body_color

    def draw(self, position):
        """Оставляем метод пустым."""
        pass

    def draw_cell(self, position, color=None):
        """Отрисовка отдельной ячейки."""
        if position:
            rect = pygame.Rect(position[0], position[1], GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, color or self.body_color, rect)
            # Рисуем контур только для активных клеток змейки или объектов
            if color != BOARD_BACKGROUND_COLOR:  # если не цвет фона
                pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, описывающий змейку и её поведение."""

    def __init__(self):
        super().__init__(SNAKE_COLOR)
        self.old_tail = None  # Атрибут для хранения позиции старого хвоста
        self.reset()

    def draw(self):
        """Отрисовка головы и, если есть, затирание хвоста."""
        # Отрисовываем голову змейки
        self.draw_cell(self.positions[0], SNAKE_COLOR)

        # Затираем старый хвост, если он есть
        if self.old_tail:
            self.draw_cell(self.old_tail, BOARD_BACKGROUND_COLOR)

    def move(self):
        """Обновление позиции змейки."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_head = ((head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH,
                    (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT)

        self.positions.insert(0, new_head)  # Добавляем новую голову

        # Если длина змейки не увеличена, удаляем старый хвост
        if len(self.positions) > self.length:
            # Сохраняем позицию старого хвоста
            self.old_tail = self.positions.pop()
        else:
            self.old_tail = None

    def grow(self):
        """Отвечает за увеличение длины змейки."""
        self.length += 1

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.positions = [(GRID_SIZE * 5, GRID_SIZE * 5)]
        self.direction = RIGHT
        self.length = 1
        self.next_direction = None
        self.old_tail = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0] if self.positions else None

    def check_collision_with_self(self):
        """Проверяет столкновение головы змейки с её телом."""
        return self.get_head_position() in self.positions[1:]


class Apple(GameObject):
    """Класс, описывающий яблоко и действия с ним."""

    def __init__(self):
        super().__init__(APPLE_COLOR)
        self.randomize_position([])

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности."""
        self.draw_cell(self.position)

    def randomize_position(self, snake_positions):
        """Устанавливает случайное положение яблока,
        избегая совпадений с позицией змейки.
        """
        while True:
            new_position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                            randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if new_position not in snake_positions:
                self.position = new_position
                break


def handle_keys(snake):
    """Обрабатывает нажатия клавиш, чтобы изменить
    направление движения змейки.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Основной цикл игры."""
    pygame.init()
    snake = Snake()
    apple = Apple()

    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Проверка на столкновение с собой
        if snake.check_collision_with_self():
            # Перезапуск игры при столкновении с собой
            snake.reset()
            # Обнуляем экран при перезапуске
            screen.fill(BOARD_BACKGROUND_COLOR)
        else:
            # Проверка на съедание яблока
            if snake.get_head_position() == apple.position:
                # Увеличиваем змейку
                snake.grow()
                # Размещаем яблоко на новом месте
                apple.randomize_position(snake.positions)

        # Рисуем змейку и яблоко
        snake.draw()
        apple.draw()

        # Обновляем экран
        pygame.display.update()

        # Ограничение по скорости игры
        clock.tick(SNAKE_SPEED)


if __name__ == '__main__':
    main()
