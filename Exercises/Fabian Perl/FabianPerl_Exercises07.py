import time
import sys
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

def make_dict(path):                                
    commands = {}
    with open(path, "r") as file:
        index = 0
        for line in file:
            commands.update({index: int(line)})
            index += 1
    return commands

def make_param_list(memory, pointer, parameter_num, offset):        #calculate parameters in mode specified by the instructions
    output = []

    for i in range(1, parameter_num + 1):
        if (memory[pointer] // (10 * 10 ** i) % 10) == 0:        #parameter in position mode
            output.append(memory[pointer+i])    
        elif (memory[pointer] // (10 * 10 ** i) % 10) == 1:      #parameter in immediate mode    
            output.append(pointer+i)
        if (memory[pointer] // (10 * 10 ** i) % 10) == 2:        #parameter in position mode
            output.append(memory[pointer+i] + offset) 
    return output
           
def render_img(results):
    
    frame = ""
    for i in range(23):                     #moves cursor up 23 lines in the consol
        sys.stdout.write("\033[F")       
    for i in range(23):            
        frame += "\n"
        for j in range(43):
            frame += results[(j, i)]
    
    time.sleep(0.02)      
    sys.stdout.write(frame)                #sys.stdout to stop flickering of animation 
        
def process_output(output_raw, output_pixel):
    
    chars = {                           #ASCII representation of the pixel values
        0: "   ",
        1: "[_]",
        2: 3*chr(9607),
        3: 3*chr(9603),
        4: " " + chr(9673) + " "      
    }

    index = range(len(output_raw))[::3]
    
    for i in index:
        
        if output_raw[i] == -1:         #score is stored at (-1, 0) --> should not be evaluated as a pixel
            global score
            score = output_raw[i + 2]
            continue
        
        elif output_raw[i+2] == 4:
            global x_of_ball
            x_of_ball = output_raw[i]
            
        elif output_raw[i+2] == 3:
            global x_of_paddle
            x_of_paddle = output_raw[i]

        output_pixel.update({(output_raw[i], output_raw[i + 1]): chars[output_raw[i+2]]})
        
    return output_pixel

def controll_paddle():
    if x_of_ball < x_of_paddle:
        return -1
    elif x_of_ball > x_of_paddle:
        return 1
    return 0
    
def compute_oppcodes(memory):
    
    pointer = 0
    offset = 0
    output_raw = []
    output_pixel = {}
    
    while True:
        
        if pointer < 0:
            raise ValueError("negative index not allowed")
        
        oppcode = memory[pointer] % 100
        
        if oppcode == 1:
            parameter_num = 3
            parameters = make_param_list(memory, pointer, parameter_num, offset)
            memory[parameters[-1]] = memory[parameters[0]] + memory[parameters[1]]
            pointer += (parameter_num + 1)
            
        elif oppcode == 2:
            parameter_num = 3
            parameters = make_param_list(memory, pointer, parameter_num, offset)
            memory[parameters[-1]] = memory[parameters[0]] * memory[parameters[1]]
            pointer += (parameter_num + 1)
            
        elif oppcode == 3:
            
            output_pixel = process_output(output_raw, output_pixel)
            output_raw = []
            render_img(output_pixel)
                             
            parameter_num = 1
            parameters = make_param_list(memory, pointer, parameter_num, offset)
            memory[parameters[-1]] = controll_paddle()
            pointer += (parameter_num + 1)
            
        elif oppcode == 4:
            parameter_num = 1
            parameters = make_param_list(memory, pointer, parameter_num, offset)
            output_raw.append(memory[parameters[0]])                                              
            pointer += (parameter_num + 1)
            
        elif oppcode == 5:
            parameter_num = 2
            parameters = make_param_list(memory, pointer, parameter_num, offset)
            if memory[parameters[0]] != 0:
                pointer = memory[parameters[1]]
            else:
                pointer += (parameter_num + 1)
                
        elif oppcode == 6:
            parameter_num = 2
            parameters = make_param_list(memory, pointer, parameter_num, offset)
            if memory[parameters[0]] == 0:
                pointer = memory[parameters[1]]
            else:
                pointer += (parameter_num + 1)
                
        elif oppcode == 7:
            parameter_num = 3
            parameters = make_param_list(memory, pointer, parameter_num, offset)
            if memory[parameters[0]] < memory[parameters[1]]:
                memory[parameters[-1]] = 1
            else:
                memory[parameters[-1]] = 0
            pointer += (parameter_num + 1)
            
        elif oppcode == 8:
            parameter_num = 3
            parameters = make_param_list(memory, pointer, parameter_num, offset)
            if memory[parameters[0]] == memory[parameters[1]]:
                memory[parameters[-1]] = 1
            else:
                memory[parameters[-1]] = 0
            pointer += (parameter_num + 1)
            
        elif oppcode == 9:
            parameter_num = 1
            parameters = make_param_list(memory, pointer, parameter_num, offset)
            offset += memory[parameters[0]]
            pointer += (parameter_num + 1)
            
        elif oppcode == 99:
            
            output_pixel = process_output(output_raw, output_pixel)
            render_img(output_pixel)
            print(f"\n\nSCORE: {score}\n")
            break
        
        else:
            raise ValueError(f"Wrong oppcode {memory[pointer]} encountert at pointer {pointer}.")
        
    return output_raw

compute_oppcodes(make_dict("data/breakout_commands.txt"))
