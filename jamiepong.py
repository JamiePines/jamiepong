from graphics import *
import keyboard
import time
from pongball import PongBall
from paddle import Paddle
from pongbot import PongBot

class Game:
	def __init__(self, window_height, window_width, paddle_speed, p_dist_from_edge, ball_radius, ball_speedup):

		self.window_height = window_height
		self.window_width = window_width
		self.paddle_speed = paddle_speed
		self.p_dist_from_edge = p_dist_from_edge
		self.ball_radius = ball_radius
		self.ball_speedup = ball_speedup
		self.ball_paddle_speed_ratio = 1.5
		self.botmode = True

		#create the window, ball, and paddles
		self.win = GraphWin("Jamie Pong", self.window_width, self.window_height)
		self.lpaddle = Paddle(self.win, self.p_dist_from_edge, self.window_height/2, self.paddle_speed, True)
		self.rpaddle = Paddle(self.win, self.window_width - self.p_dist_from_edge, self.window_height/2, self.paddle_speed, False)
		self.ball = PongBall(self.win, self.ball_paddle_speed_ratio * self.paddle_speed, 0, self.ball_speedup, self.window_width/2, \
			self.window_height/2, self.ball_radius, 0, self.window_height, self.lpaddle, self.rpaddle)

		self.pongbot = PongBot(self.win, window_height, window_width, paddle_speed, p_dist_from_edge, ball_radius, \
			self.ball_speedup, self.lpaddle, self.rpaddle, self.ball)
		#Target display code
		# self.pongbot = PongBot(self.win, window_height, window_width, paddle_speed, p_dist_from_edge, ball_radius, self.lpaddle, self.rpaddle, self.ball)
		# self.targetx, self.targety = self.pongbot.calculate_trajectory(self.ball.vx, self.ball.vy, self.ball.cen_x, self.ball.cen_y)
		# self.target = Circle(Point(self.targetx, self.targety), 5)
		# self.target.draw(self.win)

	def update(self):
		self.ball.update()
		if self.botmode:
			self.pongbot.update()
			direction = self.pongbot.move_dir()
		else:
			direction = 'none'
		self.lpaddle.update(direction)
		self.rpaddle.update("none")

		#more target display code
		# self.target.undraw()
		# self.targetx, self.targety = self.pongbot.calculate_trajectory(self.ball.vx, self.ball.vy, self.ball.cen_x, self.ball.cen_y)
		# self.target = Circle(Point(self.targetx, self.targety), 5)
		# self.target.draw(self.win)

		#if game is over, reset
		if self.ball.left() > self.window_width or self.ball.right() < 0:
			self.ball.undraw()
			self.lpaddle.undraw()
			self.rpaddle.undraw()

			self.lpaddle = Paddle(self.win, self.p_dist_from_edge, self.window_height/2, self.paddle_speed, True)
			self.rpaddle = Paddle(self.win, self.window_width - self.p_dist_from_edge, self.window_height/2, self.paddle_speed, False)
			self.ball = PongBall(self.win, self.ball_paddle_speed_ratio * self.paddle_speed, 0, self.ball_speedup, self.window_width/2,  \
				self.window_height/2, self.ball_radius, 0, self.window_height, self.lpaddle, self.rpaddle)
			self.pongbot = PongBot(self.win, self.window_height, self.window_width, self.paddle_speed, self.p_dist_from_edge, self.ball_radius, \
				self.ball_speedup, self.lpaddle, self.rpaddle, self.ball)
		
def main():
	window_width = 800
	window_height = 450
	paddle_speed = 2
	p_dist_from_edge = 50
	ball_radius = 10
	ball_speedup = 1.05
	refresh_time = .01

	game = Game(window_height, window_width, paddle_speed, p_dist_from_edge, ball_radius, ball_speedup)
	time.perf_counter()
	ref_counter = 0 #keeps track of base time
	while(True):
		if keyboard.is_pressed("esc"):
			game.win.close()
			break
		if keyboard.is_pressed("w") or keyboard.is_pressed("s"):
			game.botmode = False
		time_ellapsed = time.perf_counter() - ref_counter
		if time_ellapsed >= refresh_time:
			game.update()
			ref_counter = time.perf_counter()
		time.sleep(.0001)

main()