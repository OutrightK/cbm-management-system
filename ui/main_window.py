import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from models.student import get_all_students, search_students
from config.settings import load_settings, save_settings
from ui.theme_utils import apply_popup_theme


APP_BG = "#ecf0f1"
SIDEBAR_BG = "#2c3e50"
SIDEBAR_BUTTON_BG = "#34495e"
SIDEBAR_ACTIVE_BG = "#1abc9c"
CARD_BG = "white"
TEXT_DARK = "#2d3436"

FONT_TITLE = ("Arial", 20, "bold")
FONT_PAGE_TITLE = ("Arial", 18, "bold")
FONT_NORMAL = ("Arial", 11)
FONT_BUTTON = ("Arial", 10)

PADDING_SMALL = 5
PADDING_MEDIUM = 10
PADDING_LARGE = 20
PADDING_XL = 25


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CBM Management System")
        self.settings = load_settings()

        self.root.geometry(self.settings["window_geometry"])
        self.dark_mode = self.settings["dark_mode"]

        if self.settings["maximized"]:
            self.root.state("zoomed")

        if self.settings.get("auto_backup", True):
            self.auto_backup()

        self.create_layout()
        self.open_default_start_page()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_layout(self):
        self.sidebar = tk.Frame(self.root, width=220, bg=SIDEBAR_BG)
        self.sidebar.pack(side="left", fill="y")

        # toggle_btn = tk.Button(
        #     self.sidebar,
        #     text="Toggle Dark Mode",
        #     command=self.toggle_dark_mode,
        #     bg=SIDEBAR_BUTTON_BG,
        #     fg="white",
        #     bd=0,
        #     relief="flat",
        #     padx=20,
        #     pady=10
        # )
        # toggle_btn.pack(side="bottom", fill="x", pady=10)

        title = tk.Label(
            self.sidebar,
            text="CBM",
            font=FONT_TITLE,
            bg=SIDEBAR_BG,
            fg="white"
        )
        title.pack(pady=PADDING_XL)

        self.dashboard_btn = self.create_sidebar_button("Dashboard", self.show_dashboard_page)
        self.dashboard_btn.pack(fill="x", pady=2)

        self.students_btn = self.create_sidebar_button("Students", self.show_students_page)
        self.students_btn.pack(fill="x", pady=2)

        self.courses_btn = self.create_sidebar_button("Courses", self.show_courses_page)
        self.courses_btn.pack(fill="x", pady=2)

        self.enrollments_btn = self.create_sidebar_button("Enrollments", self.show_enrollments_page)
        self.enrollments_btn.pack(fill="x", pady=2)

        self.payments_btn = self.create_sidebar_button("Payments", self.show_payments_page)
        self.payments_btn.pack(fill="x", pady=2)

        self.right_area = tk.Frame(self.root, bg=APP_BG)
        self.right_area.pack(side="left", fill="both", expand=True)

        self.content = tk.Frame(self.right_area, bg=APP_BG)
        self.content.pack(fill="both", expand=True)

        self.status_label = tk.Label(
            self.right_area,
            text="Ready",
            bg="#dfe6e9",
            fg=TEXT_DARK,
            anchor="w",
            padx=PADDING_MEDIUM
        )
        self.status_label.pack(fill="x", side="bottom")

        self.settings_btn = tk.Button(
            self.sidebar,
            text="Settings",
            command=self.open_settings_window,
            bg=SIDEBAR_BUTTON_BG,
            fg="white",
            bd=0,
            relief="flat",
            anchor="w",
            padx=20,
            pady=10,
            activebackground=SIDEBAR_ACTIVE_BG,
            activeforeground="white"
        )
        self.settings_btn.pack(side="bottom", fill="x", pady=5)

    def create_sidebar_button(self, text, command):
        button = tk.Button(
            self.sidebar,
            text=text,
            command=lambda: self.set_active_page(button, command),
            bg=SIDEBAR_BUTTON_BG,
            fg="white",
            bd=0,
            relief="flat",
            anchor="w",
            padx=20,
            pady=10,
            activebackground=SIDEBAR_ACTIVE_BG,
            activeforeground="white"
        )
        return button

    def set_active_page(self, active_button, page_command):
        for widget in self.sidebar.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(bg=SIDEBAR_BUTTON_BG)

        active_button.config(bg=SIDEBAR_ACTIVE_BG)
        page_command()

    def set_status(self, message):
        self.status_label.config(text=message)

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def style_treeview(self):
        style = ttk.Style()
        style.configure("Treeview", rowheight=28, font=FONT_NORMAL)
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"))
        style.map(
            "Treeview",
            background=[("selected", "#74b9ff")],
            foreground=[("selected", "black")]
        )

    def show_students_page(self):
        self.clear_content()
        self.set_status("Viewing students")

        header_frame = tk.Frame(self.content, bg=APP_BG)
        header_frame.pack(fill="x", padx=PADDING_XL, pady=(PADDING_LARGE, PADDING_MEDIUM))

        title = tk.Label(
            header_frame,
            text="Students",
            font=FONT_PAGE_TITLE,
            bg=APP_BG,
            fg=TEXT_DARK
        )
        title.pack(side="left")

        subtitle = tk.Label(
            header_frame,
            text="Manage student profiles, payments, notes, and enrollments",
            font=FONT_NORMAL,
            bg=APP_BG,
            fg="#636e72"
        )
        subtitle.pack(side="left", padx=15)

        search_frame = tk.Frame(self.content, bg=APP_BG)
        search_frame.pack(fill="x", padx=PADDING_XL, pady=PADDING_MEDIUM)

        search_box = tk.Frame(search_frame, bg="white", bd=1, relief="solid")
        search_box.pack(side="left", padx=(5, 0))

        self.search_entry = tk.Entry(search_box, width=40, bd=0, relief="flat")
        self.search_entry.pack(side="left", padx=(6, 2), pady=4)
        self.search_entry.bind("<Return>", lambda event: self.search_students())

        clear_search_btn = tk.Button(
            search_box,
            text="✕",
            command=self.clear_student_search,
            bg="white",
            fg="#636e72",
            bd=0,
            relief="flat",
            cursor="hand2"
        )
        clear_search_btn.pack(side="left", padx=(2, 6))

        search_btn = tk.Button(
            search_frame,
            text="Search",
            command=self.search_students,
            bg="white",
            fg=TEXT_DARK,
            bd=1,
            relief="solid",
            cursor="hand2",
            font=("Arial", 9),
            padx=6,
            pady=2
        )
        search_btn.pack(side="left", padx=(0, PADDING_SMALL))

        btn_frame = tk.Frame(self.content, bg=APP_BG)
        btn_frame.pack(fill="x", padx=PADDING_XL, pady=PADDING_MEDIUM)

        add_student_btn = tk.Button(
            btn_frame,
            text="Add Student",
            command=self.open_add_student_window,
            bg=SIDEBAR_ACTIVE_BG,
            fg="white",
            font=FONT_BUTTON,
            relief="flat",
            padx=12,
            pady=6
        )
        add_student_btn.pack(side="left", padx=0)

        refresh_btn = ttk.Button(
            btn_frame,
            text="Refresh",
            command=self.load_students
        )
        refresh_btn.pack(side="left", padx=(8, 0))

        import_btn = ttk.Button(
            btn_frame,
            text="Import CSV",
            command=self.import_students_csv
        )
        import_btn.pack(side="left", padx=PADDING_SMALL)

        export_btn = ttk.Button(
            btn_frame,
            text="Export CSV",
            command=self.export_students_csv
        )
        export_btn.pack(side="left", padx=PADDING_SMALL)

        template_btn = ttk.Button(
            btn_frame,
            text="Template CSV",
            command=self.download_students_template_csv
        )
        template_btn.pack(side="left", padx=PADDING_SMALL)

        table_card = tk.Frame(self.content, bg=CARD_BG, bd=1, relief="solid")
        table_card.pack(fill="both", expand=True, padx=PADDING_XL, pady=(PADDING_SMALL, PADDING_LARGE))

        self.tree = ttk.Treeview(
            table_card,
            columns=("ID", "First Name", "Last Name", "Email", "Payment"),
            show="headings"
        )

        self.style_treeview()

        self.tree.heading("ID", text="ID")
        self.tree.heading("First Name", text="First Name")
        self.tree.heading("Last Name", text="Last Name")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Payment", text="Payment")

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("First Name", width=120)
        self.tree.column("Last Name", width=120)
        self.tree.column("Email", width=220)
        self.tree.column("Payment", width=120)

        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        self.tree.bind("<Double-1>", self.open_student_profile)

        self.load_students()
        self.apply_theme()

    def load_students(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        students = get_all_students()

        for index, s in enumerate(students):
            tag = "evenrow" if index % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=(s[0], s[1], s[2], s[5], s[6]), tags=(tag,))

        if self.dark_mode:
            self.tree.tag_configure("evenrow", background="#353b48", foreground="#ecf0f1")
            self.tree.tag_configure("oddrow", background="#2f3640", foreground="#ecf0f1")
        else:
            self.tree.tag_configure("evenrow", background="#f5f6fa", foreground="#2d3436")
            self.tree.tag_configure("oddrow", background="#dfe6e9", foreground="#2d3436")

    def search_students(self):
        keyword = self.search_entry.get()

        results = search_students(keyword)

        for row in self.tree.get_children():
            self.tree.delete(row)

        for index, s in enumerate(results):
            tag = "evenrow" if index % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=(s[0], s[1], s[2], s[5], s[6]), tags=(tag,))

        if self.dark_mode:
            self.tree.tag_configure("evenrow", background="#353b48", foreground="#ecf0f1")
            self.tree.tag_configure("oddrow", background="#2f3640", foreground="#ecf0f1")
        else:
            self.tree.tag_configure("evenrow", background="#f5f6fa", foreground="#2d3436")
            self.tree.tag_configure("oddrow", background="#dfe6e9", foreground="#2d3436")
            
        self.set_status("Student search completed.")

    def clear_student_search(self):
        self.search_entry.delete(0, tk.END)
        self.load_students()
        self.set_status("Student search cleared.")

    def open_add_student_window(self):
        from ui.student_ui import AddStudentWindow
        AddStudentWindow(
            self.root,
            lambda: [self.load_students(), self.set_status("Student added successfully.")],
            self.dark_mode
        )

    def open_student_profile(self, event):
        selected_item = self.tree.selection()

        if not selected_item:
            return

        student_data = self.tree.item(selected_item)["values"]
        student_id = student_data[0]

        from ui.student_profile_ui import StudentProfileWindow
        StudentProfileWindow(self.root, student_id, self.load_students)

    def show_courses_page(self):
        from models.course import get_all_courses

        self.clear_content()
        self.set_status("Viewing courses")

        title = tk.Label(
            self.content,
            text="Courses",
            font=FONT_PAGE_TITLE,
            bg=APP_BG,
            fg=TEXT_DARK
        )
        title.pack(pady=PADDING_MEDIUM)

        search_frame = tk.Frame(self.content, bg=APP_BG)
        search_frame.pack(fill="x", padx=PADDING_XL, pady=PADDING_MEDIUM)

        search_box = tk.Frame(search_frame, bg="white", bd=1, relief="solid")
        search_box.pack(side="left", padx=(5, 0))

        self.course_search_entry = tk.Entry(search_box, width=40, bd=0, relief="flat")
        self.course_search_entry.pack(side="left", padx=(6, 2), pady=4)
        self.course_search_entry.bind("<Return>", lambda event: self.search_courses())

        clear_btn = tk.Button(
            search_box,
            text="✕",
            command=self.clear_course_search,
            bg="white",
            fg="#636e72",
            bd=0,
            relief="flat",
            cursor="hand2"
        )
        clear_btn.pack(side="left", padx=(2, 6))

        search_btn = tk.Button(
            search_frame,
            text="Search",
            command=self.search_courses,
            bg="white",
            fg=TEXT_DARK,
            bd=1,
            relief="solid",
            cursor="hand2",
            font=("Arial", 9),
            padx=6,
            pady=2
        )
        search_btn.pack(side="left", padx=(0, PADDING_SMALL))

        btn_frame = tk.Frame(self.content, bg=APP_BG)
        btn_frame.pack(pady=PADDING_MEDIUM)

        add_btn = ttk.Button(
            btn_frame,
            text="Add Course",
            command=self.open_add_course_window
        )
        add_btn.pack(side="left", padx=PADDING_SMALL)

        refresh_btn = ttk.Button(
            btn_frame,
            text="Refresh",
            command=self.show_courses_page
        )
        refresh_btn.pack(side="left", padx=PADDING_SMALL)

        import_btn = ttk.Button(
            btn_frame,
            text="Import CSV",
            command=self.import_courses_csv
        )
        import_btn.pack(side="left", padx=PADDING_SMALL)

        export_btn = ttk.Button(
            btn_frame,
            text="Export CSV",
            command=self.export_courses_csv
        )
        export_btn.pack(side="left", padx=PADDING_SMALL)

        template_btn = ttk.Button(
            btn_frame,
            text="Template CSV",
            command=self.download_courses_template_csv
        )
        template_btn.pack(side="left", padx=PADDING_SMALL)

        self.course_tree = ttk.Treeview(
            self.content,
            columns=("ID", "Name", "Duration"),
            show="headings"
        )

        self.style_treeview()

        self.course_tree.heading("ID", text="ID")
        self.course_tree.heading("Name", text="Course Name")
        self.course_tree.heading("Duration", text="Duration")

        self.course_tree.column("ID", width=60, anchor="center")
        self.course_tree.column("Name", width=250)
        self.course_tree.column("Duration", width=150)

        self.course_tree.pack(fill="both", expand=True, padx=PADDING_XL, pady=PADDING_MEDIUM)
        self.course_tree.bind("<Double-1>", self.open_course_profile)

        courses = get_all_courses()

        for c in courses:
            self.course_tree.insert("", "end", values=(c[0], c[1], c[2]))

        self.apply_theme()

    def search_courses(self):
        from models.course import get_all_courses

        keyword = self.course_search_entry.get().lower()

        for row in self.course_tree.get_children():
            self.course_tree.delete(row)

        courses = get_all_courses()

        for c in courses:
            name = str(c[1]).lower()
            duration = str(c[2]).lower()

            if keyword in name or keyword in duration:
                self.course_tree.insert("", "end", values=(c[0], c[1], c[2]))

        self.set_status("Course search completed.")

    def clear_course_search(self):
        self.course_search_entry.delete(0, tk.END)
        self.show_courses_page()
        self.set_status("Course search cleared.")

    def open_add_course_window(self):
        from ui.course_ui import AddCourseWindow
        AddCourseWindow(
            self.root,
            lambda: [self.show_courses_page(), self.set_status("Course added successfully.")],
            self.dark_mode
        )

    def open_course_profile(self, event):
        selected_item = self.course_tree.selection()

        if not selected_item:
            return

        course_data = self.course_tree.item(selected_item)["values"]
        course_id = course_data[0]

        from ui.course_profile_ui import CourseProfileWindow
        CourseProfileWindow(
            self.root,
            course_id,
            lambda: [self.show_courses_page(), self.set_status("Course updated.")]
        )

    def show_enrollments_page(self):
        from models.student import get_all_students
        from models.course import get_all_courses
        from models.enrollment import enroll_student, get_students_with_courses, remove_enrollment

        self.clear_content()
        self.set_status("Managing enrollments")

        title = tk.Label(
            self.content,
            text="Enrollments",
            font=FONT_PAGE_TITLE,
            bg=APP_BG,
            fg=TEXT_DARK
        )
        title.pack(pady=PADDING_MEDIUM)

        filter_frame = tk.Frame(self.content, bg=APP_BG)
        filter_frame.pack(fill="x", padx=PADDING_XL, pady=PADDING_MEDIUM)

        search_box = tk.Frame(filter_frame, bg="white", bd=1, relief="solid")
        search_box.pack(side="left", padx=(0, 0))

        self.enrollment_filter_entry = tk.Entry(search_box, width=40, bd=0, relief="flat")
        self.enrollment_filter_entry.pack(side="left", padx=(6, 2), pady=4)
        self.enrollment_filter_entry.bind("<Return>", lambda event: self.filter_enrollments())

        clear_btn = tk.Button(
            search_box,
            text="✕",
            command=self.clear_enrollment_filter,
            bg="white",
            fg="#636e72",
            bd=0,
            relief="flat",
            cursor="hand2"
        )
        clear_btn.pack(side="left", padx=(2, 6))

        filter_btn = tk.Button(
            filter_frame,
            text="Search",
            command=self.filter_enrollments,
            bg="white",
            fg=TEXT_DARK,
            bd=1,
            relief="solid",
            cursor="hand2",
            font=("Arial", 9),
            padx=6,
            pady=2
        )
        filter_btn.pack(side="left", padx=(0, PADDING_SMALL))

        select_frame = tk.Frame(self.content, bg=APP_BG)
        select_frame.pack(pady=PADDING_MEDIUM)

        students = get_all_students()
        self.student_map = {f"{s[1]} {s[2]}": s[0] for s in students}

        self.student_var = tk.StringVar()
        student_dropdown = ttk.Combobox(
            select_frame,
            textvariable=self.student_var,
            values=list(self.student_map.keys()),
            state="readonly",
            width=25
        )
        student_dropdown.pack(side="left", padx=PADDING_MEDIUM)

        courses = get_all_courses()
        self.course_map = {f"{c[1]} ({c[2]})": c[0] for c in courses}

        self.course_var = tk.StringVar()
        course_dropdown = ttk.Combobox(
            select_frame,
            textvariable=self.course_var,
            values=list(self.course_map.keys()),
            state="readonly",
            width=25
        )
        course_dropdown.pack(side="left", padx=PADDING_MEDIUM)

        def enroll_action():
            try:
                if not self.student_var.get():
                    messagebox.showerror("Error", "Please select a student.")
                    self.set_status("Enrollment failed: no student selected.")
                    return

                if not self.course_var.get():
                    messagebox.showerror("Error", "Please select a course.")
                    self.set_status("Enrollment failed: no course selected.")
                    return

                student_id = self.student_map[self.student_var.get()]
                course_id = self.course_map[self.course_var.get()]

                enroll_student(student_id, course_id)

                load_enrollments()
                self.set_status("Student enrolled successfully.")

            except Exception as e:
                messagebox.showerror("Error", str(e))
                self.set_status("Enrollment failed.")

        enroll_btn = ttk.Button(select_frame, text="Enroll", command=enroll_action)
        enroll_btn.pack(side="left", padx=PADDING_MEDIUM)

        import_btn = ttk.Button(
            select_frame,
            text="Import CSV",
            command=self.import_enrollments_csv
        )
        import_btn.pack(side="left", padx=PADDING_SMALL)

        export_btn = ttk.Button(
            select_frame,
            text="Export CSV",
            command=self.export_enrollments_csv
        )
        export_btn.pack(side="left", padx=PADDING_SMALL)

        template_btn = ttk.Button(
            select_frame,
            text="Template CSV",
            command=self.download_enrollments_template_csv
        )
        template_btn.pack(side="left", padx=PADDING_SMALL)

        self.enrollment_tree = ttk.Treeview(
            self.content,
            columns=("Student", "Course"),
            show="headings"
        )

        self.style_treeview()

        self.enrollment_tree.heading("Student", text="Student")
        self.enrollment_tree.heading("Course", text="Course")

        self.enrollment_tree.column("Student", width=250)
        self.enrollment_tree.column("Course", width=250)

        self.enrollment_tree.pack(fill="both", expand=True, padx=PADDING_XL, pady=PADDING_MEDIUM)

        remove_btn = ttk.Button(
            self.content,
            text="Remove Selected Enrollment",
            command=lambda: remove_selected_enrollment(None)
        )
        remove_btn.pack(pady=PADDING_SMALL)

        self.apply_theme()

        def remove_selected_enrollment(_event):
            selected = self.enrollment_tree.selection()

            if not selected:
                return

            item = self.enrollment_tree.item(selected)
            student_name, course_name = item["values"]

            confirm = messagebox.askyesno(
                "Confirm Remove",
                f"Remove {student_name} from {course_name}?"
            )

            if not confirm:
                return

            try:
                student_id = self.student_map[student_name]

                course_id = None
                for key, value in self.course_map.items():
                    if key.startswith(course_name):
                        course_id = value
                        break

                if course_id is None:
                    raise ValueError("Course could not be found.")

                remove_enrollment(student_id, course_id)
                load_enrollments()
                self.set_status("Enrollment removed.")

            except Exception as e:
                messagebox.showerror("Error", str(e))
                self.set_status("Could not remove enrollment.")

        

        def load_enrollments():
            for row in self.enrollment_tree.get_children():
                self.enrollment_tree.delete(row)

            data = get_students_with_courses()

            for row in data:
                self.enrollment_tree.insert("", "end", values=row)

        load_enrollments()
        self.apply_theme()

    def filter_enrollments(self):
        from models.enrollment import get_students_with_courses

        keyword = self.enrollment_filter_entry.get().strip().lower()

        for row in self.enrollment_tree.get_children():
            self.enrollment_tree.delete(row)

        enrollments = get_students_with_courses()

        for enrollment in enrollments:
            student_name = str(enrollment[0]).lower()
            course_name = str(enrollment[1]).lower()

            if keyword in student_name or keyword in course_name:
                self.enrollment_tree.insert("", "end", values=enrollment)

        self.set_status("Enrollment filter applied.")

        self.apply_theme()

    def clear_enrollment_filter(self):
        self.enrollment_filter_entry.delete(0, tk.END)
        self.show_enrollments_page()
        self.set_status("Enrollment filter cleared.")

    def show_payments_page(self):
        self.clear_content()
        self.set_status("Viewing payments")

        title = tk.Label(
            self.content,
            text="Payments",
            font=FONT_PAGE_TITLE,
            bg=APP_BG,
            fg=TEXT_DARK
        )
        title.pack(pady=PADDING_LARGE)

        message = tk.Label(
            self.content,
            text="Payment overview will be added later.",
            bg=APP_BG
        )
        message.pack()

        self.apply_theme()

    def export_students_csv(self):
        import csv
        from models.student import get_all_students

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )

        if not file_path:
            return

        students = get_all_students()

        try:
            with open(file_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)

                writer.writerow([
                    "ID", "First Name", "Last Name", "Age",
                    "Gender", "Email", "Payment Status",
                    "Payment Method", "Notes"
                ])

                for s in students:
                    writer.writerow(s)

            self.set_status("Students exported to CSV.")

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.set_status("Export failed.")

    def export_courses_csv(self):
        import csv
        from models.course import get_all_courses

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )

        if not file_path:
            return

        courses = get_all_courses()

        try:
            with open(file_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)

                writer.writerow(["ID", "Course Name", "Duration"])

                for course in courses:
                    writer.writerow(course)

            self.set_status("Courses exported to CSV.")

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.set_status("Course export failed.")

    def export_enrollments_csv(self):
        import csv
        from models.enrollment import get_students_with_courses

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )

        if not file_path:
            return

        enrollments = get_students_with_courses()

        try:
            with open(file_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)

                writer.writerow(["Student", "Course"])

                for enrollment in enrollments:
                    writer.writerow(enrollment)

            self.set_status("Enrollments exported to CSV.")

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.set_status("Enrollment export failed.")

    def import_students_csv(self):
        import csv
        from models.student import add_student

        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv")]
        )

        if not file_path:
            return

        imported_count = 0
        skipped_count = 0

        try:
            with open(file_path, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    try:
                        age_value = row.get("Age", "").strip()

                        add_student(
                            row.get("First Name", "").strip(),
                            row.get("Last Name", "").strip(),
                            int(age_value) if age_value else None,
                            row.get("Gender", "").strip(),
                            row.get("Email", "").strip(),
                            row.get("Payment Status", "").strip(),
                            row.get("Payment Method", "").strip(),
                            row.get("Notes", "").strip()
                        )

                        imported_count += 1

                    except Exception:
                        skipped_count += 1

            self.load_students()
            self.set_status(f"Imported {imported_count} students. Skipped {skipped_count}.")

            messagebox.showinfo(
                "Import Complete",
                f"Imported: {imported_count}\nSkipped: {skipped_count}"
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.set_status("Student import failed.")

    def download_students_template_csv(self):
        import csv

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile="students_template.csv"
        )

        if not file_path:
            return

        try:
            with open(file_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)

                writer.writerow([
                    "First Name",
                    "Last Name",
                    "Age",
                    "Gender",
                    "Email",
                    "Payment Status",
                    "Payment Method",
                    "Notes"
                ])

            self.set_status("Student template CSV created.")

            messagebox.showinfo(
                "Template Created",
                "Student CSV template created successfully."
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.set_status("Could not create student template.")

    def download_courses_template_csv(self):
        import csv
    
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile="courses_template.csv"
        )
    
        if not file_path:
            return
    
        try:
            with open(file_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
    
                writer.writerow([
                    "Course Name",
                    "Duration"
                ])
    
            self.set_status("Course template CSV created.")
    
            messagebox.showinfo(
                "Template Created",
                "Course CSV template created successfully."
            )
    
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.set_status("Could not create course template.")

    def download_enrollments_template_csv(self):
        import csv

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile="enrollments_template.csv"
        )

        if not file_path:
            return

        try:
            with open(file_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)

                writer.writerow([
                    "Student Email",
                    "Course Name"
                ])

            self.set_status("Enrollment template CSV created.")

            messagebox.showinfo(
                "Template Created",
                "Enrollment CSV template created successfully."
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.set_status("Could not create enrollment template.")

    def import_courses_csv(self):
        import csv
        from models.course import add_course

        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv")]
        )

        if not file_path:
            return

        imported_count = 0
        skipped_count = 0

        try:
            with open(file_path, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    try:
                        add_course(
                            row.get("Course Name", "").strip(),
                            row.get("Duration", "").strip()
                        )

                        imported_count += 1

                    except Exception:
                        skipped_count += 1

            self.show_courses_page()
            self.set_status(f"Imported {imported_count} courses. Skipped {skipped_count}.")

            messagebox.showinfo(
                "Import Complete",
                f"Imported: {imported_count}\nSkipped: {skipped_count}"
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.set_status("Course import failed.")

    def import_enrollments_csv(self):
        import csv
        from models.student import get_student_by_email
        from models.course import get_course_by_name
        from models.enrollment import enroll_student

        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv")]
        )

        if not file_path:
            return

        imported_count = 0
        skipped_count = 0

        try:
            with open(file_path, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    try:
                        student_email = row.get("Student Email", "").strip()
                        course_name = row.get("Course Name", "").strip()

                        student = get_student_by_email(student_email)
                        course = get_course_by_name(course_name)

                        if not student or not course:
                            skipped_count += 1
                            continue

                        student_id = student[0]
                        course_id = course[0]

                        enroll_student(student_id, course_id)
                        imported_count += 1

                    except Exception:
                        skipped_count += 1

            self.show_enrollments_page()
            self.set_status(f"Imported {imported_count} enrollments. Skipped {skipped_count}.")

            messagebox.showinfo(
                "Import Complete",
                f"Imported: {imported_count}\nSkipped: {skipped_count}"
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.set_status("Enrollment import failed.")

    def show_dashboard_page(self):
        from models.student import get_all_students, get_recent_students
        from models.course import get_all_courses, get_recent_courses
        from models.enrollment import get_students_with_courses

        self.clear_content()
        self.set_status("Dashboard overview")

        title = tk.Label(
            self.content,
            text="Dashboard",
            font=FONT_PAGE_TITLE,
            bg=APP_BG,
            fg=TEXT_DARK
        )
        title.pack(anchor="w", padx=PADDING_XL, pady=(PADDING_LARGE, PADDING_SMALL))

        subtitle = tk.Label(
            self.content,
            text="Overview of students, courses, and enrollments",
            font=FONT_NORMAL,
            bg=APP_BG,
            fg="#636e72"
        )
        subtitle.pack(anchor="w", padx=PADDING_XL, pady=(0, PADDING_LARGE))

        students = len(get_all_students())
        courses = len(get_all_courses())
        enrollments = len(get_students_with_courses())

        cards_frame = tk.Frame(self.content, bg=APP_BG)
        cards_frame.pack(fill="x", padx=PADDING_XL)

        def create_card(parent, label, value):
            card = tk.Frame(parent, bg=CARD_BG, bd=1, relief="solid")
            card.pack(side="left", fill="x", expand=True, padx=5)

            tk.Label(
                card,
                text=label,
                font=FONT_NORMAL,
                bg=CARD_BG,
                fg="#636e72"
            ).pack(anchor="w", padx=15, pady=(12, 4))

            tk.Label(
                card,
                text=value,
                font=("Arial", 24, "bold"),
                bg=CARD_BG,
                fg=TEXT_DARK
            ).pack(anchor="w", padx=15, pady=(0, 15))

        create_card(cards_frame, "Total Students", students)
        create_card(cards_frame, "Total Courses", courses)
        create_card(cards_frame, "Total Enrollments", enrollments)

        recent_frame = tk.Frame(self.content, bg=APP_BG)
        recent_frame.pack(fill="both", expand=True, padx=PADDING_XL, pady=PADDING_LARGE)

        # --- Recent Students ---
        students_card = tk.Frame(recent_frame, bg=CARD_BG, bd=1, relief="solid")
        students_card.pack(side="left", fill="both", expand=True, padx=(0, PADDING_SMALL))

        tk.Label(
            students_card,
            text="Recent Students",
            font=FONT_NORMAL,
            bg=CARD_BG,
            fg=TEXT_DARK
        ).pack(anchor="w", padx=15, pady=10)

        recent_students_tree = ttk.Treeview(
            students_card,
            columns=("ID", "Name", "Email"),
            show="headings",
            height=6
        )

        recent_students_tree.heading("ID", text="ID")
        recent_students_tree.heading("Name", text="Name")
        recent_students_tree.heading("Email", text="Email")

        recent_students_tree.column("ID", width=40, anchor="center")
        recent_students_tree.column("Name", width=160)
        recent_students_tree.column("Email", width=220)

        recent_students_tree.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        def open_student_from_dashboard(event):
            selected = recent_students_tree.selection()
            if not selected:
                return

            item = recent_students_tree.item(selected)
            student_id = item["values"][0]

            from ui.student_profile_ui import StudentProfileWindow
            StudentProfileWindow(self.root, student_id, self.show_dashboard_page)

        recent_students_tree.bind("<Double-1>", open_student_from_dashboard)

        for s in get_recent_students():
            full_name = f"{s[1]} {s[2]}"
            recent_students_tree.insert("", "end", values=(s[0], full_name, s[3]))


        # --- Recent Courses ---
        courses_card = tk.Frame(recent_frame, bg=CARD_BG, bd=1, relief="solid")
        courses_card.pack(side="left", fill="both", expand=True, padx=(PADDING_SMALL, 0))

        tk.Label(
            courses_card,
            text="Recent Courses",
            font=FONT_NORMAL,
            bg=CARD_BG,
            fg=TEXT_DARK
        ).pack(anchor="w", padx=15, pady=10)

        recent_courses_tree = ttk.Treeview(
            courses_card,
            columns=("ID", "Course", "Duration"),
            show="headings",
            height=6
        )

        recent_courses_tree.heading("ID", text="ID")
        recent_courses_tree.heading("Course", text="Course")
        recent_courses_tree.heading("Duration", text="Duration")

        recent_courses_tree.column("ID", width=40, anchor="center")
        recent_courses_tree.column("Course", width=180)
        recent_courses_tree.column("Duration", width=120)

        recent_courses_tree.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        def open_course_from_dashboard(event):
            selected = recent_courses_tree.selection()
            if not selected:
                return

            item = recent_courses_tree.item(selected)
            course_id = item["values"][0]

            from ui.course_profile_ui import CourseProfileWindow
            CourseProfileWindow(self.root, course_id, self.show_dashboard_page)

        recent_courses_tree.bind("<Double-1>", open_course_from_dashboard)

        for c in get_recent_courses():
            recent_courses_tree.insert("", "end", values=(c[0], c[1], c[2]))

        self.apply_theme()

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        self.settings["dark_mode"] = self.dark_mode
        self.apply_theme()

    def apply_theme(self):
        style = ttk.Style()
        style.theme_use("clam")

        if self.dark_mode:
            theme_bg = "#2d3436"
            theme_fg = "#ecf0f1"
            theme_card = "#353b48"
            tree_bg = "#353b48"
            tree_heading_bg = "#2c3e50"
            selected_bg = "#0984e3"
        else:
            theme_bg = APP_BG
            theme_fg = TEXT_DARK
            theme_card = CARD_BG
            tree_bg = "#f5f6fa"
            tree_heading_bg = "#f0f0f0"
            selected_bg = "#74b9ff"

        self.content.config(bg=theme_bg)
        self.right_area.config(bg=theme_bg)

        style.configure(
            "Treeview",
            background=tree_bg,
            foreground=theme_fg,
            fieldbackground=tree_bg,
            rowheight=28,
            font=FONT_NORMAL
        )

        style.configure(
            "Treeview.Heading",
            background=tree_heading_bg,
            foreground=theme_fg,
            font=("Arial", 11, "bold")
        )

        style.map(
            "Treeview",
            background=[("selected", selected_bg)],
            foreground=[("selected", "white")]
        )

        def update_children(widget):
            for child in widget.winfo_children():
                try:
                    if isinstance(child, tk.Frame):
                        if child.cget("bg") in ("white", CARD_BG, "#353b48"):
                            child.config(bg=theme_card)
                        else:
                            child.config(bg=theme_bg)

                    elif isinstance(child, tk.Label):
                        if child.cget("bg") in ("white", CARD_BG, "#353b48"):
                            child.config(bg=theme_card, fg=theme_fg)
                        else:
                            child.config(bg=theme_bg, fg=theme_fg)

                except:
                    pass

                update_children(child)

        update_children(self.content)

    def auto_backup(self):
        import shutil
        import os
        from datetime import datetime

        source_path = "data/cbm.db"

        if not os.path.exists(source_path):
            return

        os.makedirs("backups", exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_path = f"backups/cbm_auto_{timestamp}.db"

        try:
            shutil.copy2(source_path, backup_path)
        except:
            pass

    def on_close(self):
        is_maximized = self.root.state() == "zoomed"

        self.settings["dark_mode"] = self.dark_mode
        self.settings["maximized"] = is_maximized

        if not is_maximized:
            self.settings["window_geometry"] = self.root.geometry()

        save_settings(self.settings)
        self.root.destroy()

    def open_settings_window(self):
        window = tk.Toplevel(self.root)
        window.title("Settings")
        window.geometry("420x450")
        window.resizable(False, False)

        card = tk.Frame(window, bg=CARD_BG, bd=1, relief="solid")
        card.pack(fill="both", expand=True, padx=20, pady=20)

        title = tk.Label(
            card,
            text="Settings",
            font=FONT_PAGE_TITLE,
            bg=CARD_BG,
            fg=TEXT_DARK
        )
        title.pack(anchor="w", padx=15, pady=(15, 5))

        # Dark Mode
        self.dark_mode_var = tk.BooleanVar(value=self.dark_mode)

        dark_mode_check = ttk.Checkbutton(
            card,
            text="Enable dark mode",
            variable=self.dark_mode_var
        )
        dark_mode_check.pack(anchor="w", padx=15, pady=10)

        # Font Style
        tk.Label(card, text="Font Style", font=FONT_NORMAL, bg=CARD_BG).pack(anchor="w", padx=15)

        self.font_family_var = tk.StringVar(value=self.settings.get("font_family", "Arial"))

        font_dropdown = ttk.Combobox(
            card,
            textvariable=self.font_family_var,
            values=["Arial", "Verdana", "Calibri", "Tahoma", "Segoe UI"],
            state="readonly"
        )
        font_dropdown.pack(anchor="w", padx=15, pady=(0, 10))

        # Font Size
        tk.Label(card, text="Font Size", font=FONT_NORMAL, bg=CARD_BG).pack(anchor="w", padx=15)

        self.font_size_var = tk.StringVar(value=str(self.settings.get("font_size", 11)))

        font_size_dropdown = ttk.Combobox(
            card,
            textvariable=self.font_size_var,
            values=["10", "11", "12", "13", "14", "16"],
            state="readonly"
        )
        font_size_dropdown.pack(anchor="w", padx=15, pady=(0, 10))

        # Default Start Page
        tk.Label(card, text="Default Start Page", font=FONT_NORMAL, bg=CARD_BG).pack(anchor="w", padx=15)

        self.start_page_var = tk.StringVar(value=self.settings.get("default_start_page", "Dashboard"))

        start_page_dropdown = ttk.Combobox(
            card,
            textvariable=self.start_page_var,
            values=["Dashboard", "Students", "Courses", "Enrollments", "Payments"],
            state="readonly"
        )
        start_page_dropdown.pack(anchor="w", padx=15, pady=(0, 10))

        # Auto Backup
        self.auto_backup_var = tk.BooleanVar(value=self.settings.get("auto_backup", True))

        auto_backup_check = ttk.Checkbutton(
            card,
            text="Enable auto-backup on startup",
            variable=self.auto_backup_var
        )
        auto_backup_check.pack(anchor="w", padx=15, pady=10)

        save_btn = tk.Button(
            card,
            text="Save Settings",
            command=lambda: self.save_app_settings(window),
            bg=SIDEBAR_ACTIVE_BG,
            fg="white",
            font=FONT_BUTTON,
            relief="flat",
            padx=12,
            pady=6
        )
        save_btn.pack(anchor="w", padx=15, pady=(10, 15))

        apply_popup_theme(window, self.dark_mode)

    def save_app_settings(self, settings_window=None):
        self.settings["font_family"] = self.font_family_var.get()
        self.settings["font_size"] = int(self.font_size_var.get())
        self.settings["default_start_page"] = self.start_page_var.get()
        self.settings["auto_backup"] = self.auto_backup_var.get()
        self.settings["dark_mode"] = self.dark_mode_var.get()

        self.dark_mode = self.dark_mode_var.get()

        save_settings(self.settings)
        self.apply_theme()

        self.set_status("Settings saved.")

        if settings_window:
            settings_window.destroy()

    def open_default_start_page(self):
        start_page = self.settings.get("default_start_page", "Dashboard")

        if start_page == "Students":
            self.set_active_page(self.students_btn, self.show_students_page)
        elif start_page == "Courses":
            self.set_active_page(self.courses_btn, self.show_courses_page)
        elif start_page == "Enrollments":
            self.set_active_page(self.enrollments_btn, self.show_enrollments_page)
        elif start_page == "Payments":
            self.set_active_page(self.payments_btn, self.show_payments_page)
        else:
            self.set_active_page(self.dashboard_btn, self.show_dashboard_page)

    def toggle_dark_mode_from_settings(self):
        self.dark_mode = self.dark_mode_var.get()
        self.settings["dark_mode"] = self.dark_mode
        save_settings(self.settings)
        self.apply_theme()
        self.set_status("Dark mode updated.")

    def run(self):
        self.root.mainloop()