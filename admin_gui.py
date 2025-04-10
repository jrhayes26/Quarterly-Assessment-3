import tkinter as tk
from tkinter import messagebox
import sqlite3
from database import DB_NAME

# Subjects and style settings
subjects = [
    'Intro to Project Management',
    'Database Management',
    'Business Applications Development',
    'Supply Chain Management',
    'Data Driven Decision Making'
]

COLORS = {
    "bg": "#e9dce5",
    "highlight": "#8c77af",
    "button": "#f6e7b4",
    "entry_bg": "#ffffff",
    "text": "#4a4a4a"
}

FONT = ("Segoe UI", 11)
TITLE_FONT = ("Segoe UI", 14, "bold")

def open_admin_gui():
    admin_win = tk.Tk()
    admin_win.title("Admin Panel")
    admin_win.geometry("300x250")
    admin_win.configure(bg=COLORS["bg"])

    tk.Label(admin_win, text="Admin Dashboard", font=TITLE_FONT, bg=COLORS["bg"], fg=COLORS["highlight"]).pack(pady=15)

    for text, command in [
        ("Add Question", lambda: add_question_gui(admin_win)),
        ("View Questions", lambda: view_questions_gui(admin_win)),
        ("Exit", admin_win.destroy)
    ]:
        tk.Button(admin_win, text=text, font=FONT, bg=COLORS["button"], fg=COLORS["text"],
                  relief="flat", activebackground=COLORS["highlight"], command=command).pack(pady=8, ipadx=10)

    admin_win.mainloop()

def add_question_gui(parent):
    add_win = tk.Toplevel(parent)
    add_win.title("Add New Question")
    add_win.geometry("400x550")
    add_win.configure(bg=COLORS["bg"])

    tk.Label(add_win, text="Select Subject:", font=FONT, bg=COLORS["bg"], fg=COLORS["text"]).pack(pady=5)
    subject_var = tk.StringVar(add_win)
    subject_var.set(subjects[0])
    tk.OptionMenu(add_win, subject_var, *subjects).pack(pady=5, fill="x")

    entries = {}
    fields = ["Question", "Option A", "Option B", "Option C", "Option D", "Correct Answer"]
    for field in fields:
        tk.Label(add_win, text=field + ":", font=FONT, bg=COLORS["bg"], fg=COLORS["text"]).pack(pady=(10, 2))
        entry = tk.Entry(add_win, width=50, font=FONT, bg=COLORS["entry_bg"])
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
            VALUES (?, ?, ?, ?, ?, ?)''',
            (data["Question"], data["Option A"], data["Option B"], data["Option C"], data["Option D"], data["Correct Answer"]))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Question added successfully.")
        add_win.destroy()

    tk.Button(add_win, text="Submit", font=FONT, bg=COLORS["button"], fg=COLORS["text"],
              relief="flat", activebackground=COLORS["highlight"], command=save_question).pack(pady=20)

def view_questions_gui(parent):
    view_win = tk.Toplevel(parent)
    view_win.title("View Questions")
    view_win.geometry("600x500")
    view_win.configure(bg=COLORS["bg"])

    tk.Label(view_win, text="Select Subject to View:", font=FONT, bg=COLORS["bg"], fg=COLORS["text"]).pack(pady=5)
    subject_var = tk.StringVar(view_win)
    subject_var.set(subjects[0])
    tk.OptionMenu(view_win, subject_var, *subjects).pack(pady=5, fill="x")

    text_area = tk.Text(view_win, wrap="word", height=15, width=70, font=FONT, bg=COLORS["entry_bg"])
    text_area.pack(pady=10)

    tk.Label(view_win, text="Enter ID to Delete:", font=FONT, bg=COLORS["bg"], fg=COLORS["text"]).pack(pady=5)
    delete_entry = tk.Entry(view_win, font=FONT, bg=COLORS["entry_bg"])
    delete_entry.pack()

    def delete_question():
        subject = subject_var.get()
        qid = delete_entry.get().strip()
        if not qid.isdigit():
            messagebox.showerror("Invalid", "Please enter a valid numeric ID.")
            return

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(f'DELETE FROM "{subject}" WHERE id = ?', (int(qid),))
        conn.commit()
        conn.close()
        messagebox.showinfo("Deleted", f"Question ID {qid} deleted.")
        load_questions()

    tk.Button(view_win, text="Delete Question", font=FONT, bg=COLORS["button"], fg=COLORS["text"],
              relief="flat", activebackground=COLORS["highlight"], command=delete_question).pack(pady=8)

    def load_questions():
        subject = subject_var.get()
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM "{subject}"')
        rows = cursor.fetchall()
        conn.close()

        text_area.delete("1.0", tk.END)
        for row in rows:
            question_id = row[0]
            question = row[1]
            options = row[2:6]
            correct = row[6]
            text_area.insert(tk.END, f"ID: {question_id}\nQ: {question}\nOptions: {options}\nAnswer: {correct}\n\n")

    tk.Button(view_win, text="Load Questions", font=FONT, bg=COLORS["button"], fg=COLORS["text"],
              relief="flat", activebackground=COLORS["highlight"], command=load_questions).pack(pady=10)