import itertools

# PART 1:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
# The deck of cards should behave like a sequence.
# When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above
# I should be able to index into the deck to retrieve one card.
# I should be able to iterate over all cards in the deck.
# Printing a cards string representation should give me a nice, 
# readable description of that card.


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return (f"The {self.rank} of {self.suit}")


class FrenchDeckOfCards:
    suits = ["diamonds", "hearts", "spades", "clubs"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    def __init__(self):
        # print(list(itertools.product(self.suits, self.ranks)))
        self.cards = list(Card(i[0], i[1]) for i in list(itertools.product(self.suits, self.ranks)))

    def __iter__(self):
        return (elem for elem in self.cards)

    def __getitem__(self, index):
        return self.cards[index]

    def __str__(self):
        string_representation = ""
        for elem in self:
            string_representation += str(elem) + ", "
        string_representation = string_representation[0: -2]
        return string_representation


# PART 2:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.


class SkatDeckOfCards(FrenchDeckOfCards):
    ranks = ["7", "8", "9", "10", "J", "Q", "K", "A"]


# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)


def test_FrenchDeckOfCards():
    french_deck = FrenchDeckOfCards()
    assert str(french_deck[0]) == 'The 2 of diamonds'
    assert str(french_deck[13]) == 'The 2 of hearts'
    assert str(french_deck[26]) == 'The 2 of spades'
    assert str(french_deck[39]) == 'The 2 of clubs'
    # print(french_deck)
    print("The test of the class FrenchDeckOfCards was succesful!")


def test_SkatDeckOfCards():
    skat_deck = SkatDeckOfCards()
    assert str(skat_deck[0]) == 'The 7 of diamonds'
    assert str(skat_deck[8]) == 'The 7 of hearts'
    assert str(skat_deck[16]) == 'The 7 of spades'
    assert str(skat_deck[24]) == 'The 7 of clubs'
    # print(skat_deck)
    print("The test of the class SkatDeckOfCards was succesful!")


test_FrenchDeckOfCards()
test_SkatDeckOfCards()


# PART 3:
# write a function that accepts two numbers, a lower bound and an upper bound.
# the function should then return the count of all numbers that meet certain criteria:
# - they are within the (left-inclusive and right-exclusive) bounds passed to the function
# - there is at least one group of exactly two adjacent digits within the number which are the same (like 33 in 123345)
# - digits only increase going from left to right
#
# Examples:
# - 123345 is a valid number
# - 123341 is not a valid number, as the digits do not increase from left to right
# - 123334 is not a valid number as there is no group of exactly two repeated digits
# - 111334 is a valid number. while there are three 1s, there is also a group of exactly two 3s.
# - 112233 is a valid number. At least one group of two is fulfilled, there is no maximum to the number of such groups.
#
# run your function with the lower bound `134564` and the upper bound `585159`. Note the resulting count
# in your pull request, please.

def number_acceptor(lower_bound, upper_bound):
    """
    This function takes a lower and upper bound as parametersd and returns
    every number which fullfills the following criteria:

    - they are within the (left-inclusive and right-exclusive) bounds passed
    to the function
    - there is at least one group of exactly two adjacent digits within the
    number which are the same
    - digits only increase going from left to right
    """
    def is_monotonic_digits():
        """
        Checks whether a number contains a group of exactly two adjacent
        digits.
        """
        nonlocal testing_number
        nonlocal testing_number_string
        nonlocal connected_equal_chars_counter
        for i in range(len(testing_number_string)-1):
            if (connected_equal_chars_counter == 2 and testing_number_string[i] != testing_number_string[i+1]) or (connected_equal_chars_counter == 1 and i == len(testing_number_string)-2 and testing_number_string[i] == testing_number_string[i+1]):
                accepted_numbers.append(testing_number)
                break
            elif testing_number_string[i] == testing_number_string[i+1]:
                connected_equal_chars_counter += 1
            else:
                connected_equal_chars_counter = 1

    def calculate_next_testing_number():
        """
        This function calculates the next number to be checked by the function.
        It ensures that no digit is greater than any digit after it.
        """
        nonlocal testing_number
        nonlocal testing_number_string
        testing_number += 1
        testing_number_string = str(testing_number)
        for i in range(len(testing_number_string)-1):
            if int(testing_number_string[i]) > int(testing_number_string[i+1]):
                testing_number_string = testing_number_string[:i] + 2*testing_number_string[i] + testing_number_string[i+2:]
        else:
            testing_number = int(testing_number_string)

    accepted_numbers = []
    testing_number = lower_bound-1
    testing_number_string = str(testing_number)
    calculate_next_testing_number()
    while testing_number < upper_bound:
        connected_equal_chars_counter = 1
        is_monotonic_digits()
        calculate_next_testing_number()
    return len(accepted_numbers)


def test_number_acceptor():
    assert number_acceptor(123345, 123346) == 1
    assert number_acceptor(123341, 123342) == 0
    assert number_acceptor(123334, 123335) == 0
    assert number_acceptor(111334, 111335) == 1
    assert number_acceptor(112233, 112234) == 1
    print("The test of the function NumberAcceptor was succesful!")


test_number_acceptor()
print(number_acceptor(134564, 585159))
