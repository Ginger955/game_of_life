import sys

import PySimpleGUI as gui
import random
import math
import time
import pygame.draw

# RULES


class Node:

	# WHITE is ALIVE
	# YELLOW is DEAD
	def __init__(self, x, y, size):
		self.size = size
		self.x = x
		self.y = y
		if random.random() <= 0.75:
			self.color = "yellow"
		else:
			self.color = "white"

	def set_color(self, color):
		self.color = color

	@property
	def get_color(self):
		return self.color

	@property
	def get_size(self):
		return self.size

	@property
	def get_coordinates(self):
		return self.x, self.y

	@property
	def get_neighbour_above_coordinates(self):
		if self.x - 1 < 0:
			return None
		return self.x - 1, self.y

	@property
	def get_neighbour_below_coordinates(self):
		if self.x + 1 == self.size:
			return None
		return self.x + 1, self.y

	@property
	def get_neighbour_left_coordinates(self):
		if self.y - 1 < 0:
			return None
		return self.x, self.y - 1

	@property
	def get_neighbour_right_coordinates(self):
		if self.y + 1 == self.size:
			return None
		return self.x, self.y + 1

	@property
	def get_neighbour_upper_right_diagonal_coordinates(self):
		if self.x - 1 < 0 or self.y + 1 == self.size:
			return None
		return self.x - 1, self.y + 1

	@property
	def get_neighbour_upper_left_diagonal_coordinates(self):
		if self.x - 1 < 0 or self.y - 1 < 0:
			return None
		return self.x - 1, self.y - 1

	@property
	def get_neighbour_lower_left_diagonal_coordinates(self):
		if self.x + 1 == self.size or self.y - 1 < 0:
			return None
		return self.x + 1, self.y - 1

	@property
	def get_neighbour_lower_right_diagonal_coordinates(self):
		if self.x + 1 == self.size or self.y + 1 == self.size:
			return None
		return self.x + 1, self.y + 1

	def get_neighbours(self):
		return [self.get_neighbour_above_coordinates, self.get_neighbour_below_coordinates,
				self.get_neighbour_left_coordinates, self.get_neighbour_right_coordinates,
				self.get_neighbour_upper_right_diagonal_coordinates, self.get_neighbour_upper_left_diagonal_coordinates,
				self.get_neighbour_lower_left_diagonal_coordinates, self.get_neighbour_lower_right_diagonal_coordinates]


class World:

	def __init__(self, size, canvas_width, canvas_height):
		self.width = canvas_width
		self.height = canvas_height
		self.size = size
		k = math.ceil(float(size / 2))
		self.world = [[Node(y, x, k) for x in range(k)] for y in range(k)]
		print("[INITIAL PRINT]")
		for i in self.world:
			for y in i:
				print("[NODE] " + str(y.get_coordinates) + ' ' + str(y.get_color) + ' [NEIGHBOURS] ' + str(y.get_neighbours()))

	def print_state(self):
		row = []
		column = []
		for list in self.world:
			for node in list:
				column.append((node.get_coordinates, node.get_color))
			row.append(column)
			print('[WORLD]' + str(row))
			column = []
			row = []

	def draw_world(self):
		pygame.init()
		DISPLAY = pygame.display.set_mode((self.width, self.height), 0, 32)
		WHITE = (255, 255, 255)
		YELLOW = (255, 255, 0)
		BLACK = (0, 0, 0)
		DISPLAY.fill(BLACK)

		top_multiplier = 0
		for nodes_list in self.world:
			left_multiplier = 0
			for node in nodes_list:
				if node.get_color == 'yellow':
					pygame.draw.rect(DISPLAY, YELLOW, (math.ceil((self.width/self.size))*left_multiplier,
													   math.ceil((self.height/self.size))*top_multiplier,
													   math.ceil(self.width/self.size),
													   math.ceil(self.height / self.size)))
				else:
					pygame.draw.rect(DISPLAY, BLACK, (math.ceil((self.width/self.size))*left_multiplier,
													  math.ceil((self.height/self.size))*top_multiplier,
													  math.ceil(self.width/self.size),
													  math.ceil(self.height / self.size)))
				left_multiplier += 1
			top_multiplier += 1
		pygame.display.update()

	def count_live_neighbours(self, neighbour_list):
		alive = 0
		for coordinates in neighbour_list:
			if coordinates is not None:
				if self.world[coordinates[0]][coordinates[1]].get_color == "white":
					alive += 1
		return alive

	def is_everyone_dead(self):
		for i in self.world:
			for y in i:
				if y.get_color == 'white':
					return False
		return True

	def is_it_stable(self, new):
		previous = []
		current = []
		for x in self.world:
			for i in x:
				previous.append(i.get_color)
		for y in new:
			for k in y:
				current.append(k.get_color)
		return previous == current

	def run(self):
		self.draw_world()
		# self.print_state()
		time.sleep(0.1)
		new_world = []
		next_generation = []
		for nodes_list in self.world:
			for node in nodes_list:
				alive_neighbours = self.count_live_neighbours(node.get_neighbours())
				current_coordinates = node.get_coordinates
				newNode = None

				# implementation of Game Of Life rules. Rules are applied simultaneously
				if alive_neighbours < 2 and node.get_color == 'white':
					newNode = Node(current_coordinates[0], current_coordinates[1], node.get_size)
					newNode.set_color('yellow')
					# print('[' + str(node.get_coordinates) + '] dies. Alive neighbours:'+str(alive_neighbours))
				elif alive_neighbours == 2 or alive_neighbours == 3 and node.get_color == 'white':
					print('['+str(node.get_coordinates)+'] lives onto the next generation')
				elif alive_neighbours > 3 and node.get_color == 'white':
					newNode = Node(current_coordinates[0], current_coordinates[1], node.get_size)
					newNode.set_color('yellow')
					# print('[' + str(node.get_coordinates) + '] dies. Alive neighbours:' + str(alive_neighbours))
				elif alive_neighbours == 3 and node.get_color == 'yellow':
					newNode = Node(current_coordinates[0], current_coordinates[1], node.get_size)
					newNode.set_color('white')
					# print('[' + str(node.get_coordinates) + '] revived. Alive neighbours:'+str(alive_neighbours))

				if newNode is not None:
					next_generation.append(newNode)
				else:
					next_generation.append(node)
			new_world.append(next_generation)
			next_generation = []
		if self.is_everyone_dead():
			# self.print_state()
			print("[EVERYONE IS DEAD]")
			sys.exit()
		elif self.is_it_stable(new_world):
			# self.print_state()
			print("[WORLD IS STABLE]")
			sys.exit()
		self.world = new_world
		self.run()


world = World(100, 1500, 1500)
world.run()
