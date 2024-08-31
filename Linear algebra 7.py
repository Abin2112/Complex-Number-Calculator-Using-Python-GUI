import tkinter as tk
from tkinter import ttk, messagebox
import cmath
import json
import matplotlib.pyplot as plt

class ComplexCalculator:
    def __init__(self, master):
        self.master = master
        master.title("Advanced Complex Number Calculator")
        master.geometry("500x500")

        # Set default background color as light blue
        self.default_bg_color = 'light blue'
        self.master.config(bg=self.default_bg_color)

        self.main_font = ('Arial', 12)

        # Initialize history list
        self.history = []

        # Labels and Entry fields for complex numbers
        self.real1_label = tk.Label(master, text="Real Part 1:", font=self.main_font, bg=self.default_bg_color)
        self.real1_label.grid(row=0, column=0, padx=10, pady=10)
        self.real1_entry = tk.Entry(master, font=self.main_font)
        self.real1_entry.grid(row=0, column=1, padx=10, pady=10)

        self.imag1_label = tk.Label(master, text="Imaginary Part 1:", font=self.main_font, bg=self.default_bg_color)
        self.imag1_label.grid(row=1, column=0, padx=10, pady=10)
        self.imag1_entry = tk.Entry(master, font=self.main_font)
        self.imag1_entry.grid(row=1, column=1, padx=10, pady=10)

        # Operation Combobox
        self.operation_label = tk.Label(master, text="Select Operation:", font=self.main_font, bg=self.default_bg_color)
        self.operation_label.grid(row=2, column=0, padx=10, pady=10)

        self.operation_var = tk.StringVar()
        self.operation_combobox = ttk.Combobox(master, textvariable=self.operation_var, font=self.main_font)
        self.operation_combobox['values'] = ('+', '-', '*', '/', 'conj', 'sqrt', 'arg', 'plot')
        self.operation_combobox.grid(row=2, column=1, padx=10, pady=10)
        self.operation_combobox.current(0)  # Default selection

        # Labels and Entry fields for second complex number
        self.real2_label = tk.Label(master, text="Real Part 2:", font=self.main_font, bg=self.default_bg_color)
        self.real2_label.grid(row=3, column=0, padx=10, pady=10)
        self.real2_entry = tk.Entry(master, font=self.main_font)
        self.real2_entry.grid(row=3, column=1, padx=10, pady=10)

        self.imag2_label = tk.Label(master, text="Imaginary Part 2:", font=self.main_font, bg=self.default_bg_color)
        self.imag2_label.grid(row=4, column=0, padx=10, pady=10)
        self.imag2_entry = tk.Entry(master, font=self.main_font)
        self.imag2_entry.grid(row=4, column=1, padx=10, pady=10)

        # Calculate Button
        self.calculate_button = tk.Button(master, text="Calculate", command=self.calculate, font=self.main_font)
        self.calculate_button.grid(row=5, column=0, columnspan=2, pady=10)

        # History Listbox
        self.history_listbox = tk.Listbox(master, height=10, font=self.main_font)
        self.history_listbox.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky='we')

        # Menu for additional features
        self.menu = tk.Menu(master)
        master.config(menu=self.menu)

        file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save History", command=self.save_history)
        file_menu.add_command(label="Load History", command=self.load_history)
        file_menu.add_command(label="Clear History", command=self.clear_history)

        theme_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Themes", menu=theme_menu)
        theme_menu.add_command(label="Light Theme", command=lambda: self.change_theme('light'))
        theme_menu.add_command(label="Dark Theme", command=lambda: self.change_theme('dark'))

        help_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Help", command=self.show_help)

    def calculate(self):
        try:
            real1 = float(self.real1_entry.get())
            imag1 = float(self.imag1_entry.get())
            c1 = complex(real1, imag1)
            operation = self.operation_var.get()

            if operation in ['+', '-', '*', '/']:
                real2 = float(self.real2_entry.get())
                imag2 = float(self.imag2_entry.get())
                c2 = complex(real2, imag2)

                if operation == '+':
                    result = c1 + c2
                elif operation == '-':
                    result = c1 - c2
                elif operation == '*':
                    result = c1 * c2
                elif operation == '/':
                    if c2 == 0:
                        result = "Error: Division by zero is not allowed."
                    else:
                        result = c1 / c2

            elif operation == 'conj':
                result = c1.conjugate()
            elif operation == 'sqrt':
                result = cmath.sqrt(c1)
            elif operation == 'arg':
                result = cmath.phase(c1)
            elif operation == 'plot':
                self.plot_complex(c1)
                return

            result_text = f"{c1} {operation} {c2 if operation in ['+', '-', '*', '/'] else ''} = {result}"
            self.history.append(result_text)  # Add the result to history
            self.history_listbox.insert(tk.END, result_text)

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values.")

    def plot_complex(self, *complex_numbers):
        plt.figure(figsize=(6, 6))
        plt.axhline(0, color='black', lw=1)
        plt.axvline(0, color='black', lw=1)
        colors = ['red', 'blue', 'green', 'purple']
        for idx, c in enumerate(complex_numbers):
            plt.scatter(c.real, c.imag, color=colors[idx % len(colors)])
            plt.text(c.real, c.imag, f'{c}', fontsize=12, ha='right')
            plt.arrow(0, 0, c.real, c.imag, head_width=0.2, head_length=0.2, fc=colors[idx % len(colors)], ec=colors[idx % len(colors)])
        plt.xlabel('Real')
        plt.ylabel('Imaginary')
        plt.title('Plot of Complex Numbers')
        plt.grid(True)
        plt.show()

    def save_history(self):
        with open("history.json", "w") as f:
            json.dump(self.history, f)

    def load_history(self):
        try:
            with open("history.json", "r") as f:
                self.history = json.load(f)
                self.history_listbox.delete(0, tk.END)
                for item in self.history:
                    self.history_listbox.insert(tk.END, item)
        except FileNotFoundError:
            messagebox.showwarning("Load Error", "No saved history found.")

    def clear_history(self):
        self.history.clear()
        self.history_listbox.delete(0, tk.END)

    def change_theme(self, theme):
        if theme == 'light':
            bg_color = 'white'
            fg_color = 'black'
        elif theme == 'dark':
            bg_color = 'black'
            fg_color = 'white'
        
        self.master.config(bg=bg_color)
        for widget in self.master.winfo_children():
            if isinstance(widget, (tk.Label, tk.Entry, tk.Listbox)):
                widget.config(bg=bg_color, fg=fg_color)
            elif isinstance(widget, tk.Button):
                widget.config(bg=bg_color, fg=fg_color, activebackground=fg_color, activeforeground=bg_color)
            elif isinstance(widget, ttk.Combobox):
                style = ttk.Style()
                style.configure('TCombobox', background=bg_color, foreground=fg_color)
                widget.configure(style='TCombobox')
            elif isinstance(widget, ttk.Button):
                style = ttk.Style()
                style.configure('TButton', background=bg_color, foreground=fg_color)
                widget.configure(style='TButton')

    def show_help(self):
        help_text = """
        Welcome to the Advanced Complex Number Calculator!

        Operations:
        + : Addition
        - : Subtraction
        * : Multiplication
        / : Division
        conj : Conjugate
        sqrt : Square Root
        arg : Argument (angle)
        plot : Plot Complex Numbers

        Enter real and imaginary parts for the first complex number and an operation.
        For binary operations, enter the second complex number.

        Themes:
        Choose between Light and Dark themes from the Themes menu.

        History Management:
        Save or load your calculation history from the File menu.
        """
        messagebox.showinfo("Help", help_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = ComplexCalculator(root)
    root.mainloop()
