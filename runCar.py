#coding=utf-8

from gpiozero import *
import os,time
import threading
import Queue
#import readchar
import lircinput

class ListQueue(Queue.Queue):
	def _init(self,maxsize):
		self.maxsize = maxsize
		self.queue = []
	def _put(self,item):
		self.queue.append(item)
	def _get(self):
		return self.queue.pop()


class DriveMotor(threading.Thread):
	def __init__(self,myqueue):
		threading.Thread.__init__(self)
		self.myqueue = myqueue

		#电机控制IO
		self.ton = LED(17)

		#左侧电动机控制
		self.ain1 = LED(16)
		self.ain2 = LED(13)
		
		#右侧电动机控制
		self.bin1 = LED(19)
		self.bin2 = LED(20)

		#左侧电机全速
		self.msa = LED(12)
		#右侧电机全速
		self.msb = LED(21)

	def up(self):
		#控制开关打开
		self.ton.on()

	        #左侧电机前进
	        self.ain1.on()
	        self.ain2.off()
	
	        #右侧电机前进
	        self.bin1.on()
	        self.bin2.off()

	def down(self):
	        #左侧电机后退
	        self.ain1.off()
	        self.ain2.on()
	
	        #右侧电机后退
	        self.bin1.off()
	        self.bin2.on()

	def turn_left(self):
	        #左侧电机停
	        self.ain1.off()
	        self.ain2.off()
	
	        #右侧电机前进
	        self.bin1.on()
	        self.bin2.off()

	def turn_right(self):
	        #左侧电机前进
	        self.ain1.on()
	        self.ain2.off()
	
	        #右侧电机停
	        self.bin1.off()
	        self.bin2.off()

	def bark(self):
	        #左侧电机停
	        self.ain1.off()
	        self.ain2.off()
	
	        #右侧电机停
	        self.bin1.off()
	        self.bin2.off()


	def run(self):
		#单片机IO口打开,接受控制
		self.ton.on()
		
		self.msa.on()
		self.msb.on()
	
		#time.sleep(1)
		while True:
		        time.sleep(1)
			motorAction = self.myqueue.get()
			print('motorAction is {}\n'.format(motorAction))
			if(motorAction == 'w'):
				self.up()
			if(motorAction == 's'):
				self.down()
			if(motorAction == 'a'):
				self.turn_left()
			if(motorAction == 'd'):
				self.turn_right()
			if(motorAction == 'h'):
				self.bark()
			if(motorAction == 'x'):
				self.ton.off()

			#time.sleep(1)


def main():
	queue = ListQueue(5)

	thd = DriveMotor(queue)
	thd.start()

	kp=lircinput.KeyPress()
	
	fnForward   = lambda:queue.put('w')
	fnBackward  = lambda:queue.put('s')
	fnTurnLeft  = lambda:queue.put('a')
	fnTurnRight = lambda:queue.put('d')
	fnBark      = lambda:queue.put('h')
	fnOff      = lambda:queue.put('x')
	
	keyMap = {\
	    'KEY_NUMERIC_2':fnForward,\
	    'KEY_NUMERIC_5':fnBackward,\
	    'KEY_NUMERIC_4':fnTurnLeft,\
	    'KEY_NUMERIC_6':fnTurnRight,\
	    'KEY_NUMERIC_8':fnBark,\
	    'KEY_NUMERIC_7':fnOff}
	
	kp.registerQuitKey('KEY_NUMERIC_9')
	kp.registerHandlers(keyMap)
	kp.start()

if __name__ == '__main__':
	main()
