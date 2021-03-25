import mysql.connector

db_conn = mysql.connector.connect(host="acit3855.westus2.cloudapp.azure.com", user="user",
password="password", database="events")

db_cursor = db_conn.cursor()

db_cursor.execute('''
 CREATE TABLE immediate
 (id INT NOT NULL AUTO_INCREMENT,
 customer_id VARCHAR(250) NOT NULL,
 city VARCHAR(250) NOT NULL,
 country VARCHAR(250) NOT NULL,
 no_of_days INTEGER NOT NULL,
 date_created VARCHAR(100) NOT NULL,
 CONSTRAINT customer_id_pk PRIMARY KEY (id))
 ''')


db_cursor.execute('''
 CREATE TABLE schedule
 (id INT NOT NULL AUTO_INCREMENT,
 customer_id VARCHAR(250) NOT NULL,
 city VARCHAR(250) NOT NULL,
 country VARCHAR(250) NOT NULL,
 check_in VARCHAR(100) NOT NULL, 
 check_out VARCHAR(100) NOT NULL,
 date_created VARCHAR(100) NOT NULL,
 CONSTRAINT customer_id_pk PRIMARY KEY (id))
 ''')
db_conn.commit()
db_conn.close()