import time

import pygame
from core import SnakeBoard

# CONSTANTS
WINDOW_SIZE = 500
GRID_COLOR = (100, 100, 100)
GRID_SIZE = 20
SNAKE_INIT_LEN = 12
SNAKE_BODY_COLOR = (255, 255, 0)
SNAKE_HEAD_COLOR = (255, 100, 0)
FOOD_COLOR = (255, 0, 0)
FOOD_SIZE = GRID_SIZE // 2 - 3
#

# WORKING_VARIABLES
end_program = False
sb = SnakeBoard(board_size=WINDOW_SIZE // GRID_SIZE, snake_init_len=SNAKE_INIT_LEN)
current_heading_direction = 'r'
prev_heading_direction = current_heading_direction
#

pygame.init()

screen = pygame.display.set_mode([WINDOW_SIZE, WINDOW_SIZE])
clock = pygame.time.Clock()

screen.fill((0, 0, 0))
pygame.display.set_caption('Snake Game')


# Functions
def draw_snake(snake_board):
    for coord in snake_board.snake.iter_through_body_cells():
        pygame.draw.rect(screen,
                         SNAKE_BODY_COLOR,
                         [
                             coord[0] * GRID_SIZE,
                             coord[1] * GRID_SIZE,
                             GRID_SIZE,
                             GRID_SIZE
                         ])


def draw_food(snake_board):
    if snake_board.food_coordinate[0] is None:
        return False

    pygame.draw.circle(screen,
                       FOOD_COLOR,
                       [
                           snake_board.food_coordinate[0] * GRID_SIZE + (GRID_SIZE // 2),
                           snake_board.food_coordinate[1] * GRID_SIZE + (GRID_SIZE // 2)
                       ],
                       FOOD_SIZE)


#


# Main Loop
while not end_program:
    if not sb.snake.is_alive:
        end_program = True

    if sb.food_coordinate[0] is None:
        sb.initialize_food()
        sb.score += 10

    # Drawing horizontal grid lines
    screen.fill((0, 0, 0))
    for x in range(1, WINDOW_SIZE // GRID_SIZE):
        pygame.draw.line(screen,
                         GRID_COLOR,
                         (GRID_SIZE * x, 0),
                         (GRID_SIZE * x, WINDOW_SIZE))

    for y in range(1, WINDOW_SIZE // GRID_SIZE):
        pygame.draw.line(screen,
                         GRID_COLOR,
                         (0, GRID_SIZE * y),
                         (WINDOW_SIZE, GRID_SIZE * y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            end_program = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                current_heading_direction = 'u'
            elif event.key == pygame.K_DOWN:
                current_heading_direction = 'd'
            elif event.key == pygame.K_LEFT:
                current_heading_direction = 'l'
            elif event.key == pygame.K_RIGHT:
                current_heading_direction = 'r'

    print("Score:", sb.score)

    if sb.snake.move(current_heading_direction) == 0:  # Move Snake
        current_heading_direction = prev_heading_direction
    else:
        prev_heading_direction = current_heading_direction

    draw_snake(sb)
    draw_food(sb)
    clock.tick(10)  # Limit to 60 FPS
    pygame.display.flip()  # Screen Update

pygame.quit()
