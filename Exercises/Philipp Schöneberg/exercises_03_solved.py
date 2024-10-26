import itertools

# PART 1:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
# The deck of cards should behave like a sequence.
# When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above
# I should be able to index into the deck to retrieve one card.
# I should be able to iterate over all cards in the deck.
# Printing a cards string representation should give me a nice, 
# readable description of that card.


class FrenchDeckOfCards:
    suits = ["diamonds", "hearts", "spades", "clubs"]

    def __init__(self):
        self.ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self.cards = list(itertools.product(self.suits, self.ranks))

    def __iter__(self):
        return (elem for elem in self.cards)

    def __getitem__(self, index):
        return self.cards[index]

    def __str__(self):
        return str(list(self))


# PART 2:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.


class SkatDeckOfCards(FrenchDeckOfCards):
    def __init__(self):
        self.ranks = ["7", "8", "9", "10", "J", "Q", "K", "A"]
        self.cards = list(itertools.product(self.suits, self.ranks))


# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)

french_deck_0 = FrenchDeckOfCards()
skat_deck_0 = SkatDeckOfCards()

print(french_deck_0)
for elem in french_deck_0:
    print(elem)

print(skat_deck_0)
for elem in skat_deck_0:
    print(elem)


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

def NumberAcceptor(lower_bound, upper_bound):
    accepted_number_counter = 0
    accepted_numbers = []
    for testing_number in range(lower_bound, upper_bound+1):
        testing_number_string = str(testing_number)
        connected_equal_chars_counter = 1
        for i in range(len(testing_number_string)-1):
            if connected_equal_chars_counter == 2 and testing_number_string[i] != testing_number_string[i+1]:
                for j in range(len(testing_number_string)-1):
                    if int(testing_number_string[j]) > int(testing_number_string[j+1]):
                        break
                else:
                    accepted_number_counter += 1
                    accepted_numbers.append(testing_number)
                    break
            elif testing_number_string[i] == testing_number_string[i+1]:
                connected_equal_chars_counter += 1
            else:
                connected_equal_chars_counter = 1
    print(accepted_numbers)
    print(accepted_number_counter)
    return accepted_number_counter


NumberAcceptor(134564, 585159)
