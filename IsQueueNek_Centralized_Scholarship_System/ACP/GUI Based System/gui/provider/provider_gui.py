import tkinter as tk
from tkinter import messagebox
from config import PROVIDER_DB_PATH, STUDENT_DB_PATH
from database import load_db, save_db
from utils.id_generator import generate_provider_id, generate_scholarship_id
from utils.security import hash_input, verify_input


class ProviderLogin(tk.Frame):
    """Handles the login interface and authentication for scholarship providers."""

    def __init__(self, parent):
        super().__init__(parent, bg="#f8fafc")
        self.parent = parent
        self.pack(fill="both", expand=True)

        self.create_card(
            self,
            "Provider Login",
            "Enter your credentials to continue",
            "Provider ID",
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
        """Builds the UI elements for the login card."""
        # Main card container
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

        # Provider ID
        tk.Label(card, text=subhead1, font=("Segoe UI", 9, "bold"), bg="white").pack(
            anchor="w"
        )
        self.provider_id_entry = tk.Entry(
            card,
            font=("Segoe UI", 9),
            bg="white",
            highlightbackground="lightgray",
            highlightthickness=1,
            relief="flat",
        )
        self.provider_id_entry.pack(fill="x", ipadx=70, ipady=5, pady=(0, 15))

        # Password
        tk.Label(card, text=subhead2, font=("Segoe UI", 9, "bold"), bg="white").pack(
            anchor="w"
        )
        self.password = tk.Entry(
            card,
            font=("Segoe UI", 9),
            bg="white",
            highlightbackground="lightgray",
            highlightthickness=1,
            relief="flat",
            show="•",
        )
        self.password.pack(fill="x", ipadx=70, ipady=5, pady=(0, 15))

        # Sign In Button
        tk.Button(
            card,
            text=subhead3,
            font=("Segoe UI", 10, "bold"),
            bg="#2563eb",
            fg="white",
            relief="flat",
            command=cmd1,
        ).pack(fill="x", ipadx=70, ipady=5, pady=(0, 15))

        # Navigation Links
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
        """Authenticates the provider and checks account status."""
        provider_id = self.provider_id_entry.get()
        password = self.password.get()
        providers_db = load_db(PROVIDER_DB_PATH)
        provider = providers_db.get(provider_id)

        # Validate credentials
        if not provider or not verify_input(provider["password"], password):
            messagebox.showerror("Login Failed", "Invalid username or password.")
            return

        # Check account approval status
        if provider["status"] == "pending":
            messagebox.showerror(
                "Access Denied",
                "Your account is still waiting for Admin approval. Please try again later.",
            )
        elif provider["status"] == "rejected":
            messagebox.showerror(
                "Access Denied",
                "Your account has been rejected. Contact admin if needed.",
            )
        elif provider["status"] == "approved":
            self.destroy()
            ProviderDashboard(self.parent, provider_id)

    def register(self):
        self.destroy()
        RegisterNewProfile(self.parent)

    def back_to_main_menu(self):
        self.parent.show_main_menu()


class RegisterNewProfile(tk.Frame):
    """Handles the creation of a new provider account."""

    def __init__(self, parent):
        super().__init__(parent, bg="#f8fafc")
        self.parent = parent
        self.pack(fill="both", expand=True)
        self.create_card(self)

    def create_card(self, parent):
        """Builds the registration form UI."""
        card = tk.Frame(
            parent,
            bg="white",
            highlightthickness=1,
            highlightbackground="lightgrey",
            relief="flat",
            padx=20,
            pady=20,
        )
        card.config(width=500, height=450)
        card.pack_propagate(False)
        card.pack(expand=True)

        tk.Label(
            card,
            text="Provider Registration",
            font=("Segoe UI", 13, "bold"),
            bg="white",
        ).pack(anchor="w")
        tk.Label(
            card,
            text="Create an account to start offering scholarships.",
            font=("Segoe UI", 10),
            bg="white",
            fg="#64748b",
        ).pack(anchor="w", pady=(0, 5))
        tk.Frame(card, bg="#e5e7eb", height=1).pack(fill="x", pady=(0, 15))

        # Organization Name
        tk.Label(
            card, text="Organization Name", font=("Segoe UI", 10, "bold"), bg="white"
        ).pack(anchor="w")
        self.org_name = tk.Entry(
            card,
            font=("Segoe UI", 10),
            bg="white",
            highlightthickness=1,
            highlightbackground="lightgray",
            relief="flat",
        )
        self.org_name.pack(fill="x", ipady=5, padx=(5, 0), pady=(0, 10))

        # Email & Contact (Grid Layout)
        subcard = tk.Frame(card, bg="white")
        subcard.columnconfigure((0, 1), weight=1)
        subcard.pack(fill="x")

        tk.Label(subcard, text="Email", font=("Segoe UI", 10, "bold"), bg="white").grid(
            row=0, column=0, sticky="w", padx=(0, 10)
        )
        tk.Label(
            subcard, text="Contact Number", font=("Segoe UI", 10, "bold"), bg="white"
        ).grid(row=0, column=1, sticky="w")

        self.email = tk.Entry(
            subcard,
            font=("Segoe UI", 10),
            bg="white",
            highlightthickness=1,
            highlightbackground="lightgray",
            relief="flat",
        )
        self.email.grid(
            row=1, column=0, sticky="ew", ipady=5, padx=(5, 10), pady=(0, 10)
        )

        self.contact_number = tk.Entry(
            subcard,
            font=("Segoe UI", 10),
            highlightthickness=1,
            highlightbackground="lightgrey",
            bg="white",
            relief="flat",
        )
        self.contact_number.grid(
            row=1, column=1, sticky="ew", ipady=5, padx=(5, 0), pady=(0, 10)
        )

        # Office Address
        tk.Label(
            card, text="Office Address", font=("Segoe UI", 10, "bold"), bg="white"
        ).pack(anchor="w")
        self.office_address = tk.Entry(
            card,
            font=("Segoe UI", 10),
            bg="white",
            highlightthickness=1,
            highlightbackground="lightgray",
            relief="flat",
        )
        self.office_address.pack(fill="x", ipady=5, padx=(5, 0), pady=(0, 10))

        # Password
        tk.Label(card, text="Password", font=("Segoe UI", 10, "bold"), bg="white").pack(
            anchor="w"
        )
        self.password = tk.Entry(
            card,
            font=("Segoe UI", 10),
            bg="white",
            highlightthickness=1,
            highlightbackground="lightgray",
            relief="flat",
        )
        self.password.pack(fill="x", ipady=5, padx=(5, 0), pady=(0, 10))

        # Buttons
        tk.Button(
            card,
            text="Submit Registration",
            font=("Segoe UI", 10, "bold"),
            bg="darkgreen",
            fg="white",
            relief="flat",
            command=self.submit_registration,
        ).pack(fill="x", ipadx=70, ipady=3, pady=(0, 15))

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

    def submit_registration(self):
        """Hashes the password and saves the new provider profile to the database."""
        providers_db = load_db(PROVIDER_DB_PATH)
        prov_id = generate_provider_id(providers_db)

        providers_db[prov_id] = {
            "organization_name": self.org_name.get(),
            "email": self.email.get(),
            "contact_number": self.contact_number.get(),
            "office_address": self.office_address.get(),
            "scholarship_provider_id": prov_id,
            "password": hash_input(self.password.get()),  # Securely hash password
            "status": "pending",
        }

        save_db(providers_db, PROVIDER_DB_PATH)

        messagebox.showinfo(
            "Registration Successful",
            f"Your Provider ID is: {prov_id}.\n\n"
            "Please don't forget your ID as you will use it to login.\n\n"
            "Note: Your account is currently PENDING. "
            "You must wait for Admin approval before logging in.",
        )

        self.destroy()
        ProviderLogin(self.parent)

    def back_to_login(self):
        self.destroy()
        ProviderLogin(self.parent)


class ProviderDashboard(tk.Frame):
    """Main navigation hub for an authenticated provider."""

    def __init__(self, parent, provider_id):
        super().__init__(parent, bg="#f8fafc")
        self.parent = parent
        self.provider_id = provider_id
        self.pack(fill="both", expand=True)
        self.create_card(self)

    def create_card(self, parent):
        """Builds the dashboard menu UI."""
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
            card,
            text="SCHOLARSHIP PROVIDER DASHBOARD",
            font=("Sogoe UI", 12, "bold"),
            bg="white",
        ).pack(expand=True)
        tk.Frame(card, bg="lightgrey", height=1).pack(
            fill="x", pady=(0, 15), expand=True
        )

        tk.Button(
            card,
            text="Create Scholarship",
            font=("Sogoe UI", 9, "bold"),
            bg="#2563eb",
            fg="white",
            relief="flat",
            command=self.create_scholarship,
        ).pack(fill="x", ipadx=70, ipady=3, pady=(0, 15))
        tk.Button(
            card,
            text="View and Assess Applicants",
            font=("Sogoe UI", 9, "bold"),
            bg="#2563eb",
            fg="white",
            relief="flat",
            command=self.view_and_assess_applicants,
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

    def create_scholarship(self):
        self.destroy()
        CreateNewScholarship(self.parent, self.provider_id)

    def view_and_assess_applicants(self):
        self.destroy()
        ViewAndAssessApplicants(self.parent, self.provider_id)

    def back_to_login(self):
        self.destroy()
        ProviderLogin(self.parent)


class CreateNewScholarship(tk.Frame):
    """Interface for providers to post a new scholarship program."""

    def __init__(self, parent, provider_id):
        super().__init__(parent, bg="#f8fafc")
        self.parent = parent
        self.provider_id = provider_id
        self.pack(fill="both", expand=True)
        self.create_card(self)

    def create_card(self, parent):
        """Builds the scholarship creation form."""
        card = tk.Frame(
            parent,
            bg="white",
            highlightthickness=1,
            highlightbackground="lightgrey",
            relief="flat",
            padx=20,
            pady=20,
        )
        card.config(width=500, height=460)
        card.pack_propagate(False)
        card.pack(expand=True)

        tk.Label(
            card, text="Create Scholarship", font=("Segoe UI", 13, "bold"), bg="white"
        ).pack(anchor="w", pady=(0, 2))
        tk.Frame(card, bg="#e5e7eb", height=1).pack(fill="x", pady=(0, 15))

        # Basic Info
        tk.Label(
            card, text="Scholarship Name", font=("Segoe UI", 10, "bold"), bg="white"
        ).pack(anchor="w")
        self.scholarship_name = tk.Entry(
            card,
            font=("Segoe UI", 10),
            bg="white",
            highlightthickness=1,
            highlightbackground="lightgrey",
            relief="flat",
        )
        self.scholarship_name.pack(fill="x", ipady=5, padx=(5, 0), pady=(0, 5))

        tk.Label(
            card, text="Short Description", font=("Segoe UI", 10, "bold"), bg="white"
        ).pack(anchor="w")
        self.short_description = tk.Entry(
            card,
            font=("Segoe UI", 10),
            bg="white",
            highlightthickness=1,
            highlightbackground="lightgrey",
            relief="flat",
        )
        self.short_description.pack(fill="x", ipady=5, padx=(5, 0), pady=(0, 5))

        # Requirements and Details (Grid Layout)
        subcard = tk.Frame(card, bg="white")
        subcard.columnconfigure((0, 1), weight=1)
        subcard.pack(fill="x")

        # Row 1: Location & Deadline
        tk.Label(
            subcard,
            text='Location (or "Any")',
            font=("Segoe UI", 10, "bold"),
            bg="white",
        ).grid(row=0, column=0, sticky="w")
        self.location = tk.Entry(
            subcard,
            font=("Segoe UI", 10),
            bg="white",
            highlightthickness=1,
            highlightbackground="lightgrey",
            relief="flat",
        )
        self.location.grid(
            row=1, column=0, sticky="ew", ipady=5, padx=(5, 0), pady=(0, 5)
        )

        tk.Label(
            subcard,
            text="Deadline (yyyy-mm-dd)",
            font=("Segoe UI", 10, "bold"),
            bg="white",
        ).grid(row=0, column=1, sticky="w")
        self.deadline = tk.Entry(
            subcard,
            font=("Segoe UI", 10),
            bg="white",
            highlightthickness=1,
            highlightbackground="lightgrey",
            relief="flat",
        )
        self.deadline.grid(
            row=1, column=1, sticky="ew", ipady=5, padx=(5, 0), pady=(0, 5)
        )

        # Row 2: GWA & Income
        tk.Label(
            subcard, text="Min GWA Required", font=("Segoe UI", 10, "bold"), bg="white"
        ).grid(row=2, column=0, sticky="w")
        self.min_gwa = tk.Entry(
            subcard,
            font=("Segoe UI", 10),
            bg="white",
            highlightthickness=1,
            highlightbackground="lightgrey",
            relief="flat",
        )
        self.min_gwa.grid(
            row=3, column=0, sticky="ew", ipady=5, padx=(5, 0), pady=(0, 5)
        )

        tk.Label(
            subcard, text="Max Income(PHP)", font=("Segoe UI", 10, "bold"), bg="white"
        ).grid(row=2, column=1, sticky="w")
        self.max_income = tk.Entry(
            subcard,
            font=("Segoe UI", 10),
            bg="white",
            highlightthickness=1,
            highlightbackground="lightgrey",
            relief="flat",
        )
        self.max_income.grid(
            row=3, column=1, sticky="ew", ipady=5, padx=(5, 0), pady=(0, 5)
        )

        # Row 3: Grant & Slots
        tk.Label(
            subcard, text="Grant Amount(PHP)", font=("Segoe UI", 10, "bold"), bg="white"
        ).grid(row=4, column=0, sticky="w")
        self.grant_amount = tk.Entry(
            subcard,
            font=("Segoe UI", 10),
            bg="white",
            highlightthickness=1,
            highlightbackground="lightgrey",
            relief="flat",
        )
        self.grant_amount.grid(
            row=5, column=0, sticky="ew", ipady=5, padx=(5, 0), pady=(0, 5)
        )

        tk.Label(
            subcard, text="Total Slots", font=("Segoe UI", 10, "bold"), bg="white"
        ).grid(row=4, column=1, sticky="w")
        self.slots = tk.Entry(
            subcard,
            font=("Segoe UI", 10),
            bg="white",
            highlightthickness=1,
            highlightbackground="lightgrey",
            relief="flat",
        )
        self.slots.grid(row=5, column=1, sticky="ew", ipady=5, padx=(5, 0), pady=(0, 5))

        # Buttons
        tk.Button(
            card,
            text="Post Scholarship",
            font=("Segoe UI", 10, "bold"),
            bg="darkgreen",
            fg="white",
            relief="flat",
            command=self.post_scholarship,
        ).pack(fill="x", ipadx=70, ipady=3, pady=(5, 5))

        back_login = tk.Label(
            card,
            text="Cancel & Back to Login",
            font=("Segoe UI Light", 10),
            bg="white",
            fg="darkgrey",
            cursor="hand2",
        )
        back_login.pack()
        back_login.bind("<Button-1>", lambda e: self.back_to_dashboard())

    def post_scholarship(self):
        """Compiles scholarship data and saves it under the provider's database record."""
        providers_db = load_db(PROVIDER_DB_PATH)
        provider_data = providers_db[self.provider_id]

        scholarship_info = {
            "scholarship_name": self.scholarship_name.get(),
            "description": self.short_description.get(),
            "location": self.location.get(),
            "min_gwa": self.min_gwa.get(),
            "max_income": self.max_income.get(),
            "grant_amount": self.grant_amount.get(),
            "slots": self.slots.get(),
            "deadline": self.deadline.get(),
        }

        # Initialize scholarships dictionary if it doesn't exist
        if "scholarships" not in provider_data:
            provider_data["scholarships"] = {}

        scholarship_id = generate_scholarship_id(provider_data)
        provider_data["scholarships"][scholarship_id] = scholarship_info

        save_db(providers_db, PROVIDER_DB_PATH)

        self.destroy()
        ProviderDashboard(self.parent, self.provider_id)

    def back_to_dashboard(self):
        self.destroy()
        ProviderDashboard(self.parent, self.provider_id)


class ViewAndAssessApplicants(tk.Frame):
    """Sub-menu for a provider to navigate between pending and approved applicants."""

    def __init__(self, parent, provider_id):
        super().__init__(parent, bg="#f8fafc")
        self.parent = parent
        self.provider_id = provider_id
        self.pack(fill="both", expand=True)
        self.create_card(self)

    def create_card(self, parent):
        card = tk.Frame(
            parent,
            bg="white",
            highlightthickness=1,
            highlightbackground="lightgrey",
            padx=20,
            pady=20,
        )
        card.config(width=400, height=200)
        card.pack_propagate(False)
        card.pack(expand=True)

        tk.Label(
            card,
            text="SCHOLARSHIP APPLICANTS",
            font=("Segoe UI", 12, "bold"),
            bg="white",
        ).pack(expand=True)
        tk.Frame(card, bg="lightgrey", height=1).pack(
            fill="x", pady=(0, 15), expand=True
        )

        tk.Button(
            card,
            text="View Approved Applicants",
            font=("Segoe UI", 9, "bold"),
            bg="#2563eb",
            fg="white",
            relief="flat",
            command=self.view_approved_applicants,
        ).pack(fill="x", ipadx=70, ipady=3, pady=(0, 15))
        tk.Button(
            card,
            text="Assess New Applicants",
            font=("Segoe UI", 9, "bold"),
            bg="#2563eb",
            fg="white",
            relief="flat",
            command=self.evaluate_new_applicants,
        ).pack(fill="x", ipady=5, pady=(0, 15))

        back_to_dashboard = tk.Label(
            card,
            text="Back to Dashboard",
            font=("Segoe UI Light", 9),
            bg="white",
            fg="darkgrey",
            cursor="hand2",
        )
        back_to_dashboard.pack()
        back_to_dashboard.bind(
            "<Button-1>", lambda e: self.back_to_provider_dashboard()
        )

    def view_approved_applicants(self):
        self.destroy()
        ViewApprovedApplicants(self.parent, self.provider_id)

    def evaluate_new_applicants(self):
        self.destroy()
        EvaluateNewApplicants(self.parent, self.provider_id)

    def back_to_provider_dashboard(self):
        self.destroy()
        ProviderDashboard(self.parent, self.provider_id)


class ViewApprovedApplicants(tk.Frame):
    """Displays a list of all applicants who have been approved by the provider."""

    def __init__(self, parent, provider_id):
        super().__init__(parent, bg="#f8fafc")
        self.parent = parent
        self.student_id = provider_id
        self.pack(fill="both", expand=True)

        # Header UI
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
            text="Approved Applicants",
            font=("Segoe UI", 16, "bold"),
            bg="white",
        ).pack(side="left", padx=20, pady=20)

        return_to_dashboard = tk.Label(
            header_frame,
            text="Return to Provider Dashboard",
            font=("Segoe UI Semibold", 10, "underline"),
            bg="white",
            cursor="hand2",
        )
        return_to_dashboard.pack(side="right", padx=20, pady=20)
        return_to_dashboard.bind(
            "<Button-1>", lambda e: self.return_dashboard(provider_id)
        )

        self.create_card(self, provider_id)

    def create_card(self, parent, provider_id):
        """Iterates through the database to fetch and display 'approved' applications."""
        students_db = load_db(STUDENT_DB_PATH)
        providers_db = load_db(PROVIDER_DB_PATH)
        scholarships = providers_db[provider_id].get("scholarships", {})

        for schl_id, schl_data in scholarships.items():
            for student_id, status in schl_data.get("applicants", {}).items():
                if status == "approved":
                    # Fetch student info
                    student_data = students_db[student_id]
                    student_name = student_data["name"]
                    student_age = student_data["age"]
                    student_gwa = student_data["gwa"]
                    student_annual_income = student_data["annual_family_income"]
                    student_address = student_data["address"]
                    scholarship_name = scholarships[schl_id]["scholarship_name"]

                    # Build individual applicant card
                    card = tk.Frame(
                        parent,
                        bg="white",
                        highlightthickness=1,
                        highlightbackground="lightgrey",
                        relief="flat",
                    )
                    card.pack(fill="x", padx=20, pady=10, ipadx=5)

                    text_container = tk.Frame(card, bg="white")
                    text_container.grid(row=0, column=0, sticky="w", padx=(5, 0))

                    tk.Label(
                        text_container,
                        text=student_name,
                        font=("Segoe UI", 14, "bold"),
                        bg="white",
                        justify="left",
                    ).pack(anchor="w")
                    tk.Label(
                        text_container,
                        text=f"Applied to: {scholarship_name} | ID: {schl_id}",
                        font=("Segoe UI", 9),
                        bg="white",
                        fg="darkgrey",
                        justify="left",
                    ).pack(anchor="w")

                    sub_text = f"ID: {student_id} | Age: {student_age}\nGWA: {student_gwa} | Annual Family Income: {student_annual_income}\nAddress: {student_address}"
                    tk.Label(
                        text_container,
                        text=sub_text,
                        font=("Segoe UI", 9),
                        bg="white",
                        fg="darkgrey",
                        justify="left",
                    ).pack(anchor="w")

                    status_container = tk.Frame(card, bg="white")
                    status_container.config(width=100, height=50)
                    card.pack_propagate(False)
                    status_container.pack(anchor="e", padx=5, expand=True)

                    tk.Label(
                        status_container,
                        text="Approved",
                        font=("Segoe UI", 10, "bold"),
                        width=10,
                        bg="darkgreen",
                        fg="white",
                        relief="flat",
                    ).pack(side="right", padx=10)

    def return_dashboard(self, provider_id):
        self.destroy()
        ProviderDashboard(self.parent, provider_id)


class EvaluateNewApplicants(tk.Frame):
    """Displays pending applicants, allowing the provider to approve or reject them."""

    def __init__(self, parent, provider_id):
        super().__init__(parent, bg="#f8fafc")
        self.parent = parent
        self.student_id = provider_id
        self.pack(fill="both", expand=True)

        # Header UI
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
            text="New Applicants",
            font=("Segoe UI", 16, "bold"),
            bg="white",
        ).pack(side="left", padx=20, pady=20)

        return_to_dashboard = tk.Label(
            header_frame,
            text="Return to Provider Dashboard",
            font=("Segoe UI Semibold", 10, "underline"),
            bg="white",
            cursor="hand2",
        )
        return_to_dashboard.pack(side="right", padx=20, pady=20)
        return_to_dashboard.bind(
            "<Button-1>", lambda e: self.return_dashboard(provider_id)
        )

        self.create_card(self, provider_id)

    def create_card(self, parent, provider_id):
        """Iterates through the database to fetch and display 'pending' applications."""
        students_db = load_db(STUDENT_DB_PATH)
        providers_db = load_db(PROVIDER_DB_PATH)
        scholarships = providers_db[provider_id].get("scholarships", {})

        for schl_id, schl_data in scholarships.items():
            for student_id, status in schl_data.get("applicants", {}).items():
                if status == "pending":
                    # Fetch student info
                    student_data = students_db[student_id]
                    student_name = student_data["name"]
                    student_age = student_data["age"]
                    student_gwa = student_data["gwa"]
                    student_annual_income = student_data["annual_family_income"]
                    student_address = student_data["address"]
                    scholarship_name = scholarships[schl_id]["scholarship_name"]

                    # Build individual applicant card
                    card = tk.Frame(
                        parent,
                        bg="white",
                        highlightthickness=1,
                        highlightbackground="lightgrey",
                        relief="flat",
                    )
                    card.pack(fill="x", padx=20, pady=10, ipadx=5)

                    text_container = tk.Frame(card, bg="white")
                    text_container.grid(row=0, column=0, sticky="w", padx=(5, 0))

                    tk.Label(
                        text_container,
                        text=student_name,
                        font=("Segoe UI", 14, "bold"),
                        bg="white",
                        justify="left",
                    ).pack(anchor="w")
                    tk.Label(
                        text_container,
                        text=f"Applied to: {scholarship_name} | ID: {schl_id}",
                        font=("Segoe UI", 9),
                        bg="white",
                        fg="darkgrey",
                        justify="left",
                    ).pack(anchor="w")

                    sub_text = f"ID: {student_id} | Age: {student_age}\nGWA: {student_gwa} | Annual Family Income: {student_annual_income}\nAddress: {student_address}"
                    tk.Label(
                        text_container,
                        text=sub_text,
                        font=("Segoe UI", 9),
                        bg="white",
                        fg="darkgrey",
                        justify="left",
                    ).pack(anchor="w")

                    # Action buttons
                    buttons_container = tk.Frame(card, bg="white")
                    buttons_container.config(width=100, height=50)
                    card.pack_propagate(False)
                    buttons_container.pack(anchor="e", padx=5, expand=True)

                    reject_bttn = tk.Button(
                        buttons_container,
                        text="Reject",
                        font=("Segoe UI", 10, "bold"),
                        width=10,
                        bg="darkred",
                        fg="white",
                        relief="flat",
                        command=lambda s_id=student_id, sc_id=schl_id, p_id=provider_id, c=card: self.update_status(
                            s_id, sc_id, p_id, c, "rejected"
                        ),
                    )
                    reject_bttn.pack(side="right", padx=10)

                    approve_bttn = tk.Button(
                        buttons_container,
                        text="Approve",
                        font=("Segoe UI", 10, "bold"),
                        width=10,
                        bg="darkgreen",
                        fg="white",
                        relief="flat",
                        command=lambda s_id=student_id, sc_id=schl_id, p_id=provider_id, c=card: self.update_status(
                            s_id, sc_id, p_id, c, "approved"
                        ),
                    )
                    approve_bttn.pack(side="right", padx=10)

    def update_status(self, student_id, schl_id, provider_id, card, status):
        """Updates the application status in both the provider and student databases, then removes the UI card."""
        students_db = load_db(STUDENT_DB_PATH)
        providers_db = load_db(PROVIDER_DB_PATH)

        # Update provider's record
        providers_db[provider_id]["scholarships"][schl_id]["applicants"][
            student_id
        ] = status

        # Update student's record
        students_db[student_id]["applications"][f"{provider_id}_{schl_id}"] = status

        save_db(students_db, STUDENT_DB_PATH)
        save_db(providers_db, PROVIDER_DB_PATH)

        # Remove the evaluated applicant from the current view
        card.destroy()

    def return_dashboard(self, provider_id):
        self.destroy()
        ProviderDashboard(self.parent, provider_id)
