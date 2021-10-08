from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

# Global variables
from numpy import broadcast
clients = {}
addresses = {}

HOST = 'Local Ip Address'
PORT = 4444
BUFSIZE = 1024
ADDRESS = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)             #Socket Creation
SERVER.bind(ADDRESS)         #This method binds the socket to address


def listen():
	""" Wait for incoming connections """
	print("Waiting for connection...")

	while True:
		# This method returns a socket object which is different from the socket object created earlier
		client, client_address = SERVER.accept()
		print("%s:%s has connected." % client_address)
		client.send(bytes("Enter your name", "utf8"))
		addresses[client] = client_address
		Thread(target=listenToClient, args=(client,)).start()


def listenToClient(client):         #Takes client socket as argument.
	""" Get client username """

	name = client.recv(BUFSIZE).decode("utf8")
	message = "Welcome to the Chatbot %s To exit please type {QUIT}" % name
	client.send(bytes(message, "utf8"))
	msg = "%s joined the chatroom" % name
	broadcast(bytes(msg, "utf8"))
	clients[client] = name
	while True:
		msg = client.recv(BUFSIZE)
		if msg != bytes("{QUIT}", "utf8"):
			sendMessage(msg, name+": ")
		else:
			client.send(bytes("{QUIT}", "utf8"))
			client.close()
			del clients[client]
			sendMessage(bytes("%s left the chat room!" %name, "utf8"))
			break


def sendMessage(msg, name=""):
	""" send message to all users present in
	the chat room"""

	for client in clients:
		client.send(bytes(name, "utf8") + msg)


if __name__ == "__main__":
	SERVER.listen(5)
	ACCEPT_THREAD = Thread(target=listen)
	ACCEPT_THREAD.start()
	ACCEPT_THREAD.join()
	SERVER.close()
