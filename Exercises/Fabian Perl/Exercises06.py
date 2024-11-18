
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

class Memory:                                                   #checks if index is in bounds, resizes list accordingly if not
    
    def __init__(self, contents):
        self.contents = contents
        self.max_index = len(self.contents) - 1
    
    def __getitem__(self, key):
        if key > self.max_index:
            self.contents += [0] * (key - self.max_index)   
        return self.contents[key]
    
    def __setitem__(self, key, new_val):
        if key > self.max_index:
            self.contents += [0] * (key - self.max_index)   
        self.contents[key] = new_val
            

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

def take_int_input():                                        #accept only int inputs
    while True:
        try:
            return int(input("Enter a number: "))
        except ValueError:
            continue

def compute_oppcodes(memory):
    pointer = 0
    offset = 0
    memory = Memory(memory)
    while True:
        current_value = memory[pointer]
        if current_value % 100 == 1:
            parameter_num = 3
            parameters = make_param_list(memory, pointer, parameter_num, offset)
            memory[parameters[-1]] = memory[parameters[0]] + memory[parameters[1]]
            pointer += (parameter_num + 1)
        elif current_value % 100 == 2:
            parameter_num = 3
            parameters = make_param_list(memory, pointer, parameter_num, offset)
            memory[parameters[-1]] = memory[parameters[0]] * memory[parameters[1]]
            pointer += (parameter_num + 1)
        elif current_value % 100 == 3:    
            parameter_num = 1
            parameters = make_param_list(memory, pointer, parameter_num, offset)
            memory[parameters[-1]] = take_int_input()
            pointer += (parameter_num + 1)
        elif current_value % 100 == 4:
            parameter_num = 1
            parameters = make_param_list(memory, pointer, parameter_num, offset)
            print(memory[parameters[0]])
            pointer += (parameter_num + 1)
        elif current_value % 100 == 5:
            parameter_num = 2
            parameters = make_param_list(memory, pointer, parameter_num, offset)
            if memory[parameters[0]] != 0:
                pointer = memory[parameters[1]]
            else:
                pointer += (parameter_num + 1)
        elif current_value % 100 == 6:
            parameter_num = 2
            parameters = make_param_list(memory, pointer, parameter_num, offset)
            if memory[parameters[0]] == 0:
                pointer = memory[parameters[1]]
            else:
                pointer += (parameter_num + 1)
        elif current_value % 100 == 7:
            parameter_num = 3
            parameters = make_param_list(memory, pointer, parameter_num, offset)
            if memory[parameters[0]] < memory[parameters[1]]:
                memory[parameters[-1]] = 1
            else:
                memory[parameters[-1]] = 0
            pointer += (parameter_num + 1)
        elif current_value % 100 == 8:
            parameter_num = 3
            parameters = make_param_list(memory, pointer, parameter_num, offset)
            if memory[parameters[0]] == memory[parameters[1]]:
                memory[parameters[-1]] = 1
            else:
                memory[parameters[-1]] = 0
            pointer += (parameter_num + 1)
        elif current_value % 100 == 9:
            parameter_num = 1
            parameters = make_param_list(memory, pointer, parameter_num, offset)
            offset += memory[parameters[0]]
            pointer += (parameter_num + 1)
        elif current_value % 100 == 99:
            break
        else:
            print(f"Wrong oppcode {memory[pointer]} encountert at pointer {pointer}.")
            break

commands = []
with open("data/input_memory_01.txt", "r") as file:
    for i in next(file).split(","):
        commands.append(int(i))

compute_oppcodes(commands)
