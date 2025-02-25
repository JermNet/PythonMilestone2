from constants import *
import turtle

class Shop:
    """Shop class for buying and different skins for the snake and food"""
    def __init__(self, game):
        """Initiallizes the class, takes game which is the SnakeGame class"""
        self.game = game
        self.shop_text = None
        self.selected_snake_skin = None
        self.selected_food_skin = None
    
    def shop(self):
        """Sets up the visual aspect of the shop, looping through the skins to present them on screen with turtle"""
        self.game.screen.clear()
        self.game.screen.bgcolor("black")
        
        self.shop_text = turtle.Turtle()
        menu_text = turtle.Turtle()
        menu_text.color("white")
        menu_text.hideturtle()
        menu_text.penup()
        self.shop_text.color("white")
        self.shop_text.hideturtle()
        self.shop_text.penup()
        self.shop_text.goto(0, 200)
        self.shop_text.write(f"SHOP - Spend Your High Score Points\nYour High Score: {self.game.score_manager.high_score}\nEach Switch Costs {SHOP_COST} Score", align="center", font=("Arial", 20, "bold"))
        
        for i, skin in enumerate(SNAKE_SKINS):
            skin_preview = turtle.Turtle()
            skin_preview.shape(skin)
            skin_preview.penup()
            skin_preview.goto(-350, 100 - (i * 60))
            menu_text.goto(-300, 100 - (i * 60))
            menu_text.write(f"Snake Skin {i+1} (Press {i+1})", align="left", font=("Arial", 14, "bold"))
            self.game.screen.onkey(lambda i=i: self.buy_snake_skin(i), str(i+1))
        
        food_keys = ["6", "7", "8", "9", "0"]
        for i, skin in enumerate(FOOD_SKINS):
            skin_preview = turtle.Turtle()
            skin_preview.shape(skin)
            skin_preview.penup()
            skin_preview.goto(0, 100 - (i * 60))
            menu_text.goto(50, 100 - (i * 60))
            menu_text.write(f"Food Skin {i+1} (Press {food_keys[i]})", align="left", font=("Arial", 14, "bold"))
            self.game.screen.onkey(lambda i=i: self.buy_food_skin(i), food_keys[i])
        
        menu_text.goto(0, -200)
        menu_text.write("Press 'Enter' to Start Game", align="center", font=("Arial", 18, "bold"))
        self.game.screen.onkey(self.game.start_game, "Return")
    
    def buy_snake_skin(self, index):
        """If high score is great or equal to the shop cost, subtract shop cost from high score"""
        if self.game.score_manager.high_score >= SHOP_COST:
            self.game.score_manager.save_score(self.game.score_manager.high_score-SHOP_COST)
            self.selected_snake_skin = SNAKE_SKINS[index]
            print(self.selected_snake_skin)
            self.update_shop_text()

    def buy_food_skin(self, index):
        """If high score is great or equal to the shop cost, subtract shop cost from high score"""
        if self.game.score_manager.high_score >= SHOP_COST:
            self.game.score_manager.save_score(self.game.score_manager.high_score-SHOP_COST)
            self.selected_food_skin = FOOD_SKINS[index]
            self.update_shop_text()
    
    def update_shop_text(self):
        """Update the high score text displayed on the menu"""
        self.game.screen.title(f"Shop - High Score: {self.game.score_manager.high_score}")
        self.shop_text.clear()
        self.shop_text.goto(0, 200)
        self.shop_text.write(f"SHOP - Spend Your High Score Points\nYour High Score: {self.game.score_manager.high_score}\nEach Switch Costs {SHOP_COST} Score", align="center", font=("Arial", 20, "bold"))