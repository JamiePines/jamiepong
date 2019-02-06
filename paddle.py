from graphics import *
import keyboard

class Paddle:
	def __init__(self, window, cen_x, cen_y, speed, isl):
		self.window = window
		self.width = 15			#PAddle width
		self.height = 50		#Paddle Height
		self.cen_x = cen_x		#position x (center)
		self.cen_y = cen_y		#position y (center)
		self.speed = speed		#Paddle speed (pixels per tick)
		self.isl = isl			#Is Left Paddle

		#Create and draw paddle object
		pt1 = Point(cen_x + self.width/2, cen_y + self.height/2)
		pt2 = Point(cen_x - self.width/2, cen_y - self.height/2)
		self.rect = Rectangle(pt1, pt2)
		self.rect.setFill("black")
		self.rect.draw(self.window)

	#Returns the top, bottom, left and right of the paddle
	def top(self):
		return self.cen_y - self.height/2

	def bottom(self):
		return self.cen_y + self.height/2

	def left(self):
		return self.cen_x - self.width/2

	def right(self):
		return self.cen_x + self.width/2

	
	#updates position one tick in time based off of keyboard inputs and bot_input
	def update(self, bot_input):
		if bot_input is "none":
			if self.isl:
				if keyboard.is_pressed('w'):
					self.move(-self.speed)
				elif keyboard.is_pressed('s'):
					self.move(self.speed)
			else:
				if keyboard.is_pressed("up"):
					self.move(-self.speed)
				elif keyboard.is_pressed("down"):
					self.move(self.speed)
		elif bot_input is "up":
			self.move(-self.speed)
		elif bot_input is "down":
			self.move(self.speed)
		else:
			return

	#Undraws from window
	def undraw(self):
		self.rect.undraw()

	#Moves paddle by Y units
	def move(self, dy):
		self.cen_y += dy
		self.rect.move(0, dy)