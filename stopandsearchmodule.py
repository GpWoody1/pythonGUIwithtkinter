
from tkinter import *
import os
import requests
import json
import pandas as pd
import numpy as np
import datetime 
from datetime import timedelta
from datetime import datetime
from dateutil.relativedelta import relativedelta
from calendar import month_name
from commonfunctionmodule import *


##----------------------------------------------------------------------------------------------
## STOP & SEARCH DATA PREPROCESSING
##----------------------------------------------------------------------------------------------

police_request = requests.get('https://data.police.uk/api/forces')

police_id = json.loads(police_request.content)

force_name = [pol['name'] for pol in police_id]

end = datetime.now()
start = end-relativedelta(years=3)
stopsearchdates_year=[]
stopsearchdates_month =[]
while start<end:
    stopsearchdates_year.append(start.strftime('%Y'))
    stopsearchdates_month.append(start.strftime('%B'))
    start += relativedelta(months=+1)
    

stopsearchdates_year = list(dict.fromkeys(stopsearchdates_year))
stopsearchdates_month= list(dict.fromkeys(stopsearchdates_month))
stopsearchdates_month = sorted(stopsearchdates_month, key= list(month_name).index )
pol_plot_type = ['Object of Search', 'Age Range of Suspects', 'Type of Search', 'Gender of Suspects',\
                 'Ethnicity of Suspects', 'Clothing Removal','Outcome', 'Total Number of Arrests']

#---------------------------------------------------------------------------------------------------------------------
##Define Stop and Search functions
#---------------------------------------------------------------------------------------------------------------------

def pol_oos(plotparent,plotspace,startyear,endyear,startmonth,endmonth,force,top):
    try:
        emptyplotspace(plotspace)
        for kfc in police_id:
            if  force == kfc['name']:
                selected_force_id = kfc['id']
        month = datetime.strptime(startmonth, '%B')
        endmonth = datetime.strptime(endmonth, '%B')
        get_date = startyear+'-'+ month.strftime('%m')
        get_enddate = endyear+'-'+ endmonth.strftime('%m')
        get_date_pd = pd.Period(get_date, 'M')
        get_enddate_pd = pd.Period(get_enddate, 'M')
        
        police_data_df =pd.DataFrame()
        
        while get_date_pd <= get_enddate_pd:
            
            police_data_request = requests.get('https://data.police.uk/api/stops-force?force=' + selected_force_id+'&date='+str(get_date_pd))
            police_data = json.loads(police_data_request.content)
            police_data_df = police_data_df.append(pd.DataFrame(police_data))
            get_date_pd = get_date_pd+1
            
        police_data_df.reset_index(drop=True, inplace=True)    
        
        outcome_stuff = [item['name'] for item in police_data_df['outcome_object']]
        police_data_df['outcome_object'] = outcome_stuff
            
        needed_police_data = police_data_df[['datetime','age_range','gender','officer_defined_ethnicity','type','removal_of_more_than_outer_clothing','object_of_search', 'outcome_object']]
        needed_police_data=needed_police_data.fillna('Unavailable')
        needed_police_data.columns = ['Date', 'Age Range of Suspects','Gender of Suspects', 'Ethnicity of Suspects', 'Type of Search', 'Clothing Removal','Object of Search', 'Outcome']
        needed_police_data['Date'] = pd.to_datetime(needed_police_data['Date']).dt.tz_localize(None)
        
    
        if 'Unavailable' in needed_police_data['Date']:
            needed_police_data.drop(needed_police_data[needed_police_data['Date']=='Unavailable'].index, inplace=True, axis=0)
        needed_police_data['Date'] = pd.to_datetime(needed_police_data['Date']).dt.tz_localize(None)
        
        list_of_pol_plots = ['Object of Search','Age Range of Suspects','Gender of Suspects','Ethnicity of Suspects', 
                             'Type of Search','Clothing Removal', 'Outcome']
        
        if top == 'Total Number of Arrests':
            plotly, fig = plot_me([111],plotspace)
            needed_police_data['Date'].dt.date.value_counts().plot(kind='line', ax=plotly[0])
            avg_by_arst = needed_police_data['Date'].dt.date.value_counts().mean()
            plotly[0].set(title= 'Total Number of Arrests by Date')
            plotly[0].axhline(y=avg_by_arst, color='r', label='AVG Arrests', linestyle='--', linewidth=1, dash_capstyle='round', fillstyle='left')
            plotly[0].legend(loc=0,fontsize='medium')
            set_label_stuff(plotly[0], 'Number of Arrests', 'Date')
            plotly[0].tick_params(axis ='x',rotation=60, labelsize=8)
            plotly[0].tick_params(axis ='y', labelsize=8)
            fig.suptitle('Analysis of '+force+' between '+ get_date+ ' to '+get_enddate, fontsize=10, fontweight='bold')
        
        else:
            for vals in list_of_pol_plots:
                if top == vals:
                    plotly, fig = plot_me([111],plotspace)
                    needed_police_data[vals].value_counts().plot(kind='barh', ax=plotly[0])
                    avg_by_obj = needed_police_data[vals].value_counts().mean()
                    plotly[0].set(title= 'Arrests by '+vals)
                    plotly[0].axvline(x=avg_by_obj, color='r', label='AVG Arrests', linestyle='--', linewidth=1, dash_capstyle='round', fillstyle='left')
                    plotly[0].legend(loc=0, fontsize='medium')
                    plotly[0].tick_params(axis='y', labelsize=8)
                    plotly[0].tick_params(axis='x', labelsize=8)
                    set_label_stuff(plotly[0],vals, 'No. of Arrests')
                    fig.suptitle('Analysis of '+force+' between '+ get_date+ ' to '+get_enddate, fontsize=10, fontweight='bold')           
            

    except (ValueError, KeyError, TypeError):
        key_error_flag = messagebox.askquestion('Error Occured', 'Oops, this data does not seem to be available, please check your entry and try again. Would you like to try another force?')
        if key_error_flag =='yes':
            emptyplotspace(plotspace)
    except json.decoder.JSONDecodeError:
        json_error = messagebox.askquestion('Error Occured', 'Oops, looks like this data has not been uploaded by "data.police.uk" yet. Would you like to select another item to process?')
        if json_error == 'no':
            go_bk(plotparent)
                
    return(police_data_request, plotly)


            
def pol_companalfunc(plotparent,plotspace,startyear,endyear,startmonth,endmonth,force1,force2,top):
    try:
        emptyplotspace(plotspace)
        for kfc in police_id:
            if  force1 == kfc['name']:
                selected_force1_id = kfc['id']
            if force2 == kfc['name']:
                selected_force2_id = kfc['id']
        month = datetime.strptime(startmonth, '%B')
        endmonth = datetime.strptime(endmonth, '%B')
        get_date = startyear+'-'+ month.strftime('%m')
        get_enddate = endyear+'-'+ endmonth.strftime('%m')
        get_date_pd = pd.Period(get_date, 'M')
        get_enddate_pd = pd.Period(get_enddate, 'M')
        
        police_data_df1 =pd.DataFrame()
        police_data_df2 = pd.DataFrame()
        
        while get_date_pd <= get_enddate_pd:
            
            police_data_request1 = requests.get('https://data.police.uk/api/stops-force?force=' + selected_force1_id+'&date='+str(get_date_pd))
            police_data1 = json.loads(police_data_request1.content)
            police_data_df1 = police_data_df1.append(pd.DataFrame(police_data1))
            
            
            police_data_request2 = requests.get('https://data.police.uk/api/stops-force?force=' + selected_force2_id+'&date='+str(get_date_pd))
            police_data2 = json.loads(police_data_request2.content)
            police_data_df2 = police_data_df2.append(pd.DataFrame(police_data2))
            
            get_date_pd = get_date_pd+1
            
        police_data_df1.reset_index(drop=True, inplace=True)    
        police_data_df2.reset_index(drop=True, inplace=True)    
        
        outcome_stuff1 = [item['name'] for item in police_data_df1['outcome_object']]
        outcome_stuff2 = [item['name'] for item in police_data_df2['outcome_object']]
        police_data_df1['outcome_object'] = outcome_stuff1
        police_data_df2['outcome_object'] = outcome_stuff2
            
        needed_police_data1 = police_data_df1[['datetime','age_range','gender','officer_defined_ethnicity','type','removal_of_more_than_outer_clothing','object_of_search', 'outcome_object']]
        needed_police_data2 = police_data_df2[['datetime','age_range','gender','officer_defined_ethnicity','type','removal_of_more_than_outer_clothing','object_of_search', 'outcome_object']]
        
        needed_police_data1 = needed_police_data1.fillna('Unavailable')
        needed_police_data2 = needed_police_data2.fillna('Unavailable')
        
        
        if 'Unavailable' in needed_police_data1['datetime']:
            needed_police_data1.drop(needed_police_data1[needed_police_data1['datetime']=='Unavailable'].index, inplace=True, axis=0)
        if 'Unavailable' in needed_police_data2['datetime']:
            needed_police_data2.drop(needed_police_data2[needed_police_data2['datetime']=='Unavailable'].index, inplace=True, axis=0)
        
        
        needed_police_data1.columns = ['Date', 'Age Range of Suspects','Gender of Suspects', 'Ethnicity of Suspects', 'Type of Search', 'Clothing Removal','Object of Search', 'Outcome']
        needed_police_data1['Date'] = pd.to_datetime(needed_police_data1['Date']).dt.tz_localize(None)
        needed_police_data2.columns = ['Date', 'Age Range of Suspects','Gender of Suspects', 'Ethnicity of Suspects', 'Type of Search', 'Clothing Removal','Object of Search', 'Outcome']
        needed_police_data2['Date'] = pd.to_datetime(needed_police_data2['Date']).dt.tz_localize(None)
        
        list_of_pol_plots = ['Object of Search','Age Range of Suspects','Gender of Suspects','Ethnicity of Suspects', 
                             'Type of Search','Clothing Removal', 'Outcome']
        
       
        if top == 'Total Number of Arrests':
            plotly,fig = plot_me([111],plotspace)
            np1 = needed_police_data1['Date'].dt.date.value_counts()
            np2 = needed_police_data2['Date'].dt.date.value_counts()

            np1.plot(kind='line', ax=plotly[0], label = force1)
            np2.plot(kind='line', ax=plotly[0], label = force2)
            
            avg1 = np1.mean()
            avg2 = np2.mean()
            plotly[0].axhline(y=avg1, color='red', label='AVG Arrests ' +force1, linestyle='--', linewidth=1, dash_capstyle='round', fillstyle='left')
            plotly[0].axhline(y=avg2, color='#AA4A44', label='AVG Arrests '+force2, linestyle='--', linewidth=1, dash_capstyle='round', fillstyle='left')
            
            
            plotly[0].set(title= 'Cummulative of Arrests by Date')
            plotly[0].legend(loc=0, fontsize='medium')
            set_label_stuff(plotly[0], 'Cummulative Arrests', 'Date')
            plotly[0].tick_params(axis ='x',rotation=60, labelsize=8)
            plotly[0].tick_params(axis ='y', labelsize=8)
            fig.suptitle('Comparative Analysis between '+force1+' & '+force2+'('+ get_date+ ' - '+get_enddate+')',  fontsize=8, fontweight='bold')
 
        else: 
            
            for vals in list_of_pol_plots:
                if top == vals:
                    plotly,fig = plot_me([111],plotspace)
                
                    columns_stuff = list(needed_police_data1[vals].append(needed_police_data2[vals]).drop_duplicates())
                    needed1 = needed_police_data1[vals].value_counts()
                    needed2 = needed_police_data2[vals].value_counts()
                
                    avg1 = needed_police_data1[vals].value_counts().mean()
                    avg2 = needed_police_data2[vals].value_counts().mean()
                
                    needed1_list = []
                    needed2_list =[]
                    for items in columns_stuff:
                        if items in needed1:
                            needed1_list.append(needed1[items])
                        else:
                            needed1_list.append(0)
                        if items in needed2:
                            needed2_list.append(needed2[items])
                        else:
                            needed2_list.append(0)
                        
                    x = np.arange(len(columns_stuff))
                    width =0.35
                    rect1 = plotly[0].barh(x-width/2, needed1_list, 0.35, label = force1)
                    rect2 = plotly[0].barh(x+width/2, needed2_list, 0.35, label = force2)
                
                    plotly[0].axvline(x=avg1, color='red', label='AVG Arrests ' +force1, linestyle='--', linewidth=1, dash_capstyle='round', fillstyle='left')
                    plotly[0].axvline(x=avg2, color='#AA4A44', label='AVG Arrests '+force2, linestyle='--', linewidth=1, dash_capstyle='round', fillstyle='left')
                
                    plotly[0].set_yticks(x)
                    plotly[0].set_yticklabels(columns_stuff)
                    plotly[0].set(title= 'Arrests by '+vals)
                    plotly[0].tick_params(axis ='x', labelsize=8)
                    plotly[0].tick_params(axis ='y', labelsize=8)
                    plotly[0].legend(loc=0)
                    set_label_stuff(plotly[0],vals,'No. of Arrests')
                    fig.suptitle('Comparative Analysis between '+force1+' & '+force2+'('+ get_date+ ' - '+get_enddate+')',  fontsize=10, fontweight='bold')
                      
            
    except (ValueError, KeyError, TypeError):
        key_error_flag = messagebox.askquestion('Error Occured', 'Oops, this data does not seem to be available, please check your entry and try again. Would you like to try another force?')
        if key_error_flag =='yes':
            emptyplotspace(plotspace)
    except json.decoder.JSONDecodeError:
        json_error = messagebox.askquestion('Error Occured', 'Oops, looks like this data has not been uploaded by "data.police.uk" yet. Would you like to select another item to process?')
        if json_error == 'no':
            go_bk(plotparent)                

    return(police_data_request1, police_data_request2, plotly)

def pol_companal():
    
    polpg1compyear = StringVar()
    polpg1compmonth = StringVar()
    polpg1compendmonth = StringVar()    
    polpg1compendyear = StringVar()
    polpg1compforce1 = StringVar()
    polpg1compforce2 = StringVar()
    polpg1compplot = StringVar()
    
    Polpg1comp = Toplevel()
    polpg1_compFrame1 = LabelFrame(Polpg1comp, padx=10, pady=10, bg= '#36454F')
    polpg1_compFrame2 = LabelFrame(Polpg1comp, padx=10, pady=10)
    
    
    polpg1_compFrame1_year = OptionMenu(polpg1_compFrame1, polpg1compyear, *stopsearchdates_year)
    polpg1_compFrame1_month = OptionMenu(polpg1_compFrame1, polpg1compmonth, *stopsearchdates_month)
    polpg1_compFrame1_endyear = OptionMenu(polpg1_compFrame1, polpg1compendyear, *stopsearchdates_year)
    polpg1_compFrame1_endmonth = OptionMenu(polpg1_compFrame1, polpg1compendmonth, *stopsearchdates_month)
    polpg1_compFrame1_force1 = OptionMenu(polpg1_compFrame1, polpg1compforce1, *force_name)
    polpg1_compFrame1_force2 = OptionMenu(polpg1_compFrame1, polpg1compforce2, *force_name)
    polpg1_compFrame1_plot = OptionMenu(polpg1_compFrame1, polpg1compplot, *pol_plot_type)
    
    year_lab = Label(polpg1_compFrame1, text='Select Start Year:', font=('Helvetica',10,'bold'), bg= '#36454F', fg='white')
    month_lab = Label(polpg1_compFrame1, text='Select Start Month:', font=('Helvetica',10,'bold'), bg= '#36454F', fg='white')
    endyear_lab = Label(polpg1_compFrame1, text='Select End Year:', font=('Helvetica',10,'bold'), bg= '#36454F', fg='white')
    endmonth_lab = Label(polpg1_compFrame1, text='Select End Month:', font=('Helvetica',10,'bold'), bg= '#36454F', fg='white')
    force_lab1 = Label(polpg1_compFrame1, text='Select Force 1:', font=('Helvetica',10,'bold'), bg= '#36454F', fg='white')
    force_lab2 = Label(polpg1_compFrame1, text='Select Force 2:', font=('Helvetica',10,'bold'), bg= '#36454F', fg='white')
    plot_lab = Label(polpg1_compFrame1, text='Select Plot to Make:', font=('Helvetica',10,'bold'), bg= '#36454F', fg='white')
    

    polpg1_Button_ap = Button(polpg1_compFrame1, text = 'PLOT', command= lambda: pol_companalfunc(plotparent=Polpg1comp,plotspace=polpg1_compFrame2,
                                                                                                  startyear=polpg1compyear.get(),endyear=polpg1compendyear.get(),
                                                                                                  startmonth=polpg1compmonth.get(),endmonth=polpg1compendmonth.get(),
                                                                                                  force1=polpg1compforce1.get(),force2=polpg1compforce2.get(),top=polpg1compplot.get()), font = ('Helvetica',10,'bold'),bg='#800000', fg='white')
    
    bk_button = Button(polpg1_compFrame1, text = '< Back', command= lambda:go_bk(Polpg1comp), font = ('Helvetica',10,'bold'))
    quit_stuff = Button(polpg1_compFrame1, text = 'Quit', command= lambda: end_program(root), font = ('Helvetica',10,'bold'))
    
    polpg1_compFrame1.grid(row=1, column=0)
    polpg1_compFrame2.grid(row=1, column=1)
    
    polpg1_compFrame1_year.grid(row=1,column=1, ipadx=85, pady=10, padx=10, sticky=NE)
    polpg1_compFrame1_month.grid(row=0,column=1, ipadx=85, pady=10, padx=10, sticky=NE)
    polpg1_compFrame1_endyear.grid(row=3,column=1, ipadx=85, pady=10, padx=10, sticky=NE)
    polpg1_compFrame1_endmonth.grid(row=2,column=1, ipadx=85, pady=10, padx=10, sticky=NE)
    polpg1_compFrame1_force1.grid(row=4,column=1, ipadx=85, pady=10, padx=10, sticky=NE)
    polpg1_compFrame1_force2.grid(row=5,column=1, ipadx=85, pady=10, padx=10, sticky=NE)
    polpg1_compFrame1_plot.grid(row=6,column=1, ipadx=85, pady=10, padx=10, sticky=NE)
    
    year_lab.grid(row=1, column=0, ipadx=25, pady=10, padx=10, sticky=NW)
    month_lab.grid(row=0, column=0, ipadx=25, pady=10, padx=10, sticky=NW)
    endyear_lab.grid(row=3, column=0, ipadx=35, pady=10, padx=10, sticky=NW)
    endmonth_lab.grid(row=2, column=0, ipadx=35, pady=10, padx=10, sticky=NW)
    force_lab1.grid(row=4, column=0, ipadx=55, pady=10, padx=10, sticky=NW)
    force_lab2.grid(row=5, column=0, ipadx=55, pady=10, padx=10, sticky=NW)
    plot_lab.grid(row=6, column=0, ipadx=25, pady=10, padx=10, sticky=NW)
    
    polpg1_Button_ap.grid(row=7, column=0, columnspan =2, ipadx=120, ipady=5, padx=10,pady=10)
    bk_button.grid(row=8, column=0, ipadx=50, ipady=5, padx=10,pady=10)
    quit_stuff.grid(row=8, column=1,ipadx=60, ipady=5, padx=10,pady=10 )
    



def qa_ss_func(plotparent,plotspace,startyear,endyear,startmonth,endmonth,force,quest):
    emptyplotspace(plotspace)
    try:
        for kfc in police_id:
            if  force == kfc['name']:
                selected_force_id = kfc['id']
        month = datetime.strptime(startmonth, '%B')
        endmonth = datetime.strptime(endmonth, '%B')
        get_date = startyear+'-'+ month.strftime('%m')
        get_enddate = endyear+'-'+ endmonth.strftime('%m')
        get_date_pd = pd.Period(get_date, 'M')
        get_enddate_pd = pd.Period(get_enddate, 'M')
        
        police_data_df =pd.DataFrame()
        
        while get_date_pd <= get_enddate_pd:
            
            police_data_request = requests.get('https://data.police.uk/api/stops-force?force=' + selected_force_id+'&date='+str(get_date_pd))
            police_data = json.loads(police_data_request.content)
            police_data_df = police_data_df.append(pd.DataFrame(police_data))
            get_date_pd = get_date_pd+1
            
        police_data_df.reset_index(drop=True, inplace=True)    
        
        outcome_stuff = [item['name'] for item in police_data_df['outcome_object']]
        police_data_df['outcome_object'] = outcome_stuff
            
        needed_police_data = police_data_df[['datetime','age_range','gender','officer_defined_ethnicity','type','removal_of_more_than_outer_clothing','object_of_search', 'outcome_object']]
        needed_police_data=needed_police_data.fillna('Unavailable')
        needed_police_data.columns = ['Date', 'Age Range of Suspects','Gender of Suspects', 'Ethnicity of Suspects', 'Type of Search', 'Clothing Removal','Object of Search', 'Outcome']
        needed_police_data['Date'] = pd.to_datetime(needed_police_data['Date']).dt.tz_localize(None) 
        
        if quest == 'Total Arrests Made':
            ans = Label(plotspace, text= 'The total arrest made by '+ force+' between \n'+get_date+ ' & '+ get_enddate+ ' is \n'+ str(needed_police_data.shape[0]),font = ('Helvetica',14,'bold'), bg= '#36454F', fg='white')
            ans.pack(expand=True)
        
        
        
        elif quest =='Most Reason for Stop and Search':
            dataset_ans = needed_police_data['Object of Search'].value_counts()[needed_police_data['Object of Search'].value_counts()==needed_police_data['Object of Search'].value_counts().max()]
            ans = Label(plotspace, text= 'The Most reason for Stop & Search by '+ force +' between \n'+get_date+ ' & '+ get_enddate+ ' is \n'+ str(dataset_ans.index[0])+'\n With a total search of '+ str(dataset_ans[0]),font = ('Helvetica',14,'bold'), bg= '#36454F', fg='white')
            ans.pack(expand=True)
        
        
        
        
        
        elif quest =='No. of Vehicle Searches':
            easter_egg = needed_police_data[(needed_police_data['Type of Search']=='Vehicle search')|(needed_police_data['Type of Search'] == 'Person and Vehicle search')]
            dataset_ans = easter_egg['Type of Search'].value_counts()[easter_egg['Type of Search'].value_counts()==easter_egg['Type of Search'].value_counts().max()]
            if dataset_ans.empty==True:
                ans = Label(plotspace, text= 'They were No Vehicle stop & search during this period',font = ('Helvetica',14,'bold'), bg= '#36454F', fg='white')
            else:
                ans = Label(plotspace, text= 'The No. of Vehicle Stop & Search by '+ force+' between \n'+get_date+ ' & '+ get_enddate+ ' is \n'+ str(dataset_ans[0]),font = ('Helvetica',14,'bold'), bg= '#36454F', fg='white')
            ans.pack(expand=True)

        
        
        
        elif quest =='No. of Personal Searches':
            easter_egg = needed_police_data[(needed_police_data['Type of Search']=='Person search')|(needed_police_data['Type of Search'] == 'Person and Vehicle search')]
            dataset_ans = easter_egg['Type of Search'].value_counts()[easter_egg['Type of Search'].value_counts()==easter_egg['Type of Search'].value_counts().max()]
            if dataset_ans.empty==True:
                ans = Label(plotspace, text= 'They were No Person stop & search during this period',font = ('Helvetica',14,'bold'), bg= '#36454F', fg='white')
            else:
                ans = Label(plotspace, text= 'The No. of Person Stop & Search by '+ force +' between \n'+get_date+ ' & '+ get_enddate+ ' is \n'+ str(dataset_ans[0]),font = ('Helvetica',14,'bold'), bg= '#36454F', fg='white')
            ans.pack(expand=True)
        
        
        
        
        elif quest =='Race Most Searched':
            dataset_ans = needed_police_data['Ethnicity of Suspects'].value_counts()[needed_police_data['Ethnicity of Suspects'].value_counts()==needed_police_data['Ethnicity of Suspects'].value_counts().max()]
            ans = Label(plotspace, text= 'The Most race for Stoped & Searched by '+ force +' between \n'+get_date+ ' & '+ get_enddate+ ' is \n'+ str(dataset_ans.index[0])+'\n With a total search of '+ str(dataset_ans[0]),font = ('Helvetica',14,'bold'), bg= '#36454F', fg='white')
            ans.pack(expand=True)

    
    
    except (ValueError, KeyError, TypeError):
        key_error_flag = messagebox.askquestion('Error Occured', 'Oops, this data does not seem to be available, please check your entry and try again. Would you like to try another force?')
        if key_error_flag =='yes':
            emptyplotspace(plotspace)
    except json.decoder.JSONDecodeError:
        json_error = messagebox.askquestion('Error Occured', 'Oops, looks like this data has not been uploaded by "data.police.uk" yet. Would you like to select another item to process?')
        if json_error == 'no':
            go_bk(plotparent)

    return(police_data_request, dataset_ans)

def qa_ss():
    
    qa_ssstartday= StringVar()
    qa_ssstartmonth= StringVar()
    qa_ssstartyear= StringVar()
    
    qa_ssendday= StringVar()
    qa_ssendmonth= StringVar()
    qa_ssendyear= StringVar()
    qa_force= StringVar()
    qa_ssquest = StringVar()


    
    SSqa = Toplevel()
    qapage1_Label = Label(SSqa, text='Stop & Search Q&A',bg='#AA4A44', fg='white', font = ('Helvetica',14,'bold'))
    qa_sspage1_Frame1 = LabelFrame(SSqa, padx=10, pady=10, bg= '#36454F')
    qa_sspage2_Frame2= LabelFrame(SSqa, padx=10, pady=10)
    qapage1_Frame1_smonth= OptionMenu(qa_sspage1_Frame1, qa_ssstartmonth, *stopsearchdates_month)
    qapage1_Frame1_syear = OptionMenu(qa_sspage1_Frame1, qa_ssstartyear, *stopsearchdates_year)
    qapage1_Frame1_force = OptionMenu(qa_sspage1_Frame1, qa_force, *force_name)
    qapage1_Frame1_quest = OptionMenu(qa_sspage1_Frame1, qa_ssquest, 'Total Arrests Made', 'Most Reason for Stop and Search', 'No. of Vehicle Searches', 'No. of Personal Searches', 'Race Most Searched')
    
    qapage1_Frame1_emonth= OptionMenu(qa_sspage1_Frame1, qa_ssendmonth, *stopsearchdates_month)
    qapage1_Frame1_eyear = OptionMenu(qa_sspage1_Frame1, qa_ssendyear, *stopsearchdates_year)
    
    smonth_lab= Label(qa_sspage1_Frame1, text= 'Select Start Month:', font = ('Helvetica',10,'bold'), bg= '#36454F', fg='white')
    syear_lab = Label(qa_sspage1_Frame1, text= 'Select Start Year:', font = ('Helvetica',10,'bold'), bg= '#36454F', fg='white')
    
    
    emonth_lab= Label(qa_sspage1_Frame1, text= 'Select End Month:', font = ('Helvetica',10,'bold'), bg= '#36454F', fg='white')
    eyear_lab = Label(qa_sspage1_Frame1, text= 'Select End Year:', font = ('Helvetica',10,'bold'), bg= '#36454F', fg='white')    
    quest_lab = Label(qa_sspage1_Frame1, text= 'Select Question:', font = ('Helvetica',10,'bold'), bg= '#36454F', fg='white')    
    force_lab = Label(qa_sspage1_Frame1, text= 'Select Force:', font = ('Helvetica',10,'bold'), bg= '#36454F', fg='white')
    
    so_bk = Button(qa_sspage1_Frame1, text= '< Back',command=lambda:go_bk(SSqa), font = ('Helvetica',10,'bold'))
    quit_butz = Button(qa_sspage1_Frame1, text= 'QUIT', command=lambda: end_program(root), font = ('Helvetica',10,'bold'))
    
    mdc_plot = Button(qa_sspage1_Frame1, text= 'Answer', command= lambda: qa_ss_func(plotparent=SSqa, plotspace=qa_sspage2_Frame2,
                                                                             startyear=qa_ssstartyear.get(), endyear=qa_ssendyear.get(),
                                                                             startmonth=qa_ssstartmonth.get(), endmonth=qa_ssendmonth.get(),
                                                                             force=qa_force.get(), quest=qa_ssquest.get()), font = ('Helvetica',10,'bold'),bg='#800000', fg='white')
    
    qapage1_Label.grid(row=0, column=0, columnspan=3, ipadx= 150, ipady=10, padx=10, pady=10)
    qa_sspage1_Frame1.grid(row=1, column=0)
    qa_sspage2_Frame2.grid(row=1, column=1, columnspan=1)
    

    qapage1_Frame1_smonth.grid(row=0, column=1, ipadx=85, pady=10, padx=10, sticky=NE)
    qapage1_Frame1_syear.grid(row=1, column=1, ipadx=85, pady=10, padx=10, sticky=NE)
    qapage1_Frame1_quest.grid(row=5, column=1, ipadx=85, pady=10, padx=10, sticky=NE)
    qapage1_Frame1_force.grid(row=4, column=1, ipadx=85, pady=10, padx=10, sticky=NE)
    
    qapage1_Frame1_emonth.grid(row=2, column=1, ipadx=85, pady=10, padx=10, sticky=NE)
    qapage1_Frame1_eyear.grid(row=3, column=1, ipadx=85, pady=10, padx=10, sticky=NE)
 
    
    force_lab.grid(row=4, column=0, ipadx=60, pady=10, padx=10, sticky=NW)
    smonth_lab.grid(row=0, column=0, ipadx=45, pady=10, padx=10, sticky=NW)
    syear_lab.grid(row=1, column=0, ipadx=55, pady=10, padx=10, sticky=NW)
    
    emonth_lab.grid(row=2, column=0, ipadx=50, pady=10, padx=10, sticky=NW)
    eyear_lab.grid(row=3, column=0, ipadx=60, pady=10, padx=10, sticky=NW)
    quest_lab.grid(row=5, column=0, ipadx=60, pady=10, padx=10, sticky=NW)

    
    quit_butz.grid(row=7, column=1, padx=10, pady=10, ipadx=60, ipady=5, sticky=NE)
    so_bk.grid(row=7, column=0, padx=10, pady=10, ipadx=40, ipady=5,sticky=NW)


    mdc_plot.grid(row=6, column=0, columnspan=2, padx=10, pady=10, ipadx=120, ipady=5)



    
def ssbydateregion():
    
    polpg1year = StringVar()
    polpg1month = StringVar()
    polpg1endmonth = StringVar()    
    polpg1endyear = StringVar()
    polpg1force = StringVar()
    polpg1plot = StringVar()
    
    Polpg1 = Toplevel()
    polpg1_Frame1 = LabelFrame(Polpg1, padx=10, pady=10, bg= '#36454F')
    polpg1_Frame2 = LabelFrame(Polpg1, padx=10, pady=10)
    
    
    polpg1_Frame1_year = OptionMenu(polpg1_Frame1, polpg1year, *stopsearchdates_year)
    polpg1_Frame1_month = OptionMenu(polpg1_Frame1, polpg1month, *stopsearchdates_month)
    polpg1_Frame1_endyear = OptionMenu(polpg1_Frame1, polpg1endyear, *stopsearchdates_year)
    polpg1_Frame1_endmonth = OptionMenu(polpg1_Frame1, polpg1endmonth, *stopsearchdates_month)
    polpg1_Frame1_force = OptionMenu(polpg1_Frame1, polpg1force, *force_name)
    polpg1_Frame1_plot = OptionMenu(polpg1_Frame1, polpg1plot, *pol_plot_type)
    
    year_lab = Label(polpg1_Frame1, text='Select Start Year:', font=('Helvetica',10,'bold'), bg= '#36454F', fg='white')
    month_lab = Label(polpg1_Frame1, text='Select Start Month:', font=('Helvetica',10,'bold'), bg= '#36454F', fg='white')
    endyear_lab = Label(polpg1_Frame1, text='Select End Year:', font=('Helvetica',10,'bold'), bg= '#36454F', fg='white')
    endmonth_lab = Label(polpg1_Frame1, text='Select End Month:', font=('Helvetica',10,'bold'), bg= '#36454F', fg='white')
    force_lab = Label(polpg1_Frame1, text='Select Force:', font=('Helvetica',10,'bold'), bg= '#36454F', fg='white')
    plot_lab = Label(polpg1_Frame1, text='Select Plot to Make:', font=('Helvetica',10,'bold'), bg= '#36454F', fg='white')
    

    polpg1_Button_ap = Button(polpg1_Frame1, text = 'PLOT', command= lambda: pol_oos(plotparent=Polpg1,plotspace =polpg1_Frame2,
                                                                                     startyear=polpg1year.get(),endyear=polpg1endyear.get(),
                                                                                     startmonth=polpg1month.get(),endmonth=polpg1endmonth.get(),
                                                                                     force=polpg1force.get(),top=polpg1plot.get()), font = ('Helvetica',10,'bold'),bg='#800000', fg='white')
    bk_button = Button(polpg1_Frame1, text = '< Back', command= lambda:go_bk(Polpg1), font = ('Helvetica',10,'bold'))
    quit_stuff = Button(polpg1_Frame1, text = 'Quit', command= lambda: end_program(root), font = ('Helvetica',10,'bold'))
    
    
    polpg1_Frame1.grid(row=1, column=0)
    polpg1_Frame2.grid(row=1, column=1)
    
    polpg1_Frame1_year.grid(row=1,column=1, ipadx=85, pady=10, padx=10, sticky=NE)
    polpg1_Frame1_month.grid(row=0,column=1, ipadx=85, pady=10, padx=10, sticky=NE)
    polpg1_Frame1_endyear.grid(row=3,column=1, ipadx=85, pady=10, padx=10, sticky=NE)
    polpg1_Frame1_endmonth.grid(row=2,column=1, ipadx=85, pady=10, padx=10, sticky=NE)
    polpg1_Frame1_force.grid(row=4,column=1, ipadx=85, pady=10, padx=10, sticky=NE)
    polpg1_Frame1_plot.grid(row=5,column=1, ipadx=85, pady=10, padx=10, sticky=NE)
    
    year_lab.grid(row=1, column=0, ipadx=25, pady=10, padx=10, sticky=NW)
    month_lab.grid(row=0, column=0, ipadx=25, pady=10, padx=10, sticky=NW)
    endyear_lab.grid(row=3, column=0, ipadx=35, pady=10, padx=10, sticky=NW)
    endmonth_lab.grid(row=2, column=0, ipadx=35, pady=10, padx=10, sticky=NW)
    force_lab.grid(row=4, column=0, ipadx=55, pady=10, padx=10, sticky=NW)
    plot_lab.grid(row=5, column=0, ipadx=25, pady=10, padx=10, sticky=NW)
    
    polpg1_Button_ap.grid(row=6, column=0, columnspan =2, ipadx=120, ipady=5, padx=10,pady=10)
    bk_button.grid(row=7, column=0,ipadx=50, ipady=5, padx=10,pady=10)
    quit_stuff.grid(row=7, column=1,  ipadx=60, ipady=5, padx=10,pady=10)