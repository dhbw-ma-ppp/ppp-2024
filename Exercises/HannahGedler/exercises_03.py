# PART 1:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
# The deck of cards should behave like a sequence.
# When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above
# I should be able to index into the deck to retrieve one card.
# I should be able to iterate over all cards in the deck.
# Printing a cards string representation should give me a nice, 
# readable description of that card.

class Deck:
    def __init__(self, list_of_suite, list_of_range):
        self.__list_of_suite = list_of_suite
        self.__list_of_range = list_of_range
        self.complete_list = []
        self.__initCardSet()

    def __initCardSet(self):
        for suite in self.__list_of_suite:
            for card in self.__list_of_range:
                self.complete_list.append(f"{suite} {card}")         
        
class FrenchDeck(Deck):
    def __init__(self):
        list_of_range = ["2","3","4","5","6","7","8","9","10","jack","lady","king","ace"]
        list_of_suite = ["diamonds", "hearts", "spades", "clubs"]
        super().__init__(list_of_suite, list_of_range)

frenchDeck = FrenchDeck()
print("French Deck:\n",frenchDeck.complete_list)





# PART 2:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.

class Skat(Deck):
    def __init__(self):
        list_of_range = ["7","8","9","10","jack","lady","king","ace"]
        list_of_suite = ["diamonds", "hearts", "spades", "clubs"]
        super().__init__(list_of_suite, list_of_range)

skat = Skat()
print("Skat Deck:\n", skat.complete_list)


# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)
print("French Deck at position 9:",frenchDeck.complete_list[9])
print("Skat Deck at position 9:", skat.complete_list[9])

correct_french_deck = ["diamonds 2", "diamonds 3", "diamonds 4", "diamonds 5", "diamonds 6", "diamonds 7", "diamonds 8", "diamonds 9", "diamonds 10", "diamonds jack", "diamonds lady", "diamonds king", "diamonds ace", "hearts 2", "hearts 3", "hearts 4", "hearts 5", "hearts 6", "hearts 7", "hearts 8", "hearts 9", "hearts 10", "hearts jack", "hearts lady", "hearts king", "hearts ace", "spades 2", "spades 3", "spades 4", "spades 5", "spades 6", "spades 7", "spades 8", "spades 9", "spades 10", "spades jack", "spades lady", "spades king", "spades ace", "clubs 2", "clubs 3", "clubs 4", "clubs 5", "clubs 6", "clubs 7", "clubs 8", "clubs 9", "clubs 10", "clubs jack", "clubs lady", "clubs king", "clubs ace"]
hopefully_correct_french_deck = frenchDeck.complete_list

correct_skat_deck = ['diamonds 7', 'diamonds 8', 'diamonds 9', 'diamonds 10', 'diamonds jack', 'diamonds lady', 'diamonds king', 'diamonds ace', 'hearts 7', 'hearts 8', 'hearts 9', 'hearts 10', 'hearts jack', 'hearts lady', 'hearts king', 'hearts ace', 'spades 7', 'spades 8', 'spades 9', 'spades 10', 'spades jack', 'spades lady', 'spades king', 'spades ace', 'clubs 7', 'clubs 8', 'clubs 9', 'clubs 10', 'clubs jack', 'clubs lady', 'clubs king', 'clubs ace']
hopefully_correct_skat_deck = skat.complete_list

def comparison_french_deck():
    assert frenchDeck.complete_list == hopefully_correct_french_deck
    print("both decks are equal")
comparison_french_deck()

def comparison_skat_deck():
     assert skat.complete_list == hopefully_correct_skat_deck
     print("this should also be equal")
comparison_skat_deck()




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

#def valid_numbers():
lower_bound = 134564
upper_bound = 585159
found_valid_numbers = []

    
def adjacent_digits(value):
    value = str(value)
    #if value[i] == value[i+1] != value [i+2] or value
    for i in range(len(value)-1):
        if i == 0: 
            if value[i] == value[i+1] != value[i+2]:
                return True
        elif i == len(value)-2:
            if value[i-1] != value[i] == value[i+1]:
                return True
        elif i > 0 : 
            if value[i-1] != value[i] == value[i+1] != value[i+2]:
                return True
        else: 
            return False

def increasing_integers(value):
        value = str(value)
        if value[0] <= value[1] <= value[2] <= value [3] <= value [4] <= value [5]:
            return True
        else:
            return False 
        

for value in range(lower_bound, upper_bound):
    if adjacent_digits(value) and increasing_integers(value) == True:
        found_valid_numbers.append(value)
        
adjacent_digits(value)
increasing_integers(value)

resulting_count = len(found_valid_numbers)
#print(found_valid_numbers)
print("The resulting count is" ,resulting_count)


