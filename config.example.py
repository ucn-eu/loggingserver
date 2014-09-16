class Config(object):
	CLIENT_ID	= "moves app client id" 
	CLIENT_SECRET 	= "moves app client secret"
	REDIRECT_URL  	= "http://[serverip]/moves/callback"
	OAUTH_URL	=  "https://api.moves-app.com/oauth/v1"
	API_URL 	= "https://api.moves-app.com/api/1.1"
	LOGFILE 	= "/var/tmp/ucn.log"
	
class TestingConfig(Config):
	pass

	
