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

def listChange(listOfInt):
    def get_value(index, mode, offset):
        if mode == 0:  # Position mode
            return listOfInt.get(listOfInt.get(index, 0), 0)
        elif mode == 1:  # Immediate mode
            return listOfInt.get(index, 0)
        elif mode == 2:  # Relative mode
            return listOfInt.get(listOfInt.get(index, 0) + offset, 0)

    def set_value(index, value, mode, offset):
        if mode == 0:  # Position mode
            listOfInt[listOfInt.get(index, 0)] = value
        elif mode == 2:  # Relative mode
            listOfInt[listOfInt.get(index, 0) + offset] = value

    def draw_board(outputs):
        tiles = {0: ' ', 1: '#', 2: '=', 3: '-', 4: 'o'}
        grid = {}
        score = 0
        ball_x, paddle_x = None, None

        for i in range(0, len(outputs), 3):
            x, y, tile_id = outputs[i], outputs[i + 1], outputs[i + 2]
            if x == -1 and y == 0:
                score = tile_id
            else:
                grid[(x, y)] = tiles.get(tile_id, ' ')
                if tile_id == 4:  # Ball
                    ball_x = x
                elif tile_id == 3:  # Paddle
                    paddle_x = x

        max_x = max((x for x, y in grid.keys()), default=0)
        max_y = max((y for x, y in grid.keys()), default=0)

        print("Score:", score)
        for y in range(max_y + 1):
            row = ''.join(grid.get((x, y), ' ') for x in range(max_x + 1))
            print(row)
        return ball_x, paddle_x

    i = 0
    offset = 0  
    outputs = []
    ball_x = None
    paddle_x = None

    while True:
        op_code = listOfInt.get(i, 0) % 100
        mode_parameter_1 = (listOfInt.get(i, 0) // 100) % 10
        mode_parameter_2 = (listOfInt.get(i, 0) // 1000) % 10
        mode_parameter_3 = (listOfInt.get(i, 0) // 10000) % 10

        if op_code == 1:  # Add
            set_value(i + 3,
                      get_value(i + 1, mode_parameter_1, offset) + get_value(i + 2, mode_parameter_2, offset),
                      mode_parameter_3, offset)
            i += 4
        elif op_code == 2:  # Multiply
            set_value(i + 3,
                      get_value(i + 1, mode_parameter_1, offset) * get_value(i + 2, mode_parameter_2, offset),
                      mode_parameter_3, offset)
            i += 4
        elif op_code == 3:  # Input
            ball_x, paddle_x = draw_board(outputs)
            
            # draw_board(outputs)
            # user_input = int(input("Enter paddle move: "))
            # set_value(i + 1, user_input, mode_parameter_1, offset)
            # i += 2

            # cheatcode :)
            if ball_x != None and paddle_x != None:
                if paddle_x < ball_x:
                    user_input = 1 
                elif paddle_x > ball_x:
                    user_input = -1 
                else:
                    user_input = 0 
            else:
                user_input = 0

            set_value(i + 1, user_input, mode_parameter_1, offset)
            i += 2
        elif op_code == 4:  # Output
            outputs.append(get_value(i + 1, mode_parameter_1, offset))
            i += 2
        elif op_code == 5:  # Jump-if-true
            if get_value(i + 1, mode_parameter_1, offset) != 0:
                i = get_value(i + 2, mode_parameter_2, offset)
            else:
                i += 3
        elif op_code == 6:  # Jump-if-false
            if get_value(i + 1, mode_parameter_1, offset) == 0:
                i = get_value(i + 2, mode_parameter_2, offset)
            else:
                i += 3
        elif op_code == 7:  # Less than
            set_value(i + 3,
                      1 if get_value(i + 1, mode_parameter_1, offset) < get_value(i + 2, mode_parameter_2, offset) else 0,
                      mode_parameter_3, offset)
            i += 4
        elif op_code == 8:  # Equals
            set_value(i + 3,
                      1 if get_value(i + 1, mode_parameter_1, offset) == get_value(i + 2, mode_parameter_2, offset) else 0,
                      mode_parameter_3, offset)
            i += 4
        elif op_code == 9:  # Adjust relative base
            offset += get_value(i + 1, mode_parameter_1, offset)
            i += 2
        elif op_code == 99:  # Halt
            draw_board(outputs)  # Final board state
            break
        else:
            print(f"Error: Unknown opcode {op_code} at position {i}")
            break


def start_memory(lst):
    input_dict = {index: value for index, value in enumerate(lst)}
    listChange(input_dict)

# Load input from file
with open("data/breakout_commands.txt", "r") as file:
    program = list(map(int, file.read().strip().splitlines()))

start_memory(program)

#score = 17159