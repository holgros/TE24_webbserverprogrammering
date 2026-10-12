"""
OBS: DU MÅSTE STARTA DATABASEN (MED XAMPP-KONTROLLPANELEN) INNAN DU KÖR PYTHONSKRIPTET!
Innan du kör koden, skapa en tabell med följande kommando (klistra in i inmatningsfältet under fliken SQL):
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,  -- Autoinkrementerande primärnyckel
    fornamn VARCHAR(50) NOT NULL,       -- Förnamn, max 50 tecken
    efternamn VARCHAR(100) NOT NULL,    -- Efternamn, max 100 tecken
    klass VARCHAR(5) NOT NULL         -- Klass, max 5 tecken
);
Alternativt får du anpassa nedanstående anrop så att de fungerar för din tabell
"""

import mysql.connector  # installera med "pip install mysql-connector-python" i kommandotolken
mydb = mysql.connector.connect(
  host="localhost",
  user="root",  # standardanvändarnamn för XAMPP
  password="",  # dito lösenord (en tom sträng)
  database="webbserverprogrammering"  # byt namn om din databas heter något annat
)
mycursor = mydb.cursor()
print("Uppkopplad till databasen!")

# Skriva till databasen
sql = "INSERT INTO students (fornamn, efternamn, klass) VALUES (%s, %s, %s)"
val = ("Graham", "Chapman", "TE24A")
mycursor.execute(sql, val)
mydb.commit()
print(mycursor.rowcount, "record inserted.")

# Läsa från databasen
mycursor.execute("SELECT * FROM students")
myresult = mycursor.fetchall()
for x in myresult:
  print(x)