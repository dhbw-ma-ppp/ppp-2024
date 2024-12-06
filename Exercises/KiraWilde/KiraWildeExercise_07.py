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


import os


#Instead of using a set as before, I now use a dictionary to address an 'infinitely' large storage space.
def load_memory_from_file(file_path):
    with open(file_path, "r") as file:
        content = file.read().strip()
        # The file contains values such as “1,0,0,0,99”, which are converted into a dictionary
        memory = {i: int(value) for i, value in enumerate(content.split())}
    return memory


def get_value(memory, parameter, mode, relative_base):
    if mode == 0:
        # Position mode
        return memory.get(parameter, 0)
    elif mode == 1:
        # Immediate mode
        return parameter
    elif mode == 2:
        # Relative mode
        return memory.get(relative_base + parameter, 0)
    else:
        raise ValueError(f"Invalid parameter mode: {mode}")


def write_value(memory, address, mode, relative_base, value):
    """Writes a value to the correct memory address, and memory addresses must always be positive."""
    if mode == 0 and address >= 0:
        # Position mode
        memory[address] = value
    elif mode == 2 and (relative_base + address) >= 0:
        # Relative mode
        memory[relative_base + address] = value
    else:
        raise ValueError("Invalid memory address: The address must be positive, or the write address must not be in immediate mode.")


def simulate_computer(memory, spielmodus):
    pointer = 0
    relativ_offset = 0
    outputs = [] 
    score = 0
    ball_x = 0
    paddle_x = 0
    while True:
        instruction = memory.get(pointer, 0)
        opcode = instruction % 100
        mode1 = (instruction // 100) % 10
        mode2 = (instruction // 1000) % 10
        mode3 = (instruction // 10000) % 10
        match opcode:
            case 99:
                break
            case 1 | 2 | 7 | 8:
                param1 = get_value(memory, memory.get(pointer + 1, 0), mode1, relativ_offset)
                param2 = get_value(memory, memory.get(pointer + 2, 0), mode2, relativ_offset)
                if opcode == 1:
                    # Addition
                    write_value(memory, memory.get(pointer + 3, 0), mode3, relativ_offset, param1 + param2)
                elif opcode == 2:
                    # Multiplication
                    write_value(memory, memory.get(pointer + 3, 0), mode3, relativ_offset, param1 * param2)
                elif opcode == 7:
                    # Less than
                    write_value(memory, memory.get(pointer + 3, 0), mode3, relativ_offset, 1 if param1 < param2 else 0)
                elif opcode == 8:
                    # Equals
                    write_value(memory, memory.get(pointer + 3, 0), mode3, relativ_offset, 1 if param1 == param2 else 0)
                pointer += 4
            case 3 | 4:
                if opcode == 3:
                    if spielmodus:
                        user_input = int(input("Move the paddle (-1 = left, 0 = stay, 1 = right):"))
                        write_value(memory, memory.get(pointer + 1, 0), mode1, relativ_offset, user_input)
                    else:
                        # Paddle input logic: Follow the ball
                        if ball_x < paddle_x:
                            user_input = -1  # Move left
                        elif ball_x > paddle_x:
                            user_input = 1  # Move right
                        else:
                            user_input = 0  # Stay
                        write_value(memory, memory.get(pointer + 1, 0), mode1, relativ_offset, user_input)
                elif opcode == 4:
                    param1 = get_value(memory, memory.get(pointer + 1, 0), mode1, relativ_offset)
                    outputs.append(param1)
                    if len(outputs) == 3:
                        x, y, tile_type = outputs
                        if (x, y) == (-1, 0):
                            # This is the score update
                            score = tile_type
                        else:
                            # Normal tile update
                            handle_output(outputs)
                            os.system("cls" if os.name == "nt" else "clear")
                            draw_ascii_art()
                            # Update ball or paddle position
                            if tile_type == 4:  # Ball
                                ball_x = x
                            elif tile_type == 3:  # Paddle
                                 paddle_x = x
                        outputs.clear()
                pointer += 2
            case 5 | 6:
                param1 = get_value(memory, memory.get(pointer + 1, 0), mode1, relativ_offset)
                param2 = get_value(memory, memory.get(pointer + 2, 0), mode2, relativ_offset)
                if opcode == 5:
                    # Jump-if-true
                    pointer = param2 if param1 != 0 else pointer + 3
                elif opcode == 6:
                    # Jump-if-eqal
                    pointer = param2 if param1 == 0 else pointer + 3
            case 9:
                # relative base adjustment
                param1 = get_value(memory, memory.get(pointer +1, 0), mode1, relativ_offset)
                relativ_offset += param1
                pointer += 2
            case _:
                raise ValueError(f"Invalid opcode {opcode} at position {pointer}")
    # return memory.get(0, 0)
    return score


def handle_output(outputs):
    x, y, tile_type = outputs
    grid[(x, y)] = tile_type


def draw_ascii_art():
    if not grid:
        print("There is no data, HELLO?")
        return
    # Determine the size of the playing field
    max_x = max(x for x, y in grid.keys())
    max_y = max(y for x, y in grid.keys())
    tile_symbols = {
        0: "  ",  # empty tiel
        1: "\u2B1C",  # wall
        2: "\U0001F7EA",  # block
        3: "[]",  # paddle
        4: "\u26BD",  # ball
    }
    for y in range(max_y +1):
        row = ""
        for x in range(max_x +1):
            tile = grid.get((x, y), 0)
            row += tile_symbols.get(tile, "?")
        print(row)


script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "..", "..", "data", "breakout_commands.txt")

grid = {} # 2D Dictionary for triplets
memory = load_memory_from_file(file_path)
spielmodus = input("Type True for playing or False for watching: ").strip().lower() == "true"
# result = simulate_computer(memory)
# print(f"Resultat: {result}")
final_score = simulate_computer(memory, spielmodus)
print(final_score)
draw_ascii_art()
