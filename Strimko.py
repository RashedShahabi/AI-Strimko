import tkinter as tk
from tkinter import messagebox, simpledialog
import random

class StreamkoGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Streamko Game")
        self.create_widgets()
        self.n = None
        self.matrix = None
        self.relation_groups = None
        self.colors = ["lightblue", "lightgreen", "lightyellow", "lightpink", "lightgrey", "lightcoral", "lightcyan"]

    def create_widgets(self):
        self.size_label = tk.Label(self.root, text="سایز ماتریس (مثال: 3)(n*n):")
        self.size_label.pack()
        
        self.size_entry = tk.Entry(self.root)
        self.size_entry.pack()
        
        self.create_matrix_button = tk.Button(self.root, text="ایجاد ماتریس", command=self.create_matrix)
        self.create_matrix_button.pack()
        
        self.relations_label = tk.Label(self.root, text="ارتباطات (مثال: 3,1/3,2/3,3#2,1/2,2/2,3#1,1/1,2/1,3):")
        self.relations_label.pack()
        
        self.relations_entry = tk.Entry(self.root)
        self.relations_entry.pack()
        
        self.apply_relations_button = tk.Button(self.root, text="اعمال روابط", command=self.apply_relations)
        self.apply_relations_button.pack()
        
        self.values_label = tk.Label(self.root, text="مقادیر پیش فرض (مثال:.../1,1,2/2,2,3):")
        self.values_label.pack()
        
        self.values_entry = tk.Entry(self.root)
        self.values_entry.pack()
        
        self.apply_values_button = tk.Button(self.root, text="اعمال مقادیر پیش فرض", command=self.apply_values)
        self.apply_values_button.pack()
        
        self.solve_button = tk.Button(self.root, text="بازی حل شود", command=self.solve_backtracking)
        self.solve_button.pack()
        
        self.matrix_frame = tk.Frame(self.root)
        self.matrix_frame.pack()

    def create_matrix(self):
        try:
            self.n = int(self.size_entry.get())
            self.matrix = [[0 for _ in range(self.n)] for _ in range(self.n)]
            self.buttons = [[None for _ in range(self.n)] for _ in range(self.n)]

            for widget in self.matrix_frame.winfo_children():
                widget.destroy()

            for i in range(self.n):
                for j in range(self.n):
                    button = tk.Button(self.matrix_frame, text="", width=5, height=2,
                                       command=lambda i=i, j=j: self.set_value(i, j))
                    button.grid(row=i, column=j)
                    self.buttons[i][j] = button
            
        except ValueError:
            messagebox.showerror("Error", "لطفاً یک عدد صحیح وارد کنید")

    def set_value(self, i, j):
        value = simpledialog.askinteger("Input", f"مقدار برای خانه ({i+1},{j+1}):", minvalue=1, maxvalue=self.n)
        if value and self.is_valid_value(i, j, value):
            self.matrix[i][j] = value
            self.buttons[i][j].config(text=str(value))
        else:
            messagebox.showerror("Error", "مقدار نامعتبر است یا تکراری")

    def apply_relations(self):
        relations = self.relations_entry.get().split('#')
        self.relation_groups = []

        if len(relations) != self.n:
            messagebox.showerror("Error", "تعداد روابط باید برابر با سایز ماتریس باشد")
            return
        
        used_colors = set()
        for relation in relations:
            pairs = relation.split('/')
            if len(pairs) != self.n:
                messagebox.showerror("Error", "تعداد خانه‌ها در هر رابطه باید برابر با سایز ماتریس باشد")
                return
            group = []
            for pair in pairs:
                x, y = map(int, pair.split(','))
                group.append((x-1, y-1))
            self.relation_groups.append(group)
            
            while True:
                color = random.choice(self.colors)
                if color not in used_colors:
                    used_colors.add(color)
                    break

            for (x, y) in group:
                self.buttons[x][y].config(bg=color)

    def apply_values(self):
        values = self.values_entry.get().split('/')

        for value in values:
            x, y, val = map(int, value.split(','))
            if self.is_valid_value(x-1, y-1, val):
                self.matrix[x-1][y-1] = val
                self.buttons[x-1][y-1].config(text=str(val))
            else:
                messagebox.showerror("Error", "مقدار نامعتبر است یا تکراری")

    def is_valid_value(self, i, j, value):
        for x in range(self.n):
            if self.matrix[i][x] == value or self.matrix[x][j] == value:
                return False
        
        for group in self.relation_groups:
            if (i, j) in group:
                for (x, y) in group:
                    if self.matrix[x][y] == value:
                        return False
        
        return True

    def solve_backtracking(self):
        def backtrack(matrix):
            for i in range(len(matrix)):
                for j in range(len(matrix)):
                    if matrix[i][j] == 0:
                        for num in range(1, len(matrix) + 1):
                            if self.is_valid_value(i, j, num):
                                matrix[i][j] = num
                                if backtrack(matrix):
                                    return True
                                matrix[i][j] = 0
                        return False
            return True

        if backtrack(self.matrix):
            for i in range(len(self.matrix)):
                for j in range(len(self.matrix)):
                    self.buttons[i][j].config(text=str(self.matrix[i][j]))
            return True
        return False

if __name__ == "__main__":
    root = tk.Tk()
    game = StreamkoGame(root)
    root.mainloop()
