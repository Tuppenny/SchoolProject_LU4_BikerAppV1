import customtkinter as ctk


class PortalHeader(ctk.CTkFrame):
    def __init__(self, parent, app, title):
        super().__init__(parent, height=60, fg_color="#2E2E2E")
        self.app = app
        self.title_text = title

        # LOGO links
        logo_label = ctk.CTkLabel(
            self,
            text="Biker Haaglanden",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        logo_label.place(x=20, rely=0.5, anchor="w")

        # TITEL midden
        center_label = ctk.CTkLabel(
            self,
            text=title,
            font=ctk.CTkFont(size=18, weight="bold")
        )
        center_label.place(relx=0.5, rely=0.5, anchor="center")

        # UITLOG-knop rechts
        logout_btn = ctk.CTkButton(
            self,
            text="Uitloggen",
            width=90,
            height=24,
            font=ctk.CTkFont(size=14),
            command=self.confirm_logout
        )
        logout_btn.place(relx=1.0, x=-20, rely=0.5, anchor="e")

        # TERUG-knop rechts (naast uitloggen)
        back_btn = ctk.CTkButton(
            self,
            text="← Terug",
            width=90,
            height=24,
            font=ctk.CTkFont(size=14),
            command=self.go_back
        )
        back_btn.place(relx=1.0, x=-120, rely=0.5, anchor="e")

    # =====================
    #   TERUG KNOP
    # =====================
    def go_back(self):
        role = self.app.logged_in_user["role"]

        if role == "manager":
            self.app.show_page("ManagerPortalPage")
        elif role == "balie":
            self.app.show_page("BaliePortalPage")     # JE VOEGT DIT LATER TOE
        elif role == "reparateur":
            self.app.show_page("ReparateurPortalPage")  # JE VOEGT DIT LATER TOE
        else:
            self.app.show_page("StaffLoginPage")

    # =====================
    #   UITLOG POPUP
    # =====================
    def confirm_logout(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Uitloggen")
        popup.geometry("300x150")
        popup.resizable(False, False)

        message = ctk.CTkLabel(
            popup,
            text="Weet u zeker dat u wilt uitloggen?",
            font=ctk.CTkFont(size=14)
        )
        message.pack(pady=20)

        btn_frame = ctk.CTkFrame(popup, fg_color="transparent")
        btn_frame.pack(pady=10)

        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Annuleren",
            width=100,
            command=popup.destroy
        )
        cancel_btn.pack(side="left", padx=10)

        yes_btn = ctk.CTkButton(
            btn_frame,
            text="Uitloggen",
            fg_color="#8b0000",
            width=100,
            command=lambda: [popup.destroy(), self.app.show_page("StaffLoginPage")]
        )
        yes_btn.pack(side="left", padx=10)
