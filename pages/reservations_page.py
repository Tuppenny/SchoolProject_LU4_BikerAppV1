import customtkinter as ctk
from pages.portal_header import PortalHeader
from tkinter import messagebox


class ReservationsPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # ==== header ====
        header = PortalHeader(self, app, "Reserveringen")
        header.pack(fill="x")

        # ==== content frame (AI gemaakt) ====
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # ==== titel ====
        title_label = ctk.CTkLabel(
            content_frame,
            text="Reserveringoverzicht",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(0, 20))

        # ==== searchbar ====
        search_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        search_frame.pack(pady=(0, 20))

        self.search_entry = ctk.CTkEntry(
            search_frame,
            width=300,
            placeholder_text="Zoek op naam of e-mail..."
        )
        self.search_entry.pack(side="left", padx=5)

        search_btn = ctk.CTkButton(
            search_frame,
            text="Zoeken",
            width=100,
            command=self.search_reservations
        )
        search_btn.pack(side="left", padx=5)

        reset_btn = ctk.CTkButton(
            search_frame,
            text="Refresh",
            width=80,
            command=self.load_reservations
        )
        reset_btn.pack(side="left", padx=5)

        # ==== scrollable table container (AI gemaakt) ====
        table_container = ctk.CTkFrame(content_frame)
        table_container.pack(fill="both", expand=True)

        # ==== canvas (AI gemaakt) ====
        self.table_canvas = ctk.CTkCanvas(
            table_container,
            bg="#1E1E1E",
            highlightthickness=0
        )
        self.table_canvas.pack(side="left", fill="both", expand=True)

        # ==== scrollbar ====
        v_scroll = ctk.CTkScrollbar(
            table_container,
            command=self.table_canvas.yview
        )
        v_scroll.pack(side="right", fill="y")
        self.table_canvas.configure(yscrollcommand=v_scroll.set)

        # ==== scrollbar horizontaal (AI gemaakt) ====
        h_scroll = ctk.CTkScrollbar(
            content_frame,
            orientation="horizontal",
            command=self.table_canvas.xview
        )
        h_scroll.pack(fill="x")
        self.table_canvas.configure(xscrollcommand=h_scroll.set)

        # inner frame (hier renderen we de tabel)
        self.table_frame = ctk.CTkFrame(self.table_canvas, fg_color="#1E1E1E")
        self.table_window = self.table_canvas.create_window(
            (0, 0),
            window=self.table_frame,
            anchor="nw"
        )

        # auto-resize scroll region
        def update_scroll_region(event=None):
            self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all"))

        self.table_frame.bind("<Configure>", update_scroll_region)

        # ==== table headers ====
        headers = [
            "Status", "ID", "Naam", "E-mail",
            "Start", "Einde",
            "Fiets", "Accessoires",
            "Totaal", "Borg",
            "Teruggavedatum", "Acties"
        ]

        for idx, text in enumerate(headers):
            lbl = ctk.CTkLabel(
                self.table_frame,
                text=text,
                font=ctk.CTkFont(size=14, weight="bold")
            )
            lbl.grid(row=0, column=idx, padx=10, pady=10)

        self.load_reservations()

    # ==== load / search data ====
    def load_reservations(self):
        self.populate_table(self.app.db.get_all_reservations())

    def search_reservations(self):
        keyword = self.search_entry.get().strip()
        if keyword == "":
            self.load_reservations()
        else:
            results = self.app.db.search_reservations(keyword)
            self.populate_table(results)

    # ==== populate table (AI geholpen)====
    def populate_table(self, data):
        for widget in self.table_frame.winfo_children():
            info = widget.grid_info()
            if info["row"] != 0:
                widget.destroy()

        if not data:
            lbl = ctk.CTkLabel(self.table_frame, text="Geen reserveringen gevonden.")
            lbl.grid(row=1, column=0, pady=20, columnspan=13)
            return

        for row_index, row in enumerate(data, start=1):
            (
                reservation_id,
                name,
                email,
                start_date,
                end_date,
                bike_type,
                accessories,
                comment,
                total_price,
                borg,
                status,
                return_date,
                borg_status
            ) = row

            status = status or "open"
            return_date = return_date or "-"
            borg_status = borg_status or "open"

            # ==== status badge ====
            badge_color = "#555555"
            if status == "uitgegeven":
                badge_color = "#2a4d8f"
            elif status == "afgerond":
                badge_color = "#2f8f46"

            status_lbl = ctk.CTkLabel(
                self.table_frame,
                text=status,
                fg_color=badge_color,
                corner_radius=6,
                padx=8,
                pady=3
            )
            status_lbl.grid(row=row_index, column=0, padx=10, pady=6)

            # ==== basisvelden ====
            ctk.CTkLabel(self.table_frame, text=str(reservation_id)).grid(row=row_index, column=1, padx=10, pady=6)
            ctk.CTkLabel(self.table_frame, text=name).grid(row=row_index, column=2, padx=10, pady=6)
            ctk.CTkLabel(self.table_frame, text=email).grid(row=row_index, column=3, padx=10, pady=6)
            ctk.CTkLabel(self.table_frame, text=start_date).grid(row=row_index, column=4, padx=10, pady=6)
            ctk.CTkLabel(self.table_frame, text=end_date).grid(row=row_index, column=5, padx=10, pady=6)
            ctk.CTkLabel(self.table_frame, text=bike_type).grid(row=row_index, column=6, padx=10, pady=6)

            # ==== accessoires wrapped ====
            acc_text = self.wrap_text(accessories, max_chars=28)
            ctk.CTkLabel(self.table_frame, text=acc_text, justify="left").grid(row=row_index, column=7, padx=10, pady=6)

            # ==== prijs & borg ====
            ctk.CTkLabel(self.table_frame, text=f"€{total_price:.2f}").grid(row=row_index, column=8, padx=10, pady=6)
            ctk.CTkLabel(self.table_frame, text=f"€{borg:.2f}").grid(row=row_index, column=9, padx=10, pady=6)

            # ==== teruggavedatum ====
            ctk.CTkLabel(self.table_frame, text=return_date).grid(row=row_index, column=10, padx=10, pady=6)

            # ==== borg status ====
            borg_color = "#777777"  # open
            if borg_status == "betaald":
                borg_color = "#2a4d8f"
            elif borg_status == "teruggegeven":
                borg_color = "#2f8f46"

            borg_lbl = ctk.CTkLabel(
                self.table_frame,
                text=borg_status,
                fg_color=borg_color,
                corner_radius=6,
                padx=8,
                pady=3
            )
            borg_lbl.grid(row=row_index, column=11, padx=10, pady=6)

            # ==== acties ====
            action_frame = ctk.CTkFrame(self.table_frame, fg_color="transparent")
            action_frame.grid(row=row_index, column=12, padx=10, pady=6)

            # ==== bekijken ====
            ctk.CTkButton(
                action_frame, text="Bekijken", width=80,
                command=lambda rid=reservation_id: self.view_popup(rid)
            ).pack(side="left", padx=3)

            # ==== uitgeven ====
            ctk.CTkButton(
                action_frame, text="Uitgeven", width=80,
                command=lambda rid=reservation_id: self.set_status_issued(rid)
            ).pack(side="left", padx=3)

            # ==== afronden ====
            ctk.CTkButton(
                action_frame, text="Afronden", width=80,
                command=lambda rid=reservation_id: self.complete_reservation_popup(rid)
            ).pack(side="left", padx=3)

            # ==== borg knoppen ====
            if borg_status == "open":
                ctk.CTkButton(
                    action_frame,
                    text="Borg betaald",
                    width=110,
                    fg_color="#2a4d8f",
                    command=lambda rid=reservation_id: self.set_borg_status(rid, "betaald")
                ).pack(side="left", padx=3)

            if borg_status == "betaald":
                ctk.CTkButton(
                    action_frame,
                    text="Borg terug",
                    width=110,
                    fg_color="#2f8f46",
                    command=lambda rid=reservation_id: self.set_borg_status(rid, "teruggegeven")
                ).pack(side="left", padx=3)

            # ===== verwijderen ====
            ctk.CTkButton(
                action_frame, text="Verwijderen", width=100, fg_color="#8b0000",
                command=lambda rid=reservation_id: self.confirm_delete(rid)
            ).pack(side="left", padx=3)

    # ==== wrap accessories text ====
    def wrap_text(self, text, max_chars=28):
        if not text:
            return "Geen"

        words = text.split()
        lines = []
        current = ""

        for word in words:
            if len(current + " " + word) <= max_chars:
                current = (current + " " + word).strip()
            else:
                lines.append(current)
                current = word

        if current:
            lines.append(current)

        return "\n".join(lines[:2])

    # ==== Bekijk reservatie (breid uit later) ====
    def view_popup(self, reservation_id):
        data = self.app.db.get_reservation(reservation_id)
        if not data:
            messagebox.showerror("Fout", "Reservering niet gevonden.")
            return

        popup = ctk.CTkToplevel(self)
        popup.title("Reservering details")
        popup.geometry("500x650")

        labels = [
            ("ID", data[0]),
            ("Naam", data[1]),
            ("E-mail", data[2]),
            ("Startdatum", data[3]),
            ("Einddatum", data[4]),
            ("Fiets", data[5]),
            ("Accessoires", data[6]),
            ("Opmerking", data[7] if data[7] else "Geen"),
            ("Totaalprijs", f"€{data[8]:.2f}"),
            ("Borg", f"€{data[9]:.2f}"),
            ("Status", data[10] or "open"),
            ("Teruggavedatum", data[11] or "-"),
        ]

        for label, value in labels:
            lbl = ctk.CTkLabel(
                popup,
                text=f"{label}: {value}",
                font=ctk.CTkFont(size=14)
            )
            lbl.pack(anchor="w", padx=20, pady=6)


    # ==== status uitgeven ====

    def set_status_issued(self, reservation_id):
        self.app.db.update_reservation_status(reservation_id, "uitgegeven")
        self.load_reservations()


    # ==== popup: afronden met teruggavedatum (AI geholpen) ====

    def complete_reservation_popup(self, reservation_id):
        popup = ctk.CTkToplevel(self)
        popup.title("Reservering afronden")
        popup.geometry("350x180")

        lbl = ctk.CTkLabel(
            popup,
            text="Voer de teruggavedatum in (dd-mm-jjjj):"
        )
        lbl.pack(pady=15)

        date_entry = ctk.CTkEntry(popup, width=180)
        date_entry.pack(pady=5)

        btn_frame = ctk.CTkFrame(popup, fg_color="transparent")
        btn_frame.pack(pady=10)

        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Annuleren",
            width=90,
            command=popup.destroy
        )
        cancel_btn.pack(side="left", padx=5)

        def on_confirm():
            return_date = date_entry.get().strip()
            if not return_date:
                messagebox.showerror("Fout", "Teruggavedatum mag niet leeg zijn.")
                return
            # geen strenge datum validatie (optie a)
            self.app.db.complete_reservation(reservation_id, return_date)
            popup.destroy()
            self.load_reservations()

        confirm_btn = ctk.CTkButton(
            btn_frame,
            text="Opslaan",
            width=90,
            command=on_confirm
        )
        confirm_btn.pack(side="left", padx=5)

    # ==== popup delete ====
    def confirm_delete(self, reservation_id):
        popup = ctk.CTkToplevel(self)
        popup.title("Bevestigen")
        popup.geometry("300x150")

        lbl = ctk.CTkLabel(
            popup,
            text="Weet u zeker dat u deze reservering wilt verwijderen?"
        )
        lbl.pack(pady=20)

        btn_frame = ctk.CTkFrame(popup, fg_color="transparent")
        btn_frame.pack()

        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Nee",
            width=80,
            command=popup.destroy
        )
        cancel_btn.pack(side="left", padx=10)

        yes_btn = ctk.CTkButton(
            btn_frame,
            text="Ja, verwijderen",
            width=120,
            fg_color="#8b0000",
            command=lambda: self.delete_reservation(reservation_id, popup)
        )
        yes_btn.pack(side="left", padx=10)


    # ==== delete reservatie ====

    def delete_reservation(self, reservation_id, popup):
        self.app.db.delete_reservation(reservation_id)
        popup.destroy()
        self.load_reservations()


    # ==== borg status ====
    def set_borg_status(self, reservation_id, new_status):
        self.app.db.update_borg_status(reservation_id, new_status)
        self.load_reservations()

    # ==== BROER FIX: auto-refresh wanneer pagina geopend ====
    def on_show(self):
        self.load_reservations()
