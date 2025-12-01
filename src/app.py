import os, json
import tkinter as tk
from json import JSONDecodeError
from tkinter import messagebox

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


# TODO: send out grades and clear the json file
def handle_send():
    pass


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
    root.title("Mailer")

    tk.Label(root, text="Prefix:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    pref_entry = tk.Entry(root, width=40)
    pref_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(root, text="Comment:").grid(row=1, column=0, sticky="nw", padx=10, pady=5)
    com_entry = tk.Text(root, width=40, height=5)
    com_entry.grid(row=1, column=1, padx=10, pady=5)

    handle_submit_btn = tk.Button(root, text="Submit", command=lambda: handle_submit(pref_entry, com_entry))
    handle_submit_btn.grid(row=2, column=1, pady=10, sticky="e")

    root.mainloop()


if __name__ == "__main__":
    main()
