import customtkinter as ctk
from base_page import BasePage

class ContactPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        label = ctk.CTkLabel(
            self.inner_frame,
            text="Contact",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        label.pack(pady=20)
