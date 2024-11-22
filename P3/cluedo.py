'''cluedo.py - project skeleton for a propositional reasoner
for the game of Clue.  Unimplemented portions have the comment "TO
BE IMPLEMENTED AS AN EXERCISE".  The reasoner does not include
knowledge of how many cards each player holds.
Originally by Todd Neller
Ported to Python by Dave Musicant
Adapted to course needs by Laura Brown

Copyright (C) 2008 Dave Musicant

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

Information about the GNU General Public License is available online at:
  http://www.gnu.org/licenses/
To receive a copy of the GNU General Public License, write to the Free
Software Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
02111-1307, USA.'''

import cnf, itertools

class Cluedo:
    suspects = ['sc', 'mu', 'wh', 'gr', 'pe', 'pl']
    weapons  = ['kn', 'cs', 're', 'ro', 'pi', 'wr']
    rooms    = ['ha', 'lo', 'di', 'ki', 'ba', 'co', 'bi', 'li', 'st']
    casefile = "cf"
    hands    = suspects + [casefile]
    cards    = suspects + weapons + rooms

    """
    Return ID for player/card pair from player/card indicies
    """
    @staticmethod
    def getIdentifierFromIndicies(hand, card):
        return hand * len(Cluedo.cards) + card + 1

    """
    Return ID for player/card pair from player/card names
    """
    @staticmethod
    def getIdentifierFromNames(hand, card):
        return Cluedo.getIdentifierFromIndicies(Cluedo.hands.index(hand), Cluedo.cards.index(card))


# **************
#  Question 6 
# **************
def deal(hand, cards):
    "Construct the CNF clauses for the given cards being in the specified hand"
    "*** YOUR CODE HERE ***"
    res = [[Cluedo.getIdentifierFromNames(hand, c)] for c in cards]
    return res


# **************
#  Question 7 
# **************
def axiom_card_exists():
    """
    Construct the CNF clauses which represents:
        'Each card is in at least one place'
    """
    "*** YOUR CODE HERE ***"
    res = [[Cluedo.getIdentifierFromNames(h, c) for h in Cluedo.hands] for c in Cluedo.cards]
    return res


# **************
#  Question 7 
# **************
def axiom_card_unique():
    """
    Construct the CNF clauses which represents:
        'If a card is in one place, it can not be in another place'
    """
    "*** YOUR CODE HERE ***"
    card_list = []
    for lst in axiom_card_exists():
        neg_list = [-card for card in lst]
        neg_combs = itertools.combinations(neg_list, 2)
        conj = [list(nc) for nc in neg_combs]
        card_list.append(conj)
    res = [card for cards in card_list for card in cards]
    return res


# **************
#  Question 7 
# **************
def axiom_casefile_exists():
    """
    Construct the CNF clauses which represents:
        'At least one card of each category is in the case file'
    """
    "*** YOUR CODE HERE ***"
    categories = [Cluedo.suspects, Cluedo.weapons, Cluedo.rooms]
    return [[Cluedo.getIdentifierFromNames(Cluedo.casefile, item) for item in category] for category in categories]


# **************
#  Question 7 
# **************
def axiom_casefile_unique():
    """
    Construct the CNF clauses which represents:
        'No two cards in each category are in the case file'
    """
    "*** YOUR CODE HERE ***"
    categories = [Cluedo.suspects, Cluedo.weapons, Cluedo.rooms]
    neg_combs = []

    for category in categories:
        identifiers = [Cluedo.getIdentifierFromNames(Cluedo.casefile, item) for item in category]
        neg = [-identifier for identifier in identifiers]
        neg_combs.extend(list(itertools.combinations(neg, 2)))

    return neg_combs


# **************
#  Question 8 
# **************
def suggest(suggester, card1, card2, card3, refuter, cardShown):
    "Construct the CNF clauses representing facts and/or clauses learned from a suggestion"
    "*** YOUR CODE HERE ***"
    # Determine the list of suspects between suggester and refuter or all except suggester
    if refuter:
        start = Cluedo.suspects.index(suggester) + 1
        end = Cluedo.suspects.index(refuter)
        mid = Cluedo.suspects[start:end]
    else:
        mid = [s for s in Cluedo.suspects if s != suggester]

    # Generate CNF clauses stating that these suspects do not have the cards
    cnf_clauses = []
    for card in (card1, card2, card3):
        cnf_clauses.extend([[-Cluedo.getIdentifierFromNames(suspect, card)] for suspect in mid])

    # Handle the cases where the refuter is known
    if refuter:
        if cardShown:
            # If a card is shown, directly specify it
            cnf_clauses.append([Cluedo.getIdentifierFromNames(refuter, cardShown)])
        else:
            # If no card is shown, any of the three could have been shown
            cnf_clauses.append([Cluedo.getIdentifierFromNames(refuter, card) for card in (card1, card2, card3)])

    return cnf_clauses

# **************
#  Question 9 
# **************
def accuse(accuser, card1, card2, card3, correct):
    "Construct the CNF clauses representing facts and/or clauses learned from an accusation"
    "*** YOUR CODE HERE ***"
    card_list = [card1, card2, card3]
    if correct:
        return [[Cluedo.getIdentifierFromNames(Cluedo.casefile, card)] for card in card_list]
    else:
        a = [[-Cluedo.getIdentifierFromNames(Cluedo.casefile, card) for card in card_list]]
        b = [[-Cluedo.getIdentifierFromNames(accuser, card)] for card in card_list]
        return a + b

