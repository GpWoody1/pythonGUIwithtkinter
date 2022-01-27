# pythonGUIwithtkinter
This collects data from UK Government police site as well as covid data, uses a user query to return graphs and answer users questions.
This program was originally written with spyder IDE and modified for Jupyter. 

You would find GUI module, common function module, covid module, stop and search module. 

common function module contains function used in all three other modules. 
covid module depends on common function module
stop and search depends on common function module
gui module depends on commonfunction, covid and stop and search modules. 

The GUI module would import all other module as part of its dependencies, so ensure they are in the same
root directory of the IDE you use. 

Ensure the image "TeessideUniLogo.jpg" is in root directory as well as it displays in the program. 
Ensure the covid data "specimenDate_ageDemographic-unstacked" is in root directory as well as it is used by the covid module. 

Packages needed for this program to run include:

tkinter
pillow
os
requests
json
pandas
numpy
matplotlib
datetime
calender

* All packages comes by default in python except pillow which may not be available in some python versions. 
I advice to use pip install pillow from command shell before running the program. 


N/B: Navigation bar at the bottom of plots can be used to adjust subplot sizes. 
Make use of the wspace, hspace and left bars to adjust subplot sizes accordingly.
Under configure subplots:
Left move the entire plot to the right or left when slidder is moved, 
bottom slider moves plot top and bottom,
right moves plot right or left, 
Top moves plot top or bottom, 
wspace adjusts the width between subplots, 
hspace adjust the heights between subplots, 
You can save the plot directly using the save option, 
You can also zooom in using the zoom option and 
You can move the contents of a graph using the anchor.


FOR COVID PLOTS:

 -> Cases Analysis by date & region:
	
	In this module, age range selection is set to optional by default and when set to optional or blank, 
	4 plots are created which summarizes all infection rate for a region. 
	The first plot of the 4 plots is for age 0-59 cummulative daily cases, the second age 60+ cummulative daily cases, the third plot 
	Total cummulative cases and the last plot are for unassigned age cases. User must select all start and end dates parameters 
	as well as the area and the area type for plot to be made. Any area without proper areatype selection would throw a warning on screen. 
	Total cases  can be selected from Age range. Also if the selected data has no content in it albeit an empty dataframe, 
	it pops up an error message saying
	theres an issue with the entry and asks you if you want to make another plot or a warning message telling you what went wrong. 
	
	
	Action on click of buttons & plots made:

		-> PLOT DAILY CASES:
			This button makes a plot of cummulative daily cases for all 4 plots as stated above 
			if age range is on optional or blank, and makes single plots for any
			age range that is selected if set. The data plotted is a cummulative of daily cases for age range
		
		-> PLOT % DAILY CASES:
			This button makes a plot of the daily percentage change of casesfor all 4 plots as stated above 
			if age range is on optional or blank, and makes single plots for any
			age range that is selected if set. The data plotted is a % daily cummulative change for age range
		
		-> PLOT WEEKLY CASES:
			This button makes a plot of the weekly cases for all 4 plots as stated above if age range is optional 
			or blank, and makes single plots for any age range if selected. 
			The data plotted is each 7 day cummulative case rate for any date range selected, so data are grouped by 7days. 
		
		-> PLOT MONTHLY CASES FOR ENTIRE DATASET:
			This button makes a plot of the entire dataset for all 4 plots as stated above if age range is set to optional 
			or blank, and makes single plot for any age range selected.
			The data plotted is monthly progression and does not take into account any date selected in the GUI, but always plots 
			monthly progression of cases for all time for the entire covid dataset. 
		
		-> QUIT:
			This ends the entire program
		
		-> BACK:
			This closes the current page opened
		
		-> CLEAR ENTRIES:
			This clears all entries from the input. Note that if all entries are cleared and you try to plot. 

 -> Comparative Analysis by date & region:
	
	In this module, age range selection is set to optional by default for both regions and when set to optional or blank, 4 plots are created which summarize
	all infection rate for both regions being compared. 
	The first plot for age 0-59 cummulative daily cases, the second age 60+ cummulative daily cases, the third plot Total cummulative cases and the last plot are
	for unassigned age cases. User must select all start and end dates parameters as well as the area and the area type. Any area without proper areatype selection 
	would throw a warning on screen. Both areas must have data provided. If one area has no data for the time selected, it throws an error on screen. 
	Total cases  can be selected from Age range. In this section, user can compare both region by either daily cases plot or 
	cummulative daily plots. 
	By default, cummulative is selected. 

	Action on click of button:
		
		-> PLOT COMPARISON:

			This plots either a cummulative or daily cases(depending on user selection) for all 4 plots as stated above if age range of any of the 
			regions being compared is blank or optional. 
			User must select an age range on both region for it to plot a single plot for comparison else it plots the default 4 plots. 


-> Covid Q&A:

	In this module, you select the date and the question you need answered from the list of questions and you would get and answer on screen. 

	Action on click of button:

		-> ANSWER:

			This answer whatever question the user selected from the select question dropdown. 



FOR STOP AND SEARCH PLOTS:

This can only plot information in the last 3 years from the current date as dates above 3 years are achieved by UK police. 
So if you run the app in June 2022, you would only have access to plot from June2019 to May 2022.

-> Stop and Search by Date & Forces
		
	Action on click of buttons & plot made:

		-> PLOT:
			outcome:
			when outcome is selected from the dropdown list of plot to make and the plot button is clicked, makes a horizontal bar plot 
			of outcome of stop and search to the total number of stops and search.
			
			object of search:
			when this is selected from the dropdown list of plot to make and the plot button is clicked, makes a horizontal bar plot 
			of object from stop and search and the total number of stops and search. 
			
			Age range of suspect:
			when this is selected from the dropdown list of plot to make and the plot button is clicked, makes a horizontal bar plot 
			of age range of suspects from stop and search to the total number of stops and search.

			Gender of suspects:
			when this is selected from the dropdown list of plot to make and the plot button is clicked, makes a horizontal bar plot 
			of gender of suspects from stop and search to the total number of stops and search.
			
			Type of search:
			when this is selected from the dropdown list of plot to make and the plot button is clicked, makes a horizontal bar plot 
			of type of search from the stop and search to the total number of stops and search. 

			Ethnicity of suspect: 
			when this is selected from the dropdown list of plot to make and the plot button is clicked, makes a horizontal bar plot 
			of ethnicity of suspect from stop and search to the total number of stops and search. 

			Clothing Removal:
			when this is selected from the dropdown list of plot to make and the plot button is clicked, makes a horizontal bar plot 
			of truth value of suspect removing more than outer clothing from stop and search. 

			Total number of Stops:
			when this is selected from the dropdown list of plot to make and the plot button is clicked, makes a line graph of the number of 
			stop and searches made daily by the selected force in the selected time period. 




FOR UNITTESTING:
	-> Simply launch the unittest programs for each modules to run tests on them
