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

def create_list_from_file(path):
    with open(path, "r") as file:
        return [int(line.strip()) for line in file]
    
def check_nums(list, depth):
    for i in range(depth, len(list)):
        can_add = False
        for j in range(i-depth, i): 
            for k in list[j+1:i]:               
                if list[j] + k == list[i]:
                    can_add = True
                    break
            if can_add:                         #break out of inner two for-loops
                break
        if can_add == False:
            print(f"Number {list[i]} at index {i} can not be reached by adding two previous numbers.")
            break

check_nums(create_list_from_file("data/input_sequence.txt"), 25)

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

def create_dict_from_file(path):
    bags = {}
    with open(path, "r") as file:
        for line in file:
            words = line.split()
            bag = words[0]+words[1]
            contents = [words[i:i+3] for i in range(4, len(words), 4)]      #create list of the contents of the current bag
            bags.update({bag: contents})
    return bags
        
def count_bags(bags, current):
    count = 0
    contents = bags[current]
    if contents == [['no', 'other', 'bags.']]:
        return 0
    for i in contents:
        next_bag = i[1] + i[2]
        count += int(i[0]) + int(i[0]) * count_bags(bags, next_bag)
    return count 
            
print(count_bags(create_dict_from_file("data/input_bags.txt"), "shinygold"))
    
