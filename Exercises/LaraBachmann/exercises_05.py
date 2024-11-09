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

from itertools import combinations

# PART 1: Find the first invalid number in the sequence
def read_numbers_from_file(filepath: str) -> list[int]:
    with open(filepath, 'r') as file:
        numbers = [int(line.strip()) for line in file]
    return numbers

def find_first_invalid_number(numbers: list[int], sequence_of_numbers: int):
    start_index = 0
    pointer = sequence_of_numbers

    for number in numbers[pointer:]:
        sequence = numbers[start_index:pointer]
        found = False

        for pair in combinations(sequence, 2):
            if sum(pair) == numbers[pointer]:
                found = True
                break

        if not found:
            print(f'First invalid number: {numbers[pointer]}')
            return numbers[pointer]
        
        start_index += 1
        pointer += 1
    
    print('There is no invalid number in the given list!')
    return None

# Example usage for Part 1
lst = [35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182, 127, 219, 299, 277, 309, 576]
find_first_invalid_number(lst, 5) # First invalid number: 127

# ACTUAL input
numbers = read_numbers_from_file('data/input_sequence.txt')
find_first_invalid_number(numbers, 25) # First invalid number: 1639024365

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

import re

# PART 2: Calculate the total number of bags within a 'shiny gold' bag
def read_bags_from_file(filepath: str) -> dict[str, dict[str, int]]:
    bags = {}

    with open(filepath, 'r') as file:
        for line in file:
            main_bag, contained_bags = line.split(" contain ")
            main_bag = main_bag.replace(" bags", "").replace(" bag", "").strip()

            if "no other bags" in contained_bags:
                bags[main_bag] = {}
                continue

            inner_bags = {}
            for bag in contained_bags.split(", "):
                match = re.match(r"(\d+) (.+?) bags?", bag)
                if match:
                    count = int(match.group(1))
                    bag_type = match.group(2)
                    inner_bags[bag_type] = count

            bags[main_bag] = inner_bags

    return bags 

def count_bags(bags, bag_type):
    total_count = 0

    for inner_bag, count in bags.get(bag_type, {}).items():
        total_count += count * (1 + count_bags(bags, inner_bag))

    return total_count

# Read the rules defining which bags are inside other bags and calculate for 'shiny gold'
bags = read_bags_from_file('data/input_bags.txt')
result = count_bags(bags, 'shiny gold')
print(f'Total bags inside "shiny gold" bag: {result}') # bags inside 'shiny gold' bag: 6260