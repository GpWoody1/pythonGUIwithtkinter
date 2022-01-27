from tkinter import *
import pandas as pd
import numpy as np
import datetime 
import matplotlib.dates as mdates
from datetime import timedelta
from datetime import datetime
from dateutil.relativedelta import relativedelta
from calendar import month_name
from commonfunctionmodule import *
##----------------------------------------------------------------------------------------------
## COVID 19 DATA PREPROCESSING
##----------------------------------------------------------------------------------------------
covid_data = pd.read_csv("static/specimenDate_ageDemographic-unstacked.csv")
needed_columns = ['areaType', 'areaCode', 'areaName', 'date',
       'newCasesBySpecimenDate-0_4', 'newCasesBySpecimenDate-0_59',
       'newCasesBySpecimenDate-10_14', 'newCasesBySpecimenDate-15_19',
       'newCasesBySpecimenDate-20_24', 'newCasesBySpecimenDate-25_29',
       'newCasesBySpecimenDate-30_34', 'newCasesBySpecimenDate-35_39',
       'newCasesBySpecimenDate-40_44', 'newCasesBySpecimenDate-45_49',
       'newCasesBySpecimenDate-50_54', 'newCasesBySpecimenDate-55_59',
       'newCasesBySpecimenDate-5_9', 'newCasesBySpecimenDate-60+',
       'newCasesBySpecimenDate-60_64', 'newCasesBySpecimenDate-65_69',
       'newCasesBySpecimenDate-70_74', 'newCasesBySpecimenDate-75_79',
       'newCasesBySpecimenDate-80_84', 'newCasesBySpecimenDate-85_89',
       'newCasesBySpecimenDate-90+', 'newCasesBySpecimenDate-unassigned']
covid_data= covid_data[needed_columns]
covid_data.columns = ['areaType', 'areaCode', 'areaName', 'date', 'Age 0-4', 'Age 0-59',
       'Age 10-14', 'Age 15-19',
       'Age 20-24', 'Age 25-29',
       'Age 30-34', 'Age 35-39',
       'Age 40-44', 'Age 45-49',
       'Age 50-54', 'Age 55-59',
       'Age 5-9', 'Age 60+',
       'Age 60-64', 'Age 65-69',
       'Age 70-74', 'Age 75-79',
       'Age 80-84', 'Age 85-89',
       'Age 90+', 'Age Unassigned']
covid_data.drop_duplicates()
covid_data['Total Cases'] = covid_data['Age 0-59']+covid_data['Age 60+']+covid_data['Age Unassigned']
covid_data['date'] = pd.to_datetime(covid_data['date'])
covid_data['date'].drop_duplicates()
covid_days = [i for i in covid_data['date'].dt.strftime('%d').drop_duplicates().sort_values()]
covid_months = [i for i in covid_data['date'].drop_duplicates().sort_values().dt.strftime('%B').drop_duplicates()]
covid_years = [i for i in covid_data['date'].dt.strftime('%Y').drop_duplicates().sort_values()]
covid_locs = [i for i in covid_data['areaName'].drop_duplicates().sort_values()]
covid_age = ['Age 0-4', 'Age 5-9', 
       'Age 10-14', 'Age 15-19',
       'Age 20-24', 'Age 25-29',
       'Age 30-34', 'Age 35-39',
       'Age 40-44', 'Age 45-49',
       'Age 50-54', 'Age 55-59',
       'Age 60-64', 'Age 65-69',
       'Age 70-74', 'Age 75-79',
       'Age 80-84', 'Age 85-89','Age 0-59', 'Age 60+',
       'Age 90+', 'Age Unassigned','Total Cases','']

covid_areatype = [i for  i in covid_data['areaType'].drop_duplicates().sort_values()]

arz= covid_data[['areaType', 'areaName']].drop_duplicates()
coi = ['Age 0-4', 'Age 0-59',
       'Age 10-14', 'Age 15-19',
       'Age 20-24', 'Age 25-29',
       'Age 30-34', 'Age 35-39',
       'Age 40-44', 'Age 45-49',
       'Age 50-54', 'Age 55-59',
       'Age 5-9', 'Age 60+',
       'Age 60-64', 'Age 65-69',
       'Age 70-74', 'Age 75-79',
       'Age 80-84', 'Age 85-89',
       'Age 90+', 'Age Unassigned','Total Cases']


#---------------------------------------------------------------------------------------------
#create new columns to show % daily difference rate and cumdaily cases
#---------------------------------------------------------------------------------------------
for columns in coi:
    dic ={}
    dic1 ={}
    dic2= {}
    for index,alloc in arz.iterrows():
        z=[0]
        x= covid_data['areaName']==alloc['areaName']
        y= covid_data['areaType']==alloc['areaType']
        p= x & y
        covid_met = covid_data[p]
        index_stuff= covid_data[p].index
        covid_met.reset_index(drop=True, inplace=True)
        for j in range(1,len(covid_met)):
            if covid_met[columns][j-1] == 0:
                k= (covid_met[columns][j] - covid_met[columns][j-1])/1
            else:
                k= (covid_met[columns][j] - covid_met[columns][j-1])/covid_met[columns][j-1]
            z.append(k)
        small_df = pd.Series(z)
        small_df.replace([np.inf, -np.inf], np.nan, inplace=True)
        k1 = covid_met[columns].cumsum()
        k2 = small_df.cumsum()
        for items in index_stuff:
            dic[items] = z[int(index_stuff.get_indexer([items]))]*100
            dic1[items] = k1[int(index_stuff.get_indexer([items]))]
            dic2[items] = k2[int(index_stuff.get_indexer([items]))]*100
    covid_data[columns+'daily%dif'] = dic.values()
    covid_data[columns+'_cum_daily%dif'] = dic2.values()
    covid_data[columns+'_cum']= dic1.values()
covid_data.replace([np.inf, -np.inf], np.nan, inplace=True)
covid_data = covid_data.fillna(0)

#---------------------------------------------------------------------------------------------------------------------
##Define covid functions
#---------------------------------------------------------------------------------------------------------------------

def daily_cases_plot(plotparent,plotspace,startmonth,endmonth,startyear,endyear,startday,endday,cage,carea,careatype):
    """
    function for plotting daily cases plots
    """
    
    emptyplotspace(plotspace)
    try:    
        cov_given_month = datetime.strptime(startmonth, '%B')
        cov_given_end_month = datetime.strptime(endmonth, '%B')
        given_cov_startdate = startyear+'-'+cov_given_month.strftime('%m')+'-'+ startday
        given_cov_enddate = endyear+'-'+cov_given_end_month.strftime('%m')+'-'+ endday
        covid_data_to_plot = covid_data[(covid_data['date'] >= given_cov_startdate) & (covid_data['date'] <= given_cov_enddate) & (covid_data['areaName']==carea)&(covid_data['areaType']==careatype)]
        covid_data_to_plot.loc[:,'date'] = covid_data_to_plot['date'].map(mdates.date2num)
        
        if cage == '' or cage == 'Optional':
            plotly,fig = plot_me([221,222,223,224],plotspace)
            fig.suptitle('Cummulative Daily plot of '+carea+' from '+given_cov_startdate+ ' to '+ given_cov_enddate, fontsize=10, fontweight='bold')
            
            gabby = ['Age 0-59_cum','Age 60+_cum','Total Cases_cum','Age Unassigned_cum']
            for items in gabby:
                plotly[gabby.index(items)].set_title(items+'mulative Cases', fontsize='medium')
                plotly[gabby.index(items)].xaxis_date()
                wakanda = covid_data_to_plot[['date',items]]
                plotly[gabby.index(items)].xaxis_date()
                wakanda.plot(x='date', y=items, kind='line', ax=plotly[gabby.index(items)])
                avg = wakanda[items].mean()
                plotly[gabby.index(items)].axhline(y=avg, color='red', label='AVG Cases', linestyle='--', linewidth=1, dash_capstyle='round', fillstyle='left')
                plotly[gabby.index(items)].tick_params(axis='x', rotation=60, labelsize=6)
                plotly[gabby.index(items)].tick_params(axis='y', labelsize=6)
                plotly[gabby.index(items)].legend(loc=0, fontsize='small')
                set_label_stuff(plotly[gabby.index(items)],'No. Cases', 'Date')
            
            if covid_data_to_plot.empty == True:
                selection_error_flag= messagebox.showerror('Error in Entry','Oops! Your entry did not bring back any data. Please try another selection')
                if selection_error_flag == 'ok':
                    emptyplotspace(plotspace)
                    

        else: 
            gabby=cage+'_cum'
            plotly,fig = plot_me([111],plotspace)
            fig.suptitle('Cummulative Daily plot of '+carea+' from '+given_cov_startdate+ ' to '+ given_cov_enddate, fontsize=10, fontweight='bold')
            
            wakanda2 = covid_data_to_plot[['date',gabby]]
            plotly[0].set(title= cage+' Cummulative Cases')
            plotly[0].xaxis_date()
            
            wakanda2.plot(x='date', y=gabby, kind='line', ax=plotly[0])
            
            avg = wakanda2[gabby].mean()
            plotly[0].axhline(y=avg, color='red', label='AVG Cases', linestyle='--', linewidth=1, dash_capstyle='round', fillstyle='left')
               

            plotly[0].tick_params(axis ='x', rotation=60, labelsize= 8)
            plotly[0].tick_params(axis ='y', labelsize= 8)
            plotly[0].legend(loc=0)
            set_label_stuff(plotly[0],'No. Cases', 'Date')
            
            if covid_data_to_plot.empty == True:
                selection_error_flag= messagebox.showerror('Error in Entry','Oops! Your query did not bring back any result. Please check your entry and try another selection')
                if selection_error_flag == 'ok':
                    emptyplotspace(plotspace)
     
        
            
    except (ValueError, KeyError, TypeError):
        response_to_error = messagebox.askquestion('An error occured','Oops!Looks like you have an empty or incorrect entry. Would you like to try again?')
        if response_to_error=='no':
            plotparent.destroy()   
            
    return(covid_data_to_plot, plotly, gabby)
        
def percentage_daily_cases_plot(plotparent,plotspace,startmonth,endmonth,startyear,endyear,startday,endday,cage,carea,careatype):
    """
    Function for plotting percentage daily plots
    """
    emptyplotspace(plotspace)
    try:
        cov_given_month = datetime.strptime(startmonth, '%B')
        cov_given_end_month = datetime.strptime(endmonth, '%B')
        given_cov_startdate = startyear+'-'+cov_given_month.strftime('%m')+'-'+startday
        given_cov_enddate = endyear+'-'+cov_given_end_month.strftime('%m')+'-'+endday
        covid_data_to_plot = covid_data[(covid_data['date'] >= given_cov_startdate) & (covid_data['date'] <= given_cov_enddate) & (covid_data['areaName']==carea)&(covid_data['areaType']==careatype)]
        covid_data_to_plot.loc[:,'date'] = covid_data_to_plot['date'].map(mdates.date2num)
        
        if cage =='' or cage == 'Optional':
            plotly,fig = plot_me([221,222,223,224],plotspace)
            fig.suptitle('% Cummulative Daily plot of '+carea+' from '+given_cov_startdate+ ' to '+ given_cov_enddate, fontsize=10, fontweight='bold')
            
            title_of_this = ['Age 0-59 %Daily Difference','Age 60+ %Daily Difference','Total Cases %Daily Difference','Unassigned %Daily Difference']
            gabby = ['Age 0-59_cum_daily%dif','Age 60+_cum_daily%dif','Total Cases_cum_daily%dif','Age Unassigned_cum_daily%dif']    
            
            
            for items in gabby:
                plotly[gabby.index(items)].set_title (title_of_this[gabby.index(items)],fontsize='medium')
                plotly[gabby.index(items)].xaxis_date()
                covid_data_to_plot.plot(x='date', y=items, kind='line', ax=plotly[gabby.index(items)])
                avg= covid_data_to_plot[items].mean()
                plotly[gabby.index(items)].axhline(y=avg, color='red', label='AVG Cases', linestyle='--', linewidth= 1, dash_capstyle='round', fillstyle='left')
                plotly[gabby.index(items)].tick_params(axis='x', rotation=60, labelsize=6)
                plotly[gabby.index(items)].tick_params(axis='y', labelsize=6)
                plotly[gabby.index(items)].legend(loc=0, fontsize='small')
                set_label_stuff(plotly[gabby.index(items)],'% of Cases', 'Date')
            
            if covid_data_to_plot.empty == True:
                selection_error_flag= messagebox.showerror('Error in Entry','Oops! Your query did not bring back any result. Please check your entry and try another selection')
                if selection_error_flag == 'ok':
                    emptyplotspace(plotspace)

            
        else:
            gabby = cage+'_cum_daily%dif'
            plotly, fig = plot_me([111],plotspace)
            fig.suptitle('% Cummulative Daily plot of '+carea+' from '+given_cov_startdate+ ' to '+ given_cov_enddate, fontsize=10, fontweight='bold')
                
            covid_data_to_plot = covid_data_to_plot[['date',gabby]]
                
            plotly[0].set(title= cage+' %Daily Difference')
            plotly[0].xaxis_date()
                
            covid_data_to_plot.plot(x='date', y=gabby, kind='line', ax=plotly[0])
            
            avg= covid_data_to_plot[gabby].mean()
            plotly[0].axhline(y=avg, color='red', label='AVG Cases', linestyle='--', linewidth=1, dash_capstyle='round', fillstyle='left')

                
            plotly[0].tick_params(axis ='x',rotation=60, labelsize=8)
            plotly[0].tick_params(axis ='y', labelsize=8)
            plotly[0].legend(loc=0)
            set_label_stuff(plotly[0],'% of Cases', 'Date')
                
            if covid_data_to_plot.empty == True:
                selection_error_flag= messagebox.showerror('Error in Entry','Oops! Your query did not bring back any result. Please check your entry and try another selection')
                if selection_error_flag == 'ok':
                    emptyplotspace(plotspace)

                    

    except (ValueError, KeyError, TypeError):
        response_to_error = messagebox.askquestion('An error occured','Oops!Looks like you have an empty or incorrect entry. Would you like to try again?')
        if response_to_error=='no':
            plotparent.destroy()
            
    return(covid_data_to_plot, plotly, gabby)
        
def monthly_cases_plot(parentplot, plotspaces, age, covarea, covareatype):
    """
    Function for plotting monthly covid cases
    
    """
    emptyplotspace(plotspaces)
    try:

        covid_data_to_plot = covid_data[(covid_data['areaName']==covarea) & (covid_data['areaType']==covareatype)]
        covid_data_to_plot.loc[:,'date'] = covid_data_to_plot['date'].dt.strftime('%Y-%m')
        
        
        
        if age == '' or age == 'Optional':
            plotly,fig = plot_me([221,222,223,224],plotspaces)
            fig.suptitle('Monthly plot of '+covarea+' from '+str(covid_data_to_plot['date'].min())+ ' to '+ str(covid_data_to_plot['date'].max()), fontsize=10, fontweight='bold')
            
            
            title_of_this = ['Age 0-59 Monthly Cases','Age 60+ Monthly Cases','Total Cases Monthly Cases','Unassigned Monthly Cases']
            gabby = ['Age 0-59_cum','Age 60+_cum','Total Cases_cum','Age Unassigned_cum']
            
            for items in gabby:
                plotly[gabby.index(items)].set_title(title_of_this[gabby.index(items)], fontsize='medium')
                plotly[gabby.index(items)].xaxis_date()
                covid_data_to_plot.plot(x='date', y=items, kind='line', ax=plotly[gabby.index(items)])
                avg= covid_data_to_plot[items].mean()
                plotly[gabby.index(items)].axhline(y=avg, color='red', label= 'AVG Cases', linestyle = '--', linewidth=1,dash_capstyle='round', fillstyle='left')
                plotly[gabby.index(items)].tick_params(axis='x', rotation=60, labelsize=6)
                plotly[gabby.index(items)].tick_params(axis='y', labelsize=6)
                plotly[gabby.index(items)].legend(loc=0, fontsize='small')
                set_label_stuff(plotly[gabby.index(items)],'No. Cases','Month')
            
                
            if covid_data_to_plot.empty == True:
                selection_error_flag= messagebox.showerror('Error in Entry','Oops! Your query did not bring back any result. Please check your entry and try another selection')
                if selection_error_flag == 'ok':
                    emptyplotspace(plotspaces)

                    
        else:
            gabby = age+'_cum'
            plotly,fig = plot_me([111],plotspaces)
            fig.suptitle('Monthly plot of '+covarea+' from '+str(covid_data_to_plot['date'].min())+ ' to '+ str(covid_data_to_plot['date'].max()), fontsize=10, fontweight='bold')
        
            plotly[0].set(title= age+' Monthly cases')
            plotly[0].xaxis_date()
            covid_data_to_plot.plot(x='date', y=gabby, kind='line', ax=plotly[0])
            
            avg= covid_data_to_plot[gabby].mean()
            plotly[0].axhline(y=avg, color='red', label='AVG Cases', linestyle='--', linewidth=1, dash_capstyle='round', fillstyle='left')

                
            plotly[0].tick_params(axis ='x',rotation=60, labelsize=8)
            plotly[0].tick_params(axis ='y', labelsize=8)
            plotly[0].legend(loc=0)
            #plotly[0].legend().set_visible(False)
            set_label_stuff(plotly[0], 'No. Cases', 'Month')
            
            if covid_data_to_plot.empty == True:
                selection_error_flag= messagebox.showerror('Error in Entry','Oops! Your query did not bring back any result. Please check your entry and try another selection')
                if selection_error_flag == 'ok':
                    emptyplotspace(plotspaces)
                    pass
    except (ValueError, KeyError, TypeError):
        response_to_error = messagebox.askquestion('An error occured','Oops!Looks like you have an empty or incorrect entry. Would you like to try again?')
        if response_to_error=='no':
            parentplot.destroy()
            
    return(covid_data_to_plot, plotly, gabby)

def weekly_cases_plot(plotparent,plotspace,startmonth,endmonth,startyear,endyear,startday,endday,cage,carea,careatype):
    
    """
    Function for plotting weekly cases
    """
    
    emptyplotspace(plotspace)
    try:
        
        cov_given_month = datetime.strptime(startmonth, '%B')
        cov_given_end_month = datetime.strptime(endmonth, '%B')
        given_cov_startdate = startyear+'-'+cov_given_month.strftime('%m')+'-'+startday
        given_cov_enddate = endyear+'-'+cov_given_end_month.strftime('%m')+'-'+endday
        covid_data_to_plot = covid_data[(covid_data['date'] >= given_cov_startdate) & (covid_data['date'] <= given_cov_enddate) & (covid_data['areaName']==carea)&(covid_data['areaType']==careatype)]
        covid_data_to_plot.loc[:,'date'] = covid_data_to_plot['date'] - pd.to_timedelta(7, unit='d')
        
        
        
        if cage == '' or cage == 'Optional':
            plotly,fig = plot_me([221,222,223,224],plotspace)
            fig.suptitle('Weekly plot of '+carea+' from '+given_cov_startdate+ ' to '+ given_cov_enddate, fontsize=10, fontweight='bold')
            
            title_of_this=['Age 0-59 Weekly Difference','Age 60+ Weekly Difference','Total Cases Weekly Difference','Unassigned Weekly Difference']  
            gabby = ['Age 0-59_cum','Age 60+_cum','Total Cases_cum','Age Unassigned_cum']
            for items in gabby:
                wakanda = covid_data_to_plot.groupby(['areaName',pd.Grouper(key='date', freq='W-MON')])[items].sum().reset_index().sort_values('date')
                wakanda['date'] = wakanda['date'].map(mdates.date2num) 
                wakanda.plot(x='date',y=items,kind='line',ax=plotly[gabby.index(items)])
                avg= wakanda[items].mean()
                plotly[gabby.index(items)].set_title(title_of_this[gabby.index(items)], fontsize='medium')
                plotly[gabby.index(items)].axhline(y=avg, color='red', label='AVG Cases', linestyle='--', linewidth=1, dash_capstyle='round', fillstyle='left')
                plotly[gabby.index(items)].xaxis_date()
                plotly[gabby.index(items)].tick_params(axis='x', rotation=60, labelsize=6)
                plotly[gabby.index(items)].tick_params(axis='y', labelsize=6)
                plotly[gabby.index(items)].legend(loc=0, fontsize='small')
                set_label_stuff(plotly[gabby.index(items)], 'No. Cases','Date')
            
            
            
            if covid_data_to_plot.empty == True:
                selection_error_flag= messagebox.showerror('Error in Entry','Oops! Your query did not bring back any result. Please check your entry and try another selection')
                if selection_error_flag == 'ok':
                    emptyplotspace(plotspace)
                    pass
        
        else:
            gabby =cage+'_cum'
            plotly,fig = plot_me([111], plotspace)
            fig.suptitle('Weekly plot of '+carea+' from '+given_cov_startdate+ ' to '+ given_cov_enddate, fontsize=10, fontweight='bold')
            
            plotly[0].set(title= cage+'Weekly Difference')
            
            wakanda= covid_data_to_plot.groupby(['areaName',pd.Grouper(key='date', freq='W-MON')])[cage+'_cum'].sum().reset_index().sort_values('date')
            wakanda['date'] = wakanda['date'].map(mdates.date2num)
            wakanda.plot(x='date', y=gabby, kind='line', ax=plotly[0])
            avg= wakanda[cage+'_cum'].mean()
            plotly[0].axhline(y=avg, color='red', label='AVG Cases', linestyle='--', linewidth=1, dash_capstyle='round', fillstyle='left')      
            plotly[0].xaxis_date()
            plotly[0].tick_params(axis ='x',rotation=60, labelsize=8)
            plotly[0].tick_params(axis ='y', labelsize=8)
            plotly[0].legend(loc=0)
            set_label_stuff(plotly[0],'No. Cases', 'Date')
            
            if covid_data_to_plot.empty == True:
                selection_error_flag= messagebox.showerror('Error in Entry','Oops! Your query did not bring back any result. Please check your entry and try another selection')
                if selection_error_flag == 'ok':
                    emptyplotspace(plotspace)
                    pass
        
        
    except (ValueError, KeyError, TypeError):
        response_to_error = messagebox.askquestion('An error occured','Oops!Looks like you have an empty or incorrect entry. Would you like to try again?')
        if response_to_error=='no':
            plotparent.destroy()


    return (covid_data_to_plot, plotly, gabby, wakanda)

def comp_analysis_func(plotparent,plotspace,startmonth,endmonth,startyear,endyear,startday,endday,cage1,cage2,carea1,carea2,careatype1,careatype2,top):
    """
    Function for plotting comparative analysis plots
    """
    try:
        emptyplotspace(plotspace) 
        cov_given_month = datetime.strptime(startmonth, '%B')
        cov_given_end_month = datetime.strptime(endmonth, '%B')
        given_cov_startdate = startyear+'-'+cov_given_month.strftime('%m')+'-'+startday
        given_cov_enddate = endyear+'-'+cov_given_end_month.strftime('%m')+'-'+endday
        covid_data_1= covid_data[(covid_data['date'] >= given_cov_startdate) & (covid_data['date'] <= given_cov_enddate) & (covid_data['areaName']==carea1)&(covid_data['areaType']==careatype1)]
        covid_data_2= covid_data[(covid_data['date'] >= given_cov_startdate) & (covid_data['date'] <= given_cov_enddate) & (covid_data['areaName']==carea2)&(covid_data['areaType']==careatype2)]
        
        gabby1 = ['Age 0-59_cum','Age 60+_cum','Total Cases_cum','Age Unassigned_cum']
        gabby2 = ['Age 0-59','Age 60+','Total Cases','Age Unassigned']
        
        if top == 'Cummulative':
            gabby = gabby1
            single_plot_ax = cage1+'_cum'
            single_plot_ax2 = cage2+'_cum'
            y_name = 'Cummulative Cases'
        else:
            gabby = gabby2
            single_plot_ax = cage1
            single_plot_ax2 = cage2
            y_name = 'No. of Cases'
            
            
        if cage1=='' or cage1=='Optional' or cage2 =='' or cage2 == 'Optional':
            plotly,fig = plot_me([221,222,223,224], plotspace)
            for items in gabby:
                covid_data_1x = covid_data_1[['date',items]]
                covid_data_1x['date']= covid_data_1['date'].map(mdates.date2num)
                covid_data_2x = covid_data_2[['date',items]]
                covid_data_2x['date']= covid_data_2['date'].map(mdates.date2num)
                covid_data_1x.plot(x='date', y=items, kind='line', ax=plotly[gabby.index(items)])
                covid_data_2x.plot(x='date', y=items, kind='line', ax=plotly[gabby.index(items)])
        
                plotly[gabby.index(items)].xaxis_date()
                plotly[gabby.index(items)].tick_params(axis='x', rotation=60, labelsize=6)
                plotly[gabby.index(items)].tick_params(axis='y', labelsize=6)
                plotly[gabby.index(items)].legend([carea1,carea2], loc=0, fontsize='small')
                plotly[gabby.index(items)].set_title(items+' Cases', fontsize='medium')
                set_label_stuff(plotly[gabby.index(items)],y_name, 'Date')
            fig.suptitle('Plot of '+carea1+' & '+carea2, fontsize=12, fontweight='bold')
            if covid_data_1.empty == True or covid_data_2.empty==True:
                selection_error_flag= messagebox.showerror('Error in Entry','Oops! One or more of your entry did not bring back any data. Please try another selection')
                if selection_error_flag == 'ok':
                    emptyplotspace(plotspace)

            
        else:
            plotly,fig = plot_me([111], plotspace)
            covid_data_1 = covid_data_1[['date',single_plot_ax]]
            covid_data_1['date']= covid_data_1['date'].map(mdates.date2num)
            covid_data_2 = covid_data_2[['date',single_plot_ax2]]
            covid_data_2['date']= covid_data_2['date'].map(mdates.date2num)
            covid_data_1.plot(x='date', y=single_plot_ax, kind='line', ax=plotly[0])
            covid_data_2.plot(x='date', y=single_plot_ax2, kind='line', ax=plotly[0])
            plotly[0].xaxis_date()
            plotly[0].tick_params(axis ='x',rotation=60, labelsize=8)
            plotly[0].tick_params(axis ='y', labelsize=8)
            plotly[0].legend([carea1,carea2], loc=0)
            plotly[0].set(title=carea1+'('+cage1+')'+' & '+ carea2+'('+cage2+')')
            set_label_stuff(plotly[0],y_name,'Date')
            fig.suptitle('Plot of '+carea1+' & '+carea2, fontsize=12, fontweight='bold')
            
            if covid_data_1.empty == True or covid_data_2.empty==True:
                selection_error_flag= messagebox.showerror('Error in Entry','Oops! One or more of your entry did not bring back any data. Please try another selection')
                if selection_error_flag == 'ok':
                    emptyplotspace(plotspace)            
            
        
            
    except (ValueError, KeyError, TypeError, UnboundLocalError):
        response_to_error = messagebox.askquestion('An error occured','Oops!Looks like you have an empty or incorrect entry. Would you like to try again?')
        if response_to_error=='no':
            plotparent.destroy()    
        
    return(covid_data_1, covid_data_2, gabby, plotly)

def qa_cov_func(plotparent,plotspace,startday,startmonth,startyear,endday,endmonth,endyear,quest):
    """
    Function for covid19 Q&A
    """
    
    emptyplotspace(plotspace)
    try:
        
        cov_given_month = datetime.strptime(startmonth, '%B')
        cov_given_end_month = datetime.strptime(endmonth, '%B')
        given_cov_startdate = startyear+'-'+cov_given_month.strftime('%m')+'-'+startday
        given_cov_enddate = endyear+'-'+cov_given_end_month.strftime('%m')+'-'+endday
        covid_data_to_answer = covid_data[(covid_data['date'] >= given_cov_startdate) & (covid_data['date'] <= given_cov_enddate)]
   
        
        
        if quest == 'Area With Highest No. Cases':
            easter_egg = covid_data_to_answer[(covid_data_to_answer['areaType'] == 'ltla') | (covid_data_to_answer['areaType'] == 'utla')]
            covid_data_qa = easter_egg.groupby(['areaName','areaType'])[['Age 0-59','Age 60+','Age Unassigned']].sum()
            covid_data_qa ['All Sum'] = covid_data_qa['Age 0-59'] + covid_data_qa['Age 60+'] + covid_data_qa['Age Unassigned']
            tot_high_daily = covid_data_qa[covid_data_qa['All Sum'] == covid_data_qa['All Sum'].max()]
            tot_high_daily_answer = tot_high_daily.index[0]
            ans= Label(plotspace, text = "The area with highest number of cases in this period is \n"+ tot_high_daily_answer[0]+ ".\n In the area Type \n" + tot_high_daily_answer[1] + "\n with a total infected rate of \n"+ str(tot_high_daily['All Sum'].values[0]),font = ('Helvetica',14,'bold'), bg= '#36454F', fg='white')
            ans.pack(fill='both')
    
        
        elif quest == 'Area With Highest No. Cases(7day period)':
            covid_data_to_answer.loc[:,'date'] = covid_data_to_answer.loc[:,'date'] - pd.to_timedelta(7, unit='d') 
            easter_egg = covid_data_to_answer[(covid_data_to_answer['areaType'] == 'ltla') | (covid_data_to_answer['areaType'] == 'utla')]
            covid_data_qa= easter_egg.groupby(['areaName','areaType', pd.Grouper(key='date', freq='W-MON')])[['Age 0-59','Age 60+','Age Unassigned']].sum()
            covid_data_qa ['All Sum'] = covid_data_qa['Age 0-59'] + covid_data_qa['Age 60+'] + covid_data_qa['Age Unassigned']
            tot_high_daily = covid_data_qa[covid_data_qa['All Sum'] == covid_data_qa['All Sum'].max()]
            tot_high_daily_answer = tot_high_daily.index[0]
            ans= Label(plotspace, text = "The area with highest number per 7-day period is \n"+ tot_high_daily_answer[0]+ ".\n In the area Type \n" + tot_high_daily_answer[1] + "\n with a total infected rate of \n"+ str(tot_high_daily['All Sum'].values[0]) + '\n In the week commencing\n' +str(tot_high_daily_answer[2]),font = ('Helvetica',14,'bold'), bg= '#36454F', fg='white')
            ans.pack(fill='both')      
          
        
        elif quest == 'Area With Positive Largest Change of Cases':
            easter_egg = covid_data_to_answer[(covid_data_to_answer['areaType'] == 'ltla') | (covid_data_to_answer['areaType'] == 'utla')]
            covid_data_qa = easter_egg.groupby(['areaName','areaType'])[['Age 0-59daily%dif','Age 60+daily%dif','Age Unassigneddaily%dif']].sum()
            covid_data_qa ['All Sum'] = covid_data_qa['Age 0-59daily%dif'] + covid_data_qa['Age 60+daily%dif'] + covid_data_qa['Age Unassigneddaily%dif']
            tot_high_daily = covid_data_qa[covid_data_qa['All Sum'] == covid_data_qa['All Sum'].max()]
            tot_high_daily_answer = tot_high_daily.index[0]
            ans= Label(plotspace, text = "The area with Largest Positive Change of cases in this period is \n"+ tot_high_daily_answer[0]+ ".\n In the area Type \n" + tot_high_daily_answer[1] + "\n with a total positive change of \n"+ str(tot_high_daily['All Sum'].values[0])+'%',font = ('Helvetica',14,'bold'), bg= '#36454F', fg='white')
            ans.pack(fill='both')

     
        
        elif quest == 'Area With Positive Largest Change of Cases (7day period)':
            covid_data_to_answer['date'] = covid_data_to_answer['date'] - pd.to_timedelta(7, unit='d') 
            easter_egg = covid_data_to_answer[(covid_data_to_answer['areaType'] == 'ltla') | (covid_data_to_answer['areaType'] == 'utla')]
            covid_data_qa= easter_egg.groupby(['areaName','areaType', pd.Grouper(key='date', freq='W-MON')])[['Age 0-59daily%dif','Age 60+daily%dif','Age Unassigneddaily%dif']].sum()
            covid_data_qa ['All Sum'] = covid_data_qa['Age 0-59daily%dif'] + covid_data_qa['Age 60+daily%dif'] + covid_data_qa['Age Unassigneddaily%dif']
            tot_high_daily = covid_data_qa[covid_data_qa['All Sum'] == covid_data_qa['All Sum'].max()]
            tot_high_daily_answer = tot_high_daily.index[0]
            ans= Label(plotspace, text = "The area with Largest Positive Change of cases per 7-day period is \n"+ tot_high_daily_answer[0]+ ".\n In the area Type \n" + tot_high_daily_answer[1] + "\n with a total infected rate of \n"+ str(tot_high_daily['All Sum'].values[0])+'%' + '\n In the week commencing\n' +str(tot_high_daily_answer[2]),font = ('Helvetica',14,'bold'), bg= '#36454F', fg='white')
            ans.pack(fill='both')
            
            
            
        elif quest == 'All Cases in UK':
            easter_egg = covid_data_to_answer[(covid_data_to_answer['areaName'] == 'United Kingdom')]
            covid_data_qa = easter_egg.groupby(['areaName','areaType'])[['Age 0-59','Age 60+','Age Unassigned']].sum()
            covid_data_qa ['All Sum'] = covid_data_qa['Age 0-59'] + covid_data_qa['Age 60+'] + covid_data_qa['Age Unassigned']
            tot_high_daily = covid_data_qa
            tot_high_daily_answer = tot_high_daily.index[0]
            ans= Label(plotspace, text = "The total number of cases in \n"+ tot_high_daily_answer[0]+ "\n for this time period is \n" + str(tot_high_daily['All Sum'].values[0]),font = ('Helvetica',14,'bold'), bg= '#36454F', fg='white')
            ans.pack(fill='both')
            
            
    except (IndexError, KeyError, ValueError, TypeError):
        response_to_error = messagebox.askquestion('An error occured','Oops!Looks like you have an empty or incorrect entry. Would you like to try again?')
        if response_to_error=='no':
            plotparent.destroy() 
            
    return(covid_data_qa)

def cccompanal():  
    
    covcompstartday= StringVar()
    covcompstartmonth= StringVar()
    covcompstartyear= StringVar()
    covcompstartday.set(covid_days[0])
    covcompstartmonth.set(covid_months[0])
    covcompstartyear.set(covid_years[0])
    
    covcompendday= StringVar()
    covcompendmonth= StringVar()
    covcompendyear= StringVar()
    covcompage1= StringVar()
    covcompage2= StringVar()
    covcomptop = StringVar()
    covcompendday.set(covid_days[0])
    covcompendmonth.set(covid_months[0])
    covcompendyear.set(covid_years[0])
    covcompage1.set('Optional')
    covcompage2.set('Optional')
    covcomptop.set('Cummulative')
    
    covcomparea1=StringVar()
    covcomparea1.set(covid_locs[0])
    
    covcomparea2=StringVar()
    covcomparea2.set(covid_locs[0])
    
    covcompareatype1 = StringVar()
    covcompareatype1.set(covid_areatype[0])
    
    covcompareatype2 = StringVar()
    covcompareatype2.set(covid_areatype[0])
    
    Covpg2 = Toplevel()
    
    covpg2_Label = Label(Covpg2, text='Covid19 Comparative Analysis',bg='#AA4A44', fg='white', font = ('Helvetica',14,'bold'))
    covpg2_Frame1 = LabelFrame(Covpg2, padx=10, pady=10, bg= '#36454F')
    covpg2_Frame2= LabelFrame(Covpg2, padx=10, pady=10)
    covpg2_Frame1_sday= OptionMenu(covpg2_Frame1, covcompstartday, *covid_days)
    covpg2_Frame1_smonth= OptionMenu(covpg2_Frame1, covcompstartmonth, *covid_months)
    covpg2_Frame1_syear = OptionMenu(covpg2_Frame1, covcompstartyear, *covid_years)
    covpg2_Frame1_top = OptionMenu(covpg2_Frame1, covcomptop, 'Daily', 'Cummulative')
    
    sday_lab= Label(covpg2_Frame1, text= 'Select Start Day:', font = ('Helvetica',10,'bold'), bg= '#36454F', fg='white')
    smonth_lab= Label(covpg2_Frame1, text= 'Select Start Month:', font = ('Helvetica',10,'bold'), bg= '#36454F', fg='white')
    syear_lab = Label(covpg2_Frame1, text= 'Select Start Year:', font = ('Helvetica',10,'bold'), bg= '#36454F', fg='white')
    
    covpg2_Frame1_eday= OptionMenu(covpg2_Frame1, covcompendday, *covid_days)
    covpg2_Frame1_emonth= OptionMenu(covpg2_Frame1, covcompendmonth, *covid_months)
    covpg2_Frame1_eyear = OptionMenu(covpg2_Frame1, covcompendyear, *covid_years)
    covpg2_Frame1_area= OptionMenu(covpg2_Frame1, covcomparea1, *covid_locs)
    covpg2_Frame1_area2= OptionMenu(covpg2_Frame1, covcomparea2, *covid_locs)
    covpg2_Frame1_age= OptionMenu(covpg2_Frame1, covcompage1, *covid_age)
    covpg2_Frame1_age2= OptionMenu(covpg2_Frame1, covcompage2, *covid_age)
    covpg2_Frame1_areatype= OptionMenu(covpg2_Frame1, covcompareatype1, *covid_areatype)
    covpg2_Frame1_areatype2= OptionMenu(covpg2_Frame1, covcompareatype2, *covid_areatype)
    
    
    eday_lab= Label(covpg2_Frame1, text= 'Select End Day:', font = ('Helvetica',10,'bold'), bg= '#36454F', fg='white')
    emonth_lab= Label(covpg2_Frame1, text= 'Select End Month:', font = ('Helvetica',10,'bold'), bg= '#36454F', fg='white')
    eyear_lab = Label(covpg2_Frame1, text= 'Select End Year:', font = ('Helvetica',10,'bold'), bg= '#36454F', fg='white')    
    area_lab = Label(covpg2_Frame1, text= 'Select Area 1:', font = ('Helvetica',10,'bold'), bg= '#36454F', fg='white')
    areatype_lab = Label(covpg2_Frame1, text= 'Select Area Type 1:', font = ('Helvetica',10,'bold'), bg= '#36454F', fg='white')
    area_lab2 = Label(covpg2_Frame1, text= 'Select Area 2:', font = ('Helvetica',10,'bold'), bg= '#36454F', fg='white')
    areatype_lab2 = Label(covpg2_Frame1, text= 'Select Area Type 2:', font = ('Helvetica',10,'bold'), bg= '#36454F', fg='white')
    top_lab = Label(covpg2_Frame1, text= 'Select Plot type:',  font = ('Helvetica',10,'bold'), bg= '#36454F', fg='white')
    
    age_lab = Label(covpg2_Frame1, text= 'Select Age Range 1:', font = ('Helvetica',10,'bold'), bg= '#36454F', fg='white')
    age_lab2 = Label(covpg2_Frame1, text= 'Select Age Range 2:', font = ('Helvetica',10,'bold'), bg= '#36454F', fg='white')
    
    c_entry = Button(covpg2_Frame1, text='Clear Entries',command=lambda: covpg1_clr(covcompstartday, covcompstartmonth, covcompstartyear, 
                                                                             covcompendday, covcompendmonth, covcompendyear,covcomparea1, covcomparea2, 
                                                                             covcompage1, covcompage2, covcompareatype1, covcompareatype2, covcomptop),font = ('Helvetica',10,'bold'))
    bk = Button(covpg2_Frame1, text= '< Back',command=lambda:go_bk(Covpg2), font = ('Helvetica',10,'bold'))
    quit_butt = Button(covpg2_Frame1, text= 'QUIT', command= lambda: end_program(root), font = ('Helvetica',10,'bold'))
    
    comp_plot = Button(covpg2_Frame1, text= 'Plot Comparative Analysis', command= lambda: comp_analysis_func(plotparent=Covpg2,plotspace=covpg2_Frame2,
                                                                                                     startmonth =covcompstartmonth.get(),endmonth=covcompendmonth.get(),
                                                                                                     startyear=covcompstartyear.get(),endyear=covcompendyear.get(),
                                                                                                     startday=covcompstartday.get(),endday=covcompendday.get(),cage1=covcompage1.get(),
                                                                                                     cage2=covcompage2.get(),carea1=covcomparea1.get(),carea2=covcomparea2.get(),
                                                                                                     careatype1=covcompareatype1.get(),careatype2=covcompareatype2.get(),top=covcomptop.get()),font = ('Helvetica',10,'bold'),bg='#800000', fg='white')

    
    covpg2_Label.grid(row=0, column=0, columnspan=4, ipadx= 150, ipady=10, padx=10, pady=10)
    covpg2_Frame1.grid(row=1, column=0)
    covpg2_Frame2.grid(row=1, column=1, columnspan=3)
    
    covpg2_Frame1_sday.grid(row=0, column=1, ipadx=85, pady=10, padx=10, sticky=NE)
    covpg2_Frame1_smonth.grid(row=1, column=1, ipadx=85, pady=10, padx=10, sticky=NE)
    covpg2_Frame1_syear.grid(row=2, column=1, ipadx=85, pady=10, padx=10, sticky=NE)
    
    covpg2_Frame1_eday.grid(row=3, column=1, ipadx=85, pady=10, padx=10, sticky=NE)
    covpg2_Frame1_emonth.grid(row=4, column=1, ipadx=85, pady=10, padx=10, sticky=NE)
    covpg2_Frame1_eyear.grid(row=5, column=1, ipadx=85, pady=10, padx=10, sticky=NE)
    covpg2_Frame1_area.grid(row=6, column=1, ipadx=85, pady=10, padx=10, sticky=NE)
    covpg2_Frame1_area2.grid(row=7, column=1, ipadx=85, pady=10, padx=10, sticky=NE)
    covpg2_Frame1_areatype.grid(row=8, column=1, ipadx=85, pady=10, padx=10, sticky=NE)
    covpg2_Frame1_areatype2.grid(row=9, column=1, ipadx=85, pady=10, padx=10, sticky=NE)
    covpg2_Frame1_age.grid(row=10, column=1, ipadx=85, pady=10, padx=10, sticky=NE)
    covpg2_Frame1_age2.grid(row=11, column=1, ipadx=85, pady=10, padx=10, sticky=NE)
    covpg2_Frame1_top.grid(row=12, column=1, ipadx=65, padx=10, pady=10, sticky=NE)
    
    sday_lab.grid(row=0, column=0, ipadx=60, pady=10, padx=10, sticky=NW)
    smonth_lab.grid(row=1, column=0, ipadx=45, pady=10, padx=10, sticky=NW)
    syear_lab.grid(row=2, column=0, ipadx=55, pady=10, padx=10, sticky=NW)
    
    eday_lab.grid(row=3, column=0, ipadx=65, pady=10, padx=10, sticky=NW)
    emonth_lab.grid(row=4, column=0, ipadx=50, pady=10, padx=10, sticky=NW)
    eyear_lab.grid(row=5, column=0, ipadx=60, pady=10, padx=10, sticky=NW)
    area_lab.grid(row=6, column=0, ipadx=85, pady=10, padx=10, sticky=NW)
    area_lab2.grid(row=7, column=0, ipadx=85, pady=10, padx=10, sticky=NW)
    areatype_lab.grid(row=8, column=0, ipadx=60, pady=10, padx=10, sticky=NW)
    areatype_lab2.grid(row=9, column=0, ipadx=60, pady=10, padx=10, sticky=NW)
    age_lab.grid(row=10, column=0, ipadx=50, pady=10, padx=10, sticky=NW)
    age_lab2.grid(row=11, column=0, ipadx=50, pady=10, padx=10, sticky=NW)
    top_lab.grid(row=12, column=0, ipadx=60, padx=10, pady=10, sticky=NW)
    
    c_entry.grid(row=13, column=0, padx=10, pady=10, ipadx=40, ipady=5, sticky=NW)
    bk.grid(row=14, column=0, padx=10, pady=10, ipadx=60, ipady=5,sticky=NW)
    quit_butt.grid(row=14, column=1, padx=10, pady=10, ipadx=70, ipady=5,sticky=NW)


    comp_plot.grid(row=13, column=1, padx=10, pady=10, ipadx=50, ipady=5, sticky=NE)

def ccbydateregion():   
    
    """
    This function creates the page for compare by region and date
    """
    covstartday= StringVar()
    covstartmonth= StringVar()
    covstartyear= StringVar()
    covstartday.set(covid_days[0])
    covstartmonth.set(covid_months[0])
    covstartyear.set(covid_years[0])
    
    covendday= StringVar()
    covendmonth= StringVar()
    covendyear= StringVar()
    covage= StringVar()
    covendday.set(covid_days[0])
    covendmonth.set(covid_months[0])
    covendyear.set(covid_years[0])
    covage.set('Optional')
    
    covarea=StringVar()
    covarea.set(covid_locs[0])
    
    covareatype = StringVar()
    covareatype.set(covid_areatype[0])
    
    SSpage1 = Toplevel()
    sspage1_Label = Label(SSpage1, text='Covid19 Cases Analysis by Date & Region',bg='#AA4A44', fg='white', font = ('Helvetica',14,'bold'))
    sspage1_Frame1 = LabelFrame(SSpage1, padx=10, pady=10, bg= '#36454F')
    sspage2_Frame2= LabelFrame(SSpage1, padx=10, pady=10)
    sspage1_Frame1_sday= OptionMenu(sspage1_Frame1, covstartday, *covid_days)
    sspage1_Frame1_smonth= OptionMenu(sspage1_Frame1, covstartmonth, *covid_months)
    sspage1_Frame1_syear = OptionMenu(sspage1_Frame1, covstartyear, *covid_years)
    
    sday_lab= Label(sspage1_Frame1, text= 'Select Start Day:', font = ('Helvetica',10,'bold'), bg= '#36454F', fg='white')
    smonth_lab= Label(sspage1_Frame1, text= 'Select Start Month:', font = ('Helvetica',10,'bold'), bg= '#36454F', fg='white')
    syear_lab = Label(sspage1_Frame1, text= 'Select Start Year:', font = ('Helvetica',10,'bold'), bg= '#36454F', fg='white')
    
    sspage1_Frame1_eday= OptionMenu(sspage1_Frame1, covendday, *covid_days)
    sspage1_Frame1_emonth= OptionMenu(sspage1_Frame1, covendmonth, *covid_months)
    sspage1_Frame1_eyear = OptionMenu(sspage1_Frame1, covendyear, *covid_years)
    sspage1_Frame1_area= OptionMenu(sspage1_Frame1, covarea, *covid_locs)
    sspage1_Frame1_age= OptionMenu(sspage1_Frame1, covage, *covid_age)
    sspage1_Frame1_areatype= OptionMenu(sspage1_Frame1, covareatype, *covid_areatype)
    
    
    eday_lab= Label(sspage1_Frame1, text= 'Select End Day:', font = ('Helvetica',10,'bold'), bg= '#36454F', fg='white')
    emonth_lab= Label(sspage1_Frame1, text= 'Select End Month:', font = ('Helvetica',10,'bold'), bg= '#36454F', fg='white')
    eyear_lab = Label(sspage1_Frame1, text= 'Select End Year:', font = ('Helvetica',10,'bold'), bg= '#36454F', fg='white')    
    area_lab = Label(sspage1_Frame1, text= 'Select Area:', font = ('Helvetica',10,'bold'), bg= '#36454F', fg='white')
    areatype_lab = Label(sspage1_Frame1, text= 'Select Area Type:', font = ('Helvetica',10,'bold'), bg= '#36454F', fg='white')

    age_lab = Label(sspage1_Frame1, text= 'Select Age Range:', font = ('Helvetica',10,'bold'), bg= '#36454F', fg='white')
    
    c_entry = Button(sspage1_Frame1, text='Clear Entries',command=lambda: covpg1_clr(covstartday, covstartmonth, covstartyear, covendday, covendmonth, covendyear, covarea, covage, covareatype),font = ('Helvetica',10,'bold'))
    bk = Button(sspage1_Frame1, text= '< Back',command=lambda:go_bk(SSpage1), font = ('Helvetica',10,'bold'))
    quit_butt = Button(sspage1_Frame1, text= 'QUIT', command=lambda: end_program(root), font = ('Helvetica',10,'bold'))
    
    dc_plot = Button(sspage1_Frame1, text= 'Plot Daily Cummulative Cases', command= lambda: daily_cases_plot(plotparent = SSpage1, plotspace = sspage2_Frame2, startmonth = covstartmonth.get(), endmonth = covendmonth.get(),
                                                                                                             startyear=covstartyear.get(),endyear = covendyear.get(),startday = covstartday.get(),
                                                                                                             endday =covendday.get(),cage =covage.get() ,carea = covarea.get(),careatype=covareatype.get()), 
                     font = ('Helvetica',10,'bold'),bg='#800000', fg='white')
    pdc_plot = Button(sspage1_Frame1, text= 'Plot % Daily Cummulative Cases', command= lambda:percentage_daily_cases_plot(plotparent = SSpage1, plotspace = sspage2_Frame2, startmonth = covstartmonth.get(), endmonth = covendmonth.get(),
                                                                                                             startyear=covstartyear.get(),endyear = covendyear.get(),startday = covstartday.get(),
                                                                                                             endday =covendday.get(),cage =covage.get() ,carea = covarea.get(),careatype=covareatype.get()), font = ('Helvetica',10,'bold'),bg='#800000', fg='white')
   
    wc_plot = Button(sspage1_Frame1, text='Plot Weekly Cases', command= lambda: weekly_cases_plot(plotparent = SSpage1, plotspace = sspage2_Frame2, startmonth = covstartmonth.get(), endmonth = covendmonth.get(),
                                                                                                             startyear=covstartyear.get(),endyear = covendyear.get(),startday = covstartday.get(),
                                                                                                             endday =covendday.get(),cage =covage.get() ,carea = covarea.get(),careatype=covareatype.get()), font = ('Helvetica',10,'bold'),bg='#800000', fg='white')
    
    mc_plot = Button(sspage1_Frame1, text='Plot Monthly Cases For Entire Data', command= lambda: monthly_cases_plot(parentplot = SSpage1, plotspaces = sspage2_Frame2, 
                                                                                                                    age=covage.get(), covarea = covarea.get(), covareatype = covareatype.get())
                     , font = ('Helvetica',10,'bold'),bg='#800000', fg='white')
    
    
    sspage1_Label.grid(row=0, column=0, columnspan=4, ipadx= 150, ipady=10, padx=10, pady=10)
    sspage1_Frame1.grid(row=1, column=0)
    sspage2_Frame2.grid(row=1, column=1, columnspan=3)
    
    sspage1_Frame1_sday.grid(row=0, column=1, ipadx=85, pady=10, padx=10, sticky=NE)
    sspage1_Frame1_smonth.grid(row=1, column=1, ipadx=85, pady=10, padx=10, sticky=NE)
    sspage1_Frame1_syear.grid(row=2, column=1, ipadx=85, pady=10, padx=10, sticky=NE)
    
    sspage1_Frame1_eday.grid(row=3, column=1, ipadx=85, pady=10, padx=10, sticky=NE)
    sspage1_Frame1_emonth.grid(row=4, column=1, ipadx=85, pady=10, padx=10, sticky=NE)
    sspage1_Frame1_eyear.grid(row=5, column=1, ipadx=85, pady=10, padx=10, sticky=NE)
    sspage1_Frame1_area.grid(row=6, column=1, ipadx=85, pady=10, padx=10, sticky=NE)
    sspage1_Frame1_areatype.grid(row=7, column=1, ipadx=85, pady=10, padx=10, sticky=NE)
    sspage1_Frame1_age.grid(row=8, column=1, ipadx=85, pady=10, padx=10, sticky=NE)
    
    sday_lab.grid(row=0, column=0, ipadx=60, pady=10, padx=10, sticky=NW)
    smonth_lab.grid(row=1, column=0, ipadx=45, pady=10, padx=10, sticky=NW)
    syear_lab.grid(row=2, column=0, ipadx=55, pady=10, padx=10, sticky=NW)
    
    eday_lab.grid(row=3, column=0, ipadx=65, pady=10, padx=10, sticky=NW)
    emonth_lab.grid(row=4, column=0, ipadx=50, pady=10, padx=10, sticky=NW)
    eyear_lab.grid(row=5, column=0, ipadx=60, pady=10, padx=10, sticky=NW)
    area_lab.grid(row=6, column=0, ipadx=85, pady=10, padx=10, sticky=NW)
    areatype_lab.grid(row=7, column=0, ipadx=60, pady=10, padx=10, sticky=NW)
    age_lab.grid(row=8, column=0, ipadx=50, pady=10, padx=10, sticky=NW)
    
    
    c_entry.grid(row=9, column=0, padx=10, pady=10, ipadx=40, ipady=5, sticky=NW)
    bk.grid(row=10, column=0, padx=10, pady=10, ipadx=60, ipady=5,sticky=NW)
    quit_butt.grid(row=11, column=0, padx=10, pady=10, ipadx=65, ipady=5,sticky=NW)


    dc_plot.grid(row=9, column=1, padx=10, pady=10, ipadx=50, ipady=5, sticky=NE)
    pdc_plot.grid(row=10, column=1, padx=10, pady=10, ipadx=43, ipady=5, sticky=NE)
    wc_plot.grid(row=11, column=1, padx=10, pady=10, ipadx=87, ipady=5, sticky=NE)
    mc_plot.grid(row=12, column=0, columnspan=3, padx=10, pady=10, ipadx=60, ipady=5)    
    
    return(SSpage1,sspage1_Frame1,sspage2_Frame2,sspage1_Frame1_eday,sspage1_Frame1_emonth,sspage1_Frame1_eyear,dc_plot)

def qa_covid():
    
    qa_covstartday= StringVar()
    qa_covstartmonth= StringVar()
    qa_covstartyear= StringVar()
    qa_covstartday.set(covid_days[0])
    qa_covstartmonth.set(covid_months[0])
    qa_covstartyear.set(covid_years[0])
    
    qa_covendday= StringVar()
    qa_covendmonth= StringVar()
    qa_covendyear= StringVar()
    qa_covendday.set(covid_days[0])
    qa_covendmonth.set(covid_months[0])
    qa_covendyear.set(covid_years[0])
    qa_covquest = StringVar()
    qa_covquest.set('Area With Highest No. Cases')

    
    CCqa = Toplevel()
    qapage1_Label = Label(CCqa, text='Covid19 Q&A',bg='#AA4A44', fg='white', font = ('Helvetica',14,'bold'))
    qapage1_Frame1 = LabelFrame(CCqa, padx=10, pady=10, bg= '#36454F')
    qapage2_Frame2= LabelFrame(CCqa, padx=10, pady=10)
    qapage1_Frame1_sday= OptionMenu(qapage1_Frame1, qa_covstartday, *covid_days)
    qapage1_Frame1_smonth= OptionMenu(qapage1_Frame1, qa_covstartmonth, *covid_months)
    qapage1_Frame1_syear = OptionMenu(qapage1_Frame1, qa_covstartyear, *covid_years)
    qapage1_Frame1_quest = OptionMenu(qapage1_Frame1, qa_covquest, 'Area With Highest No. Cases', 'Area With Highest No. Cases(7day period)','Area With Positive Largest Change of Cases', 'Area With Positive Largest Change of Cases (7day period)', 'All Cases in UK')
    
    sday_lab= Label(qapage1_Frame1, text= 'Select Start Day:', font = ('Helvetica',10,'bold'), bg= '#36454F', fg='white')
    smonth_lab= Label(qapage1_Frame1, text= 'Select Start Month:', font = ('Helvetica',10,'bold'), bg= '#36454F', fg='white')
    syear_lab = Label(qapage1_Frame1, text= 'Select Start Year:', font = ('Helvetica',10,'bold'), bg= '#36454F', fg='white')
    
    qapage1_Frame1_eday= OptionMenu(qapage1_Frame1, qa_covendday, *covid_days)
    qapage1_Frame1_emonth= OptionMenu(qapage1_Frame1, qa_covendmonth, *covid_months)
    qapage1_Frame1_eyear = OptionMenu(qapage1_Frame1, qa_covendyear, *covid_years)
    
    eday_lab= Label(qapage1_Frame1, text= 'Select End Day:', font = ('Helvetica',10,'bold'), bg= '#36454F', fg='white')
    emonth_lab= Label(qapage1_Frame1, text= 'Select End Month:', font = ('Helvetica',10,'bold'), bg= '#36454F', fg='white')
    eyear_lab = Label(qapage1_Frame1, text= 'Select End Year:', font = ('Helvetica',10,'bold'), bg= '#36454F', fg='white')    
    quest_lab = Label(qapage1_Frame1, text= 'Select Question:', font = ('Helvetica',10,'bold'), bg= '#36454F', fg='white')    

    bk = Button(qapage1_Frame1, text= '< Back',command=lambda:go_bk(CCqa), font = ('Helvetica',10,'bold'))
    quit_butt = Button(qapage1_Frame1, text= 'QUIT', command=lambda: end_program(root), font = ('Helvetica',10,'bold'))
    
    dc_plot = Button(qapage1_Frame1, text= 'Answer', command= lambda: qa_cov_func(plotparent=CCqa,plotspace=qapage2_Frame2,
                                                                          startday=qa_covstartday.get(),startmonth=qa_covstartmonth.get(),
                                                                          startyear=qa_covstartyear.get(),endday=qa_covendday.get(),
                                                                          endmonth=qa_covendmonth.get(),endyear=qa_covendyear.get(),
                                                                          quest=qa_covquest.get()), font = ('Helvetica',10,'bold'),bg='#800000', fg='white')
    
    
    
    qapage1_Label.grid(row=0, column=0, columnspan=3, ipadx= 150, ipady=10, padx=10, pady=10)
    qapage1_Frame1.grid(row=1, column=0)
    qapage2_Frame2.grid(row=1, column=1, columnspan=1)
    
    qapage1_Frame1_sday.grid(row=0, column=1, ipadx=85, pady=10, padx=10, sticky=NE)
    qapage1_Frame1_smonth.grid(row=1, column=1, ipadx=85, pady=10, padx=10, sticky=NE)
    qapage1_Frame1_syear.grid(row=2, column=1, ipadx=85, pady=10, padx=10, sticky=NE)
    qapage1_Frame1_quest.grid(row=6, column=1, ipadx=85, pady=10, padx=10, sticky=NE)
    
    qapage1_Frame1_eday.grid(row=3, column=1, ipadx=85, pady=10, padx=10, sticky=NE)
    qapage1_Frame1_emonth.grid(row=4, column=1, ipadx=85, pady=10, padx=10, sticky=NE)
    qapage1_Frame1_eyear.grid(row=5, column=1, ipadx=85, pady=10, padx=10, sticky=NE)
 
    
    sday_lab.grid(row=0, column=0, ipadx=60, pady=10, padx=10, sticky=NW)
    smonth_lab.grid(row=1, column=0, ipadx=45, pady=10, padx=10, sticky=NW)
    syear_lab.grid(row=2, column=0, ipadx=55, pady=10, padx=10, sticky=NW)
    
    eday_lab.grid(row=3, column=0, ipadx=65, pady=10, padx=10, sticky=NW)
    emonth_lab.grid(row=4, column=0, ipadx=50, pady=10, padx=10, sticky=NW)
    eyear_lab.grid(row=5, column=0, ipadx=60, pady=10, padx=10, sticky=NW)
    quest_lab.grid(row=6, column=0, ipadx=60, pady=10, padx=10, sticky=NW)

    
    quit_butt.grid(row=8, column=1, padx=10, pady=10, ipadx=60, ipady=5, sticky=NE)
    bk.grid(row=8, column=0, padx=10, pady=10, ipadx=40, ipady=5,sticky=NW)


    dc_plot.grid(row=7, column=0, columnspan=2, padx=10, pady=10, ipadx=120, ipady=5)
