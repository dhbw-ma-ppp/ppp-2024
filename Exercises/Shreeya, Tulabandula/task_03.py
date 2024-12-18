# PART 1:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
# The deck of cards should behave like a sequence.
# When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above
# I should be able to index into the deck to retrieve one card.
# I should be able to iterate over all cards in the deck.
# Printing a cards string representation should give me a nice, 
# readable description of that card.
class Card:
    suits = ['Diamonds', 'Hearts', 'Spades', 'Clubs']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        return f'{self.rank} of {self.suit}'

class FrenchDeck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in Card.suits for rank in Card.ranks]

    def __len__(self):
        return len(self.cards)

    def __getitem__(self, position):
        return self.cards[position]

    def __iter__(self):
        return iter(self.cards)


# PART 2:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.
class SkatDeck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in Card.suits for rank in Card.ranks[5:]]
        
# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)
frenchdeck = FrenchDeck()
assert len(frenchdeck) == 52
assert str(frenchdeck[0]) == "2 of Diamonds"
assert str(frenchdeck[-1]) == "Ace of Clubs"
for card in frenchdeck:
    assert isinstance(card, Card)

print("All objects in Class Frenchdeck are instances of Card!")

skatdeck = SkatDeck()
assert len(skatdeck) == 32
assert str(skatdeck[0]) == "2 of Diamonds"
assert str(skatdeck[-1]) == "Ace of Clubs"
for card in skatdeck:
    assert isinstance(card, Card)

print("All objects in Class Skatdeck are instances of Card!")


# PART 3:
# write a function that accepts two numbers, a lower bound and an upper bound.
# the function should then return the count of all numbers that meet certain criteria:
# - they are within the (left-inclusive and right-exclusive) bounds passed to the function
# - there is at least one group of exactly two adjacent digits within the number which are the same (like 33 in 123345)
# - digits only increase going from left to right

def count_valid_numbers(lower_bound, upper_bound):
    def is_valid(num):
        num_str = str(num)
        
        
        if list(num_str) != sorted(num_str):
            return False
        
        
        for i in range(1, len(num_str)):
            if num_str[i] == num_str[i - 1] and (i == 1 or num_str[i - 2] != num_str[i - 1]) and (i == len(num_str) - 1 or num_str[i + 1] != num_str[i]):
                return True
        
        return False

    
    count = 0
    for num in range(lower_bound, upper_bound):
        if is_valid(num):
            count += 1

    return count

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