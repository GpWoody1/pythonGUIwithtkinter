
from tkinter import *
from PIL import ImageTk 
from PIL import Image as imggg
import os
from commonfunctionmodule import *
from covidmodule import *
from stopandsearchmodule import *

    
##Creating Labels and button on main page

root = Tk()
root.title('Data Analysis Module')
rootLab1 = Label(root, text='PLEASE SELECT A PLOT TO VIEW', bg='#AA4A44', fg='white', font = ('Helvetica',14,'bold'))
rootFrame1 = LabelFrame(root, padx=10, pady=10, bg= '#36454F')
rootFrame2 = LabelFrame(root,  padx=10, pady=10, bg= '#36454F')


rootFrame3 = LabelFrame(root,  padx=10, pady=10)
rootquit = Button(root, text='QUIT',command=lambda: end_program(root), bg='#800000', fg='white', font=('Helvetica',12, 'bold'))
img_label = ImageTk.PhotoImage(imggg.open("static/TeessideUniLogo.jpg"))
rootImg = Label(rootFrame3, image= img_label)
rootCovLab1 = Label(rootFrame1, text='SELECT COVID19 PLOT OF INTEREST', bg='#AA4A44', fg='white', font = ('Helvetica',12,'bold'))
rootCovBut1 = Button(rootFrame1, text = 'Cases Analysis by Date & Region',font = ('Helvetica',10), command= ccbydateregion)
rootCovBut2 = Button(rootFrame1, text = 'Comparative Analysis by Date & Regions',font = ('Helvetica',10),command=cccompanal)
rootCovBut3 = Button(rootFrame1, text= 'Q&A', command = qa_covid, font = ('Helvetica',10))

rootSSLab1 = Label(rootFrame2, text= 'SELECT STOP & SEARCH PLOT OF INTEREST', bg='#AA4A44', fg='white', font = ('Helvetica',12,'bold'))
rootSSBut1 = Button(rootFrame2, text= 'Stop & Search by Date & Force',font = ('Helvetica',10), command= ssbydateregion)
rootSSBut2 = Button(rootFrame2, text= 'Comparative Analysis by Date & Force', command= pol_companal,font = ('Helvetica',10))
rootSSBut3 = Button(rootFrame2, text = 'Q&A', command= qa_ss, font = ('Helvetica',10))

## packing items on screen
rootFrame1.grid(row=1, column=0, sticky= N, columnspan=1)
rootFrame2.grid(row=1, column=2, sticky=N, columnspan=1)
rootFrame3.grid(row=1, column=1, sticky=N, columnspan=1, rowspan=4)
rootImg.grid(row=0, column  = 0)
rootquit.grid(row=2, column=1, sticky=N, columnspan=1, ipadx=20, ipady= 3, padx=10, pady=10)
rootLab1.grid(row=0, column=1, columnspan=1, ipady=10, ipadx=50)


rootCovLab1.grid(row=0, column=0, padx=10, pady=10, ipadx=50, ipady=5)
rootCovBut1.grid(row=1, column=0, padx=10, pady=10, ipadx=50, ipady=5)
rootCovBut2.grid(row=2, column=0, padx=10, pady=10, ipadx=30, ipady=5)
rootCovBut3.grid(row=3, column=0, padx=10, pady=10, ipadx=134, ipady=5)

rootSSLab1.grid(row=0, column=0, padx=10, pady=10, ipadx=50, ipady=5)
rootSSBut1.grid(row=1, column=0, padx=10, pady=10, ipadx=50, ipady=5)
rootSSBut2.grid(row=2, column=0, padx=10, pady=10, ipadx=30, ipady=5)
rootSSBut3.grid(row=3, column=0, padx=10, pady=10, ipadx=128, ipady=5)
 
mainloop()

