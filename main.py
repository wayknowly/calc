import tkinter as tk
from tkinter import messagebox
from sympy import symbols, Eq, solve, sympify, lambdify, sin, cos, tan, log, exp, pi, E, sqrt, factorial
import numpy as np
import matplotlib.pyplot as plt

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        root.title("Калькулятор вычислений")

        self.label = tk.Label(root, text="Введите выражение, уравнение или функцию:")
        self.label.pack()

        self.entry = tk.Entry(root, width=60)
        self.entry.pack(pady=5)

        self.solve_button = tk.Button(root, text="Решить", command=self.solve_expression)
        self.solve_button.pack(pady=2)

        self.graph_button = tk.Button(root, text="Построить график", command=self.plot_graph)
        self.graph_button.pack(pady=2)

        self.help_button = tk.Button(root, text="Справка", command=self.show_help)
        self.help_button.pack(pady=2)

        self.output_label = tk.Label(root, text="Решение и ответ:", font=("Arial", 10, "bold"))
        self.output_label.pack()

        self.output_text = tk.Text(root, height=15, width=70)
        self.output_text.pack()

    def solve_expression(self):
        expr = self.entry.get()
        self.output_text.delete("1.0", tk.END)

        try:
            if '=' in expr:
                x = symbols('x')
                left, right = expr.split('=')
                equation = Eq(sympify(left), sympify(right))
                solutions = solve(equation, x)
                self.output_text.insert(tk.END, f"Решение уравнения:\n{solutions}")
            else:
                result = eval(expr, {"__builtins__": None}, {
                    "sqrt": sqrt, "log": log, "ln": log, "log10": log,
                    "sin": sin, "cos": cos, "tan": tan, "pi": pi, "e": E,
                    "factorial": factorial, "abs": abs,
                    "exp": exp, **globals()
                })
                self.output_text.insert(tk.END, f"Ответ:\n{result}")
        except Exception as e:
            self.output_text.insert(tk.END, f"Ошибка при вычислении: {e}")

    def plot_graph(self):
        expr_str = self.entry.get().strip()
        self.output_text.delete("1.0", tk.END)

        x = symbols('x')
        try:
            expr = sympify(expr_str)
            func = lambdify(x, expr, modules=["numpy", {"sin": np.sin, "cos": np.cos, "tan": np.tan, "log": np.log, "exp": np.exp, "sqrt": np.sqrt}])
            
            x_vals = np.linspace(-10, 10, 500)
            y_vals = func(x_vals)

            plt.figure(figsize=(7, 5))
            plt.plot(x_vals, y_vals, label=f"y = {expr_str}")
            plt.title("График функции")
            plt.xlabel("x")
            plt.ylabel("y")
            plt.grid(True)
            plt.legend()
            plt.show()

            self.output_text.insert(tk.END, "График построен.")
        except Exception as e:
            self.output_text.insert(tk.END, f"Ошибка при построении графика:\n{e}")

    def show_help(self):
        help_text = (
            "Справка по функциям и графикам:\n\n"
            "Вы можете ввести:\n"
            " - Матем. выражение: 2+3*4, sqrt(16), factorial(5), log(100, 10)\n"
            " - Уравнение: x**2 - 4 = 0, sin(x) = 0.5\n"
            " - Функцию для графика: sin(x), x**2+3*x, exp(x)\n\n"
            "Чтобы построить график:\n"
            " - Введите выражение с переменной x, например:\n"
            "    - sin(x)\n"
            "    - x**2 + 2*x + 1\n"
            "    - exp(x)\n"
            " - Нажмите кнопку 'Построить график'\n"
            " - Диапазон x: от -10 до 10\n\n"
        )
        messagebox.showinfo("Справка", help_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
