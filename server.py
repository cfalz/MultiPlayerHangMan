import socket 
import threading
import time
import sys
import Queue
from game import *
from menu import *

DEBUG = True
SLEEP = 0.1

class Server(object):
	def __init__(self,host="",port=9046, connections=10):
		print "[+] Starting Hangman Server."
		try:
			self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			print "[+] Socket Created"
		except socket.error:
			print "[-] Failed to create socket"
			sys.exit()
		
		self.host = host
		self.port = port
		self.handler = None

		
		#Players To Join Exsisting Games
		self.q = Queue.Queue()

		#Limit Of Connections Server Will Allow
		self.connections = connections
		
		#Accounts for Users. A user name maps to a Password
		self.accounts = {"Cody" : "Falzone", "Admin" : "Admin"}

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
		
		# A Game maps to a list of Players in that game.
		self.game_lookup = {}

		# Functions Sever Can Perform.
		self.functions = {
			
				"update_menu" : self.update_menu,
				"login" : self.login, 
				"games_list" : self.games_list,
				"make_user" : self.make_user,
				"hall" : self.hall,
				"start_new_game" : self.start_new_game,
				"create_new_game" : self.create_new_game,
				"exit" : exit
				
				}
		try:
			self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.s.bind((self.host,self.port))
		except socket.error:
			print " [-] Bind Failed."

		self.s.listen(self.connections)

			
	def send(self,connection,data):
		time.sleep(0.1)
		connection.send(data)

	def receive(self,connection):
		return connection.recv(5012)
			
	""" Returns a command and parameters from data passed in. """	
	def unpack(self,data):
		if DEBUG: 
			print "Unpacking..."
			print data
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
			return data[0],[]
		else:
			raise ValueError("[-] Received Empty Packet!")
		

	""" Process a command and determines which server function to run next. """
	def process(self, menu_response, connection):
		if DEBUG:
			print "[!] In Server Process."
			print menu_response
		command, parameters = self.unpack(menu_response)

		if command in self.functions:
			parameters.append(connection)
			self.functions[command](parameters)
		else:
			self.run_game(game,connection)
			raise ValueError(" [-] Recevied Unknown Command and Parameters Combination.\n Command: " + str(command) + "\nParameters: " + str(parameters) + "\n")


	""" Listens for users connecting to the server and initializes connections. """
	def start(self):
		while True:
			connection, address = self.s.accept()
			if address not in self.connected_users:
				self.connected_users.append(address)
				player_thread = threading.Thread(name = "thread "+str(address), target = self.run, args = (connection,))
				player_thread.daemon = True
				player_thread.start()
				

	def listen(self,player,game):
		while True:
			connection, address = self.s.accept()
			if address not in self.connected_users:
				self.connected_users.append(address)
				self.q.push(connection,address)

	""" Checks the user login information in the database. """
	def check_login(self,parameters):
		print "[!] Attempting to Login " + str(parameters[0]) + " to Server..."
		if len(parameters) == 2 and parameters[0] != None and parameters[1] != None:
			if DEBUG:
				print "Login Called!"
			if parameters[0] in self.accounts.keys():
				if self.accounts[parameters[0]] == parameters[1]:
					return True
			return False

	def update_menu(self, parameters):
		if parameters[0] == "login":
			self.login(parameters[1])
		if parameters[0] == "make_user":
			self.signup(parameters[1])
		if parameters[0] == "game":
			self.game(parameters[1])
		if parameters[0] == "start_new_game":
			self.start_new_game(parameters[1])
		
	""" Retreives the login information from the user. """
	def login(self,connection):
		menu = Login()
		user_name = ""
		time.sleep(SLEEP)
		self.send(connection, "response_required@" + menu.welcome() + menu.get_user_name())
		user_name = self.receive(connection)
		if DEBUG:
			print "." + user_name + "."
		while True:
			while not menu.valid_input_string(user_name):
				time.sleep(SLEEP)
				self.send(connection, "response_required@" + menu.get_user_name() + "\n")
				user_name = self.receive(connection)
				if DEBUG:
					print "." + user_name + "."
			password = ""
			while not menu.valid_input_string(password):
				time.sleep(SLEEP)
				self.send(connection, "response_required@" + menu.get_user_password() + "\n")
				password = self.receive(connection)
				if DEBUG:
					print "." + password + "."

			if self.check_login([user_name, password]):
				self.user_lookup[connection] = user_name
				menu.successful_login(user_name)
				self.update_menu(["game",connection])
			else:
				self.send(connection, "[-] Incorrect Login Attempt. Please Try Again.\n")
				user_name = ""
				password = ""

	def run(self,connection):
		""" Prompt user for login, signup, hall or exit.\n 
		Returns command for which server function to execute next. """
		if DEBUG:
			print "[!] Initializing Player..."
		menu = Initial()
		time.sleep(SLEEP)
		self.send(connection, menu.welcome())
		if DEBUG:
			print "[!] Waiting for Player Reponse of Initial Menu..."
		while True:
			if DEBUG: 
				print "[!] Sending Initial Prompt."
			time.sleep(SLEEP)
			self.send(connection, "response_required@" + menu.prompt() + "\n[!] Please Select An Option.\n")
			user_response = self.receive(connection)
			if DEBUG: 
				print "[!] Checking " + "." + user_response + "."
			if menu.valid_input_string(user_response):
				if DEBUG:
					print "[!] Calling server process with " , user_response
				command = menu.process(user_response)
				if command != "fail":
					self.process(command, connection)

	def games_list(self,parameters):
		connection = parameters[0]
		prompt = "\n".join([ "Game: " + str(game.number) for game in self.games ])
		self.send(connection, "response_required@ " + "[+] Please Enter The Number For A Game From The List Of Games.\n" + prompt + "\n")
		selection = self.receive(connection)
		print "[+] Request To Join Game: " + str(selection)
		if int(selection) <= len(self.games):
			self.send(connection, "[!] Attempting to join Game " + str(selection))
			select = int(selection)
			self.join_game(self.user_lookup[connection],self.games[select], connection)

	def join_game(self, player, game, connection):
		self.send(connection, "[!] Please Wait While You Are Connected To Game " + str(game.number)+ "...\n") 
		self.game_lookup[player] = game
		game.add_player(player, connection)
		while game in self.game_lookup.values():
			pass
		self.game(connection)

	""" Allows user to pick a username and password for account creation. """
	def signup(self,connection):
		while True:
			menu = Signup() 
			self.send(connection, menu.welcome())
			user_name = ""
			while not self.valid_input_string(user_name):
				time.sleep(SLEEP)
				user_name = self.send(connection, "response_required@ " + menu.pick_user_name())
			password = ""
			while not self.valid_input_string(password):
				password = self.send(connection, "response_required@ " + menu.pick_user_password())
			if self.make_user("make_user" [user_name,password]):
				time.sleep(SLEEP)
				self.send(connection, menu.successful_signup())
				return

	def game(self, connection):
		menu = Game()
		while True:
			if DEBUG: 
				print "[!] Sending Game Prompt."
			time.sleep(SLEEP)
			self.send(connection, menu.welcome())
			self.send(connection, "response_required@" + menu.prompt())
			user_response = self.receive(connection)
			if DEBUG: 
				print "[!] Checking " + "." + user_response + "."
			if menu.valid_input_string(user_response):
				if DEBUG:
					print "[!] Calling server process with " , user_response
				command = menu.process(user_response)
				if DEBUG:
					print "[!] Calling server process with command: " , command
				if command != "fail":
					self.process(command, connection)
			else:
				self.send(connection, "[-] Invalid Selection.") 
		

	def make_user(self,parameters):
		print "[!] Attempting to Make User " + str(parameters[0]) + " to Server..."
		if len(parameters) == 2 and parameters[0] != None and parameters[1] != None:
			if parameters[0] not in self.accounts.keys():
				self.accounts[parameters[0]] = parameters[1]
				return True
			return False

	def start_new_game(self, connection):
		menu = StartNewGame()
		menu.welcome()
		while True:
			time.sleep(SLEEP)
			self.send(connection, "response_required@ " + menu.prompt())
			user_response = self.receive(connection)
			if DEBUG: 
				print "[!] Checking " + "." + user_response + "."
			if menu.valid_input_string(user_response):
				if DEBUG:
					print "[!] Calling server process with " , user_response
				command = menu.process(user_response)
				if command != "fail":
					self.process(command, connection)

		
	def create_new_game(self,parameters):
		print self.user_lookup
		if len(parameters) > 1:
			connection = parameters[1]
			user = self.user_lookup[connection]
			game = HangMan(parameters[0],game_id = len(self.games))
			game.add_player(user,connection)
			self.game_players[user] = game
			self.games.append(game)
			if DEBUG:
				print " [!] Creating A New Game With " + str(parameters[0]) + " Difficulty."
			self.run_game(game)
			self.game(connection)
			
	
	def run_game(self, game):
		for connection in game.connections:
			self.send(connection, game.welcome()+ "\n")
			time.sleep(0.1)

		game_over = False
		while not game_over:
			current_turn = game.update_turn()
			if DEBUG:
				print "connections:", self.connections

			for connection in game.connections:
				self.send(connection, "\n  **** HANGMAN **** \n Game " + str(game.number) + "\n" +  " On " + str(game.difficulty).upper() + " Difficulty\n") 
				self.send(connection, game.get_state() + "\n" + "It is " + self.user_lookup[game.turn] + "'s turn!.\n")

			self.send(game.turn, "response_required@" + "[+] It's Your Turn. Please Guess A Character.")
			c = self.receive(game.turn)
			game_over = game.update_player_state(self.user_lookup[current_turn], c)
		for connection in game.connections:
			connection.send("[!] Game Over...Returning To The Game Menu...")
		return True
		

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

