# PART 1:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
# The deck of cards should behave like a sequence.
# When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above
# I should be able to index into the deck to retrieve one card.
# I should be able to iterate over all cards in the deck.
# Printing a cards string representation should give me a nice, 
# readable description of that card.

class Card():
    def __init__(self, value, color) -> None:
        self.value = value
        self.color = color
    
    def cardReprTouple(self) -> tuple:
        return self.value, self.color
    
    def __eq__(self, value) -> bool:
        if type(value) != type(self):
            return NotImplemented
        if self.cardReprTouple() == value.cardReprTouple():
            return True
        
    def __str__(self) -> None:
        return f"{self.value} of {self.color}s"


class Deck():
    def __init__(self, all_values, all_colors) -> None:
        self.all_values = all_values
        self.all_colors = all_colors
        self.cards = [Card(value, color) for color in all_colors for value in all_values]

    def retrieveCard(self, index) -> Card:
        return self.cards.pop(index)
    
    def addCard(self, card, index) -> bool:
        if type(card) == Card:
            self.cards.insert(index, card)
            return True
        return False
    
    def __getitem__(self, index) -> Card:
        return self.cards[index]
    
    def __len__(self) -> int:
        return len(self.cards)

    def __iter__(self) -> tuple:
        return (card for card in self.cards)


class FrenchDeck(Deck):
    def __init__(self) -> None:
        all_values = [str(x) for x in range(2, 11)] + ["jack", "queen", "ace"]
        all_colors = ["diamond", "heart", "spade", "club"]
        super().__init__(all_values, all_colors)


french_deck = FrenchDeck()

# PART 2:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.

class SkatDeck(Deck):
    def __init__(self) -> None:
        all_values = [str(x) for x in range(7, 11)] + ["jack", "queen", "king", "ace"]
        all_colors = ["diamond", "heart", "spade", "club"]
        super().__init__(all_values, all_colors)


skat_deck = SkatDeck()

# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)

# First Card should be a 2 of diamnds and last card should be a ace of clubs
assert french_deck[1] == Card("3", "diamond")
assert skat_deck[-2] == Card("king", "club")

# after retrieving the first card the first should be a 3 of diamonds and after adding the first card should be the retrieved card
temp_card = french_deck.retrieveCard(0)
assert french_deck[0] == Card("3", "diamond")
french_deck.addCard(temp_card, 0)
assert french_deck[0] == temp_card

# Testing if print-converting a card to a string is working
test_pos = 21
print(f"The card at position {test_pos} is a {skat_deck[test_pos]}.\n") # should return a nice message

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

def specialNumbers(lower_number, upper_number):
    passed_numbers = []
    for number in range(lower_number, upper_number):
        i = 1
        str_number = str(number)
        char_number = [str_number[0], 1]
        two_consecutive_chars = False
        while i < len(str_number):
            if char_number[0] == str_number[i]:
                char_number[1] = char_number[1] + 1
                if i == len(str_number) - 1 and char_number[1] == 2:
                    two_consecutive_chars = True
            elif char_number[0] < str_number[i]:
                if char_number[1] == 2:
                    two_consecutive_chars = True
                char_number = [str_number[i], 1]
            else:
                break
            i += 1
        else:
            if two_consecutive_chars:
                passed_numbers.append(number)
    return passed_numbers

print(len(specialNumbers(134564, 585159)))
