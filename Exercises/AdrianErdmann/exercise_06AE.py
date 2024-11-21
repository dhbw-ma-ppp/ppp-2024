
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

# Idea -----------------------------------------------------------------------------------------------------------------------
# The idea is to allow spaces in the memory, so the memory doesn't need to be filled with 0 up to a index out of range
# Rather the memory is represented by a dictonary. The keys are the adresses and the values the values stored at the adresses.
# This allows to assume an IndexError as 0 and if a number needs to be added out of the boundaries of the inital memory len
# it just can be written to the adress without needing to fill a list with zeros up to the index the num will be written in.
# ----------------------------------------------------------------------------------------------------------------------------

max_parameter_needed = 3
offset = 0

# Opcode funcs
def addition(memory, adress, parameters, mode):
    global offset
    if mode[2] == 2:
        if memory[adress + 3] + offset < 0:
            raise ValueError
        memory[memory[adress + 3] + offset] = parameters[0] + parameters[1]
    else:
        if memory[adress + 3] < 0:
            raise ValueError
        memory[memory[adress + 3]] = parameters[0] + parameters[1]
    return adress + 4

def multiplication(memory, adress, parameters, mode):
    global offset
    if mode[2] == 2:
        if memory[adress + 3] + offset < 0:
            raise ValueError
        memory[memory[adress + 3] + offset] = parameters[0] * parameters[1]
    else:
        if memory[adress + 3] < 0:
            raise ValueError
        memory[memory[adress + 3]] = parameters[0] * parameters[1]
    return adress + 4

def userInput(memory, adress, parameters, mode):
    global offset
    while True:
        try:
            user_in = int(input("Bitte geben sie eine zahl ein: "))
            user_in = int(user_in)
            break
        except ValueError:
            print("Dies war keine Zahl.\n")
    if mode[0] == 2:
        memory[memory[adress + 1] + offset] = user_in
    else:
        memory[adress + 1] = user_in
    return adress + 2

def outPut(memory, adress, parameters, mode):
    print(f"{parameters[0]}")
    return adress + 2

def jumpIfTrue(memory, adress, parameters, mode):
    if bool(parameters[0]):
        return parameters[1]
    return adress + 3

def jumpIfFalse(memory, adress, parameters, mode):
    if not parameters[0]:
        return parameters[1]
    return adress + 3

def lessThan(memory, adress, parameters, mode):
    global offset
    if parameters[0] < parameters[1]:
        result = 1
    else:
        result = 0
    if mode[2] == 2:
        if memory[adress + 3] + offset < 0:
            raise ValueError
        memory[memory[adress + 3] + offset] = result
    else:
        if memory[adress + 3] < 0:
            raise ValueError
        memory[memory[adress + 3]] = result
    return adress + 4

def equals(memory, adress, parameters, mode):
    global offset
    if parameters[0] == parameters[1]:
        result = 1
    else:
        result = 0
    if mode[2] == 2:
        if memory[adress + 3] + offset < 0:
            raise ValueError
        memory[memory[adress + 3] + offset] = result
    else:
        if memory[adress + 3] < 0:
            raise ValueError
        memory[memory[adress + 3]] = result
    return adress + 4

def addOffset(memory, adress, parameters, mode):
    global offset
    # print(f"offset adjusted by {parameters[0]}")
    offset = offset + parameters[0]
    return adress + 2


opc_methods = {
    1: addition,
    2: multiplication,
    3: userInput,
    4: outPut,
    5: jumpIfTrue,
    6: jumpIfFalse,
    7: lessThan,
    8: equals,
    9: addOffset,
    99: lambda memory, adress, parameters, mode: adress,
}


def readMemoryFile(path):
    with open(path) as file:
        content = next(file)
        memory = [int(i) for i in (content.rstrip().split(","))]
    return memory

def memoryToUsableDict(memory):
    usable_memory = {}
    for i in range(len(memory)):
        usable_memory[i] = memory[i]
    return usable_memory

def splitOpcode(value):
    opcode = value % 100
    mode = []
    for i in range(max_parameter_needed):
        mode.append(value // (10 ** (i + 2)) % 10)
    return opcode, mode

def parameterWithMode(memory, working_adress, mode, mode_index):
    parameter_adress = working_adress + mode_index + 1
    this_mode = mode[mode_index]
    global offset
    try:
        match this_mode:
            case 0:
                return memory[memory[parameter_adress]]
            case 1:
                return memory[parameter_adress]
            case 2:
                key = memory[parameter_adress] + offset
                return memory[key]
            case _: # any unspecified should be considered as mode 0
                return memory[memory[parameter_adress]]
    except KeyError:
        if parameter_adress < 0:
            raise ValueError
        return 0

def compute(memory):
    global offset
    memory = memoryToUsableDict(memory)
    offset = 0
    working_adress = 0
    opc, mode = splitOpcode(memory[working_adress])
    while opc != 99:
        parameters = [parameterWithMode(memory, working_adress, mode, i) for i in range(max_parameter_needed)]
        working_adress = opc_methods[opc](memory, working_adress, parameters, mode)
        try: opc, mode = splitOpcode(memory[working_adress])
        except IndexError: opc, mode = splitOpcode(0)
    return memory[0]


memory_ = readMemoryFile("./data/input_memory_01.txt")
test_list1 = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
test_list2 = [3,9,8,9,10,9,4,9,99,-1,8]
#print(memoryToUsable(test_list))
print(compute(memory_))
