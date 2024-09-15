import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
import csv

class ExpenseTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Expense Tracker")
        self.geometry("800x600")
        self.configure(bg="#CECEFF")
        self.expenses = []
        self.categories = ["Food", "Transportation", "Utilities", "Entertainment", "Other"]
        self.create_widgets()
        self.load_expenses()

    def create_widgets(self):
        self.label = tk.Label(self, text="Expense Tracker", font=("Arial", 24, "bold"), bg="#CECEFF", fg="#5C6BC0")
        self.label.pack(pady=20)

        self.frame_list = tk.Frame(self, bg="#CECEFF")
        self.frame_list.pack(pady=20)
        
        self.scrollbar = tk.Scrollbar(self.frame_list)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.expense_listbox = tk.Listbox(self.frame_list, font=("Arial", 12), width=70, yscrollcommand=self.scrollbar.set, bg="#ffffff", fg="#333333")
        self.expense_listbox.pack(pady=5)
        self.scrollbar.config(command=self.expense_listbox.yview)

        button_font = ("Arial", 12)
        button_bg_color = "#00BFFF"
        button_hover_color = "#87CEFA"

        self.delete_button = tk.Button(self, text="Delete Expense", font=button_font, bg=button_bg_color, fg="#ffffff", activebackground=button_hover_color, command=self.delete_expense)
        self.delete_button.pack(pady=5)
        self.save_button = tk.Button(self, text="Save Expenses", font=button_font, bg=button_bg_color, fg="#ffffff", activebackground=button_hover_color, command=self.save_expenses)
        self.save_button.pack(pady=5)
        self.show_chart_button = tk.Button(self, text="Show Expenses Chart", font=button_font, bg=button_bg_color, fg="#ffffff", activebackground=button_hover_color, command=self.show_expenses_chart)
        self.show_chart_button.pack(pady=5)

        self.total_label = tk.Label(self, text="Total Expenses:", font=("Arial", 14), bg="#CECEFF", fg="#5C6BC0")
        self.total_label.pack(pady=10)

        self.add_button = tk.Button(self, text="Add Expense", font=button_font, bg=button_bg_color, fg="#ffffff", activebackground=button_hover_color, command=self.open_add_expense_window)
        self.add_button.pack(pady=10)

    def open_add_expense_window(self):
        AddExpenseWindow(self)

    def add_expense(self, expense, description, category, date):
        self.expenses.append((expense, description, category, date))
        self.refresh_list()
        self.update_total_label()

    def delete_expense(self):
        try:
            selected_expense_index = self.expense_listbox.curselection()[0]
            del self.expenses[selected_expense_index]
            self.refresh_list()
            self.update_total_label()
        except IndexError:
            messagebox.showwarning("Warning", "No expense selected to delete.")
    
    def save_expenses(self):
        with open("expenses.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Expense", "Description", "Category", "Date"])
            writer.writerows(self.expenses)
        messagebox.showinfo("Info", "Expenses saved successfully.")

    def load_expenses(self):
        try:
            with open("expenses.csv", mode="r") as file:
                reader = csv.reader(file)
                next(reader)
                self.expenses = [tuple(row) for row in reader]
                self.refresh_list()
                self.update_total_label()
        except FileNotFoundError:
            pass

    def show_expenses_chart(self):
        category_totals = {}
        for expense, _, category, _ in self.expenses:
            try:
                amount = float(expense)
            except ValueError:
                continue
            category_totals[category] = category_totals.get(category, 0) + amount
        categories = list(category_totals.keys())
        expenses = list(category_totals.values())
        plt.figure(figsize=(8, 6))
        plt.pie(expenses, labels=categories, autopct="%1.1f%%", startangle=140, shadow=True)
        plt.axis("equal")
        plt.title("Expense Categories Distribution")
        plt.show()

    def refresh_list(self):
        self.expense_listbox.delete(0, tk.END)
        for expense, description, category, date in self.expenses:
            self.expense_listbox.insert(tk.END, f"₹{expense} - {description} - {category} ({date})")

    def update_total_label(self):
        total_expenses = sum(float(expense[0]) for expense in self.expenses)
        self.total_label.config(text=f"Total Expenses: ₹{total_expenses:.2f}")


class AddExpenseWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add Expense")
        self.geometry("400x300")
        self.configure(bg="#CECEFF")
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        label_font = ("Arial", 12)
        entry_font = ("Arial", 12)

        tk.Label(self, text="Expense Amount:", font=label_font, bg="#CECEFF", fg="#5C6BC0").pack(pady=5)
        self.expense_entry = tk.Entry(self, font=entry_font)
        self.expense_entry.pack(pady=5)

        tk.Label(self, text="Item Description:", font=label_font, bg="#CECEFF", fg="#5C6BC0").pack(pady=5)
        self.item_entry = tk.Entry(self, font=entry_font)
        self.item_entry.pack(pady=5)

        tk.Label(self, text="Category:", font=label_font, bg="#CECEFF", fg="#5C6BC0").pack(pady=5)
        self.category_var = tk.StringVar(self)
        self.category_var.set(self.parent.categories[0])
        self.category_dropdown = ttk.Combobox(self, textvariable=self.category_var, values=self.parent.categories, font=entry_font)
        self.category_dropdown.pack(pady=5)

        tk.Label(self, text="Date:", font=label_font, bg="#CECEFF", fg="#5C6BC0").pack(pady=5)
        self.date_entry = DateEntry(self, font=entry_font)
        self.date_entry.pack(pady=5)

        button_font = ("Arial", 12)
        button_color = "#00BFFF"
        button_hover_color = "#87CEFA"

        tk.Button(self, text="Add Expense", font=button_font, bg=button_color, fg="#ffffff", activebackground=button_hover_color, command=self.add_expense).pack(pady=10)
        tk.Button(self, text="Cancel", font=button_font, bg=button_color, fg="#ffffff", activebackground=button_hover_color, command=self.destroy).pack(pady=5)

    def add_expense(self):
        expense = self.expense_entry.get()
        description = self.item_entry.get()
        category = self.category_var.get()
        date = self.date_entry.get_date().strftime("%Y-%m-%d")
        if expense and description and date:
            self.parent.add_expense(expense, description, category, date)
            self.destroy()
        else:
            messagebox.showwarning("Warning", "All fields are required.")


if __name__ == "__main__":
    app = ExpenseTrackerApp()
    app.mainloop()