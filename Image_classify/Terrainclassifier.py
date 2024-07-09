# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1tmih1mEhJDpsiF0j5K_TxLMJg-xuO07-
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import  LabelBinarizer
from PIL import Image
from matplotlib.image import imread
from sklearn.model_selection import train_test_split
from keras.preprocessing.image import img_to_array, array_to_img
from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers import BatchNormalization
from keras.layers import Conv2D, MaxPooling2D, Activation, Flatten, Dropout, Dense

import matplotlib.pyplot as plt
import random
import os
path = '/content/drive/MyDrive/Colab Notebooks/AI/Image_classifier/Data/Intel Image Dataset/mountain'
plt.figure(figsize =(12,12))
for i in range(1,17):
  plt.subplot(4,4,i)
  plt.tight_layout()
  rand_image = imread(path+"/"+random.choice(sorted(os.listdir(path))))
  plt.imshow(rand_image)
  plt.title("Mountains")
  plt.xlabel(rand_image.shape[1], fontsize = 10)
  plt.ylabel(rand_image.shape[0], fontsize = 10)

image_list = []
label_list = []
dir = '/content/drive/MyDrive/Colab Notebooks/AI/Image_classifier/Data/Intel Image Dataset'
root_dir = os.listdir(dir)
for directory in root_dir:
    dir_path = os.path.join(dir, directory)
    if os.path.isdir(dir_path):
        for file in os.listdir(dir_path):
            image_path = os.path.join(dir_path, file)
            if os.path.isfile(image_path):
                image = Image.open(image_path)
                image = image.resize((150, 150))
                image = img_to_array(image)
                image_list.append(image)
                label_list.append(directory)

label_counts = pd.DataFrame(label_list).value_counts()
label_counts

num_classes = len(label_counts)
num_classes

np.array(image_list).shape

label_list = np.array(label_list)
label_list.shape

xtrain, xtest, ytrain, ytest = train_test_split(image_list, label_list, test_size=0.2, random_state=42)

x_train = np.array(xtrain, dtype=np.float16) / 225.0
x_test = np.array(xtest, dtype=np.float16) / 225.0

x_train = x_train.reshape( -1, 150,150,3)
x_test = x_test.reshape( -1, 150,150,3)

lb = LabelBinarizer()
y_train = lb.fit_transform(ytrain)
y_test = lb.fit_transform(ytest)
print(lb.classes_)

x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size = 0.2)

from keras.layers import LeakyReLU
model = Sequential([
        Conv2D(16, kernel_size = (3,3), input_shape = (150,150,3)),
        BatchNormalization(),
        LeakyReLU(),

        Conv2D(32, kernel_size = (3,3)),
        BatchNormalization(),
        LeakyReLU(),
        MaxPooling2D(5,5),

        Conv2D(64, kernel_size = (3,3)),
        BatchNormalization(),
        LeakyReLU(),

        Conv2D(128, kernel_size = (3,3)),
        BatchNormalization(),
        LeakyReLU(),
        MaxPooling2D(5,5),

        Flatten(),

        Dense(64),
        Dropout(rate = 0.2),
        BatchNormalization(),
        LeakyReLU(),

        Dense(32),
        Dropout(rate = 0.2),
        BatchNormalization(),
        LeakyReLU(),

        Dense(16),
        Dropout(rate = 0.2),
        BatchNormalization(),
        LeakyReLU(1),

        Dense(6, activation = 'softmax')
        ])
model.summary()

model.compile(loss = 'categorical_crossentropy', optimizer = Adam(0.005), metrics = ['accuracy'])

epochs = 10
batch_size = 128
history = model.fit(x_train, y_train, batch_size = batch_size, epochs = epochs, validation_data = (x_val, y_val))

plt.figure(figsize=(12, 5))
plt.plot(history.history['accuracy'], color='r')
plt.plot(history.history['val_accuracy'], color='b')
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epochs')
plt.legend(['train', 'val'])
plt.show()

#Plot the loss history
plt.figure(figsize=(12, 5))
plt.plot(history.history['loss'], color='r')
plt.plot(history.history['val_loss'], color='b')
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epochs')
plt.legend(['train', 'val'])
plt.show()

# Calculating test accuracy
scores = model.evaluate(x_test, y_test)
print(f"Test Accuracy: {scores[1]*100}")

img = array_to_img(x_test[1])
img

y_pred = model.predict(x_test)

labels = lb.classes_
print(labels)
print("Originally : ",labels[np.argmax(y_test[1])])
print("Predicted : ",labels[np.argmax(y_pred[1])])