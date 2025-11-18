import customtkinter as ctk
from tkinter import messagebox
from base_page import BasePage


class ReservationPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        # Data per fietstype
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

        # ==== Titel ====
        title_label = ctk.CTkLabel(
            self.inner_frame,
            text="Nieuwe reservering",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(10, 10))

        # ==== Linkerzijde: formulier ====
        form_frame = ctk.CTkFrame(self.inner_frame, corner_radius=10)
        form_frame.grid(row=1, column=0, padx=(0, 20), pady=10, sticky="nsew")

        form_inner = ctk.CTkFrame(form_frame, fg_color="transparent")
        form_inner.pack(padx=20, pady=20, fill="x")

        # Naam
        name_label = ctk.CTkLabel(form_inner, text="Naam klant:")
        name_label.grid(row=0, column=0, sticky="e", padx=10, pady=5)
        self.name_entry = ctk.CTkEntry(form_inner, width=260)
        self.name_entry.grid(row=0, column=1, sticky="w", padx=10, pady=5)

        # E-mail
        email_label = ctk.CTkLabel(form_inner, text="E-mailadres:")
        email_label.grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.email_entry = ctk.CTkEntry(form_inner, width=260)
        self.email_entry.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        # Startdatum
        start_label = ctk.CTkLabel(form_inner, text="Startdatum (dd-mm-jjjj):")
        start_label.grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.start_entry = ctk.CTkEntry(form_inner, width=260)
        self.start_entry.grid(row=2, column=1, sticky="w", padx=10, pady=5)

        # Einddatum
        end_label = ctk.CTkLabel(form_inner, text="Einddatum (dd-mm-jjjj):")
        end_label.grid(row=3, column=0, sticky="e", padx=10, pady=5)
        self.end_entry = ctk.CTkEntry(form_inner, width=260)
        self.end_entry.grid(row=3, column=1, sticky="w", padx=10, pady=5)

        # Fietstype
        bike_type_label = ctk.CTkLabel(form_inner, text="Type fiets:")
        bike_type_label.grid(row=4, column=0, sticky="e", padx=10, pady=5)

        self.bike_type_var = ctk.StringVar(value="Herenfiets")
        self.bike_type_menu = ctk.CTkOptionMenu(
            form_inner,
            values=["Herenfiets", "Damesfiets", "E-bike"],
            variable=self.bike_type_var,
            width=260,
            command=self.on_bike_type_change  # belangrijk voor live update
        )
        self.bike_type_menu.grid(row=4, column=1, sticky="w", padx=10, pady=5)

        # Accessoires
        accessories_label = ctk.CTkLabel(form_inner, text="Accessoires:")
        accessories_label.grid(row=5, column=0, sticky="ne", padx=10, pady=5)

        self.access_childseat_var = ctk.BooleanVar()
        self.access_helmet_var = ctk.BooleanVar()

        childseat_cb = ctk.CTkCheckBox(
            form_inner,
            text="Kinderzitje",
            variable=self.access_childseat_var
        )
        childseat_cb.grid(row=5, column=1, sticky="w", padx=10, pady=2)

        helmet_cb = ctk.CTkCheckBox(
            form_inner,
            text="Helm",
            variable=self.access_helmet_var
        )
        helmet_cb.grid(row=6, column=1, sticky="w", padx=10, pady=2)

        # Opmerkingen
        comment_label = ctk.CTkLabel(form_inner, text="Opmerkingen (optioneel):")
        comment_label.grid(row=7, column=0, sticky="ne", padx=10, pady=5)

        self.comment_entry = ctk.CTkTextbox(form_inner, width=260, height=80)
        self.comment_entry.grid(row=7, column=1, sticky="w", padx=10, pady=5)

        # ===== Knoppen onder formulier =====
        button_frame = ctk.CTkFrame(self.inner_frame, fg_color="transparent")
        button_frame.grid(row=2, column=0, pady=(5, 10), sticky="w")

        submit_button = ctk.CTkButton(
            button_frame,
            text="Reservering opslaan",
            width=200,
            command=self.submit_reservation
        )
        submit_button.pack(side="left", padx=10, pady=10)

        # ==== Rechterzijde: prijs & beschrijving ====
        info_frame = ctk.CTkFrame(self.inner_frame, corner_radius=10)
        info_frame.grid(row=1, column=1, padx=(0, 0), pady=10, sticky="n")

        info_inner = ctk.CTkFrame(info_frame, fg_color="transparent")
        info_inner.pack(padx=20, pady=20)

        self.info_title_label = ctk.CTkLabel(
            info_inner,
            text="",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.info_title_label.pack(pady=(0, 10))

        self.info_price_label = ctk.CTkLabel(
            info_inner,
            text="",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.info_price_label.pack(pady=(0, 10))

        self.info_desc_label = ctk.CTkLabel(
            info_inner,
            text="",
            font=ctk.CTkFont(size=14),
            wraplength=260,
            justify="left"
        )
        self.info_desc_label.pack(pady=(0, 10))

        # Layout kolommen
        self.inner_frame.grid_columnconfigure(0, weight=1)
        self.inner_frame.grid_columnconfigure(1, weight=1)

        # Initieel info zetten
        self.update_bike_info()

    # ====== Update info rechts bij selectie ======
    def on_bike_type_change(self, choice):
        self.update_bike_info()

    def update_bike_info(self):
        bike_type = self.bike_type_var.get()
        data = self.bike_data.get(bike_type, {})

        self.info_title_label.configure(text=bike_type)
        self.info_price_label.configure(text=f"Prijs: {data.get('price', '-')}")
        self.info_desc_label.configure(text=data.get("desc", ""))

    # ====== Reservering opslaan ======
    def submit_reservation(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        start = self.start_entry.get().strip()
        end = self.end_entry.get().strip()

        if not name or not email or not start or not end:
            messagebox.showerror("Fout", "Vul minimaal naam, e-mail, start- en einddatum in.")
            return

        bike = self.bike_type_var.get()

        accs = []
        if self.access_childseat_var.get():
            accs.append("Kinderzitje")
        if self.access_helmet_var.get():
            accs.append("Helm")

        accs_text = ", ".join(accs) if accs else "Geen"

        # --- Opslaan in database via app.db ---
        self.app.db.save_reservation(
            name=name,
            email=email,
            start=start,
            end=end,
            bike_type=bike,
            accessories=accs_text,
            comment=self.comment_entry.get("1.0", "end").strip()
        )

        messagebox.showinfo("Succes", "Reservering succesvol opgeslagen!")

        # velden leegmaken
        self.name_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.start_entry.delete(0, "end")
        self.end_entry.delete(0, "end")
        self.bike_type_var.set("Herenfiets")
        self.access_childseat_var.set(False)
        self.access_helmet_var.set(False)
        self.comment_entry.delete("1.0", "end")

        # info rechts updaten (optioneel)
        self.update_bike_info()
