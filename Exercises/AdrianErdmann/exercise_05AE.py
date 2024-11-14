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


# old attempt with coroutine function -> too complex
# def buildable(numbers_build: set[int], to_test: int):
#     for number in numbers_build:
#         needed_to_build = to_test - number
#         if needed_to_build in (numbers_build - {number}):
#             return True
#     return False

# def coroutineIsBuildable(first_25_Numbers: list[int]):
#     last_25_numbers = first_25_Numbers
#     next_number = yield None
#     while True:
#         next_number = yield buildable(set(last_25_numbers), next_number)
#         last_25_numbers.append(next_number)
#         last_25_numbers.pop(0)
    
# number_not_buildable = 0

# with open("./data/input_sequence.txt") as content_iterator:
#     first_25_numbers = []
#     for i in range(0, 25):
#         first_25_numbers.append(int(next(content_iterator).rstrip()))
#     is_buildable = coroutineIsBuildable(first_25_numbers)
#     next(is_buildable)
#     for number in content_iterator:
#         number = int(number.rstrip())
#         if not is_buildable.send(number):
#             number_not_buildable = number
#             break

# print(number_not_buildable)

# better attempt with a much cleaner function
def isBuildable(numbers_build: set[int], to_test: int):
    for number in numbers_build:
        needed_to_build = to_test - number
        if needed_to_build in (numbers_build - {number}):
            return True
    return False

def getFirstNotBuildable(iterator, numbers_before_count):
    numbers_before = []
    for i in range(0, numbers_before_count):
        numbers_before.append(int(next(iterator).rstrip()))
    
    index = numbers_before_count
    while True:
        try:
            number_now = int(next(iterator).rstrip())
        except StopIteration:
            break
        if not isBuildable(set(numbers_before), number_now):
            return number_now, index
        numbers_before.pop(0)
        numbers_before.append(number_now)
        index += 1

path_sequence = "./data/input_sequence.txt"
check_umbers_before = 25
with open(path_sequence) as content_iterator:
    first_not_buildable = getFirstNotBuildable(content_iterator, check_umbers_before)
    print(f"first number that is not buildable and their index: {first_not_buildable}")
    # the first number not fulfilling the criteria is 1639024365
    # it's in the line 654 of the given input-file

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

def getBagDict(path):
    bag_dict = {}
    with open(path) as content_iterator:
        for content in content_iterator:
            bag_content = []
            if not "contain no other bags." in content:
                content = content.replace(".\n", "").replace("bags", "bag")
                bag, bag_contains = content.split(" contain ")
                bag_contains = bag_contains.split(", ")
                bag_content = []
                for arg in bag_contains:
                    arg = arg.split(maxsplit=1)
                    bag_content.append((int(arg[0]), arg[1]))
            bag_dict[bag] = tuple(bag_content)
    return bag_dict

def countBags(bag_name, bag_data):
    if not bag_name in bag_data or bag_data[bag_name] == ():
        return 0
    sum = 0
    for count, bag in bag_data[bag_name]:
        sum += count * (1 + countBags(bag, bag_data))
    return sum

path_bags = "./data/input_bags.txt"
bag_data = getBagDict(path_bags)
bag_count = countBags("shiny gold bag", bag_data)
print(f"Number of bags in the shiny gold bag: {bag_count}")
# there are 6260 bags inside the "shiny gold bag"
