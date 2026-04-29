import tkinter as tk
from tkinter import ttk, messagebox
from models.student import get_student_by_id, delete_student, update_student
from models.enrollment import get_courses_for_student, enroll_student
from models.course import get_all_courses


class StudentProfileWindow:
    def __init__(self, parent, student_id, refresh_callback):
        self.student_id = student_id
        self.refresh_callback = refresh_callback

        self.window = tk.Toplevel(parent)
        self.window.title("Student Profile")
        self.window.geometry("500x850")

        self.create_widgets()

    def create_widgets(self):
        student = get_student_by_id(self.student_id)

        if not student:
            messagebox.showerror("Error", "Student not found.")
            self.window.destroy()
            return

        self.first_name = self.create_entry("First Name", student[1])
        self.last_name = self.create_entry("Last Name", student[2])
        self.age = self.create_entry("Age", student[3])
        self.gender = self.create_entry("Gender", student[4])
        self.email = self.create_entry("Email", student[5])
        self.payment_status = self.create_entry("Payment Status", student[6])
        self.payment_method = self.create_entry("Payment Method", student[7])
        self.notes = self.create_entry("Notes", student[8])

        save_btn = ttk.Button(
            self.window,
            text="Save Changes",
            command=self.update_student_data
        )
        save_btn.pack(pady=10)

        courses_label = ttk.Label(self.window, text="Enrolled Courses")
        courses_label.pack(anchor="w", padx=20, pady=(15, 5))

        self.courses_tree = ttk.Treeview(
            self.window,
            columns=("ID", "Course", "Duration"),
            show="headings",
            height=5
        )

        self.courses_tree.heading("ID", text="ID")
        self.courses_tree.heading("Course", text="Course")
        self.courses_tree.heading("Duration", text="Duration")

        self.courses_tree.column("ID", width=40, anchor="center")
        self.courses_tree.column("Course", width=200)
        self.courses_tree.column("Duration", width=120)

        self.courses_tree.pack(padx=20, pady=5, fill="x")

        courses = get_courses_for_student(self.student_id)

        for course in courses:
            self.courses_tree.insert("", "end", values=(course[0], course[1], course[2]))

        remove_course_btn = ttk.Button(
            self.window,
            text="Remove Selected Course",
            command=self.remove_selected_course
        )
        remove_course_btn.pack(pady=5)

        add_course_label = ttk.Label(self.window, text="Add Course")
        add_course_label.pack(anchor="w", padx=20, pady=(10, 5))

        all_courses = get_all_courses()
        self.course_map = {f"{c[1]} ({c[2]})": c[0] for c in all_courses}

        self.new_course_var = tk.StringVar()

        course_dropdown = ttk.Combobox(
            self.window,
            textvariable=self.new_course_var,
            values=list(self.course_map.keys()),
            state="readonly"
        )
        course_dropdown.pack(padx=20, pady=5, fill="x")

        enroll_btn = ttk.Button(
            self.window,
            text="Enroll in Course",
            command=self.enroll_new_course
        )
        enroll_btn.pack(pady=10)

        delete_btn = ttk.Button(
            self.window,
            text="Delete Student",
            command=self.delete_current_student
        )
        delete_btn.pack(pady=10)

    def create_entry(self, label_text, value):
        label = ttk.Label(self.window, text=label_text)
        label.pack(anchor="w", padx=20)

        entry = ttk.Entry(self.window)
        entry.insert(0, "" if value is None else str(value))
        entry.pack(padx=20, pady=5, fill="x")

        return entry

    def update_student_data(self):
        try:
            update_student(
                self.student_id,
                self.first_name.get(),
                self.last_name.get(),
                int(self.age.get()) if self.age.get() else None,
                self.gender.get(),
                self.email.get(),
                self.payment_status.get(),
                self.payment_method.get(),
                self.notes.get()
            )

            self.refresh_callback()
            messagebox.showinfo("Success", "Student updated successfully!")

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def enroll_new_course(self):
        try:
            if not self.new_course_var.get():
                messagebox.showerror("Error", "Please select a course.")
                return

            course_id = self.course_map[self.new_course_var.get()]

            enroll_student(self.student_id, course_id)

            messagebox.showinfo("Success", "Student enrolled successfully.")
            self.window.destroy()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def remove_selected_course(self):
        from models.enrollment import remove_enrollment

        selected = self.courses_tree.selection()

        if not selected:
            messagebox.showerror("Error", "Please select a course to remove.")
            return

        item = self.courses_tree.item(selected)
        course_id = item["values"][0]
        course_name = item["values"][1]

        confirm = messagebox.askyesno(
            "Confirm Remove",
            f"Remove this student from {course_name}?"
        )

        if not confirm:
            return

        remove_enrollment(self.student_id, course_id)

        messagebox.showinfo("Success", "Course removed from student.")
        self.window.destroy()

    def delete_current_student(self):
        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this student?"
        )

        if confirm:
            delete_student(self.student_id)
            self.refresh_callback()
            messagebox.showinfo("Deleted", "Student deleted successfully.")
            self.window.destroy()