import random
from core.sound_effects import play_collision, play_apple_bite


class Snake:
    """
    Here head, tail, and rest of the body will be
    represented as coordinate (y, x)
    """

    class Cell:
        def __init__(self, coordinate, next_=None, prev_=None):
            self.coordinate = coordinate
            self.next = next_
            self.prev = prev_

    def __init__(self, box_size, init_len=5):
        if init_len < 2:
            raise Exception("Snake must be at least of size 2")
        self.box_size = box_size
        self.food_location = [None, None]
        self.head = self.Cell(coordinate=[0, init_len - 1])

        _iter_cell = self.head

        self.tail = None
        for i in range(init_len - 2, -1, -1):
            _iter_cell.next = self.Cell(coordinate=[0, i])
            _iter_cell.next.prev = _iter_cell
            _iter_cell = _iter_cell.next

        self.tail = _iter_cell

        self.is_alive = True  # Blowing life into this being.

    def __contains__(self, item: list):
        cell = self.head.next
        while cell is not None:
            if item == cell.coordinate:
                return True

            cell = cell.next
        return False

    def pop(self):
        removing_cell = self.tail
        self.tail = self.tail.prev
        self.tail.next = None
        removing_cell.prev = None
        return removing_cell.coordinate

    def prepend(self, coordinate):
        self.head.prev = self.Cell(coordinate)
        self.head.prev.next = self.head
        self.head = self.head.prev

    def get_direction_facing(self):
        snake_coordinate = self.head.coordinate
        snake_neck_coordinate = self.head.next.coordinate

        if snake_coordinate[0] == snake_neck_coordinate[0]:  # Horizontal
            if snake_coordinate[1] > snake_neck_coordinate[1]:  # Facing Down
                return 3
            else:  # Facing Up
                return 0
        else:  # Vertical
            if snake_coordinate[0] > snake_neck_coordinate[0]:  # Facing Right
                return 2
            else:  # Facing Left
                return 1

    def move(self, direction):
        """
        :param direction: l, r, u, d
        :return: None
        """
        if direction == 'u':
            next_coordinate = [self.head.coordinate[0], self.head.coordinate[1] - 1]
        elif direction == 'd':
            next_coordinate = [self.head.coordinate[0], self.head.coordinate[1] + 1]
        elif direction == 'l':
            next_coordinate = [self.head.coordinate[0] - 1, self.head.coordinate[1]]
        elif direction == 'r':
            next_coordinate = [self.head.coordinate[0] + 1, self.head.coordinate[1]]
        else:
            raise Exception("Invalid Direction")

        if self.head.next.coordinate == next_coordinate:
            print('Trying to move backward')
            return 0  # Signifies cannot move backward

        if -1 in next_coordinate or max(next_coordinate) >= self.box_size:
            self.is_alive = False
            play_collision()
            print("Collision with wall!")
            return -1  # Signifies Collision with Wall

        if next_coordinate in self:
            self.is_alive = False
            print("Bit Myself!")
            return -2  # Signifies Collision with itself

        if next_coordinate != self.food_location:
            self.pop()
        else:
            play_apple_bite()
            self.food_location[0] = None
            self.food_location[1] = None

        self.prepend(next_coordinate)

    def iter_through_body_cells(self):
        curr_cell = self.head.next
        while curr_cell:
            yield curr_cell.coordinate
            curr_cell = curr_cell.next


class SnakeBoard:
    DIRECTIONS = ['l', 'r', 'u', 'd']
    score = 0

    def __init__(self, board_size, snake_init_len):
        self.snake = Snake(box_size=board_size, init_len=snake_init_len)
        self.SIZE = board_size
        self.food_coordinate = self.snake.food_location
        self.initialize_food()

    def initialize_food(self):
        self.food_coordinate = self.snake.food_location = [random.randint(0, self.SIZE - 1), random.randint(0, self.SIZE - 1)]
        check = True
        while check:
            check = False
            for coord in self.snake.iter_through_body_cells():
                if coord[0] == self.food_coordinate[0] and coord[1] == self.food_coordinate[1]:
                    self.food_coordinate = self.snake.food_location = [random.randint(0, self.SIZE - 1), random.randint(0, self.SIZE - 1)]
                    check = True
                    break
