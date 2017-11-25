from menu import *

class Player(object):
	def __init__(self, connection):
		self.connection = connection
		self.user_name = None
		self.password = None
		self.menu = None
		self.functions = { 
					"send" : self.send,
					"update_menu" : self.update_menu,
					"hall" : self.hall,
					"exit" : self.exit
				 }


	def send(self, message_to_user):
		self.connection.send(message_to_user)

	def greet(self):
		self.send("[+] Greetings From the Hangman Server.")

	def welcome(self):
		self.send(self.menu.welcome())

	def prompt(self):
		self.send(self.menu.prompt())

	def receive(self):
		while True:
			selection = self.connection.recv(1024))
			if self.valid_user_selection(selection):
				return selection
			self.connection.send( "[-] Please Enter An Integer Value Corresponding To A Valid Option." ) 

	def make_user(self, username, password):

	def update_menu(self, menu):
		self.menu = menu

	def valid_input_string(self, input_string):
		return self.menu.valid_input_string(input_string)
	
	def valid_user_selection(self, selection):
		return self.menu.valid_option(selection):

	def process(self, user_reponse):
		command, parameters = menu.process(user_response)
		if command in self.functions and len(parameters) > 0:
			self.functions[command]()
		elif command in self.functions:
			self.functions[command](parameters)
		else:
			raise ValueError(" [-] Recevied Unknown Command and Parameters Combination.\n Command: " + str(command) + "\nParameters: " + str(parameters) + "\n")
		

	def initialize(self):
		self.menu = Initial()
		self.menu.welcome()
		while True:
			self.menu.prompt()
			user_response = self.receive()
			self.process(user_reponse)

	def login(self):
		self.menu = Login()
		self.menu.welcome()
		while not valid_input_string(user_name):
			user_name = self.process(self.menu.get_user_name())
		self.user_name = user_name
		while not valid_input_string(password):
			password = self.process(self.menu.get_user_password())
		self.password = password
		self.menu.successful_login()

	def signup(self):
		self.menu = Signup() 
		while not valid_input_string(user_name):
			user_name = self.process(self.menu.pick_user_name())
		while not valid_input_string(password):
			password = self.process(self.menu.pick_user_password())
		self.process("make_user" + user_name + password)
		self.menu.successful_signup()
		
		

	
