# PART 1: Find the first number that is not the sum of two of the 25 preceding numbers


def find_invalid_number(sequence, preamble_length):
    for i in range(preamble_length, len(sequence)):
        preamble = sequence[i - preamble_length:i]
        valid = any(sequence[i] == x + y for x in preamble for y in preamble)
        if not valid:
            return sequence[i]
    return None

# Read input from 'input_sequence.txt'
with open("/Users/justus/Documents/python/Uni_LAUFZEITEN/InputNumber.txt", "r") as file:
    input_sequence = [int(line.strip()) for line in file.readlines()]


result_part1 = find_invalid_number(input_sequence, 25)
print("Part 1 Result:", result_part1)


# PART 2: Calculate the total number of bags

import re
from collections import defaultdict

def parse_bag_rules(rules):
    bag_map = defaultdict(dict)
    for rule in rules:
        container, contents = rule.split(" bags contain ")
        for count, bag in re.findall(r"(\d+) ([\w\s]+) bag", contents):
            bag_map[container][bag] = int(count)
    return bag_map

def count_bags_inside(bag_map, bag_color):
    return sum(count + count * count_bags_inside(bag_map, color) for color, count in bag_map[bag_color].items())

# Read input from 'input_bags.txt'
with open("/Users/justus/Documents/python/Uni_LAUFZEITEN/InputBags.txt", "r") as file:
    input_bags = file.read().strip().split("\n")

# Parse the rules and count bags inside the 'shiny gold' bag
bag_map = parse_bag_rules(input_bags)
result_part2 = count_bags_inside(bag_map, "shiny gold")
print("Part 2 Result:", result_part2)



