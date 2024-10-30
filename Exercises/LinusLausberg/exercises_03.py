# PART 1:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
# The deck of cards should behave like a sequence.
# When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above
# I should be able to index into the deck to retrieve one card.
# I should be able to iterate over all cards in the deck.
# Printing a cards string representation should give me a nice, 
# readable description of that card.

class Card:
    def __init__(self , color , number):
        self.color = color
        self.number = number
    
    def __str__(self):
        return f'{self.color} / { self.number}'

    def get_color(self):
        return self.color
    
    def get_number(self):
        return self.number


class DeckOfCards:
    def __init__(self):
        posible_colors = ['diamonds' , 'hearts' , 'spades' , 'cluds']
        self.deck = []
        for color_on_card in posible_colors:
            for number_preview in range(2, 15): #hier umsetellen wenn zwei ace erwünscht sind
                number_on_card = str
                match number_preview:
                    case 11:
                        number_on_card = 'Bube'
                    case 12:
                        number_on_card = 'Dame'
                    case 13:
                        number_on_card = 'Koenig'
                    case 14:
                        number_on_card = 'Ace'
                    case _:
                        number_on_card = str(number_preview)
                new_Card = Card(color_on_card , number_on_card)
                self.deck.append(new_Card)

    def __getitem__(self, index):
        return self.deck[index]
    
    def __iter__(self):
        return (i for i in self.deck)
    
    def __str__(self):
        for element in self.deck:
            print(element.color , ' / ', element.number)
        return ''
    
    def search(self, color, number):
        found = False
        counter = 0
        while(found == False):
            if(counter >= len(self.deck)):
                print('Card not found!')
            card = self[counter]
            if(card.get_color() == color and card.get_number() == number):
                found = True
            else:
                counter += 1
        return counter


dc = DeckOfCards()


# PART 2:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.

class DeckOfSkartCards(DeckOfCards):
    def __init__(self):
        posible_colors = ['diamonds' , 'hearts' , 'spades' , 'cludes']
        self.deck = []
        for color_on_card in posible_colors:
            for number_preview in range(7, 15): #hier umsetellen wenn zwei ace erwünscht sind
                number_on_card = str
                match number_preview:
                    case 11:
                        number_on_card = 'Bube'
                    case 12:
                        number_on_card = 'Dame'
                    case 13:
                        number_on_card = 'Koenig'
                    case 14:
                        number_on_card = 'Ace'
                    case _:
                        number_on_card = str(number_preview)
                new_Card = Card(color_on_card , number_on_card)
                self.deck.append(new_Card)


sdc = DeckOfSkartCards()


# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)
print('Hier wird das Kartendeck ausgeben:\n')
print(dc)
print('\nHier wird das Skart-Kartendeck ausgeben:\n')
print(sdc)

#testing search on the normal deck
def test_search():
    assert dc.search('cludes' , 'Dame') == 49
    print('\npositiv testing of test_search() on the normal deck\n')

#testing search on the skart deck
def test_search():
    assert sdc.search('spades' , '9') == 18
    print('positiv testing of test_search() on the skart-deck\n')

#testing get_color on the normal deck
def test_get_color():
    assert dc[5].get_color() == 'diamonds'
    print('positiv testing of get_color() and get_card() on the normal deck\n')

#testing get_number on the skart deck
def test_get_number():
    assert sdc[9].get_number() == 8
    print('positiv testing of get_number() and get_card() on the skart-deck\n')

#testing output of a card from the normal deck
def test___str__():
    assert sdc[9] == f'hearts / 8'
    print('positiv testing of an card output from the normal deck\n')

test_search()
test_get_color()
test_get_color()
print(sdc[9])
test___str__()

print(dc[0])
print(sdc[0])


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

def investigation(lower_bound, upper_bound):
    counter = 0
    for number in range(lower_bound , upper_bound):
        positiv_ending = True
        before = -1
        count_behind = 0
        same_behind = 0
        for index in str(number):
            if (int(index) < int(before)):
                positiv_ending = False
                break
            elif(index == before):
                same_behind += 1
            else:
                if(same_behind == 1):
                    count_behind += 1
                same_behind = 0
            before = index
        if (positiv_ending == True):
            if(same_behind == 1 and index != str(number)[len(str(number))-3]):
                    count_behind += 1
            if(count_behind > 0):
                counter += 1
    return counter

print(investigation(134564 , 585159))
#Output: 1306