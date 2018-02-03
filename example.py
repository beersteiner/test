#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 08:48:04 2018

@author: john
"""

from sqlalchemy import *
import pymysql



#### GLOBALS ####

rCliOpt = '/home/john/client-ssl/CastawayCay_MySQL/.readclient.cnf'
DB_NAME = 'iris'
TBL_NAME = 'data'


#### FUNCTIONS ####

# Callable pymysql connector used for creating the engine
def db_connect_r():
    return pymysql.connect(read_default_file=rCliOpt, db=DB_NAME)

# Simple wrapper to return list of results
def run(stmt):
    rs = stmt.execute()
    return [r for r in rs]
    





#### MAIN ####

# Create the engine
db = create_engine('mysql+pymysql://', creator=db_connect_r, echo=False)
# Create the base class as an automapper
metadata = MetaData(db)
# Reflect tables in the database
data = Table(TBL_NAME, metadata, autoload=True)

#### Just some examples! ####
# Define some statement objects to make working with the data easier
i = data.insert()       # insert statement (eg. i.execute(sepal-length=5.1, ...))
s_all = data.select()   # select statement (eg. s.execute) 
rs = s_all.execute()    # result set object
row = rs.fetchone()     # gets one row from result set
rows = rs.fetchall()    # gets all rows from result set
print data.c.keys()     # column names
#for r in run(data.select(data.c.sepal_length>6.0)): print r
for r in run(data.select(((data.c.sepal_length>6.0) &
                          (data.c.petal_length>5.0)))): print r




