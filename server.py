import socket 
import threading
import time
import sys
import Queue
from repository import *
from player import *
from game import *
from menu import *

DEBUG = False
SLEEP = 0.1


class Server(object):
	def __init__(self, accounts_repo, hall_of_fame_repo, words_repo, host="", port=9046, connections=10):
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

		self.accounts_repo = accounts_repo
		
		self.hall_of_fame_repo = hall_of_fame_repo	

		self.words_repo = words_repo
		
		#Accounts for Users. A user name maps to a Password
		self.accounts = accounts_repo.get_data()

		# Record of High Scores
		self.hall_of_fame = hall_of_fame_repo.get_data()

		# The WordList for HangMan
		self.words = words_repo.get_data()

		# Users that Are currently Connected to the Server.
		self.connected_users = []
		
		# Given a Connection, will return a User.
		self.user_lookup = {}
	
		# A Game maps to a list of Players in that game.
		self.players_lookup = {}
		
		# List of all Games Currently Being Played on Server.
		self.games = []
		
		# Given a Player , will return a Game object which they are playing in.
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
				"exit" : self.exit
				
				}
		try:
			self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.s.bind((self.host,self.port))
		except socket.error:
			print " [-] Bind Failed."

		self.s.listen(self.connections)

			
	def send(self,connection,data):
		time.sleep(SLEEP)
		connection.send(data)

	def receive(self,connection):
		return connection.recv(5012)
			
	def exit(self, data):
		print "data", data
		connection = data[0]
		self.send(connection, "quit [-] Goodbye! ")
		print "Closing Connection."
		connection.close()
		print "Remvoing Connection From Connected List."
		self.connected_users.remove(connection)
		print "Calling Exit."
		for thread in threading.enumerate():
			if thread.name == "thread "+str(connection):
				print "Killing Thread: thread" + str(connection)
				sys.exit()
		
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
		command, parameters = self.unpack(menu_response)
		if DEBUG:
			print "[!] Command: ", command
			print "[!] Parameters: ", parameters

		if command in self.functions:
			parameters.append(connection)
			self.functions[command](parameters)
		else:
			self.run_game(game,connection)


	""" Listens for users connecting to the server and initializes connections. """
	def start(self):
		while True:
			connection, address = self.s.accept()
			if DEBUG:
				print "New Connection: ", connection
				print "New Address: ", address
			if connection not in self.connected_users:
				self.connected_users.append(connection)
				player_thread = threading.Thread(name = "thread "+str(connection), target = self.run, args = (connection,))
				player_thread.daemon = True
				player_thread.start()

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
				self.send(connection, "response_required@" + menu.get_user_name())
				user_name = self.receive(connection)
				if DEBUG:
					print "." + user_name + "."
			password = ""
			while not menu.valid_input_string(password):
				time.sleep(SLEEP)
				self.send(connection, "response_required@" + menu.get_user_password())
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
			if connection == None:
				print "[!] Connection is None."	
			time.sleep(SLEEP)
			self.send(connection, "response_required@" + menu.prompt() + "\n[!] Please Select An Option.\n")
			user_response = self.receive(connection)
			if DEBUG: 
				print "[!] Checking " + "." + user_response + "."
			if DEBUG:
				print "[!] Calling server process with " , user_response
			command = menu.process(user_response)
			if command != "fail":
				self.process(command, connection)
			else:
				self.send(connection, "\n[-] Invalid Selection.\n")

	def games_list(self,parameters):
		connection = parameters[0]
		if len(self.games) > 0:
			prompt = "\n".join([ "Game: " + str(game.number) for game in self.games ])
			self.send(connection, "response_required@ " + "[+] Please Enter The Number For A Game From The List Of Games.\n" + prompt + "\n")
		else:
			connection.send( "There Are Currently No Games.\n")
			self.game(connection)

		selection = self.receive(connection)
		print "[+] Request To Join Game: " + str(selection)
		if int(selection) <= len(self.games):
			self.send(connection, "[!] Attempting to join Game " + str(selection))
			select = int(selection)
			player = Player(self.user_lookup[connection], connection)
			self.join_game(player, self.games[select])

	def join_game(self, player, game):
		self.send(player.connection, "[!] Please Wait While You Are Connected To Game " + str(game.number)+ "...\n") 
		self.game_lookup[player] = game
		self.players_lookup[game].append(player)
		game.add_player(player)
		while player in game.players:
			pass
		self.hall_of_fame[player.name] += player.score
		self.hall_of_fame_repo.save(self.hall_of_fame)
		self.game(player.connection)

	""" Allows user to pick a username and password for account creation. """
	def signup(self,connection):
		menu = Signup() 
		self.send(connection, menu.welcome())
		while True:

			self.send(connection, "response_required@ " + menu.pick_user_name())
			user_name = self.receive(connection)

			self.send(connection, "response_required@ " + menu.pick_user_password())
			password = self.receive(connection)

			if user_name not in self.accounts:
				self.make_user([user_name,password])
				self.send(connection, menu.successful_signup())
				self.hall_of_fame[user_name] = 0
				self.accounts_repo.save(self.accounts)
				self.hall_of_fame_repo.save(self.hall_of_fame)
				return
			else:
				self.send(connection, "[-] Account Creation Failed. That User Name Is Already Taken.\n")

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
				else:
					self.send(connection, "[-] Invalid Selection.") 

		
	def create_new_game(self,parameters):
		print self.user_lookup
		if len(parameters) > 1:
			connection = parameters[1]
			user = self.user_lookup[connection]
			player = Player(user, connection)
			game = HangMan(parameters[0],words = self.words, game_id = len(self.games))
			game.add_player(player)
			self.games.append(game)
			self.game_lookup[player] = game
			self.players_lookup[game] = [player]
			if DEBUG:
				print " [!] Creating A New Game With " + str(parameters[0]) + " Difficulty."
			self.run_game(game)
			self.games.remove(game)
			del self.players_lookup[game]
			del self.game_lookup[player]
			self.hall_of_fame[player.name] += player.score
			self.hall_of_fame_repo.save(self.hall_of_fame)
			self.game(connection)
			
	
	def run_game(self, game):
		for player in game.players:
			self.send(player.connection, game.welcome()+ "\n")

		game_over = False
		occurences = 0
		while not game_over:
			for connection in self.connected_users:
				self.send(connection, "Players:" + ", ".join([player.name for player in game.players]))
		
			if occurences == 0:
				current_turn = game.update_turn()

			for player in game.players:
				self.send(player.connection, "\n***********************\n***     HANGMAN     ***\n***********************\n[+] Game " + str(game.number) + "\n" +  " On " + str(game.difficulty).upper() + " Difficulty\n") 
				self.send(player.connection, game.get_state() + "\n" + "It is " + game.turn.name + "'s turn!.\n")

			self.send(game.turn.connection, "response_required@" + "[+] It's Your Turn. Please Guess A Character.")
			c = self.receive(game.turn.connection)
			occurences = game.character_guess(c)
			if occurences == -1:
				player = game.turn
				self.send(player.connection, "[-] Incorrect Word Guess. Goodbye.")
				current_turn = game.update_turn()
				game.remove_player(player)
			else:
				game.update_player_state(current_turn, occurences)
				game_over = game.is_over(occurences)

		for player in game.players:
			self.send(player.connection, "\n***********************\n***     HANGMAN     ***\n***********************\n[+] Game " + str(game.number) + "\n" +  "[+] On " + str(game.difficulty).upper() + " Difficulty\n") 
			self.send(player.connection, game.get_state())
			self.send(player.connection, "[!] Game Over.\n The Winner is " + game.turn.name + ". :^] Returning To The Game Menu...")
		return True
		

	def hall(self, parameters, number=3):
		connection = parameters[0]
		hall = ""
		i = 0
		limit = number
		if len(self.hall_of_fame) == 0:
			self.send(connection, "\n[+] The Hall Of Fame Is Empty. It's Your Time To Shine!\n")
		if len(self.hall_of_fame) < 3:
			limit = len(self.hall_of_fame)
		self.send(connection, "\n ********************************** \n *****      HALL OF FAME      ***** \n ********************************** \n\n")
		for name in sorted(self.hall_of_fame, key=self.hall_of_fame.get, reverse=True):
			i += 1
  			self.send(connection, name + "     " + str(self.hall_of_fame[name]) + "\n")	
			if i == limit:
				self.send(connection, "\n")
				return

	def admin_process(self, selection):
		if selection == "users":
			print "\n".join([name for name in self.accounts.keys()])
			
		if selection == "words":
			print "\n".join(self.words)

		if selection == "add_word":
			self.words.append(raw_input("Enter Your Word To Add To The List Of Words: \n"))
			self.words_repo.save(self.words)
			
	
	def sever_menu(self):
		menu = SeverMenu()
		while True:
			print menu.welcome()
			self.admin_process(menu.process(raw_input(menu.prompt() +"\n[+] Enter Response: ")))

	
if __name__ == "__main__":

	accounts = Repository("accounts.pkl")
	hall = Repository("hall.pkl")
	words = Repository("words.pkl")
	server = Server(accounts, hall, words)

	server_menu = threading.Thread(target=server.sever_menu, args=())
	server_menu.daemon = True
	server_menu.start()

	server.start()
