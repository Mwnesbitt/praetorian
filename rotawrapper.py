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
    if response['status'] == "fail": print("SESSION FAILURE")
    else: print("SESSION ESTABLISHED")
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
    board = gamedata['board']
    center = convertChar(board[4])
    loopjunk = [board[1], board[2], board[5], board[8], board[7], board[6],board[3], board[0]]
    loop = []
    for item in loopjunk:
        loop.append(convertChar(item))
    player = convertChar(playerjunk)
    return rota.Position(player, center, loop)

def convertMove(des):
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

    for k in range(50):
        print("\n\n\n#########\nGAMES WON:"+str(k)+"\n#########\n\n\n")
        print("Initial Position from API")
        print(gamedata)
        pos = makePosition(gamedata, 'p')
        pos.printme()

        for i in range(3):
            print("\n\nGAME "+str(k))
            print("PLACING CHECKERS")
            print("\nCurrent Position:")
            pos.printme()
            mov = pos.notDumbMove()
            print("\nPlayer Move:")
            mov.printme()
            gamedata = place(cookies, convertMove(mov.destination))
            print("\nAPI Response:")
            print(gamedata)
            pos = makePosition(gamedata, 'p')
            print("\nNew Position:")
            pos.printme()

        for i in range(32):
            print("\n\nGAME "+str(k))
            print("TURN "+ str(i))
            print("\nCurrent Position:")
            pos.printme()
            mov = pos.notDumbMove()
            print("\nPlayer Move:")
            mov.printme()
            gamedata = move(cookies, convertMove(mov.origin), convertMove(mov.destination))
            print("\nAPI Response:")
            print(gamedata)
            pos = makePosition(gamedata, 'p')
            print("\nNew Position:")
            pos.printme()

        gamedata = nextGame(cookies)
    print(gamedata) #should have the hash in it?
    r = cookies.get('https://rota.praetorian.com/rota/service/play.php?request=status')
    response = r.json()
    print(response)

if __name__ == '__main__':
    runGame()
