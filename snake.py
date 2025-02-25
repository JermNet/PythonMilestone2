import turtle
import random
from constants import *
from shop import Shop
from score import ScoreManager

class Snake:
    """The snake class, where the game logic resides"""
    def __init__(self):
        """Initialize the snake game with turtle and any variables we need"""
        # Set up the turtle screen with the constants, title and bg image and make it not resizeable
        self.screen = turtle.Screen()
        self.screen.setup(WIDTH, HEIGHT)
        self.screen.title("Snake Game")
        self.screen.bgpic("assets/background.png")

        # Make it so the screen cannot be resized
        self.screen._root = self.screen.getcanvas().winfo_toplevel()
        self.screen._root.resizable(False, False)

        # This just makes it so the images can be put on screen
        for skin in SNAKE_SKINS + FOOD_SKINS:
            self.screen.register_shape(skin)
        
        # This disables auto updating the screen since I have my own game loop
        self.screen.tracer(False)
        # Listen for inputs
        self.screen.listen()

        # Only add the shop if it hasn't already been added. Since init is called twice, the second call would otherwise reset the shop, and the skin/skins it selects
        if not hasattr(self, 'shop_system'):
            self.shop_system = Shop(self)
        # Set the current skin to either the default or the one selected in the shop should a selection be made
        self.snake_skin = self.shop_system.selected_snake_skin or DEFAULT_SNAKE_SKIN
        self.food_skin = self.shop_system.selected_food_skin or DEFAULT_FOOD_SKIN
        
        # A stamper (aka a way to draw to the screen) for the snake. It does double duty as the head and segments, and changes shape in the game loop
        self.snake_stamper = turtle.Turtle()
        self.snake_stamper.color("#161813")
        # Penup makes it so 
        self.snake_stamper.penup()
        
        # Another stamper, this time for the food
        self.food = turtle.Turtle()
        self.food.shape(self.food_skin)
        # turtle is weird. The default shapesize is 20px, so if you the size to be the number you hand this method, you have to divide by 20. It doesn't make any sense, but that's just how it works
        self.food.shapesize(FOOD_SIZE / 20)
        self.food.penup()
        
        # The snake itself, which is just a list of lists, resulting in a list of positions which can be read from to draw segments 
        self.snake = [[0,0], [SNAKE_SIZE, 0], [SNAKE_SIZE*2, 0], [SNAKE_SIZE*3, 0]]
        self.snake_direction = "up"

        # Draw a random food piece
        self.food_pos = self.get_random_food()
        self.food.goto(self.food_pos)
        
        # Score stuff, high_score is a separate class since it's saved and loaded, whereas score is not
        self.score = 0
        self.score_manager = ScoreManager()
        self.high_score = self.score_manager.load_high_score()
        
        # Default no game over, and a turtle for the game over text
        self.is_game_over = False
        self.game_over_text = turtle.Turtle()
        self.game_over_text.color("red")
        self.game_over_text.hideturtle()
        self.game_over_text.penup()
        
    def start_game(self):
        """Starts a game of snake by clearing the screan, running the init, bind_direction_keys, and game_loop methods"""
        self.screen.clear()
        self.__init__()
        self.bind_direction_keys()
        self.game_loop()

    def get_random_food(self):
        """Get a random position food within the window bounds and taking into account the size of the food"""
        x = random.randint(-WIDTH // 2 + FOOD_SIZE, WIDTH // 2 - FOOD_SIZE)
        y = random.randint(-HEIGHT // 2 + FOOD_SIZE, HEIGHT // 2 - FOOD_SIZE)
        return (x, y)
    
    def get_distance(self, pos1, pos2):
        """Just get the distance between two points using the Pythagorean theorem"""
        return ((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2) ** 0.5

    def food_collision(self):
        """Checks if the head of the snake and a piece of food collide, if they do, increase score, run the save high score method, and get a new piece of food"""
        if self.get_distance(self.snake[-1], self.food_pos) < 20:
            self.score += 1
            self.score_manager.save_high_score(self.score)
            self.food_pos = self.get_random_food()
            self.food.goto(self.food_pos)
            return True
        return False

    def bind_direction_keys(self):
        
        self.screen.onkey(lambda: self.set_snake_direction("up"), "Up")
        self.screen.onkey(lambda: self.set_snake_direction("down"), "Down")
        self.screen.onkey(lambda: self.set_snake_direction("left"), "Left")
        self.screen.onkey(lambda: self.set_snake_direction("right"), "Right")
    
    def set_snake_direction(self, direction):
        if direction == "up" and self.snake_direction != "down":
            self.snake_direction = "up"
        elif direction == "down" and self.snake_direction != "up":
            self.snake_direction = "down"
        elif direction == "left" and self.snake_direction != "right":
            self.snake_direction = "left"
        elif direction == "right" and self.snake_direction != "left":
            self.snake_direction = "right"

    def game_over(self):
        self.is_game_over = True
        self.score_manager.save_high_score(self.score)
        self.game_over_text.clear()
        self.game_over_text.goto(0, 0)
        self.game_over_text.write("GAME OVER\nPress R to Restart", align="center", font=("Arial", 24, "bold"))
        self.screen.onkey(self.reset_game, "r")
    
    def reset_game(self):
        if self.is_game_over:
            self.is_game_over = False
            self.score = 0
            self.snake = [[0,0], [SNAKE_SIZE, 0], [SNAKE_SIZE*2, 0], [SNAKE_SIZE*3, 0]]
            self.snake_direction = "up"
            self.food_pos = self.get_random_food()
            self.food.goto(self.food_pos)
            self.game_over_text.clear()
            self.shop_system.shop()
    
    # def load_high_score(self):
    #     try:
    #         with open("high_score.txt", "r") as file:
    #             return int(file.read())
    #     except FileNotFoundError:
    #         return 0
    
    # def save_high_score(self):
    #     with open("high_score.txt", "w") as file:
    #         file.write(str(self.high_score))
    
    def game_loop(self):
        if self.is_game_over:
            return
        
        self.snake_stamper.clearstamps()
        new_head = self.snake[-1].copy()
        offsets = {"up": (0, SNAKE_SIZE), "down": (0, -SNAKE_SIZE), "left": (-SNAKE_SIZE, 0), "right": (SNAKE_SIZE, 0)}
        new_head[0] += offsets[self.snake_direction][0]
        new_head[1] += offsets[self.snake_direction][1]
        
        if new_head in self.snake or new_head[0] < -WIDTH / 2 or new_head[0] > WIDTH / 2 or new_head[1] < -HEIGHT / 2 or new_head[1] > HEIGHT / 2:
            self.game_over()
        else:
            self.snake.append(new_head)
            if not self.food_collision():
                self.snake.pop(0)
            
            self.snake_stamper.shape(self.snake_skin)
            self.snake_stamper.goto(self.snake[-1][0], self.snake[-1][1])
            self.snake_stamper.stamp()
            self.snake_stamper.shape("square")
            for segment in self.snake[:-1]:
                self.snake_stamper.goto(segment[0], segment[1])
                self.snake_stamper.stamp()
            
            self.screen.title(f"Snake Game. Score: {self.score} High Score: {self.score_manager.high_score}")
            self.screen.update()
            turtle.ontimer(self.game_loop, DELAY)
        
