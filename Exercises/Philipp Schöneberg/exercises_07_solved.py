import operator
import keyboard
from collections import defaultdict
from matplotlib import pyplot as plt
from typing import Iterable, Generator

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


def compute(commands_iterable: Iterable[int]) -> Generator[int, None, None]:
    """
    This function takes as input an iterator of integers and returns a single
    integer number. The numbers passed as argument form the working memory of
    a simulated computer. This computer will start by looking at the first
    value in the list passed to the function. This value will contain an `
    opcode`. Valid opcodes are 1, 2, 3, 4, 5, 6, 7, 8, 9 or 99. Encountering
    any other value when expecting an opcode or a lengthwise unfitting list
    will raise an RuntimeError. The meaning of opcodes is as follows:
    - 1 indicates addition. The function will read values from the next two
    positions of your working memory, add them, and store the result in the
    third position of your working memory. The three numbers immediately after
    your opcode indicate the memory locations to read (first two values) and
    write (third value) respectively.
    - 2 indicates multiplication. Otherwise the same rules apply as for opcode 1.
    - 3: read a single integer as input and save it to the position given by
    its only parameter.
    - 4: output the value of the single parameter for this opcode.
    - 5: jump-if-true: if the first parameter is non-zero, it sets the
    instruction pointer to the value from the second parameter. Otherwise, it
    does nothing.
    - 6: jump-if-false: if the first parameter is zero, it sets the instruction
    pointer to the value from the second parameter. Otherwise, it does nothing.
    - 7: less than: if the first parameter is less than the second parameter,
    it stores 1 in the position given by the third parameter. Otherwise, it
    stores 0.
    - 8: equals: if the first parameter is equal to the second parameter, it
    stores 1 in the position given by the third parameter. Otherwise, it
    stores 0.
    - 9: adjusts the relative offset by the value of its only parameter. the
    offset increases by the value of the parameter (or decreases if the
    parameter value is negative).
    - 99 indicates halt. the program should stop after encountering the opcode 99.\n
    After the program stops, the function should return the value in the first
    location (address 0) of your working memory.
    """
    def get_command(index: int) -> int:
        """
        This function expects an integer and returns the value stored under
        the corresponding key from the dictionary commands. If there is no
        corresponding key, it will create one with the value zero using its
        classability as a defauldict and then return it.
        """
        if index >= 0:
            return commands[index]
        else:
            raise IndexError("The index can't be negative.")

    def get_opcode(extended_opcode, opcode) -> None:
        """
        This function calculates the opcode needed to compute the next
        instruction.
        """
        extended_opcode = get_command(instruction_pointer)
        opcode = extended_opcode % 100
        extended_opcode = extended_opcode // 100
        return extended_opcode, opcode

    def get_indices_and_parameter(parameter_amount: int, extended_opcode) -> None:
        """
        This function takes as input an integer representing the number of
        parameters needed for the next operation. It then calculates the
        corresponding indices and parameters.
        """
        parameter: dict[int, int] = {}
        indices: dict[int, int] = {}
        for i in range(0, parameter_amount):
            indices[i] = get_command(instruction_pointer+i+1)
            if extended_opcode % 10 == 1:
                parameter[i] = indices[i]
            elif extended_opcode % 10 == 2:
                indices[i] += relative_offset
                parameter[i] = get_command(indices[i])
            else:
                parameter[i] = get_command(indices[i])
            extended_opcode = extended_opcode // 10
        return indices[parameter_amount-1], parameter

    commands: defaultdict[int, int] = defaultdict(int)
    operations_with_three_parameters: dict[int, object]
    instruction_pointer: int = 0
    relative_offset: int = 0
    extended_opcode: int = 0
    opcode: int = 0

    for i, elem in enumerate(commands_iterable):
        commands[i] = elem
    operations_with_three_parameters = {
        1: operator.add,
        2: operator.mul,
        5: lambda x, y: y if x != 0 else instruction_pointer+3,
        6: lambda x, y: y if x == 0 else instruction_pointer+3,
        7: lambda x, y: 1 if x < y else 0,
        8: lambda x, y: 1 if x == y else 0,
    }

    while True:
        try:
            extended_opcode, opcode = get_opcode(extended_opcode, opcode)
            match opcode:
                case 1 | 2 | 7 | 8:
                    index, parameter = get_indices_and_parameter(3, extended_opcode)
                    commands[index] = operations_with_three_parameters[opcode](parameter[0], parameter[1])
                    instruction_pointer += 4
                case 3:
                    global paddle_movement
                    index, parameter = get_indices_and_parameter(1, extended_opcode)
                    commands[index] = paddle_movement
                    instruction_pointer += 2
                case 4:
                    index, parameter = get_indices_and_parameter(1, extended_opcode)
                    yield parameter[0]
                    instruction_pointer += 2
                case 5 | 6:
                    index, parameter = get_indices_and_parameter(2, extended_opcode)
                    instruction_pointer = operations_with_three_parameters[opcode](parameter[0], parameter[1])
                case 9:
                    index, parameter = get_indices_and_parameter(1, extended_opcode)
                    relative_offset += parameter[0]
                    instruction_pointer += 2
                case 99:
                    break
                case _:
                    raise RuntimeError("The given opcode is unvalid.")
        except IndexError:
            raise RuntimeError("The given commandlist is unvalid.")
    return commands[0]


class commandsIterator:
    def __init__(self, playable: bool) -> None:
        self.playable = playable
        self.input_file: str = "breakout_commands.txt"

    def __iter__(self) -> Generator[int, None, None]:
        with open(self.input_file, "r") as f:
            if self.playable:
                next(f)
                yield 2
            for line in f:
                yield int(line.strip())


def breakout() -> None:
    def UI() -> tuple[bool, Iterable[int], int]:
        playable: int | bool = None
        playmode: int = None

        print("Welcome!")
        print("Choose if the game is playable:")
        print("- 0: The game will only show the startscreen")
        print("- 1: The game is playable\n")#

        while True:
            try:
                playable = int(input("Which mode do you choose?\n"))
                if playable == 0 or playable == 1:
                    playable = bool(playable)
                    break
                else:
                    raise ValueError
            except ValueError:
                print("\nYour input was unvalid.")
        my_iterator = commandsIterator(playable)

        if playable:
            print("\nChoose how the game should be played:")
            print("- 0: The game will be controlled by inputs in the console")
            print("- 1: The game will be controlled by pressing keys")
            print("- 2: The game will be controlled automaically\n")
            while True:
                try:
                    playmode = int(input("Which mode do you choose?\n"))
                    if playmode == 0 or playmode == 1 or playmode == 2:
                        break
                    else:
                        raise ValueError
                except ValueError:
                    print("\nYour input was unvalid.")
            if playmode == 0:
                print("\nYou are playing breakout. Control the padel through entering the following commands:")
                print("-  0: the paddle remains in position")
                print("- -1: move the paddle to the left")
                print("- +1: move the paddle to the right\n")
            elif playmode == 1:
                print("\nYou are playing breakout. Control the padel through pressing the following keys:")
                print("- down: the paddle remains in position")
                print("- left: move the paddle to the left")
                print("- right: move the paddle to the right\n")
            elif playmode == 2:
                print("\nBreakout will be played automatically.")

        return playable, my_iterator, playmode

    def paddle_controller(playmode: int, ball_coordinates: tuple, paddle_coordinates: tuple) -> int:
        global paddle_movement
        if playmode == 2:
            if ball_coordinates[0] < paddle_coordinates[0]:
                paddle_movement = -1
            elif ball_coordinates[0] > paddle_coordinates[0]:
                paddle_movement = 1
            else:
                paddle_movement = 0
        elif playmode == 1:
            plt.pause(0.2)
            while True:
                if keyboard.is_pressed('Right'):
                    paddle_movement = 1
                elif keyboard.is_pressed('Left'):
                    paddle_movement = -1
                elif keyboard.is_pressed('Down'):
                    paddle_movement = 0
        elif playmode == 0:
            while True:
                try:
                    user_input = int(input("Enter an integer: "))
                    break
                except ValueError:
                    print("The given input was not an integer.")
            paddle_movement = user_input

    def play(score: int, paddle_movement: int) -> int:
        environment: dict[int, int] = {}
        triple_lst: list[int] = []
        plt.style.use('dark_background')
        plt.show
        for elem in compute(my_iterator):
            triple_lst.append(elem)
            if len(triple_lst) == 3:
                environment[(triple_lst[0], -triple_lst[1])] = triple_lst[2]
                if triple_lst[2] == 4 and len(environment) == 990:
                    next(refresh_environment(environment))
                triple_lst = []
        score = next(refresh_environment(environment))
        return score

    def refresh_environment(environment: dict[int, int]) -> int:
        pos_colors: list = ["red", "orange", "yellow", "green", "blue", "m", "c"]
        empty_tile_x: list = []
        empty_tile_y: list = []
        wall_x: list = []
        wall_y: list = []
        block_x: list = []
        block_y: list = []
        colors: list = []
        color_counter: int = 0
        score: int = 0
        paddle_x: int
        paddle_y: int
        ball_x: int
        ball_y: int
        while True:
            plt.clf()
            for elem in environment:
                if elem == (-1, 0):
                    score = environment[elem]
                match environment[elem]:
                    case 0:
                        # 0: empty tile
                        empty_tile_x.append(elem[0])
                        empty_tile_y.append(elem[1])
                    case 1:
                        # wall (indestructible)
                        wall_x.append(elem[0])
                        wall_y.append(elem[1])
                    case 2:
                        # block (can be destroyed by the ball)
                        block_x.append(elem[0])
                        block_y.append(elem[1])
                    case 3:
                        # paddle (indestructible)
                        paddle_x = elem[0]
                        paddle_y = elem[1]
                    case 4:
                        # ball (moves diagonally and bounces off objects)
                        ball_x = elem[0]
                        ball_y = elem[1]
            color_counter = 0
            colors = []
            for i, elem in enumerate(block_y):
                if elem < block_y[i-1]:
                    if color_counter < len(pos_colors)-1:
                        color_counter += 1
                    else:
                        color_counter = 0
                colors.append(pos_colors[color_counter])
            plt.scatter(empty_tile_x, empty_tile_y, marker="s", c="black")
            plt.scatter(wall_x, wall_y, marker="s", c="grey")
            plt.scatter(block_x, block_y, marker="s", c=colors)
            plt.scatter(paddle_x, paddle_y, marker="s", c='grey')
            plt.scatter(ball_x, ball_y, marker="o", c='white')
            plt.title(f'Score: {score}')
            plt.axis("off")
            nonlocal playable
            if playable:
                plt.draw()
            else:
                plt.show()
            plt.pause(0.001)
            paddle_controller(playmode, (ball_x, ball_y), (paddle_x, paddle_y))
            yield score

    score: int = 0
    playable, my_iterator, playmode = UI()
    score = play(score, paddle_movement)
    if playable:
        print(f"The Game has ended. Your score is {score} well done!")


paddle_movement = 0
breakout()
