""" Blackjack game classes

This module contains the classes used for a black jack game.

The ruleset used is Vegas Strip Blackjack:

- Dealer stands on soft 17
- Blackjack pays 3:2
- Dealer peeks for Blackjack
- Double Down allowed on initial hand and split
- Player may split 3 times for a total of 4 hands
- Aces may only be split one time
- Only one card can be taken to split Aces
- 21 on split Aces does not count as Blackjack
- Player may split unlike 10-value cards

"""

from random import shuffle


class Card():
    """A single card in a deck.

    has a name and a value in the form of an int or a pair
    of integers inside a tuple in the case of an Ace

    """

    def __init__(self, name, value):

        self._name = name
        self._value = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __str__(self):
        return f'{self.name}'

class CardDeck():

    """A deck of cards that containing six sets of 52 unique cards

    can be shuffled, and cards can be removed from it to be dealt to
    a player or the dealer.

    """

    suits = ['clubs', 'diamonds', 'hearts', 'spades']
    face_value = {
        'Ace': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5,
        'Six': 6,
        'Seven': 7,
        'Eight': 8,
        'Nine': 9,
        'Ten' : 10,
        'Jack': 10,
        'Queen': 10,
        'King':10
        }


    def __init__(self):

        self.deck = []
        for _ in range(0, 6):
            for suit in CardDeck.suits:
                for face in CardDeck.face_value:
                    self.deck.append(Card(f'{face} of {suit}', CardDeck.face_value[face]))

    def shuffle_cards(self):
        """ shuffle cards in deck """
        shuffle(self.deck)

    def get_card(self):
        """ returns a card from the top of the deck """
        return self.deck.pop()

    # For testing only,
    def show_cards(self):

        for card in self.deck:
            print(card)

class Hand():

    """
    A hand holds a set of cards dealt to a given player for a given bet or when
    a player performs a split.

    it can be discarded, split or receive additional cards

    """

    def __init__(self, bet):
        """Initializes hand to a hold no cards, represented as an empty list."""
        self.cards = []
        self._bet = bet
        self.is_soft = False # tracks whether an ace is counted as 11
        self.value = 0

    def add_card(self, card):
        """adds a card received from the dealer to the hand and calculates
        the new value of the hand

        """

        self.cards.append(card)
        self.add_to_value(card)

    def add_to_value(self, card):
        """ adds the value of a card whenever a new card
        is added to the hand. Keeps track of whether a hand is
        counting an ace as 11 and adjust accordingly. 
        
        """

        if card.value == 1:
            if self.value >= 11:
                self.value += 1
            else:
                self.value += 11
                self.is_soft = True
        else:
            self.value += card.value
            if self.is_bust() and self.is_soft:
                self.value -= 10
                self.is_soft = False

    def is_blackjack(self):
        """checks if hand is blackjack"""
        card_one_value = self.cards[0].value
        card_two_value = self.cards[1].value

        return (card_one_value == 1 and card_two_value == 10) or (card_one_value == 10 and card_two_value == 1)

    def is_bust(self):
        """ checks if value is more than 21 """
        return self.value > 21

    def is_splitable(self):
        """ If the hand only has two cards and those cards are of the same
        value then then the hand is splittable.

        OUTPUT: returns True if splittable, False if not.

        """

        card_one = self.cards[0]
        card_two = self.cards[1]
        if len(self.cards) == 2:
            return card_one.value == card_two.value
        return False

    @property
    def bet(self):
        """ get the amount bet for the current hand """
        return self._bet

    @bet.setter
    def bet(self, amount):
        """ set the bet amount for the current hand """
        self._bet = amount

    def __str__(self):
        """Creates and returns a string representation of the
        cards in this hand and the associated bet.
        
        """

        string = f"Bet: ${self.bet}.\n"
        string += "Cards -> "
        for card in self.cards:
            string += f"{card.__str__()} - "
        string += f"\nValue of cards: {self.value}"
        return string

class Player():
    """
    A player has one or several hands containing cards and has a wallet of money.

    They can place a bet, split on a pair, double down, stand or hit.

    """

    def __init__(self):

        self.hands = []
        self.index_curr_hand = 0
        self.curr_hand = None
        self.wallet = 100

    def set_next_hand(self):
        """ Changes the players current hand to the next hand """

        self.index_curr_hand += 1
        self.curr_hand = self.hands[self.index_curr_hand]
            
    def place_bet(self, amount):
        """Places a bet and creates a hand"""
        self.hands.append(Hand(amount))
        self.curr_hand = self.hands[0]
        self.wallet -= amount

    def cash_in_bet(self, amount, multiplier):
        """ Calculate and add winnings to wallet

        OUTPUT: bet value (int), bet multiplier (float, int)

        """

        self.wallet += (amount * multiplier)

    def discard_hands(self):
        """ Discards all cards and resets values for play """
        self.hands.clear()
        self.curr_hand = None
        self.index_curr_hand = 0

    def has_blackjack(self):
        """checks for blackjack after initial deal"""

        return self.curr_hand.is_blackjack()

    def can_double_down(self):
        """ tests if the player can double down. Player can only double down if
        they have sufficient funds in their wallet to make the bet, and if they
        have only 2 cards in the hand to be double down upon

        """
        return ((self.wallet - self.curr_hand.bet) >= 0) and (len(self.curr_hand.cards) == 2)

    def double_down(self):
        """ Doubles the bet for the hand provided."""
        self.wallet -= self.curr_hand.bet
        self.curr_hand.bet *= 2

    def can_split(self):
        """ Tests if a hand can be split, and checks whether a hand has been split on an
        Ace before. If a split ace exists the current hand can't be split
        
        OUTPUT: returns True or False
        
         """
        
        if len(self.hands) < 4:
            if (self.curr_hand.cards[0].value == 1) and (len(self.hands) == 2):
                return False
            elif self.curr_hand.is_splitable():
                return True
            return False
        return False

    def split(self):
        """ Splits the hand when holding pairs to create a new hand """
        if len(self.hands) < 4:
            new_hand = Hand(self.curr_hand.bet) # makes new hand
            # decrements value of current hand by value of card to be removed
            self.curr_hand.value -= self.curr_hand.cards[1].value
            # removes card from current hand putting it in new hand
            # adding its value to the hands value
            new_hand.add_card(self.curr_hand.cards.pop(1))
            self.hands.append(new_hand)
            self.wallet -= new_hand.bet

        else:
            print("Cannot split more than 3 times per game.")

    def has_next_hand(self):
        """ Checks if the player has more hands to play

        OUTPUT: True or False
        """

        return (self.index_curr_hand) < (len(self.hands) - 1)

class Dealer():
    """A dealer has one hand of cards and a deck of cards.

    They can shuffle a deck, deal cards to players, and themselves.
    They can peek on a face up ace, and they can only stand or hit.

    """

    def __init__(self):
        self.curr_hand = Hand(0)
        self.deck = None

    def deal_card(self, player_dealer):
        """ Takes card from top of deck and deals it to themselves or a player current hand """
        card = self.deck.get_card()
        player_dealer.curr_hand.add_card(card)

    def new_deck(self):
        """ Gets a new deck and shuffles it"""
        self.deck = CardDeck()
        self.shuffle()

    def shuffle(self):
        """shuffle a deck of cards"""
        self.deck.shuffle_cards()

    def has_blackjack(self):
        """ If face up card is an ace then dealer peeks to see
        if they have blackjack.

        OUTPUT: True or False

        """
        if self.curr_hand.cards[0].value == 1:
            return self.curr_hand.is_blackjack()
        return False


    def discard_hand(self):
        """ removes all cards from his hand """
        self.curr_hand.cards.clear()
        self.curr_hand.value = 0
