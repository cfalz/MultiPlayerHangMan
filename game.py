from random import *
from words import wordlist

DEBUG = False

class HangMan(object):
	def __init__(self, difficulty="easy", words = wordlist, game_id = 0):
		self.number = game_id
		self.word = words[randint(0,len(words) - 1)]
		self.difficulty = difficulty
		self.welcome_message = "[+] Welcome To HangMan. \n[+] Game Is Set To " + str(self.difficulty).upper() + " Difficulty. \n"
		self.word_state = [ "_" for i in range(len(self.word)) ]
		self.turn = None
		#self.player_score = {}
		self.character_guesses = []
		self.players = []
		#self.connections = []
		self.limit_lookup = { "easy" : 3, "medium" : 2, "hard" : 1 }
		self.limit = self.limit_lookup[self.difficulty] * len(self.word)

	def welcome(self):
		return self.welcome_message

	def add_player(self, player):
		self.players.append(player)
		#self.connections.append(connection)
		#self.player_score[player] = 0

	def character_guess(self, character):
		if len(character) > 1:
			if character == self.word:
				self.word_state = [ c for c in self.word ]
				return len(self.word) 
			else:
				return -1
		if character not in self.character_guesses:
			self.character_guesses.append(character)
			indices = [i for i,word_character in enumerate(self.word) if word_character == character ]
			for index in indices:
				self.word_state[index] = character
			if "".join(self.word_state).count("_") == 0:
				return len(self.word)
			return self.word.count(character)
		return 0

	def update_player_state(self, player, occurences):
		player.score += occurences

	def is_over(self, occurences):
		if occurences == len(self.word):
			return True
		if len(self.character_guesses) == self.limit:
			return True
		if "".join(self.word_state).count("_") == 0:
			occurences = len(self.word)
			self.player_score[player] += occurences
			return True
		return False
		
		
	def get_players_states(self):
		player_states = ""
		for player in self.players:
			player_states += player.name + "       " +  str(player.score)
			#i = self.players.index(name)
			if str(self.turn) == player.name:
				player_states += " * "
			player_states+="\n"
		return player_states
	
	def remove_player(self, player):
		self.players.remove(player)
		
		
	def update_turn(self):
		if self.turn == None:
			self.turn = self.players[0]
			return self.turn
		i = self.players.index(self.turn)
		self.turn = self.players[(i+1)%len(self.players)]
		return self.turn
				
	
	def get_state(self):
		return " ".join(self.word_state) + "\n\n" + self.get_players_states() +"\n[!] Guessed Characters: " + ",".join(self.character_guesses) + "\n"
		

if __name__ == "__main__":
	game = HangMan()
	game.add_player("TomRiddler")
	game_over = False
	while not game_over:
		current_turn = game.update_turn()
		print game.get_state()
		c = raw_input("Enter Guess: ")
		game_over = game.update_player_state(current_turn, c)

	print "[!] Game Over."
	
	
	

	
	
	




