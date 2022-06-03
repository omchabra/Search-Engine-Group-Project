import numpy, heapq


def levDist(s1, s2):
    s1 = s1.upper()
    s2 = s2.upper()

    size1 = len(s1)
    size2 = len(s2)

    mat = [ [0 for x in range(size1)] for y in range(size2)]
    
    full = False
    diagInd = 0;
    while (not full):
        full = True
        for pnt in range(diagInd + 1):
            yInd = diagInd - pnt;
            xInd = pnt

            if (xInd > size1 - 1 or yInd > size2 - 1):
                continue
            else:
                full = False
                
            if ( (xInd == 0 or yInd == 0) and (s1[xInd] != s2[yInd]) ):
                mat[yInd][xInd] = max( (xInd, yInd) ) + 1;
            else:
                #addOn = -1
                if s1[xInd] == s2[yInd]:
                    addOn = 0
                else:
                    addOn = 1
                mat[yInd][xInd] = min( (mat[yInd-1][xInd] + 1, mat[yInd][xInd-1] + 1, mat[yInd-1][xInd-1] + addOn) )
        diagInd += 1
    # print(mat)
    return mat[-1][-1]



def generateEdits(query, word_dictionary, limit = 3 ):
    wordList = []
    for word in word_dictionary:
        if not word:
            continue
        distance = levDist(query, word)
        heapq.heappush(wordList, (distance, word))

    
    best = heapq.nsmallest(limit, wordList, key = lambda x : x[0])
    # print(wordList)

    return [x[1] for x in best]

    
print(levDist('hi', 'hello'))
