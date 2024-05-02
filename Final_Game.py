import arcade
import random

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Maze Runner"

CHARACTER_SCALING = 0.42
TILE_SCALING = 0.22
PLAYER_MOVEMENT_SPEED = 2.5



def mazeGeneration():
    '''
    1.Start with a grid full of walls.
    2. Pick a cell, mark it as part of the maze. Add the walls of the cell to the wall list.
    3.While there are walls in the list:
        1.Pick a random wall from the list. If only one of the cells that the wall divides is visited, then:
            1.Make the wall a passage and mark the unvisited cell as part of the maze.
            2.Add the neighboring walls of the cell to the wall list.
        2.Remove the wall from the list.
    '''
    #1
            # do this  for this collection   for this collection
    maze = [[1 for x in range(0,25)] for x in range(0,25)]
    #2
    x = random.choice(range(1,24))
    y = random.choice(range(1,24))
    maze[x,y] = 0
    wallList = []
    if(maze[x-1, y] == 1):
        wallList.append((x-1,y))
    if(maze[x+1, y] == 1):
        wallList.append((x+1,y))
    if(maze[x, y-1] == 1):
        wallList.append((x,y-1))
    if(maze[x, y+1] == 1):
        wallList.append((x,y+1))

    '''
    1.Start with a grid full of walls.
    2. Pick a cell, mark it as part of the maze. Add the walls of the cell to the wall list.
    3.While there are walls in the list:
        1.Pick a random wall from the list. If only one of the cells that the wall divides is visited, then:
            1.Make the wall a passage and mark the unvisited cell as part of the maze.
            2.Add the neighboring walls of the cell to the wall list.
        2.Remove the wall from the list.
    '''
    #3
    while(wallList.isEmpty()):
        randomIndex = random.choice(range(0, len(wallList)))
        randomWall = wallList[randomIndex]
        if(randomWall):
            pass    
    
    return maze


class maze(arcade.Window):
 
    def __init__(self):

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.csscolor.MEDIUM_SEA_GREEN)

        self.scene = None
        self.player = None
        self.wall_collide = None

        # store sprites in list to referrence later
        self.wall_list = None
        self.items_list = None
        self.camera = None

        #background music initialization + looping
        self.bg_music = arcade.Sound(":resources:music/funkyrobot.mp3", streaming=True)
        self.bg_music.play(volume=0.10, loop = True)

        

    def setup(self):

        self.scene = arcade.Scene()

        #implementing sprites
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.items_list = arcade.SpriteList(use_spatial_hash=True)

        #setup the player
        #TODO: change image source from arcade to user
        image_source = ":resources:images/animated_characters/male_person/malePerson_idle.png"
        self.player = arcade.Sprite(image_source, CHARACTER_SCALING)

        #TODO use algorithm to find possible start and end point of maze
        self.player.center_x = 2
        self.player.center_y = 2

        self.camera = arcade.Camera(self.width, self.height)

        #TODO: implement randomized maze algorithm (Dijkstras / Depth First Search)
        # Hardcoded right now to test maze wall creation
       
        maze = [
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

        for x in range(len(maze)):
            for y in range(len(maze[x])):
                if maze[x][y] == 1:
                    wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", TILE_SCALING)
                    wall.position = (((x * 35) + 100), ((y * 35) + 100))    
                    self.wall_list.append(wall)
                    self.scene.add_sprite("Walls", wall)        

        '''
        #use this for loop to generate the locations of boxes
        coordinate_list = [[10, 20], [30, 96]]
        for coordinate in coordinate_list:
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", TILE_SCALING)
            wall.position = coordinate
            self.wall_list.append(wall)
            self.scene.add_sprite("Walls", wall)
        '''

        #physics engine for walls (collide)
        self.wall_collide = arcade.PhysicsEngineSimple(self.player, self.scene.get_sprite_list("Walls"))
        
        #TODO: set up items and implement them on open spaces using algorithm

        #TODO: create code logic to prevent players from finishing the game before collecting all items

        #TODO: implement borders on the map to prevent players from leaving

        #TODO: implement camera view that reduces player visability (dark circle) 

    def on_draw(self):
        self.clear()
        self.wall_list.draw()
        self.camera.use()
        self.player.draw()   


    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.W:
            self.player.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.W:
            self.player.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = 0

    def on_update(self, delta_time):
        #prevent players from leaving path
        self.wall_collide.update()
        self.center_camera_to_player()


    def center_camera_to_player(self):
        screen_center_x = self.player.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player.center_y - (
            self.camera.viewport_height / 2
        )

        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)


def main():
    window = maze()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()