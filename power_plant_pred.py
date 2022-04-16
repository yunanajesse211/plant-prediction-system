from tkinter import *
import pyttsx3
from tkinter import ttk
from PIL import Image,ImageTk
from ttkthemes import themed_tk
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from tkinter import messagebox 
from sklearn.ensemble import  RandomForestRegressor


class Plant:
    def __init__(self,win):
        self.win=win
        self.win.geometry('1350x800')
        self.win.title('PLANT ENERGY PREDICTION SYSTEM')
        self.win.iconbitmap('plant.ico')
        self.win.resizable(False,True)
        self.text_f=Label(self.win,text='ENERGY PREDICTOR',font='elephant 40 bold',fg='Navyblue')
        self.text_f.pack()
        self.frame=Frame(self.win,bg='black')
        self.frame.place(x=80,y=80,width=1250,height=600)
        self.fram=Frame(self.frame,bg='blue')
        self.fram.place(x=20,y=20,width=1200,height=500)

        #temparature Widget
        self.at_l=Label(self.fram,text='ENTER AMBIENT VARIABLE TEMPARATURE VALUE:',font='arial 18 bold',fg='white',bg='blue').grid(row=0,column=0,padx=5,pady=8,sticky=W)
        self.at_value=StringVar()
        self.at_e=ttk.Entry(self.fram,width=30,textvariable=self.at_value,font='arial 15 bold')
        self.at_e.grid(row=0,column=1,padx=5,pady=8,sticky=W)

        #pressure widget
        self.ap_l=Label(self.fram,text='ENTER AMBIENT PRESSURE VALUE:',font='arial 18 bold',fg='white',bg='blue').grid(row=1,column=0,padx=5,pady=8,sticky=W)
        self.ap_value=StringVar()
        self.ap_e=ttk.Entry(self.fram,width=30,textvariable=self.ap_value,font='arial 15 bold')
        self.ap_e.grid(row=1,column=1,padx=5,pady=8,sticky=E)

        #Relative humidity widget
        self.rh_l=Label(self.fram,text='ENTER RELATIVE HUMIDITY VALUE:',font='arial 18 bold',fg='white',bg='blue').grid(row=2,column=0,padx=5,pady=8,sticky=W)
        self.rh_value=StringVar()
        self.rh_e=ttk.Entry(self.fram,width=30,textvariable=self.rh_value,font='arial 15 bold')
        self.rh_e.grid(row=2,column=1,padx=5,pady=8,sticky=E)

        #Exhaust volume widget
        self.ev_l=Label(self.fram,text='EXHAUST VACCUUM VALUE:',font='arial 18 bold',fg='white',bg='blue').grid(row=3,column=0,padx=5,pady=8,sticky=W)
        self.ev_value=StringVar()
        self.ev_e=ttk.Entry(self.fram,width=30,textvariable=self.ev_value,font='arial 15 bold')
        self.ev_e.grid(row=3,column=1,padx=5,pady=8,sticky=E)

       
        self.predict=Button(self.fram,text='VIEW PLANT ENERGY',command=self.prediction,width=30,font='cursive 15 bold',bd=0,bg='Green',fg='white')
        self.predict.place(x=400,y=250)

        self.result=Label(self.fram,text='ENERGY OUTPUT:0.00',font='arial 18 bold',fg='white',bg='blue')
        self.result.place(x=400,y=350)

         
    def prediction(self):
        try:
            self.plant_details=np.array([[float(self.at_value.get()),float(self.ev_value.get()),float(self.ap_value.get()),float(self.rh_value.get())]])
            
            #data
            self.data=pd.read_csv('dataset/power_plant.csv')
            self.x=self.data.iloc[:,:-1].values
            self.y=self.data.iloc[:,-1].values
            #training
            self.x_train,self.x_test,self.y_train,self.y_test=train_test_split(self.x,self.y,test_size=.2,random_state=40) 
            
            #making predictions
            self.rf=RandomForestRegressor(max_depth=19, n_estimators=160)

            self.rf.fit(self.x_train,self.y_train)
            self.y_pred=self.rf.predict(self.plant_details)
            

            messagebox.showinfo('success','wait for result')
            self.result.config(text='ENERGY OUTPUT:'+str(round(self.y_pred[0],3))+'MW')
            speech=pyttsx3.init()
            voice=speech.getProperty('voices')
            speech.setProperty('rate',150)
            data={'AT':[float(self.at_value.get())] ,'V':[float(self.ev_value.get())],'AP':[float(self.ap_value.get())] ,'RH':[float(self.rh_value.get())] , 'Energy Output':[round(self.y_pred[0],2)]}
            df=pd.DataFrame(data,columns=['AT','V','AP','RH','PE'])
            df.to_csv('plant_energy.csv',index=False,mode='a',header=False)
            speak='The estimated Power Energy is,'+str(round(float(self.y_pred[0]),3))+'megawatt'
            speech.say(speak)
            speech.runAndWait()
            print(float(self.at_value.get()))
            print(self.ap_value.get())
            print(self.rh_value.get())
            print('welcome')
            self.clear()
        except Exception as e:
            self.clear()
            messagebox.showerror("ERROR ALERT",'please check valid numebrs are required')
            print(e)
           
            
        
    def clear(self):
        self.at_e.delete(0,END)
        self.rh_e.delete(0,END)
        self.ev_e.delete(0,END)
        self.ap_e.delete(0,END)
      
       
        
        

if __name__=="__main__":
    win=themed_tk.ThemedTk(theme='breeze')
    obj=Plant(win)
    win.mainloop()

