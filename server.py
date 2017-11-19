import socket 
import sys
from game import *

DEBUG = True

class Server(object):
	def __init__(self,host="",port=9047, connections=10):
		print "[+] Starting Hangman Server."
		try:
			self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			print "[+] Socket Created"
		except socket.error:
			print "[-] Failed to create socket"
			sys.exit()
		
		self.host = host
		self.port = port
		
		#Limit Of Connections Server Will Allow
		self.connections = connections
		
		#Accounts for Users. A user name maps to a Password
		self.accounts = {"Cody" : "Falzone"}

		# Record of High Scores
		self.hall_of_fame = {}

		# Users that Are currently Connected to the Server.
		self.connected_users = []
		
		# Given a Connection, will return a User.
		self.user_lookup = {}
	
		# Given a user , will return a Game object which they are playing in.
		self.game_players = {}
		
		# List of all Games Currently Being Played on Server.
		self.games = []

		# Functions Sever Can Perform.
		self.functions = {
			
				"login" : self.login, 
				"make_user" : self.make_user,
				"hall" : self.hall,
				"start_new_game" : self.start_new_game
				
				}
		try:
			self.s.bind((self.host,self.port))
		except socket.error:
			print " [-] Bind Failed."

		self.s.listen(self.connections)


	def start(self):
		while True:
			connection, address = self.s.accept()
			if address not in self.connected_users:
				self.connected_users.append(address)
				self.create_player_connection(connection)

	def create_player_connection(self,connection):
		connection.send("[+] Greetings From the Hangman Server.")
		while True:
			data = connection.recv(1024)
			if data == "":
				break

			command,parameters = self.unpack(data,connection)

			if DEBUG:
				print "Command: ", command
				if parameters != None:
					print "Parameters: ", parameters

			if command in self.functions and parameters != False:
				connection.send(self.functions[str(command)](parameters,connection))
			elif command in self.functions and parameters == False:
				connection.send(self.functions[str(command)]())
			else:
				raise ValueError("[-] Invalid Command.")
		
	def unpack(self,data,connection):
		if DEBUG: 
			print "Unpacking..."
		if data =="":
			raise ValueError("[-] Received Empty Packet!")
		elif data != "":
			data = data.strip().split()
			if DEBUG:
				print "[!] Received Data: "
				print data
				print "Length of data: ", len(data)

		if len(data) > 1:
			if DEBUG:
				print "Returning" + str(data[0]) + str(data[1:])
			return (data[0],data[1:])
		elif len(data) == 1:
			if DEBUG:
				print "Returning" + str(data[0]) + str(False)
			return data[0],False
		else:
			raise ValueError("[-] Received Empty Packet!")
		

	def login(self,parameters,connection):
		print "[!] Attempting to Login " + str(parameters[0]) + " to Server..."
		if len(parameters) == 2 and parameters[0] != None and parameters[1] != None:
			if DEBUG:
				print "Login Called!"
			if parameters[0] in self.accounts.keys():
				if self.accounts[parameters[0]] == parameters[1]:
					self.user_lookup[connection] = parameters[0]
					return "game success"
			return "initial fail login"

	def make_user(self,parameters,connection):
		print "[!] Attempting to Make User " + str(parameters[0]) + " to Server..."
		if len(parameters) == 2 and parameters[0] != None and parameters[1] != None:
			if DEBUG:
				print "Make New User Called!"
			if parameters[0] not in self.accounts.keys():
				self.accounts[parameters[0]] = parameters[1]
				return "initial success"
			return "initial fail make_user"

	def start_new_game(self,parameters,connection):
		if len(parameters) > 0:
			user = self.user_lookup[connection]
			game = HangMan(parameters[0])
			game.players.append(user)
			self.game_players[user] = game
			self.games.append(game)
			if DEBUG:
				print "Creating A New Game With " + str(parameters[0]) + " Difficulty."
			
	def run_game(self,parameters,connection):			
			connection.send("game_state" + game.welcome_message)
			while True:
				connection.send(game.state())
				if self.turn[connection] == 
		else:
			raise ValueError("[-] No Sever Parameter Found.")
			
	
	def hall(self):
		hall = ""
		for name in self.hall_of_fame.keys():
			hall += " " + name + self.hall_of_fame[name] 
		if hall != "":
			return "hall " + hall
		else:
			return "hall False"
	

	
if __name__ == "__main__":
	server = Server()
	server.start()

