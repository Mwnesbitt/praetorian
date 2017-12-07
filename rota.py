#!/usr/bin/python3
#Mark Nesbitt

#make sure you can easily play the game from the interpreter-- need some kind of vehicle for stepping through positions

import random
import sys

def otherPlayer(player):
    if player == 'W': return 'B'
    else: return 'W'

class Move(object): 
    def __init__(self, player, origin, destination):
        self.player = player
        self.origin = origin
        self.destination = destination

    def printme(self):
        print("Player:" ,self.player)
        print("Origin:" ,self.origin)
        print("Destination:" ,self.destination)

class Position(object):
    def __init__(self, player, center, loop):
        self.player = player
        self.center = center
        self.loop = loop

    def printme(self):
        print("Player:" ,self.player)
        print("Center:" ,self.center)
        print("Loop:" ,self.loop)

    def allCheckers(self):
        if self.center == '':
            if self.loop.count('') == 2: return True
            else: return False
        else:
            if self.loop.count('') == 3: return True
            else: return False

    def legalMoves(self):
        movelist = []
        if self.allCheckers(): #game is underway
            for index, checker in enumerate(self.loop):
                if checker == self.player:
                    if self.center == '':
                        movelist.append(Move(self.player,index, 'center'))
                    if self.loop[(index+1)%8] == '':
                        movelist.append(Move(self.player, index, (index+1)%8))
                    if self.loop[(index-1)%8] == '':
                        movelist.append(Move(self.player,index, (index-1)%8))
            if self.center == self.player:
                openspots = [i for i,x in enumerate(self.loop) if x == '']
                for spot in openspots: 
                    movelist.append(Move(self.player,'center', spot))
        else: #checkers are still being placed
            if self.center == '': movelist.append(Move(self.player,'new', 'center'))
            loopoptions = [i for i,x, in enumerate(self.loop) if x =='']
            for spot in loopoptions: 
                movelist.append(Move(self.player,'new', spot))
        return movelist

    def isLegalMove(self, moveobject):
        result = False
        if self.player != moveobject.player: return False
        for move in self.legalMoves():
            if moveobject.origin == move.origin and moveobject.destination == move.destination:
                result = True
        return result

    def applyMove(self, moveobject):
        if not self.isLegalMove(moveobject): sys.exit("That move isn't legal")
        newplayer = otherPlayer(self.player)
        newcenter = self.center
        newloop = self.loop[:] #pointer hell...
        if moveobject.origin == 'new':
            if moveobject.destination == 'center': 
                newcenter = self.player
            else: #should probably make this an elif and make the final else an error check/catch
                newloop[moveobject.destination] = self.player
        elif moveobject.origin == 'center':
            newcenter = ''
            newloop[moveobject.destination] = self.player
        elif moveobject.destination == 'center':
            newcenter = self.player
            newloop[moveobject.origin] = ''
        else: #should probably make this an elif and make the final else an error check/catch
            newloop[moveobject.destination] = self.player
            newloop[moveobject.origin] = ''
        result = Position(newplayer, newcenter, newloop)
        #print(result.player)
        #print(result.center)
        #print(result.loop)
        return result

    def isWon(self):
        for index, spot in enumerate(self.loop):
            if spot == otherPlayer(self.player) and spot == self.loop[index-1] and spot == self.loop[index-2]:
                return True
            if spot == otherPlayer(self.player) and spot == self.center and spot == self.loop[index-4]:
                return True
        return False

    #I believe there is a bug in here, the algo made a blunder and I don't exactly know why.
    #blunder details: 
    #pos.printme()
    #Player: W
    #Center: 
    #Loop: ['B', 'B', '', 'W', '', '', 'W', ''] actually white is already screwed here
    #mov = pos.notDumbMove() #This created a dumb move!
    #mov.printme()
    #Player: W
    #Origin: new
    #Destination: center
    def isBlunder(self, moveobject):
        if not self.isLegalMove(moveobject): sys.exit("That move isn't legal")
        nextPosition = self.applyMove(moveobject)
        threatmoves = nextPosition.legalMoves()
        result = False
        for move in threatmoves:
            possibleLosingPosition = nextPosition.applyMove(move)
            if possibleLosingPosition.isWon():
                result = True
                break
        return result

    def notDumbMove(self):
        #generate list of candidate moves
        candidates = self.legalMoves()
        if len(candidates) == 1: return candidates[0]

        #check for winning moves.  return it if found
        #BUG HERE
        #applyMove() seems to be storing the move so there is a memory across this loop
        for move in candidates:
            nextPosition = self.applyMove(move)
            if nextPosition.isWon(): return move

        #eliminate moves that allow opponent to win on next turn
        #LOGIC ERROR: IF WE'RE DEALING WITH NEW CHECKERS, WE'RE NOT CHECKING THAT THE MOVES AREN'T DUMB
        newcandidates = []
        for move in candidates:
            if self.isBlunder(move):
                pass
            else:
                newcandidates.append(move)
        if len(newcandidates) == 1: return newcandidates[0]
        if len(newcandidates) == 0: return candidates[0] #we got trapped
        
        #strategery time #SHOULD THIS SECTION BE USING newcandidates?
        if self.center == self.player: #check if the player has a piece in the middle.
            doubleopen = False
            for index, piece in enumerate(self.loop):
                if piece == '' and self.loop[index + 1] == '':
                    doubleopen = True
                    chosenspot = (index + random.randint(0,1)) %8
            if doubleopen: #check if there are two adjacent open spaces.  If yes, move to one of them randomly
                move = Move(self.player, 'center',chosenspot)
            else: #when there's not a double available, move to the random space bracketed by the enemy (which I think MUST exist)
                for index, piece in enumerate(self.loop):
                    if piece != '' and piece == self.loop[index-2] and self.loop[index-1] =='':
                        move = Move(self.player,'center', (index-1)%8)
        else: #pick randomly among the moves that don't move to the middle, unless you have to move to the middle, in which case it picks randomly
            noncentermoves = []
            for move in newcandidates:
                if move.destination == 'center':
                    pass
                else:
                    noncentermoves.append(move)
            if len(noncentermoves) == 0: #If you are forced to move to the middle, does it matter who you send? (If a tree falls in the forest...)
                index = random.randint(0, len(newcandidates)-1)
                move = newcandidates[index]
            else:
                index = random.randint(0,len(noncentermoves)-1) 
                move = noncentermoves[index]
        #print(move.player)
        #print(move.origin)
        #print(move.destination)
        return move 
        
