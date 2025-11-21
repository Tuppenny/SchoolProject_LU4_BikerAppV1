import customtkinter as ctk

from database import Database

# Publieke pagina's
from pages.home_page import HomePage
from pages.reservation_page import ReservationPage
from pages.damage_page import DamagePage
from pages.overons_page import OverOnsPage
from pages.contact_page import ContactPage

# Medewerker login en portaal
from pages.staff_login_page import StaffLoginPage
from pages.manager_portal_page import ManagerPortalPage

# Universele portal-pagina's
from pages.reservations_page import ReservationsPage
from pages.damage_reports_page import DamageReportsPage
from pages.repairs_page import RepairsPage


class BikerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # ==== VENSTERINSTELLINGEN ====
        self.title("Biker Haaglanden")
        self.geometry("1500x1000")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # ==== DATABASE ====
        self.db = Database()

        # Huidige ingelogde medewerker (dict met id, username, role)
        self.logged_in_user = None

        # ==== HOOFD-CONTAINER VOOR PAGINA'S ====
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # ==== PAGINA'S AANMAKEN EN REGISTREREN ====
        self.pages = {}

        page_classes = (
            HomePage,
            ReservationPage,
            DamagePage,
            OverOnsPage,
            ContactPage,
            StaffLoginPage,
            ManagerPortalPage,
            ReservationsPage,
            DamageReportsPage,
            RepairsPage,
        )

        for PageClass in page_classes:
            page_name = PageClass.__name__
            frame = PageClass(parent=self.container, app=self)  # <-- ALTIJD parent=self.container
            self.pages[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Startpagina
        self.show_page("HomePage")

    def show_page(self, page_name: str):
        """Toon een bepaalde pagina op basis van de class-naam."""
        page = self.pages.get(page_name)
        if page:
            page.tkraise()
        else:
            print(f"Page '{page_name}' not found.")


if __name__ == "__main__":
    app = BikerApp()
    app.mainloop()
