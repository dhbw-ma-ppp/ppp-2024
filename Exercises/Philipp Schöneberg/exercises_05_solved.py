import itertools
import re

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


class CheckSumIterator0:
    def __iter__(self):
        lst: list[int] = [
            35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102,
            117, 150, 182, 127, 219, 299, 277, 309, 576
            ]
        while lst:
            yield lst.pop(0)


class CheckSumIterator1:
    def __iter__(self):
        with open("input_sequence.txt", "r") as f:
            for line in f:
                yield int(line.strip())


def check_sum(my_iterator, amount_preceding_numbers: int) -> int | None:
    """
    This function takes an iterator and an amount in form of an integer as
    input and computes whether each number in the iterator can be expressed as
    the sum of two of the given amount of numbers before it.
    """
    def add_to_preceding_numbers(elem: int) -> None:
        """
        This function expects one parameter, called the element. The function
        then checks if the given element is already used in the
        preceding_numbers dictionary. If so, the function increments the value
        stored in the dictionary on the key corresponding to the element.
        Otherwise, it creates a new key corresponding to the element and
        assigns the value one to it.
        """
        if elem in preceding_numbers:
            preceding_numbers[elem] += 1
        else:
            preceding_numbers[elem] = 1

    def delete_from_preceding_numbers() -> None:
        """
        This function expects one parameter, which will be referred to as the
        element. The function then checks whether the value stored in the
        dictionary on the key corresponding to the element is greater than one.
        If so, it decrements the value by one. Otherwise it deletes the entry.
        """
        if preceding_numbers[number_window[0]] > 1:
            preceding_numbers[number_window[0]] -= 1
        else:
            del preceding_numbers[number_window[0]]

    def check_summand(result: int, summand: int) -> bool:
        """
        This function has two inputs. First, it takes an integer representing
        the number to be derived by the current addition. The second parameter
        is an integer representing the summand of the previous successful
        addition. The function then checks whether the result can be derived
        by simply multiplying the summand by two. If this is not the case, it
        returns true and validates the summand. However, if it is possible to
        simply double the summand, it validates whether there are actually two
        of the summands in the last few numbers considered. If so, it returns
        true, otherwise false.
        """
        if 2*summand == result:
            if preceding_numbers[summand] > 1:
                return True
            else:
                return False
        else:
            return True

    number_window: list[int] = []
    preceding_numbers: dict[int, int] = {}

    for elem in itertools.islice(my_iterator, 0, amount_preceding_numbers):
        number_window.append(elem)
        add_to_preceding_numbers(elem)

    for elem in itertools.islice(my_iterator, amount_preceding_numbers, None):
        for j in preceding_numbers.items():
            if elem-j[0] in preceding_numbers and check_summand(elem, j[0]):
                delete_from_preceding_numbers()
                number_window.pop(0)
                number_window.append(elem)
                add_to_preceding_numbers(elem)
                break
        else:
            return elem
    return None


def test_check_sum() -> None:
    """
    This function tests the check_sum function with an assert statement.
    """
    assert 127 == check_sum(CheckSumIterator0(), 5)
    print("The test of the test_check_sum function was successful!")


test_check_sum()

print(check_sum(CheckSumIterator1(), 25))


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

class BagIterator0:
    def __iter__(self):
        lst: list[str] = [
            "shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.",
            "dark olive bags contain 3 faded blue bags, 4 dotted black bags.",
            "vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.",
            "faded blue bags contain no other bags.",
            "dotted black bags contain no other bags."
        ]
        while lst:
            yield lst.pop(0)


class BagIterator1:
    def __iter__(self):
        with open("input_bags.txt", "r") as f:
            for line in f:
                yield line.strip()


def count_bags(my_iterator) -> int:
    """
    This function expects an iterator that returns strings. These should
    contain a bag name, then the word contain and then the amounts and names
    of the bags inside. Each should be separated by a comma. The function will
    then calculate and return the total amount of bags in a single shiny gold
    bag.
    """
    def bag_search(bag: str) -> None:
        """
        This function takes as input a string describing a bag. It then splits
        the bags in the given bag into a list. It calculates the quantity of
        each bag and calls itself again with each bag as many times as the
        quantity suggests.
        """
        nonlocal bag_counter
        if bag in bags:
            new_bags: list[str] = re.split(r',', bags[bag])
            for elem in new_bags:
                anzahl: int = re.findall(r'\d+', elem)
                if anzahl:
                    anzahl = int(anzahl[0])
                    elem = re.findall(r'[a-zA-Z]+', elem)
                    elem = elem[0]
                    for i in range(anzahl):
                        bag_counter += 1
                        bag_search(elem)

    bags: dict[str, str] = {}
    bag_counter: int = 0
    for line in my_iterator:
        line = line.replace(" ", "")
        line = line.replace(".", "")
        line = line.replace("bags", "")
        line = line.replace("bag", "")
        line_lst = re.split(r'contain', line)
        bags[line_lst[0]] = line_lst[1]
    bag_search("shinygold")
    return bag_counter


def test_count_bags() -> None:
    """
    This function tests the count_bags function with an assert statement.
    """
    assert count_bags(BagIterator0()) == 32
    print("The test of the test_count_bags function was successful!")


test_count_bags()

print(count_bags(BagIterator1()))
