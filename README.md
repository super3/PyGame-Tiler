PyGame-Tiler
============

A simplistic 2D tile engine built with PyGame, designed to run as the base of my future 2D indie game. 

* Website - [http://super3.org](http://super3.org)
* Source Code - [https://github.com/super3/PyGame-Tiler](https://github.com/super3/IRC-Bot)

## Features 
This section is blank at the moment.

## World Module

### Class: Tile
All visible game objects (including background, buildings, etc) inherit from the Tile class. Static tiles use this class directly. Inherits from [_pygame.sprite.Sprite_](http://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite).

##### Constructor
* \_\_init\_\_(self, img_path, size, location) - Initializes vars.

	* img\_path - File path to the tile image.
	* check_size - 2-tuple of the tile size. ex.(width, height). This will check to make sure the tile size is the same as the image size.
	* location - 2-tuple of the tile screen location ex(x,y)


#### Vars
* image - Contains the sprite image (usually imported as a .PNG)
* rect.x - Coordinate X of the sprite (measured from the left edge)
* rect.y - Coordinate Y of the sprite (measured from the top edge)

### Methods
* render(screen) - Blit tile onto a passed surface. 

---

### Class: Grid
Contains an array of Tiles objects that represents the map for the game. Will return the final surface object for drawing on the screen. Also includes much of the funtional code for the tiler.


##### Constructor
* \_\_init\_\_(x, y, tile_size) - Initializes vars.

#### Vars
* x - Number of tiles in the horizonatal direction.
* y - Number of tiles in the vertical direction.
* tile_size - Square pixel size of each tile. 

#### Methods
* fill(tile) - Fill the grid with the specified tile.

---

### Class: World
When initialized it will create a world of the specified dimensions and launch the PyGame window. This will be an empty PyGame window, as no content has been added to it. You may then preload sprites, and then run the world.

#### Constructor
* \_\_init\_\_(x, y, grid, background_color = BLACK) - Initializes vars.

#### Vars

* size_x - The x dimension of the screen in pixels.
* size_y - The y dimension of the screen in pixels.
* grid - The world in grid squares.
* background_image - Contains the image of the world background. 
* background_x - The x offset for the background image. 
* background_y - The y offset for the backkound image. 
* background_color - Base color of the PyGame form. 

#### Methods
* setTitle(title) - Sets the PyGame window title.
* setIcon(path) - Sets the PyGame window icon.
* loadMusic(path) - Starts playing some background music.
* move(direction, speed) - Moves the view window.
* run(self) - Launches the world. 