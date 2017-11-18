# CODY FALZONE 
import sys


class Menu(object):
	def __init__(self):
		self.welcome_message = "[!] Base Class Welcome Message."
		self.prompt_message = "[!] Base Class Prompt Message."

	def hall(self):
		return "hall"

	def exit(self):
		print "[-] Goodbye!"
		sys.exit()

	def welcome(self):
		print self.welcome_message

	def prompt(self):
		while True:
			selection = raw_input(self.prompt_message)
			if selection > "0" and selection < "5": 
				return selection
			print "[-] Please Enter An Integer Value Corresponding To A Valid Option."

	def start(self):
		raise NotImplementedError
		
		


class Login(Menu):
	def __init__(self):
		super(Login, self).__init__()
		self.welcome_message = "[+] Let's Get You Logged In!\n"
		self.prompt_message = "[-] Login Prompt Message.\n"

	def start(self):
		while True:	
			user_name = raw_input("[!] Enter Your User Name.\n").strip()
			if user_name == "":
				print "[-] It looks like you entered Nothing, Please Re-Enter Your User Name.\n"	
			else:
				break
		while True:	
			password = raw_input("[!] Enter Your Password.\n").strip()
			if password == "":
				print "It looks like you entered Nothing, Please Re-Enter Your Password.\n"
			else:
				break

		print "[+] Greetings " + str(user_name) + "!"
		print "[+] Fetching Your Information....\n"
		
		return "login" + " " + str(user_name) + " " + str(password)

class MakeUser(Menu):
	def __init__(self):
		super(MakeUser, self).__init__()
		self.welcome_message = "[+] Please Choose A User Name and Password (No Spaces). It will be used if not already taken. \n"
		self.promt_message = "[!] Make User Prompt Called."

	def start(self):
		while True:	
			user_name = raw_input("[!] What would you like as your User Name?\n")
			if user_name == None:
				print "[-] It looks like you entered Nothing, Please Re-Enter Your Desired User Name. \n"	
			break
		while True:	
			password = raw_input("[!] What would you like as Password?\n")
			if password == None:
				print "[-] It looks like you entered Nothing, Please Re-Enter Your Desired Password. \n"	
			break

		return "make_user" + " " + str(user_name) + " " + str(password)

	
class Initial(Menu):
	def __init__(self):
		super(Initial,self).__init__()
		self.welcome_message = "[+] Welcome to The Multiplayer Hangman!"
		self.prompt_message = "1. Login \n2. Make New User\n3. Hall Of Fall\n4. Exit\n"

	def login(self):
		menu = Login()
		return menu.start()

	def make_user(self):
		menu = MakeUser()
		return menu.start()
	
	def start(self):
		self.welcome()	
		selection = self.prompt()
		if int(selection) == 1: 
			return self.login()
		if int(selection) == 2: 
			return self.make_user()
		if int(selection) == 3: 
			return self.hall()
		if int(selection) == 4: 
			self.exit()


class Game(Menu):
	def __init__(self):
		super(Game,self).__init__()
		self.welcome_message = "[+] You Have Logged In! Let's Get Playing!\n"
		self.prompt_message = "1. Start A New Game\n2. Get A List Of The Current Games\n3. Hall Of Fame\n4. Exit\n" 
	
	def start_new_game(self):
		menu = StartNewGame()
		return menu.start()

	def get_list_of_games(self):
		pass

	def start(self):
		self.welcome()
		selection = self.prompt()
		if int(selection) == 1: 
			return self.start_new_game()
		if int(selection) == 2: 
			return self.get_list_of_games()
		if int(selection) == 3: 
			return self.hall()
		if int(selection) == 4: 
			self.exit()
	
class StartNewGame(Menu):
	def __init__(self):
		super(StartNewGame, self).__init__()
		self.welcome_message = "[+] Starting A New Game."
		self.prompt_message = "1. Easy\n2. Medium\n3. Hard\n4. Exit\n"
	
	def easy(self):
		raise NotImplementedError("[!] Implemenation Needed!")

	def medium(self):
		raise NotImplementedError("[!] Implemenation Needed!")

	def hard(self):
		raise NotImplementedError("[!] Implemenation Needed!")

	def start(self):
		selection = self.prompt()
		if int(selection) == 1: 
			return self.easy()
		if int(selection) == 2: 
			return self.medium()
		if int(selection) == 3: 
			return self.hard()
		if int(selection) == 4: 
			self.exit()

if __name__ == "__main__":
	instance = ClientMenu()
	#username, password = instance.make_user()
	username, password = instance.login()

	print username
	print password

