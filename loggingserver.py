from flask import Flask, request, jsonify
import json
import os
import datetime
from datetime import date

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
