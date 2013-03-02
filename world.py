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
import pygame

# Define Basic Colors
BLACK = [  0,   0,   0]    
BLUE  = [  0,   0, 255]
GREEN = [  0, 255,   0]
RED   = [255,   0,   0]
WHITE = [255, 255, 255]
ALPHA = [255,   0, 238]

# Fake Enumerations/Constants
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Tile Class
class Tile(pygame.sprite.Sprite):
	"""
	All visible game objects (including background, buildings, etc) inherit from the Tile class.
	Static tiles use this class directly. Static/immovable objects should use this class directly.
	
	Data members:
	image -- Contains the sprite image (usually imported as a .PNG)
			 Will later be expanded as an array with multiple image
			 so it can support animation.

	Keyword arguments:
	image_path -- Relative path to the title's image. See image data member.
	check_size -- Used to make sure that the title pixel size is the same as the source image.

	"""
	def __init__(self, img_path, check_size):
		# Call the parent class (Sprite) constructor 
		pygame.sprite.Sprite.__init__(self)
		
		# Load the image, if it does not exist try to load the error image
		if os.path.exists( img_path ):
			# Create an image and remove background
			tmp_image = pygame.image.load(img_path)
		else:
			tmp_image = pygame.Surface(size)

		# Sets .PNG transparency to PyGame transparency
		self.image = tmp_image.convert_alpha() 

		# Check Image Dimensions
		if not self.image.get_size() == (check_size, check_size): raise ValueError("Invalid image size.")

	def render(self, screen, loc):
		screen.blit(self.image, (loc[0], loc[1]))

# World Class
class World:
	"""
	When initialized it will create a world of the specified dimensions	and launch the PyGame window.
	This will be an empty PyGame window, as no content has been added to it. You may then pre-load sprites, 
	and then run the world.
    
    Arguments/Data members:
    screen_size -- The pixel dimension of the screen. (2-tuple)
    world_grid_size -- The grid dimension of the world. (2-tuple)
    tile_size -- The pixel dimension of a grid square. (int)

    background_loc -- The offset for the screen display. For background scrolling.
    background_color -- Base color of the PyGame form. 
    fps -- Frames per second to display game. 
    scroll_speed -- Pixel amount to move view window for every key press. 
    map -- An array of tile objects. 

    screen -- Actual display surface.
    done -- Sentinel for game loop.
    clock -- Helps track time for FPS and animations.

	"""
	# Constructor and Magics
	def __init__(self, screen_size, world_grid_size, tile_size, background_color = BLACK, fps = 30, scroll_speed = 10):
		"""See World object's Docstring."""
		# Initialize Data Members
		self.screen_size = screen_size
		self.world_grid_size = world_grid_size
		self.tile_size = tile_size

		# Initialize Optional Data Members
		self.background_loc_x, self.background_loc_y = (0,0)
		self.background_color = background_color
		self.fps = fps
		self.scroll_speed = scroll_speed
		self.map = []
		
		# Start PyGame
		pygame.init()
		
		# Display Screen
		self.screen = pygame.display.set_mode( screen_size )
		
		# Sentinel and Game Timer
		self.done = False
		self.clock = pygame.time.Clock()
		
		# Debug Messages
		print(self)
	def __str__(self):
		output = "World Object:\n"
		output += "\tScreen Size: " + str(self.screen_size) + " px.\n"
		output += "\tWorld Grid Size: " + str(self.world_grid_size) + " tiles"
		output += ", Tile Size: " + str(self.tile_size) + " px.\n"
		output += "\tFPS: " + str(self.fps) + ", Scroll Speed: " + str(self.scroll_speed) + ".\n"
		tmp_background_loc = (self.background_loc_x, self.background_loc_y)
		output += "\tCurrent Background Location: " + str(tmp_background_loc) + "."
		return output

	# Window Methods
	def set_title(self, title):
		"""Sets the PyGame window title."""
		pygame.display.set_caption(str(title))
		print("Title Set: '" + str(title) + "'.")
	def set_icon(self, path):
		"""
		Pre-Condition: The icon must be 32x32 pixels
		
		The window icon will be set to the bitmap.
		All (255, 0, 238) color pixels will be alpha channel.
		
		Note: Can only be called once after pygame.init() and before
		somewindow = pygame.display.set_mode()

		"""
		if os.path.exists( path ):
			icon = pygame.Surface((32,32))
			icon.set_colorkey((100,100,100)) # call that color transparent
			rawicon = pygame.image.load(path) # load raw icon
			for i in range(0,32):
				for j in range(0,32):
					icon.set_at((i,j), rawicon.get_at((i,j)))
			pygame.display.set_icon(icon)
			print("Icon Set: '" + str(path) + "'.")
		else:
			print("Icon Load Failed: " + str(path) + ".")
	def load_music(self, path):
		"""Sets the background music for the world. This file can be WAV, MP3, or MIDI format."""
		if os.path.exists( path ):
			print("Background Music Started: '" + str(path) + "'.")
			pygame.mixer.music.load(path)
			pygame.mixer.music.play(-1, 0.0)
		else: 
			print("Background Music Load Failed: '" + str(path) + "'.")

	# Methods
	def fill(self, default_tile):
		"""Fill a world's map with the passed default tile."""
		self.map = [default_tile for i in range(self.world_grid_size[0] * self.world_grid_size[1])]
	def move(self, direction, speed):
		if direction == UP: self.move_up(speed)
		elif direction == DOWN: self.move_down(speed)
		elif direction == LEFT: self.move_left(speed)
		elif direction == RIGHT: self.move_right(speed)
		else: print("Invalid move direction.")

	# Movement Methods
	def move_up(self, speed = 1):
		"""Move the view window up by the speed (default 1px)."""
		if self.background_loc_y + speed < 0:
			self.background_loc_y += speed
	def move_down(self, speed = 1):
		"""Move the view window down by the speed (default 1px)."""
		if self.background_loc_y - speed > -(self.world_grid_size[1]*self.tile_size - self.screen_size[1]):
			self.background_loc_y -= speed
	def move_left(self, speed = 1):
		"""Move the view window left by the speed (default 1px)."""
		if self.background_loc_x + speed < 0:
			self.background_loc_x += speed
	def move_right(self, speed = 1):
		"""Move the view window right by the speed (default 1px)."""
		if self.background_loc_x - speed > -(self.world_grid_size[0]*self.tile_size - self.screen_size[0]):
			self.background_loc_x -= speed

	# Helper Method(s)
	def get_index(self, x, y):
		"""Returns the map list index for a given (x,y) location on the grid."""
		return x + self.world_grid_size[0] * ( self.world_grid_size[1] - y - 1 ) - 1
	
	# Run Method
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
					print("PyGame.Quit Called.")
					self.done = True
						
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
					draw_tile = self.map[self.get_index(x,y)]
					x_loc = x*self.tile_size + self.background_loc_x
					y_loc = y*self.tile_size + self.background_loc_y
					draw_tile.render(self.screen, (x_loc, y_loc))
			
			# Update Display
			pygame.display.flip()
			
			# Limit FPS of Game Loop
			self.clock.tick(self.fps)
		# End Main Game Loop
			
		# Exit Program
		print("PyGame Exit.")
		pygame.quit()
		print("System Exit.")
		sys.exit()

# Unit Test
if __name__ == "__main__":
	world = World((640,640), (16,16), 64)
	world.fill( Tile('grass.png', 64) )
	world.run()