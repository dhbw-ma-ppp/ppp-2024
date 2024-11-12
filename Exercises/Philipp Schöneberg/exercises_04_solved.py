import operator

# Extend the simulated computer from the second week:
# You will need to support a number of additional opcodes:
# - 3: read a single integer as input and save it to the position given
#      by its only parameter. the command 3,19 would read an input
#      and store the result at address 19
# - 4: output the value of the single parameter for this opcode.
#      for example 4,19 would output the value stored at address 19
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
commands = [3,225,1,225,6,6,1100,1,238,225,104,0,1101,40,71,224,1001,224,-111,224,4,224,1002,223,8,223,101,7,224,224,1,224,223,223,1102,66,6,225,1102,22,54,225,1,65,35,224,1001,224,-86,224,4,224,102,8,223,223,101,6,224,224,1,224,223,223,1102,20,80,225,101,92,148,224,101,-162,224,224,4,224,1002,223,8,223,101,5,224,224,1,224,223,223,1102,63,60,225,1101,32,48,225,2,173,95,224,1001,224,-448,224,4,224,102,8,223,223,1001,224,4,224,1,224,223,223,1001,91,16,224,101,-79,224,224,4,224,1002,223,8,223,101,3,224,224,1,224,223,223,1101,13,29,225,1101,71,70,225,1002,39,56,224,1001,224,-1232,224,4,224,102,8,223,223,101,4,224,224,1,223,224,223,1101,14,59,225,102,38,143,224,1001,224,-494,224,4,224,102,8,223,223,101,3,224,224,1,224,223,223,1102,30,28,224,1001,224,-840,224,4,224,1002,223,8,223,101,4,224,224,1,223,224,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,107,677,226,224,1002,223,2,223,1005,224,329,1001,223,1,223,8,226,226,224,102,2,223,223,1006,224,344,101,1,223,223,7,226,677,224,1002,223,2,223,1005,224,359,101,1,223,223,1007,677,226,224,1002,223,2,223,1005,224,374,1001,223,1,223,1007,677,677,224,1002,223,2,223,1006,224,389,101,1,223,223,1008,226,226,224,1002,223,2,223,1005,224,404,1001,223,1,223,108,677,226,224,1002,223,2,223,1006,224,419,1001,223,1,223,1108,677,226,224,102,2,223,223,1006,224,434,1001,223,1,223,108,226,226,224,1002,223,2,223,1005,224,449,101,1,223,223,7,677,677,224,1002,223,2,223,1006,224,464,1001,223,1,223,8,226,677,224,1002,223,2,223,1005,224,479,1001,223,1,223,107,226,226,224,102,2,223,223,1006,224,494,101,1,223,223,1007,226,226,224,1002,223,2,223,1005,224,509,1001,223,1,223,1107,226,677,224,102,2,223,223,1005,224,524,1001,223,1,223,108,677,677,224,1002,223,2,223,1005,224,539,101,1,223,223,1107,677,226,224,102,2,223,223,1005,224,554,1001,223,1,223,107,677,677,224,1002,223,2,223,1005,224,569,101,1,223,223,8,677,226,224,102,2,223,223,1005,224,584,1001,223,1,223,7,677,226,224,102,2,223,223,1006,224,599,101,1,223,223,1008,677,677,224,1002,223,2,223,1005,224,614,101,1,223,223,1008,677,226,224,102,2,223,223,1006,224,629,1001,223,1,223,1108,677,677,224,102,2,223,223,1006,224,644,101,1,223,223,1108,226,677,224,1002,223,2,223,1005,224,659,1001,223,1,223,1107,226,226,224,102,2,223,223,1006,224,674,1001,223,1,223,4,223,99,226]


def compute(lst):
    """
    This function takes as input a list of integers and returns a single
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
    def get_opcode_indices_and_parameter():
        """
        This function calculates the needed opcode, indices and parameter needed
        to compute the next instruction. 
        """
        nonlocal opcode, index_1, index_2, index_3, parameter_1, parameter_2
        extended_opcode = lst[i]
        opcode = extended_opcode % 100
        extended_opcode = extended_opcode // 100
        if len(lst)-1 > i:
            index_1 = lst[i+1]
        if len(lst)-1 > i+1:
            index_2 = lst[i+2]
        if len(lst)-1 > i+2:
            index_3 = lst[i+3]
        if extended_opcode % 10 == 1:
            parameter_1 = index_1
            extended_opcode = extended_opcode // 10
        else:
            if len(lst)-1 > index_1-1:
                parameter_1 = lst[index_1]
                extended_opcode = extended_opcode // 10
        if extended_opcode % 10 == 1:
            parameter_2 = index_2
            extended_opcode = extended_opcode // 10
        else:
            if len(lst)-1 > index_2-1:
                parameter_2 = lst[index_2]
                extended_opcode = extended_opcode // 10

    i, opcode, index_1, index_2, index_3, parameter_1, parameter_2 = 0, 0, 0, 0, 0, 0, 0
    operations_with_two_parameters = {
        1: operator.add,
        2: operator.mul,
        7: operator.is_not,
        8: operator.is_
    }
    while True:
        try:
            get_opcode_indices_and_parameter()
            match opcode:
                case 1 | 2 | 7 | 8:
                    lst[index_3] = operations_with_two_parameters[opcode](parameter_1, parameter_2)
                    i += 4
                case 3:
                    while True:
                        try:
                            user_input = int(input("Enter an integer: "))
                            break
                        except ValueError:
                            print("The given input was not an integer.")
                    lst[index_1] = user_input
                    i += 2
                case 4:
                    print(f"The value at index {index_1} is {parameter_1}.")
                    i += 2
                case 5:
                    if parameter_1 != 0:
                        i = parameter_2
                    else:
                        i += 3
                case 6:
                    if parameter_1 == 0:
                        i = parameter_2
                    else:
                        i += 3
                case 99:
                    break
                case _:
                    raise RuntimeError("The given opcode is unvalid.")
        except IndexError:
            raise RuntimeError("The given commandlist is unvalid.")
    return lst[0]


def test_compute():
    assert compute([1, 0, 0, 0, 99]) == 2
    assert compute([1, 1, 1, 4, 99, 5, 6, 0, 99]) == 30
    print('Function "compute" tested succesfully!')


test_compute()

print(compute([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]))  # 8
print(compute([3, 3, 1107, -1, 8, 3, 4, 3, 99]))  # 8
print(compute([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1]))  # 0

print(compute(commands))
