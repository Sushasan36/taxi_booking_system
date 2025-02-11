
import tkinter as tk  
from tkinter import ttk  
from tkinter import messagebox  
from tkcalendar import DateEntry  
from datetime import datetime  
from database import get_db_connection  
from feedback_window import FeedbackWindow  
  
class CustomerDashboard:  
    """  
    Customer dashboard where customers can book rides and view history.  
    """  
    def __init__(self, master, user_id):  
        self.master = tk.Toplevel(master)  
        self.master.title('Customer Dashboard')  
        self.master.geometry('800x700')  
        self.user_id = user_id  # Logged-in customer's user ID  
        self.pickup = tk.StringVar()  
        self.dropoff = tk.StringVar()  
        self.pooling = tk.IntVar(value=1)  
        self.car_type = tk.StringVar(value='Standard')  
        self.date = tk.StringVar()  
        self.time = tk.StringVar()  
        self.is_dark_mode = False  
        self.style = ttk.Style()  
        self.create_widgets()  
  
    def create_widgets(self):  
        """  
        Creates the customer dashboard interface widgets.  
        """  
        # Theme Toggle Button  
        theme_btn = tk.Button(self.master, text='Dark mode', command=self.toggle_theme)  
        theme_btn.place(x=10, y=10)  
  
        header = tk.Label(self.master, text='Book a Ride', font=('Helvetica', 24))  
        header.pack(pady=20)  
  
        frame = tk.Frame(self.master)  
        frame.pack(pady=10)  
  
        # Pickup location  
        tk.Label(frame, text='Pickup Location:', font=('Helvetica', 14)).grid(row=0, column=0, sticky='e', padx=5, pady=5)  
        pickup_menu = ttk.Combobox(frame, textvariable=self.pickup, values=['Ason', 'Boudhanath', 'Chabahil', 'Durbar Square', 'Ekalavya Park', 'Freak Street', 'Gongabu', 'Himalayan Heights', 'Indra Chowk', 'Jamsikhel', 'Kalimati',
                                    'Lalitpur', 'Maitighar', 'Naxal', 'Oasis Hotel', 'Patan', 'Sundhara', 'Thamel', 'Koteshwor', 'Balkhu', 'Bagbazar', 'Pashupatinath',
                                    'Lainchaur', 'New Road', 'Basundhara', 'Chhetrapati', 'Naya Bazaar', 'Gyaneshwor', 'Baneshwor', 'Maharajgunj', 'Purbanchal', 'Maitidevi', 'Teku', 'Kantipath', 'Swayambhunath',
                                     'Bhaktapur', 'Maha Laxmi', 'Balkot', 'Chobhar', 'Lalitpur Durbar Square', 'Kalimati', 'Chhetrapati', 'Shankhamul', 'Imadol', 'Gairidhara'], font=('Helvetica', 14), state='readonly')  
        pickup_menu.grid(row=0, column=1, padx=5, pady=5)  
        pickup_menu.current(0)  
  
        # Dropoff location  
        tk.Label(frame, text='Dropoff Location:', font=('Helvetica', 14)).grid(row=1, column=0, sticky='e', padx=5, pady=5)  
        dropoff_menu = ttk.Combobox(frame, textvariable=self.dropoff, values=['Ason', 'Boudhanath', 'Chabahil', 'Durbar Square', 'Ekalavya Park', 'Freak Street', 'Gongabu', 'Himalayan Heights',
                                                                              'Indra Chowk', 'Jamsikhel', 'Kalimati', 'Lalitpur', 'Maitighar', 'Naxal', 'Oasis Hotel', 'Patan', 'Sundhara', 'Thamel', 'Koteshwor', 'Balkhu', 'Bagbazar', 'Pashupatinath', 
                                                                              'Lainchaur', 'New Road', 'Basundhara', 'Chhetrapati', 'Naya Bazaar', 'Gyaneshwor', 'Baneshwor', 'Maharajgunj', 'Purbanchal', 'Maitidevi', 'Teku', 'Kantipath', 'Swayambhunath', 'Bhaktapur', 'Maha Laxmi', 'Balkot', 'Chobhar', 'Lalitpur Durbar Square', 
                                                                              'Kalimati', 'Chhetrapati', 'Shankhamul', 'Imadol', 'Gairidhara'], font=('Helvetica', 14), state='readonly')  
        dropoff_menu.grid(row=1, column=1, padx=5, pady=5)  
        dropoff_menu.current(1)  
        
       # Passenger Count
        tk.Label(frame, text="Passenger Count:", font=("Helvetica", 14)).grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.passenger_count = tk.Spinbox(frame, from_=1, to=8, font=("Helvetica", 14), state='readonly')
        self.passenger_count.grid(row=2, column=1, padx=5, pady=5)

        # Car Type
        tk.Label(frame, text="Car Type:", font=("Helvetica", 14)).grid(row=3, column=0, sticky="e", padx=5, pady=5)
        car_type_menu = ttk.Combobox(frame, textvariable=self.car_type, values=["Standard", "PrimeSedan", "PremiumSedan"], font=("Helvetica", 14), state="readonly")
        car_type_menu.grid(row=3, column=1, padx=5, pady=5)

        # Date Selection
        tk.Label(frame, text="Date:", font=("Helvetica", 14)).grid(row=4, column=0, sticky="e", padx=5, pady=5)
        date_entry = DateEntry(frame, textvariable=self.date, font=("Helvetica", 15), date_pattern="yyyy-mm-dd", mindate=datetime.today())
        date_entry.grid(row=4, column=1, padx=5, pady=5)
        self.date.set(date_entry.get_date().strftime("%Y-%m-%d"))

        # Time Selection
        tk.Label(frame, text="Time:", font=("Helvetica", 14)).grid(row=5, column=0, sticky="e", padx=5, pady=5)
        time_values = [f"{h:02d}:{m:02d}" for h in range(24) for m in (0, 30)]
        time_combo = ttk.Combobox(frame, textvariable=self.time, values=time_values, font=("Helvetica", 14), state="readonly")
        time_combo.grid(row=5, column=1, padx=5, pady=5)
        time_combo.current(0)

        # Fare Estimate Button
        fare_btn = tk.Button(self.master, text="Estimate Fare", font=("Helvetica", 18), command=self.estimate_fare)
        fare_btn.pack(pady=5)

        # Book Now Button
        book_btn = tk.Button(self.master, text="Book Now", font=("Helvetica", 14), command=self.book_ride)
        book_btn.pack(pady=5)

        # View Ride History Button
        history_btn = tk.Button(self.master, text="View Ride History", font=("Helvetica", 14), command=self.view_history)
        history_btn.pack(pady=5)
  
    def toggle_theme(self):  
        """  
        Toggles between dark and light themes.  
        """  
        if self.is_dark_mode:  
            self.style.theme_use('arc')  # Light theme  
            self.master.configure(bg='lightblue')  # Light mode background  
            self.is_dark_mode = False  
        else:  
            self.style.theme_use('equilux')  # Dark theme  
            self.master.configure(bg='#2b2b2b')  # Light black background  
            self.is_dark_mode = True
  
  
    def estimate_fare(self):  
        """  
        Estimates the fare based on selected options.  
        """  
        pickup = self.pickup.get()  
        dropoff = self.dropoff.get()  
        car_type = self.car_type.get()  
  
        # Simple distance mapping (example values)  
        distances = {  
            ('CampusCafe', 'AdmissionBlock'): 2,  
            ('CampusCafe', 'GirlsHostel'): 3,  
            ('CampusCafe', 'BoysHostel'): 4,  
            ('AdmissionBlock', 'GirlsHostel'): 1.5,  
            ('AdmissionBlock', 'BoysHostel'): 2.5,  
            ('GirlsHostel', 'BoysHostel'): 1,  
        }  
  
        distance = distances.get((pickup, dropoff)) or distances.get((dropoff, pickup)) or 5  
        base_fare = 50  # Base fare  
        per_km_rate = {'Standard': 10, 'PrimeSedan': 15, 'PremiumSedan': 20}  
        fare = base_fare + (distance * per_km_rate[car_type])  
  
        messagebox.showinfo('Estimated Fare', f'Estimated Fare: Rs {fare}')  
  
    def book_ride(self):  
        """  
        Handles ride booking and saves it to the database.  
        """  
        pickup = self.pickup.get()  
        dropoff = self.dropoff.get()  
        pooling = self.pooling.get()  
        car_type = self.car_type.get()  
        date = self.date.get()  
        time = self.time.get()  
  
        # Validate inputs  
        if pickup == '' or dropoff == '':  
            messagebox.showerror('Error', 'Please select pickup and dropoff locations.')  
            return  
        if date == '':  
            messagebox.showerror('Error', 'Please select a date.')  
            return  
        if time == '':  
            messagebox.showerror('Error', 'Please select a time.')  
            return  
  
        # Fare Calculation (same as in estimate_fare)  
        distances = {  
            ('CampusCafe', 'AdmissionBlock'): 2,  
            ('CampusCafe', 'GirlsHostel'): 3,  
            ('CampusCafe', 'BoysHostel'): 4,  
            ('AdmissionBlock', 'GirlsHostel'): 1.5,  
            ('AdmissionBlock', 'BoysHostel'): 2.5,  
            ('GirlsHostel', 'BoysHostel'): 1,  
        }  
  
        distance = distances.get((pickup, dropoff)) or distances.get((dropoff, pickup)) or 5  
        base_fare = 50  # Base fare  
        per_km_rate = {'Standard': 10, 'PrimeSedan': 15, 'PremiumSedan': 20}  
        fare = base_fare + (distance * per_km_rate[car_type])  
  
        # Insert booking into the database  
        conn = get_db_connection()  
        c = conn.cursor()  
        c.execute('''  
            INSERT INTO bookings (customer_id, pickup, dropoff, pooling, car_type, status, date, time, fare)  
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  
        ''', (self.user_id, pickup, dropoff, pooling, car_type, 'Pending', date, time, fare))  
        conn.commit()  
        conn.close()  
  
        messagebox.showinfo('Success', 'Your ride has been booked and is pending approval.')  
  
    def view_history(self):  
        """  
        Opens the ride history window.  
        """  
        RideHistoryWindow(self.master, self.user_id)  
  
class RideHistoryWindow:  
    """  
    Displays the customer's ride history.  
    """  
    def __init__(self, master, user_id):  
        self.master = tk.Toplevel(master)  
        self.master.title('Ride History')  
        self.master.geometry('800x400')  
        self.user_id = user_id  
        self.create_widgets()  
  
    def create_widgets(self):  
        """  
        Creates the ride history interface widgets.  
        """  
        header = tk.Label(self.master, text='Your Ride History', font=('Helvetica', 18))  
        header.pack(pady=10)  
  
        # Treeview for displaying ride history  
        self.tree = ttk.Treeview(self.master, columns=('Booking ID', 'Pickup', 'Dropoff', 'Date', 'Time', 'Status', 'Fare', 'Feedback'), show='headings')  
        self.tree.heading('Booking ID', text='ID')  
        self.tree.heading('Pickup', text='Pickup')  
        self.tree.heading('Dropoff', text='Dropoff')  
        self.tree.heading('Date', text='Date')  
        self.tree.heading('Time', text='Time')  
        self.tree.heading('Status', text='Status')  
        self.tree.heading('Fare', text='Fare')  
        self.tree.heading('Feedback', text='Feedback')  
  
        for col in ('Booking ID', 'Pickup', 'Dropoff', 'Date', 'Time', 'Status', 'Fare', 'Feedback'):  
            self.tree.column(col, width=100)  
  
        self.tree.pack(fill='both', expand=True)  
  
        self.load_history()  
  
        # Feedback Button  
        feedback_btn = tk.Button(self.master, text='Give Feedback', font=('Helvetica', 14), command=self.give_feedback)  
        feedback_btn.pack(pady=10)  
  
    def load_history(self):  
        """  
        Loads and displays the customer's ride history.  
        """  
        for row in self.tree.get_children():  
            self.tree.delete(row)  
  
        conn = get_db_connection()  
        c = conn.cursor()  
        c.execute('''  
            SELECT booking_id, pickup, dropoff, date, time, status, fare, feedback_given  
            FROM bookings  
            WHERE customer_id=?  
        ''', (self.user_id,))  
        bookings = c.fetchall()  
        conn.close()  
  
        for booking in bookings:  
            feedback_status = 'Yes' if booking['feedback_given'] else 'No'  
            self.tree.insert('', 'end', values=(  
                booking['booking_id'],  
                booking['pickup'],  
                booking['dropoff'],  
                booking['date'],  
                booking['time'],  
                booking['status'],  
                booking['fare'],  
                feedback_status  
            ))  
  
    def give_feedback(self):  
        """  
        Opens the feedback window.  
        """  
        selected_item = self.tree.selection()  
        if not selected_item:  
            messagebox.showerror('Error', 'Please select a booking to give feedback.')  
            return  
  
        booking_id = self.tree.item(selected_item)['values'][0]  
        feedback_given = self.tree.item(selected_item)['values'][7]  
  
        if feedback_given == 'Yes':  
            messagebox.showerror('Error', 'Feedback already given for this booking.')  
            return  
  
        FeedbackWindow(self.master, booking_id, self.user_id, 'Customer')  