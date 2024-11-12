# PART 1:
# Here's a sequence of numbers:
# [35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182, 127, 219, 299, 277, 309, 576]
# numbers in this list can in general be expressed as a sum of some pair of two numbers
# in the five numbers preceding them.
# For example, the sixth number (40) cam be expressed as 25 + 15
# the seventh number (62) can be expressed as 47 + 15 etc.
# 
# The only exception to this rule for this example is the number 127.
# The five preceding numbers are [95, 102, 117, 150, 182], and no possible sum of two of those
# numbers adds to 127.
#
# You can find the ACTUAL input for this exercise under `data/input_sequence.txt`. For this
# real input you should consider not only the 5 numbers, but the 25 numbers preceding.
# Find the first number in this list which can not be expressed as a
# sum of two numbers out of the 25 numbers before it.
# Please make not of your result in the PR.


class ElementsOfDocumentIterator:
    def __init__(self, inputfile):
        self.inputfile = inputfile

    def __iter__(self):
        return self
    
    def __next__(self):
        return self.inputfile.readline()

# open file, create Iterator and puts the first 25 numbers in a list before, so they can be used in the first calculation
def preprocess():
    inputfile = open(r'C:\Users\linus\Documents\GitHub\ppp-2024\data\input_sequence.txt','r')
    Elements = iter(ElementsOfDocumentIterator(inputfile))
    before:list[str]  = []
    for counter in range(0,26):
        number: str = next(Elements, inputfile)
        number_ready: str = ''
        for point in number:
            if point != '\n':
                number_ready = number_ready + point
        before.append(number_ready)
    return Elements, inputfile, before

# trys to sum up two of the Numbers in before to get the wanted Number
def checking(before):
    goal: int = int(before[25])
    for counter1 in range(0, 25):
        for counter2 in range(counter1+1, 25):
            solution: int = int(before[counter1]) + int(before[counter2])
            if solution == goal:
                return True, 0
    return False, goal

# moves the list before one position to the right. So the first Item will be deletet and one will e attached. 
# If end of file is reached, it will return False.
def move(Elements, inputfile, before) -> bool:
    before.pop(0)
    number = next(Elements, inputfile)
    if type(number) == ElementsOfDocumentIterator:
        return False
    number_ready: str = ''
    for point in number:
        if point != '\n':
            number_ready = number_ready + point
    before.append(number_ready)
    return True

# just the call of funktions
def main1():
    ending_solution: int = 0
    inputfile, Elements, before = preprocess()
    run: bool = True
    while run:
        run, solution = checking(before)
        if run:
            run = move(Elements, inputfile, before)
    ending_solution = solution
    print(ending_solution,'ist die erste Zahl, welche nicht mehr durch zwei Zahlen'
          ', 25 Stellen voher, berechnert werden kann.')
    

main1()
#Output:1639024365



# PART 2:
# The input to this exercise specifies rules for bags containing other bags.
# It is of the following form:
#
# shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
# dark olive bags contain 3 faded blue bags, 4 dotted black bags.
# vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
# faded blue bags contain no other bags.
# dotted black bags contain no other bags.
#
# You have a single 'shiny gold bag'. Consider the rules above. According
# to those rules your bag contains
# - 1 dark olive bag, in turn containing
#   - 3 faded blue bags (no further content)
#   - 4 dotted black bags (no further content
# - 2 vibrant plum bags, in turn containing
#   - 5 faded blue bags (no further content)
#   - 6 dotted black bags (no further content)
# 
# therefore, your single shiny gold bag contains a total of 32 bags
# (1 dark olive bag, containing 7 other bags, and 2 vibrant plum bags,
# each of which contains 11 bags, so 1 + 1*7 + 2 + 2*11 = 32)
#
# The ACTUAL input to your puzzle is given in `data/input_bags.txt`, and much larger
# and much more deeply nested than the example above. 
# For the actual inputs, how many bags are inside your single shiny gold bag?
# As usual, please list the answer as part of the PR.



class BagsInDocumentIterator:
    def __init__(self, inputfileb):
        self.inputfileb = inputfileb

    def __iter__(self):
        return self
    
    def __next__(self):
        return self.inputfileb.readline()
    

# reads every line from the file and fills the dict, with every bag as key and his content as value
def dict_generation(Iterator, dict_all):
    raw_row = next(Iterator)
    str_before_contain: str = ''
    lst_after_contain:list = [] 
    temp_word: str = ''
    temp_lst: str = ''
    temp_sentens: str = ''
    contain: bool = False
    for place in raw_row:
        if contain == False:
            if place == ' ':
                if temp_word == 'bag' or temp_word == 'bags' :
                    temp_word = ''
                elif temp_word == 'contain':
                    str_before_contain = temp_lst
                    temp_word = ''
                    contain = True
                    temp_lst = []
                else:
                    temp_lst = temp_lst + temp_word
                    temp_word = ''
            else:
                temp_word = temp_word + place 
        else:
            if place == ' ' or place == '.' or place == ',':
                if temp_word == 'bag' or temp_word == 'bags' :
                    temp_word = ''
                else:
                    temp_sentens = temp_sentens + temp_word
                    temp_word = ''
                    pass
            else:
                try:
                    int(place)
                    lst_after_contain.append(temp_sentens)
                    temp_word = ''
                    temp_sentens = ''
                    lst_after_contain.append(place)
                except ValueError:
                    temp_word = temp_word + place
    lst_after_contain.append(temp_sentens)
    lst_after_contain.pop(0)                
    dict_all[str(str_before_contain)] = lst_after_contain

# exchange every bag, which is in the shiny gold bag with his content. 
# Runs till all bags have no bags in them and return sum of bags in the shiny gold bag
def insert_and_counting(dict_all, search) -> int:
    end: bool = False
    content = dict_all[search]
    counter_bags_with_bags = 0
    counter = 1
    while counter < len(content):
        new_search = content[counter]
        multipler = content[counter-1]
        new_content = dict_all[new_search]
        if new_content == []:
            counter += 2
        else:
            counter_bags_with_bags += int(multipler)
            content.pop(counter-1)
            content.pop(counter-1)
            for element in new_content:
                try:
                    int(element)
                    element = str(int(element) * int(multipler))
                    content.append(element)
                except ValueError:
                    content.append(element)
            dict_all.update({search:content})
    counter: int = 0
    result: int = 0
    while counter < len(content):
        result += int(content[counter])
        counter += 2
    result += counter_bags_with_bags
    return result

# main-programm
def main2():
    dict_all = {}
    inputfileb = open(r'C:\Users\linus\Documents\GitHub\ppp-2024\data\input_bags.txt','r')  
    Iterator = iter(BagsInDocumentIterator(inputfileb))
    for x in range(0,594):
        dict_generation(Iterator, dict_all)
    result = insert_and_counting(dict_all, 'shinygold')
    print('The shiny gold bag contains', result, 'bags')


main2()
#Output: 6260