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

def simulateComputer (memory):
    pointer = 0
    while True:
        opcode = memory[pointer]
        # I have decided against using an if-else structure here, but in this case, it would have served the same purpose as a match-case.
        match opcode:
            case 99:
                # Programm endet
                break
            case 1:
                # Addition
                firstAddend = memory[pointer + 1]
                secondAddend = memory[pointer + 2]
                resultPosition = memory[pointer + 3]
                memory[resultPosition] = memory[firstAddend] + memory[secondAddend]
            case 2:
                # Multiplication
                firstFactor = memory[pointer + 1]
                secondFactor = memory[pointer + 2]
                resultPosition = memory[pointer + 3]
                memory[resultPosition] = memory[firstFactor] * memory[secondFactor]
            case _:
                # opced != 1,2 or 99
                raise ValueError(f"Invalid opcode {opcode} at position {pointer}")
                # ValueError definition: Raised when an operation or function receives an argument that has the right type but an inappropriate value [...]
        pointer += 4
    return memory[0]

# print out which value is returned by your function for the following list:
commands = [1, 12, 2, 3, 1, 1, 2, 3, 1, 3, 4, 3, 1, 5, 0, 3, 2, 1, 9, 19, 1, 5, 19, 23, 1, 6, 23, 27, 1, 27, 10, 31, 1, 31, 5, 35, 2, 10, 35, 39, 1, 9, 39, 43, 1, 43, 5, 47, 1, 47, 6, 51, 2, 51, 6, 55, 1, 13, 55, 59, 2, 6, 59, 63, 1, 63, 5, 67, 2, 10, 67, 71, 1, 9, 71, 75, 1, 75, 13, 79, 1, 10, 79, 83, 2, 83, 13, 87, 1, 87, 6, 91, 1, 5, 91, 95, 2, 95, 9, 99, 1, 5, 99, 103, 1, 103, 6, 107, 2, 107, 13, 111, 1, 111, 10, 115, 2, 10, 115, 119, 1, 9, 119, 123, 1, 123, 9, 127, 1, 13, 127, 131, 2, 10, 131, 135, 1, 135, 5, 139, 1, 2, 139, 143, 1, 143, 5, 0, 99, 2, 0, 14, 0]

# print(simulateComputer([1, 1, 1, 4, 99, 5, 6, 0, 99])) #test one
# print(simulateComputer([20, 1, 1, 4, 99, 5, 6, 0, 99])) #Trigger for ValueError
print(simulateComputer(commands),"\n")

###########################################
# Write a function that takes an arbitrary number of unnamed arguments
# All inputs will be of type string.
# the function should return two lists:
#   The first list should contain all arguments which can be interpreted
#   as a number.
#   The second list should contain all strings which contain just one character.
# Think of some good inputs to test this functionality, write down at least three
# examples and verify that the output for these examples is correct.

def categorizeArguments(*args):
    numbers = []
    singleChars = []

    for arg in args:
        try:
            float(arg) # can interprete "123","5.5","-58" and "1e8" as an number
            numbers.append(arg)
        except ValueError:
            # If a ValueError is raised, it means the string could not be converted to a float,
            # indicating that it is not a valid number. We then check if it's a single character or a word.
            if len(arg) == 1:
                singleChars.append(arg)
    return numbers, singleChars

# Test cases
print(categorizeArguments("123", "abc", "two", "a", "!", "123abc"))
# Output: (['123'], ['a', '!'])
# "abc, two, 123abc are not sorted in any of this lists, because they are neither a number or a string which contain just one character"
print(categorizeArguments("x", "y", "z", "99", "5.5", "1e5"))
# Output: (['99', '5.5', '1e5'], ['x', 'y', 'z'])
# "1e5 is the scientific notation for a number, so it is correctly sorted in the numerical list. However, if it appears as a random string,
# it could be mistakenly categorized as a number, even though 1e5 does not always represent a numerical value."
print(categorizeArguments("O", "0", "#", "_", "abc123", "-9368"))
# Output: (['0', '-9368'], ['O', '#', '_'])
# "abc123 is not sorted in any of this lists, because it is neither a number or a string which contain just one character"
