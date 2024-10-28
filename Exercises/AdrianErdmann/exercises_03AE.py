# PART 1:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
# The deck of cards should behave like a sequence.
# When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above
# I should be able to index into the deck to retrieve one card.
# I should be able to iterate over all cards in the deck.
# Printing a cards string representation should give me a nice, 
# readable description of that card.

def numberValue(arg, number_value_dict):
    for key, value in number_value_dict.items():
        if arg == key:
            return value
        if arg == value:
            return key

def colorValue(arg, color_value_dict):
    for key, value in color_value_dict.items():
        if arg == key:
            return value
        if arg == value:
            return key


class Card():
    def __init__(self, value, color, ace_value=14, number_value_dict=None, color_value_dict=None):
        if number_value_dict:
            self.number_value_dict = number_value_dict
        else:
            self.number_value_dict = {2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: "jack", 12: "queen", 13: "king"}
            self.number_value_dict[ace_value] = "ace"
        if color_value_dict:
            self.color_value_dict = color_value_dict
        else:
            self.color_value_dict = {1: "diamond", 2: "heart", 3: "spade", 4: "club"}

        if type(value) == int:
            self.value = value
            self.name = [numberValue(value, self.number_value_dict)]
        else:
            self.value = numberValue(value, self.number_value_dict)
        
        if type(color) == int:
            self.color = color
            self.name.append(colorValue(color, self.color_value_dict))
        else:
            self.color = colorValue(color, self.color_value_dict)
            self.name.append(color)
    
    def cardReprTouple(self) -> tuple:
        return self.value, self.color
    
    def cardtotalValue(self) -> int:
        return self.value * self.color
        
    def __str__(self):
        return f"{self.name[0]} of {self.name[1]}s"
    
    def __eq__(self, value: object) -> bool:
        if type(self) == type(value) and self.cardReprTouple() == value.cardReprTouple():
            return True
        return False
    
    def __lt__(self, value: object) -> bool:
        if type(self) == type(value) and self.cardTotalValue() == value.cardTotalValue():
            return True
        return False 


class Deck():
    def __init__(self, all_values, all_colors, ace_value=14, number_value_dict=None, color_value_dict=None):
        self.all_values = all_values
        self.all_colors = all_colors
        self.cards = [Card(value, color, ace_value, number_value_dict=number_value_dict, color_value_dict=color_value_dict) for color in all_colors for value in all_values]

    def retrieveCard(self, index) -> Card:
        return self.cards.pop(index)
    
    def addCard(self, card, index):
        if type(card) == Card:
            self.cards.insert(index, card)
            return True
        return False
    
    def __getitem__(self, index) -> Card:
        return self.cards[index]
    
    def __len__(self) -> int:
        return len(self.cards)

    def __iter__(self):
        return (card for card in self.cards)
    
    def __eq__(self, compare: object) -> bool:
        if type(self) == type(compare) and len(self) == len(compare):
            for i in range(len(self)):
                if self[i] == compare[i]:
                    continue
                break
            else:
                return True
        return False

full_deck = Deck(range(2, 15), range(1, 5))

# PART 2:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.

skat_deck = Deck(range(7, 15), range(1, 5))
skat_deck_test = Deck(range(7, 15), range(1, 5))

# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)

# Two decks with the same cards should be equal
assert skat_deck == skat_deck_test

# First Card should be a 2 of diamnds and last card should be a ace of clubs
assert full_deck[0] == Card(2, 1)
assert full_deck[52 - 1] == Card(14, 4)

# after retrieving the first card the first should be a 3 of diamonds and after adding the first card should be the retrieved card
temp_card = full_deck.retrieveCard(0)
assert full_deck[0] == Card(3, 1)
full_deck.addCard(temp_card, 0)
assert full_deck[0] == temp_card

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
