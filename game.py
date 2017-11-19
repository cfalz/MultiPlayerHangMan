from random import *
from words import wordlist

class HangMan(object):
	def __init__(self, difficulty="easy", word = wordlist[randint(0,len(wordlist))]):
		self.word = word
		self.players = []
		self.difficulty = difficulty
		self.welcome_message = "[+] Welcome To HangMan. \n[+] Game Is Set To " + str(self.difficulty) + " Difficulty. \n"
		self.word_state = [ "_" for i in range(len(self.word)) ]
		self.turn = None
		self.players = {}

	def welcome(self):
		print self.welcome_message

	def add_player(self, player):
		self.players[player] = 0
		self.turn = player

	def character_guess(self, character):
		if character in self.word:
			pass
	

	def get_players_states(self):
		player_states = ""
		for name in self.players:
			player_states += name + score[name]
			if self.turn == name:
				player_states += " * "
			player_states+="\n"
		return player_states

	def update_players_states(self):
		pass

	
	
	def state(self):
		state = ""
		for c in self.current_state:
			state += c
		return "game_state " + state
	
	def start(self):
		pass
		
		




	
	
	




