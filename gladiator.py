#!/usr/bin/python3
#Mark Nesbitt
#Praetorian API testing
#Current tasks: error handling from unexpected API responses.  Command line args to give user specific control.  Ability to step through rounds
import requests, json, sys
import random
import time

def getHeaders(useremail):
    email = useremail
    r = requests.post('https://mastermind.praetorian.com/api-auth-token/', data={'email':email})
    headers = r.json()
    headers['Content-Type'] = 'application/json'
    return headers

def randomGuess(colors, slots): #This is a ditch attempt at solving level 4.  I need a guess generation algo that runs faster...
    result = []
    for i in range(slots):
        result.append(random.randint(0,colors))
    if(len(result) != len(set(result))):
        return randomGuess(colors,slots)
    else:
        return result

def generateGuess(guesses, colors, slots, history):
    starttime = time.time()
    if history == []:
        guess = list(range(slots)) #formerly no if statement and just restarted cycle each time, but runtime cause API timeout
    else:
        prevround = history[-1]
        prevguess = prevround[0]
        guess = incrementGuess(prevguess, colors) 
        print(guess)
    i=0
    while i < colors**slots: #checking that the candidate guess isn't dumb.  The colors**slots is the old logic where duplicate colors were allowed
        goodguess = True
        if(len(guess) != len(set(guess))): #no dupes allowed
            guess = incrementGuess(guess, colors)
            continue
        elapsedtime = time.time() - starttime
        if elapsedtime > 9.5: #ditch attempt at solving level 4 while still using a slow AF guess generation algo.  One way to solve this more quickly without having a super smart algo would be just to spot guesses where 0 colors were correct, then never cycle through those.
            #return guess
            return randomGuess(colors, slots) 
        for item in history:
            if(guess == item[0]): #If candidate guess was guessed before, its dumb
                goodguess = False
                #print("line 25 knockout")
                break
            if(gradeguess(guess, colors, slots, item[0]) != item[1]):
                goodguess = False
                #print("line 29 knockout")
                #print(gradeguess(guess, colors, slots, item[0]), item[1])
                break
        if goodguess:
            return guess
        else:
            guess = incrementGuess(guess, colors)
        i = i+1
    print("Never found a good guess -- WTF??")

def incrementGuess(guess, numcolors): 
    flippedguess = list(reversed(guess))
    i=0
    for number in reversed(guess):
        if number != numcolors - 1:
            flippedguess[i] = number + 1
            return list(reversed(flippedguess))
        else:
            flippedguess[i] = 0
            if i == len(flippedguess)-1:
                return list(reversed(flippedguess))
        i = i+1

def gradeguess(code, colors, slots, guess): 
    blackpegs = 0
    whitepegs = 0
    i = 0

    tempCode = code[:] #haha pointers...
    tempGuess = guess[:]
    while i < slots:
        if(tempCode[i] == tempGuess[i]):
            blackpegs +=1
            tempCode[i] = 'xb'
            tempGuess[i] = 'xb'
        i+=1
    i = 0
    while i < slots:
        if(tempGuess[i] =='xb'):
            i+=1
            continue
        k = 0
        while k < slots:
            if(tempGuess[i] == tempCode[k]):
                whitepegs +=1
                tempGuess[i] = 'xw'
                tempCode[k] = 'xw'
                break
            k+=1
        i+=1
    return [blackpegs+whitepegs, blackpegs] #had this reversed before... also their definition of white pegs is different from mine

def solveRound(roundnum,headers):
    thisRound = str(roundnum)
    print("Solving round %s" %thisRound)
    r = requests.get('https://mastermind.praetorian.com/level/'+thisRound+'/', headers=headers)
    print(r.text)
    roundparams = r.json()
    slots = roundparams['numGladiators']
    guesses = roundparams['numGuesses']
    colors = roundparams['numWeapons']
    print("Round params:")
    print("Slots: %s, Colors: %s, Guesses: %s" %(slots, colors, guesses))
    history = []
    score = [0,0]
    while score[1] != slots:
        guess = generateGuess(guesses, colors, slots, history)
        print("Trying guess:")
        print(guess)
        r = requests.post('https://mastermind.praetorian.com/level/'+thisRound+'/', data = json.dumps({'guess':guess}), headers = headers)
        #print(r.text)
        response = r.json()
        #print(response)
        #NEED A WAY TO HANDLE UNEXPECTED API RESPONSES
        
        if 'error' in response:
            print(response)
            sys.exit(1)
        if 'response' not in response: #indicates the guess was correct
            #print(response, r.text)
            print("Successful guess! (in solveRound())")
            return response
        else:
            score = response['response']  #this is a list of ints
    
        temp = []
        temp.append(guess)
        temp.append(score)
        history.append(temp)
        print(history)

def main():
    headers = getHeaders("mwnesbitt@gmail.com")
    if len(sys.argv) == 2:
        if sys.argv[1] == "reset":
            r = requests.post('https://mastermind.praetorian.com/reset/', headers=headers)
            print(r.text)
    else: 
        i = 1;
        while i < 7:
            tempresult = solveRound(i, headers)
            print(tempresult, "(in main)")
            print("Just solved level %d (in main)" %i)
            print(tempresult['message'], "(in main)")
            i+=1
            if not tempresult['message'] == "Onto the next level":
                break

if __name__ == '__main__':
    main()
