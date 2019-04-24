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


#config = tf.ConfigProto()
#config.gpu_options.allow_growth = True
#session = tf.Session(config=config)

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
#    for root1, dirs, files in os.walk(path,topdown=False):
#        print(dirs)
    
#    parent_path=os.path.dirname(path)
#    lll=os.listdir(parent_path)
#    for i7 in lll:
#        n3,ext=os.path.splitext(i7)
#        if n3.find('E')>=0:#寻找文件夹中含特定字符的文件夹名
#            print(parent_path+'/'+i7)
    
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
    
#    fer=[]
#    fer1=[]
#    fer2=[]
#    fer3=[]
#    fer4=[]
#    parent_path=os.path.dirname(path)
#    lll=os.listdir(parent_path)
#    for i7 in lll:
#        n3,ext=os.path.splitext(i7)
#        if n3.find('E')>=0:#寻找文件夹中含特定字符的文件夹名
#            path1=parent_path+'/'+i7
#            result00=os.listdir(path1)
#            resulttemp00=[]
#            for element00 in result00:
#                element00=path1+'/'+element00
#                resulttemp00.append(element00)
#            for v in range(5,10):
#                fer.append(resulttemp00[v])
#        if n3.find('F')>=0:#寻找文件夹中含特定字符的文件夹名
#            path1=parent_path+'/'+i7
#            result00=os.listdir(path1)
#            resulttemp00=[]
#            for element00 in result00:
#                element00=path1+'/'+element00
#                resulttemp00.append(element00)
#            for v in range(5,10):
#                fer1.append(resulttemp00[v])
#        if n3.find('G')>=0:#寻找文件夹中含特定字符的文件夹名
#            path1=parent_path+'/'+i7
#            result00=os.listdir(path1)
#            resulttemp00=[]
#            for element00 in result00:
#                element00=path1+'/'+element00
#                resulttemp00.append(element00)
#            for v in range(5,10):
#                fer2.append(resulttemp00[v])
#        if n3.find('H')>=0:#寻找文件夹中含特定字符的文件夹名
#            path1=parent_path+'/'+i7
#            result00=os.listdir(path1)
#            resulttemp00=[]
#            for element00 in result00:
#                element00=path1+'/'+element00
#                resulttemp00.append(element00)
#            for v in range(5,10):
#                fer3.append(resulttemp00[v])
#        if n3.find('I')>=0:#寻找文件夹中含特定字符的文件夹名
#            path1=parent_path+'/'+i7
#            result00=os.listdir(path1)
#            resulttemp00=[]
#            for element00 in result00:
#                element00=path1+'/'+element00
#                resulttemp00.append(element00)
#            for v in range(5,10):
#                fer4.append(resulttemp00[v])

    
    i=0#现在位于filename的第几张图片
    big=len(result)-1#打开的文件夹有几个元素
    im=show()
    timeflag=1
    l.delete(dicom)
    dicom=l.create_image(256,256,image = im)
    var.set(str(i+1))
    l.create_text(50,10,text = var.get()+'/'+str(big+1),  fill = 'white')  
    root.mainloop()

#def getmaxandmin(filelist):#获取所选区域整个文件夹所有图片该区域的灰度最大最小值
#    global second_x,second_y,first_x,first_y
#    maxqueue=[]
#    minqueue=[]
#    b = np.matrix([])
#    for i1 in range(0,len(filelist)):
#        img_array=loadFile(filelist[i1])
#        a = np.matrix(img_array)
#        #a=haress(s2.get(),s3.get(),a)
#        if(first_x<second_x and first_y<second_y):
#            b=a[first_y:second_y,first_x:second_x]
#        if(second_x<first_x and first_y<second_y):
#            b=a[first_y:second_y,second_x:first_x]
#        if(second_x<first_x and second_y<first_y):
#            b=a[second_y:first_y,second_x:first_x]
#        if(first_x<second_x and second_y<first_y):
#            b=a[second_y:first_y,first_x:second_x]
#        maxqueue.append(b.max())
#        minqueue.append(b.min())
#        maxValue=max(maxqueue)-100
#        minValue=min(minqueue)
#    return maxValue,minValue
#
#
#def FindX(findlist,maxValue,minValue):#调整矩阵大小至选取的范围，归一化并压缩成32*32
#    global second_x,second_y,first_x,first_y
#    Matrix=[]
#    fff=np.matrix([])
#    b=np.matrix([])
#    for ff1 in range(0,5):      
#        img_array=loadFile(findlist[ff1])
#        a=np.matrix(img_array)
#        if(first_x<second_x and first_y<second_y):
#            b=a[first_y:second_y,first_x:second_x]
#        if(second_x<first_x and first_y<second_y):
#            b=a[first_y:second_y,second_x:first_x]
#        if(second_x<first_x and second_y<first_y):
#            b=a[second_y:first_y,second_x:first_x]
#        if(first_x<second_x and second_y<first_y):
#            b=a[second_y:first_y,first_x:second_x]
#        ff=np.matrix(b)   
#        fff=(ff-minValue)/(maxValue-minValue)
#        ffff=np.matrix(fff)
#        
#        
#        im1=Image.fromarray(ffff)
#        img = im1.resize((32,32))
#        fff1=np.asarray(img)
#        matrix = fff1
#        
#        
#        Matrix.append(matrix)
#    return Matrix
#
#def showtest(findlist):
#    global second_x,second_y,first_x,first_y,l1,dicom1,root
#    b=np.matrix([])
#    img_array=loadFile(findlist[0])
#    a=np.matrix(img_array)
#    if(first_x<second_x and first_y<second_y):
#        b=a[first_y:second_y,first_x:second_x]
#    if(second_x<first_x and first_y<second_y):
#        b=a[first_y:second_y,second_x:first_x]
#    if(second_x<first_x and second_y<first_y):
#        b=a[second_y:first_y,second_x:first_x]
#    if(first_x<second_x and second_y<first_y):
#        b=a[second_y:first_y,first_x:second_x]
#    ff=np.matrix(b)
##    fffffff1=ff.resize((32, 32))
#    
#    im1=Image.fromarray(ff)
#    img = im1.resize((32,32))
#    fff1=np.asarray(img)
#    
#    
#    im=Image.fromarray(fff1)
#    tkimg=ImageTk.PhotoImage(im)
#    l1.delete("all")
#    l1.create_image(256,256,image =tkimg)
#    root.mainloop()
#
#
#    
#def curb():
#    global existflag,second_x,second_y,l,first_x,first_y,filename,i,big,d,e,matrix,i,small,path
#    save3();
#    maxqueue=[]
#    minqueue=[]
#    fff=np.matrix([])
#    img_array=loadFile(filename)#得到原始图像
#    a = np.matrix(img_array)
#
#    if(first_x<second_x and first_y<second_y):
#        b1=a[first_y:second_y,first_x:second_x]
#    if(second_x<first_x and first_y<second_y):
#        b1=a[first_y:second_y,second_x:first_x]
#    if(second_x<first_x and second_y<first_y):
#        b1=a[second_y:first_y,second_x:first_x]
#    if(first_x<second_x and second_y<first_y):
#        b1=a[second_y:first_y,first_x:second_x]
#    
#    
#    for i2 in range(1,big+1):
#        if(i2<10 and small==1 and smallflag==0):
#            f=d+'_'+"0"+str((i2+small-1))+e
#        elif(i2<10 and small==1 and smallflag==1):
#            f=d+'_'+"00"+str((i2+small-1))+e
#        elif((i2+small-1)<100 and  small==1 and smallflag==1):
#            f=d+'_'+"0"+str((i2+small-1))+e
#        elif((i2+small-1)<100 and small>1):
#            f=d+'_'+"0"+str((i2+small-1))+e
#        else:
#            f=d+'_'+str((i2+small-1))+e
#        filename1=path+"\\\\"+f
#        img_array=loadFile(filename1)
#        a = np.matrix(img_array)
#        #a=haress(s2.get(),s3.get(),a)
#        if(first_x<second_x and first_y<second_y):
#            b=a[first_y:second_y,first_x:second_x]
#        if(second_x<first_x and first_y<second_y):
#            b=a[first_y:second_y,second_x:first_x]
#        if(second_x<first_x and second_y<first_y):
#            b=a[second_y:first_y,second_x:first_x]
#        if(first_x<second_x and second_y<first_y):
#            b=a[second_y:first_y,first_x:second_x]
#        maxqueue.append(b.max())
#        minqueue.append(b.min())
#        
##        print(b.max())
##        print(b.min())
##    print ("@@@@@@@@@@@@@@@@@@@@@@@@@@@")
#    #print(max(maxqueue))
#    #print(min(minqueue))
#    maxValue=max(maxqueue)-100
#    minValue=min(minqueue)
#    ff=np.array(b1)
#    fff=(ff-minValue)/(maxValue-minValue)
#    #print(fff)
#    
#    im1=Image.fromarray(fff)
#    img = im1.resize((32,32))
#    fff=np.asarray(img)   
#    
#    
#    matrix = fff 
#    predict()
#
##def curb():
##    global existflag,second_x,second_y,l,first_x,first_y,filename,big,d,e,matrix
##    save3();
##    maxqueue=[]
##    minqueue=[]
##    for i in range(1,big):
##        if(i<10):
##            f=d+"0"+str((i))+e
##        else:
##            f=d+str((i))+e
##        filename1=path+"\\\\"+f
##        img_array=loadFile(filename1)
##        a = np.matrix(img_array)
##        #a=haress(s2.get(),s3.get(),a)
##        if(first_x<second_x and first_y<second_y):
##            b=a[first_y:second_y,first_x:second_x]
##        if(second_x<first_x and first_y<second_y):
##            b=a[first_y:second_y,second_x:first_x]
##        if(second_x<first_x and second_y<first_y):
##            b=a[second_y:first_y,second_x:first_x]
##        if(first_x<second_x and second_y<first_y):
##            b=a[second_y:first_y,first_x:second_x]
##        maxqueue.append(b.max())
##        minqueue.append(b.min())
##        
##    print ("@@@@@@@@@@@@@@@@@@@@@@@@@@@")
##    #print(max(maxqueue))
##    #print(min(minqueue))
##    maxValue=max(maxqueue)-500
##    minValue=min(minqueue)
##    ff=np.array(b)
##    fff=(ff-minValue)/(maxValue-minValue)
##    #print(fff)
##    im=Image.fromarray(fff)
##    img = im.resize((32, 32))
##    print ("@@@@@@@@@@@@@@@@@@@@@@@@@@@")
##    matrix = np.asarray(img) 
##    print(matrix)
#    
#def curb1():
#    global existflag,second_x,second_y,l,first_x,first_y,filename,i,big,d,e,m5,small,path
#    save3();
#    matrix1=[]
#    matrix2=[]
#    maxqueue=[]
#    minqueue=[]
#    for i1 in range(1,big+1):
#        if(i1<10 and small==1 and smallflag==0):
#            f=d+'_'+"0"+str((i1+small-1))+e
#        elif(i1<10 and small==1 and smallflag==1):
#            f=d+'_'+"00"+str((i1+small-1))+e
#        elif((i1+small-1)<100 and  small==1 and smallflag==1):
#            f=d+'_'+"0"+str((i1+small-1))+e
#        elif((i1+small-1)<100 and small>1):
#            f=d+'_'+"0"+str((i1+small-1))+e
#        else:
#            f=d+'_'+str((i1+small-1))+e
#        filename1=path+"\\\\"+f
#        img_array=loadFile(filename1)
#        a = np.matrix(img_array)
#        #a=haress(s2.get(),s3.get(),a)
#        if(first_x<second_x and first_y<second_y):
#            b=a[first_y:second_y,first_x:second_x]
#        if(second_x<first_x and first_y<second_y):
#            b=a[first_y:second_y,second_x:first_x]
#        if(second_x<first_x and second_y<first_y):
#            b=a[second_y:first_y,second_x:first_x]
#        if(first_x<second_x and second_y<first_y):
#            b=a[second_y:first_y,first_x:second_x]
#        maxqueue.append(b.max())
#        minqueue.append(b.min())
#    if(i>=2 and i<=(big-2)):
#        for i2 in range(i-2,i+3):
#            if(i2<10 and small==1 and smallflag==0):
#                f=d+'_'+"0"+str((i2+small-1))+e
#            elif(i2<10 and small==1 and smallflag==1):
#                f=d+'_'+"00"+str((i2+small-1))+e
#            elif((i2+small-1)<100 and  small==1 and smallflag==1):
#                f=d+'_'+"0"+str((i2+small-1))+e
#            elif((i2+small-1)<100 and small>1):
#                f=d+'_'+"0"+str((i2+small-1))+e
#            else:
#                f=d+'_'+str((i2+small-1))+e
#            filename1=path+"\\\\"+f
#            img_array=loadFile(filename1)
#            a = np.matrix(img_array)
#            #a=haress(s2.get(),s3.get(),a)
#            if(first_x<second_x and first_y<second_y):
#                b=a[first_y:second_y,first_x:second_x]
#            if(second_x<first_x and first_y<second_y):
#                b=a[first_y:second_y,second_x:first_x]
#            if(second_x<first_x and second_y<first_y):
#                b=a[second_y:first_y,second_x:first_x]
#            if(first_x<second_x and second_y<first_y):
#                b=a[second_y:first_y,first_x:second_x]
#            matrix1.append(b)
#
#    #print(max(maxqueue))
#    #print(min(minqueue))
#    maxValue=max(maxqueue)-100
#    minValue=min(minqueue)
#    fff=np.matrix([])
#    for ff1 in range(0,len(matrix1)):
#        ff=np.array(matrix1[ff1])
#        fff=(ff-minValue)/(maxValue-minValue)
##        im=Image.fromarray(fff)
##        img = im.resize((32, 32))    
##        matrix = np.asarray(img)
##        matrix1[ff1]=matrix
#        
#        im1=Image.fromarray(fff)
#        img = im1.resize((32,32))
#        fff1=np.asarray(img)
#        
#        matrix = fff1
#        matrix1[ff1]=matrix
#
#    m0=np.matrix([])
#    m1=np.matrix([])
#    m2=np.matrix([])
#    m3=np.matrix([])
#    m4=np.matrix([])
#    m5=np.matrix([])
#    m0=matrix1[0]
#    m1=matrix1[1]
#    m2=matrix1[2]
#    m3=matrix1[3]
#    m4=matrix1[4]
#    m5=np.dstack((m0,m1))
#    m5=np.dstack((m5,m2))
#    m5=np.dstack((m5,m3))
#    m5=np.dstack((m5,m4))
#    predict3d()
#def predict(matrix1):
#    matrix=np.matrix(matrix1)
#    base_model = model_from_json(open('A_1_architecture.json').read())  
#    base_model.load_weights('A_1_weights.h5')
#    pred_test = base_model.predict(matrix.reshape(1,32,32,1))
#    print (pred_test[0])   
##    name_list = ['分化1','分化2','分化3']
##    num_list = pred_test[0]
##    plt.bar(range(len(num_list)), num_list,color='rgb',tick_label=name_list)
#    source_data = {'分化1': pred_test[0][0], '分化2': pred_test[0][1], '分化3': pred_test[0][2]}  # 设置原始数据
#
#    for a, b in source_data.items():
#        plt.text(a, b + 0.05, '%.3f' % b, ha='center', va='bottom', fontsize=11)  # ha 文字指定在柱体中间， va指定文字位置 fontsize指定文字体大小
#
## 设置X轴Y轴数据，两者都可以是list或者tuple
#    x_axis = tuple(source_data.keys())
#    y_axis = tuple(source_data.values())
#    plt.bar(x_axis, y_axis, color='rgb')  # 如果不指定color，所有的柱体都会是一个颜色
#
#    plt.xlabel(u"分化种类")  # 指定x轴描述信息
#    plt.ylabel(u"概率值")  # 指定y轴描述信息
#    plt.title("肿瘤分化种类概率")  # 指定图表描述信息
#    plt.ylim(0, 1.19)  # 指定Y轴的高度
#    plt.savefig('scores_par.png')
#    plt.show()
#    my_img = Image.PhotoImage(file='scores_par.png')
#    l1.delete("all")
#    l1.create_image(256,256,image =my_img)
#    root.mainloop()
#
#
#def predict3d():
#    global l1,dicom1,root
#    base_model = model_from_json(open('F5_1_architecture.json').read())  
#    base_model.load_weights('F5_1_weights.h5')
#
#    pred_test = base_model.predict(m5.reshape(1,32,32,5,1))
#    print (pred_test[0])
##    name_list = ['分化1','分化2','分化3']  
##    num_list = pred_test[0]
##    plt.bar(range(len(num_list)), num_list,color='rgb',tick_label=name_list)
#    source_data = {'分化1': pred_test[0][0], '分化2': pred_test[0][1], '分化3': pred_test[0][2]}  # 设置原始数据
#
#    for a, b in source_data.items():
#        plt.text(a, b + 0.05, '%.3f' % b, ha='center', va='bottom', fontsize=11)  # ha 文字指定在柱体中间， va指定文字位置 fontsize指定文字体大小
#
## 设置X轴Y轴数据，两者都可以是list或者tuple
#    x_axis = tuple(source_data.keys())
#    y_axis = tuple(source_data.values())
#    plt.bar(x_axis, y_axis, color='rgb')  # 如果不指定color，所有的柱体都会是一个颜色
#
#    plt.xlabel(u"分化种类")  # 指定x轴描述信息
#    plt.ylabel(u"概率值")  # 指定y轴描述信息
#    plt.title("肿瘤分化种类概率")  # 指定图表描述信息
#    plt.ylim(0, 1.19)  # 指定Y轴的高度
#    
#    
#    
#    plt.savefig('scores_par.png')
#    plt.show()
#    my_img = Image.PhotoImage(file='scores_par.png')
#    l1.delete("all")
#    l1.create_image(256,256,image =my_img)
#    root.mainloop()
def predict3dp():
    global filename,l1,i,big,m10,m11,m12,m13,m14,path
    
#    print(filename)
    
#    rule_name = r'^(.+)[E-I]'
#    compile_name = re.compile(rule_name, re.M)
#    res_name = compile_name.findall(filename)
#    #print (res_name[0])
#    filenameeum=[]
#    filenameeum.append(res_name[0]+'E 9-1')
#    filenameeum.append(res_name[0]+'F 9-2')
#    filenameeum.append(res_name[0]+'G 9-3')
#    filenameeum.append(res_name[0]+'H 9-4')
#    filenameeum.append(res_name[0]+'I 9-5')
#    
#    
#    rule_name = r'[E-I](.+)_'
#    compile_name = re.compile(rule_name, re.M)
#    res_name = compile_name.findall(filename)
#    rule_name = r'\\(.+)$'
#    compile_name = re.compile(rule_name, re.M)
#    res_name1 = compile_name.findall(res_name[0])
#    part1=res_name1[0]
    
#    print (res_name1[0])
    findlist1=[]#储存选中的五张图片在EFGHI中的路径
    findlist2=[]
    findlist3=[]
    findlist4=[]
    findlist5=[]
    
    findlist6=[]#储存选中的EFGHI的路径用于计算max和min
    findlist7=[]
    findlist8=[]
    findlist9=[]
    findlist10=[]
#    for i1 in range(i-2,i+3):
#        if(i1<10):
#            findlist1.append(filenameeum[0]+'\\'+part1+'_00'+str(i1)+'.dcm')
#        elif(i1>=10 and i1<100):
#            findlist1.append(filenameeum[0]+'\\'+part1+'_0'+str(i1)+'.dcm')
#        else:
#            findlist1.append(filenameeum[0]+'\\'+part1+'_'+str(i1)+'.dcm')
#    for i1 in range(i-2,i+3):
#        if(i1+big<10):
#            findlist2.append(filenameeum[1]+'\\'+part1+'_00'+str(i1+big)+'.dcm')
#        elif(i1+big>=10 and i1+big<100):
#            findlist2.append(filenameeum[1]+'\\'+part1+'_0'+str(i1+big)+'.dcm')
#        else:
#            findlist2.append(filenameeum[1]+'\\'+part1+'_'+str(i1+big)+'.dcm')
#    for i1 in range(i-2,i+3):
#        if(i1+big*2<10):
#            findlist3.append(filenameeum[2]+'\\'+part1+'_00'+str(i1+big*2)+'.dcm')
#        elif(i1+big*2>=10 and i1+big*2<100):
#            findlist3.append(filenameeum[2]+'\\'+part1+'_0'+str(i1+big*2)+'.dcm')
#        else:
#            findlist3.append(filenameeum[2]+'\\'+part1+'_'+str(i1+big*2)+'.dcm')
#    for i1 in range(i-2,i+3):
#        if(i1+big*3<10):
#            findlist4.append(filenameeum[3]+'\\'+part1+'_00'+str(i1+big*3)+'.dcm')
#        elif(i1+big*3>=10 and i1+big*3<100):
#            findlist4.append(filenameeum[3]+'\\'+part1+'_0'+str(i1+big*3)+'.dcm')
#        else:
#            findlist4.append(filenameeum[3]+'\\'+part1+'_'+str(i1+big*3)+'.dcm')
#    for i1 in range(i-2,i+3):
#        if(i1+big*4<10):
#            findlist5.append(filenameeum[4]+'\\'+part1+'_00'+str(i1+big*4)+'.dcm')
#        elif(i1+big*4>=10 and i1+big*4<100):
#            findlist5.append(filenameeum[4]+'\\'+part1+'_0'+str(i1+big*4)+'.dcm')
#        else:
#            findlist5.append(filenameeum[4]+'\\'+part1+'_'+str(i1+big*4)+'.dcm')
    
    parent_path=os.path.dirname(path)
    lll=os.listdir(parent_path)
    for i7 in lll:
        n3,ext=os.path.splitext(i7)
        if n3.find('E')>=0:#寻找文件夹中含特定字符的文件夹名
            path1=parent_path+'/'+i7
            result00=os.listdir(path1)
            resulttemp00=[]
            for element00 in result00:
                element00=path1+'/'+element00
                resulttemp00.append(element00)
            findlist6=resulttemp00
            for v in range(5,10):
                findlist1.append(resulttemp00[v])
        if n3.find('F')>=0:#寻找文件夹中含特定字符的文件夹名
            path1=parent_path+'/'+i7
            result00=os.listdir(path1)
            resulttemp00=[]
            for element00 in result00:
                element00=path1+'/'+element00
                resulttemp00.append(element00)
            findlist7=resulttemp00
            for v in range(5,10):
                findlist2.append(resulttemp00[v])
        if n3.find('G')>=0:#寻找文件夹中含特定字符的文件夹名
            path1=parent_path+'/'+i7
            result00=os.listdir(path1)
            resulttemp00=[]
            for element00 in result00:
                element00=path1+'/'+element00
                resulttemp00.append(element00)
            findlist8=resulttemp00
            for v in range(5,10):
                findlist3.append(resulttemp00[v])
        if n3.find('H')>=0:#寻找文件夹中含特定字符的文件夹名
            path1=parent_path+'/'+i7
            result00=os.listdir(path1)
            resulttemp00=[]
            for element00 in result00:
                element00=path1+'/'+element00
                resulttemp00.append(element00)
            findlist9=resulttemp00
            for v in range(5,10):
                findlist4.append(resulttemp00[v])
        if n3.find('I')>=0:#寻找文件夹中含特定字符的文件夹名
            path1=parent_path+'/'+i7
            result00=os.listdir(path1)
            resulttemp00=[]
            for element00 in result00:
                element00=path1+'/'+element00
                resulttemp00.append(element00)
            findlist10=resulttemp00
            for v in range(5,10):
                findlist5.append(resulttemp00[v])


#    for i1 in range(1,big+1):
#        if(i1<10):
#            findlist6.append(filenameeum[0]+'\\'+part1+'_00'+str(i1)+'.dcm')
#        elif(i1>=10 and i1<100):
#            findlist6.append(filenameeum[0]+'\\'+part1+'_0'+str(i1)+'.dcm')
#        else:
#            findlist6.append(filenameeum[0]+'\\'+part1+'_'+str(i1)+'.dcm')
#    for i1 in range(1,big+1):
#        if(i1+big<10):
#            findlist7.append(filenameeum[1]+'\\'+part1+'_00'+str(i1+big)+'.dcm')
#        elif(i1+big>=10 and i1+big<100):
#            findlist7.append(filenameeum[1]+'\\'+part1+'_0'+str(i1+big)+'.dcm')
#        else:
#            findlist7.append(filenameeum[1]+'\\'+part1+'_'+str(i1+big)+'.dcm')
#    for i1 in range(1,big+1):
#        if(i1+big*2<10):
#            findlist8.append(filenameeum[2]+'\\'+part1+'_00'+str(i1+big*2)+'.dcm')
#        elif(i1+big*2>=10 and i1+big*2<100):
#            findlist8.append(filenameeum[2]+'\\'+part1+'_0'+str(i1+big*2)+'.dcm')
#        else:
#            findlist8.append(filenameeum[2]+'\\'+part1+'_'+str(i1+big*2)+'.dcm')
#    for i1 in range(1,big+1):
#        if(i1+big*3<10):
#            findlist9.append(filenameeum[3]+'\\'+part1+'_00'+str(i1+big*3)+'.dcm')
#        elif(i1+big*3>=10 and i1+big*3<100):
#            findlist9.append(filenameeum[3]+'\\'+part1+'_0'+str(i1+big*3)+'.dcm')
#        else:
#            findlist9.append(filenameeum[3]+'\\'+part1+'_'+str(i1+big*3)+'.dcm')
#    for i1 in range(1,big+1):
#        if(i1+big*4<10):
#            findlist10.append(filenameeum[4]+'\\'+part1+'_00'+str(i1+big*4)+'.dcm')
#        elif(i1+big*4>=10 and i1+big*4<100):
#            findlist10.append(filenameeum[4]+'\\'+part1+'_0'+str(i1+big*4)+'.dcm')
#        else:
#            findlist10.append(filenameeum[4]+'\\'+part1+'_'+str(i1+big*4)+'.dcm') 
    
    maxValue=int()
    minValue=int()
    maxValue1=int()
    minValue1=int()
    maxValue2=int()
    minValue2=int()
    maxValue3=int()
    minValue3=int()
    maxValue4=int()
    minValue4=int()
    maxValue,minValue=getmaxandmin(findlist6)
    maxValue1,minValue1=getmaxandmin(findlist7)
    maxValue2,minValue2=getmaxandmin(findlist8)
    maxValue3,minValue3=getmaxandmin(findlist9)
    maxValue4,minValue4=getmaxandmin(findlist10)
    
    
    
    
    Matrix1=[]
    Matrix2=[]
    Matrix3=[]
    Matrix4=[]
    Matrix5=[]
    
    
    Matrix1=FindX(findlist1,maxValue,minValue)
    Matrix2=FindX(findlist2,maxValue1,minValue1)
    Matrix3=FindX(findlist3,maxValue2,minValue2)
    Matrix4=FindX(findlist4,maxValue3,minValue3)
    Matrix5=FindX(findlist5,maxValue4,minValue4)
#    print('done')
    
#    m1=np.array([])
#    m2=np.array([[Matrix1[0]],[Matrix1[1]],[Matrix1[2]],[Matrix1[3]],[Matrix1[4]]])
    m1=np.array(Matrix1[0])#拼成立体矩阵
    m2=np.array(Matrix1[1])
    m3=np.array(Matrix1[2])
    m4=np.array(Matrix1[3])
    m5=np.array(Matrix1[4])

    m10=np.dstack((m1,m2,m3,m4,m5))
    m1=np.array(Matrix2[0])#拼成立体矩阵
    m2=np.array(Matrix2[1])
    m3=np.array(Matrix2[2])
    m4=np.array(Matrix2[3])
    m5=np.array(Matrix2[4])

    m11=np.dstack((m1,m2,m3,m4,m5))
    m1=np.array(Matrix3[0])#拼成立体矩阵
    m2=np.array(Matrix3[1])
    m3=np.array(Matrix3[2])
    m4=np.array(Matrix3[3])
    m5=np.array(Matrix3[4])

    m12=np.dstack((m1,m2,m3,m4,m5))
    m1=np.array(Matrix4[0])#拼成立体矩阵
    m2=np.array(Matrix4[1])
    m3=np.array(Matrix4[2])
    m4=np.array(Matrix4[3])
    m5=np.array(Matrix4[4])

    m13=np.dstack((m1,m2,m3,m4,m5))
    m1=np.array(Matrix5[0])#拼成立体矩阵
    m2=np.array(Matrix5[1])
    m3=np.array(Matrix5[2])
    m4=np.array(Matrix5[3])
    m5=np.array(Matrix5[4])

    m14=np.dstack((m1,m2,m3,m4,m5))

    print('done')
#    print(findlist1[0])
#    showtest(findlist1)
    
def predict2():
    global m10,m11,m12,m13,m14
    predict3dp()
    m10=m10.reshape(1,32,32,5,1)
    m11=m11.reshape(1,32,32,5,1)
    m12=m12.reshape(1,32,32,5,1)
    m13=m13.reshape(1,32,32,5,1)
    m14=m14.reshape(1,32,32,5,1)
    num_list=[]
    num_list.append(m10)
    num_list.append(m11)
    num_list.append(m12)
    num_list.append(m13)
    num_list.append(m14)
           
    base_model = model_from_json(open('[\'E5\', \'F5\', \'G5\', \'H5\', \'I5\']ave_0_architecture.json').read())  
    base_model.load_weights('[\'E5\', \'F5\', \'G5\', \'H5\', \'I5\']ave_0_weights.h5')
    pred_test = base_model.predict(num_list)
    print (pred_test)
    
#    name_list = ['不是肿瘤','是肿瘤']  
#    num_list = pred_test[0]
#    plt.bar(range(len(num_list)), num_list,color='rgb',tick_label=name_list)  
    source_data = {'不是肿瘤': pred_test[0][0], '是肿瘤': pred_test[0][1]}  # 设置原始数据

    for a, b in source_data.items():
        plt.text(a, b + 0.05, '%.3f' % b, ha='center', va='bottom', fontsize=11)  # ha 文字指定在柱体中间， va指定文字位置 fontsize指定文字体大小

# 设置X轴Y轴数据，两者都可以是list或者tuple
    x_axis = tuple(source_data.keys())
    y_axis = tuple(source_data.values())
    plt.bar(x_axis, y_axis, color='rgb')  # 如果不指定color，所有的柱体都会是一个颜色

    plt.xlabel(u"肿瘤判断")  # 指定x轴描述信息
    plt.ylabel(u"概率值")  # 指定y轴描述信息
    plt.title("肿瘤判别概率")  # 指定图表描述信息
    plt.ylim(0, 1.19)  # 指定Y轴的高度
    
    
    
    
    plt.savefig('scores_par.png')
    plt.show()
    my_img = Image.PhotoImage(file='scores_par.png')
    l1.delete("all")
    l1.create_image(256,256,image =my_img)
    root.mainloop()
numlist=[]#装四维矩阵
def predict3():
    global m10,m11,m12,m13,m14,num_list,numlist
    predict3dp()
    num_list=[]
#    num_list.append(m10.reshape(1,32,32,5,1))
#    num_list.append(m11.reshape(1,32,32,5,1))
#    num_list.append(m12.reshape(1,32,32,5,1))
#    num_list.append(m13.reshape(1,32,32,5,1))
#    num_list.append(m14.reshape(1,32,32,5,1))
    num_list.append(m10.reshape(1,32,32,5))
    num_list.append(m11.reshape(1,32,32,5))
    num_list.append(m12.reshape(1,32,32,5))
    num_list.append(m13.reshape(1,32,32,5))
    num_list.append(m14.reshape(1,32,32,5))
    numlist=[]
    numlist=np.stack(num_list,axis=4)
    
    print("wwwwwwwww!!!!!!!!!!!!!!!!!!!!!!!!!!")
#    model = model_from_json(open('C:\\Users\\85436\\Desktop\\毕设\\keras\\Keras\\pre\\fusion_model_三分类\\[\'E5\', \'F5\', \'G5\', \'H5\', \'I5\']concat_1_architecture.json').read())  
#    model.load_weights('C:\\Users\\85436\\Desktop\\毕设\\keras\\Keras\\pre\\fusion_model_三分类\\[\'E5\', \'F5\', \'G5\', \'H5\', \'I5\']concat_1_weights.h5')
    model = model_from_json(open('[\'E5\', \'F5\', \'G5\', \'H5\', \'I5\']_1_architecture.json').read())  
    model.load_weights('[\'E5\', \'F5\', \'G5\', \'H5\', \'I5\']_1_weights.h5')
#    model.summary()
 # get the symbolic outputs of each "key" layer (we gave them unique names).
#    layer_dict = dict([(layer.name, layer) for layer in model.layers[0:]])
#    for layer in layer_dict:
#        print(layer)
   
#    base_model = model_from_json(open('C:\\Users\\85436\\Desktop\\毕设\\keras\\Keras\\pre\\fusion_model_二分类\\[\'E5\', \'F5\', \'G5\', \'H5\', \'I5\']ave_0_architecture.json').read())  
#    base_model.load_weights('C:\\Users\\85436\\Desktop\\毕设\\keras\\Keras\\pre\\fusion_model_二分类\\[\'E5\', \'F5\', \'G5\', \'H5\', \'I5\']ave_0_weights.h5')
    pred_test = model.predict(numlist)
    print (pred_test)
    
#    name_list = ['分化1','分化2','分化3']
#    num_list = pred_test[0]
#    plt.bar(range(len(num_list)), num_list,color='rgb',tick_label=name_list) 
#    
#    for i3 in range(0,3):
#        plt.text(pred_test[i3],'','%.0f', ha='center', va='bottom', fontsize=11)
#        
    source_data = {'分化1': pred_test[0][0], '分化2': pred_test[0][1], '分化3': pred_test[0][2]}  # 设置原始数据

    for a, b in source_data.items():
        plt.text(a, b + 0.05, '%.3f' % b, ha='center', va='bottom', fontsize=11)  # ha 文字指定在柱体中间， va指定文字位置 fontsize指定文字体大小

# 设置X轴Y轴数据，两者都可以是list或者tuple
    x_axis = tuple(source_data.keys())
    y_axis = tuple(source_data.values())
    plt.bar(x_axis, y_axis, color='rgb')  # 如果不指定color，所有的柱体都会是一个颜色

    plt.xlabel(u"分化种类")  # 指定x轴描述信息
    plt.ylabel(u"概率值")  # 指定y轴描述信息
    plt.title("肿瘤分化种类概率")  # 指定图表描述信息
    plt.ylim(0, 1.19)  # 指定Y轴的高度
    
    
    plt.savefig('scores_par.png')
    plt.show()
    my_img = Image.PhotoImage(file='scores_par.png')
    l1.delete("all")
    l1.create_image(256,256,image =my_img)
    
    
#    layer_name = 'conv1'
#
#    ex_model = Model(inputs=model.input, outputs=model.get_layer(layer_name).output)
#
#    #绘制图像 
#    save_map_img(layer_name, ex_model, 30, 30, 3, 6)
#
#
#    #绘制第二个卷积层特征图
#    layer_name = 'conv2'
#    ex_model = Model(inputs=model.input, outputs=model.get_layer(layer_name).output)
#
#    save_map_img(layer_name, ex_model, 12, 12, 1, 8)
##    
#    numlist=[]
#    my_img1 = PhotoImage(file='C:\\Users\\85436\\Desktop\\毕设\\keras\\Keras\\pre\\img\\conv1feature.png')
#    l1.create_image(50,100,image =my_img1)
#    my_img2 = PhotoImage(file='C:\\Users\\85436\\Desktop\\毕设\\keras\\Keras\\pre\\img\\conv2feature.png')
#    l1.create_image(80,80,image =my_img2)
    root.mainloop()
#    
def hehe():
    global filename,i,big,m10,m11,m12,m13,m14,path,second_x,second_y,first_x,first_y
    predict22(filename,i,big,m10,m11,m12,m13,m14,path,second_x,second_y,first_x,first_y)
def hehe2():
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
b10 = tk.Button(root, text='二分类',width=12,command=hehe)
b11 = tk.Button(root, text='三分类',width=12,command=hehe2)
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