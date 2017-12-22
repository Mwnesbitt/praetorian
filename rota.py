#!/usr/bin/python3
#Mark Nesbitt

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
        if self.isWon(): print("GAME IS OVER")

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
        #if not self.isLegalMove(moveobject): return "BLARGH"
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
    #Loop: ['B', 'B', '', 'W', '', '', 'W', ''] actually white is already screwed here.  WE GOT TRAPPED!
    #mov = pos.notDumbMove() #This created a dumb move! WRONG-- all moves were blunders since we were trapped.  Need better opening logic.
    #mov.printme()
    #Player: W
    #Origin: new
    #Destination: center
    def isBlunder(self, moveobject):
        #if not self.isLegalMove(moveobject): sys.exit("That move isn't legal")
        if not self.isLegalMove(moveobject): return "BLARGH" 
        nextPosition = self.applyMove(moveobject)
        threatmoves = nextPosition.legalMoves()
        result = False
        for move in threatmoves:
            possibleLosingPosition = nextPosition.applyMove(move)
            if possibleLosingPosition.isWon():
                result = True
                break
        return result

    def isOpeningBlunder(self, moveobject):
        if self.allCheckers(): return False
        if moveobject.destination == 'center': return False #Kind of bad practice, but I know that I never go to the center unless I have to...

        if self.center == '':
            count = self.loop.count(self.player)
            if count == 1:
                if (moveobject.destination -4) % 8 == self.loop.index(self.player): return True  #Addresses: New game.  White to 7, black to 0, white to 3 (threatening), black to center (blocking and threatening), white to 4 (blocking), black to 5 (forcing win).
                if moveobject.destination == (self.loop.index(self.player) +1) %8 or moveobject.destination == (self.loop.index(self.player) -1 ) % 8 : return True  #Addresses: New game: White moves to 1, black to zero, white to 2.  This is an error, but its one move beyond the vision of allowsForcedMove.  Black plays to 3, and white is screwed.  Note that because your algo is working, specifically the allowsForcedMove function is working, this means that white will always move to the center in this situation, because the loss just came into sight. The rule needs to be: when laying checkers, do not put any of your checkers side by side on the loop.
                #Next two lines are total hacks for the unexplained loss below
                if self.loop.index(self.player) == (moveobject.destination -2) % 8 and self.loop[(self.loop.index(otherPlayer(self.player)) -1) %8] != '': return True
                if self.loop.index(self.player) == (moveobject.destination +2) % 8 and self.loop[(self.loop.index(otherPlayer(self.player)) +1) %8] != '': return True
            elif count == 2:
                l = []
                for index, piece in enumerate(self.loop):
                    if piece == self.player: l.append(index)
                m = moveobject.destination
                if m == l[0] + 1 or m == l[0] -1 or m == l[1] + 1 or m == l[1]-1 : return True
                #Another loss example:  New game:  White to 4, black to 5, white to 6, black to 3, white to 7 THIS IS NOT THE MISTAKE BUT IS PROBABLY EASIER THAN THE LOGIC REQUIRED TO FIX THE MISTAKE. black to 1.  White: 4 to center, MISTAKE.  Black 1 to 0.  White center to anywhere, random. Black with forced win.  Note also that this only happens when I move first, because when the computer moves first I have to respond and I don't get the opportunity to make this mistake.
                #Unexplained loss.  New game:W to 5, B to 4, W to 3, B to 1, W to 2 THIS IS THE ERROR, but why isn't it caught by l[0] -1 == moveobject.destination??  B to center, forced win.  This should also be caught by the forced move logic... I don't get it.
            else: return False #count must be 0
        else:
            pass #currently I'm not aware of a need to do anything if I have a piece in the middle

    def allowsForcedWin(self, moveobject):
        if not self.isLegalMove(moveobject): return "BLARGH"
        nextPosition = self.applyMove(moveobject)
        threatmoves = nextPosition.legalMoves()
        result = False 
        for move in threatmoves:
            possibleForcedWin = nextPosition.applyMove(move)
            responses = possibleForcedWin.legalMoves()
            allResponsesAreBlunders = True
            for move in responses:
                allResponsesAreBlunders = allResponsesAreBlunders and possibleForcedWin.isBlunder(move)
            if allResponsesAreBlunders:
                result = True
                break
        return allResponsesAreBlunders

    def notDumbMove(self):
        #generate list of candidate moves
        candidates = self.legalMoves()
        if len(candidates) == 1: return candidates[0]

        #check for winning moves.  return it if found
        for move in candidates:
            nextPosition = self.applyMove(move)
            if nextPosition.isWon(): return move

        #eliminate moves that allow opponent to win on next turn
        newcandidates = []
        for move in candidates:
            if self.isBlunder(move):
                pass
            else:
                newcandidates.append(move)
        if len(newcandidates) == 1: return newcandidates[0]
        if len(newcandidates) == 0: return candidates[0] #we got trapped

        #Eliminate moves that allow opponent to response with a move that forces a win.  This was added later and two things to note: 1 possible runtime issues, 2 this might make all my other strategery obsolete.
        newestcandidates = []
        for move in newcandidates:
            if self.allowsForcedWin(move): pass
            else: newestcandidates.append(move)
        if len(newestcandidates) == 1: return newestcandidates[0]
        if len(newestcandidates) == 0: return newcandidates[0] #dang this game must be harder than I thought
        newcandidates = newestcandidates

        #Blocking an early trap, e.g. white is trapped ['','B','B', '', 'W', '', 'W','']
        #this should be added to the isOpeningBlunder method
        if not self.allCheckers(): 
            for index, piece in enumerate(self.loop):
                if piece == '' and self.loop[index-2] == '' and self.loop[index-1] == otherPlayer(self.player):
                    return Move(self.player, 'new', index)

        #eliminate piece placement mistakes
        newestcandidates = []
        for move in newcandidates:
            if self.isOpeningBlunder(move): pass
            else: newestcandidates.append(move)
        if len(newestcandidates) == 1: return newestcandidates[0]
        if len(newestcandidates) == 0: return newcandidates[0] #man I should study this game more
        newcandidates = newestcandidates
        
        #strategery time #SHOULD THIS SECTION BE USING newcandidates?
        if self.center == self.player: #check if the player has a piece in the middle.
            doubleopen = False
            for index, piece in enumerate(self.loop):
                if piece == '' and self.loop[(index + 1)%8] == '':
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
        
