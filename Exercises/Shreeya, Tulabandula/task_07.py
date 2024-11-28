# to solve todays exercise you will need a fully functional int-computer,
# including relative offset features. If you did not complete the last exercise
# please ask one of the other students to share their implementation of the
# int-computer with you.
#
#
# We will run 'breakout' -- the arcade game -- on our simulated computer. 
# (https://en.wikipedia.org/wiki/Breakout_(video_game))
# The code for the computer will be provided under data/breakout_commands.txt
# the code will produce outputs in triplets. every triplet that is output
# specifies (x-position, y-position, tile_type).
# tiles can be of the following types:
# 0: empty tile
# 1: wall. walls are indestructible
# 2: block. blocks can be destroyed by the ball
# 3: paddle. the paddle is indestructible
# 4: ball. the ball moves diagonally and bounces off objects
# 
# EXAMPLE:
# a sequence of output values like 1, 2, 3, 6, 5, 4 would
#  - draw a paddle (type 3) at x=1, y=2
#  - draw the ball (type 4) at x=6, y=5
#
#
# PART 1:
# run the game until it exits. Analyse the output produced during the run, and create
# a visual representation (matplotlib or ascii-art are possibilities here...) of the screen display.
# mark the different tile types as different colors or symbols. Upload the picture with your PR.
#
# PART 2:
# The game didn't actually run in part 1, it just drew a single static screen.
# Change the first instruction of the commands from 1 to 2. Now the game will actually run.
# when the game actually runs you need to provide inputs to steer the paddle. whenever the computer
# requests you to provide an input, you can chose to provide
# -  0: the paddle remains in position
# - -1: move the paddle to the left
# - +1: move the paddle to the right
#
# the game also outputs a score. when an output triplet is in position (-1, 0) the third value of
# the triplet is not a tile type, but your current score.
# You need to beat the game by breaking all tiles without ever letting the ball cross the bottom 
# edge of the screen. What is your high-score at the end of the game? provide the score as part of your PR.
#
# BONUS: (no extra points, just for fun)
# make a movie of playing the game :)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import to_rgb

class IntComputer:
    def __init__(self, program):
        self.memory = program + [0] * 10000  
        self.pointer = 0
        self.relative_base = 0
        self.input_queue = []
        self.output_queue = []
        self.halted = False

    def get_param(self, mode, offset):
        addr = self.pointer + offset
        if mode == 0:  
            return self.memory[self.memory[addr]]
        elif mode == 1:  
            return self.memory[addr]
        elif mode == 2: 
            return self.memory[self.relative_base + self.memory[addr]]

    def set_param(self, mode, offset, value):
        addr = self.pointer + offset
        if mode == 0:  
            self.memory[self.memory[addr]] = value
        elif mode == 2: 
            self.memory[self.relative_base + self.memory[addr]] = value

    def execute(self):
        while not self.halted:
            instruction = self.memory[self.pointer]
            opcode = instruction % 100
            modes = [(instruction // 10 ** i) % 10 for i in range(2, 5)]

            if opcode == 1: 
                self.set_param(modes[2], 3, self.get_param(modes[0], 1) + self.get_param(modes[1], 2))
                self.pointer += 4
            elif opcode == 2:  
                self.set_param(modes[2], 3, self.get_param(modes[0], 1) * self.get_param(modes[1], 2))
                self.pointer += 4
            elif opcode == 3:
                if not self.input_queue:
                    return 
                self.set_param(modes[0], 1, self.input_queue.pop(0))
                self.pointer += 2
            elif opcode == 4:  
                self.output_queue.append(self.get_param(modes[0], 1))
                self.pointer += 2
            elif opcode == 5: 
                if self.get_param(modes[0], 1) != 0:
                    self.pointer = self.get_param(modes[1], 2)
                else:
                    self.pointer += 3
            elif opcode == 6:  
                if self.get_param(modes[0], 1) == 0:
                    self.pointer = self.get_param(modes[1], 2)
                else:
                    self.pointer += 3
            elif opcode == 7:  
                self.set_param(modes[2], 3, int(self.get_param(modes[0], 1) < self.get_param(modes[1], 2)))
                self.pointer += 4
            elif opcode == 8:  
                self.set_param(modes[2], 3, int(self.get_param(modes[0], 1) == self.get_param(modes[1], 2)))
                self.pointer += 4
            elif opcode == 9:  
                self.relative_base += self.get_param(modes[0], 1)
                self.pointer += 2
            elif opcode == 99:  
                self.halted = True
            else:
                raise ValueError(f"Unknown opcode {opcode}")

class BreakoutGame:
    def __init__(self, program):
        self.computer = IntComputer(program)
        self.grid = {}  
        self.score = 0
        self.ball_position = (0, 0)
        self.paddle_position = (0, 0)

    def update_grid(self, output):
        for i in range(0, len(output), 3):
            x, y, tile_type = output[i:i + 3]
            if x == -1 and y == 0: 
                self.score = tile_type
            else:
                self.grid[(x, y)] = tile_type
                if tile_type == 4:  
                    self.ball_position = (x, y)
                elif tile_type == 3: 
                    self.paddle_position = (x, y)

    def compute_paddle_input(self):
        ball_x, _ = self.ball_position
        paddle_x, _ = self.paddle_position
        if ball_x < paddle_x:
            return -1 
        elif ball_x > paddle_x:
            return 1  
        return 0  

    def render(self):
        max_x = max(pos[0] for pos in self.grid)
        max_y = max(pos[1] for pos in self.grid)
        grid_array = np.zeros((max_y + 1, max_x + 1), dtype=int)

        for (x, y), tile_type in self.grid.items():
            grid_array[y, x] = tile_type
        return grid_array


TILE_COLORS = {
    0: 'black',  
    1: 'white',  
    2: 'pink',   
    3: 'orange', 
    4: 'green'   
}

def animate_game(game):
    fig, ax = plt.subplots()
    ax.axis('off')

    img = ax.imshow(np.zeros((1, 1, 3)), interpolation='nearest', origin='upper')
    score_text = ax.text(0.02, 0.95, f"Score: 0", color='white', fontsize=12, transform=ax.transAxes)

    def play_game(frame):
        if not game.computer.halted:
            game.computer.execute()
            output = game.computer.output_queue
            game.computer.output_queue = []
            game.update_grid(output)

            if not game.computer.halted:
                paddle_input = game.compute_paddle_input()
                game.computer.input_queue.append(paddle_input)

            new_grid = game.render()
            color_grid = np.zeros((new_grid.shape[0], new_grid.shape[1], 3))
            for tile_type, color_name in TILE_COLORS.items():
                color_grid[new_grid == tile_type] = to_rgb(color_name)
            img.set_data(color_grid)

            score_text.set_text(f"Score: {game.score}")

            return [img, score_text]

    ani = FuncAnimation(fig, play_game, interval=50, blit=True)
    plt.show()

def load_program(file_path):
    with open(file_path, 'r') as f:
        return list(map(int, f.read().strip().split('\n')))

program = load_program('data/breakout_commands.txt')

program[0] = 2  #part 2 updating first command from 1 to 2.

game = BreakoutGame(program)
animate_game(game)
