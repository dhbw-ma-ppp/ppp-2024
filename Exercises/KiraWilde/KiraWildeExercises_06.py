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

# The actual input is in a separate file, input_memory_01.txt under the `data` folder.
# When asked for input provide the value 2. There should be a single output. Please include it in your PR.


#Instead of using a set as before, I now use a dictionary to address an 'infinitely' large storage space.
def load_memory_from_file(file_path):
    with open(file_path, "r") as file:
        content = file.read().strip()
        # The file contains values such as “1,0,0,0,99”, which are converted into a dictionary
        memory = {i: int(value) for i, value in enumerate(content.split(","))}
    return memory

def get_value(memory, parameter, mode, relative_base):
    if mode == 0:
        # Position mode: fetch value from the address given by parameter
        return memory.get(parameter, 0)
    elif mode == 1:
        # Immediate mode: use parameter directly as value
        return parameter
    elif mode == 2:
        # # Relative mode: fetch value from address given by (relative_base + parameter)
        return memory.get(relative_base + parameter, 0)
    else:
        raise ValueError(f"Invalid parameter mode: {mode}")


def write_value(memory, address, mode, relative_base, value):
    if mode == 0:
        # Position mode
        memory[address] = value
    elif mode == 2:
        # Relative mode
        memory[relative_base + address] = value
    else:
        raise ValueError("Write address must not be in Immediate mode")


def simulate_computer(memory_list):
    pointer = 0
    relativ_offset = 0

    while True:
        instruction = memory.get(pointer, 0)
        opcode = instruction % 100
        mode1 = (instruction // 100) % 10
        mode2 = (instruction // 1000) % 10
        mode3 = (instruction // 10000) % 10

        if opcode == 99:
            break
        elif opcode in [1, 2, 7, 8]:
            param1 = get_value(memory, memory.get(pointer + 1, 0), mode1, relativ_offset)
            param2 = get_value(memory, memory.get(pointer + 2, 0), mode2, relativ_offset)
            if opcode == 1:
                # Addition
                write_value(memory, memory.get(pointer + 3, 0), mode3, relativ_offset, param1 + param2)
            elif opcode == 2:
                # Multiplication
                write_value(memory, memory.get(pointer + 3, 0), mode3, relativ_offset, param1 * param2)
            elif opcode == 7:
                # Less than
                write_value(memory, memory.get(pointer + 3, 0), mode3, relativ_offset, 1 if param1 < param2 else 0)
            elif opcode == 8:
                # Equals
                write_value(memory, memory.get(pointer + 3, 0), mode3, relativ_offset, 1 if param1 == param2 else 0)
            pointer += 4
        elif opcode in [3, 4]:
            if opcode == 3:
                 # User input
                user_input = int(input("Enter an integer: "))
                write_value(memory, memory.get(pointer + 3, 0), mode3, relativ_offset, user_input)
            elif opcode == 4:
                # Output
                param1 = get_value(memory, memory.get(pointer + 1, 0), mode1, relativ_offset)
                print(param1)
            pointer += 2
        elif opcode in [5, 6]:
            param1 = get_value(memory, memory.get(pointer + 1, 0), mode1, relativ_offset)
            param2 = get_value(memory, memory.get(pointer + 2, 0), mode2, relativ_offset)
            if opcode == 5:
                # Jump-if-true
                pointer = param2 if param1 != 0 else pointer + 3
            elif opcode == 6:
                pointer = param2 if param1 == 0 else pointer + 3
        elif opcode == 9:
            # relative base adjustment
            param1 = get_value(memory, memory.get(pointer +1, 0), mode1, relativ_offset)
            relativ_offset += param1
            pointer += 2
        else:
            raise ValueError(f"Invalid opcode {opcode} at position {pointer}")
    return memory.get(0, 0)


file_path = "input_memory_01.txt"  # Pfad zur Eingabedatei
memory = load_memory_from_file(file_path)
result = simulate_computer(memory)
print(f"Resultat: {result}")
#Result 33343
