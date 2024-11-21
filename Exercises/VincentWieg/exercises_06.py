
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

def listChange(listOfInt):
    def get_value(index, mode, offset):
        if mode == 0:  # position mode
            return listOfInt[listOfInt[index]]
        elif mode == 1:  # immediate mode
            return listOfInt[index]
        elif mode == 2:  # relative mode
            return listOfInt[listOfInt[index + offset]]


    i = 0
    offset = 0  # Relative base
    while True:
        op_code = listOfInt.get(i, 0) % 100
        mode_parameter_1 = (listOfInt[i] // 100) % 10
        mode_parameter_2 = (listOfInt[i] // 1000) % 10
        mode_parameter_3 = (listOfInt[i] // 10000) % 10

        if op_code == 1:  # add
            set_value(i + 3,
                      get_value(i + 1, mode_parameter_1, offset) + get_value(i + 2, mode_parameter_2, offset),
                      mode_parameter_3, offset)
            i += 4
        elif op_code == 2:  # multiply
            set_value(i + 3,
                      get_value(i + 1, mode_parameter_1, offset) * get_value(i + 2, mode_parameter_2, offset),
                      mode_parameter_3, offset)
            i += 4
        elif op_code == 3:  # input
            user_input = int(input("Enter Input: "))
            set_value(i + 1, user_input, mode_parameter_1, offset)
            i += 2
        elif op_code == 4:  # output
            print(get_value(i + 1, mode_parameter_1, offset))
            i += 2
        elif op_code == 5:  # jump-if-true
            if get_value(i + 1, mode_parameter_1, offset) != 0:
                i = get_value(i + 2, mode_parameter_2, offset)
            else:
                i += 3
        elif op_code == 6:  # jump-if-false
            if get_value(i + 1, mode_parameter_1, offset) == 0:
                i = get_value(i + 2, mode_parameter_2, offset)
            else:
                i += 3
        elif op_code == 7:  # less than
            set_value(i + 3,
                      1 if get_value(i + 1, mode_parameter_1, offset) < get_value(i + 2, mode_parameter_2, offset) else 0,
                      mode_parameter_3, offset)
            i += 4
        elif op_code == 8:  # equals
            set_value(i + 3,
                      1 if get_value(i + 1, mode_parameter_1, offset) == get_value(i + 2, mode_parameter_2, offset) else 0,
                      mode_parameter_3, offset)
            i += 4
        elif op_code == 9:  # adjust relative base
            offset += get_value(i + 1, mode_parameter_1, offset)
            i += 2
        elif op_code == 99:  # halt
            break
        else:
            print(f"Error: Unknown opcode {op_code} at position {i}")
            break

    return listOfInt


def start_memory(list):
    input_dict = {index: value for index, value in enumerate(list)}
    listChange(input_dict)


# Load input from file
with open("data\input_memory_01.txt", "r") as file:
    program = list(map(int, file.read().strip().split(',')))

start_memory(program)
