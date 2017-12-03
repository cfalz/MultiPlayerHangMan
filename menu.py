# CODY FALZONE 
import sys

DEBUG = False


class Menu(object):
	def __init__(self):
		self.welcome_message = "[!] Base Class Welcome Message."
		self.prompt_message = "[!] Base Class Prompt Message."
		self.number_of_options = None

	def hall(self):
		return "hall"

	def exit(self):
		return "\n[-] Goodbye!"

	def welcome(self):
		return self.welcome_message

	def prompt(self):
		return self.prompt_message

	def valid_input_string(self, input_string):
		if input_string == "":
			return False
		return True

	def empty_respose(self):
		return "\n[-] It looks like you entered Nothing.\n"

	def process(self, selection):
		raise NotImplementedError

	def valid_option(self, selection):
		return selection > 0 and selection <= self.number_of_options

	
class Initial(Menu):
	def __init__(self):
		super(Initial,self).__init__()
		self.welcome_message = "[+] Welcome to The Multiplayer Hangman!"
		self.prompt_message = "1. Login \n2. Make New User\n3. Hall Of Fall\n4. Exit\n"
		self.number_of_options = 4

	def process(self,selection):
		if DEBUG:
			print "[!] In Menu Process..."
			print "Selection: " + str(selection)

		if selection.isdigit():	
			if self.valid_option(int(selection.strip())): 
				if int(selection) == 1: 
					return "update_menu login"
				if int(selection) == 2: 
					return "update_menu make_user"
				if int(selection) == 3: 
					return  "hall"
				if int(selection) == 4: 
					return "exit"

		return "fail"

class Login(Menu):
	def __init__(self):
		super(Login,self).__init__()
		self.welcome_message ="[+] Let's Get You Logged In! \n"
		
	def get_user_name(self):
		return "\n[!] Enter Your User Name.\n"

	def get_user_password(self):
		return "\n[!] Enter Your Password.\n"

	def successful_login(self, user_name):
		return "[+] Greetings " + str(user_name) + "! \n[+] Fetching Your Information....\n"

class Signup(Menu):
	def __init__(self):
		super(Signup,self).__init__()
		self.welcome_message ="\n[+] Let's Create An Account For You.\n[+] Please Choose A User Name and Password. It will be used if not already taken. \n"

	def pick_user_name(self):
		return "\n[!] What would you like as your User Name?\n"

	def pick_user_password(self):
		return "\n[!] What would you like as Password?\n"

	def successful_signup(self):
		return "\n[!] Account Creation Successful."
		



class Game(Menu):
	def __init__(self):
		super(Game,self).__init__()
		self.welcome_message = "[+] You Have Logged In! Let's Get Playing!\n"
		self.prompt_message = "1. Start A New Game\n2. Get A List Of The Current Games\n3. Hall Of Fame\n4. Exit\n" 
		self.number_of_options = 4
	
	def process(self,selection):
		if DEBUG:
			print "[!] In Menu Process..."
			print "Selection: " + str(selection)
 		if selection.isdigit():	
			if self.valid_option(int(selection.strip())):
				if int(selection) == 1: 
					return "update_menu start_new_game"
				if int(selection) == 2: 
					return "games_list"
				if int(selection) == 3: 
					return  "hall"
				if int(selection) == 4: 
					return "exit"
		return "fail"

	
class StartNewGame(Menu):
	def __init__(self):
		super(StartNewGame, self).__init__()
		self.welcome_message = "[+] Lets Start A New Game."
		self.prompt_message = "[!] Please Select A Difficulty.\n1. Easy\n2. Medium\n3. Hard\n4. Exit\n"
		self.difficulty_lookup = {"1" : "easy","2" : "medium","3" : "hard"}
		self.number_of_options = 4
	
	def process(self,selection):
		if DEBUG:
			print "[!] In Menu Process..."
			print "Selection: " + str(selection)
 		if selection.isdigit():	
			if self.valid_option(int(selection.strip())):
				return "create_new_game " + self.difficulty_lookup[str(selection)]

class SeverMenu(Menu):
	def __init__(self):
		super(SeverMenu,self).__init__()
		self.welcome_message = "||||||||||||||||||||||||||\n||||||| Sever Menu ||||||| \n||||||||||||||||||||||||||\n"
		self.prompt_message = "1. Current List Of Users \n2. Current List Of Words \n3. Add New Word \n"
		self.number_of_options = 3

	def process(self,selection):
		if DEBUG:
			print "[!] In Menu Process..."
			print "Selection: " + str(selection)
 		if selection.isdigit():	
			if self.valid_option(int(selection.strip())):
				if int(selection) == 1: 
					return "users"
				if int(selection) == 2: 
					return "words"
				if int(selection) == 3: 
					return  "add_word"
	
if __name__ == "__main__":
	instance = ClientMenu()
	#username, password = instance.make_user()
	username, password = instance.login()

	print username
	print password

