#Assumes the pong arena is a decent bit wider than it is tall
from paddle import Paddle
from pongball import PongBall
from graphics import *

class PongBot:
	def __init__(self, win, window_height, window_width, paddle_speed, p_dist_from_edge, ball_radius, ball_speedup, lpaddle, rpaddle, ball):
		self.win = win
		self.window_height = window_height
		self.window_width = window_width
		self.paddle_speed = paddle_speed
		self.p_dist_from_edge = p_dist_from_edge
		self.ball_radius = ball_radius
		self.ball_speedup = ball_speedup
		self.lpaddle = lpaddle
		self.rpaddle = rpaddle
		self.ball = ball
		self.oldvy = self.ball.vy
		self.oldvx = self.ball.vx
		self.oldleftball = self.ball.left()
		self.target = self.calc_target()

	def update(self):
		x_pos_to_commit = self.x_pos_to_commit()
		#Recalculate target when
		#1 right paddle hits the ball
		#2 left paddle hits the ball
		#3 ball reflects off of top/bottom wall
		#4 the moment ball passes the commit threshold 
		if self.oldvx > 0 and self.ball.vx < 0 \
			or self.oldvx < 0 and self.ball.vx > 0 \
			or self.oldvy == -self.ball.vy \
			or self.ball.left() <= x_pos_to_commit and self.oldleftball > x_pos_to_commit:
			#At the moment right paddle hits the ball
			self.target = self.calc_target()


		self.oldvy = self.ball.vy
		self.oldvx = self.ball.vx
		self.oldleftball = self.ball.left()

	def move_dir(self):
		#pick the movement option that minimizes distance to target
		dist_to_target = self.lpaddle.cen_y -self.target
		up_dist = abs(dist_to_target - self.paddle_speed)
		down_dist = abs(dist_to_target + self.paddle_speed)

		if min(abs(dist_to_target), up_dist, down_dist) == abs(dist_to_target):
			return "stay"
		elif min(abs(dist_to_target), up_dist, down_dist) == up_dist:
			return "up"
		else:
			return "down"

	def calculate_trajectory(self, vx, vy, x0, y0):
		ymax = self.window_height - self.ball_radius 	#lowest ball can go before being reflected
		ymin = self.ball_radius							#highest ball can go before being reflected
		paddle_x = self.lpaddle.right() 				#x position of left paddle
		if vy != 0:
			x_at_yismin = vx/vy * (ymin-y0) + x0 		#x when y = ymin
			x_at_yismax = vx/vy * (ymax-y0) + x0 		#x when y = ymax
		y_at_paddle_x = vy/vx * (paddle_x - x0) + y0 	#y when x is paddle_x

		#ball bounces at top of screen
		if vy != 0 and x_at_yismin > paddle_x and x_at_yismin < x0:
			return self.calculate_trajectory(vx, -vy, x_at_yismin, ymin)
		#ball bounces off of bottom of screen
		elif vy != 0 and x_at_yismax > paddle_x and x_at_yismax < x0:
			return self.calculate_trajectory(vx, -vy, x_at_yismax, ymax)
		else:
			return (paddle_x, y_at_paddle_x)

	def offset_for_traj_max(self, y0):
		#offset for aiming at ymax
		return self.offset_for_traj(y0, self.window_height - self.ball_radius)

	def offset_for_traj_min(self, y0):
		#offset for aiming at ymin
		return self.offset_for_traj(y0, self.ball_radius)

	def offset_for_traj(self, y0, ygoal):
		#Calculates the offset needed from the position the ball lands to angle the ball towards ygoal
		#on the opposite side
		dy = ygoal - y0
		dx = self.window_width - 2 * self.p_dist_from_edge - self.lpaddle.width/2 + self.rpaddle.width/2
		nextvx = self.ball.vx * -self.ball_speedup
		requiredvy = dy/dx * nextvx
		y_diff = requiredvy * self.lpaddle.height / abs(nextvx)
		return -y_diff

	def x_pos_to_commit(self):
		#waits until you have time to move one paddle's length to commit to an option
		time = self.lpaddle.height / self.paddle_speed
		dist = time * abs(self.ball.vx)
		xpos = self.lpaddle.right() + dist
		return xpos

	def calc_target(self):
		#If ball is moving away, target is center, else, its where the ball will land.
		if self.ball.vx > 0:
			return self.window_height / 2
		else:
			if self.ball.left() >= self.x_pos_to_commit():
				return self.calculate_trajectory(self.ball.vx, self.ball.vy, self.ball.cen_x, self.ball.cen_y)[1]
			else:
				if self.rpaddle.cen_y > self.window_height / 2: 
					#if right paddle is in the lower half of screen, aim for top corner
					return self.calculate_trajectory(self.ball.vx, self.ball.vy, self.ball.cen_x, self.ball.cen_y)[1] + self.offset_for_traj_min(self.lpaddle.cen_y)
				else:
					#else aim for bottom corner
					return self.calculate_trajectory(self.ball.vx, self.ball.vy, self.ball.cen_x, self.ball.cen_y)[1] + self.offset_for_traj_max(self.lpaddle.cen_y)