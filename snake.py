import pygame
import random
import time
import numpy as np
import sys
should_add = False
done = False
pygame.init()
size = 800, 800
screen = pygame.display.set_mode(size)
board = [[(0, 0, 0) for _ in range(100)] for _ in range(100)]

#board[x][y] -> color
def display_board():
    for line, x in zip(board, range(0, 800, 8)):
        for color, y in zip(line, range(0, 800, 8)):
            square = pygame.Rect(x, y, 10, 10)
            pygame.draw.rect(screen, color, square)


class draw:
    def __init__(self, screen):
        self.screen = screen
        self.last_words_drawed = ''
        self.old_where_to_draw = (0, 0)
        self.last_size = 36

    def draw(self, words, size=36, color=(255, 255, 255), flip=False):
        screen.fill((0, 0, 0))
        where_to_draw = [0, 0]
        for word in words.split('\n'):
            self.draw_words(word, where_to_draw, size, color, flip)
            where_to_draw[1] += 30
        pygame.display.flip()

    def draw_words(self, word, where_to_draw=(0, 0), size=36, color=(255, 255, 255), flip=False):

        font = pygame.font.Font(None, size)
        area_of_text = font.size(word)
        area_that_could_be_blit = pygame.Rect(where_to_draw, area_of_text)

        text = font.render(word, 1, color)
        screen.blit(text, where_to_draw)

def die():
    global done
    global board
    board = [[(0, 0, 0) for _ in range(100)] for _ in range(100)]
    done = True

def win():
    print('you won!')
    die()


def user_movements(snake):
    move = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                snake.change_directions(np.array([0, 1]))
            elif event.key == pygame.K_UP:
                snake.change_directions(np.array([0, -1]))
            elif event.key == pygame.K_LEFT:
                snake.change_directions(np.array([-1, 0]))
            elif event.key == pygame.K_RIGHT:
                snake.change_directions(np.array([1, 0]))

def p():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            return True
    return False

class Snake:
    def __init__(self):
        self.squares_to_grow = 0
        def create_blocks():
            x = [50] * 5
            y = range(50, 45, -1)
            tuples = list(zip(x, y))
            arrays = []
            for tup in tuples:
                arrays.append(np.array(tup))
            #print(arrays)
            return arrays
        self.blocks = create_blocks() # [0] is the head
        self.direction = np.array([0, 1]) # x = [0], y = [1]
        self.next_direction = [0, 1]

    def move(self, grow):
        self.direction = self.next_direction
        self.squares_to_grow += grow
        def didnt_colide(self):
            if 0 <= self.blocks[0][0] <= 99:
                if 0 <= self.blocks[0][1] <= 99:
                    all_squares = list(map(tuple, self.blocks))
                    all_set_squares = list(set(list(map(tuple, self.blocks))))
                    all_squares.sort()
                    all_set_squares.sort()
                    if all_squares == all_set_squares:
                        return True
            return False

        def move_head(self):
            new_square = self.direction + self.blocks[0]
            self.blocks.insert(0, new_square)

        def draw_on_board(self, color=(0, 255, 0)):
            for x, y in self.blocks:
                try:
                    board[x][y] = color
                except IndexError:
                    d.draw('You lost.')
                    time.sleep(1.5)
                    die()
                if color == (0, 255, 0):
                    color = (255, 255, 255)

        def delete_tail(self):
            draw_on_board(self, color=(0, 0, 0))
            self.blocks.pop()

        if didnt_colide(self):
            move_head(self)
            if self.squares_to_grow <= 1:
                delete_tail(self)
            else:
                self.squares_to_grow -= 1
            draw_on_board(self)
        else:
            draw_on_board(self, color=(0, 0, 0))
            d.draw('You lost.')
            time.sleep(1.5)
            die()

    def change_directions(self, new_direction):
        for now, new in zip(self.direction, new_direction):
            if now == new:
                return False
        self.next_direction = new_direction
        return True

class Apple:
    def __init__(self, snake):
        self.squares = 1
        self.color = [255, 0, 0]
        self.move(snake)
        self.eaten = False
        self.delete = False

    def get_choice(self):
        return random.randrange(1, 99), random.randrange(1, 99)

    def move(self, snake):
        done = False
        while not done:
            choice_x, choice_y = self.get_choice()
            # if [choice_x, choice_y] not in snake.blocks:
            # if not np.isin(np.array([choice_x, choice_y]), snake.blocks).any():
            if not (np.array(snake.blocks)[:,None] == [choice_x, choice_y]).all(-1).any(-1).any():
            #if not ([choice_x, choice_y] in np.array(snake.blocks)):
                done = True
        self.x = choice_x
        self.y = choice_y
        self.draw()

    def draw(self, color=True):
        if color == True:
            color = self.color
        #print(f'and inside, the color is {color}')
        board[self.x][self.y] = color

    def on_eaten(self):
        pass

    def every_tick(self):
        pass

    def check(self, snake):
        #print(snake.blocks[0])
        is_equal = snake.blocks[0] == np.array([self.x, self.y])
        self.every_tick()
        if is_equal.all():
            # print('eaten!')
            # self.draw([0, 0, 0])
            display_board()
            self.eaten = True
            self.on_eaten()
            return self.squares
        else:
            return 0

class TimedApple(Apple):
    def __init__(self, snake):
        #print('here')
        self.squares = 0
        self.color = [255, 96, 101]
        self.colored_color = [255, 96, 101]
        self.start_time = time.time()
        self.move(snake)
        self.eaten = False
        self.secs_until_colored = 2.5
        self.secs_until_black = 2
        self.loops_executed = 1
        self.delete = False

    def on_eaten(self):
        snake.squares_to_grow += 4

    def get_delay(self):
        self.secs_until_black = self.secs_until_black / 2
        self.secs_until_colored = self.secs_until_colored / 2
    def every_tick(self):
        t = (time.time() - self.start_time)
        #print(t)
        #print(self.color)
        #if t > 5:
        if self.secs_until_colored < 2.5/60: # Fastest eyes can see
            self.draw([0, 0, 0])
            self.delete = True
        elif t > self.secs_until_colored:
            self.start_time = time.time()
            self.loops_executed += 1
            self.get_delay()
            self.color = self.colored_color
            #print(self.secs_until_black)

            #print('\nPINK')
            self.draw()
        elif t > self.secs_until_black:
            #print('\nBLACK')
            self.color = [0, 0, 0]
            self.draw()


class GoldenApple(Apple):
    def __init__(self, snake):
        #super(Apple, self).__init__(snake)
        self.squares = 3.5 # every other one go 4 (start with 4)
        self.color = [255, 255, 102]
        self.move(snake)
        self.eaten = False
        self.delete = False

    def get_choice(self):
        def get_sides():
            return random.randrange(0, 100), random.choice([0, 99])
        reverse = random.choice([-1, 1])
        return get_sides()[::reverse]

    def on_eaten(self):
        global should_add
        should_add = True

def create_apples():
    apple = Apple(snake)
    g = random.randrange(0, 11)
    if g == 0:
        goldenapple = GoldenApple(snake)
        apples = np.array([apple, goldenapple])
    else:
        apples = np.array([apple])
        #apples = np.array([Apple(snake) for _ in range(10000)])
    return apples

def clear_apples(apples):
    for apple in apples:
        if not apple.eaten:
            apple.draw([0, 0, 0])

while True:
    snake = Snake()
    apples = create_apples()
    d = draw(screen)
    pygame.event.get()
    d.draw('How to play:\nUse the arrow keys to change directions.\nGo to the apple.\n\nHit any key to play')
    while not p():
        pass
    while not done:
        if should_add == True:
            apples = np.append(apples, [TimedApple(snake) for _ in range(10)])
            should_add = False
        user_movements(snake)
        squares_grown = sum([apple.check(snake) for apple in apples])
        locations = []
        for apple, location in zip(apples, range(len(apples) - 1)):
            #print(type(apple))
            if apple.delete == True:
                locations.append(location)
        apples = np.delete(apples, locations)

        snake.move(squares_grown)
        if squares_grown > 0:
            clear_apples(apples)
            apples = create_apples()
        display_board()
        pygame.display.flip()
        time.sleep(1/26)
    done = False
    board = [[(0, 0, 0) for _ in range(100)] for _ in range(100)]
