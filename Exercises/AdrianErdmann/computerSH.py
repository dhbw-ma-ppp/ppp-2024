# Represents Soerens int computer cause mine did some weird stuff (I wansn't able to move the paddle)
import subprocess
import enum
import os
from colorama import Fore
import logging
import time
import random
from sys import platform
from computerAE import memoryToUsableDict

automated = False

class op_mode(enum.Enum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2

class operations(enum.Enum):
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


return_list = []


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
    return idx, dct


def output_value(dct: dict, idx: int, instruction: list, offset: int) -> int:
    """Handles output value operation (opcode 4)."""
    global return_list
    param_mode = op_mode(int(instruction[0]))
    idx += 1
    output = get_element(param_mode, dct, idx, offset)
    return_list.append(output)
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
    return idx, end, offset


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


class ExecutionManager:
    def __init__(self, memory: list|dict) -> None:
        if type(memory) == dict:
            self.memory = memory
        elif type(memory) == list:
            self.memory = memoryToUsableDict(memory)
        else:
            raise ValueError
        self.offset = 0
        self.working_adress = 0
        self.max_parameters_needed = 3
        return

    def computeToNextTriplet(self):
        global return_list
        return_list = []
        end = False
        while end is False and len(return_list) < 3:
            self.working_adress, end, self.offset = check_for_opcode(self.working_adress, self.memory, self.offset)
        return return_list
