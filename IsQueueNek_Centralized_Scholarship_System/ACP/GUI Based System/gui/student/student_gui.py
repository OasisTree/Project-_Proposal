import datetime
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from config import PROVIDER_DB_PATH, STUDENT_DB_PATH
from database import load_db, save_db
from utils.id_generator import generate_student_id
from utils.security import hash_input, verify_input
from utils.validator import check_text, check_input


class StudentLogin(tk.Frame):
    """Handles student authentication and the login interface."""

    def __init__(self, parent):
        super().__init__(parent, bg="#f8fafc")
        self.parent = parent
        self.pack(fill="both", expand=True)

        self.create_card(
            self,
            "Student Login",
            "Enter your credentials to continue",
            "Student ID",
            "Password",
            "Sign In",
            "Don't have an account?",
            "Register Here",
            "Back to Main Menu",
            self.sign_in,
            self.register,
            self.back_to_main_menu,
        )

    def create_card(
        self,
        parent,
        title,
        desc,
        subhead1,
        subhead2,
        subhead3,
        subhead4,
        subhead5,
        subhead6,
        cmd1,
        cmd2,
        cmd3,
    ):
        """Constructs the UI layout for the login card."""
        card = tk.Frame(
            parent,
            bg="white",
            highlightthickness=1,
            highlightbackground="#e5e7eb",
            padx=40,
            pady=30,
        )
        card.config(width=350, height=400)
        card.pack_propagate(False)
        card.pack(expand=True)

        tk.Label(card, text=title, font=("Segoe UI", 18, "bold"), bg="white").pack()
        tk.Label(card, text=desc, font=("Segoe UI", 10), bg="white", fg="#64748b").pack(
            pady=(0, 5)
        )
        tk.Frame(card, height=1, bg="#e5e7eb").pack(fill="x", pady=(0, 15))

        tk.Label(card, text=subhead1, font=("Segoe UI", 9, "bold"), bg="white").pack(
            anchor="w"
        )
        self.student_id = tk.Entry(
            card,
            font=("Segoe UI", 9),
            bg="white",
            highlightthickness=1,
            highlightbackground="lightgray",
            relief="flat",
        )
        self.student_id.pack(fill="x", ipadx=70, ipady=5, pady=(0, 15))

        tk.Label(card, text=subhead2, font=("Segoe UI", 9, "bold"), bg="white").pack(
            anchor="w"
        )
        self.password = tk.Entry(
            card,
            font=("Segoe UI", 9),
            bg="white",
            highlightthickness=1,
            highlightbackground="lightgray",
            relief="flat",
            show="•",
        )
        self.password.pack(fill="x", ipadx=70, ipady=5, pady=(0, 15))

        tk.Button(
            card,
            text=subhead3,
            font=("Segoe UI", 10, "bold"),
            bg="#2563eb",
            fg="white",
            cursor="hand2",
            relief="flat",
            command=cmd1,
        ).pack(fill="x", ipadx=70, ipady=5, pady=(0, 15))

        register_frame = tk.Frame(card, bg="white")
        register_frame.pack()
        tk.Label(
            register_frame, text=subhead4, font=("Segoe UI Light", 10), bg="white"
        ).pack(side="left")

        register = tk.Label(
            register_frame,
            text=subhead5,
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#2563eb",
            cursor="hand2",
        )
        register.pack(side="left")
        register.bind("<Button-1>", lambda e: cmd2())

        back_main_menu = tk.Label(
            card,
            text=subhead6,
            font=("Segoe UI", 10),
            bg="white",
            fg="darkgrey",
            cursor="hand2",
        )
        back_main_menu.pack(pady=(15, 0))
        back_main_menu.bind("<Button-1>", lambda e: cmd3())

    def sign_in(self):
        """Verifies student credentials against the database."""
        student_id = self.student_id.get()
        password = self.password.get()
        students_db = load_db(STUDENT_DB_PATH)

        if student_id not in students_db:
            messagebox.showerror("Login Failed", "Invalid username or password.")
            return

        student_data = students_db[student_id]

        if not verify_input(student_data["password"], password):
            messagebox.showerror("Login Failed", "Invalid username or password.")
            return
        else:
            self.destroy()
            StudentDashboard(self.parent, student_id)

    def register(self):
        self.destroy()
        RegisterNewProfile(self.parent)

    def back_to_main_menu(self):
        self.parent.show_main_menu()


class RegisterNewProfile(tk.Frame):
    """Handles the creation of a new student master profile."""

    def __init__(self, parent):
        super().__init__(parent, bg="#f8fafc")
        self.parent = parent
        self.pack(fill="both", expand=True)
        self.create_card(self)

    def create_card(self, parent):
        """Constructs the UI form for student registration."""
        card = tk.Frame(
            parent,
            bg="white",
            highlightthickness=1,
            highlightbackground="lightgrey",
            relief="flat",
            padx=20,
            pady=20,
        )
        card.config(width=550, height=490)
        card.pack_propagate(False)
        card.pack(expand=True)

        tk.Label(
            card,
            text="Student Registration (Master Profile)",
            font=("Segoe UI", 15, "bold"),
            bg="white",
        ).pack(anchor="w")
        tk.Label(
            card,
            text="Enter your details carefully. This Master Profile will automatically check your eligibility for all future scholarships.",
            font=("Segoe UI Light", 10),
            wraplength=500,
            bg="white",
            fg="#64748b",
            justify="left",
        ).pack(anchor="w", pady=(0, 5))
        tk.Frame(card, bg="lightgrey", height=1).pack(fill="x", pady=(0, 5))

        subcard = tk.Frame(card, bg="white")
        subcard.columnconfigure((0, 1), weight=1)
        subcard.pack(fill="x")

        # Basic Info
        tk.Label(
            subcard, text="Full Name", font=("Segoe UI", 10, "bold"), bg="white"
        ).grid(row=0, column=0, sticky="w")
        self.full_name = tk.Entry(
            subcard,
            font=("Segoe UI", 10),
            bg="white",
            highlightthickness=1,
            highlightbackground="lightgrey",
            relief="flat",
        )
        self.full_name.grid(
            row=1, column=0, sticky="ew", ipady=5, padx=(5, 0), pady=(0, 5)
        )

        tk.Label(subcard, text="Age", font=("Segoe UI", 10, "bold"), bg="white").grid(
            row=0, column=1, sticky="w"
        )
        self.age = tk.Entry(
            subcard,
            font=("Segoe UI", 10),
            bg="white",
            highlightthickness=1,
            highlightbackground="lightgrey",
            relief="flat",
        )
        self.age.grid(row=1, column=1, sticky="ew", ipady=5, padx=(5, 0), pady=(0, 5))

        # Academic & Financial Info
        tk.Label(
            subcard,
            text="Annual Family Income (PHP)",
            font=("Segoe UI", 10, "bold"),
            bg="white",
        ).grid(row=2, column=0, sticky="w")
        self.annual_income = tk.Entry(
            subcard,
            font=("Segoe UI", 10),
            bg="white",
            highlightthickness=1,
            highlightbackground="lightgrey",
            relief="flat",
        )
        self.annual_income.grid(
            row=3, column=0, sticky="ew", ipady=5, padx=(5, 0), pady=(0, 5)
        )

        tk.Label(
            subcard, text="GWA (Last Sem)", font=("Segoe UI", 10, "bold"), bg="white"
        ).grid(row=2, column=1, sticky="w")
        self.gwa = tk.Entry(
            subcard,
            font=("Segoe UI", 10),
            bg="white",
            highlightthickness=1,
            highlightbackground="lightgrey",
            relief="flat",
        )
        self.gwa.grid(row=3, column=1, sticky="ew", ipady=5, padx=(5, 0), pady=(0, 5))

        # File Uploads
        tk.Label(
            subcard, text="Proof of Income", font=("Segoe UI", 10, "bold"), bg="white"
        ).grid(row=4, column=0, sticky="w")
        tk.Button(
            subcard,
            text="Upload file",
            font=("Segoe UI", 9),
            bg="white",
            highlightthickness=1,
            highlightbackground="lightgrey",
            cursor="hand2",
            command=lambda: self.upload_file("income"),
        ).grid(row=5, column=0, sticky="ew", padx=(5, 0), pady=(0, 5))

        self.income_file_label = tk.Label(
            subcard,
            text="No file selected",
            font=("Segoe UI", 8),
            bg="white",
            fg="grey",
        )
        self.income_file_label.grid(row=6, column=0, sticky="w", padx=(5, 0))

        tk.Label(
            subcard, text="CTC of Grades", font=("Segoe UI", 10, "bold"), bg="white"
        ).grid(row=4, column=1, sticky="w")
        tk.Button(
            subcard,
            text="Upload file",
            font=("Segoe UI", 9),
            bg="white",
            highlightthickness=1,
            highlightbackground="black",
            cursor="hand2",
            command=lambda: self.upload_file("grades"),
        ).grid(row=5, column=1, sticky="ew", padx=(5, 0), pady=(0, 5))

        self.grades_file_label = tk.Label(
            subcard,
            text="No file selected",
            font=("Segoe UI", 8),
            bg="white",
            fg="grey",
        )
        self.grades_file_label.grid(row=6, column=1, sticky="w", padx=(5, 0))

        # Address & Security
        tk.Label(
            card, text="Complete Address", font=("Segoe UI", 10, "bold"), bg="white"
        ).pack(anchor="w")
        self.address = tk.Entry(
            card,
            font=("Segoe UI", 10),
            bg="white",
            highlightthickness=1,
            highlightbackground="lightgrey",
            relief="flat",
        )
        self.address.pack(fill="x", ipady=5, padx=(5, 0))

        tk.Label(card, text="Password", font=("Segoe UI", 10, "bold"), bg="white").pack(
            anchor="w"
        )
        self.password = tk.Entry(
            card,
            font=("Segoe UI", 10),
            bg="white",
            highlightthickness=1,
            highlightbackground="lightgrey",
            relief="flat",
        )
        self.password.pack(fill="x", ipady=5, padx=(5, 0), pady=(0, 3))

        tk.Button(
            card,
            text="Submit Registration",
            font=("Segoe UI", 10, "bold"),
            bg="darkgreen",
            fg="white",
            relief="flat",
            command=self.register_profile,
        ).pack(fill="x", ipadx=70, ipady=3, pady=(0, 5))

        back_login = tk.Label(
            card,
            text="Cancel & Back to Login",
            font=("Segoe UI Light", 10),
            bg="white",
            fg="darkgrey",
            cursor="hand2",
        )
        back_login.pack()
        back_login.bind("<Button-1>", lambda e: self.back_to_login())

    def upload_file(self, file_type):
        """Opens a file dialog to attach requirement documents."""
        filepath = filedialog.askopenfilename(
            title="Select File",
            filetypes=[
                ("PDF Documents", "*.pdf"),
                ("Image Files", "*.jpg *.jpeg *.png"),
                ("All Files", "*.*"),
            ],
        )

        if filepath:
            filename = os.path.basename(filepath)
            if file_type == "income":
                self.income_filepath = filepath
                self.income_file_label.config(text=f"Uploaded: {filename}", fg="green")
            elif file_type == "grades":
                self.grades_filepath = filepath
                self.grades_file_label.config(text=f"Uploaded: {filename}", fg="green")

    def register_profile(self):
        """Compiles input data, securely hashes the password, and saves the new student profile."""
        students_db = load_db(STUDENT_DB_PATH)
        student_id = generate_student_id(students_db)

        name = check_text(self.full_name.get())
        age = check_input(self.age.get())
        gwa = check_input(self.gwa.get())
        annual_family_income = check_input(self.annual_income.get())
        address = check_text(self.address.get())
        password = check_text(self.password.get())

        if None in (name, age, gwa, annual_family_income, address, password):
            messagebox.showerror("Invalid Input", "Please ensure that the data you input is not empty and valid")
            return

        students_db[student_id] = {
            "name": self.full_name.get(),
            "age": float(self.age.get()),
            "gwa": float(self.gwa.get()),
            "ctc_of_grades": getattr(self, "grades_filepath", None),
            "annual_family_income": float(self.annual_income.get()),
            "proof_of_income": getattr(self, "income_filepath", None),
            "address": self.address.get(),
            "student_id": student_id,
            "password": hash_input(self.password.get()),
        }

        save_db(students_db, STUDENT_DB_PATH)
        messagebox.showinfo(
            "Success",
            f"Profile created!\nYour ID: {student_id}\nPlease don't forget your ID as you will use it to login.",
        )

        self.destroy()
        StudentLogin(self.parent)

    def back_to_login(self):
        self.destroy()
        StudentLogin(self.parent)


class StudentDashboard(tk.Frame):
    """Main navigation hub for an authenticated student."""

    def __init__(self, parent, student_id):
        super().__init__(parent, bg="#f8fafc")
        self.parent = parent
        self.student_id = student_id
        self.pack(fill="both", expand=True)
        self.create_card(self)

    def create_card(self, parent):
        """Constructs the dashboard menu."""
        card = tk.Frame(
            parent,
            bg="white",
            highlightthickness=1,
            highlightbackground="lightgrey",
            padx=40,
            pady=30,
        )
        card.config(width=400, height=250)
        card.pack_propagate(False)
        card.pack(expand=True)

        tk.Label(
            card, text="STUDENT DASHBOARD", font=("Sogoe UI", 12, "bold"), bg="white"
        ).pack(expand=True)
        tk.Frame(card, bg="lightgrey", height=1).pack(
            fill="x", pady=(0, 15), expand=True
        )

        tk.Button(
            card,
            text="View and Apply Scholarship",
            font=("Sogoe UI", 9, "bold"),
            bg="#2563eb",
            fg="white",
            relief="flat",
            command=self.view_and_apply_scholarship,
        ).pack(fill="x", ipadx=70, ipady=3, pady=(0, 15))
        tk.Button(
            card,
            text="View My Profile",
            font=("Sogoe UI", 9, "bold"),
            bg="#2563eb",
            fg="white",
            relief="flat",
            command=self.view_my_profile,
        ).pack(fill="x", ipadx=70, ipady=3, pady=(0, 15))

        back_login = tk.Label(
            card,
            text="Back to Login",
            font=("Segoe UI Light", 9),
            bg="white",
            fg="darkgrey",
            cursor="hand2",
        )
        back_login.pack()
        back_login.bind("<Button-1>", lambda e: self.back_to_login())

    def view_and_apply_scholarship(self):
        self.destroy()
        ViewAndApplyScholarship(self.parent, self.student_id)

    def view_my_profile(self):
        self.destroy()
        ViewMyProfile(self.parent, self.student_id)

    def back_to_login(self):
        self.destroy()
        StudentLogin(self.parent)


class ViewAndApplyScholarship(tk.Frame):
    """Displays scholarships the student is eligible for and handles the application process."""

    def __init__(self, parent, student_id):
        super().__init__(parent, bg="#f8fafc")
        self.parent = parent
        self.student_id = student_id
        self.pack(fill="both", expand=True)

        header_frame = tk.Frame(
            self,
            bg="white",
            highlightthickness=1,
            highlightbackground="darkgrey",
            relief="flat",
        )
        header_frame.pack(fill="x")

        tk.Label(
            header_frame,
            text="Available Scholarships",
            font=("Segoe UI", 16, "bold"),
            bg="white",
        ).pack(side="left", padx=20, pady=20)

        return_to_dashboard = tk.Label(
            header_frame,
            text="Return to Student Dashboard",
            font=("Segoe UI Semibold", 10, "underline"),
            bg="white",
            cursor="hand2",
        )
        return_to_dashboard.pack(side="right", padx=20, pady=20)
        return_to_dashboard.bind(
            "<Button-1>", lambda e: self.return_dashboard(student_id)
        )

        self._filter_and_display_scholarships()

    def _filter_and_display_scholarships(self):
        """Matches student profile against available scholarships based on requirements."""
        students_db = load_db(STUDENT_DB_PATH)
        providers_db = load_db(PROVIDER_DB_PATH)

        student_id = self.student_id
        student_data = students_db[student_id]
        student_gwa = float(student_data["gwa"])
        student_annual_income = float(student_data["annual_family_income"])
        student_address = student_data["address"]

        available_scholarships = {}
        schl_ctr = 1

        # Iterate through all providers and their scholarships
        for provider_id, provider_data in providers_db.items():
            for schl_id, schl_data in provider_data.get("scholarships", {}).items():
                current_date = datetime.date.today()
                schl_deadline_date = datetime.datetime.strptime(
                    schl_data["deadline"], "%Y-%m-%d"
                ).date()

                provider = provider_data["organization_name"]
                schl_location = schl_data["location"]
                schl_max_income = float(schl_data["max_income"])
                schl_min_gwa = float(schl_data["min_gwa"])
                schl_slots_remaining = int(schl_data["slots"])

                # Ensure nested dictionaries exist to prevent KeyErrors
                if "applications" not in students_db[student_id]:
                    students_db[student_id]["applications"] = {}
                if (
                    "applicants"
                    not in providers_db[provider_id]["scholarships"][schl_id]
                ):
                    providers_db[provider_id]["scholarships"][schl_id][
                        "applicants"
                    ] = {}

                # Eligibility logic parameters
                is_prov_approved = provider_data["status"] == "approved"
                not_yet_applied = (
                    f"{provider_id}_{schl_id}"
                    not in students_db[student_id]["applications"]
                    and student_id
                    not in providers_db[provider_id]["scholarships"][schl_id][
                        "applicants"
                    ]
                )
                not_deadline = current_date <= schl_deadline_date
                slots_check = schl_slots_remaining > 0
                qualifies = (
                    student_gwa <= schl_min_gwa
                    and student_annual_income <= schl_max_income
                )
                location_match = (
                    schl_location.lower() == "national"
                    or student_address.lower() in schl_location.lower()
                    or schl_location.lower() in student_address.lower()
                )

                # Filter condition
                if (
                    is_prov_approved
                    and not_deadline
                    and slots_check
                    and qualifies
                    and location_match
                    and not_yet_applied
                ):
                    available_scholarships[str(schl_ctr)] = {
                        "provider_name": provider,
                        "provider_id": provider_id,
                        "schl_id": schl_id,
                        "schl_data": schl_data,
                    }
                    schl_ctr += 1

        # Render UI based on matching results
        if not available_scholarships:
            tk.Label(
                self,
                text="There are no scholarships available for your profile at the moment.",
                font=("Segoe UI", 10),
                bg="#f8fafc",
                fg="darkgrey",
            ).pack(fill="both", expand=True)
        else:
            self.create_card(self, available_scholarships, student_id)

    def create_card(self, parent, available_scholarships, student_id):
        """Constructs the UI for each eligible scholarship found."""
        for number, data in available_scholarships.items():
            card = tk.Frame(
                parent,
                bg="white",
                highlightthickness=1,
                highlightbackground="lightgrey",
                relief="flat",
                padx=20,
                pady=20,
            )
            card.pack(fill="x", padx=20, pady=10, ipadx=5)

            schl_data = data["schl_data"]
            text_container = tk.Frame(card, bg="white")
            text_container.grid(row=0, column=0, sticky="w", padx=(5, 0))

            tk.Label(
                text_container,
                text=schl_data["scholarship_name"],
                font=("Segoe UI", 14, "bold"),
                bg="white",
                justify="left",
            ).pack(anchor="w")
            tk.Label(
                text_container,
                text=data["provider_name"],
                font=("Segoe UI", 9, "bold"),
                bg="white",
                fg="darkgrey",
                justify="left",
            ).pack(anchor="w")

            sub_text = f"ID: {data['schl_id']} | Location: {schl_data['location']}\nMin GWA: {schl_data['min_gwa']} | Max Income: {schl_data['max_income']}\nDue: {schl_data['deadline']} | {schl_data['slots']} slots left"
            tk.Label(
                text_container,
                text=sub_text,
                font=("Segoe UI", 9),
                bg="white",
                fg="darkgrey",
                justify="left",
            ).pack(anchor="w")

            buttons_container = tk.Frame(card, bg="white")
            buttons_container.config(width=100, height=50)
            card.pack_propagate(False)
            buttons_container.pack(anchor="e", padx=5, expand=True)

            apply_bttn = tk.Button(
                buttons_container,
                text="Apply",
                font=("Segoe UI", 10, "bold"),
                width=10,
                bg="darkgreen",
                fg="white",
                relief="flat",
                command=lambda p_id=data["provider_id"], schl_id=data[
                    "schl_id"
                ], s_id=student_id, c=card: self.apply(p_id, schl_id, s_id, c),
            )
            apply_bttn.pack(side="right", padx=10)

    def apply(self, provider_id, schl_id, student_id, card):
        """Registers a pending application in both the student and provider databases."""
        students_db = load_db(STUDENT_DB_PATH)
        providers_db = load_db(PROVIDER_DB_PATH)

        if "applications" not in students_db[student_id]:
            students_db[student_id]["applications"] = {}
        students_db[student_id]["applications"][f"{provider_id}_{schl_id}"] = "pending"

        if "applicants" not in providers_db[provider_id]["scholarships"][schl_id]:
            providers_db[provider_id]["scholarships"][schl_id]["applicants"] = {}

        providers_db[provider_id]["scholarships"][schl_id]["applicants"][
            student_id
        ] = "pending"
        providers_db[provider_id]["scholarships"][schl_id]["slots"] -= 1

        save_db(students_db, STUDENT_DB_PATH)
        save_db(providers_db, PROVIDER_DB_PATH)

        card.destroy()

    def return_dashboard(self, student_id):
        self.destroy()
        StudentDashboard(self.parent, student_id)


class ViewMyProfile(tk.Frame):
    """Displays the student's master profile details and application statuses."""

    def __init__(self, parent, student_id):
        super().__init__(parent, bg="#f8fafc")
        self.parent = parent
        self.student_id = student_id
        self.pack(fill="both", expand=True)

        header_frame = tk.Frame(
            self,
            bg="white",
            highlightthickness=1,
            highlightbackground="darkgrey",
            relief="flat",
        )
        header_frame.pack(fill="x")

        tk.Label(
            header_frame,
            text="My Profile and Applications",
            font=("Segoe UI", 16, "bold"),
            bg="white",
        ).pack(side="left", padx=20, pady=20)

        return_to_dashboard = tk.Label(
            header_frame,
            text="Return to Student Dashboard",
            font=("Segoe UI Semibold", 10, "underline"),
            bg="white",
            cursor="hand2",
        )
        return_to_dashboard.pack(side="right", padx=20, pady=20)
        return_to_dashboard.bind(
            "<Button-1>", lambda e: self.return_dashboard(student_id)
        )

        self.create_card(self, student_id)

    def create_card(self, parent, student_id):
        """Constructs a split-view UI showing profile stats on the left and application history on the right."""
        card_holder = tk.Frame(parent, bg="#f8fafc", relief="flat")
        card_holder.pack_propagate(False)
        card_holder.grid_columnconfigure(0, weight=0)
        card_holder.grid_columnconfigure(1, weight=1)
        card_holder.pack(fill="both", expand=True, padx=40)

        # --- LEFT COLUMN: PROFILE CARD ---
        profile_card = tk.Frame(
            card_holder,
            bg="white",
            highlightthickness=1,
            highlightbackground="#e2e8f0",
            relief="flat",
            padx=20,
            pady=30,
        )
        profile_card.grid(row=0, column=0, sticky="n", pady=20, padx=(0, 20))

        students_db = load_db(STUDENT_DB_PATH)
        name = students_db[student_id]["name"]
        age = students_db[student_id]["age"]
        gwa = students_db[student_id]["gwa"]
        income = students_db[student_id]["annual_family_income"]
        location = students_db[student_id]["address"]

        avatar_frame = tk.Frame(
            profile_card,
            bg="#f1f5f9",
            width=80,
            height=80,
            highlightthickness=1,
            highlightbackground="#e2e8f0",
        )
        avatar_frame.pack(pady=(0, 15))
        avatar_frame.pack_propagate(False)
        tk.Label(
            avatar_frame, text="👤", font=("Segoe UI", 30), bg="#f1f5f9", fg="#94a3b8"
        ).pack(expand=True)

        tk.Label(
            profile_card,
            text=name,
            font=("Segoe UI", 14, "bold"),
            bg="white",
            justify="center",
        ).pack()
        tk.Label(
            profile_card,
            text=f"ID: {student_id}",
            font=("Segoe UI", 9),
            bg="white",
            fg="#64748b",
            justify="center",
        ).pack(pady=(0, 20))

        subcard = tk.Frame(profile_card, bg="white")
        subcard.columnconfigure((0, 1), weight=1)
        subcard.pack(fill="x", expand=True)

        stats = [
            ("Age", age),
            ("GWA", gwa),
            ("Income", f"₱{income}"),
            ("Location", location),
        ]

        for i, (label_text, val_text) in enumerate(stats):
            tk.Label(
                subcard, text=label_text, font=("Segoe UI", 9), bg="white", fg="#64748b"
            ).grid(row=i, column=0, sticky="w", pady=8)
            tk.Label(
                subcard, text=val_text, font=("Segoe UI", 9, "bold"), bg="white"
            ).grid(row=i, column=1, sticky="e", pady=8)

        # --- RIGHT COLUMN: APPLICATIONS ---
        applications_card = tk.Frame(card_holder, bg="#f8fafc", relief="flat")
        applications_card.grid(row=0, column=1, sticky="nsew", pady=20)

        tk.Label(
            applications_card,
            text="My Applications",
            font=("Segoe UI", 12, "bold"),
            bg="#f8fafc",
            justify="left",
        ).pack(anchor="w", pady=(0, 15))

        scholarship_cards = tk.Frame(applications_card, bg="#f8fafc")
        scholarship_cards.pack(fill="both", expand=True)

        # Iterate and render dynamic status cards for each applied scholarship
        for scholarship, status in (
            students_db[student_id].get("applications", {}).items()
        ):
            sub_card = tk.Frame(
                scholarship_cards,
                bg="white",
                highlightthickness=1,
                highlightbackground="#e2e8f0",
                relief="flat",
                padx=20,
                pady=15,
            )
            sub_card.grid_columnconfigure(0, weight=1)
            sub_card.grid_columnconfigure(1, weight=0)
            sub_card.pack(fill="x", pady=(0, 10))

            prov_schl = scholarship.split("_")
            providers_db = load_db(PROVIDER_DB_PATH)
            provider_id = prov_schl[0]
            schl_id = prov_schl[1]
            provider_name = str(providers_db[provider_id]["organization_name"])
            schl_name = str(
                providers_db[provider_id]["scholarships"][schl_id]["scholarship_name"]
            )

            tk.Label(
                sub_card, text=schl_name, font=("Segoe UI", 11, "bold"), bg="white"
            ).grid(row=0, column=0, sticky="w")
            tk.Label(
                sub_card,
                text=provider_name,
                font=("Segoe UI", 9),
                bg="white",
                fg="#64748b",
            ).grid(row=1, column=0, sticky="w", pady=(2, 0))

            is_approved = status.lower() == "approved"
            bg_color = "#dcfce7" if is_approved else "#fef08a"
            fg_color = "#166534" if is_approved else "#854d0e"

            tk.Label(
                sub_card,
                text=status.upper(),
                font=("Segoe UI", 8, "bold"),
                bg=bg_color,
                fg=fg_color,
                padx=10,
                pady=3,
            ).grid(row=0, rowspan=2, column=1, sticky="e")

    def return_dashboard(self, student_id):
        self.destroy()
        StudentDashboard(self.parent, student_id)
