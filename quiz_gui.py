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

def open_quiz_gui():
    quiz_win = tk.Tk()
    quiz_win.title("Choose a Subject")
    quiz_win.geometry("300x250")

    tk.Label(quiz_win, text="Select a Quiz Subject:", font=("Arial", 12)).pack(pady=15)
    for subject in subjects:
        tk.Button(quiz_win, text=subject, width=30,
                  command=lambda s=subject: start_quiz(s, quiz_win)).pack(pady=5)

    quiz_win.mainloop()

def start_quiz(subject, prev_win):
    prev_win.destroy()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM \"{subject}\"")
    questions = cursor.fetchall()
    conn.close()

    if not questions:
        messagebox.showwarning("Empty Quiz", f"No questions available for {subject}.")
        return

    index = [0]
    score = [0]
    total = len(questions)

    quiz_win = tk.Tk()
    quiz_win.title(f"{subject} Quiz")
    quiz_win.geometry("500x400")

    question_label = tk.Label(quiz_win, text="", wraplength=450, font=("Arial", 12))
    question_label.pack(pady=20)

    selected = tk.StringVar()
    option_buttons = []
    for _ in range(4):
        btn = tk.Radiobutton(quiz_win, text="", variable=selected, value="", font=("Arial", 10), anchor="w")
        btn.pack(fill="x", padx=40, pady=2)
        option_buttons.append(btn)

    def load_question():
        if index[0] >= total:
            messagebox.showinfo("Quiz Complete", f"Score: {score[0]}/{total}")
            quiz_win.destroy()
            return

        q = questions[index[0]]
        question_label.config(text=q[1])
        options = q[2:6]
        correct = q[6]

        selected.set(None)
        for i, btn in enumerate(option_buttons):
            btn.config(text=options[i], value=options[i])

        def submit():
            if not selected.get():
                messagebox.showwarning("Selection Missing", "Please select an answer.")
                return
            if selected.get() == correct:
                score[0] += 1
            index[0] += 1
            load_question()

        submit_btn.config(command=submit)

    submit_btn = tk.Button(quiz_win, text="Submit Answer", command=None)
    submit_btn.pack(pady=20)

    load_question()
    quiz_win.mainloop()
