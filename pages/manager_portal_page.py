import customtkinter as ctk

from pages.portal_header import PortalHeader

class ManagerPortalPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)

        header = PortalHeader(self, app, "Medewerkerportaal")
        header.pack(fill="x")


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


class ManagerPortalPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # ===========================
        #       TOP NAVIGATION
        # ===========================

        top_nav = ctk.CTkFrame(self, height=60, fg_color="#2E2E2E")
        top_nav.pack(fill="x")

        # LOGO (links, verticaal gecentreerd)
        logo_label = ctk.CTkLabel(
            top_nav,
            text="Biker Haaglanden",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        logo_label.place(x=20, rely=0.5, anchor="w")  # <-- verticaal gecentreerd

        # TITEL (midden)
        center_label = ctk.CTkLabel(
            top_nav,
            text="Medewerkerportaal",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        center_label.place(relx=0.5, rely=0.5, anchor="center")  # <-- perfect gecentreerd

        # UITLOGKNOP (rechts, verticaal gecentreerd)
        logout_btn = ctk.CTkButton(
            top_nav,
            text="Uitloggen",
            width=100,
            height=24,
            font=ctk.CTkFont(size=14),
            command=self.confirm_logout
        )
        logout_btn.place(relx=1.0, x=-20, rely=0.5, anchor="e")

        # ===========================
        #     MAIN BUTTON SECTION
        # ===========================

        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(expand=True)

        # Grid zodat knoppen netjes staan lol
        for col in range(3):
            main_frame.grid_columnconfigure(col, weight=1)

        # Knopafmetingen
        BTN_WIDTH = 150
        BTN_HEIGHT = 150

        BUTTON_PADX = 15
        BUTTON_PADY = 20

        # ----------- KNOP: RESERVERINGEN -----------
        reservations_btn = ctk.CTkButton(
            main_frame,
            text="Reserveringen",
            width=BTN_WIDTH,
            height=BTN_HEIGHT,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.open_reservations
        )
        reservations_btn.grid(row=0, column=0, padx=BUTTON_PADX, pady=BUTTON_PADY)

        # ----------- KNOP: SCHADE MELDINGEN -----------
        damage_btn = ctk.CTkButton(
            main_frame,
            text="Schade meldingen",
            width=BTN_WIDTH,
            height=BTN_HEIGHT,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.open_damage_reports
        )
        damage_btn.grid(row=0, column=1, padx=BUTTON_PADX, pady=BUTTON_PADY)

        # ----------- KNOP: REPARATIES -----------
        repairs_btn = ctk.CTkButton(
            main_frame,
            text="Reparaties",
            width=BTN_WIDTH,
            height=BTN_HEIGHT,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.open_repairs
        )
        repairs_btn.grid(row=0, column=2, padx=BUTTON_PADX, pady=BUTTON_PADY)

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

    # ===========================
    #      FUNCTIES PER KNOP
    # ===========================

    def open_reservations(self):
        self.app.show_page("ReservationsPage")

    def open_damage_reports(self):
        self.app.show_page("DamageReportsPage")

    def open_repairs(self):
        self.app.show_page("RepairsPage")

