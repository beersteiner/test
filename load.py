import pymysql
import sqlalchemy as sa
from odo import odo


## CLASS DEFINITIONS

# DO NOT MODIFY! - Table structure information object
class tabEntry:
    def __init__(self, name=None, csv=None, cols=None):
        self.name=name # name of table
        self.csv=csv   # path to csv source (string)
        self.cols=cols # list of tuples [(cName, cType), ...]


## GLOBALS - Modify!

wCliOpt = '/home/john/client-ssl/CastawayCay_MySQL/.writeclient.cnf'
DB_NAME = 'iris'
TABLES = []
TABLES.append(tabEntry(name = 'data',
                       csv = 'iris_ch.data',
                       cols = [('sepal_length', sa.Float),
                               ('sepal_width', sa.Float),
                               ('petal_length', sa.Float),
                               ('petal_width', sa.Float),
                               ('class', sa.String(20))]))


## FUNCTIONS

# DO NOT MODIFY! - Creates a connection to MySQL Server
def mysql_connect_w():
    return pymysql.connect(read_default_file=wCliOpt)

# DO NOT MODIFY! - Creates a connection to MySQL Database
def db_connect_w():
    return pymysql.connect(read_default_file=wCliOpt, db=DB_NAME)

# DO NOT MODIFY! - Creates a database or returns an error
def create_database(cursor):
    print 'Database `{}`:'.format(DB_NAME),
    try: cursor.execute(
            'CREATE DATABASE {}'.format(DB_NAME))
    except pymysql.MySQLError as err:
        print 'already exists.'
    else:
        print 'OK.'

# DO NOT MODIFY! - Adds an additional auto-increment column to table
def add_autoinc_col(db, t):
    conn = db.raw_connection()
    cursor = conn.cursor()
    cursor.execute('ALTER TABLE `'+t+'` ADD `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST')
    cursor.close() # Close handle for SQL server
    conn.close() # Close the connection to the SQL server


## MAIN

# Create Database
sql_eng = sa.create_engine('mysql+pymysql://', creator=mysql_connect_w)
conn = sql_eng.raw_connection()
cursor = conn.cursor() 
create_database(cursor)
cursor.close() # Close handle for SQL server
conn.close() # Close the connection to the SQL server

# Creat the sqlalchemy engine
db_eng = sa.create_engine('mysql+pymysql://', creator=db_connect_w)
metadata = sa.MetaData(bind=db_eng) # holds database information

# Loop through all table entries
for te in TABLES:
    # create the sqlalchemy.table object
    tbl = sa.Table(
        te.name,
        metadata,
        *[sa.Column(c[0],c[1]) for c in te.cols])
    print 'Table `{}`:'.format(te.name),
    if tbl.exists(): 
        print 'exists; over-writing.',
        tbl.drop(checkfirst=True)
    tbl.create()
    add_autoinc_col(db_eng, te.name)    # Add AUTOINCREMENT COLUMN
    odo(te.csv, tbl)                    # bulk-load the .csv using odo
    print 'OK.'
print 'Table loading complete!'




