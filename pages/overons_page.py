import customtkinter as ctk
from base_page import BasePage


class OverOnsPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        label = ctk.CTkLabel(
            self.inner_frame,
            text="Over Ons",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        label.pack(pady=20)
