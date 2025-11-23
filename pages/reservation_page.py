import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from base_page import BasePage


class ReservationPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        # ==== fiets data ====
        self.bike_data = {
            "Herenfiets": {"price": 15, "desc": "Comfortabele herenfiets voor dagelijks gebruik. Ideaal voor stadsritten en korte toertochten."},
            "Damesfiets": {"price": 15, "desc": "Praktische damesfiets met lage instap. Geschikt voor zowel korte als lange ritten."},
            "E-bike": {"price": 27, "desc": "Elektrische fiets met krachtige ondersteuning. Perfect voor langere ritten en tegenwind."},
        }

        # ==== accessoires prijzen ====
        self.accessory_prices = {
            "Kinderzitje": 5,
            "Helm": 5,
            "Fietstas": 7,
            "Extra slot": 6,
            "Regenponcho": 4
        }

        # ==== titel ====
        title_label = ctk.CTkLabel(
            self.inner_frame,
            text="Nieuwe reservering",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(10, 10))

        # ==== layout configuratie ====
        self.inner_frame.grid_rowconfigure(1, weight=1)
        self.inner_frame.grid_columnconfigure(0, weight=1)
        self.inner_frame.grid_columnconfigure(1, weight=0)

        # ==== linkerzijde: formulier container ====
        form_frame = ctk.CTkFrame(self.inner_frame, corner_radius=10)
        form_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 20), pady=10)
        form_frame.grid_rowconfigure(0, weight=1)
        form_frame.grid_columnconfigure(0, weight=1)

        # ==== scrollbaar formulier ====
        self.form_scroll = ctk.CTkScrollableFrame(form_frame, fg_color="transparent")
        self.form_scroll.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.form_scroll.grid_columnconfigure(0, weight=0)
        self.form_scroll.grid_columnconfigure(1, weight=1)

        # ==== formulier velden ====

        # ==== naam ====
        ctk.CTkLabel(self.form_scroll, text="Naam klant:")\
            .grid(row=0, column=0, sticky="e", padx=10, pady=5)
        self.name_entry = ctk.CTkEntry(self.form_scroll, width=260)
        self.name_entry.grid(row=0, column=1, sticky="w", padx=10, pady=5)

        # ==== email ====
        ctk.CTkLabel(self.form_scroll, text="E-mailadres:")\
            .grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.email_entry = ctk.CTkEntry(self.form_scroll, width=260)
        self.email_entry.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        # ==== startdatum =====
        ctk.CTkLabel(self.form_scroll, text="Startdatum (dd-mm-jjjj):")\
            .grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.start_entry = ctk.CTkEntry(self.form_scroll, width=260)
        self.start_entry.grid(row=2, column=1, sticky="w", padx=10, pady=5)
        self.start_entry.bind("<KeyRelease>", lambda e: self.update_total_price())

        # ==== einddatum ====
        ctk.CTkLabel(self.form_scroll, text="Einddatum (dd-mm-jjjj):")\
            .grid(row=3, column=0, sticky="e", padx=10, pady=5)
        self.end_entry = ctk.CTkEntry(self.form_scroll, width=260)
        self.end_entry.grid(row=3, column=1, sticky="w", padx=10, pady=5)
        self.end_entry.bind("<KeyRelease>", lambda e: self.update_total_price())

        # ==== type fiets ====
        ctk.CTkLabel(self.form_scroll, text="Type fiets:")\
            .grid(row=4, column=0, sticky="e", padx=10, pady=5)
        self.bike_type_var = ctk.StringVar(value="Herenfiets")
        self.bike_type_menu = ctk.CTkOptionMenu(
            self.form_scroll,
            values=list(self.bike_data.keys()),
            variable=self.bike_type_var,
            width=260,
            command=lambda *args: self.update_total_price()
        )
        self.bike_type_menu.grid(row=4, column=1, sticky="w", padx=10, pady=5)

        # ==== aantal fietsen ====
        ctk.CTkLabel(self.form_scroll, text="Aantal fietsen:")\
            .grid(row=5, column=0, sticky="e", padx=10, pady=5)
        self.bike_amount_var = ctk.StringVar(value="1")
        self.bike_amount_entry = ctk.CTkEntry(
            self.form_scroll,
            width=80,
            textvariable=self.bike_amount_var
        )
        self.bike_amount_entry.grid(row=5, column=1, sticky="w", padx=10, pady=5)
        self.bike_amount_entry.bind("<KeyRelease>", lambda e: self.update_total_price())

        # ==== accessores ====
        ctk.CTkLabel(self.form_scroll, text="Accessoires:")\
            .grid(row=6, column=0, sticky="ne", padx=10, pady=(10, 5))

        # ==== accessores opties ====
        self.access_childseat_var = ctk.BooleanVar()
        self.access_helmet_var = ctk.BooleanVar()
        self.access_bag_var = ctk.BooleanVar()
        self.access_lock_var = ctk.BooleanVar()
        self.access_poncho_var = ctk.BooleanVar()

        ctk.CTkCheckBox(self.form_scroll, text="Kinderzitje (+ €5)",
                        variable=self.access_childseat_var,
                        command=self.update_total_price)\
            .grid(row=6, column=1, sticky="w", padx=10, pady=2)

        ctk.CTkCheckBox(self.form_scroll, text="Helm (+ €5)",
                        variable=self.access_helmet_var,
                        command=self.update_total_price)\
            .grid(row=7, column=1, sticky="w", padx=10, pady=2)

        ctk.CTkCheckBox(self.form_scroll, text="Fietstas (+ €7)",
                        variable=self.access_bag_var,
                        command=self.update_total_price)\
            .grid(row=8, column=1, sticky="w", padx=10, pady=2)

        ctk.CTkCheckBox(self.form_scroll, text="Extra slot (+ €6)",
                        variable=self.access_lock_var,
                        command=self.update_total_price)\
            .grid(row=9, column=1, sticky="w", padx=10, pady=2)

        ctk.CTkCheckBox(self.form_scroll, text="Regenponcho (+ €4)",
                        variable=self.access_poncho_var,
                        command=self.update_total_price)\
            .grid(row=10, column=1, sticky="w", padx=10, pady=2)

        # ==== opmerking ====
        ctk.CTkLabel(self.form_scroll, text="Opmerking (optioneel):")\
            .grid(row=11, column=0, sticky="ne", padx=10, pady=(15, 5))
        self.comment_entry = ctk.CTkTextbox(self.form_scroll, width=260, height=80)
        self.comment_entry.grid(row=11, column=1, sticky="w", padx=10, pady=(5, 15))

        # ==== totaalprijs label ====
        self.total_price_label = ctk.CTkLabel(
            self.form_scroll,
            text="Totaalprijs: €0",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.total_price_label.grid(row=12, column=1, sticky="w", padx=10, pady=(20, 10))

        # ==== submit knop ====
        submit_button = ctk.CTkButton(
            self.form_scroll,
            text="Reservering opslaan",
            width=200,
            command=self.submit_reservation
        )
        submit_button.grid(row=13, column=1, sticky="w", padx=10, pady=(10, 20))

        # ==== fiets info ====
        info_frame = ctk.CTkFrame(self.inner_frame, corner_radius=10)
        info_frame.grid(row=1, column=1, sticky="n", pady=10)

        info_inner = ctk.CTkFrame(info_frame, fg_color="transparent")
        info_inner.pack(padx=20, pady=20)

        self.info_title_label = ctk.CTkLabel(info_inner, text="", font=ctk.CTkFont(size=22, weight="bold"))
        self.info_title_label.pack(pady=(0, 10))

        self.info_price_label = ctk.CTkLabel(info_inner, text="", font=ctk.CTkFont(size=20, weight="bold"))
        self.info_price_label.pack(pady=(0, 10))

        self.info_borg_label = ctk.CTkLabel(info_inner, text="Borg: €100",
                                            font=ctk.CTkFont(size=18, weight="bold"))
        self.info_borg_label.pack(pady=(0, 10))

        self.info_desc_label = ctk.CTkLabel(
            info_inner, text="", font=ctk.CTkFont(size=14), wraplength=260, justify="left"
        )
        self.info_desc_label.pack(pady=(0, 10))

        self.update_bike_info()
        self.update_total_price()

    # ==== datum validatie (AI gemaakt) ====
    def validate_date(self, date_text):
        try:
            return datetime.strptime(date_text, "%d-%m-%Y")
        except ValueError:
            return None

    # ==== fiets info updaten ====
    def update_bike_info(self):
        bike_type = self.bike_type_var.get()
        data = self.bike_data[bike_type]

        self.info_title_label.configure(text=bike_type)
        self.info_price_label.configure(text=f"Prijs per dag: €{data['price']}")
        self.info_desc_label.configure(text=data["desc"])

    # ==== totaalprijs berekenen (AI geholpen) ====
    def update_total_price(self):
        # datums ophalen
        start = self.start_entry.get().strip()
        end = self.end_entry.get().strip()

        start_date = self.validate_date(start)
        end_date = self.validate_date(end)

        # aantal dagen berekenen
        if start_date and end_date and end_date >= start_date:
            days = (end_date - start_date).days + 1
        else:
            days = 0

        # fietsprijs × dagen × aantal
        bike_type = self.bike_type_var.get()
        bike_price = self.bike_data[bike_type]["price"]

        try:
            amount = int(self.bike_amount_var.get())
        except:
            amount = 1

        bike_total = bike_price * days * amount

        # accessoires optellen
        acc_total = 0
        if self.access_childseat_var.get():
            acc_total += 5
        if self.access_helmet_var.get():
            acc_total += 5
        if self.access_bag_var.get():
            acc_total += 7
        if self.access_lock_var.get():
            acc_total += 6
        if self.access_poncho_var.get():
            acc_total += 4

        # borgborgborgborgborgborgborgborgborgborg
        borg = 100

        total = bike_total + acc_total + borg

        self.total_price_label.configure(text=f"Totaalprijs: €{total}")
        return total, borg

    # ==== reservering opslaan ====
    def submit_reservation(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        start = self.start_entry.get().strip()
        end = self.end_entry.get().strip()

        if not name or not email or not start or not end:
            messagebox.showerror("Fout", "Vul alle verplichte velden in.")
            return

        # ==== datummen controleren ====
        start_date = self.validate_date(start)
        end_date = self.validate_date(end)

        if not start_date:
            messagebox.showerror("Fout", "Startdatum is ongeldig (dd-mm-jjjj).")
            return
        if not end_date:
            messagebox.showerror("Fout", "Einddatum is ongeldig (dd-mm-jjjj).")
            return
        if end_date < start_date:
            messagebox.showerror("Fout", "Einddatum mag niet vóór de startdatum liggen.")
            return

        # ==== aantal fietsen valideren ====
        try:
            amount = int(self.bike_amount_var.get())
            if amount < 1:
                raise ValueError
        except:
            messagebox.showerror("Fout", "Aantal fietsen moet minimaal 1 zijn.")
            return

        bike_type = self.bike_type_var.get()
        bike_label = f"{bike_type} (x{amount})"

        # ==== accessoires verzamelen ====
        accs = []
        if self.access_childseat_var.get():
            accs.append("Kinderzitje (+5€)")
        if self.access_helmet_var.get():
            accs.append("Helm (+5€)")
        if self.access_bag_var.get():
            accs.append("Fietstas (+7€)")
        if self.access_lock_var.get():
            accs.append("Extra slot (+6€)")
        if self.access_poncho_var.get():
            accs.append("Regenponcho (+4€)")

        accs_text = ", ".join(accs) if accs else "Geen"

        # ==== prijs berekenen ====
        total, borg = self.update_total_price()

        # ==== database save ====
        self.app.db.save_reservation(
            name=name,
            email=email,
            start_date=start,
            end_date=end,
            bike_type=bike_label,
            accessories=accs_text,
            comment=self.comment_entry.get("1.0", "end").strip(),
            total_price=total,
            borg=borg
        )

        messagebox.showinfo("Succes", "Reservering succesvol opgeslagen!")
