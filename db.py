import sqlite3

class Database:
    def __init__(self):
        self.connection = sqlite3.connect("users.db")
        self.cursor = self.connection.cursor()
        
        self.pibbitConnection = sqlite3.connect("pibbit.db")
        self.pibbitCursor = self.pibbitConnection.cursor()
        self.createTable()
        
    def createTable(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                email TEXT PRIMARY KEY,
                password TEXT NOT NULL
            )
        """)
        self.connection.commit()
        
        self.pibbitCursor.execute("""
            CREATE TABLE IF NOT EXISTS pibbit (
                businessType VARCHAR NOT NULL,
                businessName VARCHAR NOT NULL,
                rating FLOAT,
            )
        """)
        self.pibbitConnection.commit()

    def addUser(self, email, password):
        try:
            self.cursor.execute(
                "INSERT INTO users VALUES (?, ?)", (email, password)
            )
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def userExists(self, email, password):
        self.cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )
        return self.cursor.fetchone() is not None
    
    def createBusiness(self, businessName, businessType): 
        try: 
             self.pibbitCursor.execute(
                "INSERT INTO pibbit VALUES (?, ?)", (businessName, businessType)
            )
             self.pibbitConnection.commit()
             return True
        except sqlite3.IntegrityError:
            return False
            
           
        