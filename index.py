import tkinter as tk  
from tkinter import ttk  
from tkinter import messagebox as ms  
import sqlite3  
import random  
import time  
import datetime  
  
# Initialize the main application window  
root = tk.Tk()  
  
# Database setup  
with sqlite3.connect('Users.db') as db:  
    c = db.cursor()  
# Create user table with role field  
c.execute('''  
    CREATE TABLE IF NOT EXISTS user (  
        username TEXT NOT NULL,  
        password TEXT NOT NULL,  
        role TEXT NOT NULL  
    )  
''')  
# Create bookings table  
c.execute('''  
    CREATE TABLE IF NOT EXISTS bookings (  
        booking_id INTEGER PRIMARY KEY AUTOINCREMENT,  
        customer TEXT NOT NULL,  
        pickup TEXT NOT NULL,  
        dropoff TEXT NOT NULL,  
        pooling INTEGER NOT NULL,  
        car_type TEXT NOT NULL,  
        status TEXT NOT NULL,  
        assigned_driver TEXT  
    )  
''')  
db.commit()  
db.close()  
  
# Main application class  
class TaxiBookingApp:  
    def __init__(self, master):  
        self.master = master  
        self.master.title('Taxi Booking System')  
        self.master.geometry('500x400')  
        self.username = tk.StringVar()  
        self.password = tk.StringVar()  
        self.role = tk.StringVar(value='Customer')  # Default role  
        self.create_widgets()  
  
    def create_widgets(self):  
        # Header  
        self.header = tk.Label(self.master, text='Taxi Booking System', font=('Arial', 24))  
        self.header.pack(pady=10)  
  
        # Frame for Login/Signup  
        self.frame = tk.Frame(self.master)  
        self.frame.pack(pady=10)  
  
        # Username  
        tk.Label(self.frame, text='Username:', font=('Arial', 14)).grid(row=0, column=0, sticky='e')  
        tk.Entry(self.frame, textvariable=self.username, font=('Arial', 14)).grid(row=0, column=1)  
  
        # Password  
        tk.Label(self.frame, text='Password:', font=('Arial', 14)).grid(row=1, column=0, sticky='e')  
        tk.Entry(self.frame, textvariable=self.password, show='*', font=('Arial', 14)).grid(row=1, column=1)  
  
        # Role Selection  
        tk.Label(self.frame, text='Role:', font=('Arial', 14)).grid(row=2, column=0, sticky='e')  
        self.role_combo = ttk.Combobox(self.frame, textvariable=self.role, font=('Arial', 14), state='readonly')  
        self.role_combo['values'] = ('Customer', 'Admin', 'Driver')  
        self.role_combo.grid(row=2, column=1)  
        self.role_combo.current(0)  
  
        # Buttons  
        self.login_btn = tk.Button(self.master, text='Login', font=('Arial', 14), command=self.login)  
        self.login_btn.pack(pady=5)  
  
        self.signup_btn = tk.Button(self.master, text='Sign Up', font=('Arial', 14), command=self.signup_screen)  
        self.signup_btn.pack()  
  
    def login(self):  
        with sqlite3.connect('Users.db') as db:  
            c = db.cursor()  
        c.execute('SELECT * FROM user WHERE username=? AND password=? AND role=?',  
                  (self.username.get(), self.password.get(), self.role.get()))  
        result = c.fetchone()  
        if result:  
            ms.showinfo('Success', f'Welcome {self.username.get()}!')  
            self.master.withdraw()  # Hide login window  
            if self.role.get() == 'Customer':  
                CustomerDashboard(self.master, self.username.get())  
            elif self.role.get() == 'Admin':  
                AdminDashboard(self.master)  
            elif self.role.get() == 'Driver':  
                DriverDashboard(self.master, self.username.get())  
        else:  
            ms.showerror('Error', 'Invalid credentials!')  
  
    def signup_screen(self):  
        signup_win = tk.Toplevel()  
        signup_win.title('Sign Up')  
        signup_win.geometry('400x300')  
  
        tk.Label(signup_win, text='Username:', font=('Arial', 14)).grid(row=0, column=0, padx=10, pady=10)  
        username_entry = tk.Entry(signup_win, font=('Arial', 14))  
        username_entry.grid(row=0, column=1)  
  
        tk.Label(signup_win, text='Password:', font=('Arial', 14)).grid(row=1, column=0)  
        password_entry = tk.Entry(signup_win, show='*', font=('Arial', 14))  
        password_entry.grid(row=1, column=1)  
  
        tk.Label(signup_win, text='Role:', font=('Arial', 14)).grid(row=2, column=0)  
        role_var = tk.StringVar(value='Customer')  
        role_combo = ttk.Combobox(signup_win, textvariable=role_var, font=('Arial', 14), state='readonly')  
        role_combo['values'] = ('Customer', 'Driver')  # Admins are added manually  
        role_combo.grid(row=2, column=1)  
        role_combo.current(0)  
  
        def signup():  
            username = username_entry.get()  
            password = password_entry.get()  
            role = role_var.get()  
            with sqlite3.connect('Users.db') as db:  
                c = db.cursor()  
            c.execute('SELECT * FROM user WHERE username=?', (username,))  
            if c.fetchone():  
                ms.showerror('Error', 'Username already exists!')  
            else:  
                c.execute('INSERT INTO user(username, password, role) VALUES(?,?,?)', (username, password, role))  
                db.commit()  
                ms.showinfo('Success', 'Account created successfully!')  
                signup_win.destroy()  
  
        signup_btn = tk.Button(signup_win, text='Sign Up', font=('Arial', 14), command=signup)  
        signup_btn.grid(row=3, column=0, columnspan=2, pady=20)  
  
# Customer Dashboard  
class CustomerDashboard:  
    def __init__(self, master, username):  
        self.username = username  
        self.master = tk.Toplevel(master)  
        self.master.title('Customer Dashboard')  
        self.master.geometry('600x500')  
        self.create_widgets()  
  
    def create_widgets(self):  
        tk.Label(self.master, text=f'Welcome, {self.username}', font=('Arial', 24)).pack(pady=10)  
        # Booking Form  
        self.pickup = tk.StringVar()  
        self.dropoff = tk.StringVar()  
        self.pooling = tk.IntVar(value=1)  
        self.car_type = tk.StringVar(value='Standard')  
  
        form_frame = tk.Frame(self.master)  
        form_frame.pack(pady=20)  
  
        tk.Label(form_frame, text='Pickup Location:', font=('Arial', 14)).grid(row=0, column=0, sticky='e')  
        pickup_combo = ttk.Combobox(form_frame, textvariable=self.pickup, font=('Arial', 14), state='readonly')  
        pickup_combo['values'] = ('CampusCafe', 'AdmissionBlock', 'GirlsHostel', 'BoysHostel')  
        pickup_combo.grid(row=0, column=1)  
        pickup_combo.current(0)  
  
        tk.Label(form_frame, text='Dropoff Location:', font=('Arial', 14)).grid(row=1, column=0, sticky='e')  
        dropoff_combo = ttk.Combobox(form_frame, textvariable=self.dropoff, font=('Arial', 14), state='readonly')  
        dropoff_combo['values'] = ('CampusCafe', 'AdmissionBlock', 'GirlsHostel', 'BoysHostel')  
        dropoff_combo.grid(row=1, column=1)  
        dropoff_combo.current(1)  
  
        tk.Label(form_frame, text='Pooling:', font=('Arial', 14)).grid(row=2, column=0, sticky='e')  
        pooling_spin = tk.Spinbox(form_frame, from_=1, to=4, textvariable=self.pooling, font=('Arial', 14))  
        pooling_spin.grid(row=2, column=1)  
  
        tk.Label(form_frame, text='Car Type:', font=('Arial', 14)).grid(row=3, column=0, sticky='e')  
        car_type_combo = ttk.Combobox(form_frame, textvariable=self.car_type, font=('Arial', 14), state='readonly')  
        car_type_combo['values'] = ('Standard', 'PrimeSedan', 'PremiumSedan')  
        car_type_combo.grid(row=3, column=1)  
        car_type_combo.current(0)  
  
        book_btn = tk.Button(self.master, text='Book Ride', font=('Arial', 14), command=self.book_ride)  
        book_btn.pack(pady=10)  
  
    def book_ride(self):  
        # Insert booking into database  
        with sqlite3.connect('Users.db') as db:  
            c = db.cursor()  
        c.execute('''  
            INSERT INTO bookings(customer, pickup, dropoff, pooling, car_type, status)  
            VALUES(?,?,?,?,?,?)  
        ''', (self.username, self.pickup.get(), self.dropoff.get(), self.pooling.get(), self.car_type.get(), 'Pending'))  
        db.commit()  
        ms.showinfo('Success', 'Ride booked successfully! Waiting for admin approval.')  
  
# Admin Dashboard  
class AdminDashboard:  
    def __init__(self, master):  
        self.master = tk.Toplevel(master)  
        self.master.title('Admin Dashboard')  
        self.master.geometry('800x600')  
        self.create_widgets()  
  
    def create_widgets(self):  
        tk.Label(self.master, text='Admin Dashboard', font=('Arial', 24)).pack(pady=10)  
        # Bookings List  
        self.tree = ttk.Treeview(self.master, columns=('ID', 'Customer', 'Pickup', 'Dropoff', 'Pooling', 'Car Type', 'Status'), show='headings')  
        self.tree.heading('ID', text='ID')  
        self.tree.heading('Customer', text='Customer')  
        self.tree.heading('Pickup', text='Pickup')  
        self.tree.heading('Dropoff', text='Dropoff')  
        self.tree.heading('Pooling', text='Pooling')  
        self.tree.heading('Car Type', text='Car Type')  
        self.tree.heading('Status', text='Status')  
        self.tree.pack(fill='both', expand=True)  
  
        # Load bookings  
        self.load_bookings()  
  
        # Approve and Assign Driver  
        action_frame = tk.Frame(self.master)  
        action_frame.pack(pady=10)  
        tk.Button(action_frame, text='Approve Booking', command=self.approve_booking).grid(row=0, column=0, padx=10)  
        tk.Button(action_frame, text='Refresh', command=self.load_bookings).grid(row=0, column=1, padx=10)  
  
    def load_bookings(self):  
        # Clear existing data  
        for i in self.tree.get_children():  
            self.tree.delete(i)  
        # Fetch bookings from database  
        with sqlite3.connect('Users.db') as db:  
            c = db.cursor()  
        c.execute('SELECT * FROM bookings')  
        bookings = c.fetchall()  
        for booking in bookings:  
            self.tree.insert('', 'end', values=booking)  
  
    def approve_booking(self):  
        selected_item = self.tree.selection()  
        if not selected_item:  
            ms.showwarning('Warning', 'No booking selected!')  
            return  
        booking_id = self.tree.item(selected_item)['values'][0]  
        # Assign a driver randomly (for simplicity)  
        with sqlite3.connect('Users.db') as db:  
            c = db.cursor()  
        c.execute('SELECT username FROM user WHERE role=?', ('Driver',))  
        drivers = c.fetchall()  
        if not drivers:  
            ms.showerror('Error', 'No drivers available!')  
            return  
        assigned_driver = random.choice(drivers)[0]  
        # Update booking status and assigned driver  
        c.execute('UPDATE bookings SET status=?, assigned_driver=? WHERE booking_id=?', ('Approved', assigned_driver, booking_id))  
        db.commit()  
        ms.showinfo('Success', f'Booking {booking_id} approved and assigned to driver {assigned_driver}.')  
        self.load_bookings()  
  
# Driver Dashboard  
class DriverDashboard:  
    def __init__(self, master, username):  
        self.master = tk.Toplevel(master)  
        self.master.title('Driver Dashboard')  
        self.master.geometry('800x600')  
        self.username = username  
        self.create_widgets()  
  
    def create_widgets(self):  
        tk.Label(self.master, text=f'Driver Dashboard - {self.username}', font=('Arial', 24)).pack(pady=10)  
        # Assigned Bookings List  
        self.tree = ttk.Treeview(self.master, columns=('ID', 'Customer', 'Pickup', 'Dropoff', 'Pooling', 'Car Type', 'Status'), show='headings')  
        self.tree.heading('ID', text='ID')  
        self.tree.heading('Customer', text='Customer')  
        self.tree.heading('Pickup', text='Pickup')  
        self.tree.heading('Dropoff', text='Dropoff')  
        self.tree.heading('Pooling', text='Pooling')  
        self.tree.heading('Car Type', text='Car Type')  
        self.tree.heading('Status', text='Status')  
        self.tree.pack(fill='both', expand=True)  
  
        # Load bookings  
        self.load_bookings()  
  
        # Mark as Completed  
        action_frame = tk.Frame(self.master)  
        action_frame.pack(pady=10)  
        tk.Button(action_frame, text='Mark as Completed', command=self.complete_booking).grid(row=0, column=0, padx=10)  
        tk.Button(action_frame, text='Refresh', command=self.load_bookings).grid(row=0, column=1, padx=10)  
  
    def load_bookings(self):  
        # Clear existing data  
        for i in self.tree.get_children():  
            self.tree.delete(i)  
        # Fetch assigned bookings from database  
        with sqlite3.connect('Users.db') as db:  
            c = db.cursor()  
        c.execute('SELECT * FROM bookings WHERE assigned_driver=? AND status=?', (self.username, 'Approved'))  
        bookings = c.fetchall()  
        for booking in bookings:  
            self.tree.insert('', 'end', values=booking)  
  
    def complete_booking(self):  
        selected_item = self.tree.selection()  
        if not selected_item:  
            ms.showwarning('Warning', 'No booking selected!')  
            return  
        booking_id = self.tree.item(selected_item)['values'][0]  
        # Update booking status  
        with sqlite3.connect('Users.db') as db:  
            c = db.cursor()  
        c.execute('UPDATE bookings SET status=? WHERE booking_id=?', ('Completed', booking_id))  
        db.commit()  
        ms.showinfo('Success', f'Booking {booking_id} marked as completed.')  
        self.load_bookings()  
  
if __name__ == '__main__':  
    app = TaxiBookingApp(root)  
    root.mainloop()  