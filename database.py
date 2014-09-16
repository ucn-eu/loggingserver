import sqlite3
import logging

log = logging.getLogger( "console_log" )

class AuthDB(object):
	
	def __init__( self, name):
		self.name = name
		self.connected = False
		
	def connect(self):
		log.debug( "connecting to sqllite database %s" % self.name )
		if self.connected is False:
			self.conn = sqlite3.connect("%s" % self.name, check_same_thread = False)
			self.connected = True
	
	def insert_token_for_host(self, host, token):
		if self.connected is not True:
			self.connect()
		self.conn.execute("INSERT INTO TOKENS(host, token) VALUES(?,?)", (host, token))
		self.conn.commit()
	
	def fetch_token_for_host(self, host):
		if self.connected is not True:
			self.connect()
		result = self.conn.execute("SELECT token FROM TOKENS WHERE host = '%s'" % host)
		token = result.fetchone()
		if token:
			return token[0]
		else:
			return None
			
	def createTables(self):
		if self.connected is not True:
			self.connect()
		
		self.conn.execute('''CREATE TABLE IF NOT EXISTS TOKENS
			(id INTEGER PRIMARY KEY AUTOINCREMENT,
			host CHAR(16),
			token CHAR(255),
			UNIQUE(host, token) ON CONFLICT REPLACE);''')	
		self.conn.commit()
	