# PART 1:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
# The deck of cards should behave like a sequence.
# When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above
# I should be able to index into the deck to retrieve one card.
# I should be able to iterate over all cards in the deck.
# Printing a cards string representation should give me a nice,
# readable description of that card.

class Card:
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['♦', '♥', '♠', '♣']  # Use of symbols instead of words

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"{self.rank}{self.suit}"


class FrenchDeck:
    def __init__(self):
        self._cards = [Card(rank, suit) for suit in Card.suits for rank in Card.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    def __iter__(self):
        return iter(self._cards)


# Tests and checks
def RunTest():
    print(f"Deck hat {len(deck)} Karten.")
    print(f"Erste Karte im Deck: {deck[0]}")
    print(f"Karte in der Mitte des Decks: {deck[len(deck) // 2]}")

    for card in deck:
        print(card)

    assert len(deck) == 52, "FrenchDeck should contain 52 cards"
    assert deck[0].rank == '2' and deck[0].suit == '♦', "First card should be '2 of ♦'"
    assert deck[-1].rank == 'A' and deck[-1].suit == '♣', "Last card should be 'A of ♣'"
    print("FrenchDeck tests passed!")

deck = FrenchDeck()
RunTest()

# PART 2:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.

class SkatDeck(FrenchDeck):
    def __init__(self):
        # Calls the constructor of the parent class and filters the cards from 7 upwards
        super().__init__()
        self._cards = [card for card in self._cards if card.rank in Card.ranks[5:]]

# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)

def test_skat_deck():
    print(f"Deck hat {len(s_deck)} Karten.")
    print(f"Erste Karte im Deck: {s_deck[0]}")
    print(f"Karte in der Mitte des Decks: {s_deck[len(s_deck) // 2]}")

    assert len(s_deck) == 32, "SkatDeck should contain 32 cards"
    assert s_deck[0].rank == '7' and s_deck[0].suit == '♦', "First card should be '7 of ♦'"
    assert s_deck[-1].rank == 'A' and s_deck[-1].suit == '♣', "Last card should be 'A of ♣'"
    print("SkatDeck tests passed!")

    for card in s_deck:
        print(card)

s_deck = SkatDeck()
test_skat_deck()

# PART 3:
    # Soeren hat gesagt ich soll dig benutzen LMAO
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
def has_pairs(num_str):
    for i in range(len(num_str) - 1):
        if num_str[i] == num_str[i + 1]:
            # Check if the pair is exactly two (not part of a larger group)
            if (i == 0 or num_str[i] != num_str[i - 1]) and (i + 2 >= len(num_str) or num_str[i] != num_str[i + 2]):
                return True
    return False

def count_valid_number(lower_bound, upper_bound):
    count = 0
    for num in range(lower_bound, upper_bound):
        num_str = str(num) # easyer to work with numbers as strings for your usecase
        if(has_pairs(num_str) & (list(num_str) == sorted(num_str))):
            count += 1
    return count

lower_bound = 134564
upper_bound = 585159
valid_number = count_valid_number(lower_bound, upper_bound)
print(f"Count of valid numbers between {lower_bound} and {upper_bound}: {valid_number}")
