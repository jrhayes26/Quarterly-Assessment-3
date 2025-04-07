import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# --- Constants for Database ---
DB_NAME = "quizbowl.db"

# --- Fixed list of subjects (matches database table names) ---
SUBJECTS = [
    "Database_Management",
    "Intro_to_Project_Management",
    "Data_Driven_Decision_Making",
    "Supply_Chain_Management",
    "Business_Application_Development"
]

# --- Function to view questions in a subject ---
def view_questions_gui():
    view_window = tk.Toplevel()
    view_window.title("View Questions")

    label = tk.Label(view_window, text="Select Subject:")
    label.pack(pady=5)

    subject_var = tk.StringVar()
    subject_dropdown = ttk.Combobox(view_window, textvariable=subject_var, values=SUBJECTS)
    subject_dropdown.pack(pady=5)

    def load_questions():
        subject = subject_var.get()
        if not subject:
            messagebox.showerror("Error", "Please select a subject.")
            return

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(f"SELECT question, option1, option2, option3, option4, correct FROM {subject}")
        rows = cursor.fetchall()
        conn.close()

        result_text.delete(1.0, tk.END)
        for idx, row in enumerate(rows, 1):
            q, o1, o2, o3, o4, correct = row
            result_text.insert(tk.END, f"Q{idx}: {q}\nA. {o1}\nB. {o2}\nC. {o3}\nD. {o4}\nCorrect: {correct}\n\n")

    load_btn = tk.Button(view_window, text="Load Questions", command=load_questions)
    load_btn.pack(pady=5)

    result_text = tk.Text(view_window, height=20, width=80)
    result_text.pack(pady=10)

# --- Main Admin GUI Window ---
def open_admin_gui():
    admin_window = tk.Toplevel()
    admin_window.title("Admin Panel")

    label = tk.Label(admin_window, text="Welcome to the Admin Panel", font=("Arial", 14))
    label.pack(pady=10)

    # Only "View Questions" is available to admin
    view_btn = tk.Button(admin_window, text="View Questions", width=20, command=view_questions_gui)
    view_btn.pack(pady=10)

    # You can add more admin features here if needed in future

# --- END OF FILE ---
