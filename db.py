'''
Gargi Madala, Grace Wu, Dhanvi Ramkumar
Pibbit Database
FBLA- Coding and Programming
26 January 2026
'''
import sqlite3

class Database:
    def __init__(self):
        #Connection to user.db database for login and signup
        self.connection = sqlite3.connect("users.db")
        self.cursor = self.connection.cursor()
        
        #Connection to the pibbit.sqlite database file
        self.pibbitConnection = sqlite3.connect("pibbit.sqlite")
        self.pibbitCursor = self.pibbitConnection.cursor()
        
        self.createTable()
        
    #Creating all tables if not existing
    def createTable(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                email TEXT PRIMARY KEY,
                password TEXT NOT NULL
            )
        """)
        #Bookmark table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookmarks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_email TEXT NOT NULL,
                biz_id INTEGER NOT NULL,
                UNIQUE(user_email, biz_id)
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
            CREATE TABLE IF NOT EXISTS coupons (
                coupon_id INTEGER PRIMARY KEY,
                biz_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                coupon_code TEXT NOT NULL,
                FOREIGN KEY(biz_id) REFERENCES businesses(biz_id)
            );
            CREATE TABLE IF NOT EXISTS reviews (
                review_id INTEGER PRIMARY KEY AUTOINCREMENT,
                biz_id INTEGER NOT NULL, 
                user_email TEXT NOT NULL,
                comment TEXT,
                FOREIGN KEY(biz_id) REFERENCES businesses(biz_id)
            );
        """)
        self.pibbitConnection.commit()

    #Bookmarks logic------------------------------------------------------------------------------------------------------------------
    #Checks if business is bookmarked based on email and business ID
    def isBookmarked(self, email, biz_id):
        self.cursor.execute("SELECT 1 FROM bookmarks WHERE user_email=? AND biz_id=?", (email, biz_id))
        return self.cursor.fetchone() is not None
    
    #Keeps track of bookmarks
    def toggleBookmark(self, email, biz_id):
        if self.isBookmarked(email, biz_id):
            self.cursor.execute("DELETE FROM bookmarks WHERE user_email=? AND biz_id=?", (email, biz_id))
            self.connection.commit()
            return "removed"
        else:
            self.cursor.execute("INSERT INTO bookmarks (user_email, biz_id) VALUES (?, ?)", (email, biz_id))
            self.connection.commit()
            return "added"
    #Puts the bookmarks in one place
    def fetchBookmarkedBusinesses(self, email):
        self.cursor.execute("SELECT biz_id FROM bookmarks WHERE user_email=?", (email,))
        ids = [row[0] for row in self.cursor.fetchall()]
        if not ids: return []
        placeholders = ', '.join(['?'] * len(ids))
        query = f"SELECT biz_id, biz_name, rating, review_count, description, website_link FROM businesses WHERE biz_id IN ({placeholders})"
        self.pibbitCursor.execute(query, ids)
        return self.pibbitCursor.fetchall()
    
    #Email, login, signup Logic--------------------------------------------------------------------------------------------------------
    def addUser(self, email, password):
        try:
            self.cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    def userExists(self, email, password):
        self.cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        return self.cursor.fetchone() is not None
    
    #Creates Businesses
    def createBusiness(self, businessName, businessDescription, sub_id): 
        try: 
            self.pibbitCursor.execute(
                "INSERT INTO businesses (biz_name, description, sub_id, rating, review_count) VALUES (?, ?, ?, ?, ?)", 
                (businessName, businessDescription, sub_id, 0.0, 0) 
            )
            self.pibbitConnection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False

    #Updates Business Rating after each user inputs rating
    def updateBusinessRating(self, biz_id, new_score):
        try:
            print(f"Business ID: {biz_id}")
            # Get current rating and review count
            self.pibbitCursor.execute("SELECT rating, review_count FROM businesses WHERE biz_id = ?", (biz_id,))
            data = self.pibbitCursor.fetchone()
            
            # Use 0.0 if rating is None, otherwise use the float value
            current_rating = float(data[0]) if data[0] is not None else 0.0
            current_count = int(data[1]) if data[1] is not None else 0
            # Recalculate average
            new_count = current_count + 1
            new_average = ((current_rating * current_count) + new_score) / new_count
            # Update the database with the rounded average
            self.pibbitCursor.execute("""
                UPDATE businesses 
                SET rating = ?, review_count = ? 
                WHERE biz_id = ?
            """, (round(new_average, 1), new_count, biz_id))
            
            self.pibbitConnection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Rating update error: {e}")
            return False
    #Businesses logic for the explore button
    #Fetches categories
    def fetchCategories(self):
        self.pibbitCursor.execute("SELECT cat_id, cat_name FROM categories ORDER BY cat_id ASC")
        return self.pibbitCursor.fetchall()
    #Fetches subcategories
    def fetchSubcategories(self, cat_id):
        self.pibbitCursor.execute("SELECT sub_id, sub_name FROM subcategories WHERE cat_id = ? ORDER BY sub_name ASC", (cat_id,))
        return self.pibbitCursor.fetchall()
    #Fetches businesses by subcategories- used for effective sorting
    def fetchBusinessesBySubs(self, sub_id):
        self.pibbitCursor.execute("SELECT biz_id, biz_name, rating, review_count, description, website_link FROM businesses WHERE sub_id = ? ORDER by biz_name ASC", (sub_id,))
        return self.pibbitCursor.fetchall()
    #Fetching all the businesses
    def fetchAllBusinesses(self):
        self.pibbitCursor.execute("SELECT biz_id, biz_name, rating, review_count, description, website_link FROM businesses ORDER by biz_name ASC")
        return self.pibbitCursor.fetchall()
    #Fetching cities for georgia community selection
    def fetchCities(self):
        self.pibbitCursor.execute("SELECT city_id, city_name FROM cities ORDER BY city_id ASC")
        return self.pibbitCursor.fetchall()
    #Used for filtering business by city
    def fetchBusinessByCity(self, city_id):
        self.pibbitCursor.execute("SELECT biz_id, biz_name, rating, review_count, description, website_link FROM businesses WHERE city_id = ? ORDER by biz_name ASC", (city_id,))
        return self.pibbitCursor.fetchall()
    #Coupons by businesses
    def fetchCouponsByBusiness(self, biz_id):
        query = """
        SELECT title, description, coupon_code 
        FROM coupons 
        WHERE biz_id = ?
        """
        self.pibbitCursor.execute(query, (biz_id,)) # Added missing (biz_id,) parameter
        return self.pibbitCursor.fetchall()
    #Fetching alll the coupons
    def fetchAllCoupons(self):
        query = """
        SELECT b.biz_name, c.title, c.description, c.coupon_code 
        FROM coupons c
        INNER JOIN businesses b ON c.biz_id = b.biz_id
        """
        self.pibbitCursor.execute(query)
        return self.pibbitCursor.fetchall()
    #Saving Reviews
    def saveReview(self, userEmail, biz_id, reviewInputText):
        print(f"User Email: {userEmail}")
        self.pibbitCursor.execute("INSERT INTO reviews (biz_id, user_email, comment) VALUES (?, ?, ?)", (biz_id, userEmail, reviewInputText))
        self.pibbitConnection.commit()
        return "added"

    def close(self):
        self.connection.close()
        self.pibbitConnection.close()