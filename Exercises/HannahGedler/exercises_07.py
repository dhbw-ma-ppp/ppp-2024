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
import sys
from matplotlib import pyplot as plt
from matplotlib import patches as patches

sys.path.append('/Users/hannah/Desktop/Ppp/ppp-2024/Exercises/HannahGedler')
with open('/Users/hannah/Desktop/Ppp/ppp-2024/Exercises/HannahGedler/breakout_commands.txt', 'r') as file: 
            actual_input = file.read().strip()
            list_actual_input = actual_input.splitlines()
            memory_dict = {index: int(wert.strip()) for index, wert in enumerate(list_actual_input)}   

test1 = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
result_dict = {index: value for index, value in enumerate(test1)} # dict for test1 

def get_parameter(number_dict, mode, instruction_counter, relative_offset):
     if mode == '1':
        if instruction_counter not in number_dict:
            number_dict[instruction_counter] = 0
        return number_dict[instruction_counter]
     elif mode == '0':
        if number_dict[instruction_counter] not in number_dict:
            number_dict[number_dict[instruction_counter]] = 0
        return number_dict[number_dict[instruction_counter]]
     elif mode == '2':
        if number_dict[instruction_counter] + relative_offset not in number_dict:
             number_dict[number_dict[instruction_counter]+ relative_offset] = 0
        return number_dict[number_dict[instruction_counter]+ relative_offset]

def find_number(test_list):
     instructionCounter = 0
     relative_offset = 0
     while True:
         opcode = str(test_list[instructionCounter])
         while len(opcode) < 5:
             opcode = "0" + opcode
         instruction = str(opcode[3:5])
         first_mode = opcode[2]
         second_mode = opcode[1]
         third_mode = opcode[0]
        # different_modes = [first_mode, second_mode]
         # opcode 1: addition
         if instruction == "01":
             firstParameter = get_parameter(test_list,first_mode, instructionCounter+1, relative_offset)
             secondParameter = get_parameter(test_list,second_mode, instructionCounter+2, relative_offset)
             result = firstParameter + secondParameter
             target = get_parameter(test_list, '1', instructionCounter+3, relative_offset) #from mode 1 because I take value of this position in line 74
             if third_mode == '2':
                target += relative_offset
             test_list[target] = result
             instructionCounter += 4
         # opcode 2: multiplication
         elif instruction == "02":
             firstParameter = get_parameter(test_list,first_mode, instructionCounter+1, relative_offset)
             secondParameter = get_parameter(test_list,second_mode, instructionCounter+2, relative_offset)
             result = firstParameter * secondParameter
             target = get_parameter(test_list, '1', instructionCounter+3, relative_offset)
             if third_mode == '2':
                target += relative_offset
             test_list[target] = result
             instructionCounter += 4
         # opcode 3: user input, no immediate mode possible
         elif instruction == "03":
            #user_input = int(input("Please enter a number:"))
            user_input = auto_play()
            save_at_position = get_parameter(test_list, '1', instructionCounter+1, relative_offset)
            if first_mode == '2':
                save_at_position += relative_offset
            test_list[save_at_position] = user_input
            instructionCounter += 2
         # opcode 4: output
         elif instruction == "04":
             if first_mode == '1':
                 yield (test_list[instructionCounter + 1])
             elif first_mode == '0':
                 yield (test_list[test_list[instructionCounter + 1]])
             elif first_mode == '2':
                 yield (test_list[test_list[instructionCounter + 1] + relative_offset]) 
             instructionCounter += 2
         # - 5: jump-if-true: if the first parameter is non-zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
         elif instruction == "05":
             firstParameter = get_parameter(test_list,first_mode, instructionCounter+1, relative_offset)
             secondParameter = get_parameter(test_list,second_mode, instructionCounter+2, relative_offset)
             if firstParameter != 0:
                 instructionCounter = secondParameter
             else:
                 instructionCounter += 3
         # - 6: jump-if-false: if the first parameter is zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
         elif instruction == "06":
             firstParameter = get_parameter(test_list,first_mode, instructionCounter+1, relative_offset)
             secondParameter = get_parameter(test_list,second_mode, instructionCounter+2, relative_offset)
             if firstParameter == 0:
                 instructionCounter = secondParameter
             else:
                 instructionCounter += 3
         # - 7: less than: if the first parameter is less than the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
         elif instruction == "07":
             firstParameter = get_parameter(test_list,first_mode, instructionCounter+1, relative_offset)
             secondParameter = get_parameter(test_list,second_mode, instructionCounter+2, relative_offset)
             resultIndex = get_parameter(test_list, '1', instructionCounter+3, relative_offset)
             if third_mode == '2':
                 resultIndex += relative_offset
             if firstParameter < secondParameter:
                 test_list[resultIndex] = 1
             else:
                 test_list[resultIndex] = 0
             instructionCounter += 4
         # - 8: equals: if the first parameter is equal to the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
         elif instruction == "08":
             firstParameter = get_parameter(test_list,first_mode, instructionCounter+1, relative_offset)
             secondParameter = get_parameter(test_list,second_mode, instructionCounter+2, relative_offset)
             resultIndex = get_parameter(test_list, '1', instructionCounter+3, relative_offset)
             if third_mode == '2':
                 resultIndex += relative_offset
             if firstParameter == secondParameter:
                 test_list[resultIndex] = 1
             else:
                 test_list[resultIndex] = 0
             instructionCounter += 4
         #opcode 9 adjusts the relative offset by the value of its only parameter.the offset increases by the value of the parameter (or decreases if the parameter value is negative).
         elif instruction == "09":
             firstParameter = get_parameter(test_list,first_mode, instructionCounter+1, relative_offset)
             relative_offset += firstParameter
             instructionCounter += 2
         elif instruction == "99":
             break
    #print("result:", test_list[0]) 


#draw
def paint(triplets): 
    fig, ax = plt.subplots()
    
    ax.set_xlim(-1, 43)
    ax.xaxis.set_visible(False) 
    ax.set_ylim(-25, 1)
    ax.yaxis.set_visible(False)
    ax.set_aspect('equal', adjustable='box')
    
    width = 1
    height = 0.5
    #blocks
    for key in triplets:
        if triplets[key] == 2:
            x = key[0]
            y = key[1]
            rect = patches.Rectangle((x - width / 2, -y), width, height, facecolor = 'lightblue')
            ax.add_patch(rect)
    #wall
        elif triplets[key] == 1:
            x = key[0]
            y = key[1]
            rect = patches.Rectangle((x - width / 2, -y), width, height,facecolor='grey' )
            ax.add_patch(rect)
        
    #paddle
        elif triplets[key] == 3:
            x = key[0]
            y = key[1]
            rect = patches.Rectangle((x - width / 2, -y), width, height,facecolor='lightpink' )
            ax.add_patch(rect)
    #ball
        elif triplets[key] == 4:
            x = key[0]
            y = key[1]
            circle = patches.Circle((x, -y), 0.2, facecolor='lightpink')
            ax.add_patch(circle)
    #score
        elif key[0] == -1 and key[1] == 0:
            score = triplets[key]
            print("This is your score:", score)
            plt.title(f'Score: {score}')
            
    
    plt.draw()


def auto_play():
    output_list = []
    ball_xkor = None 
    paddle_xkor = None 
    for i in find_number(memory_dict):
        output_list.append(i)
        if len(output_list) > 2:
            if output_list[2] == 4:     #ball
                ball_xkor = output_list[0]
            elif output_list[2] == 3:   #paddle
                paddle_xkor = output_list[0]
            output_list = []

            if ball_xkor != None and paddle_xkor != None: 
                if ball_xkor > paddle_xkor:
                    return 1
                elif ball_xkor < paddle_xkor:
                    return -1
                else:
                    return 0

def make_triplets():
    plt.show()
    output_list = []
    triplets_dict2 = {}
    stopit = False
    while stopit == False:
        for i in find_number(memory_dict):
            output_list.append(i)
            if len(output_list) > 2:
                triplets_dict2[(output_list[0], output_list[1])] = output_list[2]
                if output_list[2] == 4:
                    paint(triplets_dict2)
                    plt.pause(0.1)
                    plt.close()
                if output_list[2] == 99:
                    stopit = True
                    break
                output_list = []
    if stopit == True:
        print("You have won")
make_triplets()
#highscore: 17159