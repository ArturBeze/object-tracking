#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 21:20:58 2024

@author: artur
"""

import sys
import platform
import argparse
from pyfirmata2 import Arduino, SERVO
from PyQt5.QtSerialPort import QSerialPortInfo
from PyQt5 import QtWidgets, uic

class BoardController(Arduino):
	def __init__(self, *args, **kwargs):
		args = list(args)
		if "Mac" or "Darwin" in platform.system():
			args[0] = f"/dev/{args[0]}" #port = '/dev/tty.usbmodem11401'# Mac
			#pass
		elif "Linux" in platform.system():
			args[0] = f"/dev/{args[0]}" #port = '/dev/ttyACM3' # Linux
			#pass
		elif "Windows" in platform.system():
			args[0] = f"{args[0]}" #port = 'COM3'# Windows
			#pass
		else:
			raise ValueError("Unknown platform")
		super(BoardController, self).__init__(*args, **kwargs)
		
	def setupServo(self, horPIN, verPIN):
		self.horPIN = horPIN
		self.verPIN = verPIN
		self.digital[horPIN].mode = SERVO
		self.digital[verPIN].mode = SERVO
		
	def setServo(self, horVal=None, verVal=None):
		if horVal:
			horVal = min(max(45, horVal), 135)
			self.digital[self.horPIN].write(horVal)
		if verVal:
			verVal = min(max(45, verVal), 135)
			self.digital[self.verPIN].write(verVal)

def main():
	def horMove(val):
		board.setServo(horVal = val)
	
	def verMove(val):
		board.setServo(verVal = val)
	
	ports = QSerialPortInfo().availablePorts()
	for port in ports:
		if "Arduino" in port.manufacturer():
			board = BoardController(port.portName())
			break
	else:
		raise ValueError("Arduino device is not connected")
	
	parser = argparse.ArgumentParser(description="")
	parser.add_argument("--horPIN", type=int, default=8, help="horizontal servo motor PWM PIN")
	parser.add_argument("--verPIN", type=int, default=9, help="vertical servo motor PWM PIN")
	args = parser.parse_args()

	board.setupServo(args.horPIN, args.verPIN)
	board.setServo(90, 90)
	
	app = QtWidgets.QApplication(sys.argv)
	
	ui = uic.loadUi("mainGUI.ui")
	ui.setWindowTitle("TesterGUI")
	ui.horS.valueChanged.connect(horMove)
	ui.verS.valueChanged.connect(verMove)
	ui.show()
	sys.exit(app.exec())

if __name__ == "__main__":
	main()