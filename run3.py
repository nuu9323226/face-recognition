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


ser = serial.Serial('/dev/ttyS3', 115200) 


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
    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.6)
    sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
    with sess.as_default():
        
        pnet, rnet, onet = detect_face.create_mtcnn(sess, '.')

        minsize = 20  # minimum size of face
        threshold = [0.6, 0.7, 0.7]  # three steps's threshold
        factor = 0.709  # scale factor
        margin = 44
        frame_interval = 3
        batch_size = 1000
        image_size = 182
        input_image_size = 160

        #train human name
        HumanNames = ['Allen','Bryan','David','Diego','Forbes','Forbes_Noglass','Kelin','Mark','Sam','Vincent']
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
                            cv2.rectangle(frame, (bb[i][0], bb[i][1]), (bb[i][2], bb[i][3]), (0, 255, 0), 2)    #boxing face
    
                            #plot result idx under box
                            text_x = bb[i][0]
                            text_y = bb[i][3] + 20
                           
                            if np.max(predictions[0]) > 0.90:
                                put_text = '{name} {confidence: 3.2f}'.format(name = HumanNames[best_class_indices[0]], confidence = (np.max(predictions[0]).tolist())*100)
                                ser.write('success\r\n'.encode('utf-8'))
                            elif np.max(predictions[0]) < 0.80 and np.max(predictions[0]) > 0.60:
                                ser.write('fail\r\n'.encode('utf-8'))
            
                            else:
                                put_text = 'Stranger'
                                
                            cv2.putText(frame, put_text, (text_x, text_y), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                        1, (25, i*125, 25), thickness=2, lineType=2)                    
                            
                        except IndexError :
                            print("Oh No! IndexError : list index out of range for multi-faces")                        


                else:
                    print('Unable to align')

            sec = curTime - prevTime
            prevTime = curTime
            fps = 1 / (sec)
            str = 'FPS: %2.3f' % fps
            text_fps_x = len(frame[0]) - 150
            text_fps_y = 20
            cv2.putText(frame, str, (text_fps_x, text_fps_y),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0), thickness=1, lineType=2)
            # c+=1
            cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video_capture.release()
        # #video writer
        # out.release()
        cv2.destroyAllWindows()
