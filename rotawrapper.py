#!/usr/bin/python3
#Mark Nesbitt


import json
import requests
#import cookielib

def initialize():
    url = 'https://rota.praetorian.com/rota/service/play.php'
    #jar = cookielib.CookieJar()
    s = requests.Session()
    r = s.get(url+"?request=new&email=mwnesbitt@gmail.com")
    #print(s.cookies)
    #print(res.text)
    response = r.json()
    print(response)
    """
    r = requests.get(url+"?request=new&email=mwnesbitt@gmail.com")
    print(r.text)
    print(r.cookies)
    res = r.json()
    print(res)
    """
    if response['status'] == "fail":
        print("FAILURE")
    else:
        print("SUCCESS")
    return s

def place(session, dest):
    s = session
    url = 'https://rota.praetorian.com/rota/service/play.php'
    r = s.get(url+"?request=place&location="+dest)
    response = r.json()
    print(response)
    r = s.get(url+"?request=place&location=2")
    response = r.json()
    print(response)
    """
    print(s.cookies)
    print(s.headers)
    s.get(url+"?request=status")
    print(s)
    """


cookies = initialize()
place(cookies, "1")

