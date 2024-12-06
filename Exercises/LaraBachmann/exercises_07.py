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

import operator
from collections import defaultdict
from matplotlib import pyplot as plt
import numpy as np


def read_numbers_from_file(filepath: str) -> defaultdict:
    #  reads numbers from a file and stores them in a defaultdict
    memory = defaultdict(int)
    with open(filepath, 'r') as file:
        for i, line in enumerate(file):
            try:
                memory[i] = int(line.strip())
            except ValueError:
                print(f"Invalid number in line {i + 1}: '{line.strip()}")
    return memory


def get_parameter(memory, parameter, mode, relative_offset, is_write=False):
    #  retrieves parameters for the intcode based on the mode
    if mode == '1':
        if is_write:
            raise ValueError("Immediate mode cannot be used for writes.")
        return memory[parameter]
    elif mode == '2':
        address = relative_offset + memory[parameter]
        return address if is_write else memory[address]
    else:
        address = memory[memory[parameter]] if not is_write else memory[parameter]
        return address
    

def determine_paddle_move(ball_x, paddle_x):
    #  deteremines the paddle move based on ball and paddle positions
    if ball_x < paddle_x:
        return -1
    elif ball_x > paddle_x:
        return 1
    else:
        return 0

 
def visualize_screen(triplets, high_score):
    #  visualizes the game screen using matplotlib based on triplets of data
    plt.clf()  # deletes the current screen
    max_x = max(triplet[0] for triplet in triplets if triplet[0] >= 0)
    max_y = max(triplet[1] for triplet in triplets if triplet[1] >= 0)

    #  initialize the grid
    grid = np.zeros((max_y + 1, max_x + 1), dtype=int)
    for x, y, tile_type in triplets:
        if x >= 0 and y >= 0:
            grid[y, x] = tile_type

    #  add tiles to the plot
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            tile_type = grid[y, x]
            if tile_type == 1:  # wall
                plt.gca().add_patch(plt.Rectangle((x, y), 1, 1, color="black"))
            if tile_type == 2:  # block
                plt.gca().add_patch(plt.Rectangle((x, y), 0.9, 0.9, color="pink"))
            if tile_type == 3:  # paddle
                plt.gca().add_patch(plt.Rectangle((x, y), 1, 1, color="grey"))
            if tile_type == 4:  # ball
                plt.gca().add_patch(plt.Circle((x + 0.5, y + 0.5), 0.3, color="black"))

    plt.text(max_x / 2, -0.5, f"Score: {high_score}", color="black", fontsize=16, fontweight="bold", ha="center", va="bottom")
    plt.axis('off')
    plt.xlim(0, max_x + 1)
    plt.ylim(0, max_y + 1)
    plt.gca().invert_yaxis()
    plt.pause(0.000000001)


def simulated_computer(memory):
    pointer = 0
    relative_offset = 0
    triplet = []
    triplets = []
    high_score = 0

    opcode_map = {
        1: operator.add,
        2: operator.mul,
        7: lambda x, y: int(x < y),
        8: lambda x, y: int(x == y)
    }

    plt.ion()

    while True:
        instruction = str(memory[pointer]).zfill(5)
        opcode = int(instruction[-2:])
        modes = instruction[2::-1]
        
        if opcode in opcode_map:
            param1 = get_parameter(memory, pointer + 1, modes[0], relative_offset)
            param2 = get_parameter(memory, pointer + 2, modes[1], relative_offset)
            output_position = get_parameter(memory, pointer + 3, modes[2], relative_offset, is_write=True)
            
            memory[output_position] = opcode_map[opcode](param1, param2)
            pointer += 4

        elif opcode == 3:
            #  automatic version
            ball_x = next((t[0] for t in triplets if t[2] == 4), 0)
            paddle_x = next((t[0] for t in triplets if t[2] == 3), 0)

            move = determine_paddle_move(ball_x, paddle_x)
            target_address = get_parameter(memory, pointer + 1, modes[0], relative_offset, is_write=True)
            memory[target_address] = move

            #  manual version
            """while True:
                try:
                    print("Choose a number:")
                    print("- 0: the paddle remains in position")
                    print("- -1: move the paddle to the left")
                    print("- +1: move the paddle to the right")
                   
                    number_from_input = int(input("Please give me an input: "))
                    
                    if number_from_input in [-1, 0, 1]:
                        target_address = get_parameter(memory, pointer + 1, modes[0], relative_offset, is_write=True)
                        memory[target_address] = number_from_input
                        break
                    else:
                        print("Invalid input. Please choose -1, 0, or 1.")
                except ValueError:
                    print("Invalid input. Please enter an integer.")"""

            pointer += 2

        elif opcode in [4, 9]:
            param1 = get_parameter(memory, pointer + 1, modes[0], relative_offset)

            if opcode == 4:
                triplet.append(param1)

                if len(triplet) == 3:
                    if triplet[0] == -1 and triplet[1] == 0:
                        high_score = triplet[2]
                        # print(high_score)
                    else:
                        triplets = [t for t in triplets if not (t[2] in [3, 4] and t[2] == triplet[2])]
                        triplet_tuple = tuple(triplet)
                        triplets.append(triplet_tuple)
                        visualize_screen(triplets, high_score)
                    
                    triplet = []

            elif opcode == 9:
                relative_offset += param1
                
            pointer += 2

        elif opcode in [5, 6]:
            param1 = get_parameter(memory, pointer + 1, modes[0], relative_offset)
            param2 = get_parameter(memory, pointer + 2, modes[1], relative_offset)

            if opcode == 5 and param1 != 0:
                pointer = param2
            elif opcode == 6 and param1 == 0:
                pointer = param2
            else: 
                pointer += 3
        
        elif opcode == 99:
            print(f'Program finished. Your High Score is {high_score}.\n') 
            plt.ioff()
            visualize_screen(triplets, high_score)
            return memory[0]
        
        else:
            raise ValueError('No opcode is defined for the current numerical value. Program aborted.')


numbers = read_numbers_from_file('/Users/larabachmann/Desktop/School/Programming_and_Problemsolving_Python/ppp-2024/Exercises/LaraBachmann/breakout_commands.txt')
simulated_computer(numbers)
#  high score: 17159