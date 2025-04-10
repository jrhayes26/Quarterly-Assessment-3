import tkinter as tk
from tkinter import simpledialog, messagebox
from database import init_db
from admin_gui import open_admin_gui
from quiz_gui import open_quiz_gui

# Color palette & fonts to match the Admin Panel
COLORS = {
    "bg": "#e9dce5",
    "highlight": "#8c77af",
    "button": "#f6e7b4",
    "entry_bg": "#ffffff",
    "text": "#4a4a4a"
}

FONT = ("Segoe UI", 11)
TITLE_FONT = ("Segoe UI", 14, "bold")

def open_login_screen():
    root = tk.Tk()
    root.title("Quiz Bowl Login")
    root.geometry("320x250")
    root.configure(bg=COLORS["bg"])

    # Title
    tk.Label(root, text="Welcome to Quiz Bowl!", font=TITLE_FONT,
             bg=COLORS["bg"], fg=COLORS["highlight"]).pack(pady=(20, 10))

    # Buttons
    def admin_login():
        password = simpledialog.askstring("Admin Login", "Enter admin password:", show='*')
        if password == "admin123":
            root.destroy()
            open_admin_gui()
        else:
            messagebox.showerror("Access Denied", "Incorrect password.")

    def start_quiz():
        root.destroy()
        open_quiz_gui()

    for label, action in [
        ("Admin Login", admin_login),
        ("Take Quiz", start_quiz),
        ("Exit", root.destroy)
    ]:
        tk.Button(root, text=label, font=FONT, bg=COLORS["button"], fg=COLORS["text"],
                  relief="flat", activebackground=COLORS["highlight"], command=action).pack(pady=8, ipadx=10)

    root.mainloop()


if __name__ == "__main__":
    init_db()
    open_login_screen()
