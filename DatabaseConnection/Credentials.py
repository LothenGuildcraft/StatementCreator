import os
import tkinter as tk
from dotenv import load_dotenv, set_key

class Credentials:

    environmentPath = os.path.relpath('DatabaseConnection\\Credentials\\.env')

    def __init__(self):
        
        load_dotenv(self.environmentPath)

        self.user = os.getenv('DBUsername')
        self.password = os.getenv('Password')
        self.dsn = os.getenv('DSN')
    
    def popupmsg(self):
        credentials = tk.Tk()
        credentials.title("Database Credentials")
        credentials.geometry("300x150")
        
        username = tk.Label(credentials, text = "Username: ")
        usernameInput = tk.Entry(credentials)
        usernameInput.insert(0, self.user)
        username.grid(row=0, column=0)
        usernameInput.grid(row=0, column=1)

        password = tk.Label(credentials, text = "Password: ")
        passwordInput = tk.Entry(credentials, show="*")
        passwordInput.insert(0, self.password)
        password.grid(row=1, column=0)
        passwordInput.grid(row=1, column=1)

        dsn = tk.Label(credentials, text = "DSN: ")
        dsnInput = tk.Entry(credentials)
        dsnInput.insert(0, self.dsn)
        dsn.grid(row=2, column=0)
        dsnInput.grid(row=2, column=1)

        submitButton = tk.Button(credentials, text="Submit", command=lambda: self.submit(credentials, usernameInput, passwordInput, dsnInput))
        submitButton.grid(row=3, column=0)
        
        credentials.mainloop()

    def submit(self, root, usernameInput, passwordInput, dsnInput):
        self.user = usernameInput.get()
        self.password = passwordInput.get()
        self.dsn = dsnInput.get()
        set_key(dotenv_path=self.environmentPath, key_to_set='DBUsername', value_to_set=self.user)
        set_key(dotenv_path=self.environmentPath, key_to_set='Password', value_to_set=self.password)
        set_key(dotenv_path=self.environmentPath, key_to_set='DSN', value_to_set=self.dsn)
        root.destroy()
