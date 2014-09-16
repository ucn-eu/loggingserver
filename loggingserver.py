from flask import Flask, request, jsonify
import json
import os
import datetime
from datetime import date
<<<<<<< HEAD
import requests
import config
import logging
from database import AuthDB

app = Flask(__name__)
app.config.from_object(config.TestingConfig)
logger = logging.getLogger( "ucn_logger" )
hdlr = logging.FileHandler(app.config["LOGFILE"] or '/var/tmp/ucn.log') 
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)

#clicks on this url and is then prompted to enter pin in moves app.
@app.route("/", methods=['GET'])
def root():
	if len(request.access_route) > 1:
		host = request.access_route[-1]
	else:
		host = request.access_route[0]

	logger.debug("GET / from %s" % host)
	u =  '%s/authorize?response_type=code' % app.config["OAUTH_URL"]
	c = '&client_id=' + app.config["CLIENT_ID"]
	s = '&scope=' + 'activity location'
	url = u + c + s
	return '<a href="' + url + '">click me</a>'

#user is redirected here with the authcode
@app.route("/moves/callback")
def authcallback():
	
	if len(request.access_route) > 1:
		host = request.access_route[-1]
	else:
		host = request.access_route[0]

	logger.debug("GET /moves/callback from %s" % host)
	code = request.args.get('code')
	#now swap the code for a token?
	c = '&client_id=' +  app.config["CLIENT_ID"]
	r = '&redirect_uri=' + app.config["REDIRECT_URL"]
	s = '&client_secret=' +  app.config["CLIENT_SECRET"]
	j = requests.post(app.config["OAUTH_URL"] + '/access_token?grant_type=authorization_code&code=' + code + c + s + r)
	logger.debug("swapped code for token for host %s" % host)
	token = j.json()['access_token']
	authdb.insert_token_for_host(host, token)
	logger.debug("saved token for host %s" % host)
	return "Thanks - have saved the token!"
	
@app.route("/moves/location")
def location():
	if len(request.access_route) > 1:
		host = request.access_route[-1]
	else:
		host = request.access_route[0]
	
	token = authdb.fetch_token_for_host(host)
	result = None
	
	if token:
		qtoken = "&access_token=" + token
		result =  requests.get(app.config["API_URL"] + "/user/places/daily?pastDays=2" + qtoken).json()
	else:
		logger.error("unable to get access token for host %s" % host)
	
	logger.debug("returned location data for host %s" % host)
	return jsonify({"result":result})
	
@app.route("/log", methods=['POST'])
def log():
	
	data = request.get_json(force=False)
	datestr = datetime.datetime.now().strftime("%d-%m-%y_%H:%M:%S") 
	remoteip = ""
	if len(request.access_route) > 1:
		remoteip = request.access_route[-1]
	else:
		remoteip = request.access_route[0]

	logger.debug("received data for host %s" % host)
	
	try:
		strdata = "%s" % json.dumps(data)
		directory = "/var/log/netdata/%s" % (remoteip)

		if not os.path.exists(directory):
			logger.debug("creating new dir %s" % directory)
			os.makedirs(directory)

		with open("%s/%s.txt" % (directory, datestr), "w") as logfile:
			logfile.write(strdata)	
			logger.debug("written to %s/%s.txt" % (directory, datestr))
			return jsonify(success=True)
	
	except Exception as e:
		logger.error("exception writing data %s" % str(e))
		return jsonify(success=False, error=str(e))

	return jsonify(success=False)


if __name__ == "__main__":
	authdb = AuthDB(name="auth.db")
	#authdb.createTables()
	app.run(host='0.0.0.0', port=8000, debug=True)
=======

app = Flask(__name__)

@app.route("/log", methods=['POST'])
def log():

        data = request.get_json(force=False)
        datestr = datetime.datetime.now().strftime("%d-%m-%y_%H:%M:%S")
        print datestr
        try:
                strdata = "%s" % json.dumps(data)
                directory = "/var/log/netdata/%s" % (request.remote_addr)

                if not os.path.exists(directory):
                        os.makedirs(directory)

                with open("%s/%s.txt" % (directory, datestr), "w") as logfile:
                        logfile.write(strdata)
                        return jsonify(success=True)

        except Exception as e:
                print str(e)
                return jsonify(success=False, error=str(e))

        return jsonify(success=False)


if __name__ == "__main__":
        app.run(host='0.0.0.0', port=5000, debug=True)
>>>>>>> b6f6b7ff715ac9ebb4ad5531b09139935c698348
