import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten',
         'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7
    , 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}
playing = True


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + " of " + self.suit


class Deck:

    def __init__(self):
        self.all_cards = []

        for suit in suits:
            for rank in ranks:
                self.all_cards.append(Card(suit, rank))

    def __str__(self):
        return "There are {} cards left in the deck.".format(len(self.all_cards))

    def shuffle(self):
        random.shuffle(self.all_cards)

    def deal(self):
        return self.all_cards.pop()


class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0  # start with zero value
        self.aces = 0  # add an attribute to keep track of aces

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1  # add to self.aces

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chip:

    def __init__(self, chips=100):
        self.chips = chips
        self.bet = 0

    def win_bet(self):
        self.chips += self.bet

    def lose_bet(self):
        self.chips -= self.bet


def take_bet(chips):
    take = True

    while take:
        try:
            bet = int(input("Please make a bet: "))
        except ValueError:
            print('Sorry, a bet must be an integer!')

        else:
            if not (bet <= chips and bet > 0):
                print("Woops, you do not have enough chips")
            else:
                take = False
    return bet


def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):
    global playing  # to control an upcoming while loop

    while True:
        choose = input("hit or stand? hit = 1, stand = 2 : ")

        if choose == '1':
            hit(deck, hand)
        elif choose == '2':
            print("Player stands. Dealer is playing.")
            playing = False
        else:
            print("Woops, wrong input, please try again.")
            continue
        break


def show_some(player, dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('', dealer.cards[0])
    print("Dealer's Hand =", (dealer.value - (dealer.cards[1].value)))
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =", player.value)


def show_all(player, dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =", dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =", player.value)


def show_player_hand(player):
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =", player.value)


def show_dealer(dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =", dealer.value)


def player_busts(player, dealer, chips):
    print("Player busts!")
    chips.lose_bet()


def player_wins(player, dealer, chips):
    print("Player wins!")
    chips.win_bet()


def dealer_busts(player, dealer, chips):
    print("Dealer busts!")
    chips.win_bet()


def dealer_wins(player, dealer, chips):
    print("Dealer wins!")
    chips.lose_bet()


def push(player, dealer):
    print("There is a tie, push!")


def deposit():
    while True:
        try:
            x = int(input("please make a deposit: "))
        except:
            print("wrong input")
        else:
            if x > 0:
                break
            else:
                print("please enter a positive number.")
    return x


def balance(insert, cash_out):
    if insert > cash_out:
        print(f"Cash out for {cash_out}")
        print(f"You lost {insert - cash_out}")
    elif insert < cash_out:
        print(f"Cash out for {cash_out}")
        print(f"You won {cash_out - insert}")
    else:
        print(f"Cash out for {cash_out}")
        print("Break even")


def double_down(deck, player, player_chips):
    global playing  # to control an upcoming while loop

    if input("Do you want to double down? 'Y' or 'N' ") == 'Y':
        player_chips.bet = player_chips.bet * 2
        hit(deck, player)
        playing = False

def split(deck, player, player_chips):
    global playing  # to control an upcoming while loop

    bet = player_chips.bet

    print("\nHand One:")
    hand_one = Hand()
    hand_one.add_card(player.cards[0])
    hand_one.add_card(deck.deal())

    show_player_hand(hand_one)

    if hand_one.value <= 11:
        double_down(deck, hand_one, player_chips)

    while playing:

        hit_or_stand(deck, hand_one)
        if len(hand_one.cards) > 2:
            show_player_hand(hand_one)

        if hand_one.value > 21:
            # player_busts(player, dealer, player_chips)
            print("Hand one busted")
            player_chips.lose_bet()
            player_chips.bet = bet
            break

        if hand_one.value == 21:
            break

    player_chips.bet = bet
    print("\nHand Two:")
    playing = True
    hand_two = Hand()
    hand_two.add_card(player.cards[1])
    hand_two.add_card(deck.deal())

    show_player_hand(hand_two)

    if hand_two.value <= 11:
        double_down(deck, player, player_chips)

    while playing:

        hit_or_stand(deck, hand_two)
        if len(hand_two.cards) > 2:
            show_player_hand(hand_two)

        if hand_two.value > 21:
            # player_busts(player, dealer, player_chips)
            print("\nHand two busted")
            player_chips.lose_bet()
            player_chips.bet = bet
            break

        if hand_two.value == 21:
            break

    while dealer.value < 17:
        hit(deck, dealer)

    if hand_one.value <= 21 or hand_two.value <= 21:

        show_dealer(dealer)
        if hand_one.value <= 21:

            if dealer.value > 21:
                print("\nHand one won, dealer bust")
                player_chips.win_bet()


            elif hand_one.value > dealer.value:
                print("\nHand one won")
                player_chips.win_bet()

            elif hand_one.value < dealer.value:
                print("\nHand one lost")
                player_chips.lose_bet()

            else:
                print("\nHand one in a tie")

        player_chips.bet = bet

        if hand_two.value <= 21:

            if dealer.value > 21:
                print("\nHand two won, dealer bust")
                player_chips.win_bet()

            elif hand_two.value > dealer.value:
                print("\nHand two won")
                player_chips.win_bet()

            elif hand_two.value < dealer.value:
                print("\nHand two lost")
                player_chips.lose_bet()

            else:
                print("\nHand two in a tie")


if __name__ == '__main__':
    playing = True
    print("Welcome to BlackJack!")
    player_deposit = deposit()
    player_chips = Chip(player_deposit)

    while True:
        deck = Deck()
        deck.shuffle()
        dealer = Hand()
        player = Hand()

        bet = take_bet(player_chips.chips)
        player_chips.bet = bet

        # for_check =deck.deal()
        # for_check =deck.deal()

        player.add_card(deck.deal())
        player.add_card(deck.deal())
        # for_check =deck.deal()
        dealer.add_card(deck.deal())
        dealer.add_card(deck.deal())

        show_some(player, dealer)
        if player.value == 21 and dealer.value < 21:
            print("BlackJack")
            player_chips.bet = bet * 1.5
            player_wins(player, dealer, player_chips)

        elif player.value == 21 and dealer.value < 21:
            push(player, dealer)

        elif player.cards[0].value == player.cards[1].value and player_chips.chips >= 2 * player_chips.bet and (
                input("Do you want to split? 'Y' or 'N' ")) == 'Y':
            split(deck, player, player_chips)

        else:
            if player.value <= 11 and player_chips.chips >= 2 * player_chips.bet:
                double_down(deck, player, player_chips)
            while playing:
                hit_or_stand(deck, player)

                show_some(player, dealer)

                if player.value > 21:
                    player_busts(player, dealer, player_chips)
                    break

                if player.value == 21:
                    break

            if player.value <= 21:

                while dealer.value < 17:
                    hit(deck, dealer)

                show_all(player, dealer)

                if dealer.value > 21:
                    dealer_busts(player, dealer, player_chips)

                elif player.value > dealer.value:
                    player_wins(player, dealer, player_chips)

                elif player.value < dealer.value:
                    dealer_wins(player, dealer, player_chips)
                else:
                    push(player, dealer)

        print("\nCurrent chips : ", player_chips.chips)

        if input("Would you like to play another hand? 'Y' or 'N' : ") == 'N':
            balance(player_deposit, player_chips.chips)
            print("Thank you for playing!")
            break

        if player_chips.chips == 0:
            print("Out of chips")
            player_chips.chips = deposit()
            player_deposit += player_chips.chips

        playing = True
