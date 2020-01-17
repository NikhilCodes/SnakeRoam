import time

import pygame
from core import SnakeBoard


# SAFE-CONSTANTS
WINDOW_SIZE = 500
WINDOW_MARGIN = (40, 30, 20, 10)
GRID_COLOR = (100, 100, 100)
GRID_SIZE = 20
FLOOR_COLOR_1 = (60, 155, 0)
FLOOR_COLOR_2 = (60, 120, 0)
SNAKE_INIT_LEN = 12
SNAKE_BODY_COLOR = (255, 255, 0)
SNAKE_HEAD_PATH = 'res/snake-head.png'
FOOD_COLOR = (255, 0, 0)
FOOD_SIZE = GRID_SIZE // 2 - 3
#

# UNSAFE-CONSTANTS
angles = {
    1: 0,
    0: 270,
    3: 90,
    2: 180
}

pygame.init()

screen = pygame.display.set_mode([WINDOW_SIZE, WINDOW_SIZE + 50])
clock = pygame.time.Clock()
snake_head = pygame.image.load(SNAKE_HEAD_PATH)
snake_head = pygame.transform.scale(snake_head, (GRID_SIZE, GRID_SIZE))

screen.fill((0, 0, 0))
pygame.display.set_caption('Snake Game')

score_font = pygame.font.SysFont('Comic Sans MS', 30)


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

    coord = snake_board.snake.head.coordinate
    snake_head_tmp = pygame.transform.rotate(snake_head, angles[snake_board.snake.get_direction_facing()])
    screen.blit(snake_head_tmp, (
        coord[0] * GRID_SIZE,
        coord[1] * GRID_SIZE,
    ))


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


def main():
    session_score = 0
    play_button_size = (100, 50)
    screen.fill((0, 0, 0))

    menu_font = pygame.font.SysFont('Comic Sans MS', 50)
    prev_score_font = pygame.font.SysFont('Comic Sans MS', 40)

    def show_menu():
        screen.fill((0, 0, 0))
        menu_play_text = menu_font.render("Play!", True, (0, 0, 0))
        prev_score_text = prev_score_font.render("Score: "+str(session_score), False, (255, 255, 255))
        pygame.draw.rect(screen,
                         (100, 255, 0),
                         [
                             (WINDOW_SIZE / 2) - (play_button_size[0] / 2),
                             (WINDOW_SIZE / 2) - (play_button_size[1] / 2),
                             play_button_size[0],
                             play_button_size[1]
                         ])
        screen.blit(menu_play_text, [
            (WINDOW_SIZE / 2) - (play_button_size[0] / 2) + 10,
            (WINDOW_SIZE / 2) - (play_button_size[1] / 2) + 10
        ])

        screen.blit(prev_score_text, [
            (WINDOW_SIZE / 2) - (play_button_size[0] / 2),
            (WINDOW_SIZE / 2) - (play_button_size[1] / 2) + 60
        ])

    show_menu()
    while True:
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                pygame.quit()
                return 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if (WINDOW_SIZE / 2) - (play_button_size[0] / 2) <= mouse_pos[0] <= (WINDOW_SIZE / 2) +\
                        (play_button_size[0] / 2) and (WINDOW_SIZE / 2) - \
                        (play_button_size[1] / 2) <= mouse_pos[1] <= (WINDOW_SIZE / 2) + (play_button_size[1] / 2):
                    session_score = mainloop()

                    show_menu()


# Main Loop
def mainloop():
    current_heading_direction = 'r'
    prev_heading_direction = current_heading_direction
    sb = SnakeBoard(board_size=WINDOW_SIZE // GRID_SIZE, snake_init_len=SNAKE_INIT_LEN)

    while True:
        if not sb.snake.is_alive:
            return sb.score

        if sb.food_coordinate[0] is None:
            sb.initialize_food()
            sb.score += 10

        # Drawing horizontal grid lines
        screen.fill((0, 0, 0))
        for x in range(WINDOW_SIZE//GRID_SIZE):
            for y in range(WINDOW_SIZE//GRID_SIZE):
                if (x + y) % 2:
                    color = FLOOR_COLOR_1
                else:
                    color = FLOOR_COLOR_2
                pygame.draw.rect(screen,
                                 color,
                                 [
                                     x * GRID_SIZE,
                                     y * GRID_SIZE,
                                     GRID_SIZE,
                                     GRID_SIZE
                                 ])

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                return sb.score
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    current_heading_direction = 'u'
                elif event.key == pygame.K_DOWN:
                    current_heading_direction = 'd'
                elif event.key == pygame.K_LEFT:
                    current_heading_direction = 'l'
                elif event.key == pygame.K_RIGHT:
                    current_heading_direction = 'r'

        score_board = score_font.render("Score: " + str(sb.score), True, (255, 255, 255))
        screen.blit(score_board, (15, WINDOW_SIZE + 15))

        if sb.snake.move(current_heading_direction) == 0:  # Move Snake
            current_heading_direction = prev_heading_direction
        else:
            prev_heading_direction = current_heading_direction

        draw_snake(sb)
        draw_food(sb)
        clock.tick(10)  # Limit to 60 FPS
        pygame.display.flip()  # Screen Update


if __name__ == '__main__':
    main()
