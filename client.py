import socket
import time
from menu import *

DEBUG = True

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
		return self.s.recv(5012)


	def send(self):
		while True:
			user_response = raw_input("[Enter Reponse]: ")
			if user_response != "":
				time.sleep(0.1)
				self.s.send(user_response)
				return
			print "[-] It Looks Like You Entered Nothing..."

	


if __name__ == "__main__":
	client = Client()
	while True:
		print client.receive()
		client.send()
			
		



