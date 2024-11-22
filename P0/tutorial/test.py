import shop
import submission

def test3g(numChars, length): 
	import random 
	random.seed(42) 
	text = ''.join(chr(random.randint(ord('a'), ord('a') + numChars - 1)) for _ in range(length))
	return text

def test3f(numTokens, numTypes):
    import random
    random.seed(4811)
    text = ' '.join(str(random.randint(0, numTypes)) for _ in range(numTokens))
    return text

def main():
    #text = test3g(10,30)
    #text = "character"
    #text = ""
    #text = test3g(10,30)
    #ans = submission.lenLongestPalindrome(text)
    text = "It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a wife. However little known the feelings or views of such a man may be on his first entering a neighbourhood, this truth is so well fixed in the minds of the surrounding families, that he is considered as the rightful property of some one or other of their daughters."
    text = test3f(500,100)
    print(text)
    sw = submission.findSingletonWords(text)
    if type(sw) is set: 
        l = sorted(sw)
    else:
        l = "Error: not a set"
    print(l)

if __name__ == "__main__":
    main()


class test:
    
    text = ''
    def __init__(self) -> None:
         #text = test3g(10,30)
         #ans = self.testMethod2(text)
         #print(ans)
         pass
    
    def lenLongestPalindrome(self, text): 
        
        text = 'character'
        palindrome = []
        length = 1
        strLen = len(text)
        left = ""
        right = ""
        for i in range(0, strLen):
            tempLength = 0
            for j in range(i, strLen):
                left = text[i]
                right = text[j]
                if left == right:
                    # tempLength = tempLength + 1
                    if i != j:
                        palindrome.insert(0, left)
                        palindrome.append(right)
                    else:
                        palindrome.append(left)
                    #tempLength = j - i + 1
                    if i != 0:
                        i = i - 1
                    else:
                        break
                    #if i == 0: break
                    #else: i = i - 1
                elif (j > 1 and i < strLen) and (left == text[j-1] or text[i+1] == right):
                    #tempLength += 1
                    palindrome.insert(0, left)
                else:
                    #length = j - i + 1
                    break
            if len(palindrome) > length:
                length = len(palindrome)
        print(length)
        return length

    def testMethod(self, text):
        text = 'abcdefggghijkl'
        #text = 'character'
        ansList = []
        listL = []
        listR = []
        for i in range(0, len(text)):
            if i == 6:
                print('hello')
            tempPalindrome = []
            listL = list(reversed(text[0:i+1]))
            listR = list(text[i+1:])
            indL = 0
            #ansList.append(listL[0])
            for j in range(0, len(listL)):
                if listL[indL] in listR:
                    indR = listR.index(listL[indL])
                    if j == 0 and (indL != 0 or indR != 0):
                        tempPalindrome.append(listL[0] if indL == 0 else listR[0])
                    elif indL == 0 and indR == 0 and j == 0:
                        tempPalindrome.append(listL[0])
                    #else:
                    tempPalindrome.append(listR[indR])
                    tempPalindrome.insert(0, listL[indL])
                    if indR + 1 == len(indR):
                        break
                    listR = listR[indR+1:]
                else:
                    indL += 1
            if len(tempPalindrome) > len(ansList):
                ansList = tempPalindrome
        if len(ansList) == 0:
            ansList.append(text[0])
        print(list(text))
        print(ansList)
        print(len(ansList))
        return len(ansList)
    
    def testMethod2(self, text):
        
        length = len(text)
        dp = [[0] * length for _ in range(length)]

        for i in range(0, length):
            dp[i][i] = 1 # dp[x][y] means the length of panlindrome from x to y

        for n in range(2, length + 1): # to find all the panlindrome with length > 1
            for i in range(0, length - n + 1): # the start position from 0
                j = i + n - 1 # the end position of start from i
                if text[i] == text[j]: # if the start equal the end:
                    dp[i][j] = dp[i + 1][j - 1] + 2 if i + 1 <= j - 1 else 2 # length add 2, if they are connected, length is 2
                else:
                    dp[i][j] = max(dp[i + 1][j], dp[i][j - 1]) # if the start is not equal end, the max is  

        return dp[0][n - 1]
