from tkinter import *
import tkinter.messagebox
from PIL import Image, ImageTk
import socket, threading, sys, traceback, os
import time
from RtpPacket import RtpPacket

CACHE_FILE_NAME = "cache-"
CACHE_FILE_EXT = ".jpg"

class Client:
	INIT = 0
	READY = 1
	PLAYING = 2
	state = INIT
	
	SETUP = 0
	PLAY = 1
	PAUSE = 2
	TEARDOWN = 3

	checkSocketIsOpen = FALSE
	checkPlay = FALSE
	buffer = [None] * 1024
	# Initiation..
	def __init__(self, master, serveraddr, serverport, rtpport, filename):
		self.master = master
		self.master.protocol("WM_DELETE_WINDOW", self.handler)
		self.createWidgets()
		self.serverAddr = serveraddr
		self.serverPort = int(serverport)
		self.rtpPort = int(rtpport)
		self.fileName = filename
		self.rtspSeq = 0
		self.sessionId = 0
		self.requestSent = -1
		self.teardownAcked = 0
		self.connectToServer()
		self.frameNbr = 0
		
	# THIS GUI IS JUST FOR REFERENCE ONLY, STUDENTS HAVE TO CREATE THEIR OWN GUI 	
	def createWidgets(self):
		"""Build GUI."""
		# Create Setup button
		self.setup = Button(self.master, width=20, padx=3, pady=3)
		self.setup["text"] = "Setup"
		self.setup["command"] = self.setupMovie
		self.setup.grid(row=1, column=0, padx=2, pady=2)
		
		# Create Play button		
		self.start = Button(self.master, width=20, padx=3, pady=3)
		self.start["text"] = "Play"
		self.start["command"] = self.playMovie
		self.start.grid(row=1, column=1, padx=2, pady=2)
		
		# Create Pause button			
		self.pause = Button(self.master, width=20, padx=3, pady=3)
		self.pause["text"] = "Pause"
		self.pause["command"] = self.pauseMovie
		self.pause.grid(row=1, column=2, padx=2, pady=2)

		# Create Teardown button
		self.teardown = Button(self.master, width=20, padx=3, pady=3)
		self.teardown["text"] = "Teardown"
		self.teardown["command"] =  self.exitClient
		self.teardown.grid(row=1, column=3, padx=2, pady=2)
		
		# Create a label to display the movie
		self.label = Label(self.master, height=19)
		self.label.grid(row=0, column=0, columnspan=4, sticky=W+E+N+S, padx=5, pady=5) 
	
	def setupMovie(self):
		"""Setup button handler."""
	#TODO
	
	def exitClient(self):
		"""Teardown button handler."""
	#TODO

	def pauseMovie(self):
		"""Pause button handler."""
	#TODO
	
	def playMovie(self):
		"""Play button handler."""
	#TODO
	
	def listenRtp(self):		
		"""Listen for RTP packets."""
		#TODO
					
	def writeFrame(self, data):
		"""Write the received frame to a temp image file. Return the image file."""
	#TODO
	
	def updateMovie(self, imageFile):
		"""Update the image file as video frame in the GUI."""
	#TODO
		
	def connectToServer(self):
		"""Connect to the Server. Start a new RTSP/TCP session."""
		self.rtspSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.rtspSocket.connect((self.serverAddr, self.serverPort))
		except:
			tkinter.messagebox.showwarning('Connection Failed', 'Connect to \'%s\'  failed.' %self.serverAddr)
	#TODO
	
	def sendRtspRequest(self, requestCode):
		"""Send RTSP request to the server."""
		if requestCode == self.SETUP and self.state == self.INIT:
			self.rtspSeq = self.rtspSeq + 1
			message = "C: SETUP " + self.fileName + " RTSP/1.0 \
			C: CSeq: " + str(self.rtspSeq) + "C: Transport: RTP/UDP; client_port = " + str(self.rtpPort)
			self.rtspSocket.sendto(message.encode(), (self.serverAddr, self.serverPort))
			self.state = self.READY
		elif requestCode == self.PLAY and self.state == self.READY:
			self.rtspSeq = self.rtspSeq + 1
			message = "C: PLAY " + self.fileName + " RTSP/1.0 \
			C: CSeq: " + str(self.rtspSeq) + "C: Session: " + str(self.sessionId)
			self.rtspSocket.sendto(message.encode(), (self.serverAddr, self.serverPort))
			self.state = self.PLAYING
		elif requestCode == self.PAUSE and self.state == self.PLAYING:
			self.rtspSeq = self.rtspSeq + 1
			message = "C: PAUSE " + self.fileName + " RTSP/1.0 \
			C: CSeq: " + str(self.rtspSeq) + "C: Session: " + str(self.sessionId)
			self.rtspSocket.sendto(message.encode(), (self.serverAddr, self.serverPort))
			self.state = self.PLAYING
		elif requestCode == self.TEARDOWN:
			self.rtspSeq = self.rtspSeq + 1
			message = "C: TEARDOWN " + self.fileName + " RTSP/1.0 \
			C: CSeq: " + str(self.rtspSeq) + "C: Session: " + str(self.sessionId)
			self.rtspSocket.sendto(message.encode(), (self.serverAddr, self.serverPort))
			self.state = self.INIT
		#-------------
		# TO COMPLETE
		#-------------

	def recvRtspReply(self):
		"""Receive RTSP reply from the server."""
		#TODO

	def parseRtspReply(self, data):
		"""Parse the RTSP reply from the server."""
		#TODO
	
	def openRtpPort(self):
		"""Open RTP socket binded to a specified port."""
		#-------------
		# TO COMPLETE
		#-------------
		# Create a new datagram socket to receive RTP packets from the server
		# self.rtpSocket = ...

		# Set the timeout value of the socket to 0.5sec
		# ...
		self.checkSocketIsOpen = TRUE
		self.rtspSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # IPv4, UDP
		try:
			self.rtspSocket.bind(('', self.rtpPort))
			self.state = self.READY
		except:
			tkinter.messagebox.showwarning('Unable to bind', 'Unable to bind port=%d' %self.rtpPort)
	def handler(self):
		"""Handler on explicitly closing the GUI window."""
		#TODO
