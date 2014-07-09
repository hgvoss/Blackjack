import string, math, random

class Card (object):
  RANKS = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)

  SUITS = ('S', 'D', 'H', 'C')

  def __init__ (self, rank, suit):
    self.rank = rank
    self.suit = suit

  # Assign values to face cards
  def __str__ (self):
    if self.rank == 1:
      rank = 'A'
    elif self.rank == 13:
      rank = 'K'
    elif self.rank == 12:
      rank = 'Q'
    elif self.rank == 11:
      rank = 'J'
    else:
      rank = self.rank
    return str(rank) + self.suit

  def __eq__ (self, other):
    return (self.rank == other.rank)

  def __ne__ (self, other):
    return (self.rank != other.rank)

  def __lt__ (self, other):
    return (self.rank < other.rank)

  def __le__ (self, other):
    return (self.rank <= other.rank)

  def __gt__ (self, other):
    return (self.rank > other.rank)

  def __ge__ (self, other):
    return (self.rank >= other.rank)

# Create Deck and shuffle
class Deck (object):
  def __init__ (self):
    self.deck = []
    for suit in Card.SUITS:
      for rank in Card.RANKS:
        card = Card (rank, suit)
        self.deck.append(card)

  def shuffle (self):
    random.shuffle (self.deck)

  def __len__ (self):
    return len (self.deck)

  def deal (self):
    if len(self) == 0:
      return None
    else:
      return self.deck.pop(0)

# Create Players' hands 
class Player (object):
  def __init__ (self, cards):
    self.cards = cards

  def hit (self, card):
    self.cards.append(card)

  def getPoints (self):
    count = 0
    for card in self.cards:
      if card.rank > 9:
        count += 10
      elif card.rank == 1:
        count += 11
      else:
        count += card.rank

    # deduct 10 if Ace is there and needed as 1
    for card in self.cards:
      if count <= 21:
        break
      elif card.rank == 1:
        count = count - 10
    
    return count

  # does the player have 21 points or not
  def hasBlackjack (self):
    return len (self.cards) == 2 and self.getPoints() == 21

  # Print cards and points
  def __str__ (self):
    cardStr = ""
    for card in self.cards:
       cardStr += str(card) + " "
    return str(cardStr) + " - " + str(self.getPoints()) + " points"
    
# Dealer class inherits from the Player class
class Dealer (Player):
  def __init__ (self, cards):
    Player.__init__ (self, cards)
    self.show_one_card = True

  # Dealer hits until has at least 17 points
  def hit (self, deck):
    self.show_one_card = False
    while self.getPoints() < 17:
      self.cards.append (deck.deal())

  # Return just one card if not hit yet
  def __str__ (self):
    if self.show_one_card:
      return str(self.cards[0])
    else:
      return Player.__str__(self)

# Play Blackjack
class Blackjack (object):
  def __init__ (self):
    self.deck = Deck()
    self.deck.shuffle()

    self.Hand = []
    self.Hand.append (Player([self.deck.deal(), self.deck.deal()]))

    self.dealer = Dealer ([self.deck.deal(), self.deck.deal()])

  def play (self, currentChips, bet):
    # Print the cards that each player has
    print ('Player 1: ' + str(self.Hand[0]))

    # Print the cards that the dealer has
    print ('Dealer: ' + str(self.dealer))

    '''
    SPLITTING
    if self.Hand[0].cards[0].rank == self.Hand[0].cards[1].rank:
    split = raw_input (' Would you like to split? [y / n]: ')
    if split in ('y', 'Y'): 
        self.Hand1 = []
        self.Hand2 = []
        #self.Hand1.append(self.Hand[0].cards[0])
        self.Hand1.append(Player([self.Hand[0].cards[0], self.deck.deal()])
        print self.Hand1[0]
    '''

    # Give player the option to Double Down
    dd = raw_input (' Would you like to double down? [y / n]: ')
    if dd in ('y', 'Y'):
      bet = bet * 2

    # Each player hits until he says no
    playerPoints = []
    while True:
        choice = raw_input (' Do you want to hit? [y / n]: ')
        if choice in ('y', 'Y'):
          (self.Hand[0]).hit (self.deck.deal())
          points = (self.Hand[0]).getPoints()
          print ('Player 1: ' + str(self.Hand[0]))
          if points >= 21:
            break
        else:
          break
    playerPoints.append ((self.Hand[0]).getPoints())
    

    # Dealer's turn to hit
    self.dealer.hit (self.deck)
    dealerPoints = self.dealer.getPoints()
    print ('Dealer: ' + str(self.dealer))
    print

    # Determine the outcome
    for i in range(len(playerPoints)):
      if playerPoints[i] > 21:
        print "Player 1 loses"
        currentChips = currentChips - bet
      elif self.Hand[0].hasBlackjack():
        print "Player 1 wins"
        currentChips = currentChips + bet
      elif dealerPoints > 21:
        print"Player 1 wins"
        currentChips = currentChips + bet
      elif dealerPoints <= 21:
        if playerPoints[i] > dealerPoints:
          print "Player 1 wins"
          currentChips = currentChips + bet
        elif playerPoints[i] < dealerPoints:
          print "Player 1 loses"
          currentChips = currentChips - bet
        else:
          print "Player 1 ties"
    print "Current Chips: " + str(currentChips)
    return currentChips

def main ():
  currentChips = 100
  print "You currently have " + str(currentChips) + " chips"
  while currentChips > 0:
    bet = raw_input ('How many chips would you like to bet? ')
    while int(bet) > currentChips or int(bet) < 1:
      bet = raw_input('How many chips would you like to bet? ')
    game = Blackjack ()
    currentChips = game.play(currentChips, int(bet))




main()