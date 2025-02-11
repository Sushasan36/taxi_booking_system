
  
import tkinter as tk  
from tkinter import ttk  
from tkinter import messagebox  
from database import get_db_connection  
from feedback_window import FeedbackWindow  
  
class DriverDashboard:  
    """  
    Driver dashboard where drivers can view and manage their assigned rides.  
    """  
    def __init__(self, master, user_id):  
        self.master = tk.Toplevel(master)  
        self.master.title('Driver Dashboard')  
        self.master.geometry('800x700')  
        self.user_id = user_id  # Logged-in driver's user ID  
        self.is_dark_mode = False  
        self.style = ttk.Style()  
        self.create_widgets()  
  
    def create_widgets(self):  
        """  
        Creates the driver dashboard interface widgets.  
        """  
        # Theme Toggle Button  
        theme_btn = tk.Button(self.master, text='Dark Mode', command=self.toggle_theme)  
        theme_btn.place(x=10, y=10)  
  
        header = tk.Label(self.master, text='Driver Dashboard', font=('Helvetica', 24))  
        header.pack(pady=20)  
  
        # Treeview for assigned bookings  
        self.tree = ttk.Treeview(self.master, columns=('Booking ID', 'Customer', 'Pickup', 'Dropoff', 'Pooling', 'Car Type', 'Date', 'Time', 'Status'), show='headings')  
        self.tree.heading('Booking ID', text='ID')  
        self.tree.heading('Customer', text='Customer')  
        self.tree.heading('Pickup', text='Pickup')  
        self.tree.heading('Dropoff', text='Dropoff')  
        self.tree.heading('Pooling', text='Pooling')  
        self.tree.heading('Car Type', text='Car Type')  
        self.tree.heading('Date', text='Date')  
        self.tree.heading('Time', text='Time')  
        self.tree.heading('Status', text='Status')  
  
        for col in self.tree['columns']:  
            self.tree.column(col, width=100)  
  
        self.tree.pack(fill='both', expand=True)  
  
        # Buttons  
        btn_frame = tk.Frame(self.master)  
        btn_frame.pack(pady=10)  
        complete_btn = tk.Button(btn_frame, text='Mark as Completed', font=('Helvetica', 14), command=self.complete_booking)  
        complete_btn.pack(side='left', padx=10)  
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
        Loads and displays the driver's assigned bookings.  
        """  
        # Clear the treeview  
        for row in self.tree.get_children():  
            self.tree.delete(row)  
  
        conn = get_db_connection()  
        c = conn.cursor()  
        c.execute('''  
            SELECT bookings.booking_id, customers.username AS customer, bookings.pickup, bookings.dropoff,  
                   bookings.pooling, bookings.car_type, bookings.date, bookings.time, bookings.status  
            FROM bookings  
            JOIN users AS customers ON bookings.customer_id = customers.user_id  
            WHERE bookings.status IN ("Approved", "Completed", "Pending")  
        ''')  
        bookings = c.fetchall()  
        print(bookings)
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
                booking['status']  
            ))  
  
    def complete_booking(self):  
        """  
        Marks the selected booking as completed.  
        """  
        selected_item = self.tree.selection()  
        if not selected_item:  
            messagebox.showerror('Error', 'Please select a booking to mark as completed.')  
            return  
  
        booking_id = self.tree.item(selected_item)['values'][0]  
        status = self.tree.item(selected_item)['values'][8]  
  
        if status == 'Completed':  
            messagebox.showerror('Error', 'Booking already completed.')  
            return  
  
        # Update the booking status in the database  
        conn = get_db_connection()  
        c = conn.cursor()  
        c.execute('UPDATE bookings SET status="Completed" WHERE booking_id=?', (booking_id,))  
        conn.commit()  
        conn.close()  
  
        messagebox.showinfo('Success', f'Booking {booking_id} marked as completed.')  
        self.load_bookings()  
  
        # Open Feedback Window  
        FeedbackWindow(self.master, booking_id, self.user_id, 'Driver')  