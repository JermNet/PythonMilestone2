import turtle
import random
from constants import *
from shop import Shop
from score import ScoreManager

class Snake:
    selected_snake_skin = "assets/snake.gif"
    selected_food_skin = "assets/food.gif"
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.setup(WIDTH, HEIGHT)
        self.screen.title("Snake Game")
        self.screen.bgpic("assets/background.png")
        for skin in SNAKE_SKINS + FOOD_SKINS:
            self.screen.register_shape(skin)
        self.screen.tracer(False)
        self.screen.listen()

        # self.snake_skin
        # if self.snake_skin != SNAKE_SKINS[0]:
        if not hasattr(self, 'shop_system'):
            self.shop_system = Shop(self)
            print("test")
        self.snake_skin = self.shop_system.selected_snake_skin or Snake.selected_snake_skin
        self.food_skin = self.shop_system.selected_food_skin or Snake.selected_food_skin
        print(self.snake_skin)
        self.stamper = turtle.Turtle()
        self.stamper.shape("square")
        self.stamper.color("#161813")
        self.stamper.penup()
        
        self.food = turtle.Turtle()
        self.food.shape(self.food_skin)
        self.food.shapesize(FOOD_SIZE / 32)
        self.food.penup()
        
        self.snake = [[0,0], [SNAKE_SIZE, 0], [SNAKE_SIZE*2, 0], [SNAKE_SIZE*3, 0]]
        self.snake_direction = "up"
        self.food_pos = self.get_random_food()
        self.food.goto(self.food_pos)
        
        self.score = 0
        self.score_manager = ScoreManager()
        self.high_score = self.score_manager.load_high_score()
        self.is_game_over = False
        self.game_over_text = turtle.Turtle()
        self.game_over_text.color("red")
        self.game_over_text.hideturtle()
        self.game_over_text.penup()

        self.shop_text = None
        
        
    
    def start_game(self):
        self.screen.clear()
        self.__init__()
        self.bind_direction_keys()
        self.game_loop()
        if self.shop_system.selected_snake_skin:
            self.selected_snake_skin = self.shop_system.selected_snake_skin
            self.snake_skin = self.selected_snake_skin
            print("yep")
        if self.shop_system.selected_food_skin:
            self.selected_food_skin = self.shop_system.selected_food_skin
            self.food_skin = self.selected_food_skin

    def get_random_food(self):
        x = random.randint(-WIDTH // 2 + FOOD_SIZE, WIDTH // 2 - FOOD_SIZE)
        y = random.randint(-HEIGHT // 2 + FOOD_SIZE, HEIGHT // 2 - FOOD_SIZE)
        return (x, y)
    
    def food_collision(self):
        if self.get_distance(self.snake[-1], self.food_pos) < 20:
            self.score += 1
            self.score_manager.save_high_score(self.score)
            self.food_pos = self.get_random_food()
            self.food.goto(self.food_pos)
            return True
        return False

    def get_distance(self, pos1, pos2):
        return ((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2) ** 0.5
    
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
        
        self.stamper.clearstamps()
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
            
            self.stamper.shape(self.snake_skin)
            self.stamper.goto(self.snake[-1][0], self.snake[-1][1])
            self.stamper.stamp()
            self.stamper.shape("square")
            for segment in self.snake[:-1]:
                self.stamper.goto(segment[0], segment[1])
                self.stamper.stamp()
            
            self.screen.title(f"Snake Game. Score: {self.score} High Score: {self.score_manager.high_score}")
            self.screen.update()
            turtle.ontimer(self.game_loop, DELAY)
        
