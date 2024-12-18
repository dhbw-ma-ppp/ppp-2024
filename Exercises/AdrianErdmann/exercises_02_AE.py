import re

# A function to test if a function returns the wanted value
def testFunc(func, *args, result_expect = None):
    result_func = func(*args)
    if result_func == result_expect:
        return True
    return False

# Write a function that takes as input a list of integers and returns a single integer number.
# the numbers passed as argument form the working memory of a simulated computer.
# this computer will start by looking at the first value in the list passed to the function.
# this value will contain an `opcode`. Valid opcodes are 1, 2 or 99.
# Encountering any other value when you expect an opcode indicates an error in your coding.
# Meaning of opcodes:
#  1 indicates addition. If you encounter the opcode 1 you should read values from two positions 
#    of your working memory, add them, and store the result in a third position of your working memory.
#    The three numbers immediately after your opcode indicate the memory locations to read (first two values)
#    and write (third value) respectively. 
#    After executing the addition you should move to the next opcode by stepping forward 4 positions.
#  2 indicates multiplication. Otherwise the same rules apply as for opcode 1.
# 99 indicates halt. the program should stop after encountering the opcode 99.
# After the program stops, the function should return the value in the first location (address 0) 
# of your working memory.

# As an example, if the list of integers passed to your function is 
# [1, 0, 0, 0, 99] the 1 in the first position indicates you should read the values
# at position given by the second and third entries. Both of these indicate position 0, so you should read the value
# at position 0 twice. That value is 1. Adding 1 and 1 gives you two. You then look at the value in the fourth
# position, which is again 0, so you write the result to position 0. You then step forward by 4 steps, arriving at 99
# and ending the program. The final memory looks like [2, 0, 0, 0, 99]. Your function should return 2.

# Here's another testcase:
# [1, 1, 1, 4, 99, 5, 6, 0, 99] should become [30, 1, 1, 4, 2, 5, 6, 0, 99]
# Your function should return 30.

def operation2(memory, i, func):
    """Takes memory and applies func to the numbers at the positions given by i + 1 and i + 2\n
    Writes the result in the cell given at i + 3 and returns the new memory"""
    # execute func on values on position of indices given by cells at i + 1 and i + 2
    result = func(memory[memory[i + 1]], memory[memory[i + 2]])
    # write result in memory cell on index given by cell on i + 3
    memory[memory[i + 3]] = result

def compute(memory):
    i = 0 # i gives position of the opcode for the current execution
    while memory[i] != 99:
        try:
            # choose operation given by opcode
            match memory[i]:
                case 1:
                    # executes an operation with 2 parameters (i+1 and i+2) and addition of the 2
                    operation2(memory, i, lambda a, b: a + b)
                    # increment i
                    i += 4
                case 2:
                    # executes an operation with 2 parameters (i+1 and i+2) and multiplication of the 2
                    operation2(memory, i, lambda a, b: a * b)
                    # increment i
                    i += 4
                case _: # catch unknown opcode and return False
                    break
        
        except IndexError: # to catch if i outranges the length of memory -> memory is not executable
            break
    else: # value should only be returned if memory is executed sucessfully and finishes by opc 99
        return memory[0]
    
    return False # returns False if memory can not be executed sucessfully (with reaching opc 99)

# print out which value is returned by your function for the following list:
commands = [1, 12, 2, 3, 1, 1, 2, 3, 1, 3, 4, 3, 1, 5, 0, 3, 2, 1, 9, 19, 1, 5, 19, 23, 1, 6, 23, 27, 1, 27, 10, 31, 1, 31, 5, 35, 2, 10, 35, 39, 1, 9, 39, 43, 1, 43, 5, 47, 1, 47, 6, 51, 2, 51, 6, 55, 1, 13, 55, 59, 2, 6, 59, 63, 1, 63, 5, 67, 2, 10, 67, 71, 1, 9, 71, 75, 1, 75, 13, 79, 1, 10, 79, 83, 2, 83, 13, 87, 1, 87, 6, 91, 1, 5, 91, 95, 2, 95, 9, 99, 1, 5, 99, 103, 1, 103, 6, 107, 2, 107, 13, 111, 1, 111, 10, 115, 2, 10, 115, 119, 1, 9, 119, 123, 1, 123, 9, 127, 1, 13, 127, 131, 2, 10, 131, 135, 1, 135, 5, 139, 1, 2, 139, 143, 1, 143, 5, 0, 99, 2, 0, 14, 0]
result_commands = compute(commands)
test_result_example = testFunc(compute, [1, 1, 1, 4, 99, 5, 6, 0, 99], result_expect=30)
print(f"The execution of the example was {"sucesfull" if test_result_example else "a failure"}.")
print(f"The List given in the Task returns {result_commands} after execution of the procedure.\n")

###########################################
# Write a function that takes an arbitrary number of unnamed arguments
# All inputs will be of type string.
# the function should return two lists:
#   The first list should contain all arguments which can be interpreted
#   as a number.
#   The second list should contain all strings which contain just one character.
# Think of some good inputs to test this functionality, write down at least three
# examples and verify that the output for these examples is correct.

def isInterpretableAsNumber(to_test):
    """Takes a String an returns True if the String can be interpretet as a Number\n
    assuming all spaces are unimportant formating (for base 10 numbers) and , or . are not assigned directly to the thousand seperator,\n
    they can also be the ten, hundret, ... seperator\n
    Means: Float, Complex (in base notation a + b * i) or BASE-36 (including all bases under BASE-36)"""

    to_test_no_s = to_test.replace(" ", "")

    # check which notation is used and if the notation is used correctly (no .. or ,, but a number between would be ok -> 1,2.5 for 12.3)
    if to_test_no_s.count(",") == 1 and not re.search(r"(.)\1+", to_test_no_s):
        to_test_intformat = to_test_no_s.replace(".", "")
        to_test_intformat = to_test_intformat.replace(",", ".")
    elif to_test_no_s.count(".") == 1 and not re.search(r"(,)\1+", to_test_no_s):
        to_test_intformat = to_test_no_s.replace(",", "")
    else:
        to_test_intformat = to_test_no_s


    try: # test if number can be interpreted as float
        float(to_test_intformat)
    except ValueError : pass
    else: return True

    if to_test_no_s.count("j") == 1: # complex number needs to be as simplified as possible -> a +/- b * c
        to_test_complexformat = to_test_no_s
    elif to_test_no_s.count("i") == 1:
        to_test_complexformat = to_test_no_s.replace("i", "j")
    else: to_test_complexformat = None
    if to_test_complexformat:
        try: # test if number can be interpreted as complex
            complex(to_test_complexformat)
        except ValueError: pass
        else: return True
    
    try: # test if number can be interpreted is Base-36 (including al bases below)
        int(to_test, 36)
    except ValueError: pass
    else: return True

    return False # if nothing of the above applies False is returned

def stringSort(*args):
    """Takes an arbitrary number of unnamed Arguments\n
    All Arguments need to be Strings\n
    Returns one list with all argumnents that can be interpretet as a number\n
    The second list contains all arguments with only one character"""
    first_list = []
    second_list = []
    for ele in args:
        if isInterpretableAsNumber(ele):
            first_list.append(ele)
        if len(ele) == 1:
            second_list.append(ele)
    return first_list, second_list

# first test with all random strings
testparameters = ("abc", "1", "a", "hello", "12", "13", "2635E10", "hello world")
testresult = testFunc(stringSort, *testparameters, result_expect=(['abc', '1', 'a', 'hello', '12', '13', '2635E10'], ['1', 'a']))
print(f"For the testparameters: {testparameters} was the test {"sucesfull" if testresult else "a failure"}.")

# second test with fractal numbers, binary, hex, base 36 and complex numbers
testparameters = ("5.32.32,78", "345,232.00", "010001110101", "23A4C6", "3j - 4j + 5", "3j - 4", "34 + 5j", "A56GHU89L", "3 - 45i", "23..34.45,345")
testresult = testFunc(stringSort, *testparameters, result_expect=(['5.32.32,78', '345,232.00', '010001110101', '23A4C6', '34 + 5j', 'A56GHU89L', '3 - 45i'], []))
print(f"For the testparameters: {testparameters} was the test {"sucesfull" if testresult else "a failure"}.")

# third test with whitespaces and special characters
testparameters = ("a b c", "1", "a", " ", "  ", "%", "§", "5%3")
testresult = testFunc(stringSort, *testparameters, result_expect=(["1", "a"], ["1", "a", " ", "%", "§"]))
print(stringSort(*testparameters))
print(f"For the testparameters: {testparameters} was the test {"sucesfull" if testresult else "a failure"}.")
