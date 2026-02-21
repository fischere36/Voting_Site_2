import pysqlite3 as sql
import sys
import csv
import json


class database:

    def __init__(self):
        self.con = sql.connect('prototype.db', check_same_thread=False)
        self.con.isolation_level = None
        self.cur = self.con.cursor()
        self.createDB()

    def createDB(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS quotes(
                        quote_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        timestamp TEXT, 
                        author TEXT, 
                        quote TEXT)""")
        
        self.cur.execute("""CREATE TABLE IF NOT EXISTS ballot(
                        ballot_id INTEGER PRIMARY KEY AUTOINCREMENT
                        quote_id_1 INTEGER, 
                        quote_id_2 INTEGER, 
                        FOREIGN KEY(quote_id_1) REFERENCES quotes(quotes_id),
                        FOREIGN KEY(quote_id_2) REFERENCES quotes(quotes_id)  """)
        
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_name TEXT NOT NULL UNIQUE,
                        email TEXT NOT NULL UNIQUE,
                        first_name TEXT,
                        last_name TEXT,
                        number_of_votes INTEGER)""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS votes(
                        vote_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        quote_id INTERGER NOT NULL,
                        voter_id INTERGER NOT NULL,
                        FOREIGN KEY(voter_id) REFERENCES users(user_id),
                        FOREIGN KEY(quote_id) REFERENCES quotes(quote_id),
                        number_of_votes INTEGER)""")

    def createUser(self, username, email, fName, lName):
        self.cur.execute('INSERT INTO users (user_name, email, first_name, last_name) VALUES (?, ?, ?, ?)', (username, email, fName, lName))
        


    def login(self,username,email):
        userData=self.pullUserData(username)
        if userData["email"]==email:
            return(0)
        

        

    def pullUserData(self,username):
        self.cur.execute('''SELECT * FROM users WHERE user_name = ?''',(username,))
        userDataTuple = self.cur.fetchall()
        userDataTuple=userDataTuple[0]
        userData={
            "user_id":userDataTuple[0],
            "user_name":userDataTuple[1],
            "email":userDataTuple[2],
            "first_name":userDataTuple[3],
            "last_name":userDataTuple[4]
        } 
        return(userData)


    def readCSV(self,quoteFile):
        #quoteFile="./quotesfiles/"+"The Better SMP - Main - quotes [837444835472441414].csv"
        print("run readCSV")
        try:
            opened = open(quoteFile, mode='r', encoding = 'utf-8-sig')
        except IOError as err:
            print(f"Unable to open the files '{quoteFile}': {err}", file=sys.stderr)
            sys.exit(1)
        
        qreader=csv.DictReader(opened)
        for row in qreader:
            #print("run readCSV quote read")
            author=row["Author"]
            quote=row["Content"]
            timestamp=row["Date"]
            #self.writeQuote(timestamp,author,quote)
            try :
                
                quote.index('''"''')
                quote.index(''' ''')
                #print("run readCSV quote screend")
                self.writeQuote(timestamp,author,quote)
                #print("run readCSV quote writen")
            except:
                pass

    def writeQuote(self,timestamp,author,quote):
        
        self.cur.execute('INSERT INTO quotes (timestamp, author, quote) VALUES (?, ?, ?)', (timestamp,author,quote))
        #self.con.commit()

    def decodeTimeStamp(self,timestamp):
        timestamp
        tempList=timestamp.split("T")
        dateUnsplit=tempList[0]
        timeWithOffset=tempList[1]
        date=dateUnsplit.split("-")
        timeWithOffset.split("-")
        time=timeWithOffset[0]
        offset=timeWithOffset[0]
        timeDict={
            "Year": date[0],
            "Month": date[1],
            "Day": date[2],
            "Hour": time[0],
            "Minute": time[1],
            "Second": time[2],
            "Offset": offset
        }
        return(timeDict)