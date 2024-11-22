# submission.py
# ----------------
# Attribution Information: This part of the project was adapted from CS221 and 
# the PacMan Projects. 
# For the PacMan Projects: 
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
# 08-2020
 

from __future__ import print_function
import math 
import collections
import shop


############################################################
# Question 1 - addition 

def add(a, b): 
    "Return the sum of a and b"
    "*** YOUR CODE HERE ***"
    # BEGIN_YOUR_CODE 
    return a + b
    # END_YOUR_CODE


############################################################
# Question 2 - buyLotsOfFruit 
fruitPrices = {'apples':2.00, 'oranges': 1.50, 'pears': 1.75,
                'limes':0.75, 'strawberries':1.00}

def buyLotsOfFruit(orderList):
    """
        orderList: List of (fruit, numPounds) tuples

    Returns cost of order. If some fruit is not in list, print an error 
    message and return None.
    """
    totalCost = 0.0
    "*** YOUR CODE HERE ***"
    # BEGIN_YOUR_CODE
    # iterate the orderlist, check the inventory
    for order in orderList:
        fruitName = order[0]
        fruitWeight = order[1]
        # not available in inventory
        if fruitName not in fruitPrices:
            print("Sorry we do not have %s", fruitName)
            return None
        else:
            totalCost += fruitWeight * fruitPrices[fruitName]
    return totalCost
    # END_YOUR_CODE


############################################################
# Question 3 - shopSmart 

def shopSmart(orderList, fruitShops):
    """
        orderList: List of (fruit, numPound) tuples
        fruitShops: List of FruitShops

    Return the FruitShop where your order costs the least.
    """
    "*** YOUR CODE HERE ***"
    # BEGIN_YOUR_CODE
    costList = []
    for shop in fruitShops:
        # save prices from each shops in a list
        costList.append(shop.getPriceOfOrder(orderList))
    # find the cheapest price shop
    return fruitShops[costList.index(min(costList))]
    # END_YOUR_CODE


############################################################
# Question 4 - findAlphabetLastWord 

def findAlphabetLastWord(text):
    """
    Given a string |text|, return the word in |text| that comes last
    alphabetically (that is, the word that would appear last in a dictionary).
    A word is defined by a maximal sequence of characters without whitespaces.
    You might find max() and list comprehensions handy here.
    """
    "*** YOUR CODE HERE ***"
    # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
    # text will be turn to a word list by split function
    # max() find the last alphabetically word
    return max(text.split(' '))
    # END_YOUR_CODE


############################################################
# Question 5 - euclideanDistance 

def euclideanDistance(loc1, loc2):
    """
    Return the Euclidean distance between two locations, where the locations
    are pairs of numbers (e.g., (3, 5)).
    """
    "*** YOUR CODE HERE ***"
    # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
    return math.sqrt((loc2[1]-loc1[1])**2 + (loc2[0]-loc1[0])**2)
    # END_YOUR_CODE


############################################################
# Question 6 - findSingletonWords

def findSingletonWords(text):
    """
    Splits the string |text| by whitespace and returns the set of words that
    occur exactly once.
    If no singleton words exist return the emptyset.
    """
    "*** YOUR CODE HERE ***"
    # BEGIN_YOUR_CODE (our solution is 4 lines of code, but don't worry if you deviate from this)
    dic = {}
    for word in text.split(' '):
        if word in dic:
            dic[word] += 1
        else:
            dic[word] = 1
    dic = {k: v for k, v in dic.items() if v == 1}
    return set(dic)
    # END_YOUR_CODE


############################################################
# Question 7 - lenLongestPalindrome

def lenLongestPalindrome(text): 
    """
    A palindrome is a string that is equal to its reverse (e.g., 'ana'). 
    Computer the length of the longest palindrome that can be obtained by 
    deleting letters from text. 
    Do not try a brute force approach on this function.  Your algorithm should 
    run in O(len(text)^2) time. 
    Consider defining a recurrence before you begin coding. 
    """
    "*** YOUR CODE HERE ***"
    # BEGIN_YOUR_CODE 
    length = len(text)
        
    if length == 0:
        return 0
    
    # dp[x][y] means the length of panlindrome from x to y
    dp = [[0] * length for _ in range(length)]
    # single letter's length is 1
    for i in range(0, length):
        dp[i][i] = 1 

    # iterate all the panlindromes in different length, from 2
    for n in range(2, length + 1): 
        for i in range(0, length - n + 1): # the start position from 0 to i
            j = i + n - 1 # j is the end position when the substring start from i
            # judge if the start letter is equal to the end letter:
            if text[i] == text[j]:
                # when they are adjacent the length is 2, else plus 2
                dp[i][j] = dp[i + 1][j - 1] + 2 if i + 1 <= j - 1 else 2
            else:
                #choose the longest substring between statr letter and end letter
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])

    return dp[0][length - 1]
    #END_YOUR_CODE    


############################################################
#  Extra Functions you may want to define