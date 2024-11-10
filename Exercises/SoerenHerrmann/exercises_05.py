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
import itertools
import pathlib

from colorama import Fore
import os

# shift of positions to look for values
SHIFT = 25
# path to the number sequence
script_dir = os.path.dirname(os.path.abspath(__file__))
sequence_path = os.path.join(
    script_dir, "..", "..", "data", "input_sequence.txt"
)
colors = [
    Fore.RED, Fore.GREEN, Fore.YELLOW, 
    Fore.BLUE, Fore.MAGENTA, Fore.CYAN
]
color_cycle = itertools.cycle(colors) 


def set_next_color():
    color = next(color_cycle)
    print(color, end='') 


def read_input_sequence(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
        # convert lines into integers
        lines = [int(line.strip()) for line in lines] 
        return lines


def find_sums(lines):
    for i in range(len(lines) - SHIFT):
        found_sum = False
        elem = lines[i + SHIFT]
        set_next_color()
        print(f'Looking for sum for number {elem}')
        
        summands = lines[i:i + SHIFT]
        summands_set = set(summands)
        set_next_color()
        print(summands)

        for number in summands:
            target = elem - number

            if target in summands_set and target != number:
                set_next_color()
                print(f'Sum of {elem} is {number} + {target}')
                found_sum = True
                break

        if not found_sum:
            set_next_color()
            print(f'No working sum found at index {i + SHIFT}')
            break


lines = read_input_sequence(sequence_path)
# found not working sum at index 653 
find_sums(lines)

# --- Bags ---
bag_path = os.path.join(
    script_dir, "..", "..", "data", "input_bags.txt"
)

class Bag():
    def __init__(self, type:str):
        self.type = type
        self.inventory = {}

    def add_content(self, bag_type:str, quantity:int):
        self.inventory[bag_type] =quantity

    def __repr__(self):
        return f'Bag({self.type}, contains={self.inventory})'

def parse_bag_line(line):
    words = line.split()

    main_bag_name = ' '.join(words[:3])
    main_bag = Bag(main_bag_name)
    if "no other bags" in line:
        return main_bag

    contents_part = ' '.join(words[4:])
    items = contents_part.split(', ')

    for item in items:
        item_parts = item.split()
        quantity = int(item_parts[0])
        bag_type = ' '.join(item_parts[1:3]) + " bags"

        main_bag.add_content(bag_type, quantity)

    return main_bag


def read_bags(path:pathlib.Path):
    with open(path, "r") as f:
        lines = f.readlines()
        bags = {}
        for line in lines:
            bag = parse_bag_line(line)
            bags[bag.type] = bag
        f.close()

    return bags

# each line contains a seperate bag statement
sequence_bags = read_bags(bag_path)

def count_bag(bag):
    if type(bag) is str:
        bag = sequence_bags[bag]

    if bag.inventory == {}:
            return 1


    count = 1
    for sub_bag in bag.inventory.keys():
        count += count_bag(sub_bag)

    return count

bag_count = 0
for bag in sequence_bags:
    bag_count += count_bag(bag)

set_next_color()
print(f'There are exactly {bag_count} bags in the file')