import tkinter as tk
from tkinter import ttk, messagebox
from models.student import add_student


class AddStudentWindow:
    def __init__(self, parent, refresh_callback=None, dark_mode=False):
        from ui.theme_utils import apply_popup_theme
        self.refresh_callback = refresh_callback

        self.window = tk.Toplevel(parent)
        self.window.title("Add Student")
        self.window.geometry("400x500")

        self.dark_mode = dark_mode
        self.create_widgets()

        apply_popup_theme(self.window, self.dark_mode)

    def create_widgets(self):
        self.first_name_entry = self.create_label_entry("First Name")
        self.last_name_entry = self.create_label_entry("Last Name")
        self.age_entry = self.create_label_entry("Age")
        self.gender_entry = self.create_label_entry("Gender")
        self.email_entry = self.create_label_entry("Email")
        self.payment_status_entry = self.create_label_entry("Payment Status")
        self.payment_method_entry = self.create_label_entry("Payment Method")
        self.notes_entry = self.create_label_entry("Notes")

        submit_btn = ttk.Button(
            self.window,
            text="Save Student",
            command=self.save_student
        )
        submit_btn.pack(pady=20)

    def create_label_entry(self, label_text):
        label = ttk.Label(self.window, text=label_text)
        label.pack()

        entry = ttk.Entry(self.window)
        entry.pack(pady=5)

        return entry

    def save_student(self):
        try:
            add_student(
                self.first_name_entry.get(),
                self.last_name_entry.get(),
                int(self.age_entry.get()) if self.age_entry.get() else None,
                self.gender_entry.get(),
                self.email_entry.get(),
                self.payment_status_entry.get(),
                self.payment_method_entry.get(),
                self.notes_entry.get()
            )

            if self.refresh_callback:
                self.refresh_callback()

            messagebox.showinfo("Success", "Student added successfully!")
            self.window.destroy()

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    