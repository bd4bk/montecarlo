from operator import concat
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt

class Die:
    """
        Description: Die have faces, and each face has a weight (defaults to 1.). 
        Weights can be changed for individual faces. 
        Die can be rolled to return a list of faces randomly selected based on their weights. Die can show its faces and weights
        
        Attributes: None

        Functions: w_change(face, new_w), roll(n = 1), show()
        """
    def __init__(self, n):
        """
        Description: Initializer function for Die, takes an array of faces and stores faces in a DataFrame with default weight of 1.0

        Params: n = array of faces, array data type can be a number or string

        Returns: None
        """
        self._df = pd.DataFrame(
        columns = ["w"],
        index = n,
        data = ([1.0] * len(n)))
    
    def w_change(self, face, new_w):
        """
        Description: function to change the weight of a specific face. 
        Checks if the face is in the Die and if the new weight is a valid number

        Params: face = face to change weight of, new_w = new weight of face

        Returns: None
        """
        if face in self._df.index:
            if isinstance(new_w, float):
                self._df.loc[face] = new_w
            elif isinstance(new_w, int):
                self._df.loc[face] = float(new_w)
            elif isinstance(new_w, str):
                try:
                    float(new_w)
                    self._df.loc[face] = float(new_w)
                except ValueError:
                    print("not a float")
                    
            else:
                print("not a valid weight")
        else:
            print("not a valid face")
        
    def roll(self, n = 1):
        """
        Description: function to roll the die n times based on the die faces and weights and return the results in a list

        Params: n = number of rolls desired, int. default value is 1

        Returns: list rolls = list of the die rolls
        """
        rolls = []
        for i in range(n):
            pick = random.choices(self._df.index, weights = self._df.values / (sum(self._df.values)))[0]
            rolls.append(pick)
        return rolls
    
    def show(self):
        """
        Return the faces and weights of the Die
        """
        return self._df
        
class Game:
    """
        Description: Games are a collection of similar Die. Games can play() and roll all their Die a given number of times.
        Game stores the results of play() and can return them with show(), either in wide or narrow format.

        Attributes dice = list of Die housed within the Game

        Functions: play(rolls), show(form = 'wide')
        """
    def __init__(self, dice):
        """
        Description: Initializer function to create game from a list of dice. Raises exception if dice do not have the same faces

        Params: dice = list of dice, all dice in list must have the same faces

        Returns:None
        """
        if all(die._df.index.tolist() == dice[0]._df.index.tolist() for die in dice):
            self.dice = dice 
        else:
            raise Exception("Invalid Dice. Dice must have the same faces")
    
    def play(self, rolls):
        """
        Description: function to roll all dice in the game and save the results in a private dataframe

        Params: rolls = number of times you'd like to roll the dice, int

        Returns: None
        """
        die_dict = {}
        n=1
        for die in self.dice:
            die_dict["Die " + str(n)] = die.roll(rolls)
            n+=1
        self._df = pd.DataFrame(die_dict)
        self._df = self._df.rename(index = lambda x : x + 1)
    
    def show(self, form = "wide"):
        """
        Description: function to show the most recent results from the play() method. Can present the data in either wide or long form. Narrow form has a two-column index with the roll number and the die number, and a column for the face rolled. Wide form has a single column index with the roll number, and each die number as a column.

        Params: form = "wide" or "narrow", how you would like the data presented. Default is "wide"

        Returns: DataFrame of play() results
        """
        if form == "wide":
            return self._df
        elif form == "narrow":
            return self._df.stack().to_frame()
        else:
            raise Exception("invalid format (can only be 'wide' or 'narrow'")

class Analyzer:
    """
    Description: Analyzer takes a Game and can provide various descriptive statistical properties about its play(). The DataFrames used to compute these properties are stored as Attributes once they are computed
    
    Attributes: 
        jackpots = pd.DataFrame with the roll # as index and boolean values for if the roll was a jackpot or not
        
        combos = pd.DataFrame with a multi-columned index with each Die as an index, the rolled face as the index value, and 
        the amount of times the entire roll combination occured in the Game as the value
        
        face_count = pd.DataFrame with the roll # as index , the face values as columns, and the count of the face per roll as
        the value
    
    Functions: jackpot(), combo(), face_counts()
    """
    def __init__(self, game):
        """
        Description: Initializer function for Analyzer class. 
        
        Params:game = a previously instantiated Game
        
        Returns: None
        """
        self.game = game
        
    def jackpot(self):
        """
        Description: Computes and returns (as an int) how many times the game resulted in all faces being identical. Also stores the results as the DataFrame jackpots
        
        Params: None
        
        Returns: int, count of how many jackpots there were
        """
        gamelist = self.game._df.values.tolist()
        data = [all(die == roll[0] for die in roll) for roll in self.game._df.values.tolist()]
        self.jackpots = pd.DataFrame(
            index = self.game._df.index,
            columns = ["jackpot_result"],
            data = data)
        self.jackpots.index.name = "roll"
        self.jackpot_count = sum(data)
        return self.jackpot_count
        
    
    def combo(self):
        """
        Description: Computes the distinct combinations of faces rolled and their counts. Stores the results in the DataFrame combos

        Params: None

        Returns: None
        """
        self.combos = self.game._df.apply(lambda x: pd.Series(sorted(x)),1).value_counts().to_frame()
        
        #Non multi-index code (could use for easy graphing)
        # combo_dict = {}
        # for roll in self.game._df.values.tolist():
        #     sorted_roll = sorted(roll)
        #     if ','.join(map(str,sorted_roll)) in combo_dict:
        #         combo_dict[','.join(map(str,sorted_roll))] += 1
        #     else:
        #         combo_dict[','.join(map(str,sorted_roll))] = 1
        # self.combos = pd.DataFrame.from_dict(
        # combo_dict, orient = 'index')
        # return self.combos

    def face_counts(self):
        """
        Description: Computes how many times each face was rolled in each roll and stores the results in the DataFrame face_count

        Params: None

        Returns: None
        """
        count_dicts = {}
        for i in self.game.dice[0]._df.index:
            counts = self.game._df.isin({i}).sum(1)
            count_dicts[i] = counts
        self.face_count = pd.DataFrame(count_dicts)