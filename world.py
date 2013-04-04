# ------------------------------------------------------------
# Filename: world.py
#
# Author: Shawn Wilkinson
# Author Website: http://super3.org/
# Author Email: me@super3.org
#
# Website: http://super3.org/
# Github Page: https://github.com/super3/PyGame-Tiler/
# 
# Creative Commons Attribution 3.0 Unported License
# http://creativecommons.org/licenses/by/3.0/
# ------------------------------------------------------------

# System Imports
import os
import sys
import json
import pygame
import logging
from pprint import pprint
from pygame.locals import Color

# Declare Alpha
ALPHA = (100, 100, 100)

# Fake Enumerations/Constants
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Start Logging
logging.basicConfig(filename="sample.log", filemode="w", level=logging.DEBUG)

# Tile Class
class Tile(pygame.sprite.Sprite):
	"""
	All visible game objects (including background, buildings, etc) inherit from the Tile class.
	Static tiles use this class directly. Static/immovable objects should use this class directly.
	
	Data members:
	image 	   -- Contains the sprite image (usually imported as a .PNG). Will later be expanded
				  as an array with multiple image so it can support animation.

	Arguments:
	image_path -- Relative path to the title's image. See image data member.
	check_size -- Used to make sure that the title pixel size is the same as the source image.

	"""
	def __init__(self, img_path, check_size):
		# Call the parent class (Sprite) constructor 
		pygame.sprite.Sprite.__init__(self)
		
		#  Try to load image
		if os.path.exists(img_path):
			# Create an image
			tmp_image = pygame.image.load(img_path)
		else:
			# Else return a blank surface
			tmp_image = pygame.Surface(size)

		# Sets .PNG transparency to PyGame transparency
		# self.image = tmp_image.convert_alpha() 
		self.image = tmp_image # hack

		# Check Image Dimensions
		if not self.image.get_size() == (check_size, check_size): 
			print(self.image.get_size())
			raise ValueError("Invalid image size.")

	def render(self, screen, loc):
		screen.blit(self.image, (loc[0], loc[1]))


# Map Class
class Map:
	"""
	Converts a JSON map file into a playable map.

	Data members:
	map_name  -- The title of the map.
	map_data  -- Raw tile data for the map.
	map_size  -- The grid dimensions of the world. (2-tuple)
	tile_size -- The pixel dimensions of a grid square. (int)
	tile_list -- List of Tile objects for use in map.

	"""
	def __init__(self, path):
		"""Load a mapfile."""
		if os.path.exists(path):
			self.load(path)
			logging.info("Map File Loaded: '" + str(path) + "'.")
		else:
			logging.error("Map File Load Failed: '" + str(path) + "'.")

	def get_index(self, x, y, world_grid_size):
		"""Returns the map list index for a given (x,y) location on the grid."""
		return x + world_grid_size[0] * ( world_grid_size[1] - y - 1 ) - 1

	def load(self, path):
		# Get JSON Data
		data = json.load(open(path))
		# Get Map Data
		self.map_name = data["layers"][0]["name"]
		self.raw_data = data["layers"][0]["data"]
		self.map_size = (data["layers"][0]["height"], data["layers"][0]["width"])
		self.tile_size = data["tileheight"] # we assume tile is square
		# Get Tiles
		self.tile_list = []
		for json_tile in data["tilesets"]: 
			self.tile_list.append( Tile(json_tile["image"], 56) )
		# Make Map
		self.map_data = []
		counter = 0

		self.fill(None)

		# What a hack
		for y in range(self.map_size[1]):
			for x in range(self.map_size[0]):
				self.map_data[self.get_index(x,y,self.map_size)] = self.tile_list[ self.raw_data[counter] -1 ]
				counter = counter + 1

	def fill(self, default_tile):
		"""Fill a world's map with the passed default tile."""
		self.map_data = [default_tile for i in range(self.map_size[0] * self.map_size[1])]


# World Class
class World:
	"""
	When initialized it will create a world of the specified dimensions	and launch the PyGame window.
	This will be an empty PyGame window, as no content has been added to it. You may then pre-load a map, 
	and then run the world.

	Data members:
	screen_size 	 -- The pixel dimension of the screen. (2-tuple)
	map_obj          -- Contains world dimension, tile info, and everything else.

	offset_x 	 	 -- The x offset for the screen display. For background scrolling.
	offset_y 	 	 -- The y offset for the screen display. For background scrolling.
	background_color -- Base color of the PyGame form. 
	fps 			 -- Frames per second to display game. 
	scroll_speed 	 -- Pixel amount to move view window for every key press. 
	map 	         -- An array of tile objects. 

	screen 			 -- Actual display surface.
	done 	         -- Sentinel for game loop.
	clock 	         -- Helps track time for FPS and animations.

	Arguments:
	icon -- Will set the window icon of the window.
	See data members.

	"""
	# Constructor and Magics
	def __init__(self, screen_size, map_obj, icon_path = None, fps = 30, scroll_speed = 10):
		"""See World object's Docstring."""
		# Initialize Data Members
		self.screen_size = screen_size
		self.map_obj = map_obj
		self.world_grid_size = map_obj.map_size
		self.tile_size = map_obj.tile_size

		# Initialize Optional Data Members
		self.offset_x, self.offset_y = (0,0)
		self.background_color = Color("Black")
		self.fps = fps
		self.scroll_speed = scroll_speed
		self.map = []
		
		# Start PyGame
		pygame.init()

		# Set Icon
		if not icon_path == None: self._set_icon(icon_path)
		
		# Display Screen
		self.screen = pygame.display.set_mode(screen_size)
		
		# Sentinel and Game Timer
		self.done = False
		self.clock = pygame.time.Clock()
		
		# Logging Messages
		logging.info('World Object Created.')
		logging.debug(str(self))

	def __str__(self):
		output = "World Object:\n"
		output += "\tScreen Size: " + str(self.screen_size) + " px.\n"
		output += "\tWorld Grid Size: " + str(self.world_grid_size) + " tiles"
		output += ", Tile Size: " + str(self.tile_size) + " px.\n"
		output += "\tFPS: " + str(self.fps) + ", Scroll Speed: " + str(self.scroll_speed) + ".\n"
		tmp_offset = (self.offset_x, self.offset_y)
		output += "\tCurrent Background Location: " + str(tmp_offset) + "."
		return output


	# Window Methods
	def set_title(self, title):
		"""Sets the PyGame window title."""
		pygame.display.set_caption(str(title))
		logging.info("Title Set: '" + str(title) + "'.")

	def _set_icon(self, path):
		"""
		Pre-Condition: The icon must be 32x32 pixels
		
		The window icon will be set to the bitmap.
		All (255, 0, 238) color pixels will be alpha channel.
		
		Note: Can only be called once after pygame.init() and before
		somewindow = pygame.display.set_mode()

		"""
		if os.path.exists(path):
			icon = pygame.Surface((32,32))
			icon.set_colorkey(ALPHA) # call that color transparent
			rawicon = pygame.image.load(path) # load raw icon
			for i in range(0,32):
				for j in range(0,32):
					icon.set_at((i,j), rawicon.get_at((i,j)))
			pygame.display.set_icon(icon)
			logging.info("Icon Set: '" + str(path) + "'.")
		else:
			logging.error("Icon Load Failed: '" + str(path) + "'.")

	def load_music(self, path):
		"""Sets the background music for the world. This file can be WAV, MP3, or MIDI format."""
		if os.path.exists(path):
			logging.info("Background Music Started: '" + str(path) + "'.")
			pygame.mixer.music.load(path)
			pygame.mixer.music.play(-1, 0.0)
		else: 
			logging.error("Background Music Load Failed: '" + str(path) + "'.")


	# Movement Methods
	def _move_up(self, speed = 1):
		"""Move the view window up by the speed (default 1px)."""
		if self.offset_y + speed < 0:
			self.offset_y += speed

	def _move_down(self, speed = 1):
		"""Move the view window down by the speed (default 1px)."""
		if self.offset_y - speed > -(self.world_grid_size[1]*self.tile_size - self.screen_size[1]):
			self.offset_y -= speed

	def _move_left(self, speed = 1):
		"""Move the view window left by the speed (default 1px)."""
		if self.offset_x + speed < 0:
			self.offset_x += speed

	def _move_right(self, speed = 1):
		"""Move the view window right by the speed (default 1px)."""
		if self.offset_x - speed > -(self.world_grid_size[0]*self.tile_size - self.screen_size[0]):
			self.offset_x -= speed


	# Location Methods
	def _get_index(self, x, y):
		"""Returns the map list index for a given (x,y) location on the grid."""
		return x + self.world_grid_size[0] * ( self.world_grid_size[1] - y - 1 ) - 1
	def get_tile(self, pos):
		"""Returns the (x,y) location of a tile for the given mouse location."""
		x = (pos[0]+abs(self.offset_x))/self.tile_size
		y = (pos[1]+abs(self.offset_y))/self.tile_size
		return (int(x), int(y))


	# Methods
	def move(self, direction, speed):
		"""Move the view camera by the specified direction and pixel speed."""
		if direction == UP: self._move_up(speed)
		elif direction == DOWN: self._move_down(speed)
		elif direction == LEFT: self._move_left(speed)
		elif direction == RIGHT: self._move_right(speed)
		else: logging.warning("Invalid move direction.: " + str(direction) + ".")	

	def run(self):
		"""
		Contains the main game loop for the world, which will basically draw everything
		to the screen at the specified FPS.

		"""
		
		# Main Game Loop
		while self.done == False:			
			# Check for Events
			for event in pygame.event.get(): 
				# Quit Game
				if event.type == pygame.QUIT:
					logging.info("PyGame.Quit Called.")
					self.done = True
				elif event.type == pygame.MOUSEBUTTONDOWN:
					print("You clicked: on tile:" + str(self.get_tile(pygame.mouse.get_pos())))
						
			# Check for Keys
			key=pygame.key.get_pressed()

			# Move View Window
			if key[pygame.K_UP]:
				self.move(UP, self.scroll_speed)
			elif key[pygame.K_DOWN]:
				self.move(DOWN, self.scroll_speed)
			elif key[pygame.K_LEFT]:
				self.move(LEFT, self.scroll_speed)
			elif key[pygame.K_RIGHT]:
				self.move(RIGHT, self.scroll_speed) 	
				
			# Clear the Screen
			self.screen.fill(self.background_color)

			# Draw all Sprites
			for y in range(self.world_grid_size[1]):
				for x in range(self.world_grid_size[0]):
					draw_tile = self.map_obj.map_data[self._get_index(x,y)]
					x_loc = x*self.tile_size + self.offset_x
					y_loc = y*self.tile_size + self.offset_y
					draw_tile.render(self.screen, (x_loc, y_loc))

			# Hover Tile
			mos_x, mos_y = self.get_tile(pygame.mouse.get_pos())

			rect = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA, 32)
			rect.fill((23, 100, 255, 50))
			self.screen.blit(rect, (mos_x*self.tile_size, mos_y*self.tile_size))
			
			# Update Display
			pygame.display.flip()
			
			# Limit FPS of Game Loop
			self.clock.tick(self.fps)
		# End Main Game Loop


# Unit Test
if __name__ == "__main__":
	map_obj = Map('map2.json')
	world = World((560,560), map_obj, 'assets/icon.png')
	world.run()