import sqlite3

class Database:
    def __init__(self):
        # Connection for user authentication
        self.connection = sqlite3.connect("users.db")
        self.cursor = self.connection.cursor()
        
        # Connection for the app data
        self.pibbitConnection = sqlite3.connect("pibbit.sqlite")
        self.pibbitCursor = self.pibbitConnection.cursor()
        
        self.createTable()
        
    def createTable(self):
        # 1. Create Users Table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                email TEXT PRIMARY KEY,
                password TEXT NOT NULL
            )
        """)
        self.connection.commit()
        self.pibbitCursor.executescript("""
            CREATE TABLE IF NOT EXISTS categories (
                cat_id INTEGER PRIMARY KEY,
                cat_name TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS subcategories (
                sub_id INTEGER PRIMARY KEY, 
                cat_id INTEGER,
                sub_name TEXT NOT NULL,
                FOREIGN KEY (cat_id) REFERENCES categories (cat_id)
            );

            CREATE TABLE IF NOT EXISTS businesses (
                biz_id INTEGER PRIMARY KEY,
                sub_id INTEGER,
                biz_name TEXT NOT NULL,
                rating REAL,
                review_count INTEGER,
                description TEXT,
                website_link TEXT,
                FOREIGN KEY(sub_id) REFERENCES subcategories(sub_id)
            );
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
    
    def createBusiness(self, businessName, businessDescription, sub_id): 
        try: 
            # Changed table name from 'pibbit' to 'businesses'
            # Added sub_id so the business is actually linked to a subcategory
            self.pibbitCursor.execute(
                "INSERT INTO businesses (biz_name, description, sub_id, rating, review_count) VALUES (?, ?, ?, ?, ?)", 
                (businessName, businessDescription, sub_id, 0.0, 0) 
            )
            self.pibbitConnection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
        
    def fetchCategories(self):
        self.pibbitCursor.execute(
            "SELECT cat_id, cat_name FROM categories ORDER BY cat_id ASC"
        )
        return self.pibbitCursor.fetchall()

    def fetchSubcategories(self, cat_id):
        self.pibbitCursor.execute(
            "SELECT sub_id, sub_name FROM subcategories WHERE cat_id = ? ORDER BY sub_name ASC",
            (cat_id,)
        )
        return self.pibbitCursor.fetchall()

    def fetchBusinessesBySubs(self, sub_id):
        self.pibbitCursor.execute(
            "SELECT biz_id, biz_name, rating, review_count, description, website_link FROM businesses WHERE sub_id = ? ORDER by biz_name ASC", 
            (sub_id,)
        )
        return self.pibbitCursor.fetchall()

    def close(self):
        self.connection.close()
        self.pibbitConnection.close()