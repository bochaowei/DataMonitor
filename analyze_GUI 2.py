import datetime
from datetime import datetime
import json
import upload
import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
from PIL import ImageTk, Image
import web
read=1
#while read:
#    try:
#        filename=input('Please provide a file name')
#        filename=filename+'.txt'
#        with open(filename,'r') as f:
#            data=json.load(f)
#        read=0
#    except IOError:
#        print('Can not find the file, please re-enter the filename')
#    #except:
#        print('error')
#################################start the GUI
root = Tk()

setmaximum=DoubleVar()
setmaximum.set(10**6)
lab=Label(root,text='Please enter the upper limit')
lab.grid(row=1,column=1,sticky=W)
Entry(root,textvariable=setmaximum).grid(row=1,column=2)


setminimum=DoubleVar()
setminimum.set(-1000)
lab2=Label(root,text='Please enter the lower limit')
lab2.grid(row=2,column=1,sticky=W)
Entry(root,textvariable=setminimum).grid(row=2,column=2)
#################################################for statistics
Label(root,text="Mean").grid(row=3,column=1,sticky=W)
datamean=Label(root,text='wait')
datamean.grid(row=3,column=2)

Label(root,text="Range").grid(row=4,column=1,sticky=W)
datarange=Label(root,text='wait')
datarange.grid(row=4,column=2)

Label(root,text="Standard deviation").grid(row=5,column=1,sticky=W)
datastd=Label(root,text='wait')
datastd.grid(row=5,column=2)

emailaddress=StringVar()
lab=Label(root,text='Your email address for warning email:')
lab.grid(row=6,column=1,sticky=W)
Entry(root,textvariable=emailaddress).grid(row=6,column=2)
global count
count=0

warninglabel=Label(root)
warninglabel.grid(row=7,column=1,columnspan=3)


plotlabel= Label(root)
plotlabel.grid(row=30,column=1,columnspan=3)


def analyze():
    upload.download_from_bucket('data.txt', 'downloaded data.txt', 'dataset111')
    with open('downloaded data.txt','r') as f:
        data=json.load(f)
    reading=[]
    time=[]
    total=[]
    #print(setmaximum.get())
    for i in range(0,len(data)):
        reading.append(data[i][0])
        deltatime=datetime.strptime(data[i][1],'%Y-%m-%d %H:%M:%S.%f')-datetime.strptime(data[0][1],'%Y-%m-%d %H:%M:%S.%f')
        total.append((deltatime.total_seconds(),data[i][0]))
    result=total.copy()
    mean=np.mean(reading)
    
    global count
    for i in range(0,len(total)):
        if total[i][1]>mean*2 or total[i][1]<mean/5:
            result.remove(total[i])
    
    for point in result:
        rounddata=round(point[1]*10000)/10000
        if point[1]>setmaximum.get() or point[1]<setminimum.get():
            if '@' in emailaddress.get() and count<1:
                web.email(emailaddress.get(),'Data is over the limit, the reading now is '+str(rounddata))
                count=5
            #print(point[1])
            warninglabel.config(text='Warning!Reading is '+str(rounddata))
            warninglabel.config(font=("Courier", 26,'bold'),fg='red')
    if result[len(result)-1][1]<setmaximum.get() and result[len(result)-1][1]>setminimum.get():
        count=0
        roundreading=round(result[len(result)-1][1]*10000)/10000
        warninglabel.config(text='Reading is '+str(roundreading))
        warninglabel.config(font=("Courier", 15,'bold'),fg='black')
    #for i in range(0,len(reading)-1):
    #    if abs(reading[i]-reading[i+1])/reading[i]>0.5:
    #        if abs(reading[i]-mean)>abs(reading[i+1]-mean):
    #            readings.remove(reading[i])
    #            del time[i]
    #        else:
    #            readings.remove(reading[i+1])
    #            del time[i+1]
    result = np.array(result)
    std=np.std(result[:,1])
    datastd.config(text=str(round(std*10000)/10000))
    newmean=np.mean(result[:,1])
    ranges=max(result[:,1])-min(result[:,1])
    datamean.config(text=str(round(newmean*10000)/10000))
    datarange.config(text=str(round(ranges*10000)/10000))
    plt.plot(result[:,0],result[:,1])
    plt.xlabel('Time(s)')
    plt.ylabel('Signal')
    plt.savefig('plot.jpg')
    plot2 = ImageTk.PhotoImage(Image.open("plot.jpg").resize((700,500),Image.ANTIALIAS))
    plotlabel.config(image=plot2)
    plotlabel.image=plot2
    root.after(700, analyze)
analyze()


root.mainloop()