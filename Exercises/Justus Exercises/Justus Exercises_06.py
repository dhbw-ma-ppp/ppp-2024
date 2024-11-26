
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



import os
from collections import defaultdict


def parse_instruction(instruction):
    """
    Parses an instruction into opcode and parameter modes.
    - The last two digits represent the opcode (e.g., 1 for addition, 2 for multiplication).
    - The other digits represent parameter modes, in order:
    """
    opcode = instruction % 100  # Extract the last two digits
    modes = [(instruction // 10 ** i) % 10 for i in range(2, 5)]
    return opcode, modes


def intcode_computer(memory):
    """
    Simulates the Intcode computer.
    - Memory is initialized from the input list and expanded as needed using defaultdict.
    - Executes instructions in a loop until encountering opcode 99 (halt).
    """
    memory = defaultdict(int, enumerate(memory)) # Convert the memory list into a defaultdict
    relative_base = 0 # Tracks the relative base for mode 2 operations
    i = 0 # Instruction pointer
    output = None # Holds the last output value

    def get_value(param, mode):
        if mode == 0: # Position mode
            return memory[param]
        elif mode == 1: # Immediate mode
            return param
        elif mode == 2: # Relative mode
            return memory[relative_base + param]
        else:
            raise ValueError(f"Invalid parameter mode: {mode}")

    def write_value(param, mode, value):
        if mode == 0: # Position mode
            memory[param] = value
        elif mode == 2: # Relative mode
            memory[relative_base + param] = value
        else:
            raise ValueError(f"Invalid parameter mode for writing: {mode}")

    while True:
        instruction = memory[i]
        opcode, modes = parse_instruction(instruction)
        mode1, mode2, mode3 = modes

        if opcode == 99:
            break

        elif opcode == 1:  # Addition
            param1, param2, param3 = memory[i + 1], memory[i + 2], memory[i + 3]
            write_value(param3, mode3, get_value(param1, mode1) + get_value(param2, mode2))
            i += 4

        elif opcode == 2:  # Multiplication
            param1, param2, param3 = memory[i + 1], memory[i + 2], memory[i + 3]
            write_value(param3, mode3, get_value(param1, mode1) * get_value(param2, mode2))
            i += 4

        elif opcode == 3:  # Input
            param1 = memory[i + 1]
            input_val = int(input("Please enter a number: "))  # Prompt the user for input
            write_value(param1, mode1, input_val)
            i += 2

        elif opcode == 4:  # Output
            param1 = memory[i + 1]
            output = get_value(param1, mode1)
            print(f"Output: {output}")
            i += 2

        elif opcode == 5:  # Jump-if-true
            param1, param2 = memory[i + 1], memory[i + 2]
            if get_value(param1, mode1) != 0:
                i = get_value(param2, mode2)
            else:
                i += 3

        elif opcode == 6:  # Jump-if-false
            param1, param2 = memory[i + 1], memory[i + 2]
            if get_value(param1, mode1) == 0:
                i = get_value(param2, mode2)
            else:
                i += 3

        elif opcode == 7:  # Less than
            param1, param2, param3 = memory[i + 1], memory[i + 2], memory[i + 3]
            write_value(param3, mode3, 1 if get_value(param1, mode1) < get_value(param2, mode2) else 0)
            i += 4

        elif opcode == 8:  # Equals
            param1, param2, param3 = memory[i + 1], memory[i + 2], memory[i + 3]
            write_value(param3, mode3, 1 if get_value(param1, mode1) == get_value(param2, mode2) else 0)
            i += 4

        elif opcode == 9:  # Adjust relative base
            param1 = memory[i + 1]
            relative_base += get_value(param1, mode1)
            i += 2

        else:
            raise ValueError(f"Unknown opcode {opcode} encountered at index {i}")

    return output

def load_memory_from_file(file_path):
    """
    Reads a file containing a comma-separated list of integers and returns it as a list.
    """
    with open(file_path, 'r') as file:
        return list(map(int, file.read().strip().split(',')))

# Determine the path to the input file (assumes file is in the same directory as this script)
current_dir = os.path.dirname(__file__)
data_file_path = os.path.join(current_dir, 'InputMemory.txt')

# Load memory from the file
memory = load_memory_from_file(data_file_path)

# Run the computer
result = intcode_computer(memory)
print("Final output:", result)
