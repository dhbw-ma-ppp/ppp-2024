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

import keyboard
from PIL import Image
import matplotlib.pyplot as plt

with open("data/breakout_commands.txt") as file:
    content = file.read()
    commands = [int(line) for line in content.splitlines()]

background_img = Image.open(r"C:\Users\kevin.siess\Desktop\OneDrive (privat)\OneDrive\Dokumente\Studium\DHBW Mannheim\Modul\Python\Repo\ppp-2024\Exercises\Kevin Siess\background_images.jpeg")
old_tiles = {}
tile_scatter = {}
tiles = {}
score = 0
row_colors = ["red", "orange", "yellow", "purple", "pink", "blue", "green"]
color_map = {0:"none", 1: "black", 3: "white", 4: "white"}
marker_map = {"Wall": "s", "Ball": "o", "Block": "s", "Player": "s"}
ball_scatter = None
ball_position = None
player_position = None

def initialize_game():
    ax.imshow(background_img, extent=[0, 42, 0, 23], aspect="auto")
    ax.axis('off')
    plt.gca().invert_yaxis()

def get_row_color(y):
    return row_colors[y % len(row_colors)]

# def extend_player_tiles(tiles): # increase Player
#     extended_tiles = tiles.copy()
#     for (x, y), tile_type in tiles.items():
#         if tile_type == 3:  
#             extended_tiles[(x - 1, y)] = 3
#             extended_tiles[(x + 1, y)] = 3
#             extended_tiles[(x - 2, y)] = 3
#             extended_tiles[(x + 2, y)] = 3
#     return extended_tiles

def find_tile_differences(old_tiles, new_tiles):
    to_add = {}
    to_remove = []

    for position, tile_type in new_tiles.items():
        if position not in old_tiles or old_tiles[position] != tile_type:
            to_add[position] = tile_type

    for position, old_tile_type in old_tiles.items():
        if position not in new_tiles or new_tiles[position] != old_tile_type:
            to_remove.append(position)
            
    return to_add, to_remove

def update_game_display_partial(tiles, score):
    global old_tiles, ball_scatter, tile_scatter

    if tile_scatter is None:
        tile_scatter = {}

    to_add, to_remove = find_tile_differences(old_tiles, tiles)

    # Entferne alte Tiles
    for position in to_remove:
        if position in tile_scatter:
                tile_scatter[position].remove()
                del tile_scatter[position]

    # Füge neue Tiles hinzu
    for position, tile_type in to_add.items():
        x, y = position
        scatter = None  # Initialisiere scatter

        if tile_type == 1:  # Wall
            scatter = ax.scatter(x, y, c=color_map[tile_type], marker=marker_map["Wall"], s=300)
        elif tile_type == 2:  # Block
            color = get_row_color(y)
            scatter = ax.scatter(x, y, c=color, marker=marker_map["Block"], s=300)
        elif tile_type == 3:  # Player
            scatter = ax.scatter(x, y, c=color_map[tile_type], marker=marker_map["Player"], s=300)
        elif tile_type == 4:  # Ball
            
            ball_scatter = ax.scatter(x, y, c=color_map[tile_type], marker=marker_map["Ball"], s=300)
            scatter = ball_scatter

        if scatter is not None:
            tile_scatter[position] = scatter

    old_tiles = tiles.copy()
    ax.set_title(f"Score: {score}")
    plt.pause(0.001)

def intcode_process(memory):    #initiate Computer
    pointer = 0  
    relative_offset = 0 
    outputs = []
    
    def get_instruction(instruction):   #extract values for opcodes and mode
        opcode = instruction % 100
        param_mode1 = (instruction // 100) % 10
        param_mode2 = (instruction // 1000) % 10
        param_mode3 = (instruction // 10000) % 10
        return opcode, param_mode1, param_mode2, param_mode3

    def check_memoryspace(memory, index):   #dynamically increase memory
        if index >= len(memory):
            memory.extend([0] * (index - len(memory) + 1))

    def get_pointer_position(pointer):  #increase pointer
        check_memoryspace(memory, pointer + 3)
        pos1 = memory[pointer + 1]
        pos2 = memory[pointer + 2]
        pos3 = memory[pointer + 3]
        return pos1, pos2, pos3

    def check_mode(pos, mode, relative_offset): #check mode
        if mode == 0:  # position-mode
            check_memoryspace(memory, pos)
            return memory[pos]
        elif mode == 1:  # immediate-mode
            return pos
        elif mode == 2:  # relative-mode
            check_memoryspace(memory, pos + relative_offset)
            return memory[pos + relative_offset]
        else:
            raise ValueError(f"Invalid Mode: {mode}")

    global score
    while True:
        instruction = memory[pointer]
        opcode, param_mode1, param_mode2, param_mode3 = get_instruction(instruction)
        pos1, pos2, pos3 = get_pointer_position(pointer)

        match opcode:

            case 99:  # end of program
                print(f"Memory: {len(memory)}")
                print(f"Highscore: {score}")
                plt.ioff()
                return outputs

            case 1:  # addition
                if param_mode3 == 2:
                    pos3 += relative_offset
                check_memoryspace(memory, pos3)
                memory[pos3] = check_mode(pos1, param_mode1, relative_offset) + check_mode(pos2, param_mode2, relative_offset)
                pointer += 4

            case 2:  # multiplication
                if param_mode3 == 2:
                    pos3 += relative_offset
                check_memoryspace(memory, pos3)
                memory[pos3] = check_mode(pos1, param_mode1, relative_offset) * check_mode(pos2, param_mode2, relative_offset)
                pointer += 4

            case 3:  # input
                if param_mode1 == 2:
                    pos1 += relative_offset
                check_memoryspace(memory, pos1)
                
                # # manuel-mode
                # if keyboard.is_pressed("left"):
                #     key_input = -1
                # elif keyboard.is_pressed("right"):
                #     key_input = 1
                # else:
                #     key_input = 0

                # Automatische Steuerung
                key_input = 0
                if ball_position and player_position:
                    ball_x, _ = ball_position
                    paddle_x, _ = player_position

                    if ball_x < paddle_x:
                        key_input = -1
                    elif ball_x > paddle_x:
                        key_input = 1

                memory[pos1] = key_input
                pointer += 2

            case 4:  # output
                value = check_mode(pos1, param_mode1, relative_offset)
                outputs.append(value)
                if len(outputs) == 3:
                    x, y, tile_type = outputs
                    if (x, y) == (-1, 0):
                        score = tile_type  # Update score
                    else:
                        tiles[(x, y)] = tile_type  # Update tile

                        if tile_type == 4:  # Ball
                            ball_position = (x, y)

                        elif tile_type == 3:  # Paddle
                            player_position = (x, y)
                    outputs = []  # Reset outputs
                    update_game_display_partial(tiles, score)
                pointer += 2

            case 5:  # jump-if-true
                if check_mode(pos1, param_mode1, relative_offset) != 0:
                    pointer = check_mode(pos2, param_mode2, relative_offset)

                else:
                    pointer += 3

            case 6:  # jump-if-false
                if check_mode(pos1, param_mode1, relative_offset) == 0:
                    pointer = check_mode(pos2, param_mode2, relative_offset)
                    
                else:
                    pointer += 3

            case 7:  # less than
                if param_mode3 == 2:
                    pos3 += relative_offset
                check_memoryspace(memory, pos3)
                result = 1 if check_mode(pos1, param_mode1, relative_offset) < check_mode(pos2, param_mode2, relative_offset) else 0
                memory[pos3] = result
                pointer += 4

            case 8:  # equals
                if param_mode3 == 2:
                    pos3 += relative_offset
                check_memoryspace(memory, pos3)
                result = 1 if check_mode(pos1, param_mode1, relative_offset) == check_mode(pos2, param_mode2, relative_offset) else 0
                memory[pos3] = result
                pointer += 4

            case 9:  # adjust relative
                relative_offset += check_mode(pos1, param_mode1, relative_offset)
                pointer += 2

            case _:  # Error
                raise ValueError(f"Invalid Opcode {opcode} found at position {pointer}")
            
fig, ax = plt.subplots()
initialize_game()
result = intcode_process(commands.copy())

# Triplets in Tiles konvertieren
for i in range(0, len(result), 3):
    x, y, tile_type = result[i:i + 3]
    tiles[(x, y)] = tile_type


