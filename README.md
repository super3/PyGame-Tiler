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
* \_\_init\_\_(self, img_path, check_size) - Initializes vars.

	* img\_path - File path to the tile image.
	* check_size - Square tile pixel size. Will check to make sure the tile size is the same as the image size.

#### Vars
* image - Contains the sprite image (usually imported as a .PNG)

#### Methods
* render(screen) - Blit tile onto a passed surface. 

#### Example Code
	tile = Tile('grass.png', 64)

---

### Class: Grid (Not Yet Implemented)
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
* \_\_init\_\_(screen\_size, world\_grid\_size, tile\_size) - Initializes vars.

#### Vars

    screen_size 	 -- The pixel dimension of the screen. (2-tuple)
    world_grid_size  -- The grid dimension of the world. (2-tuple)
    tile_size 		 -- The pixel dimension of a grid square. (int)

    background_loc 	 -- The offset for the screen display. For background scrolling.
    background_color -- Base color of the PyGame form. 
    fps 			 -- Frames per second to display game. 
    scroll_speed 	 -- Pixel amount to move view window for every key press. 
    map 	         -- An array of tile objects. 

    screen 			 -- Actual display surface.
    done 	         -- Sentinel for game loop.
    clock 	         -- Helps track time for FPS and animations.

#### "Public" Methods
* set_title(title) - Sets the PyGame window title.
* set_icon(path) - Sets the PyGame window icon.
* load_music(path) - Starts playing some background music.
* fill(default_tile) - Fill a world's map with the passed default tile.
* move(direction, speed) - Moves the view window.
* run() - Launches the world. 

#### "Private" Methods
* move_up(speed) - Moves the view window up.
* move_down(speed) - Moves the view window down.
* move_left(speed) - Moves the view window left.
* move_right(speed) - Moves the view window right.
* get_index(x, y) - Returns the map list index for a given (x,y) location on the grid.

#### Example Code
	world = World((640,640), (16,16), 64)
	world.fill( Tile('grass.png', 64) )
	world.run()