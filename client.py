import socket
from menu import *

DEBUG = True

class Client(object):
	def __init__(self,host="localhost",port=9047):
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
		self.menu = Initial()

		try:
			self.s.connect((self.host,self.port))
			print "[+] Connected To Server Successful."
			data = self.s.recv(1024)
			print data
			
		except socket.error:
			print "[-] Failed To Connect To Server."
			sys.exit()

	def receive(self):
		return self.s.recv(1024)

	def package(self,response):
		return response

	def unpack(self,response):
		if server_response != "":
			r = server_response.strip().split()
			if DEBUG:
				print "Server Response: " , r
			if len(r) > 1:
				return r[0],r[1:]
			elif len(r) == 1:
				return r[0]
			else:
				print  "[-] Empty Server Response."
				sys.exit()

	def update_menu(self,menu):
		if menu == "initial":
			self.menu = Initial()
		elif menu == "game":
			self.menu = Game()
		else:
			raise ValueError("[-] Unrecognized Menu Option.")
		
		
	def process(self,command,parameters):
		if DEBUG:
			print "Processing " + str(command) + str(parameters)
		if command == "game":
			if len(parameters) > 0:
				if parameters[0] == "success":
					print "[+] Login Successful.\n" 
					self.update_menu(command)
			
		if command == "initial":
			if len(parameters) > 0:
				if parameters[0] == "success":
					print "[+] Account Created Successfully.\n" 
				elif parameters[0] == "fail":
					if len(parameters) == 2: 
						if parameters[1] == "login":
							print "[+] Incorrect User Name Or Password.\n" 
						if parameters[1] == "make_user":
							print "[+] Sorry, That Account Name Is Already Taken.\n"
			else:
				raise ValueError("[-] No Parameters Found In Sever Response.")
			self.update_menu(command)
		if command == "hall":
			if len(parameters) > 0:
				if parameters[0] == "False":
					print "[!] No Hall Of Fame Record! It Is Your Time To Shine!\n"
				else:
					print "[+] Hall Of Fame: \n"
					print parameters[0]
		

	def send(self,packet):
		self.s.send(packet)

	def start(self):
		return self.menu.start()


if __name__ == "__main__":
	client = Client()
	while True:
		user_response = client.start()
		print user_response
		packet = client.package(user_response)
		if DEBUG:
			print "Sending Packet ", packet
		client.send(packet)
		server_response = client.receive()
		if DEBUG:
			print server_response
		command, parameters = client.unpack(server_response)
		client.process(command, parameters)	
			
		



