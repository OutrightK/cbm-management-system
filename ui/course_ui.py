import tkinter as tk
from tkinter import ttk, messagebox
from models.course import add_course


class AddCourseWindow:
    def __init__(self, parent, refresh_callback, dark_mode=False):
        from ui.theme_utils import apply_popup_theme
        self.refresh_callback = refresh_callback

        self.window = tk.Toplevel(parent)
        self.window.title("Add Course")
        self.window.geometry("350x250")

        self.dark_mode = dark_mode

        self.create_widgets()

        apply_popup_theme(self.window, self.dark_mode)

    def create_widgets(self):
        self.name_entry = self.create_entry("Course Name")
        self.duration_entry = self.create_entry("Duration")

        save_btn = ttk.Button(
            self.window,
            text="Save Course",
            command=self.save_course
        )
        save_btn.pack(pady=15)

    def create_entry(self, label_text):
        label = ttk.Label(self.window, text=label_text)
        label.pack(anchor="w", padx=20)

        entry = ttk.Entry(self.window)
        entry.pack(padx=20, pady=5, fill="x")

        return entry

    def save_course(self):
        try:
            add_course(
                self.name_entry.get(),
                self.duration_entry.get()
            )

            self.refresh_callback()
            messagebox.showinfo("Success", "Course added successfully!")
            self.window.destroy()

        except ValueError as e:
            messagebox.showerror("Error", str(e))