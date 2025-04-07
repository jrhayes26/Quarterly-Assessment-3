import tkinter as tk
from tkinter import simpledialog, messagebox
from database import init_db
from admin_gui import open_admin_gui
from quiz_gui import open_quiz_gui

class LoginScreen:
    def __init__(self, master):
        self.master = master
        master.title("Quiz Bowl Login")
        master.geometry("300x200")

        tk.Label(master, text="Welcome! Choose an option:").pack(pady=20)

        tk.Button(master, text="Admin Login", width=20, command=self.admin_login).pack(pady=5)
        tk.Button(master, text="Take Quiz", width=20, command=self.start_quiz).pack(pady=5)

    def admin_login(self):
        password = simpledialog.askstring("Admin Login", "Enter admin password:", show='*')
        if password == "admin123":  # Replace with secure auth later
            self.master.destroy()
            open_admin_gui()
        else:
            messagebox.showerror("Access Denied", "Incorrect password.")

    def start_quiz(self):
        self.master.destroy()
        open_quiz_gui()

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    LoginScreen(root)
    root.mainloop()
