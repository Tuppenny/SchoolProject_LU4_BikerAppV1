import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from base_page import BasePage


class ReservationPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        # ===== FIETS DATA =====
        self.bike_data = {
            "Herenfiets": {
                "price": "€ 777,-",
                "desc": (
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                    "Nullam feugiat urna ac mauris molestie, sed varius massa luctus."
                )
            },
            "Damesfiets": {
                "price": "€ 888,-",
                "desc": (
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                    "Vivamus sit amet dui in velit ultricies tincidunt sed non leo."
                )
            },
            "E-bike": {
                "price": "€ 999,-",
                "desc": (
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                    "Praesent convallis lacus at mauris vulputate, vel cursus justo pulvinar."
                )
            },
        }

        # ===== TITEL =====
        title_label = ctk.CTkLabel(
            self.inner_frame,
            text="Nieuwe reservering",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(10, 10))

        # ===== LINKERZIJDE (FORMULIER) =====
        form_frame = ctk.CTkFrame(self.inner_frame, corner_radius=10)
        form_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 20), pady=10)

        form_inner = ctk.CTkFrame(form_frame, fg_color="transparent")
        form_inner.pack(padx=20, pady=20, fill="x")

        # Naam
        ctk.CTkLabel(form_inner, text="Naam klant:").grid(row=0, column=0, sticky="e", padx=10, pady=5)
        self.name_entry = ctk.CTkEntry(form_inner, width=260)
        self.name_entry.grid(row=0, column=1, sticky="w", padx=10, pady=5)

        # Email
        ctk.CTkLabel(form_inner, text="E-mailadres:").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.email_entry = ctk.CTkEntry(form_inner, width=260)
        self.email_entry.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        # Startdatum
        ctk.CTkLabel(form_inner, text="Startdatum (dd-mm-jjjj):").grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.start_entry = ctk.CTkEntry(form_inner, width=260)
        self.start_entry.grid(row=2, column=1, sticky="w", padx=10, pady=5)

        # Einddatum
        ctk.CTkLabel(form_inner, text="Einddatum (dd-mm-jjjj):").grid(row=3, column=0, sticky="e", padx=10, pady=5)
        self.end_entry = ctk.CTkEntry(form_inner, width=260)
        self.end_entry.grid(row=3, column=1, sticky="w", padx=10, pady=5)

        # Type fiets
        ctk.CTkLabel(form_inner, text="Type fiets:").grid(row=4, column=0, sticky="e", padx=10, pady=5)
        self.bike_type_var = ctk.StringVar(value="Herenfiets")
        self.bike_type_menu = ctk.CTkOptionMenu(
            form_inner,
            values=["Herenfiets", "Damesfiets", "E-bike"],
            variable=self.bike_type_var,
            width=260,
            command=self.on_bike_type_change
        )
        self.bike_type_menu.grid(row=4, column=1, sticky="w", padx=10, pady=5)

        # Accessoires
        ctk.CTkLabel(form_inner, text="Accessoires:").grid(row=5, column=0, sticky="ne", padx=10, pady=5)

        self.access_childseat_var = ctk.BooleanVar()
        self.access_helmet_var = ctk.BooleanVar()

        ctk.CTkCheckBox(
            form_inner,
            text="Kinderzitje",
            variable=self.access_childseat_var
        ).grid(row=5, column=1, sticky="w", padx=10, pady=2)

        ctk.CTkCheckBox(
            form_inner,
            text="Helm",
            variable=self.access_helmet_var
        ).grid(row=6, column=1, sticky="w", padx=10, pady=2)

        # Opmerkingen
        ctk.CTkLabel(form_inner, text="Opmerkingen (optioneel):").grid(row=7, column=0, sticky="ne", padx=10, pady=5)
        self.comment_entry = ctk.CTkTextbox(form_inner, width=260, height=80)
        self.comment_entry.grid(row=7, column=1, sticky="w", padx=10, pady=5)

        # Opslaan
        submit_button = ctk.CTkButton(
            self.inner_frame,
            text="Reservering opslaan",
            width=200,
            command=self.submit_reservation
        )
        submit_button.grid(row=2, column=0, sticky="w", pady=10)

        # ===== RECHTERZIJDE (BIKE INFO) =====
        info_frame = ctk.CTkFrame(self.inner_frame, corner_radius=10)
        info_frame.grid(row=1, column=1, sticky="n", pady=10)

        info_inner = ctk.CTkFrame(info_frame, fg_color="transparent")
        info_inner.pack(padx=20, pady=20)

        self.info_title_label = ctk.CTkLabel(
            info_inner, text="", font=ctk.CTkFont(size=22, weight="bold")
        )
        self.info_title_label.pack(pady=(0, 10))

        self.info_price_label = ctk.CTkLabel(
            info_inner, text="", font=ctk.CTkFont(size=20, weight="bold")
        )
        self.info_price_label.pack(pady=(0, 10))

        self.info_desc_label = ctk.CTkLabel(
            info_inner, text="", font=ctk.CTkFont(size=14), wraplength=260, justify="left"
        )
        self.info_desc_label.pack(pady=(0, 10))

        # Kolom layout
        self.inner_frame.grid_columnconfigure(0, weight=1)
        self.inner_frame.grid_columnconfigure(1, weight=1)

        # Eerste keer info laden
        self.update_bike_info()

    # =====================================================
    #              DATUM VALIDATIE FUNCTIE
    # =====================================================
    def validate_date(self, date_text):
        try:
            return datetime.strptime(date_text, "%d-%m-%Y")
        except ValueError:
            return None

    # =====================================================
    #                  BIKE INFO UPDATES
    # =====================================================
    def on_bike_type_change(self, *_):
        self.update_bike_info()

    def update_bike_info(self):
        bike_type = self.bike_type_var.get()
        data = self.bike_data[bike_type]

        self.info_title_label.configure(text=bike_type)
        self.info_price_label.configure(text=f"Prijs: {data['price']}")
        self.info_desc_label.configure(text=data["desc"])

    # =====================================================
    #                  RESERVERING OPSLAAN
    # =====================================================
    def submit_reservation(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        start = self.start_entry.get().strip()
        end = self.end_entry.get().strip()

        if not name or not email or not start or not end:
            messagebox.showerror("Fout", "Vul alle verplichte velden in.")
            return

        # Datum validatie
        start_date = self.validate_date(start)
        end_date = self.validate_date(end)

        if not start_date:
            messagebox.showerror("Fout", "Startdatum is ongeldig. Gebruik dd-mm-jjjj.")
            return

        if not end_date:
            messagebox.showerror("Fout", "Einddatum is ongeldig. Gebruik dd-mm-jjjj.")
            return

        if end_date < start_date:
            messagebox.showerror("Fout", "Einddatum moet na de startdatum liggen.")
            return

        bike = self.bike_type_var.get()

        # ACCESSOIRES
        accs = []
        if self.access_childseat_var.get():
            accs.append("Kinderzitje")
        if self.access_helmet_var.get():
            accs.append("Helm")

        accs_text = ", ".join(accs) if accs else "Geen"

        # OPSLAAN
        self.app.db.save_reservation(
            name=name,
            email=email,
            start_date=start,
            end_date=end,
            bike_type=bike,
            accessories=accs_text,
            comment=self.comment_entry.get("1.0", "end").strip()
        )

        messagebox.showinfo("Succes", "Reservering succesvol opgeslagen!")
