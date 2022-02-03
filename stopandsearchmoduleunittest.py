import unittest
from stopandsearchmodule import *

class TestPolOOS(unittest.TestCase):
    def setUp(self):
        self.plotparent = Tk()
        self.plotspace = LabelFrame(self.plotparent)
        self.startyear = '2020'
        self.endyear = '2020'
        self.startmonth = 'February'
        self.endmonth = 'February'
        self.force = 'Avon and Somerset Constabulary'
        self.top = 'Total Number of Arrests'
        self.force1 = 'Avon and Somerset Constabulary'
        self.force2 = 'Cleveland Police'
        self.quest = 'Most Reason for Stop and Search'
        
        
        
        self.confirmation = requests.get('https://data.police.uk/api/stops-force?force=avon-and-somerset&date=2020-02')
        self.force1_confirmation = requests.get('https://data.police.uk/api/stops-force?force=avon-and-somerset&date=2020-02')
        self.force2_confirmation = requests.get('https://data.police.uk/api/stops-force?force=cleveland&date=2020-02')
        
        
    def test_pol_oos(self):
        self.police_data_request,self.plotly = pol_oos(self.plotparent,self.plotspace,self.startyear,self.endyear,self.startmonth,self.endmonth,self.force,self.top)
        self.assertEqual(self.police_data_request.content,self.confirmation.content, 'Data is wrongly imported')
        self.assertIsNotNone(self.plotly,'axes subplot is not working')
        
        
    def test_pol_oos_empty_dataframe(self):
        police_data_request= []
        self.police_data_request,self.plotly = pol_oos(self.plotparent,self.plotspace,self.startyear,self.endyear,self.startmonth,self.endmonth,self.force,self.top)
        self.assertRaises(KeyError)
        
        
    def test_pol_comp_anal(self):
        self.police_data_request1, self.police_data_request2, self.plotly = pol_companalfunc(self.plotparent, self.plotspace, self.startyear, self.endyear, self.startmonth, self.endmonth, self.force1, self.force2, self.top)
        self.assertEqual(self.police_data_request1.content,self.force1_confirmation.content, 'Data is wrongly imported')
        self.assertEqual(self.police_data_request2.content,self.force2_confirmation.content, 'Data is wrongly imported')
        self.assertIsNotNone(self.plotly,'axes subplot is not working')
        
    def test_pol_comp_anal_empty_dataframe(self):
        police_data_request1= []
        police_data_request2 =[]
        self.police_data_request1, self.police_data_request2, self.plotly = pol_companalfunc(self.plotparent, self.plotspace, self.startyear, self.endyear, self.startmonth, self.endmonth, self.force1, self.force2, self.top)
        self.assertRaises(KeyError)
        
    def test_pol_comp_anal_with_top(self):
        self.top = 'Age Range of Suspects'
        self.police_data_request1, self.police_data_request2, self.plotly = pol_companalfunc(self.plotparent, self.plotspace, self.startyear, self.endyear, self.startmonth, self.endmonth, self.force1, self.force2, self.top)
        self.assertIsNotNone(self.plotly,'axes subplot is not working')
        
    def test_pol_qa(self):
        self.police_data_request, self.dataset_ans = qa_ss_func(self.plotparent,self.plotspace,self.startyear,self.endyear,self.startmonth,self.endmonth,self.force,self.quest)
        self.assertEqual(self.police_data_request.content,self.confirmation.content, 'Data wrongly imported')
        self.assertEqual(self.dataset_ans.index[0],'Controlled drugs', 'Not giving right answer')
        
        
if __name__ == '__main__':
    unittest.main()        
                
        
        
        
        
        