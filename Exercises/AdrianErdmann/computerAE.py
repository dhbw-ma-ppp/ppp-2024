# Represents my int-cumputer programmed in exercise 06; this how it would have been implemented
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

def splitOpcode(value, max_parameters_needed):
    opcode = value % 100
    mode = []
    for i in range(max_parameters_needed):
        mode.append(value // (10 ** (i + 2)) % 10)
    return opcode, mode

def parameterWithMode(memory, working_adress, offset, mode, mode_index):
    parameter_adress = working_adress + mode_index + 1
    this_mode = mode[mode_index]
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
        self.next_triplet = []
        opc, mode = splitOpcode(self.memory[self.working_adress], self.max_parameters_needed)
        while opc != 99:
            if len(self.next_triplet) >= 3: break
            parameters = [parameterWithMode(self.memory, self.working_adress, self.offset, mode, i) for i in range(self.max_parameters_needed)]
            self.working_adress = self.opc_methods[opc](self, parameters, mode)
            try: opc, mode = splitOpcode(self.memory[self.working_adress], self.max_parameters_needed)
            except IndexError: opc, mode = splitOpcode(0)
        else: return [-1, 0, self.memory[0]]
        return self.next_triplet

    def addition(self, parameters, mode):
        if mode[2] == 2:
            if self.memory[self.working_adress + 3] + self.offset < 0:
                raise ValueError
            self.memory[self.memory[self.working_adress + 3] + self.offset] = parameters[0] + parameters[1]
        else:
            if self.memory[self.working_adress + 3] < 0:
                raise ValueError
            self.memory[self.memory[self.working_adress + 3]] = parameters[0] + parameters[1]
        return self.working_adress + 4

    def multiplication(self, parameters, mode):
        if mode[2] == 2:
            if self.memory[self.working_adress + 3] + self.offset < 0:
                raise ValueError
            self.memory[self.memory[self.working_adress + 3] + self.offset] = parameters[0] * parameters[1]
        else:
            if self.memory[self.working_adress + 3] < 0:
                raise ValueError
            self.memory[self.memory[self.working_adress + 3]] = parameters[0] * parameters[1]
        return self.working_adress + 4

    def userInput(self, parameters, mode):
        while True:
            try:
                user_in = int(input("Bitte geben sie eine zahl ein: "))
                user_in = int(user_in)
                break
            except ValueError:
                print("Dies war keine Zahl.\n")
        if mode[0] == 2:
            self.memory[self.memory[self.working_adress + 1] + self.offset] = user_in
        else:
            self.memory[self.working_adress + 1] = user_in
        return self.working_adress + 2

    def outPut(self, parameters, mode):
        self.next_triplet.append(parameters[0])
        return self.working_adress + 2

    def jumpIfTrue(self, parameters, mode):
        if bool(parameters[0]):
            return parameters[1]
        return self.working_adress + 3

    def jumpIfFalse(self, parameters, mode):
        if not parameters[0]:
            return parameters[1]
        return self.working_adress + 3

    def lessThan(self, parameters, mode):
        if parameters[0] < parameters[1]:
            result = 1
        else:
            result = 0
        if mode[2] == 2:
            if self.memory[self.working_adress + 3] + self.offset < 0:
                raise ValueError
            self.memory[self.memory[self.working_adress + 3] + self.offset] = result
        else:
            if self.memory[self.working_adress + 3] < 0:
                raise ValueError
            self.memory[self.memory[self.working_adress + 3]] = result
        return self.working_adress + 4

    def equals(self, parameters, mode):
        if parameters[0] == parameters[1]:
            result = 1
        else:
            result = 0
        if mode[2] == 2:
            if self.memory[self.working_adress + 3] + self.offset < 0:
                raise ValueError
            self.memory[self.memory[self.working_adress + 3] + self.offset] = result
        else:
            if self.memory[self.working_adress + 3] < 0:
                raise ValueError
            self.memory[self.memory[self.working_adress + 3]] = result
        return self.working_adress + 4

    def addOffset(self, parameters, mode):
        self.offset = self.offset + parameters[0]
        return self.working_adress + 2

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
        99: lambda self: self.working_adress,
    }
