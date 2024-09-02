from random import choice, randint
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
DIRECTION_UP = (0, -1)
DIRECTION_DOWN = (0, 1)
DIRECTION_LEFT = (-1, 0)
DIRECTION_RIGHT = (1, 0)

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
        self.position = []
        self.body_color = body_color

    def draw_cell(self, position):
        """Отрисовка отдельной ячейки."""
        cell_rectangle = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, cell_rectangle)
        pygame.draw.rect(screen, BORDER_COLOR, cell_rectangle, 1)


class Snake(GameObject):
    """Класс, описывающий змейку и её поведение."""

    def __init__(self):
        super().__init__(SNAKE_COLOR)
        self.positions = [(GRID_SIZE * 5, GRID_SIZE * 5)]
        self.current_direction = choice([DIRECTION_RIGHT, DIRECTION_DOWN, DIRECTION_LEFT, DIRECTION_UP])
        self.length = 1
        self.next_direction = None

    def draw(self):
        """Отрисовка всех ячеек змейки."""
        for position in self.positions:
            self.draw_cell(position)

    def move(self):
        """Обновление позиции змейки и отрисовка изменений."""
        current_head_x, current_head_y = self.positions[0]
        direction_x, direction_y = self.current_direction
        new_head_position = ((current_head_x + direction_x * GRID_SIZE) % SCREEN_WIDTH,
                             (current_head_y + direction_y * GRID_SIZE) % SCREEN_HEIGHT)

        self.positions.insert(0, new_head_position)
        self.draw_cell(new_head_position)  # Отрисовка новой головы

        if len(self.positions) > self.length:
            tail_position = self.positions.pop()
            self.draw_cell(tail_position)  # Затирание старого хвоста

    def grow(self):
        """Отвечает за увеличение длины змейки."""
        self.length += 1

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.current_direction = self.next_direction
            self.next_direction = None

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.positions = [(GRID_SIZE * 5, GRID_SIZE * 5)]
        self.current_direction = DIRECTION_RIGHT
        self.length = 1
        self.next_direction = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0] if self.positions else None

    def check_collision_with_self(self):
        """Проверяет столкновение головы змейки с её телом."""
        if self.get_head_position() in self.positions[1:]:
            return True
        return False


class Apple(GameObject):
    """Класс, описывающий яблоко и действия с ним."""

    def __init__(self):
        super().__init__(APPLE_COLOR)
        self.position = self.randomize_position([])

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности."""
        self.draw_cell(self.position)

    def randomize_position(self, snake_positions):
        """Устанавливает случайное положение яблока, избегая совпадений с позицией змейки."""
        while True:
            new_position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                            randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if new_position not in snake_positions:
                self.position = new_position
                break
        return self.position


def handle_keys(snake):
    """Обрабатывает нажатия клавиш, чтобы изменить направление движения змейки."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.current_direction != DIRECTION_DOWN:
                snake.next_direction = DIRECTION_UP
            elif event.key == pygame.K_DOWN and snake.current_direction != DIRECTION_UP:
                snake.next_direction = DIRECTION_DOWN
            elif event.key == pygame.K_LEFT and snake.current_direction != DIRECTION_RIGHT:
                snake.next_direction = DIRECTION_LEFT
            elif event.key == pygame.K_RIGHT and snake.current_direction != DIRECTION_LEFT:
                snake.next_direction = DIRECTION_RIGHT


def main():
    """Основной цикл игры."""
    pygame.init()
    snake = Snake()
    apple = Apple()

    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.check_collision_with_self():
            pygame.quit()
            raise SystemExit("Game Over")

        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.randomize_position(snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()
        clock.tick(SNAKE_SPEED)


if __name__ == '__main__':
    main()