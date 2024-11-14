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

with open('data/input_sequence.txt') as file:
    numbers_lst = [int(line.strip()) for line in file]

# lst = [35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182, 127, 219, 299, 277, 309, 576]
pointer = 26

while pointer < len(numbers_lst):
    target = numbers_lst[pointer]
    found = False  

    for a, b in combinations(numbers_lst[pointer - (pointer-1):pointer], 2):
        if a + b == target:
            print(f"{target} = {a} + {b}")
            found = True 
            break
    
    if found:
        pointer += 1

    else:
        print(f"{target} at index: {pointer} is not creatable with the 25 preceding terms.")
        break

else: 
    print(f"Pointer: {pointer} is out of range.")


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

with open('data/input_bags.txt') as file:
    text =file.read()

# text = """shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
#           dark olive bags contain 3 faded blue bags, 4 dotted black bags.
#           vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
#           faded blue bags contain no other bags.
#           dotted black bags contain no other bags."""

bags = {}

def check_bags():

    for line in text.splitlines():
        main_bag, sub_bag = line.split(" contain ")
        main_bag = main_bag.replace(" bags", "").replace(" bag", "").strip()
        sub_bag = sub_bag.replace(" bags", "").replace(" bag", "").replace(".", "").strip()

        if "no other" in sub_bag:
            bags[main_bag] = {}
            continue

        bags[main_bag] = {}

        for elem in sub_bag.split(", "):
            elem_value = re.findall(r'\d+', elem)
            elem_type = re.sub(r'\d+', '', elem).strip()

            if elem_value:
                bags[main_bag][elem_type] = int(elem_value[0])

    return bags

def count_bags(bag_name):
    total_count = 0

    for sub_bag, quantity in bags.get(bag_name, {}).items():
        contained_bags_count = count_bags(sub_bag)
        print(f"{quantity} {sub_bag} bags in {bag_name} contains {contained_bags_count} bags inside each.")
        total_count += quantity * (1 + contained_bags_count)

    return total_count

check_bags()

total_bags = count_bags("shiny gold")
print(f"\nThe total amount of bags in 'shiny gold' is: {total_bags}")


