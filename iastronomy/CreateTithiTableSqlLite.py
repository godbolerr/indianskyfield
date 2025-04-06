import sqlite3

conn = sqlite3.connect('puneTithi2000.db')

print("Opened database successfully")

# 2024-01-01 07:19:26.872772+05:30XXXXXXX

conn.execute('''CREATE TABLE tithi (
              sqid INTEGER PRIMARY KEY,   
              tithiSeq INTEGER NOT NULL,  
              paksha varchar(1) NOT NULL,       
              tithiId INTEGER NOT NULL,
              sunriseDate VARCHAR(40) NOT NULL,

              year INTEGER NOT NULL,
              month INTEGER NOT NULL,
              day INTEGER NOT NULL,
              hour INTEGER NOT NULL,
              minute INTEGER NOT NULL,

              second REAL NOT NULL,
              tithiDate varchar(40) NOT NULL,
              kshayFlag varchar(1) NOT NULL,
              tyear INTEGER NOT NULL,
              tmonth INTEGER NOT NULL,

              tday INTEGER NOT NULL,
              thour INTEGER NOT NULL,
              tminute INTEGER NOT NULL,
              tsecond REAL NOT NULL,             
              timeFromSunrise INTEGER NOT NULL,

              duration  REAL NOT NULL,
              durationPeriod varchar(10) NOT NULL,
              slongd REAL NOT NULL,
              slongm REAL NOT NULL,  
              slongs REAL NOT NULL,
              
              slatd REAL NOT NULL,
              slatm REAL NOT NULL,  
              slats REAL NOT NULL,
              mlongd REAL NOT NULL,
              mlongm REAL NOT NULL,
               
              mlongs REAL NOT NULL,
              mlatd REAL NOT NULL,
              mlatm REAL NOT NULL,
              mlats REAL NOT NULL)''')
