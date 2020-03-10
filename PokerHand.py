# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 22:13:38 2020

@author: Hans Hidalgo Alta
"""

from collections import Counter

class PokerHand:
  """
  Class that represents a Poker Hand. This class has a constructor 
  that accepts a string containing 5 cards. Also has a method
  to compare it with another Pokerhand.
  
  For this, I used a score according to the values of the cards.
    # 10: Royal Flush
    # 9: Straight Flush
    # 8: Four of a kind
    # 7: Full house
    # 6: Flush
    # 5: Straight
    # 4: Three of a kind
    # 3: Two pair
    # 2: One pair
    # 1: High card
    
  It also validates that the input (Poker Hand) is correct.
    
  Parameters
  ----------
  poker_hand : str
        String containing 5 cards
  """
  # Constructor
  def __init__(self, poker_hand):
    """
    Constructor that accepts a string containing 5 cards.
    """
    self.poker_hand = poker_hand

  @property
  def poker_hand(self):
    return self.__poker_hand

  @poker_hand.setter
  def poker_hand(self,poker_hand):
    """
    Method to validate the Poker Hand
    
    Parameters
    ----------
    poker_hand: str
        Poker Hand to evaluate.

    Returns
    ----------
    'ERROR': If the input of the Poker Hand is not correct
    """
    # It has to have 5 cards
    if len(poker_hand.split(' '))!=5:
        raise ValueError("You must enter 5 poker cards per hand")
    
    # Two strings per card
    if max([len(x) for x in poker_hand.split(' ')])!=min([len(x) for x in poker_hand.split(' ')]):
       raise ValueError("Incorrect format of the poker card")
    elif max([len(x) for x in poker_hand.split(' ')])!=2:
        raise ValueError("Incorrect format of the poker card")
        
    # Evaluate the values of the cards
    posible_values = ["2","3","4","5","6","7","8","9","T","J","Q","K","A"]
    if sum([x[0] in posible_values for x in poker_hand.split(' ')])!=5:
        raise ValueError("Invalid value")
        
    # Evaluate the suit of the cards
    posible_suit = ["S","H","D","C"]
    if sum([x[1] in posible_suit for x in poker_hand.split(' ')])!=5:
        raise ValueError("Invalid suit")
    
    self.__poker_hand =  poker_hand

    
  def compare_with(self,poker_hand_2):
    """
    Method to compare it with another Pokerhand.
    
    Parameters
    ----------
    self.poker_hand: str
        First Poker Hand to compare.
        
    poker_hand_2.poker_hand: str
        Second Poker Hand to compare.

    Returns
    ----------
    'WIN': If the First Poker Hand wins to the Second
    'LOSS': Otherwise
    """
    # Each poker hand is transformed into two lists, the first with the card values and the second with the card suits
    values_hand_1, suits_hand_1 = self.poker_hand_to_list(self.poker_hand)
    values_hand_2, suits_hand_2 = self.poker_hand_to_list(poker_hand_2.poker_hand)
    
    # Obtain the poker hand score and maximum value of the cards in denomination sequence (if it exists).
    score_hand_1, max_value_in_sequence_1 = self.score_hand(values_hand_1,suits_hand_1)
    score_hand_2, max_value_in_sequence_2 = self.score_hand(values_hand_2,suits_hand_2)
    
    # If the scores are different, a winner is defined.
    if score_hand_1!=score_hand_2:
      return 'WIN' if score_hand_1>score_hand_2 else 'LOSS'
    # If the scores are equal, the winner is the one with the highest value in the denomination sequences.
    elif (score_hand_1==score_hand_2)&(score_hand_1>0)&(max_value_in_sequence_1 != max_value_in_sequence_2):
      return 'WIN' if max_value_in_sequence_1>max_value_in_sequence_2 else 'LOSS'
    # Otherwise, the winner is the hand with the card of the highest denomination.
    else:
      return 'WIN' if self.high_card(values_hand_1, values_hand_2) else 'LOSS'
  
  def poker_hand_to_list(self,poker_hand):
    """
    Method to transformed a string of Poker Hand in two lists, 
    the first with the card values and the second with the card suits
    
    Parameters
    ----------
    poker_hand: str
        Poker Hand to transform.
        
    Returns
    ----------
    values_hand: list
        List of values of the Poker Hand (int).
        
    suits_hand: list
        List of suits of the Poker Hand (str).
    """
    # Dictionary to identify the card value (from str to int)
    values_dict = {"2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "T":10, "J":11, "Q":12, "K":13, "A":14}
    # Get the value of the cards with values_dict
    values_hand = [values_dict[x[0]] for x in poker_hand.split(' ')]
    # Get the suit of the cards
    suits_hand = [x[1] for x in poker_hand.split(' ')]
    return values_hand, suits_hand

  def is_Flush(self,suits_hand):
    """
    Method to evaluate if the poker hand is "Flush"
    
    Parameters
    ----------
    suits_hand: list
        List of suits of the Poker Hand (str).
        
    Returns
    ----------
    True: If the poker hand is "Flush"
    False: Otherwise
    """
    return len(set(suits_hand))==1
  
  def is_Straight(self,values_hand):
    """
    Method to evaluate if the poker hand has five cards in denomination sequence ("Straight").
    For this, 5 values must be different and the difference between minimum and maximum value is 4.
    
    Parameters
    ----------
    suits_hand: list
        List of suits of the Poker Hand (str).
        
    Returns
    ----------
    True: If the poker hand is "Straight"
    False: Otherwise
    """
    return (len(set(values_hand))==5)&((max(values_hand) - min(values_hand))==4)

  def score_Flush_Straight(self,values_hand,suits_hand):
    """
    Method to calculate the Poker Hand score if it has a "Flush" and/or "Straight"
    
    The ratings to evaluate are:
    # 10: Royal Flush
    # 9: Straight Flush
    # 6: Flush
    # 5: Straight
    
    The following variables and formula is used:
    hand_is_Flush: 2 if Poker Hand is Flush otherwise 0
    hand_is_Straight: 1 if Poker Hand is Straight otherwise 0
    min_is_10: 1 if the min value of the Poker Hand is 10 otherwise 0
    
    auxiliar_score_Flush_Straight = hand_is_Flush + hand_is_Straight + hand_is_Straight*min_is_10*(hand_is_Flush/2)
    
    With this table the "auxiliar_score_Flush_Straight" is converted to "FINAL SCORE"
    ---------------------------------------------------------
    |  FINAL SCORE       |   auxiliar_score_Flush_Straight  |
    ---------------------------------------------------------
    | 10: Royal Flush    |               4                  | 
    | 9: Straight Flush  |               3                  |
    | 6: Flush           |               2                  |
    | 5: Straight        |               1                  |
    | Otherwise          |               0                  |
    ---------------------------------------------------------
    
    Parameters
    ----------
    values_hand: list
        List of values of the Poker Hand (int).
        
    suits_hand: list
        List of suits of the Poker Hand (str).
        
    Returns
    ----------
    score_Flush_Straight: int
        Score of the Poker Hand if it has a "Flush" and/or "Straight"
        else return 0
    """
    # Dictionary to convert auxiliar_score_Flush_Straight to the "FINAL SCORE"
    score_Flush_Straight_dict = {4: 10,
                                3: 9,
                                2: 6,
                                1: 5,
                                0: 0}
    # Create the variables
    hand_is_Flush = int(self.is_Flush(suits_hand))*2
    hand_is_Straight = int(self.is_Straight(values_hand))
    min_is_10 = int(min(values_hand)==10)
    
    # Calculate the valor of auxiliar_score_Flush_Straight
    auxiliar_score_Flush_Straight = hand_is_Flush + hand_is_Straight + hand_is_Straight*min_is_10*(hand_is_Flush/2)
    return score_Flush_Straight_dict[auxiliar_score_Flush_Straight]

  def score_denomination_sequence(self,values_hand):
    """
    Method to calculate the Poker Hand score if it has values with the same denomination.
    
    The ratings to evaluate are:
    # 8: Four of a kind
    # 7: Full house
    # 4: Three of a kind  
    # 3: Two pair         
    # 2: One pair         
    
    The following variables and formula is used:
    counter_values_hand: Dictionary with the following structure: 
        key: different values of the Poker Hand
        value: number of repetitions of the card value
    different_values: number of different values of the Poker Hand
    max_count_of_one_value: maximum number of repetitions of the card value
    
    auxiliar_score_denomination_sequence = (3 - different_values) + max_count_of_one_value
    
    With this table the "auxiliar_score_denomination_sequence" is converted to "FINAL SCORE"

    --------------------------------------------------------------------------------------------------------
    |     FINAL SCORE    | different_values | max_count_of_one_value | auxiliar_score_denomination_sequence|
    --------------------------------------------------------------------------------------------------------
    | 8: Four of a kind  |        2         |           4            |           (3-2) + 4 = 5             |
    | 7: Full house      |        2         |           3            |           (3-2) + 3 = 4             |
    | 4: Three of a kind |        3         |           3            |           (3-3) + 3 = 3             |
    | 3: Two pair        |        3         |           2            |           (3-3) + 2 = 4             |
    | 2: One pair        |        4         |           2            |           (3-4) + 2 = 1             |
    | Other              |        4         |           1            |           (3-5) + 1 = -1            |
    --------------------------------------------------------------------------------------------------------
    
    Parameters
    ----------
    values_hand: list
        List of values of the Poker Hand (int).    
        
    Returns
    ----------
    score_denomination_sequence: int
        Score of the Poker Hand if it has a values with the same denomination
        else return 0
    
    max_value_in_sequence: int
        Value of the denomination with greater sequence -max_count_of_one_value- (in the case of a tie)
    """
    # Dictionary to convert auxiliar_score_denomination_sequence to the "FINAL SCORE"
    score_denomination_sequence_dict = {5: 8,
                                        4: 7,
                                        3: 4,
                                        2: 3,
                                        1: 2,
                                        -1: 0}
    # Dictionary with different values of the Poker Hand (key) and number of repetitions of the card value (value)
    counter_values_hand = dict(Counter(values_hand))
    # Number of different values of the Poker Hand
    different_values = len(counter_values_hand)
    # Maximum number of repetitions of the card value
    max_count_of_one_value = max(counter_values_hand.values())
    # Calculate the valor of auxiliar_score_denomination_sequence
    auxiliar_score_denomination_sequence = (3 - different_values) + max_count_of_one_value
    return score_denomination_sequence_dict[auxiliar_score_denomination_sequence], max([k for k, v in counter_values_hand.items() if v == max_count_of_one_value])

  def score_hand(self,values_hand,suits_hand):
    """
    Method to calculate the score of the Poker Hand if it has "Flush"/"Straight"
    or it has values with the same denomination.
    
    Parameters
    ----------
    values_hand: list
        List of values of the Poker Hand (int).
        
    suits_hand: list
        List of suits of the Poker Hand (str).
        
    Returns
    ----------
    score_hand: int
        Score of the Poker Hand.
        
    max_value_in_sequence: int
        Value of the denomination with greater sequence if the Poker Hand
        has values with the same denomination, otherwise 0.
    """
    return self.score_denomination_sequence(values_hand) if self.score_denomination_sequence(values_hand)[0]>0 else (self.score_Flush_Straight(values_hand,suits_hand),0)

  def high_card(self,values_hand_1, values_hand_2):
    """
    Recursive Method to define the winner of the Poker Hand with the maxmimum value
    of the two hands.
    
    Parameters
    ----------
    values_hand_1: list
        List of values of the first Poker Hand (int).
        
    values_hand_2: list
        List of values of the second Poker Hand (int).
        
    Returns
    ----------
    True: If the first Poker Hand is the winner
    False: Otherwise
    """
    # Sort the list values descending
    values_hand_1.sort(reverse=True)
    values_hand_2.sort(reverse=True)
    # If the maximum values are different, a winner is defined.
    if values_hand_1[0] != values_hand_2[0]:
      return values_hand_1[0]>values_hand_2[0]
    # Evalute the next highest card
    elif len(values_hand_1)>1:
      return self.high_card(values_hand_1[1:], values_hand_2[1:])
    else:
      return True

# Example
poker_hand_1 = PokerHand("KS KH 5C JS TD")
poker_hand_2 = PokerHand("9C 9H 5C 5H AC")

result = poker_hand_1.compare_with(poker_hand_2)

print(result)

# Unit tests

import unittest

class PokerHandTest(unittest.TestCase):
  def test_compare_with(self):
    self.assertTrue(PokerHand("TC TH 5C 5H KH").compare_with(PokerHand("9C 9H 5C 5H AC")) == 'WIN')
    self.assertTrue(PokerHand("TS TD KC JC 7C").compare_with(PokerHand("JS JC AS KC TD")) == 'LOSS')
    self.assertTrue(PokerHand("7H 7C QC JS TS").compare_with(PokerHand("7D 7C JS TS 6D")) == 'WIN')
    self.assertTrue(PokerHand("5S 5D 8C 7S 6H").compare_with(PokerHand("7D 7S 5S 5D JS")) == 'LOSS')
    self.assertTrue(PokerHand("AS AD KD 7C 3D").compare_with(PokerHand("AD AH KD 7C 4S")) == 'LOSS')
    self.assertTrue(PokerHand("TS JS QS KS AS").compare_with(PokerHand("AC AH AS AS KS")) == 'WIN')
    self.assertTrue(PokerHand("TS JS QS KS AS").compare_with(PokerHand("TC JS QC KS AC")) == 'WIN')
    self.assertTrue(PokerHand("TS JS QS KS AS").compare_with(PokerHand("QH QS QC AS 8H")) == 'WIN')
    self.assertTrue(PokerHand("AC AH AS AS KS").compare_with(PokerHand("TC JS QC KS AC")) == 'WIN')
    self.assertTrue(PokerHand("AC AH AS AS KS").compare_with(PokerHand("QH QS QC AS 8H")) == 'WIN')
    self.assertTrue(PokerHand("TC JS QC KS AC").compare_with(PokerHand("QH QS QC AS 8H")) == 'WIN')
    self.assertTrue(PokerHand("7H 8H 9H TH JH").compare_with(PokerHand("JH JC JS JD TH")) == 'WIN')
    self.assertTrue(PokerHand("7H 8H 9H TH JH").compare_with(PokerHand("4H 5H 9H TH JH")) == 'WIN')
    self.assertTrue(PokerHand("7H 8H 9H TH JH").compare_with(PokerHand("7C 8S 9H TH JH")) == 'WIN')
    self.assertTrue(PokerHand("7H 8H 9H TH JH").compare_with(PokerHand("TS TH TD JH JD")) == 'WIN')
    self.assertTrue(PokerHand("7H 8H 9H TH JH").compare_with(PokerHand("JH JD TH TC 4C")) == 'WIN')
    self.assertTrue(PokerHand("JH JC JS JD TH").compare_with(PokerHand("4H 5H 9H TH JH")) == 'WIN')
    self.assertTrue(PokerHand("JH JC JS JD TH").compare_with(PokerHand("7C 8S 9H TH JH")) == 'WIN')
    self.assertTrue(PokerHand("JH JC JS JD TH").compare_with(PokerHand("TS TH TD JH JD")) == 'WIN')
    self.assertTrue(PokerHand("JH JC JS JD TH").compare_with(PokerHand("JH JD TH TC 4C")) == 'WIN')
    self.assertTrue(PokerHand("4H 5H 9H TH JH").compare_with(PokerHand("7C 8S 9H TH JH")) == 'WIN')
    self.assertTrue(PokerHand("4H 5H 9H TH JH").compare_with(PokerHand("TS TH TD JH JD")) == 'LOSS')
    self.assertTrue(PokerHand("4H 5H 9H TH JH").compare_with(PokerHand("JH JD TH TC 4C")) == 'WIN')
    self.assertTrue(PokerHand("7C 8S 9H TH JH").compare_with(PokerHand("TS TH TD JH JD")) == 'LOSS')
    self.assertTrue(PokerHand("7C 8S 9H TH JH").compare_with(PokerHand("JH JD TH TC 4C")) == 'WIN')
    self.assertTrue(PokerHand("TS TH TD JH JD").compare_with(PokerHand("JH JD TH TC 4C")) == 'WIN')

if __name__ == "__main__":
    unittest.main()

# If you use Jupyter Notebook
#if __name__ == '__main__':
#    unittest.main(argv=['first-arg-is-ignored'], exit=False)
