import os, json
import tkinter as tk
from tkinter import messagebox

from mailer import GradeMailer

GRADES_PATH = "./data/grades.json"


def writeGrade(pref, comment):
    if not os.path.exists(GRADES_PATH):
        data = json.dumps({pref: comment})
        with open(GRADES_PATH, "w") as f:
            f.write(data)
        return

    with open(GRADES_PATH, "r+") as f:
        data = json.load(f)
        data[pref] = comment
        data_json = json.dumps(data)
        f.write(data_json)


def submit(pref_entry, com_entry):
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
    root.title("Mailer")

    tk.Label(root, text="Prefix:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    pref_entry = tk.Entry(root, width=40)
    pref_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(root, text="Comment:").grid(row=1, column=0, sticky="nw", padx=10, pady=5)
    com_entry = tk.Text(root, width=40, height=5)
    com_entry.grid(row=1, column=1, padx=10, pady=5)

    submit_btn = tk.Button(root, text="Submit", command=lambda: submit(pref_entry, com_entry))
    submit_btn.grid(row=2, column=1, pady=10, sticky="e")

    root.mainloop()


if __name__ == "__main__":
    main()
