import Quordle_Simulation as sim        # Simulation funcitons
import random                           # Random Guessing
from time import time                   # Timing the Games
from tqdm import trange                 # Progress bar
    
with open('solutions.txt') as f:        # Get the solutions
    solution = f.readline().split(" ")

with open('allowed.txt') as f:          # Get the allowed guesses
    allowed = f.readline().split(" ")
    
solution = solution[1:-1]               # Get rid of white space
allowed = allowed[1:-1]

# Allowed doesn't contain any solutions, so the full set of allowed words is allowed+solutions
allowed += solution                     # Concatenate lists

# MAX OCCURRENCE OF LETTER IN A WORD IS 3

# Simulate a number of random games, guessing randomly from allowed words
# If starting is not empty, the simulation will first guess the words defined in starting
def randSolveSim(epochs = 10, starting = []): 
    
    avgSolTime = 0                                      # Average time (in secs) for a game
    avgSteps = [0, 0, 0, 0]                             # Average number of steps in which each solution was found
    for epoch in trange(epochs):                        # For each epoch
        sim.init()                                      #   Create a new random game
        startTime = time()                              #   Save the start time

        ald = [allowed.copy() for i in range(4)]        # All words are allowed initially
        resp = ["","","",""]                            # No response has been given yet
        idx = 1                                         # Index for guess number
        solTime = [-1,-1,-1,-1]                         # Number of steps for this epoch

        for g in starting:                              # Go through any words defined in starting
            resp = sim.guess(g)                         #   Get the response for those words
            ald = sim.reduce(g, resp, ald)              #   Reduce the words we're allowed to guess
            for i in range(4):                          #   For each response
                if resp[i] == "GGGGG":                  #   If any words are solved
                    solTime[i] = idx                    #       Update that word's solution time
            idx += 1                                    #   Move to the next guess
        
        for i in range(4):                              # Guess one word at a time
            while resp[i] != "GGGGG" and solTime[i]<0:  #   While we haven't found a solution
                g = ald[i][random.randint(0, (len(ald[i])-1))] # Get a random allowed guess
                resp = sim.guess(g)                     #        Make that guess and get a response
                ald = sim.reduce(g, resp, ald)          #   Update the allowed array
                idx += 1                                #   Move to the next guess
            solTime[i] = idx-1                          #   Update this word's solution time when we have solved it
            
        avgSolTime += (time()-startTime)/epochs         # Update the average solultion time
        for i in range(4):
            avgSteps[i] += solTime[i]/epochs            # Update each average step
    
    print('Avg Time: ',avgSolTime)                      # Print metrics after simultion completes
    print('Avg Steps:',avgSteps)
    print('Overall Avg:', (avgSteps[0]+avgSteps[1]+avgSteps[2]+avgSteps[3])/4)


# Play one game, guessing one word at a time and guessing randomly from allowed words
# If starting is not empty, the simulation will first guess the words defined in starting
# If solution is not empty, the game will be set to that solution and not a random solution
# This is the same as randSolveSim ran with 1 epoch with the exception of print statements
#   so I will not comment this function
def randSolveSingleGame(starting = [], solution = []):
    
    sim.init()
    if len(solution) == 4:
        sim.currSol = solution
    else:
        print('Using random game')
    
    print("----- :",sim.currSol)
    print()
    startTime = time()

    ald = [allowed.copy() for i in range(4)]
    resp = ["","","",""]
    idx = 1
    solTime = [-1,-1,-1,-1]

    for g in starting:
        resp = sim.guess(g)
        print(g,":",resp)
        ald = sim.reduce(g, resp, ald)
        for i in range(4):
            if resp[i] == "GGGGG":
                solTime[i] = idx
        idx += 1
        #print([len(ald[0]), len(ald[1]), len(ald[2]), len(ald[3])]) # Debug (number of words still allowed)
    
    for i in range(4):
        while(resp[i] != "GGGGG") and solTime[i]<0:
            g = ald[i][random.randint(0, (len(ald[i])-1))]
            resp = sim.guess(g)
            print(g,":",resp)
            ald = sim.reduce(g, resp, ald)
            #print([len(ald[0]), len(ald[1]), len(ald[2]), len(ald[3])]) # Debug (number of words still allowed)
            idx += 1
            
        if solTime[i] < 0:
            solTime[i] = idx-1
        
    print('Time: ',(time()-startTime))
    print('Steps:',solTime)


# Simulate a number of random games, guessing randomly from allowed words
# Guess a word if there is one allowed word for that solution
# If starting is not empty, the simulation will first guess the words defined in starting
def randSim_v2(epochs = 10, starting = []): 
    
    avgSolTime = 0                                      # Average time (in secs) for a game
    avgSteps = [0, 0, 0, 0]                             # Average number of steps in which each solution was found
    for epoch in trange(epochs):                        # For each epoch
        sim.init()                                      #   Create a new random game
        startTime = time()                              #   Save the start time

        ald = [allowed.copy() for i in range(4)]        # All words are allowed initially
        resp = ["","","",""]                            # No response has been given yet
        idx = 1                                         # Index for guess number
        solTime = [-1,-1,-1,-1]                         # Number of steps for this epoch

        for g in starting:                              # Go through any words defined in starting
            resp = sim.guess(g)                         #   Get the response for those words
            ald = sim.reduce(g, resp, ald)              #   Reduce the words we're allowed to guess
            for i in range(4):                          #   For each response
                if resp[i] == "GGGGG":                  #   If any words are solved
                    solTime[i] = idx                    #       Update that word's solution time
            idx += 1                                    #   Move to the next guess
        
        inc = [0,1,2,3]                                 # Incomplete Indices
        while len(inc) > 0:                             # While we haven't solved everything
            for i in inc:                               # For each incomplete index
                if len(ald[i]) == 1:                    #   If there is only one allowed solution
                    g = ald[i][0]                       #       Guess it
                    resp = sim.guess(g)                 #       Get the Response
                    ald = sim.reduce(g, resp, ald)      #       Update ald
                    solTime[i] = idx                    #       Mark it as solved
                    inc.remove(i)                       #       Remove the index from incomplete
                    idx += 1                            #       Move to the next guess
            if len(inc) == 0:                           # If we're done
                break                                   #   Break
            
            g = ald[inc[0]][random.randint(0, (len(ald[inc[0]])-1))] # Pick a guess from an incomplete index
            resp = sim.guess(g)                         # Get the response
            ald = sim.reduce(g, resp, ald)              # Update ald
            
            for i in inc:
                if resp[i] == "GGGGG":                  # If we have found the answer for this index
                    solTime[i] = idx                    #     Mark it as solved
                    inc.remove(i)                       #     Remove it from incomplete
            idx += 1                                    # Move to the next guess
                        
        avgSolTime += (time()-startTime)/epochs         # Update the average solultion time
        for i in range(4):
            avgSteps[i] += solTime[i]/epochs            # Update each average step
    
    print('Avg Time: ',avgSolTime)                      # Print metrics after simultion completes
    print('Avg Steps:',avgSteps)
    print('Overall Avg:', (avgSteps[0]+avgSteps[1]+avgSteps[2]+avgSteps[3])/4)


st = ["CRATE", "SPOIL", "BUNDY"]
sol = ["SPOIL", "CRATE", "PLANE", "STREP"]
randSolveSim()
print()
randSim_v2()
print()
randSolveSingleGame()

#randSolveSingleGame(starting=st, solution=sol)



