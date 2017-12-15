#!/usr/bin/python3
#Mark Nesbitt
import json
import requests
import rota

def initialize():
    url = 'https://rota.praetorian.com/rota/service/play.php'
    s = requests.Session()
    r = s.get(url+"?request=new&email=mwnesbitt@gmail.com")
    response = r.json()
    #print(response)
    if response['status'] == "fail": print("FAILURE")
    else: print("SUCCESS")
    return s, response['data']

def place(session, dest):
    s = session
    url = 'https://rota.praetorian.com/rota/service/play.php'
    r = s.get(url+"?request=place&location="+dest)
    response = r.json()
    return response['data']

def convertChar(char):
    if char == 'c': return 'B'
    if char == 'p': return 'W'
    if char == '-': return ''

def makePosition(gamedata, playerjunk):
    #need player, center, loop
    board = gamedata['board']
    center = convertChar(board[4])
    loopjunk = [board[1], board[2], board[5], board[8], board[7], board[6],board[3], board[0]]
    loop = []
    for item in loopjunk:
        loop.append(convertChar(item))
    player = convertChar(playerjunk)
    return rota.Position(player, center, loop)

def convertMove(des):#NEED TO UPDATE FOR POST-PLACEMENT
    if des == 'center': return "5"
    if des == 0: return "2"
    if des == 1: return "3"
    if des == 2: return "6"
    if des == 3: return "9"
    if des == 4: return "8"
    if des == 5: return "7"
    if des == 6: return "4"
    if des == 7: return "1"

def move(session, orig, dest):
    s = session
    url = 'https://rota.praetorian.com/rota/service/play.php'
    r = s.get(url+"?request=move&from=%s&to=%s" %(orig, dest))
    response = r.json()
    return response['data']

def nextGame(session):
    s = session
    url = 'https://rota.praetorian.com/rota/service/play.php'
    r = s.get(url+"?request=next")
    response = r.json()
    return response['data']

def runGame():
    cookies, gamedata= initialize()

    for k in range(2):
        print("\n\n\n GAMES WON:"+str(k)+"\n\n")
        print(gamedata)
        pos = makePosition(gamedata, 'p')
        pos.printme()

        for i in range(3):
            print("\nGAME "+str(k+1))
            print("PLACING CHECKERS\n")
            mov = pos.notDumbMove()
            mov.printme()
            gamedata = place(cookies, convertMove(mov.destination))
            print(gamedata)
            pos = makePosition(gamedata, 'p')
            pos.printme()

        for i in range(32):
            print("\nGAME "+str(k+1))
            print("TURN "+ str(i)+" \n")
            mov = pos.notDumbMove()
            mov.printme()
            gamedata = move(cookies, convertMove(mov.origin), convertMove(mov.destination))
            print(gamedata)
            pos = makePosition(gamedata, 'p')
            pos.printme()

        gamedata = nextGame(cookies)
        print(gamedata)


runGame()






