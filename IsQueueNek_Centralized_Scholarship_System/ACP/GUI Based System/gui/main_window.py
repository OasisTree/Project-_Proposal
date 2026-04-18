import tkinter as tk
import os
from gui.admin.admin_gui import AdminLogin
from gui.provider.provider_gui import ProviderLogin
from gui.student.student_gui import StudentLogin


class MainMenu(tk.Tk):
    """Main entry window for role selection (Student, Provider, Admin)."""

    def __init__(self):
        super().__init__()

        self.title("IsQueueNek: Centralized Scholarship Management System")
        self.geometry("900x500")
        self.resizable(False, False)
        self.configure(bg="#f8fafc")

        # Main container
        self.main_frame = tk.Frame(self, bg="#f8fafc")
        self.main_frame.pack(fill="both", expand=True)

        center_frame = tk.Frame(self.main_frame, bg="#f8fafc")
        center_frame.pack(expand=True)

        tk.Label(
            center_frame,
            text="Welcome to IsQueueNek",
            font=("Segoe UI", 25, "bold"),
            bg="#f8fafc",
        ).pack()

        tk.Label(
            center_frame,
            text="Where every deserving student has equal opportunities.",
            font=("Segoe UI", 11),
            bg="#f8fafc",
            fg="darkgrey",
        ).pack(pady=(0, 20))

        cards_frame = tk.Frame(center_frame, bg="#f8fafc")
        cards_frame.pack()
        cards_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Resolve image directory path
        current_file = os.path.dirname(__file__)
        project_root = os.path.dirname(current_file)
        images_dir = os.path.join(project_root, "images")

        # Load icons
        self.student_icon = tk.PhotoImage(
            file=os.path.join(images_dir, "1_student_icon.png")
        ).subsample(6, 6)
        self.provider_icon = tk.PhotoImage(
            file=os.path.join(images_dir, "2_provider_icon.png")
        ).subsample(6, 6)
        self.admin_icon = tk.PhotoImage(
            file=os.path.join(images_dir, "3_admin_icon.png")
        ).subsample(6, 6)

        # Role cards
        self.create_card(
            cards_frame,
            0,
            self.student_icon,
            "Student",
            "Apply for scholarships and track your application status.",
            "Open Student",
            self.open_student,
        )

        self.create_card(
            cards_frame,
            1,
            self.provider_icon,
            "Provider",
            "Post scholarships and assess student applications.",
            "Open Provider",
            self.open_provider,
        )

        self.create_card(
            cards_frame,
            2,
            self.admin_icon,
            "Admin",
            "Manage system access and approve new providers.",
            "Open Administrator",
            self.open_admin,
        )

        # Exit option
        exit_text = tk.Label(
            center_frame,
            text="Exit Program",
            font=("Segoe UI", 10, "underline"),
            bg="#f8fafc",
            fg="darkgrey",
            cursor="hand2",
        )
        exit_text.pack(pady=(20, 0))
        exit_text.bind("<Button-1>", lambda e: self.destroy())

    def create_card(self, parent, column, icon, title, desc, bttn_txt, cmd):
        """Create a role selection card."""
        card = tk.Frame(
            parent,
            bg="white",
            bd=1,
            relief="flat",
            highlightthickness=1,
            highlightbackground="#e5e7eb",
        )
        card.config(width=200, height=300)
        card.grid(row=0, column=column, padx=20)
        card.pack_propagate(False)

        tk.Label(card, image=icon, bg="white").pack(pady=(30, 30))

        tk.Label(card, text=title, font=("Segoe UI", 14, "bold"), bg="white").pack(
            pady=(0, 10)
        )

        tk.Label(
            card,
            text=desc,
            font=("Segoe UI", 9),
            bg="white",
            fg="darkgray",
            wraplength=180,
        ).pack(padx=10, pady=(0, 10))

        tk.Button(
            card,
            text=bttn_txt,
            font=("Segoe UI", 9),
            bg="#2563eb",
            fg="white",
            relief="flat",
            command=cmd,
        ).pack(fill="x", ipady=10, padx=20, pady=(10, 20))

    def open_student(self):
        """Open student login view."""
        self.main_frame.pack_forget()
        StudentLogin(self)

    def open_provider(self):
        """Open provider login view."""
        self.main_frame.pack_forget()
        ProviderLogin(self)

    def open_admin(self):
        """Open admin login view."""
        self.main_frame.pack_forget()
        AdminLogin(self)

    def show_main_menu(self):
        """Return to main menu view."""
        for widget in self.winfo_children():
            if widget != self.main_frame:
                widget.destroy()

        self.main_frame.pack(fill="both", expand=True)
