import pickle
from words import wordlist

"""By Default the Repository Class Uses a Dictonary for the Database. Open to Extension to allow for any in the future. Just Inherit. """
class Repository(object):

	def __init__(self, filename):
		self.filename = filename

	def get_data(self):
		try:
			return pickle.load(open(self.filename, 'rb'))
		except:
			return {}

	def save(self, d):
		pickle.dump(d, open(self.filename, 'wb'))

class WordList(Repository):
	def __init__(self, filename):
		super(WordList,self).__init__(filename)

	def get_data(self):
		try:
			data = pickle.load(open(self.filename, 'rb'))
			return data
			if data == None:
				return []
		except:
			return []

		
	def save(self, l):
		pickle.dump(l, open(self.filename, 'wb'))


if __name__ == "__main__":
	w = WordList("words.pkl")
	w.save(wordlist)
	l = w.get_data()
	print l
	l.append("mediation")
	l.append("algorithm")
	w.save(l)
	print "New List", w.get_data()
	

