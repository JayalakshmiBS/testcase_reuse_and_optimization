# calculator_gui.py

from tkinter import *
from calcu_logic import CalculatorLogic

class CalculatorGUI:
    def __init__(self, root):
        self.logic = CalculatorLogic()
        self.root = root
        self.root.title("Calculator")
        self.var = StringVar()

        self.create_widgets()

    def create_widgets(self):
        entry = Entry(self.root, textvariable=self.var, font=('Arial', 20), bd=10, insertwidth=2, width=14, borderwidth=4, justify='right')
        entry.grid(row=0, column=0, columnspan=4)

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('C', 4, 2), ('+', 4, 3),
            ('(', 5, 0), (')', 5, 1), ('DEL', 5, 2), ('=', 5, 3),
        ]

        for (text, row, col) in buttons:
            command = lambda t=text: self.on_button_click(t)
            Button(self.root, text=text, padx=20, pady=20, font=('Arial', 12), command=command).grid(row=row, column=col)

    def on_button_click(self, char):
        if char == "C":
            self.var.set(self.logic.clear())
        elif char == "DEL":
            self.var.set(self.logic.delete_last())
        elif char == "=":
            self.var.set(self.logic.evaluate())
        else:
            self.var.set(self.logic.input(char))

if __name__ == "__main__":
    root = Tk()
    gui = CalculatorGUI(root)
    root.mainloop()
