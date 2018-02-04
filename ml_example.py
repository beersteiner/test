#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 11:33:50 2018

@author: john
"""

# From Tutorial at: 
#   https://elitedatascience.com/keras-tutorial-deep-learning-in-python#step-3


import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.utils import np_utils
from keras.datasets import mnist
from matplotlib import pyplot as plt


np.random.seed(123) # set random seed so tutorial is reproducible

# Load pre-shuffled MNIST data into train and test sets
(X_train, y_train), (X_test, y_test) = mnist.load_data()

print X_train.shape
# (60000, 28, 28) or 60k samples of 28x28 pixels

plt.imshow(X_train[0])

# Reshaping to show depth of 1; tensorflow expects (Num,Hight,Wid,Chan)
X_train = X_train.reshape(X_train.shape[0], 28, 28, 1)
X_test = X_test.reshape(X_test.shape[0], 28, 28, 1)

print X_train.shape
# (60000, 1, 28, 28)

print y_train.shape
# (60000,) ... should be (60000, 10)

y_train = np_utils.to_categorical(y_train, 10)
y_test = np_utils.to_categorical(y_test, 10)

print y_train.shape
# (60000, 10) ... better!

model = Sequential()
# Add a convolution layer
#   32 convolution filters with 3 rows and 3 columns
#   rectified linear unit activation function
#   input shape must be same as image shapes
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(28,28,1)))
model.add(Conv2D(32, (3, 3), activation='relu'))    # another conv layer
model.add(MaxPooling2D(pool_size=(2,2)))            # max pooling layer
model.add(Dropout(0.25)) # drops some previous layer nodes to prevent overfitting
model.add(Flatten()) # required prior to passing to dense (fully cnctd) layers
model.add(Dense(128, activation='relu'))            # fully connected size 128
model.add(Dropout(0.5))                             # to prevent overfitting
model.add(Dense(10, activation='softmax'))          # output layer
# Now compile model
#   loss is the loss function
#   optimizer is the optimizer function
#   metrics is the function to judge performance
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
# Fit the model to the training data
model.fit(X_train, Y_train, 
          batch_size=32, nb_epoch=10, verbose=1)
# Evaluate the model on test data
loss, accuracy = model.evaluate(X_test, Y_test, verbose=0)
print loss, accuracy








