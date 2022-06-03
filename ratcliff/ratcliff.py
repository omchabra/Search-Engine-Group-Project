def ratcliff(s1, s2):
    s1 = s1.upper()
    s2 = s2.upper()

    return 2*float(getMatching(s1, s2))/(len(s1) + len(s2))

def getMatching(s1, s2):
    #print("in:", s1, s2)
    leng, start1, start2 = findLongestSub(s1, s2)    
    #print("match: ", s1[start1: start1+ leng])

    if (leng == 0):
        return 0

    return leng + getMatching(s1[0: start1], s2[0: start2]) + getMatching(s1[start1 + leng:], s2[start2 + leng:])


def findLongestSub(s1, s2):
    longestLen = 0
    startingIndS1 = 0
    startingIndS2 = 0
    
    for ind1 in range(0, len(s1)):

       firstIndex = s1[ind1]
       secondStart = 0
       longestSub = 0
       
       for ind2 in range(0, len(s2)):
           secondIndex = s2[ind2]
    
           if (secondIndex == firstIndex):
               currentSubLen = 0
               
               maxString = min(len(s2) - ind2, len(s1) - ind1)

               for ind3 in range(0, maxString):
                   if (s2[ind2 + ind3] == s1[ind1 + ind3]):
                       currentSubLen += 1
                   else:
                       break

               if currentSubLen > longestSub:
                  longestSub = currentSubLen
                  secondStart = ind2
                  
       if longestSub > longestLen:
           startingIndS1 = ind1
           startingIndS2 = secondStart
           longestLen = longestSub

    return longestLen, startingIndS1, startingIndS2

print(ratcliff("GESTALT PATTERN MATCHING", "GESTALT PRACTICE"))
