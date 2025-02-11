# database.py  
  
import sqlite3  
  
def get_db_connection():  
    """  
    Establishes and returns a connection to the SQLite database.  
    """  
    conn = sqlite3.connect('taxi_booking.db')  
    conn.row_factory = sqlite3.Row  # To access columns by name  
    return conn  
  
def initialize_db():  
    """  
    Initializes the database by creating the required tables if they don't exist.  
    """  
    conn = get_db_connection()  
    c = conn.cursor()  
    # Create users table  
    c.execute('''  
        CREATE TABLE IF NOT EXISTS users (  
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,  
            username TEXT NOT NULL UNIQUE,  
            password TEXT NOT NULL,  
            role TEXT NOT NULL  
        )  
    ''')  
    # Create bookings table  
    c.execute('''  
        CREATE TABLE IF NOT EXISTS bookings (  
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,  
            customer_id INTEGER NOT NULL,  
            pickup TEXT NOT NULL,  
            dropoff TEXT NOT NULL,  
            passanger count INTEGER NOT NULL,  
            car_type TEXT NOT NULL,  
            status TEXT NOT NULL,  
            driver_id INTEGER,  
            date TEXT NOT NULL,  
            time TEXT NOT NULL,  
            fare REAL NOT NULL,  
            feedback_given INTEGER DEFAULT 0,  
            FOREIGN KEY(customer_id) REFERENCES users(user_id),  
            FOREIGN KEY(driver_id) REFERENCES users(user_id)  
        )  
    ''')  
    # Create feedbacks table  
    c.execute('''  
        CREATE TABLE IF NOT EXISTS feedbacks (  
            feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,  
            booking_id INTEGER NOT NULL,  
            user_id INTEGER NOT NULL,  
            rating INTEGER NOT NULL,  
            comment TEXT,  
            role TEXT NOT NULL,  
            FOREIGN KEY(booking_id) REFERENCES bookings(booking_id),  
            FOREIGN KEY(user_id) REFERENCES users(user_id)  
        )  
    ''')  
    conn.commit()  
    conn.close()  