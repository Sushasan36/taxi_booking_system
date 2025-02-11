  
import tkinter as tk  
from tkinter import messagebox  
from database import get_db_connection  
  
class FeedbackWindow:  
    """  
    Window for submitting feedback after completing a ride.  
    """  
    def __init__(self, master, booking_id, user_id, role):  
        self.master = tk.Toplevel(master)  
        self.booking_id = booking_id  
        self.user_id = user_id  
        self.role = role  # 'Customer' or 'Driver'  
        self.rating = tk.IntVar()  
        self.comment = tk.StringVar()  
        self.create_widgets()  
  
    def create_widgets(self):  
        """  
        Creates the feedback interface widgets.  
        """  
        header_text = 'Provide Feedback for Booking ID ' + str(self.booking_id)  
        header = tk.Label(self.master, text=header_text, font=('Helvetica', 16))  
        header.pack(pady=10)  
  
        # Rating  
        tk.Label(self.master, text='Rating (1-5):', font=('Helvetica', 14)).pack(pady=5)  
        rating_frame = tk.Frame(self.master)  
        rating_frame.pack(pady=5)  
        for i in range(1, 6):  
            tk.Radiobutton(rating_frame, text=str(i), variable=self.rating, value=i, font=('Helvetica', 14)).pack(side='left')  
  
        # Comment  
        tk.Label(self.master, text='Comment:', font=('Helvetica', 14)).pack(pady=5)  
        tk.Entry(self.master, textvariable=self.comment, font=('Helvetica', 14), width=50).pack(pady=5)  
  
        # Submit Button  
        submit_btn = tk.Button(self.master, text='Submit Feedback', font=('Helvetica', 14), command=self.submit_feedback)  
        submit_btn.pack(pady=10)  
  
    def submit_feedback(self):  
        """  
        Saves the feedback to the database.  
        """  
        rating = self.rating.get()  
        comment = self.comment.get()  
  
        if rating == 0:  
            messagebox.showerror('Error', 'Please select a rating.')  
            return  
  
        conn = get_db_connection()  
        c = conn.cursor()  
        c.execute('''  
            INSERT INTO feedbacks (booking_id, user_id, rating, comment, role)  
            VALUES (?, ?, ?, ?, ?)  
        ''', (self.booking_id, self.user_id, rating, comment, self.role))  
        c.execute('UPDATE bookings SET feedback_given=1 WHERE booking_id=?', (self.booking_id,))  
        conn.commit()  
        conn.close()  
  
        messagebox.showinfo('Success', 'Thank you for your feedback!')  
        self.master.destroy()  