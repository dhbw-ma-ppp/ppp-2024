# PART 1:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
# The deck of cards should behave like a sequence.
# When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above
# I should be able to index into the deck to retrieve one card.
# I should be able to iterate over all cards in the deck.
# Printing a cards string representation should give me a nice, 
# readable description of that card.

class Card:
    
    def __init__(self, sym, num):
        self.symbol = sym
        self.number = num
        
    def __str__(self):
        return f"This is the {self.number} of {self.symbol}."

class FrenchCardDeck:
    
    def make_Deck(self, syms, nums):
        output = []
        for i in syms:
            for j in nums:
                output.append(Card(i, j))
        return output
    
    def __init__(self):
        self.all_syms = ["diamonds", "hearts", "spades", "clubs"]
        self.all_nums = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self.deck = self.make_Deck(self.all_syms, self.all_nums)
        
    def __iter__(self):
        return (i for i in self.deck)        
        
    def __getitem__(self, i):
        if i < len(self.all_syms) * len(self.all_nums):
            return list(self)[i]
        else:
            return "this card does not exist"
 
def test_code(deck):
    count = 0
    print("------------------------------------------------------------------------------------------------------")
    print("------------------------------------------------------------------------------------------------------")
    print("Cards in deck:")
    for i in deck:
        count += 1
        print(i)
    print(f"There are {count} cards in the deck.")
    print("------------------------------------------------------------------------------------------------------")
    print("Card at index 5:")
    print(deck[5])
    print("------------------------------------------------------------------------------------------------------")
    print("Card at index 5245678:")
    print(deck[5245678])
    print("------------------------------------------------------------------------------------------------------")
    print("------------------------------------------------------------------------------------------------------")

test_code(FrenchCardDeck())

# PART 2:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.

class SkatCardDeck(FrenchCardDeck):
    
    def __init__(self):
        self.all_syms = ["diamonds", "hearts", "spades", "clubs"]
        self.all_nums = ["7", "8", "9", "10", "J", "Q", "K", "A"]
        self.deck = self.make_Deck(self.all_syms, self.all_nums)

test_code(SkatCardDeck())

# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)


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

def count_nums(lower, upper):
    count = 0
    for i in range(lower, upper):
        two_adj = False
        only_increase = True
        while i > 0:
            current = i % 10
            next = (i // 10) % 10
            next_next = (i // 100) % 10
            if (current == next) and (current != next_next): 
                two_adj = True
            while i % 10 == current:
                i = i // 10
            next = i % 10
            if current < next:
                only_increase = False
        if two_adj and only_increase:
            count += 1
    return count

print(f"Counted valid numbers: {count_nums(134564, 585159)}")
                
