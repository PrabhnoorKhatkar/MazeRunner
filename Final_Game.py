import arcade
import random

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Maze Runner"

CHARACTER_SCALING = 0.35
TILE_SCALING = 0.45
COIN_SCALING = 0.30
PLAYER_MOVEMENT_SPEED = 7.5


def populateMaze(width, height):
    '''Make a chessboard like maze for maze algo'''
    maze = [[1 for y in range(height)]  for x in range(width)]  
    for x in range(width):
        for y in range(height):
            if(x % 2 == 0 and y % 2 == 1): #if row = even, col = odd
                maze[x][y] = 0

    return maze


def mazeGeneration(width, height):
    # Psuedocode from DFS iterative wikipedia maze generation TODO add link
    '''1. Choose the initial cell, mark it as visited and push it to the stack
       2.While the stack is not empty
            1.Pop a cell from the stack and make it a current cell
            2.If the current cell has any neighbours which have not been visited
                1.Push the current cell to the stack
                2.Choose one of the unvisited neighbours
                3.Remove the wall between the current cell and the chosen cell
                4.Mark the chosen cell as visited and push it to the stack'''
    
    maze = populateMaze(width, height)


    # Choose the initial cell, mark it as visited and push it to the stack
    rndRow = random.randrange(0,height)
    rndCol = random.randrange(0,width)

    stack = []
    visited = []
    while(maze[rndRow][rndCol] == 1):
        rndRow = random.randrange(0,height)
        rndCol = random.randrange(0,width)

    maze[rndRow][rndCol] = 0  
    stack.append((rndRow, rndCol)) 
    visited.append((rndRow, rndCol))
    
    # While the stack is not empty
    while stack:
        currCell = stack.pop()  
        neighbor = choose_neighbor(currCell, width, height, visited, maze)

        # If the current cell has any neighbours which have not been visited
        if neighbor is not None:
            stack.append(currCell) 
            maze[currCell[0]][currCell[1]] = 0  

            #1.2.3 Remove the wall between the current cell and the chosen cell
            maze[(currCell[0] + neighbor[0]) // 2][(currCell[1] + neighbor[1]) // 2] = 0  
            stack.append(neighbor)  
            visited.append(neighbor) 

    # Add border walls
    for i in range(height):
        maze[i][0] = maze[i][-1] = 1
    for j in range(width):
        maze[0][j] = maze[-1][j] = 1

    return maze

def choose_neighbor(cell, width, height, visited, maze):
    directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]  # left, right, up, down
    random.shuffle(directions)

    for direction in directions:
        farNeighbor = (cell[0] + direction[0]*2, cell[1] + direction[1]*2)
        nearNeighbor = (cell[0] + direction[0], cell[1] + direction[1])
        if 1 <= farNeighbor[0] < height-1 and 1 <= farNeighbor[1] < width-1 and farNeighbor not in visited:
            return farNeighbor
        
        if not farNeighbor:
            maze[nearNeighbor[0]][nearNeighbor[1]] = 0 # Break the wall edge case (prevents nonconnected paths)
    return None


class maze(arcade.Window):
 
    def __init__(self):

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.csscolor.BURLYWOOD)

        self.scene = None
        self.player = None
        self.wall_collide = None

        # store sprites in list to referrence later
        self.wall_list = None
        self.items_list = None
        self.camera = None
        self.score = 0

        #background music initialization + looping
        #Commented out because unreliable on MacOS and dependenices are installed but still gives issues 
        #self.bg_music = arcade.Sound(":resources:music/funkyrobot.mp3", streaming=True)
        #self.bg_music.play(volume=0.10, loop = True)


    def setup(self):

        self.scene = arcade.Scene()
        self.dark_circle_sprite = arcade.Sprite("dark_circle.png")

        #implementing sprites
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.items_list = arcade.SpriteList(use_spatial_hash=True)

        player_idle = ":resources:images/animated_characters/male_person/malePerson_idle.png"
        self.player = arcade.Sprite(player_idle, CHARACTER_SCALING)
        
        self.camera = arcade.Camera(self.width, self.height)

        maze = mazeGeneration(25,25)

        emptySpace = []
        for x in range(len(maze)):
            for y in range(len(maze[x])): 
                if maze[x][y] == 1:
                    wall = arcade.Sprite(":resources:images/topdown_tanks/tileGrass2.png", TILE_SCALING)
                    wall.position = (((x * 35) + 100), ((y * 35) + 100))    
                    self.wall_list.append(wall)
                    self.scene.add_sprite("Walls", wall)  
                elif maze[x][y] == 0:
                    emptySpace.append((x,y))

        random.shuffle(emptySpace)
        coinList = emptySpace[0:4]
        self.player.center_x = ((coinList[-1][0] * 35) + 100)
        self.player.center_y = ((coinList[-1][1] * 35) + 100)  
        coinList = coinList[0:3]
        
        for x,y in coinList:
            coin = arcade.Sprite(":resources:images/items/coinGold.png", COIN_SCALING)
            coin.position = (((x * 35) + 100), ((y * 35) + 100))  
            self.items_list.append(coin)
            self.scene.add_sprite("Coins", coin)
                    

        #physics engine for walls (collide)
        self.wall_collide = arcade.PhysicsEngineSimple(self.player, self.scene.get_sprite_list("Walls"))
        
    def on_draw(self):
        self.clear()
        self.wall_list.draw()
        self.items_list.draw()
        #self.dark_circle_sprite.draw()
        self.camera.use()
        self.player.draw()  
        self.center_camera_to_player()
       
        

    def on_update(self, delta_time):
        self.dark_circle_sprite.center_x = self.player.center_x
        self.dark_circle_sprite.center_y = self.player.center_y
        
        #prevent players from leaving path
        self.wall_collide.update()
        self.center_camera_to_player()
        coin_touch = arcade.check_for_collision_with_list(self.player,self.items_list)

        for coin in coin_touch:
            coin.remove_from_sprite_lists()
            self.score += 1
        
        if self.score == 3:
            self.center_camera_to_player()


    def center_camera_to_player(self):
        screen_center_x = self.player.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player.center_y - (self.camera.viewport_height / 2)

        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

        arcade.draw_text(f"Score: {self.score}", start_x=screen_center_x + 820, start_y=screen_center_y + 630, color=arcade.color.WHITE, font_size=20)
        if self.score == 3:
            arcade.draw_text(f"You Win!" , start_x=screen_center_x + 440, start_y=screen_center_y + 550, color=arcade.color.BLUE, font_size=20)

    def on_key_press(self, key, modifiers):
        player_left = arcade.load_texture(":resources:images/animated_characters/male_person/malePerson_walk2.png", flipped_horizontally= True)
        player_right = arcade.load_texture(":resources:images/animated_characters/male_person/malePerson_walk2.png")
        player_down = arcade.load_texture(":resources:images/animated_characters/male_person/malePerson_walk0.png")
        player_up = arcade.load_texture(":resources:images/animated_characters/male_person/malePerson_climb1.png")

        if key == arcade.key.UP or key == arcade.key.W:
            self.player.change_y = PLAYER_MOVEMENT_SPEED
            self.player.texture = player_up

        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player.change_y = -PLAYER_MOVEMENT_SPEED
            self.player.texture = player_down

        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = -PLAYER_MOVEMENT_SPEED
            self.player.texture = player_left

        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = PLAYER_MOVEMENT_SPEED
            self.player.texture = player_right
            

    def on_key_release(self, key, modifiers):
        player_idle = arcade.load_texture(":resources:images/animated_characters/male_person/malePerson_idle.png")

        if key == arcade.key.UP or key == arcade.key.W:
            self.player.change_y = 0
            self.player.texture = player_idle

        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player.change_y = 0
            self.player.texture = player_idle
            
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = 0
            self.player.texture = player_idle
            
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = 0
            self.player.texture = player_idle

def main():
    window = maze()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()