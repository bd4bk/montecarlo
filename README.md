# Metadata
## Name: Brennan Danek
## ID: bd4bk
## Project Name: Monte Carlo Simulator
    
# Synposis

## Installation
You can install this package with the following address: https://github.com/bd4bk/montecarlo.git
by downloading the package and running the setup.py package
```bash
python setup.py install
```

## Importing
You can import the package in python with
```python
import montecarlo
```

or you can import individual classes with
```python
#from montecarlo import Die
```

## Creating Die
You can create the Die class with Die() function, which takes 1 parameter: an array of faces
```python
die = Die(["Heads","Tails"])
```

Die faces have weights that default to 1. when the Die is created. You can change the weights of individual faces with the Die.w_change(face, new_weight) function
```python
die.w_change("Heads", 2.)
```

You can roll die to return a list of faces selected based on their weights. Die.roll() takes 1 parameter: int for how many rolls you would like it to return. Die.roll() defaults to 1 roll.
```python
die.roll(5)
```

You can also use Die.show() to present current faces and weights of the Die.
```python
die.show()
```

## Playing Games
Once you have Die created, you can play Games with multiple Die. Die must be similar (identical faces) for Game to work
```python
game = Game([die, die, die, die])
```

Die can however have different weights
```python
f_die = Die(["H","T"])
u_die = Die(["H","T"])
u_die.w_change("H", 5)

u_game = Game([f_die, u_die])
```

Once your Game is created, you can Game.play(n) your game in order to roll all the Die n times. This Game is then stored within the Game and can be accessed with the Game.show() function.
```python
u_game.play(100)
u_game.show()
```

Game.show() can also be used to present the Game in narrow form, but form defaults to "wide"
```python
u_game.show(form = "narrow")
```

## Analyzing Games
Now that you've played your Game, you can use the Analyzer class to recieve various descriptive statistical properties about it
```python
u_analyzer = Analyzer(u_game)
```

With Analyzer, you can find how many jackpots, or rolls where all faces are identical, your Game had with Analyzer.jackpot()
```python
u_analyzer.jackpot()
```

This will return the number of jackpots, but once you run the jackpot() function, you can recieve a datframe of rolls and booleans of if they were a jackpot or not with Analyzer.jackpots 
```python
u_analyzer.jackpots
```

Analyzer can also compute the amount of each specific combination that was rolled within the Game with Analyzer.combo()
```python
u_analyzer.combo()
```
This creates a DataFrame with the data that can be accessed with u_analyzer.combos
```python
u_analyzer.combos
```

Finally, Analyzer can create a DataFrame that shows the face counts per roll with Analyzer.face_counts()
```python
u_analyzer.face_counts()
```

This can be accessed afterwards with Analyzer.face_count
```python
u_analyzer.face_count
```

# API Description


## Die Class

### Description
Die have faces, and each face has a weight (defaults to 1.). 
Weights can be changed for individual faces. 
Die can be rolled to return a list of faces randomly selected based on their weights. Die can show its faces and weights
Params: n = list of int or str

### Methods
w_change(self, face, new_w)
Description: function to change the weight of a specific face. Checks if the face is in the Die and if the new weight is a valid number
Params: face = (int or str) face of weight to change, new_w = (float, int, or str) new weight of face
Returns: None


roll(n = 1):
Description: function to roll the die n times based on the die faces and weights and return the results in a list
Params: n = (int) number of rolls desired, default = 1
Returns: (list) of the die rolls

show():
Description: returns the faces and weights of the Die
Params: None
Returns: (DataFrame) of Die faces and weights

### Attributes

None


## Game Class

### Description

Games are a collection of similar Die. Games can play() and roll all their Die a given number of times. Game stores the results of play() and can return them with show(), either in wide or narrow format.
Params: dice = (list) of Die with identical faces

### Methods

play()
Description: function to roll all dice in the game and save the results in a private dataframe (can be accessed with show())
Params: None
Returns:None

show(form)
Description: function to show the most recent results from the play() method. Can present the data in either wide or long form. Narrow form has a two-column index with the roll number and the die number, and a column for the face rolled. Wide form has a single column index with the roll number, and each die number as a column. 
Params: form = (str) way to display data, "wide" or "narrow". default = "wide"
Returns: (DataFrame) of play() results

### Attributes

None


## Analyzer Class

### Description

Analyzer takes a Game and can provide various descriptive statistical properties about its play(). The DataFrames used to compute these properties are stored as Attributes once they are computed
Params:(Game) game

### Methods

jackpot()
Description: Computes and returns (as an int) how many times the game resulted in all faces being identical. Also stores the results as the DataFrame jackpots.
Params: None
Returns: (int) count of how many jackpots there were

Description: Computes the distinct combinations of faces rolled and their counts. Stores the results in the DataFrame combos
Params: None
Returns: None

Description: Computes how many times each face was rolled in each roll and stores the results in the DataFrame face_count
Params: None
Returns: None

### Attributes

jackpots = (DataFrame) with the roll # as index and boolean values for if the roll was a jackpot or not. Created with .jackpot()

combos = pd.DataFrame with a multi-columned index with each Die as an index, the rolled face as the index value, and  
the amount of times the entire roll combination occured in the Game as the value. Created with .combo()

face_count = pd.DataFrame with the roll # as index , the face values as columns, and the count of the face per roll as 
the value. Created with .face_counts()

# Manifest

montecarlo/
    LICENSE.txt
    montecarlo_tests.py
    montecarlo_tests_results.txt
    montecarlo_scenarios.ipynb
    README.md
    setup.py
    montecarlo/
        __init__.py
        montecarlo.py