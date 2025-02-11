
import sqlite3
import tkinter as tk  
from tkinter import ttk  
from tkinter import messagebox  
from ttkthemes import ThemedTk  
from PIL import Image, ImageTk  
from database import get_db_connection  
from customer_dashboard import CustomerDashboard  
from admin_dashboard import AdminDashboard  
from driver_dashboard import DriverDashboard  
import os  
  
class LoginWindow:  
    """  
    Handles user login functionality.  
    """  
    def __init__(self, master):  
        self.master = master  
        self.master.title('Taxi Booking System - Login')  
        self.master.geometry('600x600')  
        self.username = tk.StringVar()  
        self.password = tk.StringVar()  
        self.role = tk.StringVar(value='Customer')  
        self.admin_code = tk.StringVar()  
        self.is_dark_mode = False  
        self.style = ttk.Style()  
        self.create_widgets()  
  
    def create_widgets(self):  
        """  
        Creates the login interface widgets.  
        """  
        # Background Image  
        try:  
            bg_image_path = os.path.join('assets', 'background.jpg')  
            bg_image = Image.open(bg_image_path)  
            bg_image = bg_image.resize((600, 600), Image.ANTIALIAS)  
            bg_photo = ImageTk.PhotoImage(bg_image)  
            bg_label = tk.Label(self.master, image=bg_photo)  
            bg_label.image = bg_photo  
            bg_label.place(relwidth=1, relheight=1)  
        except Exception as e:  
            # If image not found, use a solid background color  
            self.master.configure(bg='lightblue')  
  
        # Theme Toggle Button  
        theme_btn = tk.Button(self.master, text='Dark Mode', command=self.toggle_theme)  
        theme_btn.place(x=10, y=10)  
  
        # Login Frame  
        login_frame = tk.Frame(self.master, bg='white', bd=5)  
        login_frame.place(relx=0.5, rely=0.5, anchor='center')  
  
        # Header  
        header = tk.Label(login_frame, text='Login', font=('Helvetica', 24, 'bold'), bg='white')  
        header.pack(pady=10)  
  
        # Username  
        tk.Label(login_frame, text='Username', font=('Helvetica', 14), bg='white').pack(pady=5)  
        tk.Entry(login_frame, textvariable=self.username, font=('Helvetica', 14)).pack()  
  
        # Password  
        tk.Label(login_frame, text='Password', font=('Helvetica', 14), bg='white').pack(pady=5)  
        tk.Entry(login_frame, textvariable=self.password, show='•', font=('Helvetica', 14)).pack()  
  
        # Role  
        tk.Label(login_frame, text='Login As', font=('Helvetica', 14), bg='white').pack(pady=5)  
        self.role_menu = ttk.Combobox(login_frame, textvariable=self.role, values=['Customer', 'Driver', 'Admin'], font=('Helvetica', 14), state='readonly')  
        self.role_menu.pack()  
        self.role_menu.bind('<<ComboboxSelected>>', self.show_admin_code_field)  
  
        # Admin Code (Hidden by default)  
        self.admin_code_label = tk.Label(login_frame, text='Admin Code', font=('Helvetica', 14), bg='white')  
        self.admin_code_entry = tk.Entry(login_frame, textvariable=self.admin_code, show='•', font=('Helvetica', 14))  
  
        # Login Button  
        login_btn = tk.Button(login_frame, text='Login', font=('Helvetica', 14), command=self.login)  
        login_btn.pack(pady=10)  
  
        # Sign Up Button  
        signup_btn = tk.Button(login_frame, text='Sign Up', font=('Helvetica', 14), command=self.open_signup_window)  
        signup_btn.pack() 
  
    def show_admin_code_field(self, event):  
        """  
        Shows or hides the admin code field based on the selected role.  
        """  
        role = self.role.get()  
        if role == 'Admin':  
            # Show admin code field  
            self.admin_code_label.pack(pady=5)  
            self.admin_code_entry.pack()  
        else:  
            # Hide admin code field  
            self.admin_code_label.pack_forget()  
            self.admin_code_entry.pack_forget()  
  
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
  
    def login(self):  
        """  
        Authenticates the user and opens the appropriate dashboard.  
        """  
        username = self.username.get()  
        password = self.password.get()  
        role = self.role.get()  
        admin_code = self.admin_code.get()  
  
        if role == 'Admin' and admin_code != 'ADMIN123':  # Replace with your actual admin code  
            messagebox.showerror('Error', 'Invalid admin code.')  
            return  
  
        conn = get_db_connection()  
        c = conn.cursor()  
        c.execute('SELECT user_id FROM users WHERE username=? AND password=? AND role=?', (username, password, role))  
        user = c.fetchone()  
        conn.close()  
  
        if user:  
            # Open the appropriate dashboard  
            self.master.withdraw()  # Hide the login window  
            if role == 'Customer':  
                CustomerDashboard(self.master, user['user_id'])  
            elif role == 'Admin':  
                AdminDashboard(self.master, user['user_id'])  
            elif role == 'Driver':  
                DriverDashboard(self.master, user['user_id'])  
        else:  
            messagebox.showerror('Error', 'Invalid username or password.')  
  
    def open_signup_window(self):  
        """  
        Opens the sign-up window.  
        """  
        SignupWindow(self.master)  
  
class SignupWindow:  
    """  
    Handles user sign-up functionality.  
    """  
    def __init__(self, master):  
        # Use the existing master instead of creating a new Toplevel window.
        self.master = master  
        self.master.title('Sign Up')  
        self.master.geometry('600x600')  
        self.username = tk.StringVar()  
        self.password = tk.StringVar()  
        self.role = tk.StringVar(value='Customer')  
        self.admin_code = tk.StringVar()  
        self.create_widgets()
  
  
    def create_widgets(self):  
        """  
        Creates the sign-up interface widgets.  
        """  
        # Sign Up Frame  
        signup_frame = tk.Frame(self.master, bg='white', bd=5)  
        signup_frame.place(relx=0.5, rely=0.5, anchor='center')  
  
        # Header  
        header = tk.Label(signup_frame, text='Sign Up', font=('Helvetica', 24, 'bold'), bg='white')  
        header.pack(pady=10)  
  
        # Username  
        tk.Label(signup_frame, text='Username', font=('Helvetica', 14), bg='white').pack(pady=5)  
        tk.Entry(signup_frame, textvariable=self.username, font=('Helvetica', 14)).pack()  
  
        # Password  
        tk.Label(signup_frame, text='Password', font=('Helvetica', 14), bg='white').pack(pady=5)  
        tk.Entry(signup_frame, textvariable=self.password, show='•', font=('Helvetica', 14)).pack()  
  
        # Role  
        tk.Label(signup_frame, text='Sign Up As', font=('Helvetica', 14), bg='white').pack(pady=5)  
        self.role_menu = ttk.Combobox(signup_frame, textvariable=self.role, values=['Customer', 'Driver', 'Admin'], font=('Helvetica', 14), state='readonly')  
        self.role_menu.pack()  
        self.role_menu.bind('<<ComboboxSelected>>', self.show_admin_code_field)  
  
        # Admin Code (Hidden by default)  
        self.admin_code_label = tk.Label(signup_frame, text='Admin Code', font=('Helvetica', 14), bg='white')  
        self.admin_code_entry = tk.Entry(signup_frame, textvariable=self.admin_code, show='•', font=('Helvetica', 14))  
  
        # Sign Up Button  
        signup_btn = tk.Button(signup_frame, text='Sign Up', font=('Helvetica', 14), command=self.signup)  
        signup_btn.pack(pady=10)
        
        # Back Button  
        back_btn = tk.Button(signup_frame, text='Back to Login', font=('Helvetica', 14), command=lambda: [signup_frame.destroy(), LoginWindow(self.master)])  
        back_btn.pack(pady=10)  # Add padding as needed
  
    def show_admin_code_field(self, event):  
        """  
        Shows or hides the admin code field based on the selected role.  
        """  
        role = self.role.get()  
        if role == 'Admin':  
            # Show admin code field  
            self.admin_code_label.pack(pady=5)  
            self.admin_code_entry.pack()  
        else:  
            # Hide admin code field  
            self.admin_code_label.pack_forget()  
            self.admin_code_entry.pack_forget()  
  
    def signup(self):  
        """  
        Registers a new user.  
        """  
        username = self.username.get()  
        password = self.password.get()  
        role = self.role.get()  
        admin_code = self.admin_code.get()  
  
        if username == '' or password == '':  
            messagebox.showerror('Error', 'Please fill all fields.')  
            return  
  
        if role == 'Admin':  
            if admin_code != 'ADMIN123':  # Replace with your secret admin code  
                messagebox.showerror('Error', 'Invalid admin code.')  
                return  
  
        conn = get_db_connection()  
        c = conn.cursor()  
        try:  
            c.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (username, password, role))  
            conn.commit()  
            messagebox.showinfo('Success', 'Account created successfully.')  
        except sqlite3.IntegrityError:  
            messagebox.showerror('Error', 'Username already exists.')  
        finally:  
            conn.close()  