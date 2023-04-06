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
	checkIsPlaying = FALSE
	buffer = [None] * 2048
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
		while True:
			try:
				data = self.rtpSocket.recv(20480)
				if data:
					rtpPacket = RtpPacket()
					rtpPacket.decode()
					seqNum = rtpPacket.seqNum()
					payload = rtpPacket.getPayload()
					timeStamp = rtpPacket.timestamp()
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
		if self.checkSocketIsOpen:
			if requestCode == self.SETUP and self.state == self.INIT:
				self.rtspSeq = self.rtspSeq + 1
				message = "SETUP " + self.fileName + " RTSP/1.0\n\
				CSeq: " + str(self.rtspSeq) + "\n\
				Transport: RTP/UDP; client_port= " + str(self.rtpPort)
				self.rtspSocket.sendto(message.encode(), (self.serverAddr, self.serverPort))
				self.state = self.READY
				self.requestSent = self.SETUP
			elif requestCode == self.PLAY and self.state == self.READY:
				self.rtspSeq = self.rtspSeq + 1
				message = "PLAY " + self.fileName + " RTSP/1.0\n\
				CSeq: " + str(self.rtspSeq) + "\n\
				Session: " + str(self.sessionId)
				self.rtspSocket.sendto(message.encode(), (self.serverAddr, self.serverPort))
				self.state = self.PLAYING
				self.requestSent = self.PLAY
			elif requestCode == self.PAUSE and self.state == self.PLAYING:
				self.rtspSeq = self.rtspSeq + 1
				message = "PAUSE " + self.fileName + " RTSP/1.0\n\
				CSeq: " + str(self.rtspSeq) + "\n\
				Session: " + str(self.sessionId)
				self.rtspSocket.sendto(message.encode(), (self.serverAddr, self.serverPort))
				self.state = self.PLAYING
				self.requestSent = self.PAUSE
			elif requestCode == self.TEARDOWN:
				self.rtspSeq = self.rtspSeq + 1
				message = "TEARDOWN " + self.fileName + " RTSP/1.0\n\
				CSeq: " + str(self.rtspSeq) + "\n\
				Session: " + str(self.sessionId)
				self.rtspSocket.sendto(message.encode(), (self.serverAddr, self.serverPort))
				self.state = self.INIT
				self.requestSent = self.TEARDOWN
				self.rtspSocket.close()
		#-------------
		# TO COMPLETE
		#-------------

	def recvRtspReply(self):
		"""Receive RTSP reply from the server."""
		while True:
			replyMessage = self.rtspSocket.recvfrom(1024)
			if replyMessage:
				self.parseRtspReply(replyMessage.decode("UTF-8"))
			if self.requestSent == self.TEARDOWN:
				self.rtspSocket.shutdown(socket.SHUT_RDWR)
				self.rtspSocket.close()
				break
		#TODO

	def parseRtspReply(self, data):
		"""Parse the RTSP reply from the server."""
		# data = self.recvRtspReply()
		# response = data.split(' ')
		# if response[2] == 'OK':
		# 	self.checkIsPlaying = TRUE
		# else:
		# 	tkinter.messagebox.showwarning('Request Failed', 'Send request to \'%s\'  failed.' %self.serverAddr)
		lines = data.split('\n')
		seqNum = lines[1].split(' ')[1]
		if seqNum == self.rtspSeq:
			session = lines[2].split(' ')[1]
			if session == self.sessionId:
				replyCode = lines[0].split(' ')[1]
				if replyCode == '200':
					if self.requestSent == self.SETUP and self.state == self.INIT:
						self.state = self.READY
					elif self.requestSent == self.PLAY and self.state == self.READY:
						self.state = self.PLAYING
					elif self.requestSent == self.PAUSE and self.state == self.PLAYING:
						self.state = self.READY
					elif self.requestSent == self.TEARDOWN and not self.state == self.INIT:
						self.state = self.INIT
						self.teardownAcked = 1
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
		self.rtpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # IPv4, UDP
		self.checkSocketIsOpen = TRUE
		self.rtpSocket.settimeout(0.5)
		try:
			self.rtpSocket.bind(('', self.rtpPort))
			self.state = self.READY
		except:
			tkinter.messagebox.showwarning('Unable to bind', 'Unable to bind port=%d' %self.rtpPort)
	def handler(self):
		"""Handler on explicitly closing the GUI window."""
		#TODO
