import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import re
from math import *


class FalsePositionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("False Position Method Solver")
        self.root.geometry("1000x800")
        self.root.configure(bg="#2d3436")

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.style.configure('.', background="#2d3436", foreground="#dfe6e9")
        self.style.configure('TFrame', background="#2d3436")
        self.style.configure('TLabel', background="#2d3436", foreground="#dfe6e9", font=('Helvetica', 10))
        self.style.configure('TButton', font=('Helvetica', 10, 'bold'), padding=8)
        self.style.configure('TEntry', font=('Helvetica', 10), padding=5, fieldbackground="#636e72")
        self.style.configure('TLabelframe', background="#2d3436", foreground="#dfe6e9")
        self.style.configure('TLabelframe.Label', font=('Helvetica', 10, 'bold'), foreground="#74b9ff")
        self.style.configure('TText', background="#636e72", foreground="#dfe6e9")

        self.style.map('Black.TButton',
                       foreground=[('active', '#ffffff'), ('!disabled', '#ffffff')],
                       background=[('active', '#000000'), ('!disabled', '#000000')])

        creator_frame = ttk.Frame(root)
        creator_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        ttk.Label(creator_frame, text="Created by Diyar Penjweny",
                  font=('Helvetica', 10), foreground="#b2bec3").pack(side=tk.RIGHT)

        input_frame = ttk.LabelFrame(root, text="Parameters", padding=15)
        input_frame.pack(fill=tk.X, padx=15, pady=10)

        ttk.Label(input_frame, text="Function f(x):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.func_entry = ttk.Entry(input_frame, width=40)
        self.func_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        self.func_entry.insert(0, "x**3 - 4*x - 9")
        ttk.Label(input_frame, text="Example: x**2 + sin(x) - 2", foreground="#b2bec3").grid(row=0, column=2,
                                                                                             sticky=tk.W, padx=5)

        ttk.Label(input_frame, text="Lower bound (a):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.a_entry = ttk.Entry(input_frame)
        self.a_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.a_entry.insert(0, "2")

        ttk.Label(input_frame, text="Upper bound (b):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.b_entry = ttk.Entry(input_frame)
        self.b_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        self.b_entry.insert(0, "3")

        ttk.Label(input_frame, text="Tolerance (E):").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.e_entry = ttk.Entry(input_frame)
        self.e_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        self.e_entry.insert(0, "0.00001")

        ttk.Button(input_frame, text="FIND ROOT", command=self.calculate,
                   style='Black.TButton').grid(row=4, column=0, columnspan=3, pady=15, sticky=tk.EW)

        results_frame = ttk.LabelFrame(root, text="Results", padding=15)
        results_frame.pack(fill=tk.X, padx=15, pady=10)

        self.result_text = tk.Text(results_frame, height=8, width=80, font=('Courier New', 10),
                                   bg="#636e72", fg="#dfe6e9", insertbackground="#dfe6e9",
                                   padx=10, pady=10, relief=tk.FLAT)
        self.result_text.pack()

        plot_frame = ttk.LabelFrame(root, text="Function Visualization", padding=15)
        plot_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        info_label = ttk.Label(root,
                               text="Visualization shows the function curve with iterations. Blue line = function, Red dots = root approximation",
                               font=('Helvetica', 9),
                               foreground="#b2bec3",
                               wraplength=800,
                               justify=tk.CENTER)
        info_label.pack(pady=(0, 10))

        plt.style.use('dark_background')
        self.fig, self.ax = plt.subplots(figsize=(8, 5), facecolor='#2d3436')
        self.ax.set_facecolor('#2d3436')
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.status = ttk.Label(root, text="Ready", relief=tk.SUNKEN, anchor=tk.W,
                                font=('Helvetica', 9), foreground="#dfe6e9", background="#0984e3")
        self.status.pack(fill=tk.X, padx=15, pady=(5, 15))

        self.update_plot(2, 3)

    def safe_eval(self, expr, x_val):
        try:
            expr = expr.replace('^', '**')
            expr = expr.replace('sin', 'np.sin')
            expr = expr.replace('cos', 'np.cos')
            expr = expr.replace('tan', 'np.tan')
            expr = expr.replace('log', 'np.log')
            expr = expr.replace('exp', 'np.exp')
            expr = expr.replace('sqrt', 'np.sqrt')
            return eval(expr, {'x': x_val, 'np': np, 'pi': np.pi, 'e': np.e})
        except:
            return None

    def f(self, x):
        expr = self.func_entry.get()
        return self.safe_eval(expr, x)

    def falsiPosition(self, a, b, E):
        counter = 0
        iterations = []

        if self.f(a) * self.f(b) > 0:
            return None, "No root in interval (f(a) and f(b) must have opposite signs)", iterations
        else:
            while abs(b - a) > E:
                counter += 1
                try:
                    mid = (a * self.f(b) - b * self.f(a)) / (self.f(b) - self.f(a))
                except ZeroDivisionError:
                    return mid, f"Division by zero at iteration {counter}", iterations

                iterations.append((counter, a, b, mid, self.f(mid)))

                if self.f(mid) == 0:
                    return mid, f"Exact root found in {counter} iterations", iterations
                elif self.f(a) * self.f(mid) > 0:
                    a = mid
                else:
                    b = mid

                if counter == 1000:
                    return mid, f"Approximate root (reached max {counter} iterations)", iterations

            return mid, f"Converged in {counter} iterations", iterations

    def calculate(self):
        self.status.config(text="Calculating...")
        self.root.update()

        try:
            a = float(self.a_entry.get())
            b = float(self.b_entry.get())
            E = float(self.e_entry.get())

            if self.f(0) is None:
                messagebox.showerror("Error", "Invalid function expression")
                self.status.config(text="Error in function expression")
                return

            root, message, iterations = self.falsiPosition(a, b, E)

            if root is None:
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, message)
                messagebox.showerror("Error", message)
                self.status.config(text="Calculation failed")
            else:
                result_str = f"Root: {root:.10f}\n{message}\n\nIterations:\n"
                for iter_data in iterations[-10:]:
                    result_str += (f"Iter {iter_data[0]:3d}: a={iter_data[1]:.8f}, "
                                   f"b={iter_data[2]:.8f}, mid={iter_data[3]:.8f}, "
                                   f"f(mid)={iter_data[4]:.8f}\n")

                if len(iterations) > 10:
                    result_str += f"\n... (showing last 10 of {len(iterations)} iterations)"

                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, result_str)

                self.update_plot(a, b, root, iterations)
                self.status.config(text=f"Success! {message}")

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")
            self.status.config(text="Invalid input")

    def update_plot(self, a, b, root=None, iterations=None):
        self.ax.clear()

        x = np.linspace(a - 1, b + 1, 400)
        y = np.array([self.f(xi) for xi in x])
        self.ax.plot(x, y, '#74b9ff', label=f'f(x) = {self.func_entry.get()}', linewidth=2)
        self.ax.axhline(0, color='#dfe6e9', linewidth=0.8, linestyle='--')

        self.ax.axvline(a, color='#e17055', linestyle='--', alpha=0.7, label='Initial interval')
        self.ax.axvline(b, color='#e17055', linestyle='--', alpha=0.7)

        if iterations:
            for i, (counter, a_iter, b_iter, mid, f_mid) in enumerate(iterations):
                color = plt.cm.viridis(i / len(iterations))
                self.ax.plot([a_iter, b_iter], [self.f(a_iter), self.f(b_iter)], 'o-',
                             color=color, alpha=0.5, markersize=4)
                self.ax.axvline(mid, color=color, linestyle=':', alpha=0.3)

        if root is not None:
            self.ax.plot(root, self.f(root), 'ro', markersize=8,
                         label=f'Root ≈ {root:.6f}')

        self.ax.set_xlabel('x', fontsize=10)
        self.ax.set_ylabel('f(x)', fontsize=10)
        self.ax.set_title('False Position Method Visualization', fontsize=12)
        self.ax.legend(loc='upper right')
        self.ax.grid(True, color='#636e72', alpha=0.3)

        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = FalsePositionApp(root)
    root.mainloop()