# PART 1:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
# The deck of cards should behave like a sequence.
# When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above
# I should be able to index into the deck to retrieve one card.
# I should be able to iterate over all cards in the deck.
# Printing a cards string representation should give me a nice, 
# readable description of that card.

class Card():
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    SUITS = ['Diamonds', 'Hearts', 'Spades', 'Clubs']

    def __init__(self, rank, suit) -> None:
        if(rank not in Card.RANKS and suit not in Card.SUITS):
            raise ValueError("Please enter a correct suit and/or rank")
        self.rank = rank
        self.suit = suit

    def __str__(self) -> str:
        return f"{self.rank} of {self.suit}"

class FrenchDeck():
    def __init__(self):
        self.cards = [Card(rank, suit) for suit in Card.SUITS for rank in Card.RANKS]

    def __getitem__(self, index):
        return self.cards[index]

    def __iter__(self):
        return iter(self.cards)

    def __len__(self):
        return len(self.cards)


# PART 2:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.

class SkatDeck(FrenchDeck):
    def __init__(self):
        self.ranks = ["7", "8", "9", "10", "J", "Q", "K", "A"]
        self.cards =  [Card(rank, suit) for suit in Card.SUITS for rank in self.ranks]

    





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

def validate_number_range(low, high):
    """
    This function accepts a lower and upper bound number. The number returns the count of numbers that meet the following criteria:
    - they are within the (left-inclusive and right-exclusive) bounds passed to the function
    - there is at least one group of exactly two adjacent digits within the number which are the same (like 33 in 123345)
    - digits only increase going from left to right
 
    The following function is implemented using a dictionary.
    """
    count = 0
    
    for number in range(low, high):
        number_dict = {}
        num_str = str(number)
        has_exact_pair = False

        # test if the number is going higher
        if list(num_str) == sorted(num_str):
            
            for i in range(len(num_str)-1):
                if num_str[i] == num_str[i + 1]:
                    if num_str[i] in number_dict:
                        number_dict[num_str[i]] += 1
                    else:
                        number_dict[num_str[i]] = 1

            for key, value in number_dict.items():
                if value == 1:  # if there is exactly one pair then count
                    has_exact_pair = True
                    break

            if has_exact_pair:
                count += 1
        

    return count

print(validate_number_range(134564, 585159))


def test_validate_numbers():
    assert validate_number_range(134564, 585159) == 1306, "Function produces the wrong output"


# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)


def deck_test(deckType):
    match deckType:
        case "skat":
            deck = SkatDeck()
            assert str(deck[0]) == '7 of Diamonds'
            assert str(deck[-1]) == 'A of Clubs'
            assert len(deck) == 32
            skat_ranks = RANKS = ['7', '8', '9', '10', 'J', 'Q', 'K', 'A']
            card_list = [Card(rank, suit) for suit in Card.SUITS for rank in skat_ranks]
            for elem in deck: 
                assert str(elem) in [str(card) for card in card_list]
        case "french":
            deck = FrenchDeck()
            card_list = [Card(rank, suit) for suit in Card.SUITS for rank in Card.RANKS]
            assert str(deck[0]) == '2 of Diamonds'
            assert str(deck[-1]) == 'A of Clubs'
            assert len(deck) == 52
            for elem in deck: 
                assert str(elem) in [str(card) for card in card_list]

def test_skat():
    deck_test("skat")
    

def test_french():
    deck_test("french")
