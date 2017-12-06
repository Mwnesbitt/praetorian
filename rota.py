#!/usr/bin/python3
#Mark Nesbitt

#Crappy data structures:
#move: (piece, destination) 
#gamestate: len = 2 array, position 0 is either '' or 'W' or 'B' which is what is in the middle.  Position 1 is a list of len 8 with '', 'W', or 'B' in each of the positions such that '' is in 3 positions, W in 3, and B and 3. 

#keeping track of things and dealing with pointers is getting cumbersome and spaghettifying the code.  While I believe that breakdown in responsibilities between the functions is probably correct, the code should be changed to implement the moves and gamestate as classes and pass around object to update the game. 
#Pass "player" around into these -- don't make yourself have to determine the player based on the move and also it's important for when its a new checker joining the board

import random

class Move(object): #check that move is legal?
    def __init__(self, player, origin, destination):
        self.origin = origin
        self.destination = destination
        self.player = player

class Game(object):
    def __init__(self, player, center, looppositions):
        self.player = player
        self.center = center
        self.loop = looppositions

    def allCheckers():
        if self.center == '':
            if looppositions.count('') == 2: return True
            else: return False
        else:
            if looppositions.count('') == 3: return True
            else: return False

#need to adapt isblunder, makemove
#add isLegal(gameobject, move)-- just check that move is in legalMoves(gameobject)
#make sure you can easily play the game from the interpreter
#change islegal and legalmoves to be functions inside of gameobject.  Should most of these functions be put inside the classes?
def isLegal(gameobject, moveobject)
    result = False
    if gameobject.player != moveobject.player: return False
    for move in TisLegal(gameobject):
        if moveobject.origin == move.origin and moveobject.destination == move.destination:
            result = True
    return result

def TupdateGame(gameobject, moveobject, player): #need more internal checks and how to handle redundancy (i.e. player is already in gameobject and move, so how should that be handled?  Should minimize duplication-- perhaps player gets pulled out of gameobject and there's a check that the move requested makes sense given the state of the game.
    #assumes move is legal, for now
    gamecenter = gameobject.center 
    gamelooppositions = gameobject.loop 
    if moveobject.origin == 'new' and moveobject.destination == 'center': gamecenter = player
    if moveobject.origin == 'new' and isinstance(moveobject.destination, int): gamelooppositions[moveobject.destination] = player
    if moveobject.origin == 'center':
        gamecenter = ''
        gamelooppositions[moveobject.destination] = player
    elif moveobject.destination == 'center':
        gamecenter = player
        gamelooppositions[moveobject.destination] = ''
    else:
        gamelooppositions[moveobject.destination] = player
        gamelooppositions[moveobject.origin] = ''
    result = Game(otherplayer(player), gamecenter, gamelooppositions)
    return result

def otherPlayer(player):
    if player == 'W': return 'B'
    else: return 'W'

def TisWon(gameobject, player):
    for index, spot in enumerate(gameobject.loop):
        if spot == player and spot == loop[index-1] and item == loop[index-2]:
            return True
        if spot == player and spot == gameobject.center and spot == loop[index-4]:
            return True
    return False

def TlegalMoves(gameobject, player): 
    movelist = []
    if gameobject.allCheckers(): #game is underway
        for index, checker in enumerate(gameobject.loop):
            if checker == player:
                if gameobject.center == '':
                    movelist.append(Move(player,index, 'center'))
                if gameobject.loop[(index+1)%8] == '':
                    movelist.append(Move(player, index, (index+1)%8))
                if gameobject.loop[(index-1)%8] == '':
                    movelist.append(Move(player,index, (index-1)%8))
        if gameobject.center == player:
            openspots = [i for i,x in enumerate(gameobject.loop) if x == '']
            for spot in openspots:
                movelist.append(Move(player,'center', spot))
    else: #checkers are still being placed
        if gameobject.center == '': movelist.append(Move(player,'new', 'center'))
        loopoptions = [i for i,x, in enumerate(gameobject.loop) if x =='']
        for spot in options: movelist.append(Move(player,'center', spot))
    return movelist

def makeMove(gamestate, player): #need to update how to handle when new moves have to be made
    #BUG: makeMove(['',['W','','B','W','B','W','B','']], 'W')
    #generate list of candidate moves
    candidates = legalMoves(gamestate, player)
    #print("candidates", candidates)
    if len(candidates) == 1: return candidates[0]

    #check for winning moves.  return it if found
    for move in candidates:
        if isWon(updateGame(gamestate, move),player): return move

    #eliminate moves that allow opponent to win on next turn
    newcandidates = []
    for move in candidates:
        if isBlunder(gamestate, move):
            pass
        else:
            newcandidates.append(move)
    if len(newcandidates) == 1: return newcandidates[0]
    if len(newcandidates) == 0: return candidates[0] #we got trapped
    #print("newcandidates", newcandidates)

    """
    I think the blunder section covers failing to make defensive moves
    forcedmoves = []
    for move in newcandidates:
        if isForced(gamestate, move):
            forcedmoves.append(move)
    if len(forcedmoves) == 1: return forcedmoves[0]
    elif len(forcedmoves) > 1: finalcandidates = forcedmoves
    else: finalcandidates = newcandidates
    """
    looppositions = gamestate[1]
    if gamestate[0] == player: #check if I have a piece in the middle.
        doubleopen = False
        for index, checker in enumerate(looppositions):
            if checker == '' and looppositions[index-1] == '':
                doubleopen = True
                chosenspot = (index - random.randint(0,1)) %8
        if doubleopen: #check if there are two adjacent open spaces.  If yes, move to one of them randomly
            move = ('center',chosenspot)
        else: #move to random space bracketed by the enemy
            for index, checker in enumerate(looppositions):
                if checker != '' and checker == looppositions[index-2] and looppositions[index-1] =='':
                    move = ('center', (index-1)%8)
    else: #pick randomly among the moves that don't move to the middle
        noncentermoves = []
        for move in newcandidates:
            if move[1] == 'center':
                pass
            else:
                noncentermoves.append(move)
        if len(noncentermoves) == 0:
            index = random.randint(0, len(newcandidates)-1)
            move = newcandidates[index]
        else:
            index = random.randint(0,len(noncentermoves)-1) #this line triggers a bug
            move = noncentermoves[index]

    return move 

def isBlunder(gamestate, move): #needs to be updated for new moves
    looppositions = gamestate[1]
    print("gamestate", gamestate)
    print("move", move)
    if move[0] == 'center':
        blunderer = gamestate[0]
    else:
        blunderer = looppositions[move[0]]
    if blunderer == 'W': opponent = 'B'
    else: opponent = 'W'

    newstate = updateGame(gamestate,move)
    threatmoves = legalMoves(newstate, opponent)
    result = False
    for move in threatmoves:
        if isWon(updateGame(newstate, move), opponent):
            result = True
            break
    return result

def legalMoves(gamestate, player):
    movelist = []
    looppositions = gamestate[1]
    #print(looppositions)
    #print(looppositions.count('W'))
    center = 0
    if gamestate[0] == player: center = 1
    if looppositions.count(player) + center == 3:
        for index, checker in enumerate(looppositions, start=0):
            if checker == player:
                if gamestate[0] == '':
                    movelist.append((index, 'center'))
                if looppositions[(index-1)%8] == '':
                    movelist.append((index, (index-1)%8))
                if looppositions[(index+1)%8] == '':
                    movelist.append((index, (index+1)%8))
        openspots = [i for i,x in enumerate(looppositions) if x == '']
        if gamestate[0] == player:
            for spot in openspots:
                movelist.append(('center',spot))
    else:
        options = [i for i,x in enumerate(looppositions) if x =='']
        for spot in options:
            movelist.append(('new',spot))
        if gamestate[0] == '':
            movelist.append(('new', 'center'))
    return movelist

def updateGame(gamestate, move):
    #assumes move is legal, for now
    #stupid list of lists... pointer hell.  USE A CLASS IDIOT
    origcenter = gamestate[0]
    origlooppositions = gamestate[1] 
    oldlooppositions = origlooppositions[:]
    newlooppositions = origlooppositions[:]
    newcenter = origcenter

    if move[0] == 'new': #update for new moves
        if move[1] == 'center':
            newcenter #argh NEED player!
    elif move[0] == 'center':
        newlooppositions[move[1]] = origcenter
        newcenter = ''
    elif move[1] == 'center':
        newcenter = oldlooppositions[move[0]]
        newlooppositions[move[0]] = ''
    else:
        newlooppositions[move[1]] = oldlooppositions[move[0]]
        newlooppositions[move[0]] = ''
    return [newcenter, newlooppositions]

def isWon(gamestate, player):
    looppositions = gamestate[1]
    for index,item in enumerate(looppositions):
            if item == player and item == looppositions[index-1] and item == looppositions[index-2]:
                return True
            if item == player and item == gamestate[0] and item == looppositions[index-4]:
                return True
    return False
