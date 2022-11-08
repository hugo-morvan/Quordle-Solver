import random  # For Random Initialization

global currSol # currSol needs to be accessed everywhere
currSol = [-1, -1, -1, -1]

def init(): # Initialize a new random game
    
    solution = []   # List of legal solutions
    
    with open('solutions.txt') as f: # Read the solutions in from the file containing legal solutions
        solution = f.readline().split(" ")
        
    solution = solution[1:-1] # The resulting list has a blank space at the beginnning and end, so get rid of them

    idx = []                                                    # list for used indices
    for i in range(4):                                          # pick four random words
        curr = random.randint(0, len(solution)-1)                     # get a random index
        while curr in idx:                                          # if it's already been used, pick a different one
            curr = random.randint(0, len(solution)-1)
        idx.append(curr)                                            # mark the index as used
        currSol[i] = solution[curr]                              # use the chosen index from the legal solutions
    
# Responses:
#   G: (Green)  The corresponding letter is in the solution and in the correct place
#   Y: (Yellow) The corresponding letter is in the solution and in the wrong place
#   R: (Grey)   The corresponding letter is not in the solution
#
#   Ex: Solution: TARES | Guess: CARET | Response: RGGGY
#
#
# If there are n occurrences of a letter in the solution, the first n responses will be either G or Y and subsequent responses will be R
#
#   Ex: Solution: TARES | Guess: ATTIC | Response: YYRRR


def guess(s): # Make a guess; returns a list of length 4 containing the responses as described above
    s = s.upper()                                           # Force the guess into upper case

    thisFMap= [[],[],[],[]]                                 # Frequency Lists (reffered to as Maps) for Multiple-Occurence Labeling
    
    for i in range(ord('A'), ord('Z')+1):                   # A loop from the ASCII value of 'A' to the ASCII value of 'Z'
        for j in range(4):                                  #   For each list in the Frequency Map
            thisFMap[j].append(0)                           #       Add another 0 (to end up with 26 0's)

    for i in range(4):                                      # For Each Solution
        for c in currSol[i]:                                #   For Each Character in the Solution
            thisFMap[i][ord(c)-ord('A')] += 1               #       Increment the appropriate place in the list 
    
    ret = []                                                # List for Returning
    for i in range(4):                                      # For Each Solution
        out = ["","","","",""]                              #   List of length 5 for each response
        for c in range(5):                                  #   For each index in [0..4]
            if s[c] == currSol[i][c]:                       #       If the letter is correct and in the right place
                out[c] = 'G'                                #           The response is G
                thisFMap[i][ord(s[c])-ord('A')] -= 1        #           Update the frequency list
        for c in range(5):                                  #   Go through all the indices again
            if out[c] == "":                                #       If a G response hasn't already been given,
                if thisFMap[i][ord(s[c])-ord('A')] > 0:     #           If we haven't reached the frequency yet for this letter
                    out[c] = 'Y'                            #               The response is Y
                    thisFMap[i][ord(s[c])-ord('A')] -= 1    #               We have one less occurrence of this letter allowed
                else:                                       #           If there are no more occurrences of the letter allowed
                    out[c] = 'R'                            #               The response is R
        
        outStr = ""                                         # Turn the response list into a string
        for c in out:                                       # For every character in the response
            outStr += c                                     #   Append to the string
        ret.append(outStr)                                  # Add this string to the list of responses
    return ret                                              # Return the responses


def reduce(g, resp, ald): #reduce allowed lists (ald) based on the response (resp) from guess g

    for i in range(len(ald)):                       # For every set of allowed words
        r = resp[i]                                 # Get the latest response for that set
        
        m = []                                      # Initialize an empty frequency list
        cap = []                                    # Initialize capacity boolean list
        for a in range(ord('A'), ord('Z')+1):       # Loop of length 26
            m.append(0)                             #   Add a 0 to the frequency list
            cap.append(False)                       #   Add False to the capacity list
            
        for c in range(5):                          # for every character in the response
            rm = []                                 # Initialize a list of words to remove
            
            if r[c] == 'G':                         # Green Response
                m[ord(g[c])-ord('A')] += 1          #    increment freq for this character
                for s in ald[i]:                    #    for every allowed word
                    if s[c] != g[c]:                #    if this character doesn't match
                        rm.append(s)                #       remove this word
                    
            elif r[c] == 'R':                       # Grey Response
                cap[ord(g[c])-ord('A')] = True      #   This character frequency is capped (will look at it later)
                
            else:                                   # Yellow Response
                m[ord(g[c])-ord('A')] += 1          #   increment freq for this character
                for s in ald[i]:                    #   For every allowed word...
                    if g[c] == s[c]:                #       If the character at this location matches the guess
                        rm.append(s)                #           Remove it (Yellow means char is in a different spot)

            for s in rm:                            # Execute the removals thus far
                ald[i].remove(s)
        rm = []                                     # Clear the removal array
        
        for s in ald[i]:                            # For every currently allowed response
            currM = m.copy()                        #   Make a copy of the frequency map based on information received
            for c in s:                             #   For every character in the word
                currM[ord(c)-ord('A')] -= 1         #       Decrease the frequency map by one
            for n in range(len(m)):                 #   For each character frequency
                if currM[n]>0 or (currM[n]<0 and cap[n]): # If the current word has too little or too many of a letter
                    rm.append(s)                    #           remove it
                    break                           #           stop checking this word

        for s in rm:                                # Execute the rest of the removals
            ald[i].remove(s)
            
    return ald                                      # Return the allowed array

'''
########## DEBUG ############
init()
print('----- :',currSol)
ret = guess(currSol[0])
print(currSol[0],":",ret)
reduce(currSol[0], guess(currSol[0]), [[],[],[],[]])
'''