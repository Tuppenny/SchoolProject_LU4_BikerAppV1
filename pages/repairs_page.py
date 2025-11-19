import customtkinter as ctk
from pages.portal_header import PortalHeader


class RepairsPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # ===== HEADER =====
        header = PortalHeader(self, app, "Reparaties")
        header.pack(fill="x")

        # ===== CONTENT =====
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True)

        title = ctk.CTkLabel(
            content_frame,
            text="Reparaties",
            font=ctk.CTkFont(size=26, weight="bold")
        )
        title.pack(pady=40)

        subtitle = ctk.CTkLabel(
            content_frame,
            text="(Hier komen alle reparatiestatussen en open reparaties)",
            font=ctk.CTkFont(size=15)
        )
        subtitle.pack(pady=10)
