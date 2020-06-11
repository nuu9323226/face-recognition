from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from scipy import misc
import sys
import os
import argparse
import tensorflow as tf
import numpy as np
import facenet
import detect_face
import random
from time import sleep


def get_dataset(paths,personget, has_class_directories=True):
    dataset = []
    
    for path in paths.split(':'):
        path_exp = os.path.expanduser(path)
        classes = os.listdir(path_exp)
        
        classes=personget
        print('classes',classes)
        
        
        classes.sort()
        nrof_classes = len(classes)
        for i in range(nrof_classes):
            class_name = classes[i]
            facedir = os.path.join(path_exp, class_name)
            image_paths = get_image_paths(facedir)
            dataset.append(ImageClass(class_name, image_paths))
  
    return dataset

def get_image_paths(facedir):
    image_paths = []
    if os.path.isdir(facedir):
        images = os.listdir(facedir)
        image_paths = [os.path.join(facedir,img) for img in images]
    return image_paths


class ImageClass():
    "Stores the paths to images for a given class"
    def __init__(self, name, image_paths):
        self.name = name
        self.image_paths = image_paths
  
    def __str__(self):
        return self.name + ', ' + str(len(self.image_paths)) + ' images'
  
    def __len__(self):
        return len(self.image_paths)


def main(personget,mode):
    #global current
    if mode=='person':
        output_dir_path = '~/facenet/models/personout'
        datadir = '~/facenet/models/person'
    else:
        output_dir_path =  '~/facenet/models/personout'
        datadir = '~/facenet/datasets/historyImage'       
    
    output_dir = os.path.expanduser(output_dir_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    
    dataset = get_dataset(datadir,personget)
    print('dataset',dataset)
    
    print('Creating networks and loading parameters')
    with tf.Graph().as_default():
        gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.9)
        sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
        with sess.as_default():
            pnet, rnet, onet = detect_face.create_mtcnn(sess, './')
    
    #minsize = 300  # minimum size of face
    minsize = 200  # minimum size of face
    threshold = [0.6, 0.7, 0.7]  # three steps's threshold
    factor = 0.709  # scale factor
    margin = 44
    #image_size = 182
    image_size = 182
    
    # Add a random key to the filename to allow alignment using multiple processes
    random_key = np.random.randint(0, high=99999)
    bounding_boxes_filename = os.path.join(output_dir, 'bounding_boxes_%05d.txt' % random_key)
    print('Goodluck')
    
    with open(bounding_boxes_filename, "w") as text_file:
        nrof_images_total = 0
        nrof_successfully_aligned = 0
        for cls in dataset:
            output_class_dir = os.path.join(output_dir, cls.name)
            if not os.path.exists(output_class_dir):
                os.makedirs(output_class_dir)
            for image_path in cls.image_paths:
                nrof_images_total += 1
                filename = os.path.splitext(os.path.split(image_path)[1])[0]
                output_filename = os.path.join(output_class_dir, filename + '.png')
                print(image_path)
                if not os.path.exists(output_filename):
                    try:
                        img = misc.imread(image_path)
                        print('read data dimension: ', img.ndim)
                    except (IOError, ValueError, IndexError) as e:
                        errorMessage = '{}: {}'.format(image_path, e)
                        print(errorMessage)
                    else:
                        if img.ndim < 2:
                            print('Unable to align "%s"' % image_path)
                            text_file.write('%s\n' % (output_filename))
                            continue
                        if img.ndim == 2:
                            img = facenet.to_rgb(img)
                            print('to_rgb data dimension: ', img.ndim)
                        img = img[:, :, 0:3]
                        print('after data dimension: ', img.ndim)
    
                        bounding_boxes, _ = detect_face.detect_face(img, minsize, pnet, rnet, onet, threshold, factor)
                        nrof_faces = bounding_boxes.shape[0]
                        print('detected_face: %d' % nrof_faces)
                        if nrof_faces > 0:
                            det = bounding_boxes[:, 0:4]
                            img_size = np.asarray(img.shape)[0:2]
                            if nrof_faces > 1:
                                bounding_box_size = (det[:, 2] - det[:, 0]) * (det[:, 3] - det[:, 1])
                                img_center = img_size / 2
                                offsets = np.vstack([(det[:, 0] + det[:, 2]) / 2 - img_center[1],
                                                     (det[:, 1] + det[:, 3]) / 2 - img_center[0]])
                                offset_dist_squared = np.sum(np.power(offsets, 2.0), 0)
                                index = np.argmax(bounding_box_size - offset_dist_squared * 2.0)  # some extra weight on the centering
                                det = det[index, :]
                            det = np.squeeze(det)
                            bb_temp = np.zeros(4, dtype=np.int32)
    
                            bb_temp[0] = det[0]
                            bb_temp[1] = det[1]
                            bb_temp[2] = det[2]
                            bb_temp[3] = det[3]
    
                            cropped_temp = img[bb_temp[1]:bb_temp[3], bb_temp[0]:bb_temp[2], :]
                            try:
                                scaled_temp = misc.imresize(cropped_temp, (image_size, image_size), interp='bilinear')
                                nrof_successfully_aligned += 1
                                misc.imsave(output_filename, scaled_temp)
                                text_file.write('%s %d %d %d %d\n' % (output_filename, bb_temp[0], bb_temp[1], bb_temp[2], bb_temp[3]))                                
                            except:
                                print('error:woring size')
                                pass

                        else:
                            print('Unable to align "%s"' % image_path)
                            text_file.write('%s\n' % (output_filename))
    
    print('Total number of images: %d' % nrof_images_total)
    print('Number of successfully aligned images: %d' % nrof_successfully_aligned)

    
