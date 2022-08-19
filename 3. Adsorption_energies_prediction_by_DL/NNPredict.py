#! /usr/env python3.6
from keras.models import load_model
import tensorflow as tf
import keras.backend.tensorflow_backend as KTF
import keras as K
import numpy as np
import os
import sys

os.environ["CUDA_VISIBLE_DEVICES"]="-1"
os.environ["HDF5_USE_FILE_LOCKING"]="FALSE"
gpu_options=tf.GPUOptions(per_process_gpu_memory_fraction=1)
KTF.set_session(tf.Session(config=tf.ConfigProto(device_count={'cpu':0},log_device_placement=True,inter_op_parallelism_threads=1,intra_op_parallelism_threads=1,gpu_options=gpu_options)))

net=load_model('model_file.h5')
file=open("properties_of_alloys.txt","r")
line=file.readline()
first_line=True

while line and line !=" ":
        line=line.replace("\n","")
        line_list=line.split(" ")
        line_list=[x for x in line_list if x!=""]
        if first_line:
                x_predict=np.array(line_list[3:])
                first_line=False
        else:
                x_data=np.array([line_list[3:]])
                x_predict=np.vstack((x_predict,x_data))
        line=file.readline()
file.close()
y_predict=net.predict(x_predict)
print('\n initial !!!!!!!!!!!!!!!!!!')
#print(y_predict)
j=1
for i in y_predict:
        if j != 6:
                print(str(i)+" ",end='')
                j=j+1
        else:
                print(i)
                j=1

