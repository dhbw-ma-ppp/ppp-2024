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

import operator
from collections import defaultdict

def read_numbers_from_file(filepath: str) -> defaultdict:
    with open(filepath, 'r') as file:
        content = file.read()
        numbers = {i: int(num) for i, num in enumerate(content.split(","))}
    return numbers

def get_parameter(memory, parameter, mode, relative_offset, is_write=False):
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

def simulated_computer(memory):
    pointer = 0
    relative_offset = 0

    opcode_map = {
        1: operator.add,
        2: operator.mul,
        7: lambda x, y: int(x < y),
        8: lambda x, y: int(x == y)
    }

    while True:
        instruction = str(memory[pointer]).zfill(5)
        opcode = int(instruction[-2:])
        modes = instruction[2::-1]
        
        if opcode in opcode_map:
            param1 = get_parameter(memory, pointer + 1, modes[0], relative_offset)
            param2 = get_parameter(memory, pointer + 2, modes[1], relative_offset)
            output_position = get_parameter(memory, pointer + 3, modes[2], relative_offset, is_write = True)
            
            memory[output_position] = opcode_map[opcode](param1, param2)
            pointer += 4

        elif opcode == 3:
            number_from_input = int(input('Please give me a number: '))
            target_address = get_parameter(memory, pointer + 1, modes[0], relative_offset, is_write = True)
            memory[target_address] = number_from_input
            pointer += 2

        elif opcode in [4, 9]:
            param1 = get_parameter(memory, pointer + 1, modes[0], relative_offset)

            if opcode == 4:
                print(f'The output by opcode 4 is {param1}')
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
            print(f'Program finished. The value at the 0. place of the list is {memory[0]}.\n') 
            return memory[0]
        
        else:
            raise ValueError('No opcode is defined for the current numerical value. Program aborted.')

numbers = read_numbers_from_file('data/input_memory_01.txt')
simulated_computer(numbers)