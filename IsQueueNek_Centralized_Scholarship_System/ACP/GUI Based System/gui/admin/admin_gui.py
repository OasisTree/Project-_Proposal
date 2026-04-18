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

        tk.Label(card, text=title, bg="white", font=("Segoe UI", 18, "bold")).pack()

        tk.Label(card, text=desc, bg="white", fg="#64748b", font=("Segoe UI", 10)).pack(
            pady=(0, 5)
        )

        tk.Frame(card, height=1, bg="#e5e7eb").pack(fill="x", pady=(0, 15))

        tk.Label(card, text=subhead1, bg="white", font=("Segoe UI", 9, "bold")).pack(
            anchor="w"
        )

        self.username = tk.Entry(
            card, font=("Segoe UI", 9), bg="white", highlightthickness=1, relief="flat"
        )
        self.username.pack(fill="x", ipady=5, pady=(0, 15))

        tk.Label(card, text=subhead2, bg="white", font=("Segoe UI", 9, "bold")).pack(
            anchor="w"
        )

        self.password = tk.Entry(
            card,
            font=("Segoe UI", 9),
            bg="white",
            highlightthickness=1,
            relief="flat",
            show="•",
        )
        self.password.pack(fill="x", ipady=5, pady=(0, 15))

        tk.Button(
            card,
            text="Sign In",
            font=("Segoe UI", 10, "bold"),
            bg="#2563eb",
            fg="white",
            relief="flat",
            command=cmd1,
        ).pack(fill="x", ipady=5)

        back = tk.Label(
            card,
            text="Back to Main Menu",
            font=("Segoe UI", 10),
            bg="white",
            fg="darkgrey",
            cursor="hand2",
        )
        back.pack(pady=(15, 0))
        back.bind("<Button-1>", lambda e: cmd2())

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

        header = tk.Frame(
            self, bg="white", highlightthickness=1, highlightbackground="darkgrey"
        )
        header.pack(fill="x")

        tk.Label(
            header,
            text="Review Pending Providers",
            font=("Segoe UI", 16, "bold"),
            bg="white",
        ).pack(side="left", padx=20, pady=20)

        tk.Label(
            header,
            text="Logout",
            font=("Segoe UI Semibold", 10, "underline"),
            bg="white",
            cursor="hand2",
        ).pack(side="right", padx=20)
        header.bind("<Button-1>", lambda e: self.logout())

        self.providers_db = load_db(PROVIDER_DB_PATH)
        self.pending_count = 0

        for pid, data in self.providers_db.items():
            if data["status"] == "pending":
                self.pending_count += 1
                self.create_card(pid, data)

        self.check_pending()

    def create_card(self, provider_id, provider_data):
        """Create provider review card."""

        card = tk.Frame(
            self, bg="white", highlightthickness=1, highlightbackground="lightgrey"
        )
        card.pack(fill="x", padx=20, pady=10)

        info = (
            f"ID: {provider_id} | Email: {provider_data['email']}\n"
            f"Contact: {provider_data['contact_number']} | "
            f"Location: {provider_data['office_address']}"
        )

        tk.Label(
            card,
            text=provider_data["organization_name"],
            font=("Segoe UI", 14, "bold"),
            bg="white",
        ).pack(anchor="w")

        tk.Label(card, text=info, font=("Segoe UI", 9), fg="darkgrey", bg="white").pack(
            anchor="w"
        )

        btn_frame = tk.Frame(card, bg="white")
        btn_frame.pack(anchor="e", padx=5)

        tk.Button(
            btn_frame,
            text="Reject",
            bg="darkred",
            fg="white",
            command=lambda: self.update_status(provider_id, card, "rejected"),
        ).pack(side="right", padx=5)

        tk.Button(
            btn_frame,
            text="Approve",
            bg="darkgreen",
            fg="white",
            command=lambda: self.update_status(provider_id, card, "approved"),
        ).pack(side="right", padx=5)

    def update_status(self, provider_id, card, status):
        """Update provider status."""

        self.providers_db = load_db(PROVIDER_DB_PATH)
        self.providers_db[provider_id]["status"] = status
        save_db(self.providers_db, PROVIDER_DB_PATH)

        card.destroy()
        self.pending_count -= 1
        self.check_pending()

    def check_pending(self):
        """Show message if no pending providers."""
        if self.pending_count == 0:
            tk.Label(
                self, text="No providers left to evaluate.", bg="#f8fafc", fg="darkgrey"
            ).pack(expand=True)

    def logout(self):
        """Return to login screen."""
        self.destroy()
        AdminLogin(self.parent)
