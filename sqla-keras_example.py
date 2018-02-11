#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 11:33:50 2018

@author: john
"""

# From Tutorial at: 
#   https://elitedatascience.com/keras-tutorial-deep-learning-in-python#step-3


import numpy as np
import pymysql
from sqlalchemy import *
from random import random
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten



# GLOBALS

#rCliOpt = '/home/john/client-ssl/CastawayCay_MySQL/.readclient.cnf' # from Tortuga VM
rCliOpt = '/home/john/Application_Files/MySQL/.local_sql.cnf' # from John's laptop
DB_NAME = 'sandbox'
TBL_NAME = 'iris'
BCH_SIZE = 10
ID_NAME = 'id'
L_NAME = 'class_name'
SPLIT = 0.9 # percentage of data to use for training (remaining for test)


# FUNCTIONS 

# Callable pymysql connector used for creating the engine
def db_connect_r():
    return pymysql.connect(read_default_file=rCliOpt, db=DB_NAME)

def to_categorical(a):
    d = {'Iris_versicolor':(1,0,0), 'Iris_virginica':(0,1,0), 'Iris_setosa':(0,0,1)}
    res = [0 for i in range(len(a))]
    for i in range(len(a)):
        res[i] = d[a[i][0]]
    return res


# MAIN

# Grab a Table object for the data using sqlalchemy
db = create_engine('mysql+pymysql://', creator=db_connect_r, echo=False)
metadata = MetaData(db)
data = Table(TBL_NAME, metadata, autoload=True)
n = select([func.count()]).select_from(data).execute().fetchone()[0] # total data
n_trn = int(SPLIT*n) # number to use for training
n_tst = n - n_trn  # number to use for testing

# Get a random training and test sample from the table
seed = np.random.randint(100) # set the random seed
# Define the list of feature columns
xcols = [k for k in data.c.keys() if k not in [ID_NAME, L_NAME]]
# Create select statements for training data
X_trn_stmt = select(columns=xcols, from_obj=data).order_by(func.rand(seed)).limit(n_trn)
Y_trn_stmt = select(columns=[L_NAME], from_obj=data).order_by(func.rand(seed)).limit(n_trn)
# Create select statements for testing data
X_tst_stmt = select(columns=xcols, from_obj=data).order_by(func.rand(seed)).offset(n_trn+1)
Y_tst_stmt = select(columns=[L_NAME], from_obj=data).order_by(func.rand(seed)).offset(n_trn+1)
# Load the data
X_trn = X_trn_stmt.execute().fetchall()
Y_trn = to_categorical(Y_trn_stmt.execute().fetchall())
X_tst = X_tst_stmt.execute().fetchall()
Y_tst = to_categorical(Y_tst_stmt.execute().fetchall())

# Build the model
model = Sequential()
model.add(Dense(16, activation='relu', input_shape=(4,)))            # fully connected size 128
model.add(Dense(3, activation='softmax'))          # output layer
# Now compile model
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

# Fit the model to the training data
print '\nTraining Model...'
model.fit(X_trn, Y_trn, batch_size=BCH_SIZE, epochs=100, verbose=0)

# Evaluate the model on test data
print '\nEvaluating on Test Data...'
loss, accuracy = model.evaluate(X_tst, Y_tst, verbose=1)
print '\nLoss and Accuracy:'
print loss, accuracy
#
#
#
#
#
#
#
#
