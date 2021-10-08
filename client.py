from socket import AF_INET, socket, SOCK_STREAM
""" here, we are importing the socket library, AF_INET refers to the address-family ipv4. 
The SOCK_STREAM means connection-oriented TCP protocol.
Using these we can connect to a server """

from threading import Thread
"""threading allows  to run different parts of the program run simultaneously, which is necessary
In this case, we’re running run the client and the server on the same PC simultaneously for 
the chatbot to work and also for simplicity """

import tkinter     #We are using the tkinter module to develop the graphical user interface (GUI) for our chatbot

def receiveMessage():
	"""This Handles receiving of messages"""

	while True:
		try:
			msg = client_socket.recv(BUFSIZ).decode("utf8")   #We Used this method to receive messages at endpoints
			msgList.insert(tkinter.END, msg)
		except OSError:		        #If the client leaves the chat
			break

def sendMessage(event=None):
	""" Event passed by Tkinter GUI. This handles sending of messages"""
	msg = message.get()
	message.set("")
	client_socket.send(bytes(msg, "utf8"))       #We Used this method to send messages at endpoints
	if msg == "{QUIT}":
		client_socket.close()                    #We used this method to close the socket
		top.quit()                               #top. quit() is used to kill mainloop

def closeWindow(event=None):
	"""This function is to be called when the window is closed."""
	message.set("{QUIT}")
	sendMessage()


top = tkinter.Tk()                #This instance helps to display the root window
top.title("Chatbot")              #this will be displayed on the top of our chat window
top.geometry("600x620")           #defining the size of our window

"""Here, we are passing the path to the image to the file argument to create a new PhotoImage object."""
filename = tkinter.PhotoImage(file="background.png")
background_label = tkinter.Label(top, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)      #setting the background image

frame = tkinter.Frame(top)      #creating a frame

message = tkinter.StringVar()        #here we are taking client's input
message.set("Type your message!")    #this will display on the typing window where the client will type messages

scrollbar = tkinter.Scrollbar(frame, bg="#251f36")  #creating a scrollbar
"""creating a listbox object"""
msgList = tkinter.Listbox(frame, height=25, width=30, yscrollcommand=scrollbar.set, bg="#251f36", fg="white")
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msgList.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msgList.pack()
frame.pack(pady=20)

# creating a entry for input, message using widget Entry
entry_field = tkinter.Entry(top, textvariable=message, bg="#251f36", fg="white")
entry_field.bind("<Return>", sendMessage)

# creating a button using the widget, Button that will call the Send Message function
send_button = tkinter.Button(top, text="Send", command=sendMessage, highlightbackground="#000000", width=8)
entry_field.pack(side=tkinter.LEFT, padx=(55, 10))
entry_field.config(highlightbackground="black")
send_button.pack(side=tkinter.LEFT, fill=tkinter.X)


'''
Here we are creating the input field 
'''
top.protocol("WM_DELETE_WINDOW", closeWindow)
HOST = 'Local Ip Address'
PORT = 4444
BUFSIZ = 1024
ADDR = (HOST, PORT)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

#begin the thread
receive_thread = Thread(target=receiveMessage)
receive_thread.start()
tkinter.mainloop()
