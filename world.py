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
import pygame, os
from helper import *

class Tile(pygame.sprite.Sprite):
	"""
	Basic PyGame Sprite Class.
	Pretty much every sprite should be derived from this.
	Static/immovable objects should use this class directly.
	
	Data members:
	image -- Contains the sprite image (usually imported as a .PNG)
			 Will later be expanded as an array with multiple image
			 so it can support animation
	rect -- Contains the bounds of the loaded image
	rect.x -- Coordinate X of the sprite (measured from the left edge)
	rect.y -- Coordinate Y of the sprite (measured from the bottom edge initially and then as PyGame )
	"""
	def __init__(self, x, y, img):
		# Call the parent class (Sprite) constructor 
		pygame.sprite.Sprite.__init__(self)
		
		# Load the image, if it does not exist try to load the error image. 
		if fileExists( img, "Block Class Image"):
			# Create an image and remove background
			tmpImage = pygame.image.load(img)
		else:
			tmpImage = pygame.image.load('view/tiles/error.png')

		# Takes World Dimentions
		worldX = worldDim[0]
		worldY = worldDim[1]
		groundHeight = worldDim[2]

		# Sets .PNG transparency to PyGame transparency
		self.image = tmpImage.convert_alpha() 
		# Set bounds
		self.rect = self.image.get_rect()
		# Set draw location
		self.rect.x = locX
		self.rect.y = worldY - (locY + self.rect.height) - groundHeight
	def render(self, screen):
		screen.blit(self.image, [self.rect.x, self.rect.y])

	def Tile(pygame.sprite.Sprite):
		pass

	def Grid(pygame.sprite.Sprite):
		pass

# World Class
class World:
	"""A class for the creation of a PyGame 2D grid world."""
	def __init__(self, x, y, worldX, worldY, gridSize):
		"""
		When initialized it will create a world of the specified dimensions
		and launch the PyGame window. This will be an empty PyGame window,
		as no content has been added to it. You may then preload sprites, 
		and then run the world.
	    
	    Arguments/Data members:
	    sizeX -- The x dimension of the screen in pixels.
	    sizeY -- The y dimension of the screen in pixels.
	    gridX -- The x dimension of the world in grid squares.
	    gridY -- The y dimension of the world in grid squares.
	    worldX -- The x dimension of the world in pixels.
	    worldY -- The y dimension of the world in pixels.
	    gridSize -- The square dimension of a grid square in pixels.
	   	background_image -- Contains the image of the world background. 
			Althought it will not return an error, the background image resolution 
			should be the same as the world dimentions. If the background image does
			not cover the full world background, or no background image is set, black 
			will be the background color.
	    backgroundX -- The x offset for the background image. For horizontal scrolling.
	    backgroundY -- The y offset for the backkound image. For vertical scrolling.
		
	    Extra Data Members:
	    backgroundColor -- Base color of the PyGame form. This should be covered up by
	    			  	   a background color or tile. 
		"""
		
		# Initialize Data Members
		self.sizeX = x
		self.sizeY = y

		self.gridX = gridX
		self.gridY = gridY
		self.gridSize = gridSize
		self.worldX = gridX * gridSize
		self.worldY = gridY * gridSize

		self.background_image = None
		self.backgroundX = 0 
		self.backgroundY = 0

		# Extra Data Members
		# Basically Some Render Settings
		self.backgroundColor = BLACK
		self.fps = 30
		self.scrollSpeed = 10
		
		# Start PyGame
		pygame.init()
		
		# Display Screen
		self.screen = pygame.display.set_mode( [self.sizeX*self.gridSize, self.sizeY*self.gridSize] )
		
		# Sentinel and Game Timer
		self.done = False
		self.clock = pygame.time.Clock()
		
		# Create RenderPlain
		self.sprites = pygame.sprite.RenderPlain()
		
		# Debug Messages
		printDebug("World Initialized.")
		printDebug("Screen Size: " + str(x) + "x" + str(y) + ".")
		printDebug("World Size: " + str(self.worldX) + "x" + str(self.worldY) + ".")
		printDebug("Grid Size: " + str(gridX) + "x" + str(gridY) + ".")
		printDebug("Grid Square Size: " + str(gridSize) + "px.")

	def setTitle(self, title):
		"""Sets the PyGame window title"""
		pygame.display.set_caption(str(title))
		
		# Debug Message
		printDebug("Title Set: '" + str(title) + "'.")
		
	def setIcon(self, path):
		"""
		Pre-Condition: The icon must be 32x32 pixels
		
		Grey (100,100,100) will be alpha channel
		The window icon will be set to the bitmap, but the grey pixels
		will be full alpha channel
		
		Note: Can only be called once after pygame.init() and before
		somewindow = pygame.display.set_mode()
		"""
		if fileExists( path, "Icon"):
			icon = pygame.Surface((32,32))
			icon.set_colorkey((100,100,100)) # call that color transparent
			rawicon = pygame.image.load(path) # load raw icon
			for i in range(0,32):
				for j in range(0,32):
					icon.set_at((i,j), rawicon.get_at((i,j)))
			pygame.display.set_icon(icon)
			printDebug("Icon Set: '" + str(path) + "'.")

	def loadMusic(self, path):
		"""Sets the background music for the world. Src argument is the path
		   of the sound file to load. This file can be WAV, MP3, or MIDI format."""
		# Seems to crash with view/sound/backgound2.mpg, perhaps because of the 
		# cover art that seems to be embedded into the .mp3
		if fileExists( path, "Background Music"):
			printDebug("Background Music Started.")
			pygame.mixer.music.load(path)
			pygame.mixer.music.play(-1, 0.0)

	def moveUp(self, speed = 1):
		"""Move the view window up by the speed (default 1px)"""
		if self.backgroundY < 0:
			self.backgroundY += speed
			for sprite in self.sprites:
				sprite.rect.y += speed
	def moveDown(self, speed = 1):
		"""Move the view window down by the speed (default 1px)"""
		if self.backgroundY > -(self.worldY - self.sizeY):
			self.backgroundY -= speed
			for sprite in self.sprites:
				sprite.rect.y -= speed
	def moveLeft(self, speed = 1):
		"""Move the view window left by the speed (default 1px)"""
		if self.backgroundX < 0:
			self.backgroundX += speed
			for sprite in self.sprites:
				sprite.rect.x += speed
	def moveRight(self, speed = 1):
		"""Move the view window right by the speed (default 1px)"""
		if self.backgroundX > -(self.worldX - self.sizeX):
			self.backgroundX -= speed
			for sprite in self.sprites:
				sprite.rect.x -= speed
	
	def run(self):
		"""Contains the main game loop for the world, which will basically draw everything
		to the screen for the specified FPS."""
		# Main Game Loop
		while self.done == False:			
			# Check for Events
			for event in pygame.event.get(): 
				# Quit Game
				if event.type == pygame.QUIT:
					printDebug("PyGame.Quit Called.")
					self.done = True
						
			# Check for Keys
			key=pygame.key.get_pressed()
			
			# Move View Window
			if key[pygame.K_LEFT]:
				self.moveLeft(self.scrollSpeed)
			elif key[pygame.K_RIGHT]:
				self.moveRight(self.scrollSpeed) 
			elif key[pygame.K_UP]:
				self.moveUp(self.scrollSpeed)
			elif key[pygame.K_DOWN]:
				self.moveDown(self.scrollSpeed)
				
			# Clear the Screen
			self.screen.fill(self.backgroundColor)
			
			# Try to Draw Background
			if self.background_image != None: 
				self.screen.blit( self.background_image, [self.backgroundX, self.backgroundY] )
				
			# Draw all Sprites
			for sprite in self.sprites:
				sprite.render(self.screen)
			
			# Update Display
			pygame.display.flip()
			
			# Limit FPS of Game Loop
			self.clock.tick(self.fps) # Magic Int!
		# End Main Game Loop
			
		# Exit Program
		printDebug("PyGame Exit.")
		pygame.quit()
		printDebug("System Exit.")
		sys.exit()