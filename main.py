import customtkinter as ctk

from pages.home_page import HomePage
from pages.reservation_page import ReservationPage
from pages.overons_page import OverOnsPage
from pages.contact_page import ContactPage
from pages.staff_login_page import StaffLoginPage

from database import Database   # ← DEZE REGEL TOEVOEGEN




class BikerApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        # ------- WINDOW SETTINGS -------
        self.title("Biker Haaglanden")
        self.geometry("1000x650")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # ------- DATABASE AANMAKEN (HIER!) -------
        self.db = Database()   # ← HIER wordt de database gemaakt

        # ------- MAIN CONTAINER -------
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        # Dictionary voor pages
        self.pages = {}

        # ------- REGISTER ALL PAGES -------
        for PageClass in (
            HomePage,
            ReservationPage,
            OverOnsPage,
            ContactPage,
            StaffLoginPage
        ):
            page_name = PageClass.__name__
            frame = PageClass(parent=self.container, app=self)
            self.pages[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Startpagina
        self.show_page("HomePage")

    def show_page(self, page_name: str):
        """Wissel van pagina."""
        page = self.pages.get(page_name)
        if page:
            page.tkraise()
        else:
            print(f"Page '{page_name}' not found.")



if __name__ == "__main__":
    app = BikerApp()
    app.mainloop()
