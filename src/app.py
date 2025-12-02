import os, json
import tkinter as tk
from json import JSONDecodeError
from tkinter import messagebox
from tkinter import ttk

from mailer import GradeMailer

GRADES_FILE = "./data/grades.json"


def writeGrade(pref, comment):
    try:
        if os.stat(GRADES_FILE).st_size == 0:
            print("[LOG] File was empty writing JSON")
            data = json.loads('{}')
        else:
            with open(GRADES_FILE, "r") as f:
                data = json.load(f)

        data.update({pref: comment})
        with open(GRADES_FILE, "w") as f:
            json.dump(data, f)
        print("[LOG] Appended to JSON file")

    except FileNotFoundError:
        print(f"[ERROR] File '{GRADES_FILE}' was not found")
    except JSONDecodeError:
        print(f"[ERROR] Could not decode the file '{GRADES_FILE}'")


def handle_send(gm):
    gm.readGrades(GRADES_FILE)
    gm.mailGrades()
    print("[LOG] Sent out grades")

    with open(GRADES_FILE, "w") as f:
        json.dump({}, f)


def handle_submit(pref_entry, com_entry):
    pref = pref_entry.get()
    comment = com_entry.get("1.0", tk.END).strip()

    if not pref or not comment:
        messagebox.showwarning("Missing Info", "Please fill in both fields.")
        return

    writeGrade(pref, comment)

    pref_entry.delete(0, tk.END)
    com_entry.delete("1.0", tk.END)


def main():
    gm = GradeMailer()
    gm.auth()

    root = tk.Tk()
    root.title("Grade Mailer Dashboard 📧")

    style = ttk.Style()
    style.theme_use('clam')

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    main_frame = ttk.Frame(root, padding="15 15 15 15")
    main_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
    main_frame.columnconfigure(1, weight=1)

    ttk.Label(main_frame, text="Prefix:").grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))
    pref_entry = ttk.Entry(main_frame, width=50)
    pref_entry.grid(row=0, column=1, padx=10, pady=(10, 5), sticky=(tk.W, tk.E))

    ttk.Label(main_frame, text="Comment:").grid(row=1, column=0, sticky="nw", padx=10, pady=5)

    text_frame = ttk.Frame(main_frame)
    text_frame.grid(row=1, column=1, padx=10, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
    text_frame.columnconfigure(0, weight=1)
    text_frame.rowconfigure(0, weight=1)

    com_entry = tk.Text(text_frame, width=40, height=8, wrap="word", font=('Arial', 10))
    com_entry.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    button_frame = ttk.Frame(main_frame)
    button_frame.grid(row=2, column=1, columnspan=2, pady=(15, 0), sticky='e')

    style.configure('Primary.TButton', font=('Arial', 10, 'bold'), foreground='white', background='#0078D7')

    submit_btn = ttk.Button(button_frame, text="Submit Changes",
                            command=lambda: handle_submit(pref_entry, com_entry),
                            style='TButton')
    submit_btn.pack(side=tk.LEFT, padx=10)

    send_btn = ttk.Button(button_frame, text="🚀 Send Grades",
                          command=lambda: handle_send(gm),
                          style='Primary.TButton')
    send_btn.pack(side=tk.LEFT)

    root.mainloop()


if __name__ == "__main__":
    main()
