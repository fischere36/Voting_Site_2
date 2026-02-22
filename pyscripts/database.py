import pysqlite3 as sql
import sys
import csv
import json
from werkzeug.security import generate_password_hash , check_password_hash
from pyscripts.user import User



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
        
        #self.cur.execute("""CREATE TABLE IF NOT EXISTS ballot(
        #                ballot_id INTEGER PRIMARY KEY AUTOINCREMENT
        #                quote_id_1 INTEGER, 
        #                quote_id_2 INTEGER, 
        #                FOREIGN KEY(quote_id_1) REFERENCES quotes(quotes_id),
        #                FOREIGN KEY(quote_id_2) REFERENCES quotes(quotes_id)  """)
        
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_name TEXT NOT NULL UNIQUE,
                        email TEXT NOT NULL UNIQUE,
                        password_hash TEXT NOT NULL)""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS votes(
                        vote_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        
                        quote_id_1 INTEGER NOT NULL, 
                        quote_id_2 INTEGER NOT NULL, 
                        voted_for INTEGER,
                        voter_id INTEGER NOT NULL,
                        
                        FOREIGN KEY(quote_id_1) REFERENCES quotes(quote_id),
                        FOREIGN KEY(quote_id_2) REFERENCES quotes(quote_id),
                        FOREIGN KEY(voted_for) REFERENCES quotes(quote_id),
                        FOREIGN KEY(voter_id) REFERENCES users(user_id),
                        
                        UNIQUE(quote_id_1, quote_id_2, voter_id)

                        )""")


    def pull_user_data_user_name(self,user_name):
        self.cur.execute("SELECT user_id, user_name, email, password_hash FROM users WHERE user_name = ?",(user_name,))
        user_row = self.cur.fetchone()
        if user_row is None:
            return(None)
        user=User.from_db_row(user_row)
        return(user)

    def pull_user_data_email(self,email):
        self.cur.execute("SELECT user_id, user_name, email, password_hash FROM users WHERE email = ?",(email,))
        user_row = self.cur.fetchone()
        if user_row is None:
            return(None)
        user=User.from_db_row(user_row)
        return(user)
    
    def pull_user_data_id(self,id):
        self.cur.execute("SELECT user_id, user_name, email, password_hash FROM users WHERE user_id = ?",(id,))
        user_row = self.cur.fetchone()
        if user_row is None:
            return(None)
        user=User.from_db_row(user_row)
        return(user)

    def readCSV(self, quoteFile):
        print("run readCSV")

        try:
            with open(quoteFile, mode='r', encoding='utf-8-sig') as opened:
                qreader = csv.DictReader(opened)

                for row in qreader:
                    author = row.get("Author")
                    quote = row.get("Content")
                    timestamp = row.get("Date")

                    # Only write quotes that contain both a space and a double quote
                    if '"' in quote and ' ' in quote:
                        self.writeQuote(timestamp, author, quote)

        except IOError as err:
            print(f"Unable to open the file '{quoteFile}': {err}", file=sys.stderr)
            return False

        return True


    def new_user(self,user:User):
        print(user.user_name)
        try:
            self.cur.execute(
                'INSERT INTO users (user_name, email, password_hash) VALUES (?, ?, ?)',
                (user.user_name, user.email, user.password_hash)
            )
            return True

        except sql.IntegrityError as e:
            message = str(e)

            if "user_name" in message:
                return "username_taken"
            if "email" in message:
                return "email_taken"

            return "integrity_error"

        except Exception as e:
            # Catch any other unexpected errors
            return "unknown_error"

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