# PART 1:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
# The deck of cards should behave like a sequence.
# When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above
# I should be able to index into the deck to retrieve one card.
# I should be able to iterate over all cards in the deck.
# Printing a cards string representation should give me a nice, 
# readable description of that card.

class FrenchDeck:
    SUITES = ['diamonds', 'hearts', 'spades', 'clubs']
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

    def __init__(self):
        
        self._cards = [
            Card(rank, suite) 
            for suite in self.SUITES 
            for rank in self.RANKS
        ]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    def __iter__(self):
        return iter(self._cards)


class Card:
    def __init__(self, rank, suite):
        self.rank = rank
        self.suite = suite

    def __str__(self):
        return f"{self.rank} of {self.suite}"

    def __repr__(self):
        return f"Card('{self.rank}', '{self.suite}')"


# PART 2:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.

class SkatDeck(FrenchDeck):
    RANKS = ['7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace'] # Cards for Skat 

    def __init__(self):
        # Create the full French deck first
        super().__init__()
        
        # Create the Skat deck 
        self._cards = [
            card for card in self._cards 
            if card.rank in self.RANKS
        ]





# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)

def test_deck(deck, expected_length, first_card, last_card, deck_name):
    # Test length
    assert len(deck) == expected_length, f"{deck_name} should have {expected_length} cards"

    # Test indexing
    assert str(deck[0]) == first_card, f"First card should be {first_card}"
    #print(first_card)
    assert str(deck[-1]) == last_card, f"Last card should be {last_card}"
    #print(last_card)
    #print('\n')

    # Test iteration
    card_list = list(deck)
    assert len(card_list) == expected_length, f"Iteration for {deck_name} should work correctly"
    assert str(card_list[0]) == first_card, f"First card in iteration should be {first_card}"

# Test French Deck
french_deck = FrenchDeck()
test_deck(french_deck, 52, "2 of diamonds", "Ace of clubs", "French deck")

# Test Skat Deck
skat_deck = SkatDeck()
test_deck(skat_deck, 32, "7 of diamonds", "Ace of clubs", "Skat deck")

print("All deck tests passed!")
print('\n')



# PART 3:
# write a function that accepts two numbers, a lower bound and an upper bound.
# the function should then return the count of all numbers that meet certain criteria:
# - they are within the (left-inclusive and right-exclusive) bounds passed to the function
# - there is at least one group of exactly two adjacent digits within the number which are the same (like 33 in 123345)
# - digits only increase going from left to right

def count_special_numbers(lower_bound, upper_bound):
    def is_valid_number(num_str):
        # Check if digits are increasing
        if list(num_str) != sorted(num_str):
            return False
        
        # Check for at least one group of exactly two repeated digits
        for i in range(len(num_str) - 1):
            if num_str.count(num_str[i]) == 2:
                return True
        
        return False

    # Count numbers meeting the criteria
    count = sum(
        1 for num in range(lower_bound, upper_bound) 
        if is_valid_number(str(num))
    )
    
    return count

# Test the function 
result = count_special_numbers(134564, 585159)
print(f"Count of special numbers: {result}")


# Examples:
# - 123345 is a valid number
# - 123341 is not a valid number, as the digits do not increase from left to right
# - 123334 is not a valid number as there is no group of exactly two repeated digits
# - 111334 is a valid number. while there are three 1s, there is also a group of exactly two 3s.
# - 112233 is a valid number. At least one group of two is fulfilled, there is no maximum to the number of such groups.
#
# run your function with the lower bound `134564` and the upper bound `585159`. Note the resulting count
# in your pull request, please.


