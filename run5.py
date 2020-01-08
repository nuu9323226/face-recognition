from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

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
import datetime
predictionMax=0.73
predictionMin=0.60

ser = serial.Serial('/dev/ttyS3', 115200) 

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



def historyFull(name,confidence):
    date=month_and_day()
    xtime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    chineseNow = open('/home/vincent/facenet/models/'+date+'-Full','a')
    
    chineseNow.write(name+'@'+confidence+'@'+xtime+'\n')
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


def recv(serial):    
    while True:    
        data =serial.read(11)  
        print(data)
        if data == '': 
            #print(data)
            continue  
        else:  
            break  
        #sleep(0.02)   
    return data    

print('Creating networks and loading parameters')



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
        while True:
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
                                ser.write('success\r\n'.encode('utf-8'))
                                cv2.rectangle(frame, (bb[i][0], bb[i][1]), (bb[i][2], bb[i][3]), (225, 225, 0), 2)    #boxing face
                                cv2.putText(frame, put_text, (text_x, text_y), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                            1, (225, 225, 0), thickness=2, lineType=2)
                                confidence111=' {confidence: 3.2f}'.format(confidence = (np.max(predictions[0]).tolist())*100)
                                print('Identification pass by name: %s'%(HumanNames[best_class_indices[0]])+'  confidence:' + confidence111 )
                                x = datetime.datetime.now()
                                print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                
                                #historyIdentification(HumanNames[best_class_indices[0]] ,confidence111 )
                                historyFull(HumanNames[best_class_indices[0]] ,confidence111 )
                                print(x)
                                
                            elif np.max(predictions[0]) < predictionMax and np.max(predictions[0]) > predictionMin and HumanNames[best_class_indices[0]]:
                                put_text = '{name} {confidence: 3.2f}'.format(name = HumanNames[best_class_indices[0]], confidence = (np.max(predictions[0]).tolist())*100)
                                
                                cv2.rectangle(frame, (bb[i][0], bb[i][1]), (bb[i][2], bb[i][3]), (225, 0, 255), 2)    #boxing face
                                cv2.putText(frame, put_text, (text_x, text_y), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                            1, (225, 0, 255), thickness=2, lineType=2)                                   
                                ser.write('fail\r\n'.encode('utf-8'))
                                confidence222=' {confidence: 3.2f}'.format(confidence = (np.max(predictions[0]).tolist())*100)
                                historyFull(HumanNames[best_class_indices[0]] ,confidence222 )
            
                            else:
                                put_text = 'Stranger'
                                cv2.rectangle(frame, (bb[i][0], bb[i][1]), (bb[i][2], bb[i][3]), (0, 225, 255), 2)    #boxing face
                                cv2.putText(frame, put_text, (text_x, text_y), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                            1, (0, 225, 255), thickness=2, lineType=2)                                  
                                historyFull(put_text ,put_text )
                                ser.write('stranger\r\n'.encode('utf-8'))
                            #cv2.putText(frame, put_text, (text_x, text_y), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                        #1, (25, i*125, 25), thickness=2, lineType=2)                    
                            
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
