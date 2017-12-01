import socket
import time
from menu import *

DEBUG = 0

class Client(object):
	def __init__(self,host="localhost",port=9046):
		try:
			self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			if DEBUG:
				print "Socket Created."
		except socket.error:
			if DEBUG:
				print "Failed to create socket"
			sys.exit()
		
		self.host = host
		self.port = port
		self.game = None

		try:
			self.s.connect((self.host,self.port))
			print "[+] Connected To Server Successful."
			data = self.s.recv(1024)
			print data
			
		except socket.error:
			print "[-] Failed To Connect To Server."
			sys.exit()

	def receive(self):
		return self.s.recv(16384)


	def send(self):
		while True:
			user_response = raw_input("[Enter Reponse]: ")
			if user_response != "":
				time.sleep(0.1)
				self.s.send(user_response)
				return
			print "[-] It Looks Like You Entered Nothing..."

	def exit(self, message):
		if len(message.split("quit ")) > 1:
			return True
		return False
		
	def response_required(self, message):
		if len(message.split("@")) > 1:
			return True
		return False
		

if __name__ == "__main__":
	client = Client()
	while True:
		data = client.receive()
		
		if client.response_required(data):
			print data.split("@")[1]
			client.send()
		elif client.exit(data):
			print data.split("quit")[1]
			sys.exit()
		else:
			if data != "":
				print data
			
