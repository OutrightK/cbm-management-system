import tkinter as tk
from tkinter import ttk, messagebox
from models.course import get_course_by_id, update_course, delete_course
from models.enrollment import get_students_in_course, remove_enrollment


class CourseProfileWindow:
    def __init__(self, parent, course_id, refresh_callback):
        self.course_id = course_id
        self.refresh_callback = refresh_callback

        self.window = tk.Toplevel(parent)
        self.window.title("Course Profile")
        self.window.geometry("500x600")

        self.create_widgets()

    def create_widgets(self):
        course = get_course_by_id(self.course_id)

        if not course:
            messagebox.showerror("Error", "Course not found.")
            self.window.destroy()
            return

        self.name_entry = self.create_entry("Course Name", course[1])
        self.duration_entry = self.create_entry("Duration", course[2])

        save_btn = ttk.Button(
            self.window,
            text="Save Changes",
            command=self.save_changes
        )
        save_btn.pack(pady=10)

        students_label = ttk.Label(self.window, text="Enrolled Students")
        students_label.pack(anchor="w", padx=20, pady=(15, 5))

        self.students_tree = ttk.Treeview(
            self.window,
            columns=("ID", "Name", "Email"),
            show="headings",
            height=6
        )

        self.students_tree.heading("ID", text="ID")
        self.students_tree.heading("Name", text="Name")
        self.students_tree.heading("Email", text="Email")

        self.students_tree.column("ID", width=50, anchor="center")
        self.students_tree.column("Name", width=200)
        self.students_tree.column("Email", width=220)

        self.students_tree.pack(padx=20, pady=5, fill="x")

        students = get_students_in_course(self.course_id)

        for s in students:
            self.students_tree.insert("", "end", values=(s[0], s[1], s[2]))

        remove_student_btn = ttk.Button(
            self.window,
            text="Remove Selected Student",
            command=self.remove_selected_student
        )
        remove_student_btn.pack(pady=5)

        delete_btn = ttk.Button(
            self.window,
            text="Delete Course",
            command=self.delete_current_course
        )
        delete_btn.pack(pady=10)

    def create_entry(self, label_text, value):
        label = ttk.Label(self.window, text=label_text)
        label.pack(anchor="w", padx=20)

        entry = ttk.Entry(self.window)
        entry.insert(0, "" if value is None else str(value))
        entry.pack(padx=20, pady=5, fill="x")

        return entry

    def save_changes(self):
        try:
            update_course(
                self.course_id,
                self.name_entry.get(),
                self.duration_entry.get()
            )

            self.refresh_callback()
            messagebox.showinfo("Success", "Course updated successfully.")

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def remove_selected_student(self):
        selected = self.students_tree.selection()

        if not selected:
            messagebox.showerror("Error", "Please select a student.")
            return

        item = self.students_tree.item(selected)
        student_id = item["values"][0]
        student_name = item["values"][1]

        confirm = messagebox.askyesno(
            "Confirm Remove",
            f"Remove {student_name} from this course?"
        )

        if not confirm:
            return

        remove_enrollment(student_id, self.course_id)

        messagebox.showinfo("Success", "Student removed from course.")
        self.window.destroy()

    def delete_current_course(self):
        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this course?"
        )

        if confirm:
            delete_course(self.course_id)
            self.refresh_callback()
            messagebox.showinfo("Deleted", "Course deleted successfully.")
            self.window.destroy()