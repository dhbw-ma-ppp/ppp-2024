
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

import sys

sys.path.append('/Users/hannah/Desktop/Ppp/ppp-2024/Exercises/HannahGedler')

with open('/Users/hannah/Desktop/Ppp/ppp-2024/Exercises/HannahGedler/input_memory_01.txt', 'r') as file: 
            actual_input = file.read().strip()
            list_actual_input = actual_input.split(",")
            memory_dict = {index: int(wert) for index, wert in enumerate(list_actual_input)}   
            
test1 = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
result_dict = {index: value for index, value in enumerate(test1)} # dict for test1 

def get_parameter(number_dict, mode, instruction_counter, relative_offset):
     if mode == '1':
        if instruction_counter not in number_dict:
            number_dict[instruction_counter] = 0
        return number_dict[instruction_counter]
     elif mode == '0':
        if number_dict[instruction_counter] not in number_dict:
            number_dict[number_dict[instruction_counter]] = 0
        return number_dict[number_dict[instruction_counter]]
     elif mode == '2':
        if number_dict[instruction_counter] + relative_offset not in number_dict:
             number_dict[number_dict[instruction_counter]+ relative_offset] = 0
        return number_dict[number_dict[instruction_counter]+ relative_offset]
         
def find_number(test_list):
     instructionCounter = 0
     relative_offset = 0
     while True:
         opcode = str(test_list[instructionCounter])
         while len(opcode) < 5:
             opcode = "0" + opcode
         instruction = str(opcode[3:5])
         first_mode = opcode[2]
         second_mode = opcode[1]
         third_mode = opcode[0]
        # different_modes = [first_mode, second_mode]
         # opcode 1: addition
         if instruction == "01":
             firstParameter = get_parameter(test_list,first_mode, instructionCounter+1, relative_offset)
             secondParameter = get_parameter(test_list,second_mode, instructionCounter+2, relative_offset)
             result = firstParameter + secondParameter
             target = get_parameter(test_list, '1', instructionCounter+3, relative_offset) #from mode 1 because I take value of this position in line 74
             if third_mode == '2':
                target += relative_offset
             test_list[target] = result
             instructionCounter += 4
         # opcode 2: multiplication
         elif instruction == "02":
             firstParameter = get_parameter(test_list,first_mode, instructionCounter+1, relative_offset)
             secondParameter = get_parameter(test_list,second_mode, instructionCounter+2, relative_offset)
             result = firstParameter * secondParameter
             target = get_parameter(test_list, '1', instructionCounter+3, relative_offset)
             if third_mode == '2':
                target += relative_offset
             test_list[target] = result
             instructionCounter += 4
         # opcode 3: user input, no immediate mode possible
         elif instruction == "03":
             user_input = int(input("Please enter a number:"))
             save_at_position = get_parameter(test_list, '1', instructionCounter+1, relative_offset)
             if first_mode == '2':
                 save_at_position += relative_offset
             test_list[save_at_position] = user_input
             instructionCounter += 2
         # opcode 4: output
         elif instruction == "04":
             if first_mode == '1':
                 print(test_list[instructionCounter + 1])
             elif first_mode == '0':
                 print(test_list[test_list[instructionCounter + 1]])
             elif first_mode == '2':
                 print(test_list[test_list[instructionCounter + 1] + relative_offset]) 
             instructionCounter += 2
         # - 5: jump-if-true: if the first parameter is non-zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
         elif instruction == "05":
             firstParameter = get_parameter(test_list,first_mode, instructionCounter+1, relative_offset)
             secondParameter = get_parameter(test_list,second_mode, instructionCounter+2, relative_offset)
             if firstParameter != 0:
                 instructionCounter = secondParameter
             else:
                 instructionCounter += 3
         # - 6: jump-if-false: if the first parameter is zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
         elif instruction == "06":
             firstParameter = get_parameter(test_list,first_mode, instructionCounter+1, relative_offset)
             secondParameter = get_parameter(test_list,second_mode, instructionCounter+2, relative_offset)
             if firstParameter == 0:
                 instructionCounter = secondParameter
             else:
                 instructionCounter += 3
         # - 7: less than: if the first parameter is less than the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
         elif instruction == "07":
             firstParameter = get_parameter(test_list,first_mode, instructionCounter+1, relative_offset)
             secondParameter = get_parameter(test_list,second_mode, instructionCounter+2, relative_offset)
             resultIndex = get_parameter(test_list, '1', instructionCounter+3, relative_offset)
             if third_mode == '2':
                 resultIndex += relative_offset
             if firstParameter < secondParameter:
                 test_list[resultIndex] = 1
             else:
                 test_list[resultIndex] = 0
             instructionCounter += 4
         # - 8: equals: if the first parameter is equal to the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
         elif instruction == "08":
             firstParameter = get_parameter(test_list,first_mode, instructionCounter+1, relative_offset)
             secondParameter = get_parameter(test_list,second_mode, instructionCounter+2, relative_offset)
             resultIndex = get_parameter(test_list, '1', instructionCounter+3, relative_offset)
             if third_mode == '2':
                 resultIndex += relative_offset
             if firstParameter == secondParameter:
                 test_list[resultIndex] = 1
             else:
                 test_list[resultIndex] = 0
             instructionCounter += 4
         #opcode 9 adjusts the relative offset by the value of its only parameter.the offset increases by the value of the parameter (or decreases if the parameter value is negative).
         elif instruction == "09":
             firstParameter = get_parameter(test_list,first_mode, instructionCounter+1, relative_offset)
             relative_offset += firstParameter
             instructionCounter += 2
         elif instruction == "99":
             break
     print("result:", test_list[0]) # result: 1102
find_number(memory_dict)            # output: 33343