# Simple Blackjack Game - Samantha Song - started 2024.12.09

# Simple Blackjack game between a computer and player. 
# Steps:
#   Shuffle Cards
#   Deal Cards - 2 cards each (player first), second card facing up
#       Dealer [][2]
#       Player [Q][5]
#   Check if either player has Blackjack
#   Hold or Hit (player) - As many rounds as they want
#       If Player busts (goes over 21), they automatically lose
#   Hold or Hit (dealer) - Must hit if total < 17
#       Dealer [][2][7]
#       Player [Q][5][2]
#   Show all cards and determine who wins

# Packages
import random
import keyboard
import time
from colored import fg

# Creates stack of cards
# Ordered by Spades, Hearts, Diamonds, Clubs (A -> K within each suit)
card_deck = list(range(52))

# Card order will be AJQK then numericals
faces = ['A', 'J', 'Q', 'K']

# Shuffle Cards
random.seed()
random.shuffle(card_deck)

# Initialize all variables
card_ind = 0
player = []
dealer = []
player_turn = True
dealer_turn = True
time_delay = 0.25

# ------------------------ Functions ------------------------

# Determines Card Value (1, 2, ..., 10, 10, 10, 10)
# A value will be handled elsewhere
def card_value(card):
    no_suit = card % 13 + 1
    if no_suit <= 10:
        return no_suit
    else:
        return 10

# Determines Printed Card Character (A, 2, ..., 10, J, Q, K)
def card_char(card):
    no_suit = card % 13 + 1
    if no_suit in range(2, 11):
        return no_suit
    else:
        # A = 1, J = 11, Q = 12, K = 13
        index = (no_suit / 10) + (no_suit % 10) - 1
        return faces[int(index)]
    
# Determines Suit (Spades, Hearts, Diamonds, Clubs)
def card_suit(card):
    suit = card / 13
    if suit < 1:
        return "\U00002660"
    elif suit < 2:
        return "\U00002665"
    elif suit < 3:
        return "\U00002666"
    else:
        return "\U00002664"
    
# Determines Card Color (Spades, Hearts, Diamonds, Clubs)
def card_color(card):
    color = int(card / 13) % 2
    if color == 0:
        return 'black'
    else:
        return 'red'
    
# Deals next card from card deck
def deal():
    global card_ind
    next_card = card_deck[card_ind]
    card_ind += 1
    return next_card

# Show cards for both players
# If game is finished, then show all cards
# By default, game is not finished
def show(p1, p2, finished=False):
    # Show Dealer's cards
    print(fg('black') + "\nDealer:")
    # If finished, show all of dealer's cards, else hide dealer's first card
    if finished:
        print(fg(card_color(p1[0])), end='')
        print("[" + str(card_suit(p1[0])) + str(card_char(p1[0])) + "]", end='')
    else:
        print("[ ]", end='')
    for i in range(1, len(p1)):
        print(fg(card_color(p1[i])), end='')
        print("[" + str(card_suit(p1[i]))+ str(card_char(p1[i])) + "]", end='')
    # Show all of Player's cards
    print(fg('black') + "\nPlayer:")
    for j in p2:
        print(fg(card_color(j)), end='')
        print("[" + str(card_suit(j))+ str(card_char(j)) + "]", end='')
    print(fg('black'), end='')

# Calculate score
# Returns 0 if Bust, or highest valid value (<= 21)
def calculate(hand):
    sum = [0]
    # Calculates all possible sums: A = 1 and 11
    for i in range(len(hand)):
        if card_value(hand[i]) == 1:
            sum_1 = [x + 1 for x in sum]
            sum_11 = [x + 11 for x in sum]
            sum = sum_1 + sum_11
        else:
            sum = [x + card_value(hand[i]) for x in sum]
    # Removes all sums that bust
    sum = list(filter(lambda x: x <= 21, sum))
    # If all sums bust, return 0
    if len(sum) == 0:
        return 0
    # Sorts remaining sums from highest to lowest
    sum.sort(reverse=True)
    # Returns highest sum
    return sum[0]
    

# ------------------------ Play Simple Blackjack ------------------------
# First 2 cards are dealt to each player
for i in range(2):
    player.append(deal())
    dealer.append(deal())

# Show board to player
show(dealer, player)

# Player hits until they choose to hold
print("\nPress \'f\' to hold or \'j\' to hit.")
while player_turn:
    # If player busts, end game
    if calculate(player) == 0:
        player_turn = False
        dealer_turn = False
        print("You busted. Sorry, you lose.")
    # Player Hits - Add Card - Update board
    if keyboard.is_pressed('j'):
        player.append(deal())
        show(dealer, player)
        time.sleep(time_delay)
        print("\nPress \'f\' to hold or \'j\' to hit.")
    # Player Holds - End Player turn
    if keyboard.is_pressed('f'):
        player_turn = False

# Dealer hits until their total score is >= 17
while dealer_turn:
    time.sleep(1)
    if calculate(dealer) == 0:
        print(fg('green') + "You won, the dealer busted.")
        dealer_turn = False
    elif calculate(dealer) < 17:
        dealer.append(deal())
        print("\nDealer hit.\n")
        show(dealer, player)
    else:
        dealer_turn = False
    print("\n")

# Determine Winner
time.sleep(1)
show(dealer, player, finished=True)
dealer_score = calculate(dealer)
player_score = calculate(player)
print("\n")
print("Dealer Score: " + str(dealer_score))
print("Player Score: " + str(player_score))

if (dealer_score > player_score):
    print("The Dealer won.")
else:
    print(fg('green') + "You won!")

