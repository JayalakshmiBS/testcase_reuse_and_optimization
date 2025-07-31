import tkinter as tk
from calc_logic import CalculatorLogic

LARGE_FONT_STYLE = ("Arial", 40, "bold")
SMALL_FONT_STYLE = ("Arial", 16)
DIGITS_FONT_STYLE = ("Arial", 24, "bold")
DEFAULT_FONT_STYLE = ("Arial", 20)

OFF_WHITE = "#F8FAFF"
WHITE = "#FFFFFF"
LIGHT_BLUE = "#CCEDFF"
LIGHT_GRAY = "#F5F5F5"
LABEL_COLOR = "#25265E"

class CalculatorUI:
    def __init__(self):
        self.logic = CalculatorLogic()
        self.window = tk.Tk()
        self.window.geometry("375x667")
        self.window.resizable(0, 0)
        self.window.title("Calculator")

        self.display_frame = self.create_display_frame()
        self.total_label, self.label = self.create_display_labels()

        self.digits = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            0: (4, 2), '.': (4, 1)
        }
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}
        self.buttons_frame = self.create_buttons_frame()

        for x in range(5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)

        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.bind_keys()

    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))
        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))

    def create_display_frame(self):
        frame = tk.Frame(self.window, height=221, bg=LIGHT_GRAY)
        frame.pack(expand=True, fill="both")
        return frame

    def create_display_labels(self):
        total_label = tk.Label(self.display_frame, anchor=tk.E, bg=LIGHT_GRAY,
                               fg=LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill='both')

        label = tk.Label(self.display_frame, anchor=tk.E, bg=LIGHT_GRAY,
                         fg=LABEL_COLOR, padx=24, font=LARGE_FONT_STYLE)
        label.pack(expand=True, fill='both')

        return total_label, label

    def update_total_label(self):
        expression = self.logic.get_total_expression()
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.total_label.config(text=expression)

    def update_label(self):
        self.label.config(text=self.logic.get_current_expression())

    def add_to_expression(self, value):
        self.logic.add_to_expression(value)
        self.update_label()

    def append_operator(self, operator):
        self.logic.append_operator(operator)
        self.update_total_label()
        self.update_label()

    def clear(self):
        self.logic.clear()
        self.update_label()
        self.update_total_label()

    def square(self):
        self.logic.square()
        self.update_label()

    def sqrt(self):
        self.logic.sqrt()
        self.update_label()

    def evaluate(self):
        self.logic.evaluate()
        self.update_total_label()
        self.update_label()

    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg=WHITE, fg=LABEL_COLOR,
                               font=DIGITS_FONT_STYLE, borderwidth=0,
                               command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def create_operator_buttons(self):
        i = 0
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg=OFF_WHITE, fg=LABEL_COLOR,
                               font=DEFAULT_FONT_STYLE, borderwidth=0,
                               command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1

    def create_special_buttons(self):
        tk.Button(self.buttons_frame, text="C", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                  borderwidth=0, command=self.clear).grid(row=0, column=1, sticky=tk.NSEW)

        tk.Button(self.buttons_frame, text="x\u00b2", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                  borderwidth=0, command=self.square).grid(row=0, column=2, sticky=tk.NSEW)

        tk.Button(self.buttons_frame, text="\u221ax", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                  borderwidth=0, command=self.sqrt).grid(row=0, column=3, sticky=tk.NSEW)

        tk.Button(self.buttons_frame, text="=", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                  borderwidth=0, command=self.evaluate).grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)

    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = CalculatorUI()
    app.run()
