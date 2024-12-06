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

with open('data/input_memory_01.txt') as file:
    content = file.read()
    commands = [int(numbers) for numbers in content.split(",")]

#commands = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]

def intcode_process(memory):

    pointer = 0   # position of pointer
    relative_offset = 0  # offset start

    def get_instruction(instruction):
        opcode = instruction % 100
        param_mode1 = (instruction // 100) % 10
        param_mode2 = (instruction // 1000) % 10
        param_mode3 = (instruction // 10000) % 10
        return opcode, param_mode1, param_mode2, param_mode3

    def check_memoryspace(memory, index):
        if index >= len(memory):
            memory.extend([0] * (index - len(memory) + 1))
    
    def get_pointer_position(pointer):
        check_memoryspace(memory, pointer + 3)
        pos1 = memory[pointer + 1]
        pos2 = memory[pointer + 2]
        pos3 = memory[pointer + 3]
        return pos1, pos2, pos3

    def check_mode(pos, mode, relative_offset):
        if mode == 0:  # position-mode
            check_memoryspace(memory, pos)
            return memory[pos]
        elif mode == 1:  # immediate-mode
            return pos
        elif mode == 2:  # relative-mode
            check_memoryspace(memory, pos + relative_offset)
            return memory[pos + relative_offset]
        else:
            raise ValueError(f"Invalid Mode: {mode}")

    while True:
        instruction = memory[pointer]
        opcode, param_mode1, param_mode2, param_mode3 = get_instruction(instruction)
        pos1, pos2, pos3 = get_pointer_position(pointer)

        match opcode:

            case 99:  # end of program
                return memory

            case 1:  # addition
                if param_mode3 == 2:
                    pos3 += relative_offset
                check_memoryspace(memory, pos3)
                memory[pos3] = check_mode(pos1, param_mode1, relative_offset) + check_mode(pos2, param_mode2, relative_offset)
                pointer += 4

            case 2:  # multiplication
                if param_mode3 == 2:
                    pos3 += relative_offset
                check_memoryspace(memory, pos3)
                memory[pos3] = check_mode(pos1, param_mode1, relative_offset) * check_mode(pos2, param_mode2, relative_offset)
                pointer += 4

            case 3:  # input
                if param_mode1 == 2:
                    pos1 += relative_offset
                check_memoryspace(memory, pos1)
                while True:
                    input_value = input("Input a whole Number: ")
                    if input_value.lstrip('-').isdigit():  # Allow negative numbers
                        memory[pos1] = int(input_value)
                        break
                    else:
                        print(f"Invalid Input: {input_value}. Please enter a whole number.\n")
                pointer += 2

            case 4:  # output
                print(f"Value: {check_mode(pos1, param_mode1, relative_offset)}")
                pointer += 2

            case 5:  # jump-if-true
                if check_mode(pos1, param_mode1, relative_offset) != 0:
                    pointer = check_mode(pos2, param_mode2, relative_offset)
                else:
                    pointer += 3

            case 6:  # jump-if-false
                if check_mode(pos1, param_mode1, relative_offset) == 0:
                    pointer = check_mode(pos2, param_mode2, relative_offset)
                else:
                    pointer += 3

            case 7:  # less than
                if param_mode3 == 2:
                    pos3 += relative_offset
                check_memoryspace(memory, pos3)
                if check_mode(pos1, param_mode1, relative_offset) < check_mode(pos2, param_mode2, relative_offset):
                    memory[pos3] = 1
                else:
                    memory[pos3] = 0
                pointer += 4

            case 8:  # equals
                if param_mode3 == 2:
                    pos3 += relative_offset
                check_memoryspace(memory, pos3)
                if check_mode(pos1, param_mode1, relative_offset) == check_mode(pos2, param_mode2, relative_offset):
                    memory[pos3] = 1
                else:
                    memory[pos3] = 0
                pointer += 4

            case 9:  # adjust relative base
                relative_offset += check_mode(pos1, param_mode1, relative_offset)
                pointer += 2

            case _:  # Error
                raise ValueError(f"Invalid Opcode {opcode} found at position {pointer}")

result = intcode_process(commands)
print("First Value in Memory:", result[0])
print(result)
