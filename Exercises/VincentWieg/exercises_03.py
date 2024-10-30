# PART 1:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
# The deck of cards should behave like a sequence.
# When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above
# I should be able to index into the deck to retrieve one card.
# I should be able to iterate over all cards in the deck.
# Printing a cards string representation should give me a nice, 
# readable description of that card.


class Card:
    suits = ["diamond", "heart", "spade", "club"]
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king", "ace"]

    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __repr__(self):
        return f"{self.value} of {self.suit}"

class FrenchCards:
    def __init__(self):
        # Initialize the deck of cards in a well-defined order
        self.cards = [Card(value, suit) for suit in Card.suits for value in Card.values]

    def __getitem__(self, index):
        return self.cards[index]

    def __iter__(self):
        return iter(self.cards)

    def __len__(self):
        return len(self.cards)


# PART 2:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.

class SkatDeck(FrenchCards):
    def __init__(self):
        self.cards = [Card(value, suit) for suit in Card.suits for value in Card.values[5:]]  # Start from "7"

# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)

deck = FrenchCards()
print(deck[0])             
print(len(deck))           
print(list(deck)[:5])
print(deck[2])

skat_deck = SkatDeck()
print(skat_deck[31])
print(len(skat_deck))


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

def NumberCount(low_bound, high_bound):
    def HasAdjacentPair(num_str):
        for i in range(len(num_str) - 1):
            #check if digit is same as next:
            if num_str[i] == num_str[i + 1]:
                 #check if there are exactly 2 of the digit:
                 if (i - 1 < 0 or num_str[i - 1] != num_str[i]) and (i + 2 >= len(num_str) or num_str[i + 2] != num_str[i]):
                    return True
    
    def IsIncreasing(num_str):
        return all(num_str[i] <= num_str[i+1] for i in range(len(num_str) - 1))

    count = 0
    for num in range(low_bound, high_bound):
        num_str = str(num)
        if HasAdjacentPair(num_str) and IsIncreasing(num_str):
                count += 1
    return count


print(NumberCount(134564, 585159))