import customtkinter as ctk
from base_page import BasePage

class HomePage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        title = ctk.CTkLabel(
            self.inner_frame,
            text="Welkom bij Biker Haaglanden",
            font=ctk.CTkFont(size=30, weight="bold")
        )
        title.pack(pady=20)

        info = ctk.CTkLabel(
            self.inner_frame,
            text="Reserveer snel en eenvoudig uw fiets.",
            font=ctk.CTkFont(size=18)
        )
        info.pack(pady=10)
