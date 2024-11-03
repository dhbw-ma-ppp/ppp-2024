# PART 1:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
# The deck of cards should behave like a sequence.
# When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above
# I should be able to index into the deck to retrieve one card.
# I should be able to iterate over all cards in the deck.
# Printing a cards string representation should give me a nice,
# readable description of that card.

class FrenchDeck:
    suits = ['Diamonds', 'Hearts', 'Spades', 'Clubs']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ass']

    def __init__(self):
        self.cards = [f'\n{rank} of {suit}' for suit in self.suits for rank in self.ranks]

    def __getitem__(self, position):
        return self.cards[position]

    def __iter__(self):
        return iter(self.cards)
 
    def __str__(self):
        return ', '.join(str(card) for card in self.cards)

    def __len__(self):
        return len(self.cards)
            
# PART 2:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.

class Skat(FrenchDeck):

    def __init__(self):
        self.ranks = ['7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ass']
        self.cards = [f'\n{rank} of {suit}' for suit in FrenchDeck.suits for rank in self.ranks]

# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)

french_deck = FrenchDeck()
print(f'Length of the French Deck: {len(french_deck)}')
assert len(french_deck) == 52
print(f'\nFrench Deck: {french_deck}')

skat_deck = Skat()
print(f'\nLength of the Skat Deck: {len(skat_deck)}')
assert len(skat_deck) == 32
print(f'\nSkat Deck: {skat_deck}')

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

def validnumbers(lower_bound, upper_bound):
    valid_numbers = []
    valid_counter = 0

    for number in range(lower_bound, upper_bound):
        number_str = str(number)
        is_valid = True
        has_pair = False
        
        for position in range(len(number_str) - 1):
            if number_str[position] > number_str[position + 1]:
                is_valid = False
                break

        if is_valid:    
            for position in range(len(number_str) - 1):
                if number_str[position] == number_str[position + 1]:
                    if  (position == 0 or number_str[position] != number_str[position - 1]) and \
                        (position + 2 >= len(number_str) or number_str[position + 1] != number_str[position + 2]):
                        has_pair = True
                        break
               
        if is_valid and has_pair:    
            valid_numbers.append(number)
            valid_counter += 1

    print(f'For a lower bound of {lower_bound} and an upper bound of {upper_bound}, the following numbers are valid: {valid_numbers}.\nThere are a total of {valid_counter} valid numbers.')

validnumbers(134564, 585159)
# The resulting count is a total of 1306 valid numbers.