import os
# For this weeeks exercise you again need to add a feature to your existing simulated computer:

# - The computer needs to implement memory much /larger/ than the set of initial commands.
#   Any memory address not part of the initial commands can be assumed to be initialized to 0.
#   Only positive addresses are valid, but any positive address can be both read and written.
# - You need to support a new parameter mode, called 'relative mode', and denoted as mode 2 in 
#   the 'mode' part of the instructions.
#   Relative mode is similar to position mode (the first access mode you implemented). However, 
#   parameters in relative mode count not from 0, but from a value called 'relative offset'. 
#   When the computer is initialized, the relative offset is initialized to 0, and as long as it remains
#   0 relative mode and position mode are identical.
#   In general though parameters in relative mode address the memory location at 'relative offset + parameter value'.
#   EXAMPLE: if the relative offset is 50, the mode is 2, and the value you read from memory is 7 you should 
#     retrieve data from the memory address 57.
#     Equally, if you read -7, you should retrieve data from the memory address 43.
#   This applies to both read- and write operations (!)

# - You need to implement a new opcode, opcode 9. opcode 9 adjusts the relative offset by the value of its only parameter.
#   the offset increases by the value of the parameter (or decreases if the parameter value is negative).

# Here is a short program to test your implementation:
#   [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99] should output a copy of itself
#   
# The actual input is in a separate file, input_memory_01.txt under the `data` folder.
# When asked for input provide the value 2. There should be a single output. Please include it in your PR.


def investigation(start, offset):
    instruction = str(working_dict[start])
    instruction = instruction.zfill(5)
    opcode = instruction[3] + instruction[4]
    first_parameter = modes_differentiation(start, 1, instruction, offset)
    second_parameter = modes_differentiation(start, 2, instruction, offset)
    third_parameter = modes_differentiation(start, 3, instruction, offset)
    if third_parameter == 101:
        pass
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
            return start, end, offset
        case '02':
            start = multiplication(start, first_parameter, second_parameter, third_parameter)
            return start, end, offset
        case '03':
            start = inputs(start, first_parameter)
            return start, end, offset
        case '04':
            start = output(start, first_parameter)
            return start, end, offset
        case '05':
            start = jump_if_true(start, first_parameter, second_parameter)
            return start, end, offset
        case '06':
            start = jump_if_false(start, first_parameter, second_parameter)
            return start, end, offset
        case '07':
            start = less_than(start, first_parameter, second_parameter, third_parameter)
            return start, end, offset
        case '08':
            start = equals(start, first_parameter, second_parameter, third_parameter)
            return start, end, offset
        case '09':
            start, offset = relativ_offset(start, first_parameter, offset)
            return start, end, offset
        case '99':
            end = True
            return 1, end, offset


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


def addition(start, first_parameter, second_parameter, third_parameter):
    solution = working_dict[first_parameter] + working_dict[second_parameter]
    working_dict[third_parameter] = solution
    return start + 4


def multiplication(start, first_parameter, second_parameter, third_parameter):
    solution = working_dict[first_parameter] * working_dict[second_parameter]
    working_dict[third_parameter] = solution
    return start + 4


def inputs(start, first_parameter):
    solution = input('Bitte gibt einen Input ein:')
    working_dict[first_parameter] = int(solution)
    return start + 2


def output(start, first_parameter):
    print('Output wegen Opcode 4:', working_dict[first_parameter])
    return start + 2


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
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sequence_path = os.path.join(script_dir, "..", "..", "data",
                                 "input_memory_01.txt")
    with open(sequence_path, 'r') as inputfile:
        line = inputfile.readline()[:-1]
        str_numbers = line.split(',')
        empty_position = 0
        while empty_position < len(str_numbers):
            working_dict[empty_position] = int(str_numbers[empty_position])
            empty_position += 1


def execute():
    reading_input()
    end = False
    position = 0
    offset = 0
    while end is False:
        position, end, offset = investigation(position, offset)
    print('Die Endzahl ist:', working_dict[0])


test1 = {0: 109, 1: 1, 2: 204, 3: -1, 4: 1001, 5: 100, 6: 1, 7: 100, 8: 1008,
         9: 100, 10: 16, 11: 101, 12: 1006, 13: 101, 14: 0, 15: 99}
# working_dict = test1
working_dict = {}
execute()
# Output durch Opcode 4: 33343
# Output durch Opcode 99: 1102
