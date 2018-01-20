#!/usr/bin/env python
#Python 2v8
#AMS V7 Release
#Under CC-SA
#Ref:26Aug17
#Author: Samad Haque <mailto:ubdussamad@gmail.com>
#TODO Fix error (handling and reporting) scenarios
# Noticed Exceptions :
# *DivisionByZero Error
# *Index overflow
# *Catinated errors if file is not found!
try:
    from tkinter import *
except:
    from Tkinter import * #For python 3 Compatibility

import re,time

from datetime import datetime


#--------Declaring Variables!
profile = "username"

def sheet(profile,mode,state='n/a'):
    try:
        with open('%s_stats.dat'%(profile,),'r') as register_: #file contains:#of Working Days|#of Days student was present|datetime object in from of string
            register = register_.read().strip('\n').split('|')
            register_.close()
    except: return 100
    percentage_attendence = ( ( float(register[1]) / float(register[0]) ) * 100.0 ) #Calc % attendence!
    if mode.lower() == 'r': #Only for reading data!
        return [percentage_attendence]+register #Note that register still has values in strings inside!
    elif mode.lower() == 'w':
        register_obj = open('%s_stats.dat'%(profile,),'w')
        if state == 'p':#Case when student was pesent today!
            data = [ (int(register[0])+1) , (int(register[1])+1) ,
                     (datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')) ]
            register_obj.write("%d|%d|%s"%tuple(data))
            register_obj.flush()
            register_obj.close()
        elif state == 'a':#Case when student was absent today!
            data = [ (int(register[0])+1) , (int(register[1])) ,
                     (datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')) ]
            register_obj.write("%d|%d|%s"%tuple(data))
            register_obj.flush()
            register_obj.close()
        else:
            return 102
def dummy(*args):
    print('This is a Dummy Function for test!')
def time_updater(label):
    def update():
        label.config(text=str(time.ctime()))
        label.after(1000,update)
    update()
def mycolor(x,return_gradient_color=False):
    if return_gradient_color:
        R = int((255 * (100-x)) / 100)
        G = int((255 * x) / 100)
        return '#%02x%02x%02x' % (R,G,0)
    return '#%02x%02x%02x' % x
def update_percentage(percentage):
    def update():
        data = sheet(profile,'r')
        perc = data[0]
        percentage.config(text=(format(perc,'.2f')+'%'),
                          fg=mycolor(int(perc),True))
        percentage.after(100,update) #Time intervel is flexible but must be greater than 10ms otherwise cpu usage will skyrocket
    update()
def sequence(*functions):
    def func(*args, **kwargs):
        return_value = None
        for function in functions:
            return_value = function(*args , **kwargs)
        return return_value
    return func


def regist_needed():
    print("Checke4d!")
    return (datetime.strptime(str(sheet(profile,'r')[3]),"%Y-%m-%d %H:%M:%S.%f").date()<datetime.now().date())

def unpack(*widgets):
    for widget in widgets:widget.pack_forget()
def check_loop(root):
    if regist_needed():buttons(root)
    else:
        hard_register = Button(root,text='Hard Register',command = lambda : sequence(buttons(root),unpack(hard_register)),font="NanumGothicCoding 12 bold")
        hard_register.pack()
def buttons(root):
    absent = Button(root,text='Absent',font="NanumGothicCoding 12 bold",bg='red',
                    command=lambda:sequence(dummy() ,sheet(profile,'w','a'),unpack(absent,present),check_loop(root)))
    absent.pack(side=RIGHT,padx=20)
    present = Button(root,text='Present',font="NanumGothicCoding 12 bold",bg='green',
                     command=lambda: sequence(sheet(profile,'w','p'),unpack(absent,present),check_loop(root)))
    present.pack(side=LEFT,padx=20)
    
def main():
    root = Tk()
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    logo = PhotoImage(file="UmbrellaCorporation3.png")
    logo_ = Label(root,justify=LEFT,compound = LEFT,padx = 10,
    text='Umbrella Corporate.\n Cleansing Life!',
    font="NanumGothicCoding 12 bold",fg=mycolor((10,40,60)),image=logo)
    logo_.pack(padx=15,pady=20)
    root.overrideredirect(2)
    root.geometry("%dx%d+%d+%d" % (280, 400,(w-280),(h-500)))
    root.grid()
    root.resizable(0,0)
    l1=Label(root,text="Attendence Monitoring System \n",fg="black",font="NanumGothicCoding 10 bold").pack()
    head_timer = Label(root, fg="dark green",font = "NanumGothicCoding 12 bold")
    head_timer.pack(padx=20)
    time_updater(head_timer)
    data = sheet(profile,'r')
    percentile_lb = Label(root,text='Your % Attendence is:',fg = "grey",
    font = "NanumGothicCoding 12 bold").pack(pady=10)#Updated every 100ms
    percentage = Label(root,fg = mycolor(data[0],True),font = "NanumGothicCoding 25 bold")
    percentage.pack()
    update_percentage(percentage)
    l1=Label(root,text="Were you?",fg="black",font="NanumGothicCoding 10 bold").pack()
    exit_button = Button(root,text='Exit!',font="NanumGothicCoding 12 bold",fg='dark red',command=root.destroy).pack(fill=Y)
    check_loop(root)
    l1=Label(root,text="Ubdussamad | Bachmanity Inc.",fg="black",font="NanumGothicCoding 8 bold").pack(side=BOTTOM)
    root.mainloop()
if __name__ == '__main__':
    main()
