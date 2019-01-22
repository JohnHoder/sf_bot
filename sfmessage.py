#!/usr/bin/python
# -*- coding: UTF-8 -*-

import urllib2
import urllib
import sys
import time
import random
import re
import os
import cookielib
import socket

import hashlib

#sfbot 2014 - Jan Hodermarsky

class yolo_http_client:

    def __init__(self, proxy=None):
        self.cookie_handler   = urllib2.HTTPCookieProcessor(cookielib.CookieJar())
        self.redirect_handler = urllib2.HTTPRedirectHandler()
        self.http_handler     = urllib2.HTTPHandler()
        self.https_handler    = urllib2.HTTPSHandler()

        self.opener = urllib2.build_opener(self.http_handler,
                                           self.https_handler,
                                           self.cookie_handler,
                                           self.redirect_handler)

        if proxy:
            self.proxy_handler = urllib2.ProxyHandler(proxy)
            self.opener.add_handler(self.proxy_handler)

        useragent = [
		   'Opera/9.80 (Windows NT 6.1; U; en-US) Presto/2.7.62 Version/11.01',
		   'Mozilla/5.0 (Windows; U; Windows NT 5.1; en; rv:1.9.0.4) Gecko/2008102920 Firefox/3.0.4',
		   'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.2pre) Gecko/20100207 Ubuntu/9.04 (jaunty) Namoroka/3.6.2pre',
		   'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser;',
		   'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)',
		   'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1)',
		   'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6)',
		   'Microsoft Internet Explorer/4.0b1 (Windows 95)',
		   'Opera/8.00 (Windows NT 5.1; U; en)',
		   'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
		   'Mozilla/4.0 (compatible; MSIE 5.0; Windows ME) Opera 5.11 [en]'
	    ]

        referer	= ['http://google.com','http://bing.com','http://facebook.com']

        self.opener.addheaders = [('User-agent', random.choice(useragent)), ('Referer', random.choice(referer))]
       
        urllib2.install_opener(self.opener)
   
    def request(self, url, params={}, timeout=5):
        if params:
            params = urllib.urlencode(params)
            html = urllib2.urlopen(url, params, timeout)
        else:
            html = urllib2.urlopen(url)
           
        return html.read()

##########################################################
##########################################################

def helpscr():
        print "Usage of " + sys.argv[0] + ":\n" 
        print "--ToAll -> send a message to every player on the server\n"
        print "--ToUser username -> to send a message to the specified user\n"
        print "--ToRange x-y -> to send a message to the specified range of users - e.g. 1000-1300, the numbers indicate the postion of players from top\n"

def clear():
        if os.name in ['nt', 'win32', 'dos']:
            	os.system('cls')
        else:
        	os.system('clear')

##########################################################
#get config and message content from files

with open("config.txt") as f:
	config = f.readlines()
config = [x.strip('\n') for x in config]

server = config[0].split(' ')[1]
username = config[1].split(' ')[1]
password = config[2].split(' ')[1]

with open("text.txt") as l:
	text = l.readlines()
text = [x.strip('\n') for x in text]

subject = text[0]
del text[0] #delete subject name from array
del text[0]

content = ""
for line in text:
	content = content + line + " "

##########################################################

listPlayers = []
bot = yolo_http_client()

def login(username, password):
	hashx = hashlib.md5(password).hexdigest()
	requestLogin = '/request.php?req=00000000000000000000000000000000002' + username + '%3B' + hashx + '%3B&random=%2&rnd=9078657111356293884012'
	res = bot.request(server + requestLogin)
	return res

def getInfo():
	cookie = getCookie()
	requestInfo = '/request.php?req={0}004&rnd=5646764536'.format(cookie)
	res = bot.request(server + requestInfo)
	return res

def getSSID():
	res = login(username, password)
	#get SSID
	m = re.findall(r'\d+', res)
	ssid = m[2]
	return ssid

def getCookie():
	res = login(username, password)
	#get Cookie
	rawShitForCookie = res.split('/')
	RawCookie = rawShitForCookie[511]
	cookie = RawCookie.split(';')[2]
	return cookie

def getPlayersTen(position):
	cookie = getCookie()
	requestGetPlayers = '/request.php?req={0}007%3B{1}&random=%2&rnd=15165867331407603789267'.format(cookie, position)

	res = bot.request(server + requestGetPlayers)
	rawShitPlayers = res.split('/')

	sh = 1
	for shit in rawShitPlayers:
		if(sh == 2):
			listPlayers.append(shit)
		elif((sh-2)%5==0):
			listPlayers.append(shit)
		sh=sh+1
	return listPlayers

def getPlayers(x,y):
	for number in range(x,y): 
		if(number%10==0):
			getPlayersTen(number)
	return listPlayers

def sendMessage(recipient, subject, content):
	cookie = getCookie()
	requestSendMessage = '/request.php?req={0}509{1};{2};{3}&random=%2&rnd=160282871407685038247'.format(cookie, recipient, subject, content)
	res = bot.request(server + requestSendMessage)
	return res

def sendMessageToAll(x, y, subject, content):
	listPlayers = getPlayers(x, y)
	for player in listPlayers:
		print sendMessage(player, subject, content)

def sendTest():
	cookie = getCookie()
	message = '/request.php?req={0}509lioneers%26Pozvanka%26lel&random=%2&rnd=160282871407685038247'.format(cookie)
	
	res = bot.request(server + message)
	return res

def getMushroom():
	cookie = getCookie()
	requestGetMushroom = '/request.php?req={0}5171201&random=%2&rnd=17437022931407755509575'.format(cookie)
	res = bot.request(server + requestGetMushroom)
	return res

#####################################################################################################################

def getQuests():
	cookie = getCookie()
	requestInfo = '/request.php?req={0}010&random=%2&rnd=10259999771412184355127'.format(cookie)
	res = bot.request(server + requestInfo)
	return res

def getBestQuestForExp():
	quests = getQuests()
	rawShitForQuests = quests.split('/')
	q1 = (int)((int)(rawShitForQuests[280])/(int)(rawShitForQuests[241]))
	q2 = (int)((int)(rawShitForQuests[281])/(int)(rawShitForQuests[242]))
	q3 = (int)((int)(rawShitForQuests[282])/(int)(rawShitForQuests[243]))
	print "{0}, {1}, {2}".format(q1,q2,q3)
	RawQuest = [q1,q2,q3]
	maxim = max(RawQuest)
	for i in [i for i,x in enumerate(RawQuest) if x == maxim]:
		BestQuest = i + 1
	return BestQuest

def doQuest():
	questNumber = getBestQuestForExp()
	print questNumber
	cookie = getCookie()
	requestInfo = '/request.php?req={0}510{1}%3B&random=%2&rnd=11672216221412186509353'.format(cookie, questNumber)
	res = bot.request(server + requestInfo)
	return res
	


if __name__ == '__main__':
	if "--test" in sys.argv:
		print getBestQuestForExp()

		print getQuests()
		k = 1
		for ue in getQuests().split('/'):
			k = k +1
			if(ue == "23700"):
				print '{0}  \n  {1}'.format(ue, k)


		print doQuest()

		raise SystemExit

	if "--ToAll" in sys.argv:
		print "Please use --ToRange option, this feature is not fully supported yet!\n"

	elif "--ToUser" in sys.argv:
		lulz = sys.argv.index("--ToUser") + 1
		name = sys.argv[lulz]
		print sendMessage(name, subject, content)
	elif "--ToRange" in sys.argv:
		lulz = sys.argv.index("--ToRange") + 1
		rangexy = sys.argv[lulz]
		rangexy = rangexy.split('-')
		rangex = rangexy[0]
		rangey = rangexy[1]
		print sendMessageToAll(rangex, rangey, subject, content)
	else:
		helpscr()
		raise SystemExit

	if "-h" in sys.argv:
		helpscr()
		raise SystemExit


#http://s6.sfgame.cz/request.php?req={0}010&random=%2&rnd=10259999771412184355127
#282,283,284

	


