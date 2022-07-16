import unittest
from montecarlo import *

class TestMonteCarlo(unittest.TestCase):
    fcoin = Die(["H", "T"])
    ucoin = Die(["H","T"])
    ucoin.w_change("H",5)
    fdie = Die(list(range(1,7)))
    udie = Die(list(range(1,7)))
    udie.w_change(6,5)
    fgame = Game([fdie,fdie])
    fanal = Analyzer(fgame)
    
    
    #Die Unit Tests
    
    def test_Die_init(self):
        """Tests if Die initializes correctly by putting the faces in the Die's df index"""
        die = Die(["H", "T"])
        self.assertTrue(die._df.w[0] == 1.0, die._df.index.tolist() == ["H","T"])
    
    def test_weight_change_success(self):
        """ tests if Die's w_change() function will accurately change a face's weight given a string"""
        self.fcoin.w_change("H",2.0)
        self.assertEqual(self.fcoin._df.loc["H"].values, 2.0)
    
    def test_weight_change_fail(self):
        """tests if Die's w_change() function does not change the weight if given an improper value"""
        self.fcoin.w_change("H","D")
        self.assertEqual(self.fcoin._df.loc["H"].values, 1.0)
            
    def test_roll_length(self):
        """tests if Die's roll() function creates a list of the same length as given to the function"""
        x = self.fdie.roll(5)
        self.assertEqual(len(x),5)
        
    def test_roll_vals(self):
        """tests if a Die's roll() function produces values only within the faces"""
        x = self.fdie.roll()[0]
        self.assertTrue(1 <= x <= 6)
        
    def test_show(self):
        """test if Die's show() produces the same DataFrame as stored within Die"""
        show = self.udie.show()
        x = self.udie._df.equals(show)
        self.assertTrue(x)
        
    #Game Unit Tests    
    
    def test_Game_init(self):
        """tests if Game's initializer accurately and consistently stores the Die it is given"""
        x = Game([self.fdie,self.fdie])
        self.assertEqual(x.dice,self.fgame.dice)
        
    def test_play_shape(self):
        """tests if Game's play() creates a DataFrame of the correct shape (rolls, amt of Die)"""
        self.fgame.play(10)
        self.assertEqual(self.fgame._df.shape, (10,2))
    
    def test_play_index(self):
        """tests if Game's play() creates a DataFrame  with an index of the rolls"""
        self.fgame.play(10)
        self.assertEqual(self.fgame._df.index.values.tolist(), list(range(1,11)))
        
    def test_show_shape(self):
        """tests if Game's show() produces the expected shape (rolls, amt of Die)"""
        self.fgame.play(5)
        self.assertEqual(self.fgame._df.shape, (5,2))
    
    
    #Analyzer Unit Tests
    
    def test_anal_init(self):
        """tests if Analyzer's initializer accurately stores the Game it is given"""
        self.fgame.play(5)
        test = Analyzer(self.fgame)
        x = test.game._df
        btest = self.fanal.game._df.equals(x)
        self.assertTrue(btest)
    
    def test_anal_jackpot_df(self):
        """tests if Analyzer's jackpot() function creates a DataFrame to store the results"""
        self.fgame.play(5)
        self.fanal.jackpot()
        self.assertIsInstance(self.fanal.jackpots, pd.DataFrame)
        
    def test_anal_combo_index_shape(self):
        """tests if Analyzer's combo() function creates index's of the correct shape(len should be equal to how many Die there are)"""
        self.fgame.play(100)
        self.fanal.combo()
        indexlist = self.fanal.combos.index.tolist()
        self.assertEqual(len(indexlist[0]), 2)
        
    def test_face_counts_shape(self):
        """tests if Analyzer's face_counts() function creates a DataFrame of the correct shape to store the results (rolls, Die)"""
        self.fgame.play(100)
        self.fanal.face_counts()
        x = self.fanal.face_count.shape
        self.assertEqual(x, (100,6))
        
if __name__ == '__main__':
    unittest.main(verbosity=3)