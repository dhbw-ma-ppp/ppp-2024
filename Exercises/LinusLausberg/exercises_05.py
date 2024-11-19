import pathlib
import os
import itertools

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

# open file, create Iterator and puts the first 25 numbers in a list before, so they can be used in the first calculation
def preprocess(inputfile):
    before_and_goal:list[str]  = []
    for counter in range(0,26):
        number: str = inputfile.readline()
        number_ready: str = ''
        for point in number:
            if point != '\n':
                number_ready = number_ready + point
        before_and_goal.append(int(number_ready))
    return before_and_goal

def pathfindernumbers():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sequence_path = os.path.join(
    script_dir, "..", "..", "data", "input_sequence.txt")
    return sequence_path

# trys to sum up two of the Numbers in before to get the wanted Number
def checking(before_and_goal):
    goal: int = int(before_and_goal[25])
    before = before_and_goal[:-1]
    for pair in itertools.combinations(before,2):
        solution: int = sum(pair)
        if solution == goal:
            return True, 0
    return False, goal

# moves the list before one position to the right. So the first Item will be deletet and one will e attached. 
# If end of file is reached, it will return False.
def move(inputfile, before_and_goal) -> bool:
    before_and_goal.pop(0)
    number = inputfile.readline()
    if number == '':
        return False
    number_ready: str = ''
    for point in number:
        if point != '\n':
            number_ready = number_ready + point
    before_and_goal.append(int(number_ready))
    return True

# just the call of funktions
def main1():
    path = pathfindernumbers()
    with open(path,'r') as inputfile:
        ending_solution: int = 0
        before_and_goal = preprocess(inputfile)
        run: bool = True
        while run:
            run, solution = checking(before_and_goal)
            if run:
                run = move(inputfile, before_and_goal)
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

def dict_generation(dict_all, raw_row):
    bag_inventory_differentiation = raw_row.split('contain')
    bag: str = bag_inventory_differentiation[0][:-1]
    bag = bag.replace('bags', '')
    bag = bag.replace(' ', '')
    inventory:list = []
    inventory =''.join(bag_inventory_differentiation[1])
    if inventory == ' no other bags.\n':
        inventory = []
    else:
        inventory = inventory.replace('bags', '')
        inventory = inventory.replace('bag', '')
        inventory = inventory.replace(', ', '')
        inventory = inventory.split(' ')
        inventory = inventory[1:-1]
        for index in range(1, len(inventory) -1, 2):
            if index <= len(inventory) - 2:
                element = inventory[index]
                next_element = inventory[index + 1]
                element = element + next_element
                inventory.insert(inventory.index(next_element) + 1, element)
                del inventory[index:index + 2]
            else:
                break
    dict_all[bag] = inventory

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
    for counter in range(0, len(content),2):
        result += int(content[counter])
    result += counter_bags_with_bags
    return result

def pathfinderbags():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sequence_path = os.path.join(
    script_dir, "..", "..", "data", "input_bags.txt")
    return sequence_path

# main-programm
def main2():
    path = pathfinderbags()
    dict_all = {}
    with open(path,'r') as inputfileb:
        for raw_row in inputfileb:
            dict_generation(dict_all, raw_row)
    result = insert_and_counting(dict_all, 'shinygold')
    print('The shiny gold bag contains', result, 'bags.')

main2()
#Output: 6260