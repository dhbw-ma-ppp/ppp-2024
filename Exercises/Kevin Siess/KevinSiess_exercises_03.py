# PART 1:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
# The deck of cards should behave like a sequence.
# When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above
# I should be able to index into the deck to retrieve one card.
# I should be able to iterate over all cards in the deck.
# Printing a cards string representation should give me a nice, 
# readable description of that card.

def read_cards(deck):
    print(f"Decktype: {type(deck).__name__}")  # Print the name of the class
    print(f"Decklength: {len(deck)}")          # Length of deck
    print(f"First Card: {deck[0]}")            # First card
    print(f"Last Card: {deck[-1]}")            # Last card

    print("All cards in the deck:")
    for card in deck:  # Iteration over all cards
        print(card)

# Card class definition
class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

# Frenchdeck
class Frenchdeck:
    ranks = [str(n) for n in range(2, 11)] + ["Jack", "Queen", "King", "Ace"]
    suits = ["Diamonds", "Hearts", "Spades", "Clubs"]
    
    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

# Skatdeck
class Skatdeck(Frenchdeck):
    ranks = [str(n) for n in range(7, 11)] + ["Jack", "Queen", "King", "Ace"]
    suits = ["Diamonds", "Hearts", "Spades", "Clubs"]

# Instantiate and test Frenchdeck
print(f"Testing Frenchdeck:")
french_deck = Frenchdeck()
read_cards(french_deck)

# Assertions for Frenchdeck
assert len(french_deck) == 52, "Frenchdeck should have 52 cards"
assert french_deck[0].__repr__() == "2 of Diamonds", "The first card should be '2 of Diamonds'"
assert french_deck[-1].__repr__() == "Ace of Clubs", "The last card should be 'Ace of Clubs'"

# Instantiate and test Skatdeck
print(f"\nTesting Skatdeck:")
skat_deck = Skatdeck()
read_cards(skat_deck)

# Assertions for Skatdeck
assert len(skat_deck) == 32, "Skatdeck should have 32 cards"
assert skat_deck[0].__repr__() == "7 of Diamonds", "The first card should be '7 of Diamonds'"
assert skat_deck[-1].__repr__() == "Ace of Clubs", "The last card should be 'Ace of Clubs'"

print(f"\nAll tests were sucessful!")


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

def count_valid_numbers(lower, upper):
    # check for digit_twins
    def digit_twins(number):
        number_str = str(number)
        count = 1  
        for i in range(1, len(number_str)):
            if number_str[i] == number_str[i - 1]:
                count += 1
            else:
                if count == 2:  
                    return True
                count = 1  
        return count == 2 
    
    #check if digits increase from left to right
    def digits_increase(number):
        number_str = str(number)

        if sorted(number_str) != list(number_str):
            return False
        
        for i in range(1, len(number_str)):
            if number_str[i] < number_str[i - 1]:
                return False
        return True


    valid_count = 0
    for number in range(lower, upper):
        if digit_twins(number) and digits_increase(number):
            valid_count += 1

    return valid_count


lower_bound = 134564
upper_bound = 585159
result = count_valid_numbers(lower_bound, upper_bound)
print(f"Count of valid numbers: {result}")

