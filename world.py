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
BLACK = [0, 0 ,0]
WHITE = [255, 255, 255]
BLUE = [ 0, 0 , 255]
GREEN = [ 0, 255, 0]
RED = [255, 0, 0]
ALPHA = [255, 0, 238]

class Tile(pygame.sprite.Sprite):
	"""
	All visible game objects (including background, buildings, etc) inherit from the Tile class.
	Static tiles use this class directly. Static/immovable objects should use this class directly.
	
	Data members:
	image -- Contains the sprite image (usually imported as a .PNG)
			 Will later be expanded as an array with multiple image
			 so it can support animation
	rect.x -- Coordinate X of the sprite (measured from the left edge)
	rect.y -- Coordinate Y of the sprite (measured from the top edge)

	"""
	def __init__(self, img_path, size, location):
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

		# Set bounds
		self.rect = self.image.get_rect()
		# Check Image Dimentions
		if not self.image.get_size == size: raise 
		# Set draw location
		self.rect.x = location[0]
		self.rect.y = location[1]

	def render(self, screen):
		screen.blit(self.image, [self.rect.x, self.rect.y])

# World Class
class World:
	"""
	When initialized it will create a world of the specified dimensions
	and launch the PyGame window. This will be an empty PyGame window,
	as no content has been added to it. You may then preload sprites, 
	and then run the world.
    
    Arguments/Data members:
    screen_size -- The pixel dimension of the screen. (2-tuple)
    world_grid_size -- The grid dimension of the world. (2-tuple)
    tile_size -- The pixel dimension of a grid square. (int)

    background_loc -- The offset for the screen display. For background scrolling.
    background_color -- Base color of the PyGame form. 
    fps -- Frames per second to display game. 
    scroll_speed -- Pixel amount to move view window for every keypress. 
    map -- An array of tile objects. 

	"""
	# Constructor and Magics
	def __init__(self, screen_size, world_grid_size, tile_size, background_color = BLACK, fps = 30, scroll_speed = 10):
		
		# Initialize Data Members
		self.screen_size = screen_size
		self.world_grid_size = world_grid_size
		self.tile_size = tile_size

		# Initialize Optional Data Members
		self.background_loc = (0,0)
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
		
		# Create RenderPlain
		self.sprites = pygame.sprite.RenderPlain()
		
		# Debug Messages
		print(self)
	def __str__(self):
		output = "World Object Debug Dump:\n"
		output += "\tScreen Size: " + str(self.screen_size) + " px.\n"
		output += "\tWorld Grid Size: " + str(self.world_grid_size) + " tiles.\n"
		output += "\tTile Size: " + str(self.tile_size) + " px.\n"
		return output

	# Startup Methods
	def fill(self, default_tile):
		"""Fill a world's grid with the passed default tile."""
		pass
	
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
				
			# Clear the Screen
			self.screen.fill(self.background_color)
				
			# # Draw all Sprites
			# for sprite in self.sprites:
			# 	sprite.render(self.screen)
			
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
	world = World((500,500), (5,5), 50)
	world.run()