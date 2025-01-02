# Simple Blackjack Game
## Description
This is a program that runs a simple Blackjack game between the player and the computer. 
Cards are dealt to both the player and the computer, and the player can choose to either hit (get another card), or hold (pass on the turn to the computer).
The Computer always hits if their hand is less than or equal to 17. 
Cards are valued at their face value, with the exeption of face cards and Aces. All face cards have a value of 10, and Aces have a value of either 1 or 11.
In the event that either the player or the character busts (their hand is over 21), the other automatically wins. 
If neither the player nor the computer busts after their turns, the winner is determined by whoever has the higher hand. 
After the winner is determined, the program automatically ends.

## Determining the Card (Value, Character, Suit, and Color)
A card deck is initialized, which are represented as a list of numbers. 
Each number is associated with a different card. 
For example, 0 is the Ace of Spades, 1 is the 2 of Spades, etc.
The card value is determined by the ```card_value()``` function, with the exception of an Ace card, which is handled when determining the value of a hand.
```
def card_value(card):
    no_suit = card % 13 + 1
    if no_suit <= 10:
        return no_suit
    else:
        return 10
```
The card character displayed is determined by the ```card_char()``` function (i.e. A, 2, 3, ..., 10, J, Q, K).
```
def card_char(card):
    no_suit = card % 13 + 1
    if no_suit in range(2, 11):
        return no_suit
    else:
        # A = 1, J = 11, Q = 12, K = 13
        index = (no_suit / 10) + (no_suit % 10) - 1
        return faces[int(index)]
```
The card suit is determined by the ```card_suit()``` function, and returns the unicode of the assocaited suit. 
The suits are in the order of Spades, Hearts, Diamonds, Clubs in the unshuffled deck. (&spades;, &hearts;, &diams;, &clubs;)
```
def card_suit(card):
    suit = card / 13
    if suit < 1:
        return "\U00002660"
    elif suit < 2:
        return "\U00002665"
    elif suit < 3:
        return "\U00002666"
    else:
        return "\U00002663"
```
The colors of the suits are determined in a seperate function ```card_color()```, and returns either black `#000000` (for Spades and Clubs), or red `#FF0000` (for Hearts and Diamonds).
```
def card_color(card):
    color = (int(card / 13) + 3) % 4
    if color >= 2:
        return 'black'jj
    else:
        return 'red'
```
## Dealing and Drawing Cards
The card deck is then shuffled and the cards are dealt, starting with the player. 
Per the rules of Blackjack, the player sees their hand, but only second (and onward) cards of the dealer's hand.
The player then either hits or holds by either pressing ```j``` or ```f``` on their keyboard, respectively.
If the player holds, their turn ends.

```
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
```
As for the computer, they automatically hit if their score is less than 17. 
```
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
```

## Displaying Cards
After the cards are initially dealt and each time either the player or the dealer hits, the board is displayed in the terminal via the ```show()``` funciton.
The player's hand, computer's hand, and optionally a boolean determining whether the game is finished (by default, the game is not finished).
If finished, all of the computer's cards are displayed. Otherwise, it is not shown.
All other cards are shown with the proper character, suit, and color using the ```card_char()```, ```card_suit()```, and ```card_color()``` functions.
```
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
```
## Calculating Scores and Determining the Winner
When calculating the score, all possible sums are stored in a sums list.
For each Ace in each hand, they are scored as both a 1 and 11.
(Thus, the list of sums doubles with each Ace in hand.)
Once all sums have been calculated, all sums that bust (over 21) are moved from the sums list.
If there are no remaining sums (i.e. the hand busts), the score returned is 0.
The highest non-bust score is returned otherwise.
```
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
```
The winner is then calculated simply by whoever got the higher score.
The winner is then displayed, and the program ends.
```
dealer_score = calculate(dealer)
player_score = calculate(player)
print("\n")
print("Dealer Score: " + str(dealer_score))
print("Player Score: " + str(player_score))

if (dealer_score > player_score):
    print("The Dealer won.")
else:
    print(fg('green') + "You won!")
```
