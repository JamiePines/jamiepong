from graphics import *

class PongBall:
	def __init__(self, window, vx, vy, ball_speedup, cen_x, cen_y, radius, miny, maxy, lpaddle, rpaddle):
		self.window = window
		self.vx = vx 				#velocity in the x direction
		self.vy = vy 				#velocity in the y direction
		self.cen_x = cen_x 			#x coordinate of the center
		self.cen_y = cen_y 			#y coordinate of the center
		self.radius = radius		
		self.miny = miny			#Position of the top ceiling
		self.maxy = maxy			#position of the bottom ceiling
		self.lastcollision = None	#Last paddle collided with (prevents multiple collisions with same paddle)
		self.lpaddle = lpaddle		#left paddle
		self.rpaddle = rpaddle		#right paddle
		self.ball_speedup = ball_speedup #ballspeed multiplier upon paddle hit
		#draw the ball in the window
		pt1 = Point(cen_x + self.radius, cen_y + self.radius)
		pt2 = Point(cen_x - self.radius, cen_y - self.radius)
		self.rect = Rectangle(pt1, pt2)
		self.rect.setFill("green")
		self.rect.draw(self.window)

	#Handles the movement of the ball with one tick of time. Updates the following:
		#Position
		#Velocity
		#Last Paddle Collided with
		#Redraws in window

	def update(self):
		oldcen_x = self.cen_x
		oldcen_y = self.cen_y

		#Increment position based on velocity
		self.cen_x += self.vx
		self.cen_y += self.vy

		#ball is colliding with bottom of screen
		if self.cen_y > self.maxy - self.radius:
			self.cen_y = self.maxy - self.radius
			self.vy = -self.vy

		#ball is colliding with top of screen
		if self.cen_y < self.miny + self.radius:
			self.cen_y = self.miny + self.radius
			self.vy = -self.vy

		#ball collides with left paddle
		if self.is_colliding(self.lpaddle):
			self.vx = -self.vx * self.ball_speedup
			self.vy = self.calc_new_vy(self.lpaddle)

		#ball collides with right paddle
		elif self.is_colliding(self.rpaddle):
			self.vx = -self.vx * self.ball_speedup
			self.vy = self.calc_new_vy(self.rpaddle)

		#Update position in window
		dx = self.cen_x - oldcen_x
		dy = self.cen_y - oldcen_y
		self.rect.move(dx, dy)

	#the top, bottom, left and right sides of the ball
	def top(self):
		return self.cen_y - self.radius

	def bottom(self):
		return self.cen_y + self.radius

	def left(self):
		return self.cen_x - self.radius

	def right(self):
		return self.cen_x + self.radius

	def undraw(self):
		self.rect.undraw()
		return None

	#checks to see if ball is colliding with a paddle, if yes, sets last collision to the paddle
	def is_colliding(self, paddle):
		if self.bottom() >= paddle.top() and self.top() <= paddle.bottom() and self.right() >= paddle.left() and self.left() <= paddle.right():
			if self.lastcollision is not paddle:
				self.lastcollision = paddle
				return True
		return False

	#returns new y velocity upon paddle collision
	def calc_new_vy(self, paddle):
		y_diff = self.cen_y - paddle.cen_y
		return abs(self.vx) * y_diff / paddle.height
