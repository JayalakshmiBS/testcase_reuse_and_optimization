import tkinter as tk
from tkinter import messagebox
from calculator_logic import binary_operation, unary_operation

state = {"operation": "", "first": ""}

root = tk.Tk()
root.geometry("400x500")
root.title("Scientific Calculator")

entry = tk.Entry(root, font=("Arial", 20), bd=5, justify="right")
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=20)

operation_label = tk.Label(root, text="", font=("Arial", 12), fg="blue")
operation_label.grid(row=1, column=0, columnspan=4)


def set_operation(op):
    state["first"] = entry.get()
    state["operation"] = op
    operation_label.config(text=f"{state['first']} {op}")
    entry.delete(0, tk.END)


def calculate():
    second = entry.get()
    result = binary_operation(state["first"], second, state["operation"])
    if result == "Error" or result == "Invalid":
        messagebox.showerror("Error", "Invalid input or operation")
    else:
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(result))
        operation_label.config(text=f"= {result}")
    state["first"] = ""
    state["operation"] = ""


def clear():
    entry.delete(0, tk.END)
    operation_label.config(text="")
    state["operation"] = ""
    state["first"] = ""


def backspace():
    current = entry.get()
    entry.delete(len(current) - 1, tk.END)


def insert(value):
    entry.insert(tk.END, value)


def apply_function(func):
    val = entry.get()
    result = unary_operation(val, func)
    if result == "Error" or result == "Unknown":
        messagebox.showerror("Error", "Invalid input or operation")
    else:
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(result))
        operation_label.config(text=f"{func}({val}) = {result}")


# ---- Button UI ----

button_config = {
    "padx": 15,
    "pady": 10,
    "bd": 3,
    "font": ("Arial", 14)
}

buttons = [
    ("7", lambda: insert("7")), ("8", lambda: insert("8")), ("9", lambda: insert("9")), ("/", lambda: set_operation("/")),
    ("4", lambda: insert("4")), ("5", lambda: insert("5")), ("6", lambda: insert("6")), ("*", lambda: set_operation("*")),
    ("1", lambda: insert("1")), ("2", lambda: insert("2")), ("3", lambda: insert("3")), ("-", lambda: set_operation("-")),
    ("0", lambda: insert("0")), (".", lambda: insert(".")), ("=", calculate), ("+", lambda: set_operation("+")),
    ("C", clear), ("⌫", backspace), ("%", lambda: set_operation("%")), ("^", lambda: set_operation("^")),
    ("sin", lambda: apply_function("sin")), ("cos", lambda: apply_function("cos")),
    ("√", lambda: apply_function("√")), ("x²", lambda: apply_function("x²")),
    ("x³", lambda: apply_function("x³")), ("!", lambda: apply_function("!")),
    ("log", lambda: apply_function("log")), ("1/x", lambda: apply_function("1/x")),
]

row_index = 2
col_index = 0
for (text, command) in buttons:
    btn = tk.Button(root, text=text, command=command, **button_config)
    btn.grid(row=row_index, column=col_index, sticky="nsew")
    col_index += 1
    if col_index > 3:
        col_index = 0
        row_index += 1

for i in range(6):
    root.rowconfigure(i, weight=1)
for j in range(4):
    root.columnconfigure(j, weight=1)

root.mainloop()
