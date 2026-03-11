import sqlite3

class Database:
    def __init__(self):
        # Connection to user.db database for login and signup
        self.connection = sqlite3.connect("users.db")
        self.cursor = self.connection.cursor()
        
        # Connection to the pibbit.sqlite database file
        self.pibbitConnection = sqlite3.connect("pibbit.sqlite")
        self.pibbitCursor = self.pibbitConnection.cursor()
        
        self.createTable()
        

    # ───────────────────────────────────────────────
    # CREATE NECESSARY TABLES
    # ───────────────────────────────────────────────

    def createTable(self):
        # Users + Bookmarks (users.db)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                email TEXT PRIMARY KEY,
                password TEXT NOT NULL
            )
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookmarks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_email TEXT NOT NULL,
                biz_id INTEGER NOT NULL,
                UNIQUE(user_email, biz_id)
            )
        """)
        self.connection.commit()
        
        # PIBBIT TABLES
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
                city_id INTEGER,
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


    # ───────────────────────────────────────────────
    # USER + BOOKMARK LOGIC
    # ───────────────────────────────────────────────

    def isBookmarked(self, email, biz_id):
        self.cursor.execute("SELECT 1 FROM bookmarks WHERE user_email=? AND biz_id=?", 
                            (email, biz_id))
        return self.cursor.fetchone() is not None
    

    def toggleBookmark(self, email, biz_id):
        if self.isBookmarked(email, biz_id):
            self.cursor.execute("DELETE FROM bookmarks WHERE user_email=? AND biz_id=?", 
                                (email, biz_id))
            self.connection.commit()
            return "removed"
        else:
            self.cursor.execute("INSERT INTO bookmarks (user_email, biz_id) VALUES (?, ?)", 
                                (email, biz_id))
            self.connection.commit()
            return "added"


    def fetchBookmarkedBusinesses(self, email):
        self.cursor.execute("SELECT biz_id FROM bookmarks WHERE user_email=?", (email,))
        ids = [row[0] for row in self.cursor.fetchall()]
        if not ids: 
            return []
        
        placeholders = ', '.join(['?'] * len(ids))
        query = f"""
            SELECT biz_id, biz_name, rating, review_count, description, website_link 
            FROM businesses 
            WHERE biz_id IN ({placeholders})
        """
        
        self.pibbitCursor.execute(query, ids)
        return self.pibbitCursor.fetchall()


    # ───────────────────────────────────────────────
    # LOGIN/SIGNUP
    # ───────────────────────────────────────────────

    def addUser(self, email, password):
        try:
            self.cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", 
                                (email, password))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False


    def userExists(self, email, password):
        self.cursor.execute("SELECT * FROM users WHERE email=? AND password=?", 
                            (email, password))
        return self.cursor.fetchone() is not None


    # ───────────────────────────────────────────────
    # BUSINESS CREATION
    # ───────────────────────────────────────────────

    # FIXED: Now inserts all 6 fields expected by display + recommendations
    def createBusiness(self, name, description, sub_id, website_link="", city_id=None):
        try:
            self.pibbitCursor.execute("""
                INSERT INTO businesses 
                (biz_name, description, sub_id, rating, review_count, website_link, city_id)
                VALUES (?, ?, ?, 0.0, 0, ?, ?)
            """, (name, description, sub_id, website_link, city_id))

            self.pibbitConnection.commit()
            return True
        except sqlite3.Error as e:
            print("Create business error:", e)
            return False


    # ───────────────────────────────────────────────
    # RATINGS
    # ───────────────────────────────────────────────

    def updateBusinessRating(self, biz_id, new_score):
        try:
            self.pibbitCursor.execute(
                "SELECT rating, review_count FROM businesses WHERE biz_id = ?", 
                (biz_id,)
            )
            data = self.pibbitCursor.fetchone()

            current_rating = float(data[0]) if data[0] is not None else 0.0
            current_count = int(data[1]) if data[1] is not None else 0

            new_count = current_count + 1
            new_average = ((current_rating * current_count) + new_score) / new_count

            self.pibbitCursor.execute("""
                UPDATE businesses 
                SET rating = ?, review_count = ?
                WHERE biz_id = ?
            """, (round(new_average, 1), new_count, biz_id))

            self.pibbitConnection.commit()
            return True

        except sqlite3.Error as e:
            print("Rating update error:", e)
            return False


    # ───────────────────────────────────────────────
    # REVIEW SYSTEM (FIXED!)
    # ───────────────────────────────────────────────

    # FIXED: Review count now increments
    def saveReview(self, userEmail, biz_id, reviewInputText):
        try:
            self.pibbitCursor.execute("""
                INSERT INTO reviews (biz_id, user_email, comment)
                VALUES (?, ?, ?)
            """, (biz_id, userEmail, reviewInputText))

            # Increase official review_count
            self.pibbitCursor.execute("""
                UPDATE businesses
                SET review_count = COALESCE(review_count, 0) + 1
                WHERE biz_id = ?
            """, (biz_id,))

            self.pibbitConnection.commit()
            return "added"

        except sqlite3.Error as e:
            print("Review insert error:", e)
            return None


    # ───────────────────────────────────────────────
    # BUSINESS + CATEGORY FETCHING
    # ───────────────────────────────────────────────

    def fetchCategories(self):
        self.pibbitCursor.execute("SELECT cat_id, cat_name FROM categories ORDER BY cat_id ASC")
        return self.pibbitCursor.fetchall()


    def fetchSubcategories(self, cat_id):
        self.pibbitCursor.execute(
            "SELECT sub_id, sub_name FROM subcategories WHERE cat_id=? ORDER BY sub_name ASC",
            (cat_id,)
        )
        return self.pibbitCursor.fetchall()


    def fetchBusinessesBySubs(self, sub_id):
        self.pibbitCursor.execute("""
            SELECT biz_id, biz_name, rating, review_count, description, website_link
            FROM businesses
            WHERE sub_id = ?
            ORDER BY biz_name ASC
        """, (sub_id,))
        return self.pibbitCursor.fetchall()


    def fetchAllBusinesses(self):
        self.pibbitCursor.execute("""
            SELECT biz_id, biz_name, rating, review_count, description, website_link
            FROM businesses
            ORDER BY biz_name ASC
        """)
        return self.pibbitCursor.fetchall()


    # ───────────────────────────────────────────────
    # CITY FILTERING
    # ───────────────────────────────────────────────

    def fetchCities(self):
        self.pibbitCursor.execute("SELECT city_id, city_name FROM cities ORDER BY city_id ASC")
        return self.pibbitCursor.fetchall()


    def fetchBusinessByCity(self, city_id):
        self.pibbitCursor.execute("""
            SELECT biz_id, biz_name, rating, review_count, description, website_link
            FROM businesses
            WHERE city_id = ?
            ORDER BY biz_name ASC
        """, (city_id,))
        return self.pibbitCursor.fetchall()


    # ───────────────────────────────────────────────
    # COUPONS
    # ───────────────────────────────────────────────

    def fetchCouponsByBusiness(self, biz_id):
        self.pibbitCursor.execute("""
            SELECT title, description, coupon_code
            FROM coupons
            WHERE biz_id = ?
        """, (biz_id,))
        return self.pibbitCursor.fetchall()


    def fetchAllCoupons(self):
        self.pibbitCursor.execute("""
            SELECT b.biz_name, c.title, c.description, c.coupon_code
            FROM coupons c
            INNER JOIN businesses b ON c.biz_id = b.biz_id
        """)
        return self.pibbitCursor.fetchall()


    # ───────────────────────────────────────────────
    # RECOMMENDATION SUPPORT (FIXED!)
    # ───────────────────────────────────────────────

    # FIXED: Filter out NULL subcategories
    def fetchUserReviewedCategories(self, userEmail):
        self.pibbitCursor.execute("""
            SELECT b.sub_id
            FROM reviews r
            JOIN businesses b ON r.biz_id = b.biz_id
            WHERE r.user_email = ? AND b.sub_id IS NOT NULL
        """, (userEmail,))
        return [row[0] for row in self.pibbitCursor.fetchall()]


    # FIXED: Never return None — use -1 instead
    def getBusinessSubId(self, biz_id):
        self.pibbitCursor.execute("SELECT sub_id FROM businesses WHERE biz_id = ?", (biz_id,))
        result = self.pibbitCursor.fetchone()
        return result[0] if result and result[0] is not None else -1


    # ───────────────────────────────────────────────

    def close(self):
        self.connection.close()
        self.pibbitConnection.close()