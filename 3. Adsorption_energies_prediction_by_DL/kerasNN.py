#! /bin/env python3.6

import tensorflow as tf
import keras.backend.tensorflow_backend as KTF
import keras.backend as K
from keras.models import Sequential,load_model
from keras import initializers
from keras.layers import Dense,Activation,Dropout
from keras.optimizers import SGD,Adam,Nadam,Adamax
import numpy as np
import sys
import random
import os

os.environ["CUDA_VISIBLE_DEVICES"]="-1"
os.environ["HDF5_USE_FILE_LOCKING"]="FALSE"
gpu_options=tf.GPUOptions(per_process_gpu_memory_fraction=1)
KTF.set_session(tf.Session(config=tf.ConfigProto(device_count={'cpu':0},log_device_placement=True,inter_op_parallelism_threads=1,intra_op_parallelism_threads=1,gpu_options=gpu_options)))

def create_net(neurons=20,dropoutrate=0.3,initializer=initializers.VarianceScaling(scale=3.0,mode='fan_in',distribution='normal'),activation='elu'):
        net=Sequential()
        net.add(Dense(neurons,input_dim=21,kernel_initializer=initializer,activation=activation))
        net.add(Dropout(dropoutrate))
        net.add(Dense(neurons,activation=activation,kernel_initializer=initializer))
        net.add(Dense(neurons,activation=activation,kernel_initializer=initializer))
        net.add(Dense(neurons,activation=activation,kernel_initializer=initializer))
        net.add(Dense(neurons,activation=activation,kernel_initializer=initializer))
        net.add(Dense(neurons,activation=activation,kernel_initializer=initializer))
        net.add(Dense(20,activation=activation,kernel_initializer=initializer))
        net.add(Dense(neurons,activation=activation,kernel_initializer=initializer))
        net.add(Dense(1,activation='linear'))
        return net


file=open("database_DNN.dat","r")
line=file.readline()
first_line=True
while line and line != " ":
        line=line.replace("\n","")
        line_list=line.split(" ")
        line_list=[x for x in line_list if x != ""]
        if first_line:
                x_train=np.array(line_list[3:-1])
                y_train=np.array([line_list[-1]])
                first_line=False
        else:
                x_data=np.array([line_list[3:-1]])
                y_data=np.array([line_list[-1]])
                x_train=np.vstack((x_train,x_data))
                y_train=np.vstack((y_train,y_data))
        line=file.readline()
file.close()
data=list(zip(x_train,y_train))
random.shuffle(data)
train_data=data[:710]
test_data=data[711:]
x_train,y_train=zip(*train_data)
x_test,y_test=zip(*test_data)
x_train,y_train,x_test,y_test=map(np.array,[x_train,y_train,x_test,y_test])
#trainDS,testDS=DS.splitWithProportion(0.8)
net=load_model('model_file'+sys.argv[1]+'.h5')
#net=create_net()
adamax=Adamax(lr=0.004,beta_1=0.9,beta_2=0.999,epsilon=1e-08,decay=0.0)
net.compile(loss='mae',optimizer=adamax,metrics=['mse'])
mae_0=10
mse_0=0
for i in range(1):
        print("++++++++++++++++++"+str(i))
        K.set_value(adamax.lr,0.5*K.get_value(adamax.lr))
        for j in range(100):
                net.fit(x_train,y_train,epochs=400,verbose=2,batch_size=710)
                score=net.evaluate(x_test,y_test,batch_size=200)
                lr=K.get_value(adamax.lr)
                list_score=eval(str(score))
                print(list_score)
                if mae_0 > list_score[0]:
                        mae_0=list_score[0]
                        mse_0=list_score[1]
                        y_predict=net.predict(x_test)
                        net.save('/home/phys/zjlin/cmk/alloy_MSR/alloy_O/keras/model_file'+sys.argv[1]+'.h5')
                print(lr)
for i,j in zip(y_predict,y_test):
        print(str(i)+" "+str(j))
print(str(mae_0)+" "+str(mse_0))


