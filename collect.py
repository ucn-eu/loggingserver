import requests
from config import TestingConfig
import json

from database import AuthDB

def fetchlocations():
	
	tokens = authdb.fetch_tokens()
 	
 	for token in tokens:
 		result = None
 		print "%s %s" % (token['host'], token['token'])
 		if token:
 			qtoken = "&access_token=" + token['token']
 			url    = cfg.API_URL + "/user/places/daily?pastDays=2" + qtoken
 			print url
			result =  requests.get(url).json()
			
 		else:
 			print "unable to get access token for host %s" % token['host']
 			return
 			
 	print "returned location data for host %s" % token['host']
	print result
	#return jsonify({"result":result})
	
if __name__ == "__main__":
	authdb = AuthDB(name="auth.db")
	cfg = TestingConfig()
	fetchlocations()