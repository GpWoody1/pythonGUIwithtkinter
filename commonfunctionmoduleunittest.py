
import unittest
from commonfunctionmodule import *


class TestSetLabelStuff(unittest.TestCase):
    def setUp(self):
        fig = Figure(figsize=(5,5))
        self.plot = fig.add_subplot()
    def test_set_label_stuff(self):
        set_label_stuff(self.plot,'This should be a Y axis', 'This should be an x axis')
        self.assertEqual(self.plot.get_xlabel(),'This should be an x axis', 'Xlabel NOT passes')
        self.assertEqual(self.plot.get_ylabel(), 'This should be a Y axis', 'Ylabel NOT passes')

    

class TestEmptyPlotSpace(unittest.TestCase):
    def setUp(self):
        tk_item = Tk()
        self.frame = LabelFrame(tk_item)
        
    def test_plot_space_empty(self):
        emptyplotspace(self.frame)
        self.assertEqual(self.frame.winfo_children(), [], 'The function does not clears all items in the frame')
        


class TestPlotMe(unittest.TestCase):
    def setUp(self):
        self.tk = Tk()
    def test_plot_me(self):
        self.plotly, self.fig = plot_me([111],self.tk)
        self.assertIsInstance(self.plotly[0],matplotlib.axes.Axes,'Plotly does not seem to be a matplotlib instance of axis')
    def tearDown(self):
        self.tk.destroy()

class TestCov_Pg1_Clr(unittest.TestCase):
    def setUp(self):
        self.tk = Tk()
        self.covstartday = StringVar()
        self.covareatype = StringVar()
        self.covstartday.set('I am a bug')
    
    
    def test_cov_pg1_clr(self):
        covpg1_clr(self.covstartday, self.covareatype )
        self.assertEqual(self.covstartday.get(),'', 'The clear button is not clearing items as it should')
        self.assertEqual(self.covareatype.get(),'', 'The clear button is not clearing items as it should')

    def tearDown(self):
        self.tk.destroy()
    
class Test_Go_bk(unittest.TestCase):
    def setUp(self):
        self.tetris = Tk()
    def test_go_bk(self):
        go_bk(self.tetris)
        self.assertRaises(TclError,self.tetris.state)
        
        
class TestEndProgram(unittest.TestCase):
    def test_end_program(self):
        self.root= Tk()
        end_program(self.root)
        self.assertRaises(TclError,self.root.state)

if __name__ == '__main__':
    unittest.main()        
        