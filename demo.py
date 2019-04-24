# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 15:18:08 2018

@author: rain
"""
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
import warnings
warnings.filterwarnings("ignore")
import numpy as np
import re
#np.set_printoptions(threshold=np.inf)
import tkinter as tk
from PIL import Image, ImageTk
from keras.models import model_from_json
import SimpleITK as sitk
import xlwt
import os
from tkinter.filedialog import askdirectory
import matplotlib.pyplot as plt
import tensorflow as tf
from diagnose import predict22,predict33

def loadFile(filename):
    ds = sitk.ReadImage(filename)
    img_array = sitk.GetArrayFromImage(ds)
    frame_num,width,height=img_array.shape
    return img_array
smallflag=0#判断前几个文件如1是不是要补两个0 001
m5=np.matrix([])
first_x=0
first_y=0
second_x=0
second_y=0
final_x=0
final_y=0
dragflag=0#是否拖动
flag=0#first time?
flag1=0#是否在范围内

temp_x=0
temp_y=0
matrix=np.matrix([])
existflag=0
num_list=[]
save_filename=''
m10=np.array([])
m11=np.array([])
m12=np.array([])
m13=np.array([])
m14=np.array([])

save_x1=0
save_y1=0
save_x2=0
save_y2=0
save_z1=0
save_z2=0

root=tk.Tk() #Toplevel()
i=int()
var = tk.StringVar()
var.set(str(i))


big=0
small=0
filename=''
path=''
timeflag=0
d=""
e=""
filetype ='.dcm'
dicom=str()
dicom1=str()
def first(event):#第一次点下鼠标
    global first_x,first_y,flag,flag1,temp_x,temp_y#flag是否为第一次点击，flag1代表是否按住鼠标
    if(flag==0):         
        first_x=event.x
        first_y=event.y
    if(flag==1):
        if(((event.x-first_x)*(event.x-second_x))<0 and ((event.y-first_y)*(event.y-second_y))<0):
            flag1=1          
            temp_x=event.x
            temp_y=event.y
            
        
def second(event):#点下并拖动鼠标
    global second_x,second_y,l,first_x,first_y,rect,dragflag,flag,temp_x,temp_y,flag1
    if (flag==0):  
        dragflag=1
        l.delete(rect)
        second_x=event.x
        second_y=event.y
        rect=l.create_rectangle(first_x, first_y, second_x, second_y,outline='green')
    if(flag==1 and flag1==1):
        if(first_x<second_x and first_y<second_y):
            if(first_x+event.x-temp_x>=0 and first_y+event.y-temp_y>=0 and second_x+event.x-temp_x<=512 and second_y+event.y-temp_y<=512):
                l.delete(rect)
                dragflag=1
                rect=l.create_rectangle(first_x+event.x-temp_x, first_y+event.y-temp_y, second_x+event.x-temp_x, second_y+event.y-temp_y,outline='red')
        if(first_x>second_x and first_y<second_y):
            if(first_x+event.x-temp_x<=512 and first_y+event.y-temp_y>=0 and second_x+event.x-temp_x>=0 and second_y+event.y-temp_y<=512):
                l.delete(rect)
                dragflag=1
                rect=l.create_rectangle(first_x+event.x-temp_x, first_y+event.y-temp_y, second_x+event.x-temp_x, second_y+event.y-temp_y,outline='red')
        if(first_x>second_x and first_y>second_y):
            if(first_x+event.x-temp_x<=512 and first_y+event.y-temp_y<=512 and second_x+event.x-temp_x>=0 and second_y+event.y-temp_y>=0):
                l.delete(rect)
                dragflag=1
                rect=l.create_rectangle(first_x+event.x-temp_x, first_y+event.y-temp_y, second_x+event.x-temp_x, second_y+event.y-temp_y,outline='red')
        if(first_x<second_x and first_y>second_y):
            if(first_x+event.x-temp_x>=0 and first_y+event.y-temp_y<=512 and second_x+event.x-temp_x<=512 and second_y+event.y-temp_y>=0):
                l.delete(rect)
                dragflag=1
                rect=l.create_rectangle(first_x+event.x-temp_x, first_y+event.y-temp_y, second_x+event.x-temp_x, second_y+event.y-temp_y,outline='red')


def final(event):#松开鼠标
    global dragflag,flag,rect,second_x,second_y,l,first_x,first_y,temp_x,temp_y,flag1,existflag
    existflag=1
    if (flag==0):       
        if (dragflag==1):  
            l.delete(rect)
            second_x=event.x
            second_y=event.y
            rect=l.create_rectangle(first_x, first_y, second_x, second_y,outline='green')
        dragflag=0
        flag=1;
    if(flag==1 and flag1==1 and dragflag==1):
        first_x=first_x+event.x-temp_x
        first_y=first_y+event.y-temp_y
        second_x=second_x+event.x-temp_x
        second_y=second_y+event.y-temp_y
        l.delete(rect)
        rect=l.create_rectangle(first_x, first_y, second_x, second_y,outline='green')
        temp_x=0
        temp_y=0
        dragflag=0
        flag1=0
         
def haress(wc1,ww1,a):
    wc=(wc1/4096)*255
    ww=(ww1/4096)*255
    min = (2*wc - ww)/2.0 + 0.5
    max = (2*wc + ww)/2.0 + 0.5
    dFactor = 255.0/(max - min); 
    a[a<min]=0
    a[a>max]=255
    a = (a - min)*dFactor
    a[a<0]=0
    a[a>255]=255
    return a 
   
    

wc1=tk.IntVar()
wc1.set(1585)
ww1=tk.IntVar()
ww1.set(1585)
def show():
    global filename,i
    img_array=loadFile(filename[i])
    a = np.matrix(img_array)
    a=haress(s2.get(),s3.get(),a)
    im=Image.fromarray(a)
    tkimg=ImageTk.PhotoImage(im)
    return tkimg

def processWheel(event):
    global im,filename,var,dicom,second_x,second_y,l,first_x,first_y,rect,big,d,e,i,timeflag,small,smallflag
    if(timeflag==1):
        if (event.delta > 0 and i<big):
            i=i+1
            im=show()
            l.delete(dicom)
            dicom=l.create_image(256,256,image = im)
            var.set(str(i+1))
            l.create_text(50,10,text = var.get()+'/'+str(big+1),  fill = 'white')
        
            l.delete(rect)
            rect=l.create_rectangle(first_x, first_y, second_x, second_y,outline='green') 
        elif(event.delta < 0 and i>=1):
            i=i-1
            im=show()
            l.delete(dicom)
            dicom=l.create_image(256,256,image = im)
            var.set(str(i+1))
            l.create_text(50,10,text = var.get()+'/'+str(big+1),  fill = 'white')      
            l.delete(rect)
            rect=l.create_rectangle(first_x, first_y, second_x, second_y,outline='green')
        
        
def change(event):#改变窗位窗宽对图像造成的影响
    global im,l,dicom,second_x,second_y,l,first_x,first_y,rect,timeflag,var,i
    if(timeflag==1):
        im=show()
        l.delete(dicom)
        dicom=l.create_image(256,256,image = im)
        var.set(str(i+1))
        l.create_text(50,10,text = var.get()+'/'+str(big+1),  fill = 'white')  
        l.delete(rect)
        rect=l.create_rectangle(first_x, first_y, second_x, second_y,outline='green')

def delete():#清除
    global l,second_x,second_y,l,first_x,first_y,rect,dragflag,flag,flag1,temp_x,temp_y,existflag
    first_x=0
    first_y=0
    second_x=0
    second_y=0
    temp_x=0
    temp_y=0
    flag=0
    flag1=0
    dragflag=0
    l.delete(rect)
    existflag=0
    

def save1():
    global save_z1,i,save_z2
    if(save_z1==i):
        tk.messagebox.showinfo('提示', '不要重复保存')
    else:
        save_z1=i
    if(save_z1==save_z2):
        tk.messagebox.showinfo('提示', '两个位置重复')
def save2():
    global save_z1,i,save_z2
    if(save_z2==i):
        tk.messagebox.showinfo('提示', '不要重复保存')
    else:
        save_z2=i
    if(save_z1==save_z2):
        tk.messagebox.showinfo('提示', '两个位置重复')
def save3():
    global save_x1,save_y1,save_x2,save_y2,second_x,second_y,l,first_x,first_y,flag,save_filename,filename,i
    if(flag==0):
        tk.messagebox.showinfo('提示', '未选取范围')
    else:
        save_x1=first_x
        save_y1=first_y
        save_x2=second_x
        save_y2=second_y
        save_filename=filename[i]
        
DATA=[('路径','z1','z2','x1','y1','x2','y2','分化')
   ]
def settle():
    global save_x1,save_y1,save_x2,save_y2,save_filename,save_z1,save_z2,i,DATA,loop_text
    workbook=xlwt.Workbook(encoding='utf-8')
    booksheet=workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)

    DATA.append((save_filename,save_z1,save_z2,save_x1,save_y1,save_x2,save_y2,loop_text.get()))
    DATA1=tuple(DATA)
    for i,row in enumerate(DATA1):
        for j,col in enumerate(row):
            booksheet.write(i,j,col)
            workbook.save('grade.xls')
    save_z1=0
    save_z2=0
    
def get_filename(path,filetype):
    name =[]
    final_name = []
    for root,dirs,files in os.walk(path):
        for i in files:
            if filetype in i:
                name.append(i.replace(filetype,''))
    final_name = [item +'.dcm' for item in name]
    return final_name


def get():
    global path,filetype,filename,big,d,e,i,timeflag,l,root,dicom,var,small,smallflag
    
    filename=[]
    path=askdirectory()#tkinter 选择路径 
    try:
        result=os.listdir(path)
    except(FileNotFoundError):
        print("没有选择文件夹")
        return
    result1=[]
    for element in result:
        element=path+'/'+element
        result1.append(element)
    #print(result1)
    filename=result1
    
    i=0#现在位于filename的第几张图片
    big=len(result)-1#打开的文件夹有几个元素
    im=show()
    timeflag=1
    l.delete(dicom)
    dicom=l.create_image(256,256,image = im)
    var.set(str(i+1))
    l.create_text(50,10,text = var.get()+'/'+str(big+1),  fill = 'white')  
    root.mainloop()

def he():
    global filename,i,big,m10,m11,m12,m13,m14,path,second_x,second_y,first_x,first_y
    predict22(filename,i,big,m10,m11,m12,m13,m14,path,second_x,second_y,first_x,first_y)
def he2():
    global filename,i,big,m10,m11,m12,m13,m14,path,second_x,second_y,first_x,first_y
    predict33(filename,i,big,m10,m11,m12,m13,m14,path,second_x,second_y,first_x,first_y)
s2 = tk.Scale(root,
      from_ = 10,#设置最小值
      to = 40950,#设置最大值
      orient = tk.HORIZONTAL,#设置横向
      resolution=5,#设置步长
      tickinterval = 5000,#设置刻度
      length = 500,# 设置像素
      variable = ww1,
      command=change)#绑定变
s2.grid(row=1,column=1)

s3 = tk.Scale(root,
      from_ = 20,#设置最小值
      to = 40950,#设置最大值
      resolution=5,#设置步长
      tickinterval = 5000,#设置刻度
      length = 500,# 设置像素
      variable = wc1,
      command=change)#绑定变量
s3.grid(row=0,column=2) 


l = tk.Canvas(root,width = 512, height = 512,bg = 'white')

l.bind("<MouseWheel>", processWheel)

rect=l.create_rectangle(first_x, first_y, second_x, second_y)
l.bind("<Button-1>",first)
l.bind("<B1-Motion>",second)
l.bind("<ButtonRelease-1>",final)
l.grid(row=0,column=1)



b1 = tk.Button(root, text='清除',width=12,command=delete)
#b2 = tk.Button(root, text='截取',width=12,command=cut)
b3 = tk.Button(root, text='肿瘤起始坐标',width=12,command=save1)
b4 = tk.Button(root, text='肿瘤终止坐标',width=12,command=save2)
b5 = tk.Button(root, text='肿瘤截面范围',width=12,command=save3)
b6 = tk.Button(root, text='记录',width=12,command=settle)
b7 = tk.Button(root, text='读取',width=12,command=get)

b7.grid(row=0,column=0,sticky='N') 
b10 = tk.Button(root, text='二分类',width=12,command=he)
b11 = tk.Button(root, text='三分类',width=12,command=he2)
b1.place(x = 0, y = 40)
#b2.place(x = 0, y = 80)
b3.place(x = 0, y = 120)
b4.place(x = 0, y = 160)
b5.place(x = 0, y = 200)
b6.place(x = 0, y = 240)
b10.place(x = 0, y = 360)
b11.place(x = 0, y = 400)


l3 = tk.Label(root, text="分化程度：")
l3.place(x = 10, y = 280)
loop_text = tk.StringVar()
loop = tk.Entry(root, textvariable = loop_text,width=12)
loop_text.set(" ")
loop.place(x = 5, y = 300)

root.mainloop()
    
    
def welcome2():
    global b99,b122
    b99.destroy()
    b122.destroy()
    s2 = tk.Scale(root,
          from_ = 10,#设置最小值
          to = 40950,#设置最大值
          orient = tk.HORIZONTAL,#设置横向
          resolution=5,#设置步长
          tickinterval = 5000,#设置刻度
          length = 500,# 设置像素
          variable = ww1,
          command=change)#绑定变
    s2.grid(row=1,column=1)
    
    s3 = tk.Scale(root,
          from_ = 20,#设置最小值
          to = 40950,#设置最大值
          resolution=5,#设置步长
          tickinterval = 5000,#设置刻度
          length = 500,# 设置像素
          variable = wc1,
          command=change)#绑定变量
    s3.grid(row=0,column=2) 
    
    
    l = tk.Canvas(root,width = 512, height = 512,bg = 'white')
    
    l.bind("<MouseWheel>", processWheel)
    
    rect=l.create_rectangle(first_x, first_y, second_x, second_y)
    l.bind("<Button-1>",first)
    l.bind("<B1-Motion>",second)
    l.bind("<ButtonRelease-1>",final)
    l.grid(row=0,column=1)
    
    
    
    b10 = tk.Button(root, text='二分类',width=12,command=predict2)
    b11 = tk.Button(root, text='三分类',width=12,command=predict3)
    b10.grid(row=0,column=0,sticky='N') 
    #b2.place(x = 0, y = 80)
    b11.place(x = 0, y = 40)

#    b10.place(x = 0, y = 360)
#    b11.place(x = 0, y = 400)
    

    
    root.mainloop()

#b99 = tk.Button(root, text='清除',width=12,command=welcome)
#b122 = tk.Button(root, text='清除',width=12,command=welcome2)
#b99.place(x = 0, y = 0)
#b122.place(x = 0, y = 30)
#root.mainloop()