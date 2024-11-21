import operator
from collections import defaultdict

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


class commandsIterator:
    def __init__(self):
        self.input_file: str
        self.input_file = "input_memory_01.txt"

    def __iter__(self):
        with open(self.input_file, "r") as f:
            for line in f:
                line = line.split(",")
                for elem in line:
                    try:
                        yield int(elem)
                    except ValueError:
                        pass


def compute(commands_iterable: object) -> int:
    """
    This function takes as input an iterator of integers and returns a single
    integer number. The numbers passed as argument form the working memory of
    a simulated computer. This computer will start by looking at the first
    value in the list passed to the function. This value will contain an `
    opcode`. Valid opcodes are 1, 2, 3, 4, 5, 6, 7, 8 or 99. Encountering any
    other value when expecting an opcode or a lengthwise unfitting list will
    raise an RuntimeError. The meaning of opcodes is as follows:
    - 1 indicates addition. The function will read values from the next two
    positions of your working memory, add them, and store the result in the
    third position of your working memory. The three numbers immediately after
    your opcode indicate the memory locations to read (first two values) and
    write (third value) respectively.
    - 2 indicates multiplication. Otherwise the same rules apply as for opcode 1.
    - 3: read a single integer as input and save it to the position given by
    its only parameter.
    - 4: output the value of the single parameter for this opcode.
    - 5: jump-if-true: if the first parameter is non-zero, it sets the
    instruction pointer to the value from the second parameter. Otherwise, it
    does nothing.
    - 6: jump-if-false: if the first parameter is zero, it sets the instruction
    pointer to the value from the second parameter. Otherwise, it does nothing.
    - 7: less than: if the first parameter is less than the second parameter,
    it stores 1 in the position given by the third parameter. Otherwise, it
    stores 0.
    - 8: equals: if the first parameter is equal to the second parameter, it
    stores 1 in the position given by the third parameter. Otherwise, it stores 0.
    - 99 indicates halt. the program should stop after encountering the opcode 99.\n
    After the program stops, the function should return the value in the first
    location (address 0) of your working memory.
    """
    def get_command(index: int) -> int:
        """
        This function expects an integer and returns the value stored under
        the corresponding key from the dictionary commands. If there is no
        corresponding key, it will create one with the value zero using its
        classability as a defauldict and then return it.
        """
        if index >= 0:
            return commands[index]
        else:
            raise RuntimeError("The index can't be negative.")

    def get_opcode() -> None:
        """
        This function calculates the opcode needed to compute the next
        instruction.
        """
        nonlocal extended_opcode, opcode

        extended_opcode = get_command(instruction_pointer)
        opcode = extended_opcode % 100
        extended_opcode = extended_opcode // 100

    def get_indices_and_parameter(parameter_amount: int) -> None:
        """
        This function takes as input an integer representing the number of
        parameters needed for the next operation. It then calculates the
        corresponding indices and parameters.
        """
        nonlocal extended_opcode
        for i in range(0, parameter_amount):
            indices[i] = get_command(instruction_pointer+i+1)
            if extended_opcode % 10 == 1:
                parameter[i] = indices[i]
            elif extended_opcode % 10 == 2:
                indices[i] += relative_offset
                parameter[i] = get_command(indices[i])
            else:
                parameter[i] = get_command(indices[i])
            extended_opcode = extended_opcode // 10

    commands: defaultdict[int, int] = defaultdict(int)
    operations_with_three_parameters: dict[int, object]
    operations_with_two_parameters: dict[int, object]
    parameter: dict[int, int] = {}
    indices: dict[int, int] = {}
    instruction_pointer: int = 0
    relative_offset: int = 0
    extended_opcode: int = 0
    opcode: int = 0

    for i, elem in enumerate(commands_iterable):
        commands[i] = elem
    operations_with_three_parameters = {
        1: operator.add,
        2: operator.mul,
        7: lambda x, y: 1 if x < y else 0,
        8: lambda x, y: 1 if x == y else 0,
    }
    operations_with_two_parameters = {
        5: lambda x, y: y if x != 0 else instruction_pointer+3,
        6: lambda x, y: y if x == 0 else instruction_pointer+3,
    }

    while True:
        try:
            get_opcode()
            match opcode:
                case 1 | 2 | 7 | 8:
                    get_indices_and_parameter(3)
                    commands[indices[2]] = operations_with_three_parameters[opcode](parameter[0], parameter[1])
                    instruction_pointer += 4
                case 3:
                    get_indices_and_parameter(1)
                    while True:
                        try:
                            user_input = int(input("Enter an integer: "))
                            break
                        except ValueError:
                            print("The given input was not an integer.")
                    commands[indices[0]] = user_input
                    instruction_pointer += 2
                case 4:
                    get_indices_and_parameter(1)
                    print(f"The value at index {indices[0]} is {parameter[0]}.")
                    instruction_pointer += 2
                case 5 | 6:
                    get_indices_and_parameter(2)
                    instruction_pointer = operations_with_two_parameters[opcode](parameter[0], parameter[1])
                case 9:
                    get_indices_and_parameter(1)
                    relative_offset += parameter[0]
                    instruction_pointer += 2
                case 99:
                    break
                case _:
                    raise RuntimeError("The given opcode is unvalid.")
        except IndexError:
            raise RuntimeError("The given commandlist is unvalid.")
    return commands[0]


def test_compute():
    assert compute([1, 0, 0, 0, 99]) == 2
    assert compute([1, 1, 1, 4, 99, 5, 6, 0, 99]) == 30
    print('Function "compute" tested succesfully!')


test_compute()

print(compute([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]))                # Test function requiring 8 as input.
print(compute([3, 3, 1107, -1, 8, 3, 4, 3, 99]))                    # Test function requiring 8 as input.
print(compute([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1]))   # Test function requiring 0 as input.

print(compute([109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]))

compute(commandsIterator())
