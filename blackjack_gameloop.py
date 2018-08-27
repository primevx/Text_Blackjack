import blackjack
from time import sleep

DEALER = blackjack.Dealer()
PLAYER = blackjack.Player()

def main_menu():

    prompt = "\n1. play\n2. quit game\n\nSelect an option (1-2): "
    user_input = get_valid_input(prompt, ['1', '2'])

    if user_input == '1':
        game()
        main_menu()
    elif user_input == '2':
        exit()
    else:
        print("\n\tInvalid Input!\n")
        main_menu()

def game():

    #INITIALIZE VARIABLES
    global DEALER
    global PLAYER
    DEALER.new_deck()
    print("\n-------------------------\n Dealer shuffles deck \n-------------------------\n")

    playing = True #game-loop control variable

    while playing:

        prompt = "\n1. bet\n2. stop playing\n\nSelect an option (1-2): "
        user_input = get_valid_input(prompt, ['1', '2'])
        
        if user_input == '1':
            bet_amount = bet() # Place a bet
            if bet_amount == None:
                print("Insufficient funds, GAME OVER.")
                break
            initialize_play_phase() # Dealer deals cards to player and dealer
            if DEALER.has_blackjack() and PLAYER.has_blackjack():
                print_play_area()
                print("-------- PUSH --------")
                print("----------------------")
                print("--- PLAYER & HOUSE ---")
                print("--- HAVE BLACKJACK ---")
                print("======================")
                print(f"bet of ${bet_amount} returned")
            elif PLAYER.has_blackjack():
                print_play_area()
                print("----- PLAYER HAS BLACKJACK! -----")
                dealer_play_hand()
                compare_hands()
            elif DEALER.has_blackjack():
                print_play_area()
                print("----- HOUSE HAS BLACKJACK! -----")
                print("---------- HOUSE WINS ----------")
                print("================================")
                print(f"Bet of ${bet_amount} lost")
            else:
                print("-------------------")
                print("-- PLAYER'S TURN --")
                print("-------------------")
                for _ in PLAYER.hands:
                    if PLAYER.has_next_hand():
                        set_next_hand()
                    play_hand()
                dealer_play_hand()
                compare_hands()
        else:
            playing = False

def bet():
    """ Discards old hands, and requests player how much they would like
    to bet ($1, $5, or $10)

    OUTPUT: Integer 1, 5, or 10

    """

    PLAYER.discard_hands()
    DEALER.discard_hand()
    print(f"\nPlayer has ${PLAYER.wallet} in their wallet!")
    valid_bets = get_valid_bets()
    prompt = f"\nHow much would you like to bet {valid_bets}: "
    if valid_bets == None:
        return None
    else:
        bet_amount = int(get_valid_input(prompt, valid_bets))
        PLAYER.place_bet(bet_amount)
        return bet_amount

def get_valid_bets():
    """ generates a list of bets the player can make based on current availble wallet """

    bet_values = ['1', '5', '10', '50' ,'100']

    if PLAYER.wallet <= 0:
        return None
    elif PLAYER.wallet >= 100:
        return bet_values
    elif PLAYER.wallet >= 50:
        return bet_values[0:4]
    elif PLAYER.wallet >= 10:
        return bet_values[0:3]
    elif PLAYER.wallet >= 5:
        return bet_values[0:2]
    else:
        return bet_values[0]

def initialize_play_phase():
    """ Deals cards to each player at start of a game """
    # bet place, dealer deals cards to player.
    DEALER.deal_card(PLAYER)
    DEALER.deal_card(PLAYER)
    # dealer deals to themselves.
    DEALER.deal_card(DEALER)
    DEALER.deal_card(DEALER)
           
def play_hand():
    """ Game loop for playing out the current player's hand """
    while True:
        
        print_play_area()   
        can_split = PLAYER.can_split()
        can_double_down = PLAYER.can_double_down()
        num_of_curr_hand = PLAYER.index_curr_hand + 1
        user_input = play_options(can_double_down, can_split)

        if user_input == '1':
            # Stand and move to next hand if there is one
            print_hand_result(f"hand {num_of_curr_hand}: {PLAYER.curr_hand.value} ")
            break
        elif user_input == '2':
            # Hit
            DEALER.deal_card(PLAYER)
        elif user_input == '3':
            # Double down, and take one more card.
            PLAYER.double_down()
            DEALER.deal_card(PLAYER)
            print_play_area()
            if PLAYER.curr_hand.is_bust():
                print_hand_result(f"BUST: {PLAYER.curr_hand.value} ")
            else:    
                print_hand_result(f"hand {num_of_curr_hand}: {PLAYER.curr_hand.value} ")
            break
        elif user_input == '4':
            # Split hand
            PLAYER.split()
            DEALER.deal_card(PLAYER)
        if PLAYER.curr_hand.value == 21:
            print_hand_result(f"hand {num_of_curr_hand}: {PLAYER.curr_hand.value} ")
            break    
        if PLAYER.curr_hand.is_bust():
            print_hand_result(f"BUST: {PLAYER.curr_hand.value} ")
            break

def dealer_play_hand():
    """ Play out the dealers hand. First checks for blackjack, or
    checks if value is less than 17 or a soft 17 and deals a card, or
    checks if value is over 21.

    OUTPUT: 'blackjack', 'bust', or value of the dealers hand as integer

    """
    print("---------------------------------")
    print("--------- DEALER'S TURN ---------")
    print("---------------------------------\n")

    while True:
        hand_value = DEALER.curr_hand.value
        is_hand_soft = DEALER.curr_hand.is_soft
        print("\nDealer's " + DEALER.curr_hand.__str__()[9:])
        if DEALER.has_blackjack():
            return "blackjack"
        elif hand_value < 17 or (hand_value == 17 and is_hand_soft):
            DEALER.deal_card(DEALER)
        elif hand_value > 21:
            return "bust"
        else:
            return hand_value
        sleep(0.2)
        
def compare_hands():
    """Compares player's hands with the dealers hand, prints results and winnings
    and adds winning to wallet.

    """
    num = 1 # Number of current hand
    dealers_hand = DEALER.curr_hand
    
    for players_hand in PLAYER.hands:
        
        bet_amount = players_hand.bet
        if num > 1:
            print("\n\n=================================")
            print(f"----------- Hand {num} -------------")
        print("=================================")
        print(f"-- Dealer: {dealers_hand.value}  vs  Player: {players_hand.value} --")
        print("=================================")
        if dealers_hand.is_blackjack() and players_hand.is_blackjack() :
            print("------------- PUSH --------------")
            print("---------------------------------")
            print("-------- PLAYER & HOUSE ---------")
            print("-------- HAVE BLACKJACK ---------")
            print("=================================")
            print(f"Hand {num}'s bet of ${bet_amount} returned")
            print("=================================")
            PLAYER.cash_in_bet(bet_amount, 1)
        elif dealers_hand.is_blackjack():
            print("----- DEALER HAS BLACKJACK! -----")
            print("---------- DEALER WINS ----------")
            print("=================================")
            print(f"Hand {num}'s bet of ${bet_amount} lost")
            print("=================================")
        elif players_hand.is_blackjack():
            print("----- PLAYER HAS BLACKJACK! -----")
            print("---------- PLAYER WINS ----------")
            print("=================================")
            print(f"Hand {num} wins you ${2.5*bet_amount}")
            print("=================================")
            PLAYER.cash_in_bet(bet_amount, 2.5)
        elif dealers_hand.is_bust() and players_hand.is_bust():
            print("------------- PUSH --------------")
            print("=================================")
            print(f"Hand {num}'s bet of ${bet_amount} returned")
            print("=================================")
            PLAYER.cash_in_bet(bet_amount, 1)
        elif dealers_hand.is_bust():
            print("--------- PLAYER WINS! ----------")
            print("=================================")
            print(f"Hand {num} wins you ${2*bet_amount}")
            print("=================================")
            PLAYER.cash_in_bet(bet_amount, 2)
        elif players_hand.is_bust():
            print("--------- DEALER WINS! ----------")
            print("=================================")
            print(f"Hand {num}'s bet of ${bet_amount} is lost")
        elif dealers_hand.value == players_hand.value:
            print("------------- PUSH --------------")
            print("=================================")
            print(f"Hand {num} bet of ${bet_amount} returned")
            print("=================================")
            PLAYER.cash_in_bet(bet_amount, 1)
        elif dealers_hand.value > players_hand.value:
            print("--------- DEALER WINS! ----------")
            print("=================================")
            print(f"Hand {num}'s bet of ${bet_amount} is lost")
            print("=================================")
        elif players_hand.value > dealers_hand.value:
            print("--------- PLAYER WINS! ----------")
            print("=================================")
            print(f"Hand {num} wins you ${2*bet_amount}")
            print("=================================")
            PLAYER.cash_in_bet(bet_amount, 2)
        num += 1 # increment hand number
        sleep(0.3)

def print_play_area():
    """ Prints details for a hand in play """


    total_hands = len(PLAYER.hands)
    num_of_curr_hand = PLAYER.index_curr_hand + 1

    print("\n===================================================")
    print("Wallet: ${}  ".format(PLAYER.wallet))
    print("===================================================")
    print(f"Dealer showing -> {DEALER.curr_hand.cards[0].name}")
    print("---------------------------------------------------")
    print(f"hand {num_of_curr_hand} of {total_hands}")
    print(PLAYER.curr_hand.__str__())
    print("---------------------------------------------------\n")
    
def set_next_hand():
    """ prints that next hand is being played and updates players current hand
    to that of the next hand available
    
    """

    print("|     Next hand     |")
    print("=" * 21)
    PLAYER.set_next_hand()
    DEALER.deal_card(PLAYER)

def print_hand_result(result):
    """ prints out result window of played hand
    
    INPUT: expects string of even length

    """
    
    if len(result) % 2:
        empty_space = " " * int((19 - len(result)) / 2)
    else:
        empty_space = " " * int((18 - len(result)) / 2)
    print("\n" + "=" * 21)
    print("|" + empty_space + f"{result}" + empty_space + "|")
    print("=" * 21)

def play_options(can_double_down, can_split):
    """ List all options a player has available to them when playing a given hand.
    Validates input for each set of options, if valid returns the input.

    OUTPUT: single character '1', '2', '3', or '4'
    """

    options = ("1) Stand.", "2) Take hit", "3) Double down", "4) Split hand")
    prompt = ""
    if can_double_down and can_split:
        # Request user choice between first 4 options
        for option in options:
            prompt += option + "\n"
        prompt += "Select an option (1-4): "
        return get_valid_input(prompt, ['1', '2', '3', '4'])
    elif can_double_down:
        # Request user choice between first 3 options
        for option in options[0:3]:
            prompt += option + "\n"
        prompt += "Select an option (1-3): "
        return get_valid_input(prompt, ['1', '2', '3'])
    else:
        # Request user choice between first 2 options
        for option in options[0:2]:
            prompt += option + "\n"
        prompt += "Select an option (1-2): "
        return get_valid_input(prompt, ['1', '2'])

def get_valid_input(prompt, valid_input):
    """ prompts user for input and using the provided list
    of valid inputs validates the input.

    INPUT: string prompt, list of valid inputs
    OUTPUT: validated input
    """
    is_valid = False
    while not is_valid:
        user_input = input(prompt)
        is_valid = user_input in valid_input # validates input

    return user_input

main_menu()
