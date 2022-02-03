
import unittest
from covidmodule import *


class TestCovidPlot(unittest.TestCase):

    def setUp(self):

        self.plotparent = Tk()
        self.plotspace = LabelFrame(self.plotparent)
        self.sm = 'March'
        self.em = 'March'
        self.sd = '16'
        self.ed = '20'
        self.sy = '2020'
        self.ey = '2020'
        self.cage = ''
        self.carea = 'Hartlepool'
        self.careatype = 'ltla'
        self.quest = 'All Cases in UK'
        self.covid_data = pd.DataFrame({'areaType': ['ltla','ltla','ltla','ltla','ltla'],
                                   'areaCode':	['E06000001','E06000001','E06000001','E06000001','E06000001'],
                                   'areaName': ['Hartlepool','Hartlepool','Hartlepool','Hartlepool','Hartlepool'],
                                   'date': ['16/03/2020', '17/03/2020', '18/03/2020', '19/03/2020','20/03/2020'],
                                   'Age 0-4':[0,0,0,0,0],
                                   'Age 0-59':[0,0,0,0,0],
                                   'Age 10-14':[0,0,0,0,0],
                                   'Age 15-19':[0,0,0,0,0],
                                   'Age 20-24':[0,0,0,0,0],
                                   'Age 25-29':[0,0,0,0,0],
                                   'Age 30-34':[0,0,0,0,0],
                                   'Age 35-39':[0,0,0,0,0],
                                   'Age 40-44':[0,0,0,0,0],
                                   'Age 45-49':[0,0,0,0,0],
                                   'Age 50-54':[0,0,0,0,0],
                                   'Age 55-59':[0,0,0,0,0],
                                   'Age 5-9':[0,0,0,0,0],
                                   'Age 60+':[1,0,1,0,1],
                                   'Age 60-64':[1,0,0,0,0],
                                   'Age 65-69':[0,0,0,0,0],
                                   'Age 70-74':[0,0,0,0,0],
                                   'Age 75-79':[0,0,0,0,0],
                                   'Age 80-84':[0,0,1,0,0],
                                   'Age 85-89':[0,0,0,0,1],
                                   'Age 90+':[0,0,0,0,0],
                                   'Age Unassigned':[0,0,0,0,0],
                                   })
        
        self.covid_data['Total Cases'] = self.covid_data['Age 0-59']+self.covid_data['Age 60+']+self.covid_data['Age Unassigned']
        self.months = ['2020-03','2020-04','2020-05','2020-06','2020-07','2020-08','2020-09','2020-10','2020-11']
        self.covid_data['date'] = pd.to_datetime(self.covid_data['date'])
        self.columns_of_interest = ['Age 0-4', 'Age 0-59',
       'Age 10-14', 'Age 15-19', 'Age 20-24', 'Age 25-29', 'Age 30-34',
       'Age 35-39', 'Age 40-44', 'Age 45-49', 'Age 50-54', 'Age 55-59',
       'Age 5-9', 'Age 60+', 'Age 60-64', 'Age 65-69', 'Age 70-74',
       'Age 75-79', 'Age 80-84', 'Age 85-89', 'Age 90+', 'Age Unassigned','Total Cases']
        for columns in self.columns_of_interest:
            empty_list = [0]
            self.covid_data[columns+'_cum'] = self.covid_data[columns].cumsum()
            for index in range(1,5):
                if self.covid_data[columns][index-1]!=0:
                    k= (self.covid_data[columns][index]-self.covid_data[columns][index-1])/(self.covid_data[columns][index-1])
                else:
                    k=self.covid_data[columns][index]-self.covid_data[columns][index-1]/1
                empty_list.append(k)
            self.covid_data[columns+'daily%dif'] = empty_list
            self.covid_data[columns+'_cum_daily%dif'] = self.covid_data[columns+'daily%dif'].cumsum()
            
        
    def test_daily_cases_plot(self):
        self.covid_data_to_plot, self.plotly, self.gabby = daily_cases_plot(self.plotparent,self.plotspace,self.sm,self.em,self.sy,self.ey,self.sd,self.ed,self.cage,self.carea,self.careatype)
        self.assertListEqual(self.gabby,['Age 0-59_cum','Age 60+_cum','Total Cases_cum','Age Unassigned_cum'], 'not slicing through correct list ')
        self.assertIsNotNone(self.plotly,'not returning the correct number of plots')
        for items in self.columns_of_interest:
            self.assertListEqual(list(self.covid_data_to_plot[items].values),list(self.covid_data[items].values), 'Dataframe is not sliced as expected')
        for cols in list(self.covid_data_to_plot.columns):
            self.assertIn(cols,list(self.covid_data.columns), 'Dataframe column name is not sliced as expected') 

    def test_daily_cases_single_plot(self):
        self.cage = 'Age 0-4'
        self.covid_data_to_plot, self.plotly, self.gabby = daily_cases_plot(self.plotparent,self.plotspace,self.sm,self.em,self.sy,self.ey,self.sd,self.ed,self.cage,self.carea,self.careatype)
        self.assertIsNotNone(self.plotly, 'not returning the correct number of plots')
        self.assertEqual(self.gabby, 'Age 0-4_cum', 'not takeing correct column')
        

    def test_daily_cases_empty_data(self):
        covid_data = []
        daily_cases_plot(self.plotparent,self.plotspace,self.sm,self.em,self.sy,self.ey,self.sd,self.ed,self.cage,self.carea,self.careatype)
        self.assertRaises(KeyError)

 
    def test_percentage_daily_cases_plot(self):
        self.covid_data_to_plot, self.plotly, self.gabby = percentage_daily_cases_plot(self.plotparent,self.plotspace,self.sm,self.em,self.sy,self.ey,self.sd,self.ed,self.cage,self.carea,self.careatype)
        self.assertListEqual(self.gabby,['Age 0-59_cum_daily%dif','Age 60+_cum_daily%dif','Total Cases_cum_daily%dif','Age Unassigned_cum_daily%dif'], 'not slicing through correct list ')
        self.assertIsNotNone(self.plotly,'not returning the correct number of plots')
        for items in self.columns_of_interest:
            self.assertListEqual(list(self.covid_data_to_plot[items].values),list(self.covid_data[items].values), 'Dataframe is not sliced as expected')
        for cols in list(self.covid_data_to_plot.columns):
            self.assertIn(cols,list(self.covid_data.columns), 'Dataframe column name is not sliced as expected') 


    def test_percentage_daily_cases_single_plot(self):
        self.cage = 'Age 0-4'
        self.covid_data_to_plot, self.plotly, self.gabby = percentage_daily_cases_plot(self.plotparent,self.plotspace,self.sm,self.em,self.sy,self.ey,self.sd,self.ed,self.cage,self.carea,self.careatype)
        self.assertIsNotNone(self.plotly, 'not returning the correct number of plots')
        self.assertEqual(self.gabby, 'Age 0-4_cum_daily%dif', 'not takeing correct column')
        


    def test_percentage_daily_cases_empty_data(self):
        covid_data = []
        percentage_daily_cases_plot(self.plotparent,self.plotspace,self.sm,self.em,self.sy,self.ey,self.sd,self.ed,self.cage,self.carea,self.careatype)
        self.assertRaises(KeyError)


    def test_monthly_cases_plot(self):
        self.covid_data_to_plot, self.plotly, self.gabby = monthly_cases_plot(self.plotparent,self.plotspace,self.cage,self.carea,self.careatype)
        self.assertListEqual(self.gabby,['Age 0-59_cum','Age 60+_cum','Total Cases_cum','Age Unassigned_cum'], 'not slicing through correct list ')
        self.assertIsNotNone(self.plotly,'not returning the correct number of plots')
        self.assertListEqual(list(self.covid_data_to_plot['date'].drop_duplicates()),self.months, 'Dataframe is not sliced as expected')
        for cols in list(self.covid_data_to_plot.columns):
            self.assertIn(cols,list(self.covid_data.columns), 'Dataframe column name is not sliced as expected') 
    
    def test_monthly_cases_single_plot(self):
        self.cage = 'Age 0-4'
        self.covid_data_to_plot, self.plotly, self.gabby = monthly_cases_plot(self.plotparent,self.plotspace,self.cage,self.carea,self.careatype)
        self.assertIsNotNone(self.plotly, 'not returning the correct number of plots')
        self.assertEqual(self.gabby, 'Age 0-4_cum', 'not takeing correct column')
        

    def test_monthly_cases_empty_data(self):
        covid_data = []
        monthly_cases_plot(self.plotparent,self.plotspace,self.cage,self.carea,self.careatype)
        self.assertRaises(KeyError)
        

    def test_weekly_cases_plot(self):
        self.covid_data_to_plot, self.plotly, self.gabby, self.wakanda = weekly_cases_plot(self.plotparent,self.plotspace,self.sm,self.em,self.sy,self.ey,self.sd,self.ed,self.cage,self.carea,self.careatype)
        self.assertListEqual(self.gabby,['Age 0-59_cum','Age 60+_cum','Total Cases_cum','Age Unassigned_cum'], 'not slicing through correct list ')
        self.assertIsNotNone(self.plotly,'not returning the correct number of plots')
        for items in self.columns_of_interest:
            self.assertListEqual(list(self.covid_data_to_plot[items].values),list(self.covid_data[items].values), 'Dataframe is not sliced as expected')
        for cols in list(self.covid_data_to_plot.columns):
            self.assertIn(cols,list(self.covid_data.columns), 'Dataframe column name is not sliced as expected') 
        self.wakanda['date'] = pd.to_datetime(self.wakanda['date'].map(mdates.num2date)).dt.tz_localize(None)
        self.assertEqual('2020-03-09 00:00:00', str(self.wakanda['date'][0]), 'Not slicing weekly accordingly')
        self.assertEqual('2020-03-16 00:00:00', str(self.wakanda['date'][1]), 'Not slicing weekly accordingly')
        


    def test_weekly_cases_single_plot(self):
        self.cage = 'Age 0-4'
        self.covid_data_to_plot, self.plotly, self.gabby, self.wakanda = weekly_cases_plot(self.plotparent,self.plotspace,self.sm,self.em,self.sy,self.ey,self.sd,self.ed,self.cage,self.carea,self.careatype)
        self.assertIsNotNone(self.plotly, 'not returning the correct number of plots')
        self.assertEqual(self.gabby, 'Age 0-4_cum', 'not takeing correct column')
        self.wakanda['date'] = pd.to_datetime(self.wakanda['date'].map(mdates.num2date)).dt.tz_localize(None)
        self.assertEqual('2020-03-09 00:00:00', str(self.wakanda['date'][0]), 'Not slicing weekly accordingly')
        self.assertEqual('2020-03-16 00:00:00', str(self.wakanda['date'][1]), 'Not slicing weekly accordingly')
        
        

    def test_weekly_cases_empty_data(self):
        covid_data = []
        weekly_cases_plot(self.plotparent,self.plotspace,self.sm,self.em,self.sy,self.ey,self.sd,self.ed,self.cage,self.carea,self.careatype)
        self.assertRaises(KeyError)

    def test_qa_cov_func(self):
        self.covid_data_qa = qa_cov_func(self.plotparent,self.plotspace,self.sd,self.sm,self.sy,self.ed,self.em,self.ey,self.quest)
        self.assertEqual(self.covid_data_qa['All Sum'].values[0],4152)

    def tearDown(self):
        self.plotparent.destroy()

class TestCovidCompAnalysis(unittest.TestCase):
    
    def setUp(self):

        self.plotparent = Tk()
        self.plotspace = LabelFrame(self.plotparent)
        self.sm = 'March'
        self.em = 'March'
        self.sd = '16'
        self.ed = '20'
        self.sy = '2020'
        self.ey = '2020'
        self.cage1 = ''
        self.cage2 = ''
        self.carea1 = 'Hartlepool'
        self.carea2 = 'Halton'
        self.careatype1 = 'ltla'
        self.careatype2 = 'ltla'
        self.top = 'Daily'
        self.covid_data_I = pd.DataFrame({'areaType': ['ltla','ltla','ltla','ltla','ltla'],
                                   'areaCode':	['E06000001','E06000001','E06000001','E06000001','E06000001'],
                                   'areaName': ['Hartlepool','Hartlepool','Hartlepool','Hartlepool','Hartlepool'],
                                   'date': ['16/03/2020', '17/03/2020', '18/03/2020', '19/03/2020','20/03/2020'],
                                   'Age 0-4':[0,0,0,0,0],
                                   'Age 0-59':[0,0,0,0,0],
                                   'Age 10-14':[0,0,0,0,0],
                                   'Age 15-19':[0,0,0,0,0],
                                   'Age 20-24':[0,0,0,0,0],
                                   'Age 25-29':[0,0,0,0,0],
                                   'Age 30-34':[0,0,0,0,0],
                                   'Age 35-39':[0,0,0,0,0],
                                   'Age 40-44':[0,0,0,0,0],
                                   'Age 45-49':[0,0,0,0,0],
                                   'Age 50-54':[0,0,0,0,0],
                                   'Age 55-59':[0,0,0,0,0],
                                   'Age 5-9':[0,0,0,0,0],
                                   'Age 60+':[1,0,1,0,1],
                                   'Age 60-64':[1,0,0,0,0],
                                   'Age 65-69':[0,0,0,0,0],
                                   'Age 70-74':[0,0,0,0,0],
                                   'Age 75-79':[0,0,0,0,0],
                                   'Age 80-84':[0,0,1,0,0],
                                   'Age 85-89':[0,0,0,0,1],
                                   'Age 90+':[0,0,0,0,0],
                                   'Age Unassigned':[0,0,0,0,0],
                                   })
        
        self.covid_data_II = pd.DataFrame({'areaType': ['ltla','ltla','ltla','ltla','ltla'],
                                   'areaCode':	['E06000001','E06000001','E06000001','E06000001','E06000001'],
                                   'areaName': ['Halton','Halton','Halton','Halton','Halton'],
                                   'date': ['16/03/2020', '17/03/2020', '18/03/2020', '19/03/2020','20/03/2020'],
                                   'Age 0-4':[0,0,0,0,0],
                                   'Age 0-59':[0,2,0,0,0],
                                   'Age 10-14':[0,0,0,0,0],
                                   'Age 15-19':[0,0,0,0,0],
                                   'Age 20-24':[0,0,0,0,0],
                                   'Age 25-29':[0,0,0,0,0],
                                   'Age 30-34':[0,1,0,0,0],
                                   'Age 35-39':[0,0,0,0,0],
                                   'Age 40-44':[0,0,0,0,0],
                                   'Age 45-49':[0,0,0,0,0],
                                   'Age 50-54':[0,0,0,0,0],
                                   'Age 55-59':[0,1,0,0,0],
                                   'Age 5-9':[0,0,0,0,0],
                                   'Age 60+':[1,0,0,0,1],
                                   'Age 60-64':[1,0,0,0,0],
                                   'Age 65-69':[0,0,0,0,0],
                                   'Age 70-74':[0,0,0,0,0],
                                   'Age 75-79':[0,0,0,0,0],
                                   'Age 80-84':[0,0,0,0,1],
                                   'Age 85-89':[0,0,0,0,0],
                                   'Age 90+':[0,0,0,0,0],
                                   'Age Unassigned':[0,0,0,0,0],
                                   })
        
        
        self.covid_data_I['Total Cases'] = self.covid_data_I['Age 0-59'] + self.covid_data_I['Age 60+']+ self.covid_data_I['Age Unassigned']
        self.covid_data_II['Total Cases'] = self.covid_data_II['Age 0-59'] + self.covid_data_II['Age 60+']+ self.covid_data_II['Age Unassigned']
        self.covid_data_I['date'] = pd.to_datetime(self.covid_data_I['date'])
        self.covid_data_II['date'] = pd.to_datetime(self.covid_data_II['date'])
        self.columns_of_interest = ['Age 0-4', 'Age 0-59',
       'Age 10-14', 'Age 15-19', 'Age 20-24', 'Age 25-29', 'Age 30-34',
       'Age 35-39', 'Age 40-44', 'Age 45-49', 'Age 50-54', 'Age 55-59',
       'Age 5-9', 'Age 60+', 'Age 60-64', 'Age 65-69', 'Age 70-74',
       'Age 75-79', 'Age 80-84', 'Age 85-89', 'Age 90+', 'Age Unassigned','Total Cases']
        for columns in self.columns_of_interest:
            empty_list_I = [0]
            empty_list_II = [0]
            self.covid_data_I[columns+'_cum'] = self.covid_data_I[columns].cumsum()
            self.covid_data_II[columns+'_cum'] = self.covid_data_II[columns].cumsum()
            for index in range(1,5):
                if self.covid_data_I[columns][index-1]!=0:
                    kI= (self.covid_data_I[columns][index]-self.covid_data_I[columns][index-1])/(self.covid_data_I[columns][index-1])
                else:
                    kI=self.covid_data_I[columns][index]-self.covid_data_I[columns][index-1]/1
                    
                if self.covid_data_II[columns][index-1]!=0:
                    kII= (self.covid_data_II[columns][index]-self.covid_data_II[columns][index-1])/(self.covid_data_II[columns][index-1])
                else:
                    kII=self.covid_data_II[columns][index]-self.covid_data_II[columns][index-1]/1
                empty_list_I.append(kI)
                empty_list_II.append(kII)
            self.covid_data_I[columns+'daily%dif'] = empty_list_I
            self.covid_data_I[columns+'_cum_daily%dif'] = self.covid_data_I[columns+'daily%dif'].cumsum()
            self.covid_data_II[columns+'daily%dif'] = empty_list_II
            self.covid_data_II[columns+'_cum_daily%dif'] = self.covid_data_II[columns+'daily%dif'].cumsum()
  
    def test_comp_anal_func(self):
        self.covid_data_1, self.covid_data_2, self.gabby, self.plotly = comp_analysis_func(self.plotparent,self.plotspace,
                                                                                           self.sm,self.em,
                                                                                           self.sy,self.ey,self.sd,
                                                                                           self.ed,self.cage1,self.cage2,self.carea1,
                                                                                           self.carea2,self.careatype1,
                                                                                           self.careatype2,self.top)
        
        self.assertListEqual(self.gabby,['Age 0-59','Age 60+','Total Cases','Age Unassigned'], 'not slicing through correct list ')
        self.assertIsNotNone(self.plotly,'there is a problem with your ploting call')
        for items in self.columns_of_interest:
            self.assertListEqual(list(self.covid_data_1[items].values),list(self.covid_data_I[items].values), 'Dataframe1 is not sliced as expected')
            self.assertListEqual(list(self.covid_data_2[items].values),list(self.covid_data_II[items].values), 'Dataframe2 is not sliced as expected')
        for cols in list(self.covid_data_1.columns):
            self.assertIn(cols,list(self.covid_data_I.columns), 'Dataframe1 column name is not sliced as expected') 
        for cols in list(self.covid_data_2.columns):
            self.assertIn(cols,list(self.covid_data_II.columns), 'Dataframe2 column name is not sliced as expected') 

    def test_cummulative_comp_anal_func(self):
        self.top = 'Cummulative'
        self.covid_data_1, self.covid_data_2, self.gabby, self.plotly = comp_analysis_func(self.plotparent,self.plotspace,
                                                                                           self.sm,self.em,
                                                                                           self.sy,self.ey,self.sd,
                                                                                           self.ed,self.cage1,self.cage2,self.carea1,
                                                                                           self.carea2,self.careatype1,
                                                                                           self.careatype2,self.top)
        self.assertListEqual(self.gabby,['Age 0-59_cum','Age 60+_cum','Total Cases_cum','Age Unassigned_cum'], 'list is not sliced as expected')
        
    def test_comp_anal_with_age_func(self):
        self.cage1 = 'Age 0-4'
        self.cage2 = 'Age 0-4'
        self.covid_data_1, self.covid_data_2, self.gabby, self.plotly = comp_analysis_func(self.plotparent,self.plotspace,
                                                                                           self.sm,self.em,
                                                                                           self.sy,self.ey,self.sd,
                                                                                           self.ed,self.cage1,self.cage2,self.carea1,
                                                                                           self.carea2,self.careatype1,self.careatype2,self.top)
        self.assertIsNotNone(self.plotly,'there is a problem with your ploting call')
        
        for items in ['Age 0-4']:
            self.assertListEqual(list(self.covid_data_1[items].values),list(self.covid_data_I[items].values), 'Dataframe1 is not sliced as expected')
            self.assertListEqual(list(self.covid_data_2[items].values),list(self.covid_data_II[items].values), 'Dataframe2 is not sliced as expected')
        for cols in list(self.covid_data_1.columns):
            self.assertIn(cols,['date','Age 0-4'], 'Dataframe1 column name is not sliced as expected') 
        for cols in list(self.covid_data_2.columns):
            self.assertIn(cols,['date','Age 0-4'], 'Dataframe2 column name is not sliced as expected')                                                                                   


    def test_comp_anal_empty_df(self):
        covid_data= []
        comp_analysis_func(self.plotparent,self.plotspace,self.sm,self.em,
                           self.sy,self.ey,self.sd,self.ed,self.cage1,self.cage2,self.carea1,
                           self.carea2,self.careatype1,self.careatype2,self.top)
        self.assertRaises(KeyError)

    def tearDown(self):
        self.plotparent.destroy()

if __name__ == '__main__':
    unittest.main()        
        