
import tkinter as tk  
from tkinter import ttk  
from tkinter import messagebox  
from database import get_db_connection  
import random  
  
class AdminDashboard:  
    """  
    Admin dashboard to manage bookings and assign drivers.  
    """  
    def __init__(self, master, user_id):  
        self.master = tk.Toplevel(master)  
        self.master.title('Admin Dashboard')  
        self.master.geometry('1000x700')  
        self.user_id = user_id  
        self.is_dark_mode = False  
        self.style = ttk.Style()  
        self.create_widgets()  
  
    def create_widgets(self):  
        """  
        Creates the admin dashboard interface widgets.  
        """  
        # Theme Toggle Button  
        theme_btn = tk.Button(self.master, text='Dark Mode', command=self.toggle_theme)
        theme_btn.place(x=10, y=10)  
  
        header = tk.Label(self.master, text='Admin Dashboard', font=('Helvetica', 24))  
        header.pack(pady=20)  
  
        # Treeview for displaying bookings  
        self.tree = ttk.Treeview(self.master, columns=('Booking ID', 'Customer', 'Pickup', 'Dropoff', 'Pooling', 'Car Type', 'Date', 'Time', 'Status', 'Driver'), show='headings')  
        self.tree.heading('Booking ID', text='ID')  
        self.tree.heading('Customer', text='Customer')  
        self.tree.heading('Pickup', text='Pickup')  
        self.tree.heading('Dropoff', text='Dropoff')  
        self.tree.heading('Pooling', text='Pooling')  
        self.tree.heading('Car Type', text='Car Type')  
        self.tree.heading('Date', text='Date')  
        self.tree.heading('Time', text='Time')  
        self.tree.heading('Status', text='Status')  
        self.tree.heading('Driver', text='Driver')  
  
        for col in self.tree['columns']:  
            self.tree.column(col, width=100)  
  
        self.tree.pack(fill='both', expand=True)  
  
        # Buttons  
        btn_frame = tk.Frame(self.master)  
        btn_frame.pack(pady=10)  
        approve_btn = tk.Button(btn_frame, text='Approve Booking', font=('Helvetica', 14), command=self.approve_booking)  
        approve_btn.pack(side='left', padx=10)  
        refresh_btn = tk.Button(btn_frame, text='Refresh', font=('Helvetica', 14), command=self.load_bookings)  
        refresh_btn.pack(side='left', padx=10)  
  
        self.load_bookings()  
  
    def toggle_theme(self):  
        """  
        Toggles between dark and light themes.  
        """  
        if self.is_dark_mode:  
            self.style.theme_use('arc')  # Light theme  
            self.is_dark_mode = False  
        else:  
            self.style.theme_use('equilux')  # Dark theme  
            self.is_dark_mode = True  
  
    def load_bookings(self):  
        """  
        Loads and displays all bookings in the treeview.  
        """  
        # Clear the treeview  
        for row in self.tree.get_children():  
            self.tree.delete(row)  
  
        conn = get_db_connection()  
        c = conn.cursor()  
        c.execute('''  
            SELECT bookings.booking_id, customers.username AS customer, bookings.pickup, bookings.dropoff,  
                   bookings.pooling, bookings.car_type, bookings.date, bookings.time, bookings.status,  
                   drivers.username AS driver  
            FROM bookings  
            JOIN users AS customers ON bookings.customer_id = customers.user_id  
            LEFT JOIN users AS drivers ON bookings.driver_id = drivers.user_id  
        ''')  
        bookings = c.fetchall()  
        conn.close()  
  
        for booking in bookings:  
            self.tree.insert('', 'end', values=(  
                booking['booking_id'],  
                booking['customer'],  
                booking['pickup'],  
                booking['dropoff'],  
                booking['pooling'],  
                booking['car_type'],  
                booking['date'],  
                booking['time'],  
                booking['status'],  
                booking['driver'] if booking['driver'] else 'Not Assigned'  
            ))  
  
    def approve_booking(self):  
        """  
        Approves the selected booking and assigns a driver.  
        """  
        selected_item = self.tree.selection()  
        if not selected_item:  
            messagebox.showerror('Error', 'Please select a booking to approve.')  
            return  
  
        booking_id = self.tree.item(selected_item)['values'][0]  
  
        # Assign a driver randomly  
        conn = get_db_connection()  
        c = conn.cursor()  
        c.execute('SELECT user_id FROM users WHERE role="Driver"')  
        drivers = c.fetchall()  
  
        if not drivers:  
            messagebox.showerror('Error', 'No drivers available.')  
            conn.close()  
            return  
  
        driver_id = random.choice(drivers)['user_id']  
  
        # Update the booking in the database  
        c.execute('UPDATE bookings SET status="Approved", driver_id=? WHERE booking_id=?', (driver_id, booking_id))  
        conn.commit()  
        conn.close()  
  
        messagebox.showinfo('Success', f'Booking {booking_id} approved and assigned to a driver.')  
        self.load_bookings()  