import MySQLdb

db = MySQLdb.connect("localhost", "root", "980814", "LipStickKey", charset='utf8')

cursor = db.cursor()

#sql1 = "USE LipStickKey;CREATE TABLE KEYU(ID INT NOT NULL,Name VARCHAR(40), Colour VARCHAR(40),ColorURL VARCHAR(256),ProductURL VARCHAR(256),R INT,B INT, G INT, PRIMARY KEY(ID))ENGINE=InnoDB DEFAULT CHARSET=utf8;"

#cursor.execute(sql1)
#db.commit()


f = open("key.txt", "r")
line = f.readline()

while line:
    lineSplit = line.split('\t')
    idu = lineSplit[0]
    name = lineSplit[1]
    colour = lineSplit[2]
    coloururl = lineSplit[3]
    producturl = lineSplit[4]
    r = lineSplit[5]
    b = lineSplit[6]
    g = lineSplit[7]
    sql2 = "INSERT INTO KEYU(ID, Name, Colour, ColorURL, ProductURL, R, B, G) VALUES (" + idu)"
    cursor.execute(sql2)

f.close()
