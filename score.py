# Use pickle to save and load binary information
import pickle
from constants import *

class ScoreManager:
    """A class for managing reading and writing a high score from a dat file"""
    def __init__(self, filename="high_score.dat"):
        """Initialize the class with the file name (default is high_score.dat) and the high score using the load_high_score() method"""
        self.filename = filename
        self.high_score = self.load_high_score()

    def load_high_score(self):
        """Using pickle, try to reada a file in binary"""
        try:
            with open(self.filename, "rb") as file:
                return pickle.load(file)
        except (FileNotFoundError, EOFError):
            print("Error loading file.")
            return 0

    def save_high_score(self, score):
        """Takes score. If score is greater than high score, write to the file"""
        if score > self.high_score:
            self.high_score = score
            try:
                with open(self.filename, "wb") as file:
                    pickle.dump(self.high_score, file)
            except (FileNotFoundError, EOFError):
                print("Error loading file.")
                return 0

    def save_score(self, score):
        """Takes score. Writes to file regardless of high score"""
        self.high_score = score
        try:
            with open(self.filename, "wb") as file:
                pickle.dump(self.high_score, file)
        except (FileNotFoundError, EOFError):
            print("Error loading file.")
            return 0