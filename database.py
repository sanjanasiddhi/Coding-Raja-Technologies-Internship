import tkinter as tk
from tkinter import Label, ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
from tkinter import PhotoImage

class Task:
    def __init__(self, name, priority, due_date):
        self.name = name
        self.priority = priority
        self.due_date = due_date

class ToDoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("My-To-Do-List")
        self.tasks = []
        self.completed_tasks = []
        self.my_task_var = tk.StringVar()
        self.priority_var = tk.StringVar()
        self.due_date_var = tk.StringVar()

        self.create_widgets()
        Image_icon = PhotoImage(file="C:/Users/sanja/Downloads/todolist.png")
        root.iconphoto(False, Image_icon)

    def create_widgets(self):
        self.task_list_treeview = ttk.Treeview(self.root, columns=("Priority", "Due Date"))
        self.task_list_treeview.grid(row=225, column=55, columnspan=2, padx=10, pady=10)
        self.task_list_treeview.heading("#0", text="My Task")
        self.task_list_treeview.heading("Priority", text="Priority")
        self.task_list_treeview.heading("Due Date", text="Due Date")

        tk.Label(self.root, text="My Task Name:").grid(row=222, column=46)
        my_task_name_entry = tk.Entry(self.root, textvariable=self.my_task_var)
        my_task_name_entry.grid(row=222, column=47, padx=10, pady=80)

        tk.Label(self.root, text="Priority level:").grid(row=222, column=53)
        priority_values = ["Low", "Medium", "High"]
        priority_dropdown = ttk.Combobox(self.root, textvariable=self.priority_var, values=priority_values)
        priority_dropdown.grid(row=222, column=54, padx=10, pady=0)

        tk.Label(self.root, text="Due Date:").grid(row=222, column=59)
        due_date_entry = DateEntry(self.root, textvariable=self.due_date_var, date_pattern="yyyy-mm-dd")
        due_date_entry.grid(row=222, column=60, padx=10, pady=10)

        add_task_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        add_task_button.grid(row=280, column=52, columnspan=2, padx=10, pady=5)

        delete_completed_task_button = tk.Button(self.root, text="Delete Task", command=self.delete_task)
        delete_completed_task_button.grid(row=280, column=67, padx=10, pady=5)

    
        self.completed_task_list_treeview = ttk.Treeview(self.root, columns=("Status"))
        self.completed_task_list_treeview.grid(row=300, column=55, columnspan=2, padx=10, pady=10)
        self.completed_task_list_treeview.heading("#0", text="My Task")
        self.completed_task_list_treeview.heading("Status", text="Status")

        complete_task_button = tk.Button(self.root, text="Complete Task", command=self.complete_task)
        complete_task_button.grid(row=280, column=58, columnspan=2, padx=10, pady=10)


    def add_task(self):
        name = self.my_task_var.get()
        priority = self.priority_var.get()
        due_date = self.due_date_var.get()

        if name and priority and due_date:
            task = Task(name, priority, due_date)
            self.tasks.append(task)
            self.task_list_treeview.insert("", tk.END, text=task.name, values=(task.priority, task.due_date))
            self.my_task_var.set("")
            self.priority_var.set("")
            self.due_date_var.set("")   
            self.save_tasks_to_file()
        else:
            messagebox.showerror("Error", "Enter valid data. Retry!!")

    def complete_task(self):
        selected_item = self.task_list_treeview.selection()
        if selected_item:
            completed_task = self.task_list_treeview.item(selected_item)
            self.task_list_treeview.delete(selected_item)
            completed_task["values"] = ("Completed", datetime.now().strftime("%Y-%m-%d"))
            task_name = completed_task["text"]
            for task in self.tasks:
                if task.name == task_name:
                    self.tasks.remove(task)
                    self.completed_tasks.append(task)
                    self.completed_task_list_treeview.insert("", tk.END, text=task.name, values=("Completed", datetime.now().strftime("%Y-%m-%d")))
                    self.save_tasks_to_file()
                    break

    def delete_task(self):
        selected_item = self.task_list_treeview.selection()
        if selected_item:
            task_name = self.task_list_treeview.item(selected_item)["text"]
            for task in self.tasks:
                if task.name == task_name:
                    self.tasks.remove(task)
                    self.task_list_treeview.delete(selected_item)
                    self.save_tasks_to_file()
                    break

    def save_tasks_to_file(self):
        with open("tasks.txt", "w") as file:
            for task in self.tasks:
                file.write(f"{task.name}-{task.priority}-{task.due_date}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoListApp(root)
    Label(root, text='Hi!! Welcome To Your To-Do-List', bg='gray', font=("Times New Roman", 25), wraplength=600).place(x=650, y=0)
    Label(root, text='Dont just make a to-do list, make a to-thrive list.....', bg='yellow green', font=("Calligraphic", 20), wraplength=650).place(x=520, y=820)
    
    root.mainloop()