import tkinter as tk
from tkinter import messagebox
import sqlite3
from database import DB_NAME

subjects = [
    'Intro to Project Management',
    'Database Management',
    'Business Applications Development',
    'Supply Chain Management',
    'Data Driven Decision Making'
]

def open_admin_gui():
    admin_win = tk.Tk()
    admin_win.title("Admin Panel")
    admin_win.geometry("300x200")

    tk.Label(admin_win, text="Admin Dashboard", font=("Arial", 14)).pack(pady=10)
    tk.Button(admin_win, text="Add Question", command=add_question_gui).pack(pady=5)
    tk.Button(admin_win, text="View Questions", command=view_questions_gui).pack(pady=5)
    tk.Button(admin_win, text="Exit", command=admin_win.destroy).pack(pady=10)
    admin_win.mainloop()

def add_question_gui():
    add_win = tk.Toplevel()
    add_win.title("Add New Question")
    add_win.geometry("400x500")

    tk.Label(add_win, text="Select Subject:").pack()
    subject_var = tk.StringVar(add_win)
    subject_var.set(subjects[0])
    tk.OptionMenu(add_win, subject_var, *subjects).pack()

    entries = {}
    fields = ["Question", "Option A", "Option B", "Option C", "Option D", "Correct Answer"]
    for field in fields:
        tk.Label(add_win, text=field + ":").pack()
        entry = tk.Entry(add_win, width=50)
        entry.pack()
        entries[field] = entry

    def save_question():
        subject = subject_var.get()
        data = {f: entries[f].get().strip() for f in fields}
        if "" in data.values():
            messagebox.showwarning("Incomplete", "Please fill in all fields.")
            return

        if data["Correct Answer"] not in [data["Option A"], data["Option B"], data["Option C"], data["Option D"]]:
            messagebox.showerror("Invalid", "Correct answer must match one of the options.")
            return

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(f'''
            INSERT INTO "{subject}" (question, option_a, option_b, option_c, option_d, correct_answer)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data["Question"], data["Option A"], data["Option B"], data["Option C"], data["Option D"], data["Correct Answer"]))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Question added successfully.")
        add_win.destroy()

    tk.Button(add_win, text="Submit", command=save_question).pack(pady=20)

def view_questions_gui():
    view_win = tk.Toplevel()
    view_win.title("View Questions")
    view_win.geometry("600x400")

    tk.Label(view_win, text="Select Subject to View:").pack()
    subject_var = tk.StringVar(view_win)
    subject_var.set(subjects[0])
    tk.OptionMenu(view_win, subject_var, *subjects).pack()

    text_area = tk.Text(view_win, wrap="word", height=15, width=70)
    text_area.pack(pady=10)
    
    tk.Label(view_win, text="Enter ID to Delete:").pack()
    delete_entry = tk.Entry(view_win)
    delete_entry.pack()

    def delete_question():
        subject = subject_var.get()
        qid = delete_entry.get().strip()
        if not qid.isdigit():
            messagebox.showerror("Invalid", "Please enter a valid numeric ID.")
            return

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {subject} WHERE id = ?", (int(qid),))
        conn.commit()
        conn.close()
        messagebox.showinfo("Deleted", f"Question ID {qid} deleted.")
        load_questions()  # Refresh list

    tk.Button(view_win, text="Delete Question", command=delete_question).pack(pady=5)


    def load_questions():
        subject = subject_var.get()
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM \"{subject}\"")
        rows = cursor.fetchall()
        conn.close()

        text_area.delete("1.0", tk.END)
        for row in rows:
            question_id = row[0]
            question = row[1]
            options = row[2:6]
            correct = row[6]
            text_area.insert(tk.END, f"ID: {question_id}\nQ: {question}\nOptions: {options}\nAnswer: {correct}\n\n")

    tk.Button(view_win, text="Load Questions", command=load_questions).pack()