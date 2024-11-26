import os
from matplotlib import pyplot as plt
import keyboard   #pip install keyboard
import numpy as np

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


def investigation(playing_mode):
    plt.show()
    plt.figure(figsize=(7.17, 3.7))
    picture_data: list = []
    element_data: tuple = []
    score: int = None
    start = 0
    offset = 0
    end = False
    while end is False:
        instruction = str(working_dict[start])
        instruction = instruction.zfill(5)
        opcode = instruction[3] + instruction[4]
        first_parameter = modes_differentiation(start, 1, instruction, offset)
        second_parameter = modes_differentiation(start, 2, instruction, offset)
        third_parameter = modes_differentiation(start, 3, instruction, offset)
        try:
            working_dict[first_parameter]
        except KeyError:
            first_parameter = 0
        try:
            working_dict[second_parameter]
        except KeyError:
            second_parameter = 0
        end = False
        match opcode:
            case '01':
                start = addition(start, first_parameter, second_parameter, third_parameter)
            case '02':
                start = multiplication(start, first_parameter, second_parameter, third_parameter)
            case '03':
                start = inputs(start, first_parameter, picture_data, score, playing_mode)
            case '04':
                start, element_data, picture_data, score = output(start, first_parameter, element_data, picture_data, score)
            case '05':
                start = jump_if_true(start, first_parameter, second_parameter)
            case '06':
                start = jump_if_false(start, first_parameter, second_parameter)
            case '07':
                start = less_than(start, first_parameter, second_parameter, third_parameter)
            case '08':
                start = equals(start, first_parameter, second_parameter, third_parameter)
            case '09':
                start, offset = relativ_offset(start, first_parameter, offset)
            case '99':
                end = True
    drawing(picture_data, score)
    plt.show()


def modes_differentiation(start, index, instructions, offset):
    match index:
        case 1:
            mode_decider = 2
        case 2:
            mode_decider = 1
        case 3:
            mode_decider = 0
    if instructions[mode_decider] == '0':
        try:
            return working_dict[start + index]
        except KeyError:
            return len(working_dict) + 1
    elif instructions[mode_decider] == '1':
        return start + index
    elif instructions[mode_decider] == '2':
        try:
            return working_dict[start + index] + offset
        except KeyError:
            return len(working_dict) + 1


def drawing(picture_data, score):
    plt.clf()
    empty = [[], []]
    block = [[], []]
    wall = [[], []]
    paddle = [[], []]
    ball = [[], []]
    for element_data in picture_data:
        x = element_data[0]
        y = element_data[1]
        style = element_data[2]
        match style:
            case 0:
                empty[0].append(x)
                empty[1].append(y)
            case 1:
                wall[0].append(x)
                wall[1].append(y)
            case 2:
                block[0].append(x)
                block[1].append(y)
            case 3:
                paddle[0].append(x)
                paddle[1].append(y)
            case 4:
                ball[0].append(x)
                ball[1].append(y)
    for i in range(0,2):
        ball[i] = ball[i][-1]
        paddle[i] = paddle[i][-1]
    plt.axes().invert_yaxis()
    plt.scatter(wall[0], wall[1],s = 75, color = 'k', marker = 's', edgecolor='w')
    plt.scatter(block[0], block[1],s = 75, color = 'r', marker = 's', edgecolor='w')
    plt.scatter(empty[0], empty[1],s = 75, color = 'k', marker = 's', edgecolor='none')
    plt.scatter(paddle[0], paddle[1],s = 75, color = 'b', marker = 's', edgecolor='none')
    plt.scatter(ball[0], ball[1],s = 75, color = 'g', marker = 'o', edgecolor='none')
    plt.axis('off')
    plt.title(f'Score: {score}')
    plt.draw()
    plt.pause(0.001)
    return ball[0], paddle[0]


def automatik(x_ball, x_paddle):
    if x_ball < x_paddle:
        return -1
    elif x_ball > x_paddle:
        return 1
    else:
        return 0


def key_input():
    plt.pause(0.2)
    while True:
        if keyboard.is_pressed('Right'):
            return 1
        elif keyboard.is_pressed('Left'):
            return -1
        elif keyboard.is_pressed('Down'):
            return 0


def addition(start, first_parameter, second_parameter, third_parameter):
    solution = working_dict[first_parameter] + working_dict[second_parameter]
    working_dict[third_parameter] = solution
    return start + 4


def multiplication(start, first_parameter, second_parameter, third_parameter):
    solution = working_dict[first_parameter] * working_dict[second_parameter]
    working_dict[third_parameter] = solution
    return start + 4


def inputs(start, first_parameter, picture_data, score, playing_mode):
    solution = 0
    x_ball, x_paddle = drawing(picture_data, score)
    if playing_mode == '1':
        # solution = input('Wie soll sich dein Paddle bewegen? -1: links, 0: beleiben, 1:rechts: ')
        solution = key_input()
    elif playing_mode == '2':
        solution = automatik(x_ball, x_paddle)
    try:
        working_dict[first_parameter] = int(solution)
    except ValueError:
        exit
    return start + 2


def output(start, first_parameter, elemet_data: list, picture_data: list, score):
    requested = working_dict[first_parameter]
    elemet_data.append(requested)
    if len(elemet_data) < 3:
        pass
    elif elemet_data[0] == -1 and elemet_data[1] == 0 and len(elemet_data) == 3:
        if score != elemet_data[2]:
            score = elemet_data[2]
            elemet_data.clear()
    else:
        elemet_data = tuple(elemet_data)
        picture_data.append(elemet_data)
        elemet_data = list(elemet_data)
        elemet_data.clear()
    return start + 2, elemet_data, picture_data, score


def jump_if_true(start, first_parameter, second_parameter):
    if working_dict[first_parameter] != 0:
        return working_dict[second_parameter]
    else:
        return start+3


def jump_if_false(start, first_parameter, second_parameter):
    if working_dict[first_parameter] == 0:
        return working_dict[second_parameter]
    else:
        return start+3


def less_than(start, first_parameter, second_parameter, third_parameter):
    if working_dict[first_parameter] < working_dict[second_parameter]:
        working_dict[third_parameter] = 1
    else:
        working_dict[third_parameter] = 0
    return start + 4


def equals(start, first_parameter, second_parameter, third_parameter):
    if working_dict[first_parameter] == working_dict[second_parameter]:
        working_dict[third_parameter] = 1
    else:
        working_dict[third_parameter] = 0
    return start + 4


def relativ_offset(start, first_parameter, offset):
    offset += working_dict[first_parameter]
    return start + 2, offset


def reading_input():
    empty_position = 0
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sequence_path = os.path.join(script_dir, "..", "..", "data",
                                 "breakout_commands.txt")
    with open(sequence_path, 'r') as inputfile:
        for line in inputfile:
            line = line[:-1]         
            working_dict[empty_position] = int(line)
            empty_position += 1
    print('1:Bildgeneriertung\n2:Spielen')
    start_mode = input('Welcher Startmodus soll ausgeführt werden:')
    if start_mode == '1':
        working_dict[0] = 1
    elif start_mode == '2':
        working_dict[0] = 2
        print('1: Selberspielen\n2: Autoplay')
        playing_mode = input('Welchen Modus willst du:')
        if playing_mode == 1:
            pass

        return playing_mode
    return 0    

def execute():
    global working_dict
    working_dict = {}
    playing_mode = reading_input()
    investigation(playing_mode)
    print('Die Endzahl ist:', working_dict[0])


execute()
# Score after finish: 17159
