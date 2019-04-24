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
def loadFile(filename):
    ds = sitk.ReadImage(filename)
    img_array = sitk.GetArrayFromImage(ds)
    frame_num,width,height=img_array.shape
    return img_array
def getmaxandmin(filelist,second_x,second_y,first_x,first_y):#获取所选区域整个文件夹所有图片该区域的灰度最大最小值
    maxqueue=[]
    minqueue=[]
    b = np.matrix([])
    for i1 in range(0,len(filelist)):
        img_array=loadFile(filelist[i1])
        a = np.matrix(img_array)
        #a=haress(s2.get(),s3.get(),a)
        if(first_x<second_x and first_y<second_y):
            b=a[first_y:second_y,first_x:second_x]
        if(second_x<first_x and first_y<second_y):
            b=a[first_y:second_y,second_x:first_x]
        if(second_x<first_x and second_y<first_y):
            b=a[second_y:first_y,second_x:first_x]
        if(first_x<second_x and second_y<first_y):
            b=a[second_y:first_y,first_x:second_x]
        maxqueue.append(b.max())
        minqueue.append(b.min())
        maxValue=max(maxqueue)-100
        minValue=min(minqueue)
    return maxValue,minValue


def FindX(findlist,maxValue,minValue,second_x,second_y,first_x,first_y):#调整矩阵大小至选取的范围，归一化并压缩成32*32
    Matrix=[]
    fff=np.matrix([])
    b=np.matrix([])
    for ff1 in range(0,5):      
        img_array=loadFile(findlist[ff1])
        a=np.matrix(img_array)
        if(first_x<second_x and first_y<second_y):
            b=a[first_y:second_y,first_x:second_x]
        if(second_x<first_x and first_y<second_y):
            b=a[first_y:second_y,second_x:first_x]
        if(second_x<first_x and second_y<first_y):
            b=a[second_y:first_y,second_x:first_x]
        if(first_x<second_x and second_y<first_y):
            b=a[second_y:first_y,first_x:second_x]
        ff=np.matrix(b)   
        fff=(ff-minValue)/(maxValue-minValue)
        ffff=np.matrix(fff)
        
        
        im1=Image.fromarray(ffff)
        img = im1.resize((32,32))
        fff1=np.asarray(img)
        matrix = fff1
        
        
        Matrix.append(matrix)
    return Matrix
def predict3dp(filename,i,big,m10,m11,m12,m13,m14,path,second_x,second_y,first_x,first_y):
    
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
    maxValue,minValue=getmaxandmin(findlist6,second_x,second_y,first_x,first_y)
    maxValue1,minValue1=getmaxandmin(findlist7,second_x,second_y,first_x,first_y)
    maxValue2,minValue2=getmaxandmin(findlist8,second_x,second_y,first_x,first_y)
    maxValue3,minValue3=getmaxandmin(findlist9,second_x,second_y,first_x,first_y)
    maxValue4,minValue4=getmaxandmin(findlist10,second_x,second_y,first_x,first_y)
    
    
    
    
    Matrix1=[]
    Matrix2=[]
    Matrix3=[]
    Matrix4=[]
    Matrix5=[]
    
    
    Matrix1=FindX(findlist1,maxValue,minValue,second_x,second_y,first_x,first_y)
    Matrix2=FindX(findlist2,maxValue1,minValue1,second_x,second_y,first_x,first_y)
    Matrix3=FindX(findlist3,maxValue2,minValue2,second_x,second_y,first_x,first_y)
    Matrix4=FindX(findlist4,maxValue3,minValue3,second_x,second_y,first_x,first_y)
    Matrix5=FindX(findlist5,maxValue4,minValue4,second_x,second_y,first_x,first_y)
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
    return m10,m11,m12,m13,m14
#    print(findlist1[0])
#    showtest(findlist1)
    
def predict22(filename,i,big,m10,m11,m12,m13,m14,path,second_x,second_y,first_x,first_y):
    m10,m11,m12,m13,m14=predict3dp(filename,i,big,m10,m11,m12,m13,m14,path,second_x,second_y,first_x,first_y)
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
 #   my_img = Image.PhotoImage(file='scores_par.png')

numlist=[]#装四维矩阵
def predict33(filename,i,big,m10,m11,m12,m13,m14,path,second_x,second_y,first_x,first_y):
    m10,m11,m12,m13,m14=predict3dp(filename,i,big,m10,m11,m12,m13,m14,path,second_x,second_y,first_x,first_y)
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
  #  my_img = Image.PhotoImage(file='scores_par.png')

    
    
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
#    
    
           
#    img_array=loadFile(findlist1[0])
#    a = np.matrix(img_array)
#    a=haress(s2.get(),s3.get(),a)
#    im=Image.fromarray(a)
#    tkimg=ImageTk.PhotoImage(im)
#    l1.delete("all")
#    l1.create_image(256,256,image =tkimg)
#    root.mainloop()