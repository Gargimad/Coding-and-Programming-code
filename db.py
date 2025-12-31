import sqlite3

class Database:
    def __init__(self):
        self.connection = sqlite3.connect("users.db")
        self.cursor = self.connection.cursor()
        
        self.pibbitConnection = sqlite3.connect("pibbit.sqlite")
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
        
        # Removed the trailing comma after FLOAT
        self.pibbitCursor.execute("""
            CREATE TABLE IF NOT EXISTS pibbit (
                businessType TEXT NOT NULL,
                businessName TEXT NOT NULL,
                rating FLOAT,
                subType TEXT,
                trending BOOLEAN,
                bookmarked BOOLEAN, 
                bussID INTEGER
            )
        """)
        self.pibbitConnection.commit()

    def addUser(self, email, password):
        try:
            # Note: In a real app, hash the password before saving!
            self.cursor.execute(
                "INSERT INTO users (email, password) VALUES (?, ?)", (email, password)
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
            # Added explicit column names and handled the 3rd column (rating) as NULL/default
            self.pibbitCursor.execute(
                "INSERT INTO pibbit (businessName, businessType, rating) VALUES (?, ?, ?)", 
                (businessName, businessType, 0.0) 
            )
            self.pibbitConnection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False

    def close(self):
        self.connection.close()
        self.pibbitConnection.close()