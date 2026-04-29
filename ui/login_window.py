import tkinter as tk
from tkinter import ttk, messagebox
from models.user import verify_login
from ui.main_window import MainWindow


class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CBM Login")
        self.center_window(350, 250)
        self.root.resizable(False, False)

        self.create_widgets()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
    
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
    
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):
        title = ttk.Label(
            self.root,
            text="CBM Login",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=20)

        self.username_entry = self.create_entry("Username")
        self.password_entry = self.create_entry("Password", show="*")

        login_btn = ttk.Button(
            self.root,
            text="Login",
            command=self.login
        )
        login_btn.pack(pady=20)

        self.root.bind("<Return>", lambda event: self.login())

    def create_entry(self, label_text, show=None):
        label = ttk.Label(self.root, text=label_text)
        label.pack(anchor="w", padx=40)

        entry = ttk.Entry(self.root, show=show)
        entry.pack(padx=40, pady=5, fill="x")

        return entry

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        user = verify_login(username, password)

        if user:
            self.root.destroy()

            app = MainWindow()
            app.run()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def run(self):
        self.root.mainloop()