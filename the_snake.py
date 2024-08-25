from random import choice, randint

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
SPEED = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)


pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()


class GameObject:
    """Это базовый класс, от которого наследуются другие игровые объекты.
    Он содержит общие атрибуты игровых объектов — например,
    эти атрибуты описывают позицию и цвет объекта.
    Этот же класс содержит и заготовку метода для отрисовки
    объекта на игровом поле — draw.
    """

    def __init__(self, body_color=(0, 0, 0)):
        self.position = []
        self.body_color = body_color

    def draw(self):
        """это абстрактный метод, который предназначен для переопределения
        в дочерних классах.
        Этот метод должен определять,
        как объект будет отрисовываться на экране.
        По умолчанию — pass.
        """
        pass


class Snake(GameObject):
    """Класс, унаследованный от GameObject, описывающий змейку и её поведение.
    Этот класс управляет её движением, отрисовкой,
    а также обрабатывает действия пользователя.
    """

    def __init__(self):
        super().__init__(SNAKE_COLOR)
        self.positions = [(GRID_SIZE * 5, GRID_SIZE * 5)]
        self.direction = choice([RIGHT, DOWN, LEFT, UP])
        self.growing = False
        self.next_direction = None
        self.length = 1

    def draw(self):
        """отрисовывает змейку на экране, затирая след"""
        for positions in self.positions:
            rect = pygame.Rect(positions, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def move(self):
        """обновляет позицию змейки (координаты каждой секции),
        добавляя новую голову в начало списка positions
        и удаляя последний элемент, если длина змейки не увеличилась.
        """
        x, y = self.positions[0]
        dx, dy = self.direction
        new_head = ((x + dx * GRID_SIZE) % SCREEN_WIDTH,
                    (y + dy * GRID_SIZE) % SCREEN_HEIGHT)

        if new_head in self.positions[:-1]:
            pygame.quit()
            raise SystemExit("Game Over")

        self.positions = [new_head] + self.positions
        if not self.growing:
            self.positions.pop()
        else:
            self.growing = False

    def grow(self):
        """Отвечает за рост змейки"""
        self.growing = True
        self.length += 1

    def update_direction(self):
        """обновляет направление движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self):
        """сбрасывает змейку в начальное состояние."""
        self.positions = [(GRID_SIZE * 5, GRID_SIZE * 5)]
        self.direction = RIGHT
        self.growing = False
        self.next_direction = None

    def get_head_position(self):
        """возвращает позицию головы змейки
        (первый элемент в списке positions)
        """
        return self.positions[0] if self.positions else None


class Apple(GameObject):
    """класс, унаследованный от GameObject, описывающий яблоко и действия
    с ним. Яблоко должно отображаться в случайных клетках игрового поля.
    """

    def __init__(self):
        super().__init__(APPLE_COLOR)
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self):
        """отрисовывает яблоко на игровой поверхности"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self):
        """устанавливает случайное положение яблока на игровом поле —
        задаёт атрибуту position новое значение.
        Координаты выбираются так,
        чтобы яблоко оказалось в пределах игрового поля.
        """
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)


def handle_keys(snake):
    """обрабатывает нажатия клавиш,
    чтобы изменить направление движения змейки
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
    """Основной цикл игры"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()

    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.positions[0] == apple.position:
            snake.grow()
            apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
