import os 
import random
suits = ('Hearts', 'Spades', 'Diamonds', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,'Queen':10, 'King':10, 'Ace':11}


class Deck():
  """A deck of cards for BlackJack."""
  base_setup = [2,3,4,5,6,7,8,9,10,'Knight','Queen','King','Ace']
  def __init__(self):
    self.discards = []
    self.deck = []
    for suit in suits:
      for rank in ranks:
        self.deck.append((rank,suit))
    self.shuffle()
  
  def shuffle(self):
    random.shuffle(self.deck)

  def reshuffle(self):
    self.deck.extend(self.discards[:])
    self.shuffle(self.deck)
    self.discards = []

  def deal_card(self):
    if self.deck:
      return self.deck.pop()
    else:
      print("Deck is empty")
      #Fix reshuffle
  
  def discard(self,cards):
    self.discards.extend(cards)

class Person():
  """This is the base class for participants of BlackJack dealer and players and should not be used directly"""
  def __init__(self):
    self.cards = []
    self.aces = 0
    
  def __str__(self):
    return "This is the base class for participants of BlackJack"

  def deal_cards(self,deck,amount):
    for n in range(amount):
      self.cards.append(deck.deal_card())
      if self.cards[-1][0] == 'Ace':
        self.aces += 1
  
  def discard_hand(self,deck):
    deck.discard(self.cards[:])
    self.cards = []
    self.aces = 0

  def get_value(self):
    value = 0
    for rank,suits in self.cards:
      value += values[rank]
    if not self.aces:
      return value
    elif value <= 31:
      return value-10
    elif value <= 41 and self.aces>1:
      return value-20
    elif value <= 51 and self.aces>2:
      return value-30
    elif value <= 61 and self.aces>3:
      return value-40
    else:
      return value

  def display_hand(self):
    print(f'\n{self.name} hand (value: {self.get_value()}):')
    for rank,suit in self.cards:
      print(f'{rank} of {suit}')

class Player(Person):
  """This is the player class.
  
  Attributes:
  name = string with player name
  money = float of player funds for the game"""

  def __init__(self,name,money=10.0):
    self.name = name
    self.chips = money
    self.cards = []
    self.aces = 0
  
  def __str__(self):
    return f"Player name: {self.name}\nMoney: {self.chips}"

  def get_chipcount(self):
    return self.chips

  def make_bet(self,bet):
    if self.chips > bet:
      self.chips -= bet
      return True
    else:
      return False
  
  def collect_winnings(self,amount):
    self.chips += amount
    print(f'Winnings collected. New chipcount: {self.chips}')

class Dealer(Person):
  """This is the dealer class."""

  name = 'Dealer'

  def __str__(self):
    return "This is the dealer."

  def display_one(self):
    print(f'\n{self.name} hand:\nFirst card hidden\n{self.cards[1][0]} of {self.cards[1][1]}')

def clear():
  os.system('clear')

def player_turn(player):
  """Function for player turn. 
  Returns Tuple of (Outcome,Hand value)
  Outcome is a string of 'BJ', 'Over' or 'Under'
  Hand value is an int of hand value"""
  while True:
    clear()
    dealer.display_one()
    player.display_hand()
    
    if player.get_value() > 21: #Check if bust
      return ('Over',player.get_value()) 
    elif player.get_value() == 21: #Check if 21
      if len(player.cards) == 2: #Check if BLackJack
        return ('BJ',player.get_value())
      return ('Under',player.get_value())
    else: #Continue play
      player_choice = input("\nDo you want to HIT or STAND?\n")
      if player_choice[0].upper() == 'H':
        player.deal_cards(deck,1)
        continue
      elif player_choice[0].upper() == 'S':
        return ('Under',player.get_value())

def dealer_turn():
  """Function for dealer turn. 
  Returns Tuple of (Outcome,Hand value)
  Outcome is a boolean with TRUE if safe and FALSE if bust
  Hand value is an int of hand value"""
  while True:
    clear()
    dealer.display_hand()
    player.display_hand()
    
    if dealer.get_value() < 17: #Check if should hit
      dealer.deal_cards(deck,1)
      continue
    elif dealer.get_value() > 21: #Check if bust
      return (False,dealer.get_value())
    else: #Return if not bust
      return (True,dealer.get_value())

def play_loop(deck, dealer, player):
  """Function for the main game loop which takes input of deck and has no output.
  The deck should be a List of Tuples according to ('card_rank','card suit')"""
  clear()
  print(f"Great! Starting a game for {player.name} who has a chiptotal of {player.chips}")
  #check input and funds
  while True:
    try:
      bet = float(input("Make bet: "))
    except ValueError:
      print("Not a number, try again!")
      continue
    else:
      if player.make_bet(bet):
        print("Bet accepted. Lets Play!")
        break
      else:
        print(f"Not available funds. Yout chiptotal is: {player.chips}")
        continue

  #initialize game
  dealer.deal_cards(deck,2)
  player.deal_cards(deck,2)

  #Player turn
  p_outcome, p_value = player_turn(player)
  print("\n")
  if p_outcome == 'Over': #Check bust
    print("You busted!")
  elif p_outcome == 'BJ': #Check BlackJack
    print(f"You got BlackJack! You win {bet*2}!")
    player.collect_winnings(bet*2)
  else:
    d_outcome, d_value = dealer_turn()
    print("\n")
    if d_outcome: #Dealer not bust
      if p_value > d_value: #Player win
        print(f"You got {p_value} and the dealer got {d_value}, you win {bet*1.5}")
        player.collect_winnings(bet*1.5) 
      elif p_value == d_value: #Draw
        print(f"You got {p_value} and the dealer got {d_value}, it's a Draw! You get your money back.")
        player.collect_winnings(bet)
      else: #Player lose
        print(f"You got {p_value} and the dealer got {d_value}, you lose.") 
    else: #Dealer bust
      print(f"Dealer busted! You win {bet*1.5}!")
      player.collect_winnings(bet*1.5)

  while True:
    again = input("\nDo you want to play again? (Y/N)\n")
    if again.lower() == 'y':
      player.discard_hand(deck)
      dealer.discard_hand(deck)
      play_loop(deck, dealer, player)
      break
    elif again.lower() == 'n':
      break
    else:
      print("Sorry i didn't understand that. Try again!")
      continue


"""
Start of game
"""
print('Welcome to BlackJack!')
print('Dealer will hit always hit under 17.\n')
name = input("What is your name? ")
while True:
  try:
    cash = float(input("How much money do you want to turn inte chips? "))
  except ValueError:
    print("Not a number, try again!")
  else:
    break

#initializing deck, players and starting game
deck = Deck()
player = Player(name,cash)
dealer = Dealer()
play_loop(deck, dealer, player)

"""
Try including multiple players.
Try adding in Double-Down and card splits!
"""