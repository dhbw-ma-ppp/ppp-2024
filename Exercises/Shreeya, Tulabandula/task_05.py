# PART 1:
# Here's a sequence of numbers:
#list = [35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182, 127, 219, 299, 277, 309, 576]
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


def read_numbers_file(input_sequence):
    with open(input_sequence, 'r') as file:
        numbers = [int(line.strip()) for line in file]
    return numbers

def find_exception(numbers, size):
    for i in range(size, len(numbers)):
        target = numbers[i]
        previous_numbers = numbers[i - size : i]

        found = False 
        for j in range(size):
            for k in range(j + 1, size):
                if previous_numbers[j] + previous_numbers[k] == target:
                    found = True
                    break
            if found:
                break
        if not found:
            print(f'This value has no match: {target}')
            return target

input_sequence = 'data/input_sequence.txt'
numbers = read_numbers_file(input_sequence)

find_exception(numbers, 25)
# this value has no match: 1639024365

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
from collections import defaultdict

def read_bag_rules(file_bags):
    rules = defaultdict(list)
    with open(file_bags, 'r') as file:
        for line in file:
            parent_bag, contained_bags = line.split(" bags contain ")
            if "no other bags" in contained_bags:
                continue
            for count, child_bag in re.findall(r"(\d+) (\w+ \w+) bag", contained_bags):
                rules[parent_bag].append((int(count), child_bag))
    return rules

def count_bags_inside(bag_rules, bag_color):
    total = 0
    for count, inner_bag in bag_rules[bag_color]:
        total += count + count * count_bags_inside(bag_rules, inner_bag)
    return total

file_path = 'data/input_bags.txt'
bag_rules = read_bag_rules(file_path)

target = 'shiny gold'
total_bags_inside = count_bags_inside(bag_rules, target)

print(f"Total bags inside a single '{target}' bag: {total_bags_inside}")
# Total bags inside a single 'shiny gold' bag: 6260
