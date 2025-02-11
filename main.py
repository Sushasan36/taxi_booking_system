 
  
from ttkthemes import ThemedTk  
from login import LoginWindow  
from database import initialize_db  
  
def run_app():  
    """  
    Initializes the database and runs the application.  
    """  
    initialize_db()  # Initialize the database  
    root = ThemedTk(theme="arc")  # Start with a light theme  
    root.geometry('600x600')  
    app = LoginWindow(root)  
    root.mainloop()  
  
if __name__ == '__main__':  
    
 run_app()  
 
 
 
  

    
    
    