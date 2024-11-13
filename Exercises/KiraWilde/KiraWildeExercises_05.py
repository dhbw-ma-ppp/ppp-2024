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

def find_invalid_number_in_sequence(sequence, compare_lenght):
    for i in range(compare_lenght,len(sequence)):
        preceding_elements = sequence[i - compare_lenght:i]
        current_number = sequence[i]
        '''
        #if not any(current_number == preceding_elements[x] + preceding_elements[y] for x in range(compare_lenght) for y in range (x + 1, compare_lenght)):
        #    return current_number
        #
        # This was my first solution, but it is difficult to read, so here is a more understandable version:
        '''
        is_sum_found = False
        for x in range(compare_lenght):
            for y in range(x + 1, compare_lenght):
                if (current_number == preceding_elements[x] + preceding_elements[y]):
                    is_sum_found = True
                    break
            if is_sum_found:
                break
        if not is_sum_found:
            return current_number
    return None
  
with open("data/input_sequence.txt", "r") as file:
    sequence = [int(line.strip()) for line in file.readlines()]

sequence_test = [35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182, 127, 219, 299, 277, 309, 576]
lenght = 25
invalid_number_in_sequence = find_invalid_number_in_sequence(sequence, lenght)
print(f"the first invalid number is: {invalid_number_in_sequence}")
# result: 1639024365

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

def parse_input(filename):
    rules = {}
    with open(filename, "r") as file:
        for line in file:
            parts = line.strip().split(" contain ")
            outer_bag = parts[0].split(" bag")[0]
            inner_bags = parts[1].split(", ")
            contents = []
            for bag in inner_bags:
                if bag == "no other bags.":
                    continue
                number, color = bag.split(" ", 1)
                contents.append((int(number), color.rsplit(" ", 1)[0]))
            rules[outer_bag] = contents
    #print("Parsed rules:", rules)
    return rules

def count_bags(rules, bag):
    total = 0
    for count, inner_bag in rules.get(bag, []):
        total += count + count * count_bags(rules, inner_bag)
    return total

def solve(filename):
    rules = parse_input(filename)
    #print("Final rules:", rules.keys())
    return count_bags(rules, "shiny gold")

# Example usage
print(solve("data/input_bags.txt"))
#result 6260
