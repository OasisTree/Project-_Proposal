import tkinter as tk
from tkinter import messagebox
from config import ADMIN_DB_PATH, PROVIDER_DB_PATH
from database import load_db, save_db
from utils.security import hash_input, verify_input


class AdminLogin(tk.Frame):
    """Admin login screen."""

    def __init__(self, parent):
        super().__init__(parent, bg="#f8fafc")
        self.parent = parent
        self.pack(fill="both", expand=True)

        self.create_card(
            self,
            "Admin Login",
            "Enter your credentials to continue",
            "Username",
            "Password",
            self.sign_in,
            self.back_to_main_menu,
        )

    def create_card(self, parent, title, desc, subhead1, subhead2, cmd1, cmd2):
        """Build login UI card."""
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

        # Title
        tk.Label(card, text=title, bg="white", font=("Segoe UI", 18, "bold")).pack()

        # Description
        tk.Label(card, text=desc, bg="white", fg="#64748b", font=("Segoe UI", 10)).pack(
            pady=(0, 5)
        )

        # Horizontal divider line
        tk.Frame(card, height=1, bg="#e5e7eb").pack(fill="x", pady=(0, 15))

        # Username label
        tk.Label(card, text=subhead1, bg="white", font=("Segoe UI", 9, "bold")).pack(
            anchor="w"
        )

        # Username input field
        self.username = tk.Entry(
            card,
            font=("Segoe UI", 9),
            bg="white",
            highlightbackground="lightgray",
            highlightthickness=1,
            relief="flat",
        )
        self.username.pack(fill="x", ipady=5, ipadx=70, pady=(0, 15))

        # Password label
        tk.Label(card, text=subhead2, bg="white", font=("Segoe UI", 9, "bold")).pack(
            anchor="w"
        )

        # Password input field
        self.password = tk.Entry(
            card,
            font=("Segoe UI", 9),
            bg="white",
            highlightbackground="lightgrey",
            highlightthickness=1,
            relief="flat",
            show="•",
        )
        self.password.pack(fill="x", ipady=5, ipadx=70, pady=(0, 15))

        # Sign In button
        tk.Button(
            card,
            text="Sign In",
            font=("Segoe UI", 10, "bold"),
            bg="#2563eb",
            fg="white",
            relief="flat",
            command=cmd1,
        ).pack(fill="x", ipady=5, ipadx=70)

        # Back to Main Menu link
        back_main_menu = tk.Label(
            card,
            text="Back to Main Menu",
            font=("Segoe UI", 10),
            bg="white",
            fg="darkgrey",
            cursor="hand2",
        )
        back_main_menu.pack(pady=(15, 0))
        back_main_menu.bind("<Button-1>", lambda e: cmd2())

    def sign_in(self):
        """Authenticate admin credentials."""
        username = self.username.get()
        password = self.password.get()
        admin_db = load_db(ADMIN_DB_PATH)
        hashed_username = hash_input(username)

        if hashed_username in admin_db and verify_input(
            admin_db[hashed_username]["password"], password
        ):
            self.destroy()
            AdminDashboard(self.parent)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def back_to_main_menu(self):
        """Return to main menu."""
        self.parent.show_main_menu()


class AdminDashboard(tk.Frame):
    """Admin dashboard for reviewing providers."""

    def __init__(self, parent):
        super().__init__(parent, bg="#f8fafc")
        self.parent = parent
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
            text="Review Pending Providers",
            font=("Segoe UI", 16, "bold"),
            bg="white",
        ).pack(side="left", padx=20, pady=20)

        return_to_dashboard = tk.Label(
            header_frame,
            text="Logout",
            font=("Segoe UI Semibold", 10, "underline"),
            bg="white",
            cursor="hand2",
        )
        return_to_dashboard.pack(side="right", padx=20, pady=20)
        return_to_dashboard.bind("<Button-1>", lambda e: self.logout())

        providers_db = load_db(PROVIDER_DB_PATH)

        self.pending_count = 0

        for provider_id, provider_data in providers_db.items():
            if provider_data["status"] == "pending":
                self.pending_count += 1
                self.create_card(provider_id, provider_data)

        self.check_pending()

    def create_card(self, provider_id, provider_data):
        """Create provider review card."""
        org_name = provider_data["organization_name"]
        id = provider_id
        email = provider_data["email"]
        number = provider_data["contact_number"]
        address = provider_data["office_address"]

        card = tk.Frame(
            self,
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
            text=org_name,
            font=("Segoe UI", 14, "bold"),
            bg="white",
            justify="left",
        ).pack(anchor="w")

        sub_text = f"ID: {id} | Email: {email}\nContact: {number} | Location: {address}"

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

        reject_bttn = tk.Button(
            buttons_container,
            text="Reject",
            font=("Segoe UI", 10, "bold"),
            width=10,
            bg="darkred",
            fg="white",
            relief="flat",
            command=lambda p_id=provider_id, c=card: self.update_status(
                p_id, c, "rejected"
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
            command=lambda p_id=provider_id, c=card: self.update_status(
                p_id, c, "approved"
            ),
        )
        approve_bttn.pack(side="right", padx=10)

    def update_status(self, provider_id, card, status):
        """Update provider status."""
        providers_db = load_db(PROVIDER_DB_PATH)
        providers_db[provider_id]["status"] = status
        save_db(providers_db, PROVIDER_DB_PATH)
        card.destroy()
        self.pending_count -= 1
        self.check_pending()

    def check_pending(self):
        """Show message if no pending providers."""
        if self.pending_count == 0:
            tk.Label(
                self,
                text="No providers left to evaluate.",
                font=("Segoe UI", 10),
                bg="#f8fafc",
                fg="darkgrey",
            ).pack(fill="both", expand=True)

    def logout(self):
        """Return to login screen."""
        self.destroy()
        AdminLogin(self.parent)
