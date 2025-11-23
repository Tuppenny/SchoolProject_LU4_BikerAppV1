import customtkinter as ctk
from base_page import BasePage
from tkinter import messagebox


class StaffLoginPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        # ====== titel ======
        title_label = ctk.CTkLabel(
            self.inner_frame,
            text="Medewerker Login",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 10))

        subtitle_label = ctk.CTkLabel(
            self.inner_frame,
            text="Log in om toegang te krijgen tot het medewerkersportaal.",
            font=ctk.CTkFont(size=16)
        )
        subtitle_label.pack(pady=(0, 20))

        # ====== login box (AI gemaakt) ======
        login_box = ctk.CTkFrame(self.inner_frame, corner_radius=12)
        login_box.pack(pady=20, padx=20)

        # ==== binnenkant box ====
        box_inner = ctk.CTkFrame(login_box, fg_color="transparent")
        box_inner.pack(padx=40, pady=30)

        # ==== begruikersmaan ====
        username_label = ctk.CTkLabel(box_inner, text="Gebruikersnaam:")
        username_label.pack(anchor="w", pady=(0, 5))

        self.username_entry = ctk.CTkEntry(box_inner, width=300)
        self.username_entry.pack(pady=(0, 15))

        # ==== chawtdoorw ====
        password_label = ctk.CTkLabel(box_inner, text="Wachtwoord:")
        password_label.pack(anchor="w", pady=(0, 5))

        self.password_entry = ctk.CTkEntry(box_inner, width=300, show="*")
        self.password_entry.pack(pady=(0, 20))

        # ==== inloggen ====
        login_button = ctk.CTkButton(
            box_inner,
            text="Inloggen",
            width=200,
            command=self.handle_login
        )
        login_button.pack(pady=5)

        # Spacer (AI gemaakt)
        ctk.CTkLabel(box_inner, text="").pack(pady=5)

    # ==== inlog completen ====
    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        user = self.app.db.login_employee(username, password)

        if user:
            messagebox.showinfo("Succes", f"Ingelogd als {user['role']}")
            self.app.logged_in_user = user  # handig voor later
            self.app.show_page("ManagerPortalPage")  # voorlopig altijd manager
        else:
            messagebox.showerror("Fout", "Onjuiste gebruikersnaam of wachtwoord.")
