import sqlite3

conn = sqlite3.connect('readings.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE immediate
          (id INTEGER PRIMARY KEY ASC, 
           customer_id VARCHAR(250) NOT NULL,
           city VARCHAR(250) NOT NULL,
           country VARCHAR(250) NOT NULL,
           no_of_days INTEGER NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

c.execute('''
          CREATE TABLE schedule
          (id INTEGER PRIMARY KEY ASC, 
           customer_id VARCHAR(250) NOT NULL,
           city VARCHAR(250) NOT NULL,
           country VARCHAR(250) NOT NULL,
           check_in VARCHAR(100) NOT NULL, 
           check_out VARCHAR(100) NOT NULL, 
           date_created VARCHAR(100) NOT NULL)
          ''')

conn.commit()
conn.close()
