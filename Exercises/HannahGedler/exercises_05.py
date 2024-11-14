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

import sys
sys.path.append('/Users/hannah/Desktop/Ppp/ppp-2024/Exercises/HannahGedler')


test_list2 = [35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182, 127, 219, 299, 277, 309, 576]

with open('/Users/hannah/Desktop/Ppp/ppp-2024/Exercises/HannahGedler/input_sequence.txt', 'r') as file:
            actual_input = [zeile.strip() for zeile in file.readlines()]
            

def test_for_wrong_numbers(list_of_all_numbers):
    consider_last_numbers = 25
    currentNumber = 25
    find_wrong_numbers = 1
    list_of_wrong_numbers = []

    while len(list_of_wrong_numbers) < find_wrong_numbers:
        compare_with = int(list_of_all_numbers[currentNumber])
        if not is_wrong_number(list_of_all_numbers,currentNumber, consider_last_numbers, compare_with):
            list_of_wrong_numbers.append(compare_with)
        currentNumber += 1
    print("first number which can not be expressed as a sum of two numbers out of the 25 numbers before it:",list_of_wrong_numbers[0])
    

def is_wrong_number(list_of_all_numbers, currentNumber, considerLastNumbers, compare_with):
    for summand_index1 in range(currentNumber-considerLastNumbers, currentNumber):
        for summand_index2 in range(currentNumber-considerLastNumbers, currentNumber):
            if(summand_index1 == summand_index2): continue

            summand1 = int(list_of_all_numbers[summand_index1])
            summand2 = int(list_of_all_numbers[summand_index2])
            if summand1 + summand2 == compare_with:
                return True
    return False
    
test_for_wrong_numbers(actual_input)
            

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


from dataclasses import dataclass

@dataclass
class ContentItem:
    name: str
    count: int

@dataclass
class Bag:
    name: str

    content: list[ContentItem]

def get_bag_by_name(bag_list, bag_name):
    for bag in bag_list:
        if bag.name == bag_name:
            return bag

def init_bag_list():
    every_bag_list = []
    with open('/Users/hannah/Desktop/Ppp/ppp-2024/Exercises/HannahGedler/input_bags.txt', 'r') as file2:
        for line in file2:
            every_word = line.split()
            bag_name = ' '.join(every_word[0:3]).replace("bags", "bag").replace(",", "")
            contains_number_of_bags = int(len(every_word[4:]) / 4)
            bag_content = []
            for number in range(contains_number_of_bags):
                count = int(every_word[number * 4 + 4])
                start_index = number * 4 + 4 + 1
                end_index = number * 4 + 4*2
                bag_content_item_name = ' '.join(every_word[start_index:end_index]).replace("bags", "bag").replace(",", "").replace(".","")
                bag_content.append(ContentItem(bag_content_item_name, count))

            every_bag_list.append(Bag(bag_name, bag_content))
    return every_bag_list


def count_bags(every_bag_list, bag):
    total = 0

    for inner_bag in bag.content:
        total += (inner_bag.count * count_bags(every_bag_list, get_bag_by_name(every_bag_list, inner_bag.name)))+ inner_bag.count

    return total

every_bag_list = init_bag_list()
total = count_bags(every_bag_list, get_bag_by_name(every_bag_list, "shiny gold bag"))
print("count of bags in the single shiny gold bag:",total)
