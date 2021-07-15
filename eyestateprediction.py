# -*- coding: utf-8 -*-
"""EyeStatePrediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YG6rsYRKOCuCVaxyq7xFg-DL_srPMvLs
"""

import matplotlib.pyplot as plt
import numpy as np              
import pandas as pd

from google.colab import drive
drive.mount('/content/drive')

#Define Directories for train, test & Validation Set
train_path = '/content/drive/MyDrive/Final Year Project/DriverDrowsinessDetection/highDimensionEyeImageDataset/train'
test_path = '/content/drive/MyDrive/Final Year Project/DriverDrowsinessDetection/highDimensionEyeImageDataset/test'
valid_path = '/content/drive/MyDrive/Final Year Project/DriverDrowsinessDetection/highDimensionEyeImageDataset/val'
#The batch refers to the number of training examples utilized in one iteration
batch_size = 16
#The dimension of the image
img_height = 40
img_width = 40

from tensorflow.keras.preprocessing.image import ImageDataGenerator
# Create Image Data Generator for Train Set
image_gen = ImageDataGenerator(
                                  rescale = 1./255,
                                  shear_range = 0.2,
                                  zoom_range = 0.2,
                                  horizontal_flip = True,          
                               )
# Create Image Data Generator for Test/Validation Set
test_data_gen = ImageDataGenerator(rescale = 1./255)

train = image_gen.flow_from_directory(
      train_path,
      target_size=(img_height, img_width),
      color_mode='grayscale',
      class_mode='binary',
      batch_size=batch_size
      )
test = test_data_gen.flow_from_directory(
      test_path,
      target_size=(img_height, img_width),
      color_mode='grayscale',
      shuffle=False,  
      class_mode='binary',
      batch_size=batch_size
      )
valid = test_data_gen.flow_from_directory(
      valid_path,
      target_size=(img_height, img_width),
      color_mode='grayscale',
      class_mode='binary', 
      batch_size=batch_size
      )

plt.figure(figsize=(12, 12))
for i in range(0, 15):
    plt.subplot(3, 5, i+1)
    for X, Y in train:
        image = X[0]        
        dic = {0:'closed', 1:'open'}
        plt.title(dic.get(Y[0]))
        plt.imshow(np.squeeze(image),cmap='gray',interpolation='nearest')
        break
plt.tight_layout()
plt.show()

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Conv2D,Flatten,MaxPooling2D
from tensorflow.keras.callbacks import EarlyStopping,ReduceLROnPlateau

cnn = Sequential()
cnn.add(Conv2D(32, (5, 5), activation="relu", input_shape=(img_width, img_height, 1)))
cnn.add(MaxPooling2D(pool_size = (2, 2)))
cnn.add(Conv2D(32, (5, 5), activation="relu", input_shape=(img_width, img_height, 1)))
cnn.add(MaxPooling2D(pool_size = (2, 2)))
cnn.add(Conv2D(32, (5, 5), activation="relu", input_shape=(img_width, img_height, 1)))
cnn.add(MaxPooling2D(pool_size = (2, 2)))
cnn.add(Flatten())
cnn.add(Dense(activation = 'relu', units = 64))
cnn.add(Dense(activation = 'sigmoid', units = 1))
cnn.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

cnn.summary()

#MODEL SUMMARY
# Hyperparameters of Conv2D
Conv2D(
    32,
    kernel_size = (5,5),
    strides=(1, 1),
    padding="valid",
    activation="relu",
    input_shape=(img_height,img_width,1)
    )
# Hyperparameters of MaxPooling2D 
MaxPooling2D(
    pool_size=(2, 2), strides=None, padding="valid"
    )

from tensorflow.keras.utils import plot_model
plot_model(cnn,show_shapes=True, show_layer_names=True, rankdir='TB', expand_nested=True)

early = EarlyStopping(monitor='val_loss', mode='min', patience=3)
learning_rate_reduction = ReduceLROnPlateau(monitor='val_loss', patience = 2, verbose=1,factor=0.3, min_lr=0.000001)
callbacks_list = [ early, learning_rate_reduction]

from sklearn.utils.class_weight import compute_class_weight
weights = compute_class_weight('balanced', np.unique(train.classes), train.classes)
cw = dict(zip( np.unique(train.classes), weights))
print(cw)

cnn.fit(train,epochs=20, validation_data=valid, class_weight=cw, callbacks=callbacks_list)

test_accu = cnn.evaluate(test)
print('The testing accuracy is :',test_accu[1]*100, '%')

cnn.save('/content/drive/MyDrive/Final Year Project/DriverDrowsinessDetection/model.h5', overwrite=True)

from keras.models import load_model
import numpy as np
import cv2
#load the trained model
model = load_model('/content/drive/MyDrive/Final Year Project/DriverDrowsinessDetection/model4033.h5')

#single static image prediction
categories = ['closed','open']
def prepare(filepath):
  img_size = 40
  img_array = cv2.imread(filepath,cv2.IMREAD_GRAYSCALE)
  new_array = cv2.resize(img_array,(img_size,img_size))
  return new_array.reshape(-1,img_size,img_size,1)

closedEyeFilepath = '/content/drive/MyDrive/Final Year Project/DriverDrowsinessDetection/highDimensionEyeImageDataset/test/closed/closed_eye_0024.jpg_face_2_L.jpg'
openEyeFilepath = '/content/drive/MyDrive/Final Year Project/DriverDrowsinessDetection/highDimensionEyeImageDataset/test/open/Alina_Kabaeva_0001_L.jpg'
predictions = model.predict([prepare(closedEyeFilepath)])
print(categories[int(predictions[0][0])])
print(predictions)

import os
import cv2
def prepare(filepath):
  img_size = 40
  img_array = cv2.imread(filepath,cv2.IMREAD_GRAYSCALE)
  new_array = cv2.resize(img_array,(img_size,img_size))
  return new_array.reshape(-1,img_size,img_size,1)

# # !pip install playsound
# # from playsound import playsound 
# path = '/content/drive/MyDrive/Final Year Project/DriverDrowsinessDetection/Execution/closedeye'
# # total_frames = len(os.listdir(path))
# # print(total_frames)
# score = 0
# for img in os.listdir(path):
#   img_path = os.path.join(path,img)
#   pred = model.predict([prepare(img_path)])
#   # print("{} is {}".format(img,pred))
#   if(int(pred[0][0]) == 0):
#     score += 1
#   else:
#     score -= 1
#   if(score < 0):
#     score = 0
#   if(score == 15):
#     print("Drowsiness detected")
#     score = 0

# !pip install playsound
# from playsound import playsound 
path = '/content/drive/MyDrive/Final Year Project/DriverDrowsinessDetection/Execution/drowsy'
total_frames = len(os.listdir(path))
# print(total_frames)
filename = "drowsy"
score = 0
flag = 0
cameraFps = 26
threshold = cameraFps / 2
for img in range(total_frames):
  img_name = filename + str(img + 1) + ".png"
  img_path = os.path.join(path,(img_name))
  pred = model.predict([prepare(img_path)])
  print("{} is {}".format(img_name,pred))
  if(int(pred[0][0]) == 0):
    score += 1
  else:
    score -= 1
  if(score < 0):
    score = 0
  if(score == threshold):
    print("\nDrowsiness detected\n")
    flag = 1
    score = 0

#no drowsiness condition
if flag == 0:
  print("Drowsiness not detected")