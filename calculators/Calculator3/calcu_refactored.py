from tkinter import *
import re
# Logic class (independent from GUI)
class CalculatorLogic:
    def __init__(self):
        self.expression = ""

    def click_button(self, value):
        self.expression += str(value)
        return self.expression

    def clear(self):
        self.expression = ""
        return self.expression

    def delete(self):
        self.expression = self.expression[:-1]
        return self.expression

    def evaluate(self):
        try:
            # Validate only allowed characters
            if not re.fullmatch(r"[0-9+\-*/(). ]*", self.expression):
                raise ValueError("Invalid characters")

            # Sanitize expression to remove leading zeros
            cleaned_expr = self.preprocess_expression(self.expression)

            result = str(eval(cleaned_expr))
            self.expression = result
            return result
        except Exception:
            self.expression = ""
            return "Error"

# GUI Class (uses the logic)
class CalculatorGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Calculator")
        self.logic = CalculatorLogic()
        self.var = StringVar()

        # Entry for displaying expressions
        self.entry = Entry(master, textvariable=self.var, font=('arial', 20), bd=10, insertwidth=4,
                           bg="powder blue", justify='right')
        self.entry.grid(columnspan=4)

        # Buttons
        self.create_buttons()

    def create_buttons(self):
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('(', 4, 2), (')', 4, 3),
            ('C', 5, 0), ('DEL', 5, 1), ('=', 5, 2), ('+', 5, 3)
        ]

        for (text, row, col) in buttons:
            action = lambda x=text: self.on_button_click(x)
            Button(self.master, text=text, padx=20, pady=20, font=('Helvetica', 14),
                   command=action, bg='black', fg='cyan').grid(row=row, column=col, sticky='nsew')

        # Make grid scalable
        for i in range(6):
            self.master.grid_rowconfigure(i, weight=1)
        for j in range(4):
            self.master.grid_columnconfigure(j, weight=1)

    def on_button_click(self, char):
        if char == 'C':
            self.var.set(self.logic.clear())
        elif char == 'DEL':
            self.var.set(self.logic.delete())
        elif char == '=':
            self.var.set(self.logic.evaluate())
        else:
            self.var.set(self.logic.click_button(char))


if __name__ == '__main__':
    root = Tk()
    app = CalculatorGUI(root)
    root.mainloop()
