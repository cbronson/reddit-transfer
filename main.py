#!/usr/bin/env python
import sys
import requests
from requests import Request
import webbrowser
import socket
from urlparse import urlparse, parse_qs
import json


#globals
user_agent = 'my-app/0.0.1'


def startServer():
	host = ''
	port = 3030
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	try:
		s.bind((host,port))
	except socket.error as e:
		print(str(e))

	s.listen(5)
	print 'Waiting for authorization code (check your browser)...';

	listenForData = True

	while listenForData:
		c,addr = s.accept()
		print('Received connection!')
		print(str(addr))
		data = c.recv(1024)
		if(data):
			print 'Recevied data!'
			c.send('HTTP/1.0 200 OK\n')
			c.send('Content-Type: text/html\n')
			c.send('\n')
			c.send("""
				<html>
				<body>
				<h1>You may now close this window.</h1>
				</body>
				</html>
			""") 
			c.close()
			listenForData = False
			return data

def getCodeFromData(data):
	split = data.split('\n', 1)[0]
	split2 = split.split(' ', 2)[1]
	parsed = parse_qs(urlparse(split2).query)
	code = ''.join(parsed.get('code'))
	return code


def authorize(client_id, secret):
	ac = getAuthorizationCode(client_id)
	at = getAccessToken(ac, client_id, secret)

	print 'Access Token: '
	print at

	return at


def getAuthorizationCode(client_id):
	payload = {
	'client_id': client_id, 
	'response_type': 'code',
	'state': 'randotexto',
	'redirect_uri': 'http://127.0.0.1:3030/callback',
	'duration': 'temporary',
	'scope': 'mysubreddits subscribe'
	}

	headers = {'user-agent': user_agent}


	req = Request('GET', 'https://www.reddit.com/api/v1/authorize', params=payload, headers=headers)
	p = req.prepare()


	webbrowser.open(p.url);

	data = startServer();

	if(data is False):
		print 'Connection to server failed!'

	code = getCodeFromData(data)

	print 'Code:'
	print code

	return code

def getAccessToken(code, client_id, secret):	
	postURL = 'https://www.reddit.com/api/v1/access_token'

	accessPayload = {
		'grant_type': 'authorization_code',
		'code': code,
		'redirect_uri': 'http://127.0.0.1:3030/callback'
	}

	accessHeaders = {
		'user-agent': user_agent,
	}

	postAccessToken = requests.post(postURL, data=accessPayload, headers=accessHeaders, auth=(client_id,secret))
	

	accessToken = postAccessToken.json().get('access_token')

	return accessToken




def getSubscriptions(accessToken):
	getSubscriptionsHeaders = {
		'user-agent': user_agent,
		'Authorization': 'Bearer '+accessToken
	}

	getSubscriptions = requests.get('https://oauth.reddit.com/subreddits/mine/subscriber?limit=100', headers=getSubscriptionsHeaders)

	print getSubscriptions

	subs_data = json.loads(getSubscriptions.text)

	subs_parent = subs_data['data']['children']


	subNameList = [];

	for s in subs_parent:
		print s['data']['name']
		subNameList.append(s['data']['name'])


	subscriptionsString = ','.join(subNameList)

	return subscriptionsString


def setSubscriptions(accessToken, subscriptions):
	subscribePayload = {
		'action': 'sub',
		'sr': subscriptions 
	}

	subscriptionsHeaders = {
		'user-agent': user_agent,
		'Authorization': 'Bearer '+accessToken
	}

	setSubscriptions = requests.post('https://oauth.reddit.com/api/subscribe', data=subscribePayload, headers=subscriptionsHeaders)

	print setSubscriptions.text

def setSingleSubscription(accessToken):
	subscribePayload = {
		'action': 'sub',
		'sr': 't5_1rqwi' #temporary subreddit subscription
	}

	subscriptionsHeaders = {
		'user-agent': user_agent,
		'Authorization': 'Bearer '+accessToken
	}

	setSubscriptions = requests.post('https://oauth.reddit.com/api/subscribe', data=subscribePayload, headers=subscriptionsHeaders)

	print 'Set temporary subscription'
	print setSubscriptions.text

def clearSubscriptions(accessToken):

	#Possible bug: it seems we may not be able to retreive subscriptions from a new account
	#until the user has subscribed to at least one other sub.

	setSingleSubscription(accessToken)
	s = getSubscriptions(accessToken)
	#print s

	print 'Unsubscribing from all subscriptions'
	subscribePayload = {
		'action': 'unsub',
		'sr': s 
	}

	subscriptionsHeaders = {
		'user-agent': user_agent,
		'Authorization': 'Bearer '+accessToken
	}

	setSubscriptions = requests.post('https://oauth.reddit.com/api/subscribe', data=subscribePayload, headers=subscriptionsHeaders)
	print setSubscriptions

tg = "TESTING"
def testFunc():
	return tg
#MAIN
#read accounts from accounts.json
with open('accounts.json') as accountsFile:
	data = json.load(accountsFile)

print testFunc()


# #User input
# a = raw_input('Follow the setup instructions at _________. \nPress Enter to Begin\n')
# print '==== Authorizing First Account ====\n'
# b = raw_input('Log in to the Reddit account you want to export subscriptions from.\nPress Enter when ready.')

# firstAccountAccessToken = authorize(data["fromAccount"]["client_id"], data["fromAccount"]["secret"])


# c = raw_input('\nLog in to the Reddit account you want to import subscriptions to\nPress Enter when ready.')

# print '==== Authorizing Second Account ====\n'
# secondAccountAccessToken = authorize(data["toAccount"]["client_id"], data["toAccount"]["secret"])

# if(secondAccountAccessToken):
# 	print 'Received second access token!\n'
# 	d = raw_input('Accounts ready. Press Enter to begin transfer.\nCAUTION: This will overwrite any subscriptions on the second account')
# else:
# 	print 'Error occured retreiving second account token!\n'


# subList = getSubscriptions(firstAccountAccessToken)
# clearSubscriptions(secondAccountAccessToken)
# setSubscriptions(secondAccountAccessToken, subList)

# print '==== Done ===='


#TODO: prompt user input
#TODO: allow socket connection reuse
#TODO: Error handling
#TODO: Verbose/debug mode
#TODO: Set proper user agent 
#TODO: What if the user accidently hits "decline" when authorizing app