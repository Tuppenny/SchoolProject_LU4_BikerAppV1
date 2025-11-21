import customtkinter as ctk
from pages.portal_header import PortalHeader
from tkinter import messagebox


class ReservationsPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # ===== HEADER =====
        header = PortalHeader(self, app, "Reserveringen")
        header.pack(fill="x")

        # ===== CONTENT FRAME =====
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # ===== TITLE =====
        title_label = ctk.CTkLabel(
            content_frame,
            text="Reserveringen Overzicht",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(0, 20))

        # ===== SEARCH BAR =====
        search_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        search_frame.pack(pady=(0, 20))

        self.search_entry = ctk.CTkEntry(search_frame, width=300, placeholder_text="Zoek op naam of e-mail...")
        self.search_entry.pack(side="left", padx=5)

        search_btn = ctk.CTkButton(search_frame, text="Zoeken", width=100, command=self.search_reservations)
        search_btn.pack(side="left", padx=5)

        reset_btn = ctk.CTkButton(search_frame, text="Reset", width=80, command=self.load_reservations)
        reset_btn.pack(side="left", padx=5)

        # ===== TABLE FRAME =====
        self.table_frame = ctk.CTkScrollableFrame(
            content_frame,
            width=950,
            height=450,
            fg_color="#1E1E1E"
        )
        self.table_frame.pack(fill="both", expand=True)

        # TABLE HEADERS
        headers = [
            "ID", "Naam", "E-mail",
            "Start", "Einde",
            "Fiets", "Accessoires", "Acties"
        ]

        for idx, text in enumerate(headers):
            lbl = ctk.CTkLabel(
                self.table_frame,
                text=text,
                font=ctk.CTkFont(size=14, weight="bold")
            )
            lbl.grid(row=0, column=idx, padx=10, pady=10)

        # Load data
        self.load_reservations()

    # ==========================================================
    #     LOAD / SEARCH DATA
    # ==========================================================
    def load_reservations(self):
        self.populate_table(self.app.db.get_all_reservations())

    def search_reservations(self):
        keyword = self.search_entry.get().strip()
        if keyword == "":
            self.load_reservations()
        else:
            results = self.app.db.search_reservations(keyword)
            self.populate_table(results)

    # ==========================================================
    #     POPULATE TABLE
    # ==========================================================
    def populate_table(self, data):
        # Clear old rows
        for widget in self.table_frame.winfo_children():
            info = widget.grid_info()
            if info["row"] != 0:
                widget.destroy()

        # No data
        if not data:
            lbl = ctk.CTkLabel(self.table_frame, text="Geen reserveringen gevonden.")
            lbl.grid(row=1, column=0, pady=20, columnspan=8)
            return

        # Populate table
        for row_index, row in enumerate(data, start=1):
            reservation_id = row[0]

            # Render reservation fields
            for col_index, cell in enumerate(row[:-1]):  # Last one is comment, skip for now
                lbl = ctk.CTkLabel(self.table_frame, text=str(cell))
                lbl.grid(row=row_index, column=col_index, padx=10, pady=8)

            # ACTION BUTTONS
            action_frame = ctk.CTkFrame(self.table_frame, fg_color="transparent")
            action_frame.grid(row=row_index, column=7, padx=10, pady=8)

            # View button
            view_btn = ctk.CTkButton(
                action_frame,
                text="Bekijken",
                width=80,
                command=lambda rid=reservation_id: self.view_popup(rid)
            )
            view_btn.pack(side="left", padx=5)

            # Delete button
            del_btn = ctk.CTkButton(
                action_frame,
                text="Verwijderen",
                width=100,
                fg_color="#8b0000",
                command=lambda rid=reservation_id: self.confirm_delete(rid)
            )
            del_btn.pack(side="left", padx=5)

    # ==========================================================
    #     POPUP: BEKIJK DETAILS
    # ==========================================================
    def view_popup(self, reservation_id):
        data = self.app.db.get_reservation(reservation_id)
        if not data:
            messagebox.showerror("Fout", "Reservering niet gevonden.")
            return

        popup = ctk.CTkToplevel(self)
        popup.title("Reservering Details")
        popup.geometry("450x500")

        fields = [
            ("ID", data[0]),
            ("Naam", data[1]),
            ("E-mail", data[2]),
            ("Startdatum", data[3]),
            ("Einddatum", data[4]),
            ("Fiets", data[5]),
            ("Accessoires", data[6]),
            ("Opmerking", data[7] if data[7] else "Geen")
        ]

        for label, value in fields:
            lbl = ctk.CTkLabel(popup, text=f"{label}: {value}", font=ctk.CTkFont(size=14))
            lbl.pack(pady=10, anchor="w", padx=20)

    # ==========================================================
    #     POPUP: DELETE CONFIRMATION
    # ==========================================================
    def confirm_delete(self, reservation_id):
        popup = ctk.CTkToplevel(self)
        popup.title("Bevestigen")
        popup.geometry("300x150")

        lbl = ctk.CTkLabel(popup, text="Weet u zeker dat u deze reservering wilt verwijderen?")
        lbl.pack(pady=20)

        # Buttons
        btn_frame = ctk.CTkFrame(popup, fg_color="transparent")
        btn_frame.pack()

        cancel_btn = ctk.CTkButton(btn_frame, text="Nee", width=80, command=popup.destroy)
        cancel_btn.pack(side="left", padx=10)

        yes_btn = ctk.CTkButton(
            btn_frame,
            text="Ja, verwijderen",
            width=120,
            fg_color="#8b0000",
            command=lambda: self.delete_reservation(reservation_id, popup)
        )
        yes_btn.pack(side="left", padx=10)

    def delete_reservation(self, reservation_id, popup):
        self.app.db.delete_reservation(reservation_id)
        popup.destroy()
        self.load_reservations()
