PyGame-Tiler
============

A simplistic 2D tile engine built with PyGame, designed to run as the base of my future 2D indie game. 

* Website - [http://super3.org](http://super3.org)
* Source Code - [https://github.com/super3/PyGame-Tiler](https://github.com/super3/IRC-Bot)

## Features 
This section is blank at the moment.

## Grid Module

### Class: Tile
All visible game objects (including background, buildings, etc) inherit from the Tile class. Static tiles use this class directly. Inherits from [_pygame.sprite.Sprite_](http://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite).

##### Constructor and Magics
* \_\_init\_\_(x, y, img) - Initializes vars.

#### Vars
* image - Tile image.
* rect - Bounds and location of tile in world.

### Methods
* render(screen) - Blit tile on a surface. 

---

### Class: Grid
Contains an array of Tiles objects that represents the map for the game. Will return the final surface object for drawing on the screen. Also includes much of the funtional code for the tiler.


##### Constructor and Magics
* \_\_init\_\_(x, y, tile_size) - Initializes vars.

#### Vars
* x - Number of tiles in the horizonatal direction.
* y - Number of tiles in the vertical direction.
* tile_size - Square pixel size of each tile. 

#### Methods
* fill(tile) - Fill the grid with the specified tile.