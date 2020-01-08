from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from apscheduler.schedulers.background import BackgroundScheduler
#sudo pip3 install apscheduler
from os import getcwd
import tensorflow as tf
from scipy import misc
import cv2
import matplotlib.pyplot as plt
import numpy as np
import argparse
import facenet
import detect_face
import os
from os.path import join as pjoin
import sys
import time
import copy
import math
import pickle
from sklearn.svm import SVC
from sklearn.externals import joblib
import serial
import time
import threading
import tkinter
from tkinter import Tk, Label, Entry, Radiobutton, IntVar
import datetime,re
from multiprocessing import Process, Pipe
import queue
import chardet
#update release 2019/12/23 更新gui為同一份code,整合成兩個threading
#update release 2019/12/24 更新清除登入門禁人物資訊

reading='stranger'
predictionMax=0.73
predictionMin=0.60
setFailLimit=0.67
successNum=2
failNum=5
strangerNum=11
passRate=1

q = queue.Queue(maxsize = 1)
ser = serial.Serial('/dev/ttyS3', 115200) 
ser.write( 'set_0'.encode('utf-8') + str(successNum).encode('utf-8')+'_'.encode('utf-8')+str(strangerNum).encode('utf-8')+'_0'.encode('utf-8')+str(failNum).encode('utf-8')+'_'.encode('utf-8')+str(int(predictionMax*1000)).encode('utf-8')+'_'.encode('utf-8')+str(int(setFailLimit*1000)).encode('utf-8')+'_'.encode('utf-8')+str(passRate*100).encode('utf-8')+'\r\n'.encode('utf-8'))
print('[Set System] (Success Limit): %s (Stranger Limit): %s (Fail Limit): %s (Prediction Max): %s (Prediction Min): %s (Set Fail Limit): %s (Pass Rate): %s \n'%(str(successNum) ,str(strangerNum) ,str(failNum) ,str(predictionMax) ,str(predictionMin) ,str(setFailLimit) ,str(passRate) ) )
#set_success筆數_stranger筆數_fail筆數_辨識度上限_辨識度下限_打折率\r\n



def frameflesh():

    with tf.Graph().as_default():
        gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.9)
        sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
        with sess.as_default():
            
            pnet, rnet, onet = detect_face.create_mtcnn(sess, '.')
    
            minsize = 80  # minimum size of face
            threshold = [0.6, 0.7, 0.7]  # three steps's threshold
            factor = 0.709  # scale factor
            #factor = 0.709  # scale factor
            margin = 44
            #margin = 44
            frame_interval = 3
            batch_size = 1000
            image_size = 182
            input_image_size = 170
    
            #train human name
            HumanNames =read_train_object()
            print (str(HumanNames))
    
            print('Loading feature extraction model')
            
            modeldir = '/home/vincent/facenet/models/20180402-114759/20180402-114759.pb'
            #modeldir = '/home/vincent/facenet/models/20180408-102900/20180408-102900.pb'
            facenet.load_model(modeldir)
    
            images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
            embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
            
            phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
            embedding_size = embeddings.get_shape()[1]
    
            classifier_filename = '/home/vincent/facenet/models/my_classifier.pkl'
            classifier_filename_exp = os.path.expanduser(classifier_filename)
            with open(classifier_filename_exp, 'rb') as infile:
                (model, class_names) = pickle.load(infile)
                print('load classifier file-> %s' % classifier_filename_exp)
    
            video_capture = cv2.VideoCapture(0)
            video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            c = 0
    
            # #video writer
            # fourcc = cv2.VideoWriter_fourcc(*'DIVX')
            # out = cv2.VideoWriter('3F_0726.avi', fourcc, fps=30, frameSize=(640,480))
    
            print('Start Recognition!')
            prevTime = 0
            #ser.open()
    
            #while not q.empty():
                #reading=q.get()
                #updategui(reading)
                
    
            while True:
                
                #reading=q.get()
                #updategui(reading)            
                #data =recv(ser) 
                
                ret, frame = video_capture.read()
    
                # frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)    #resize frame (optional)
    
                curTime = time.time()    # calc fps
                timeF = frame_interval # = 3
    
                if (c % timeF == 0):
                    find_results = []
    
                    # if 2dim img then cvt to rgb
                    if frame.ndim == 2:
                        frame = facenet.to_rgb(frame)
                    frame = frame[:, :, 0:3]
                   
                    bounding_boxes, _ = detect_face.detect_face(frame, minsize, pnet, rnet, onet, threshold, factor)
                    
                    nrof_faces = bounding_boxes.shape[0]
                    
                    print('Number of Faces are detected: {}'.format(nrof_faces))
                    if nrof_faces==0:
                        #print (ser.portstr)
                        ser.write('ready\r\n'.encode('utf-8'))
                        #self.textCtrl1.Value = ser.read(5)
                    if nrof_faces > 0:
                        det = bounding_boxes[:, 0:4]
                        
                        img_size = np.asarray(frame.shape)[0:2]
    
                        cropped = []
                        scaled = []
                        scaled_reshape = []
                        bb = np.zeros((nrof_faces,4), dtype=np.int32)
    
                        for i in range(nrof_faces):
                            emb_array = np.zeros((1, embedding_size))
    
                            bb[i][0] = det[i][0]
                            bb[i][1] = det[i][1]
                            bb[i][2] = det[i][2]
                            bb[i][3] = det[i][3]
    
                            # inner exception
                            if bb[i][0] <= 0 or bb[i][1] <= 0 or bb[i][2] >= len(frame[0]) or bb[i][3] >= len(frame):
                                print('face is inner of range!')
                                continue
    
                            cropped.append(frame[bb[i][1]:bb[i][3], bb[i][0]:bb[i][2], :])
                            try:
                                cropped[i] = facenet.flip(cropped[i], False)
                                scaled.append(misc.imresize(cropped[i], (image_size, image_size), interp='bilinear'))
                                
                                scaled[i] = cv2.resize(scaled[i], (input_image_size,input_image_size),
                                                       interpolation=cv2.INTER_CUBIC)
                                scaled[i] = facenet.prewhiten(scaled[i])
                                scaled_reshape.append(scaled[i].reshape(-1,input_image_size,input_image_size,3))
                                feed_dict = {images_placeholder: scaled_reshape[i], phase_train_placeholder: False}
                               
                                emb_array[0, :] = sess.run(embeddings, feed_dict=feed_dict)
                              
                                predictions = model.predict_proba(emb_array)
                                best_class_indices = np.argmax(predictions, axis=1)
                                best_class_probabilities = predictions[np.arange(len(best_class_indices)), best_class_indices]
                                
        
                                #plot result idx under box
                                text_x = bb[i][0]
                                text_y = bb[i][3] + 20
    
    
                                if np.max(predictions[0]) > predictionMax  :
                                    put_text = '{name} {confidence: 3.2f}'.format(name = HumanNames[best_class_indices[0]], confidence = (np.max(predictions[0]).tolist())*100)
                                    #gonumber=int((np.max(predictions[0]).tolist())*1000)
                                    #print(gonumber)
                                    ser.write( 'success_'.encode('utf-8')+str(int((np.max(predictions[0]).tolist())*1000)).encode('utf-8')+'_'.encode('utf-8')+HumanNames[best_class_indices[0]].encode('utf-8')+'\r\n'.encode('utf-8') )
                                    reading= 'success_'.encode('utf-8')+str(int((np.max(predictions[0]).tolist())*1000)).encode('utf-8')+'_'.encode('utf-8')+HumanNames[best_class_indices[0]].encode('utf-8')+'\r\n'.encode('utf-8')
                                    cv2.rectangle(frame, (bb[i][0], bb[i][1]), (bb[i][2], bb[i][3]), (225, 225, 0), 2)    #boxing face
                                    cv2.putText(frame, put_text, (text_x, text_y), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                                1, (225, 225, 0), thickness=2, lineType=2)
                                    #confidence111=' {confidence: 3.2f}'.format(confidence = (np.max(predictions[0]).tolist())*100)
                                    print('Identification pass by name: %s'%(HumanNames[best_class_indices[0]])+'  confidence:' + str(np.max(predictions[0]).tolist()) ) 
                                    #x = datetime.datetime.now()
                                    #print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) 
                                    historyFull(HumanNames[best_class_indices[0]] ,int((np.max(predictions[0]).tolist())*100) )
                                    #reading=HumanNames[best_class_indices[0]] ,int((np.max(predictions[0]).tolist())*100) 
                                    #reading(ser)
                                    #updategui(reading)
                                elif np.max(predictions[0]) < predictionMax and np.max(predictions[0]) > predictionMin and HumanNames[best_class_indices[0]]:
                                    put_text = '{name} {confidence: 3.2f}'.format(name = HumanNames[best_class_indices[0]], confidence = (np.max(predictions[0]).tolist())*100)
                                    #gonumber1=int((np.max(predictions[0]).tolist())*1000)
                                    cv2.rectangle(frame, (bb[i][0], bb[i][1]), (bb[i][2], bb[i][3]), (225, 0, 255), 2)    #boxing face
                                    cv2.putText(frame, put_text, (text_x, text_y), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                                1, (225, 0, 255), thickness=2, lineType=2)                                   
                                    ser.write( 'fail_'.encode('utf-8')+str(int((np.max(predictions[0]).tolist())*1000)).encode('utf-8')+'_'.encode('utf-8')+HumanNames[best_class_indices[0]].encode('utf-8')+'\r\n'.encode('utf-8') )
                                    #reading= 'fail_'.encode('utf-8')+str(int((np.max(predictions[0]).tolist())*1000)).encode('utf-8')+'_'.encode('utf-8')+HumanNames[best_class_indices[0]].encode('utf-8')+'\r\n'.encode('utf-8')
                                    historyFull(HumanNames[best_class_indices[0]] ,int((np.max(predictions[0]).tolist())*100) )
                                    #reading(ser)
                                    #updategui(reading)
                                else:
                                    put_text = 'Stranger'
                                    cv2.rectangle(frame, (bb[i][0], bb[i][1]), (bb[i][2], bb[i][3]), (0, 225, 255), 2)    #boxing face
                                    cv2.putText(frame, put_text, (text_x, text_y), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                                1, (0, 225, 255), thickness=2, lineType=2)                                  
                                    historyFull(put_text ,put_text )
                                    ser.write('stranger\r\n'.encode('utf-8'))
                                    reading= 'stranger\r\n'.encode('utf-8')
                                    #updategui(reading)
                                #cv2.putText(frame, put_text, (text_x, text_y), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                            #1, (25, i*125, 25), thickness=2, lineType=2)                    
                                    #reading(ser)
                            except IndexError :
                                print("Oh No! IndexError : list index out of range for multi-faces")                        
    
    
                    else:
                        print('Unable to align')
                
    
                sec = curTime - prevTime
                prevTime = curTime
                fps = 1 / (sec)
                str1 = 'FPS: %2.3f' % fps
                text_fps_x = len(frame[0]) - 150
                text_fps_y = 20
                cv2.putText(frame, str1, (text_fps_x, text_fps_y),
                            cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0), thickness=1, lineType=2)
                # c+=1
                cv2.imshow('Video', frame)
    
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    
            video_capture.release()
            # #video writer
            # out.release()
            cv2.destroyAllWindows()


def recordfile(dataframe):
    hhq=open(dataframe, 'r')  
    lines = hhq.readlines() 
    last_line = lines[-1]      
    return last_line



#def read_from_port():
    #while True:
        #full = ser.readline()
        ##print('full: ',full)
        #historyFull_setting(str(full))
        #q.put(full)
    
#def read_from_port1():
    ##while True:
    #full = ser.readline()
    ##print('full: ',full)
    ##historyFull_setting(str(full))



def month_and_day():
    x = datetime.datetime.now()
    
    # x.month=10
    if x.month<10 and x.month>=1:
        month='0'+str(x.month)
        #print (month)
    else :
        month=str(x.month)
    if x.day<10 and x.day>=1:
        day='0'+str(x.day)
        #print (day)
    else:
        day=str(x.day)  
    year=str(x.year)
    return year+month+day

   


def historyIdentification(name,confidence):
    date=month_and_day()
    xtime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    chineseNow = open('/home/vincent/facenet/models/'+date+'-Identification','a')
    
    chineseNow.write(name+'@'+confidence+'@'+xtime+'\n')
    chineseNow.close    

def historyFull_setting(setting):
    date=month_and_day()
    xtime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    chineseNow = open('/home/vincent/facenet/models/'+date+'-Full','a')
    
    chineseNow.write(setting+'\n')
    
    chineseNow.close   

def historyFull(name,confidence):
    date=month_and_day()
    xtime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    chineseNow = open('/home/vincent/facenet/models/'+date+'-Full','a')
    
    chineseNow.write(name+'@'+str(confidence)+'@'+xtime+'\n')
    chineseNow.close    

def read_name():
    try:
        detect_path = '/home/vincent/facenet/models/name.txt'
        detectfile1=open(detect_path,'r')
        lines = detectfile1.readlines() #讀取所有行
        if 0==len(lines):
            write_name('unknow')
            lines='unknow'
        lines1=lines[-1].strip('\n')
        detectfile1.close
        return lines1
    except:
        print('error: please mk file "facenet/models/name.txt". ') 


def read_train_object():
    train_name = open('/home/vincent/facenet/models/name.txt','r') 
    
    lines = train_name.readlines()
    count=0
    for a in lines:
        b=a.split('\n')
        lines[count]=b[0]
        count += 1
    train_name.close
    return lines

def alert_time():
    timefile=open('/home/vincent/facenet/models/time.txt','r')
    lines = timefile.readlines()
    count=0
    for a in lines:
        b=a.split('\n')
        lines[count]=b[0]
        count += 1
    timefile.close
    return lines


def settime(hours_t,min_t):
    scheduler = BackgroundScheduler()
    scheduler.add_job(restart, 'cron', hour=hours_t, minute=min_t)
    scheduler.start()

def restart():
    os.system("sudo reboot")
    
    
def reflesh():

    time.sleep(2)
    firstLabel = Label(mainWin, text='辨識中..' ,font=('Arial',50) )        
    successLabel = Label(mainWin, text="門禁限制",font=('Arial',50),fg="#DC143C" )
    
    resultLabel = Label(mainWin, text="辨識身份",font=('Arial',50))
    personLabel = Label(mainWin,  text='                 ',font=('Arial',50),fg="#9400D3" )
    
    pdLabel = Label(mainWin, text="部門為",font=('Arial',50))
    pdresultLabel = Label(mainWin,  text='                 ',font=('Arial',50),fg="#9400D3" )        
    firstLabel.grid(row=1,column=0, sticky='w')
    successLabel.grid(row=1,column=1, sticky='w')
    resultLabel.grid(row=2,column=0, sticky='w')
    personLabel.grid(row=2,column=1, sticky='w')
    pdLabel.grid(row=3,column=0, sticky='w')
    pdresultLabel.grid(row=3,column=1, sticky='w') 
    mainWin.update()     



#os.system("sudo ln -sf /dev/ttyACM0 /dev/ttyS3")
print ('set : train and timer')
#time.sleep(1)
set_time=alert_time()
hours_t=int(set_time[0])
min_t=int(set_time[1])
print('initialization set timer: '+str(hours_t)+':'+str(min_t) )
#time.sleep(1)
print ('start system....')    
settime(hours_t,min_t)
print('Creating networks and loading parameters')
historyFull_setting('[Set System] (Success Limit): '+ str(successNum)  + ' (Stranger Limit): '+ str(strangerNum)+ ' (Fail Limit): '+ str(failNum) + ' (Prediction Max): '+ str(predictionMax) + ' (Prediction Min): '+ str(predictionMin) + ' (Set Fail Limit): '+ str(setFailLimit) + ' (Pass Rate): '+ str(passRate))

#建立子程序
ts=threading.Thread(target=frameflesh,args=())
ts.start()

today=month_and_day()
print(today)
dataframe = '/home/vincent/facenet/models/'+today+'-Full'
print(dataframe)
# 步驟二：建立主視窗。
mainWin = Tk()
#var = IntVar()
operation = [ '+', '-', '*', '/']

# 視窗標題
mainWin.title("face-gui")
# 視窗大小
mainWin.geometry("640x280")

# 步驟三：建立視窗控制項元件。
# 建立標籤

#var1 = tkinter.StringVar()
#a1='辨識中..'
#var1.set(a1)


allname=read_train_object()
print(allname)
name123=[]
number123=[]
pd123=[]
for a in allname:
    print(a)
    all_23=a.split("_")
    print(all_23)
    number15=all_23[0]
    name15=all_23[1]
    pd15=all_23[2]
    number123.append(number15)
    name123.append(name15)
    pd123.append(pd15)
    
print(name123)
print(number123)
print(pd123)

persenID = dict(zip(number123, name123))
pdID = dict(zip(number123, pd123))
print(persenID)
print(pdID)


firstLabel = Label(mainWin, text='辨識中..' ,font=('Arial',50) )        
successLabel = Label(mainWin, text="門禁限制",font=('Arial',50),fg="#DC143C" )

resultLabel = Label(mainWin, text="辨識身份",font=('Arial',50))
personLabel = Label(mainWin,  text='                 ',font=('Arial',50),fg="#9400D3" )

pdLabel = Label(mainWin, text="部門為",font=('Arial',50))
pdresultLabel = Label(mainWin,  text='                 ',font=('Arial',50),fg="#9400D3" )        
 
firstLabel.grid(row=1,column=0, sticky='w')
successLabel.grid(row=1,column=1, sticky='w')
resultLabel.grid(row=2,column=0, sticky='w')
personLabel.grid(row=2,column=1, sticky='w')
pdLabel.grid(row=3,column=0, sticky='w')
pdresultLabel.grid(row=3,column=1, sticky='w') 
mainWin.update() 

while True:


    reading = ser.readline()
    historyFull_setting(str(reading))        
    encode_type = chardet.detect(reading)  
    reading = reading.decode(encode_type['encoding']) 
    print('reading : ',reading)
    #https://blog.csdn.net/jieli_/article/details/70166244
    #mainWin.after(20)  
          
    if re.findall("Open", reading) or re.findall("Pass", reading) :
        

        
        print(reading)
        strangercount=re.findall("Stranger:+[0-9]+[0-9]", reading)
        strangercount1=strangercount[0].split(":")
        print(strangercount1)
        
        if re.findall("Open", reading):
            
            print(re.findall("ID:+[0-9]+[0-9]", reading) )
            idd=re.findall("ID:+[0-9]+[0-9]", reading)
            print(idd)
            iddd=idd[0].split(":")
            realID=iddd[1]

            person = tkinter.StringVar()
            person.set(persenID[realID]+'                            ')

            pd = tkinter.StringVar()
            pd.set('DP '+pdID[realID]+'             ')       

            firstLabel = Label(mainWin, text='辨識中..',font=('Arial',50) )        
            successLabel = Label(mainWin,text="辨識成功",font=('Arial',50),fg="#40E0D0" )

            resultLabel = Label(mainWin, text="辨識身份",font=('Arial',50))
            personLabel = Label(mainWin,  textvariable=person,font=('Arial',50),fg="#9400D3" )

            pdLabel = Label(mainWin, text="部門為",font=('Arial',50))
            pdresultLabel = Label(mainWin,  textvariable=pd,font=('Arial',50),fg="#9400D3" )
   
            
            firstLabel.grid(row=1,column=0, sticky='w')
            successLabel.grid(row=1,column=1, sticky='w')
            resultLabel.grid(row=2,column=0, sticky='w')
            personLabel.grid(row=2,column=1, sticky='w')
            pdLabel.grid(row=3,column=0, sticky='w')
            pdresultLabel.grid(row=3,column=1, sticky='w') 
            mainWin.update() 
            reflesh()

        #elif re.findall("Pass", autosave) and int(strangercount1[1])<=8:
            #print(re.findall("ID:+[0-9]+[0-9]", reading) )
            #idd=re.findall("ID:+[0-9]+[0-9]", reading)
            #print(idd)
            #iddd=idd[0].split(":")
            #realID=iddd[1]

            #person = tkinter.StringVar()
            #person.set(persenID[realID]+'                            ')

            #pd = tkinter.StringVar()
            #pd.set('DP '+pdID[realID]+'             ')       

            #firstLabel = Label(mainWin, text='辨識中..' ,font=('Arial',50) )        
            #successLabel = Label(mainWin, text="辨識失敗",font=('Arial',50),fg="#DC143C" )

            #resultLabel = Label(mainWin, text="辨識身份",font=('Arial',50))
            #personLabel = Label(mainWin,  text="             ",font=('Arial',50),fg="#9400D3" )

            #pdLabel = Label(mainWin, text="提醒          ",font=('Arial',50),fg="#DC143C")
            #pdresultLabel = Label(mainWin, text="請勿兩人同時辨識",font=('Arial',28),fg="#9400D3" )
        
        elif re.findall("Pass", reading) and int(strangercount1[1])>=8  :
            firstLabel = Label(mainWin, text='辨識中..' ,font=('Arial',50) )        
            successLabel = Label(mainWin, text="門禁限制",font=('Arial',50),fg="#DC143C" )

            resultLabel = Label(mainWin, text="辨識身份",font=('Arial',50))
            personLabel = Label(mainWin,  text="陌生人     ",font=('Arial',50),fg="#9400D3" )

            pdLabel = Label(mainWin, text="提醒    ",font=('Arial',50),fg="#DC143C")
            pdresultLabel = Label(mainWin,  text="請看鏡頭重新辨識",font=('Arial',28),fg="#9400D3" )
            firstLabel.grid(row=1,column=0, sticky='w')
            successLabel.grid(row=1,column=1, sticky='w')
            resultLabel.grid(row=2,column=0, sticky='w')
            personLabel.grid(row=2,column=1, sticky='w')
            pdLabel.grid(row=3,column=0, sticky='w')
            pdresultLabel.grid(row=3,column=1, sticky='w') 
            mainWin.update()   





