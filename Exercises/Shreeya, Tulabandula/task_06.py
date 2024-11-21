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


import itertools
from collections import defaultdict

def file_read(file):
    with open(file, 'r') as file:
        return list(map(int, file.read().strip().split(',')))

def file_run(file_path):
    memory = file_read(file_path)
    execute_program(memory)

def execute_program(memory):
    position = 0
    relative_base = 0
    outputs = []
    memory = defaultdict(int, enumerate(memory))

    def get_value(param, mode):
        if mode == 0:
            return memory[param]
        elif mode == 1: 
            return param
        elif mode == 2: 
            return memory[relative_base + param]
        else:
            raise ValueError(f"Invalid mode: {mode}")

    def set_value(param, mode, value):
        if mode == 0: 
            memory[param] = value
        elif mode == 2:  
            memory[relative_base + param] = value
        else:
            raise ValueError(f"Invalid mode: {mode}")

    while True:
        instruction = memory[position]
        opcode = instruction % 100
        mode1 = (instruction // 100) % 10
        mode2 = (instruction // 1000) % 10
        mode3 = (instruction // 10000) % 10

        if opcode == 1: 
            param1 = get_value(memory[position + 1], mode1)
            param2 = get_value(memory[position + 2], mode2)
            set_value(memory[position + 3], mode3, param1 + param2)
            position += 4
        elif opcode == 2:  
            param1 = get_value(memory[position + 1], mode1)
            param2 = get_value(memory[position + 2], mode2)
            set_value(memory[position + 3], mode3, param1 * param2)
            position += 4
        elif opcode == 3:  
            user_input = int(input("Enter a number: "))
            set_value(memory[position + 1], mode1, user_input)
            position += 2
        elif opcode == 4:  
            output_value = get_value(memory[position + 1], mode1)
            outputs.append(output_value)
            position += 2
        elif opcode == 5:  
            param1 = get_value(memory[position + 1], mode1)
            param2 = get_value(memory[position + 2], mode2)
            position = param2 if param1 != 0 else position + 3
        elif opcode == 6: 
            param1 = get_value(memory[position + 1], mode1)
            param2 = get_value(memory[position + 2], mode2)
            position = param2 if param1 == 0 else position + 3
        elif opcode == 7:  
            param1 = get_value(memory[position + 1], mode1)
            param2 = get_value(memory[position + 2], mode2)
            set_value(memory[position + 3], mode3, 1 if param1 < param2 else 0)
            position += 4
        elif opcode == 8: 
            param1 = get_value(memory[position + 1], mode1)
            param2 = get_value(memory[position + 2], mode2)
            set_value(memory[position + 3], mode3, 1 if param1 == param2 else 0)
            position += 4
        elif opcode == 9:  
            relative_base += get_value(memory[position + 1], mode1)
            position += 2
        elif opcode == 99: 
            break
        else:
            raise ValueError(f"Unknown opcode: {opcode}")

    print(outputs)

# test_program = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
# execute_program(test_program)  # Output: copy of test_program list

file = 'data/input_memory_01.txt'  
file_run(file)
