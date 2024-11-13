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
import os



with open("data\input_sequence.txt", "r") as file:
    file_content = file.read()

file_content_list = list(map(int, file_content.split()))


#inputSequence = [35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182, 127, 219, 299, 277, 309, 576]

def sequenceChecker(inputSequence):
    numbers_can_be_added = 25 

    for index_of_digit_to_check in range(numbers_can_be_added, len(inputSequence)):
        digit_to_check = inputSequence[index_of_digit_to_check]
        list_to_check = inputSequence[index_of_digit_to_check - numbers_can_be_added : index_of_digit_to_check]

        found_sum = False
        for i in range(len(list_to_check)):
            for j in range(i + 1, len(list_to_check)): 
                if list_to_check[i] + list_to_check[j] == digit_to_check:
                    found_sum = True
                    break
            if found_sum:
                break


        if found_sum == False:
            print("First number that cannot be expressed as the sum of 2 numbers is:", digit_to_check)
            return digit_to_check

    return None


sequenceChecker(file_content_list)



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


def bag_rules(line):
    container, contains = line.split("contain")
    container = container.replace("bags", "").strip()
    contains_list = []

    if "no other bags" not in contains:
        contains_parts = contains.split(",") #split with ,
        for part in contains_parts:
            match = re.match(r"(\d+) (.+?) bag", part.strip()) #r = regualr string, (/d+) = reads numbers (.+?) = ready characters --> will match bag type
            if match:
                count = int(match.group(1))
                bag_type = match.group(2)
                contains_list.append((bag_type, count))
    return container, contains_list


rules= {}
with open("data\input_bags.txt", "r") as file:
    input_file = file.readlines()



for line in input_file:
    container, contains = bag_rules(line)
    rules[container] = contains


def count_bags(bag_type, rules):
    total = 0
    for inner_bag, count in rules.get(bag_type, []):
        total += count * (1 + count_bags(inner_bag, rules))
    return total


result = count_bags("shiny gold", rules)
print(result)


#output :6260
