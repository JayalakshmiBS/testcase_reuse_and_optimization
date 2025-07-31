from tkinter import *
import re

# ----------------------------
# Logic Class (Testable)
# ----------------------------
class CalculatorLogic:
    def __init__(self):
        self.expression = ""
        self.result_shown = False  # New flag

    def insert(self, val):
        if self.result_shown:
            if val in '+-*/':
                self.expression += val  # Continue from result
            else:
                self.expression = val  # Start new expression
            self.result_shown = False
        else:
            # Handle leading zero case
            if (len(self.expression) >= 1 and 
                self.expression[-1] == '0' and 
                (len(self.expression) == 1 or self.expression[-2] in '+-*/(') and 
                val.isdigit() and val != '0'):
                # Replace the '0' with the new digit (to avoid '05', '06', etc.)
                self.expression = self.expression[:-1] + val
            else:
                self.expression += val
        return self.expression


    def cancel(self):
        self.expression = ""
        self.result_shown = False
        return self.expression

    def delete_last(self):
        self.expression = self.expression[:-1]
        return self.expression

    
    def calculate(self):
        try:
            # Clean leading zeros: turn '0002+03' into '2+3'
            cleaned = re.sub(r'\b0+(\d)', r'\1', self.expression)
            result = eval(cleaned)
            self.expression = str(result)
            self.result_shown = True
            return self.expression
        except ZeroDivisionError:
            self.expression = ""
            return "Error"
        except Exception:
            self.expression = ""
            return "Error"

# ----------------------------
# GUI Class (Uses Logic)
# ----------------------------
# class CalculatorGUI:
#     def __init__(self):
#         self.logic = CalculatorLogic()
#         self.root = Tk()
#         self.root.title("Calculator")
#         self.root.geometry("290x260")
#         self.root.maxsize(290, 260)
#         self.root.minsize(290, 260)
#         self.root.config(bg="grey")

#         self.resultwindow = Entry(self.root, borderwidth=5, relief=SUNKEN, font=("Arial", 18))
#         self.resultwindow.grid(row=0, column=0, columnspan=6, pady=5)
#         self.resultwindow.focus_set()

#         self.create_buttons()
#         self.bind_keys()
#         self.root.mainloop()

#     def update_display(self):
#         self.resultwindow.delete(0, END)
#         self.resultwindow.insert(0, self.logic.expression)

#     def on_click(self, val):
#         self.logic.insert(val)
#         self.update_display()

#     def on_cancel(self):
#         self.logic.cancel()
#         self.update_display()

#     def on_delete(self):
#         self.logic.delete_last()
#         self.update_display()

#     def on_result(self):
#         self.logic.calculate()
#         self.update_display()

#     def key_input(self, event):
#         key = event.char
#         if key in '0123456789+-*/().':
#             self.logic.insert(key)
#             self.update_display()

#     def bind_keys(self):
#         self.root.bind("<Key>", self.key_input)
#         self.root.bind("<Return>", lambda event: self.on_result())
#         self.root.bind("<BackSpace>", lambda event: self.on_delete())
#         self.root.bind("<Delete>", lambda event: self.on_cancel())
#         self.root.bind("<Escape>", lambda event: self.on_cancel())

#     def create_buttons(self):
#         btns = [
#             ('1', 1, 0), ('2', 1, 1), ('3', 1, 2),
#             ('4', 2, 0), ('5', 2, 1), ('6', 2, 2),
#             ('7', 3, 0), ('8', 3, 1), ('9', 3, 2),
#             ('0', 4, 0), ('(', 4, 1), (')', 4, 2),
#             ('+', 1, 3), ('-', 1, 4),
#             ('/', 2, 3), ('*', 2, 4),
#             ('Del', 3, 3), ('C', 3, 4),
#             ('=', 4, 3)
#         ]

#         for (text, row, col) in btns:
#             if text == '=':
#                 b = Button(self.root, text=text, width=7, bg='#FFEE58', command=self.on_result)
#                 b.grid(row=row, column=col, columnspan=2, padx=3, pady=3)
#             elif text == 'C':
#                 b = Button(self.root, text=text, width=3, bg='#EF5350', fg='white', command=self.on_cancel)
#                 b.grid(row=row, column=col, padx=3, pady=3)
#             elif text == 'Del':
#                 b = Button(self.root, text=text, width=3, command=self.on_delete)
#                 b.grid(row=row, column=col, padx=3, pady=3)
#             else:
#                 b = Button(self.root, text=text, width=3, bg='light green', command=lambda val=text: self.on_click(val))
#                 b.grid(row=row, column=col, padx=3, pady=3)

#             b.config(font=("Arial", 18))

# # ----------------------------
# # Main
# # ----------------------------
# if __name__ == "__main__":
#     CalculatorGUI()
