import customtkinter as ctk
from pages.portal_header import PortalHeader
from tkinter import messagebox


class DamageReportsPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # ===== HEADER =====
        header = PortalHeader(self, app, "Schademeldingen")
        header.pack(fill="x")

        # ===== CONTENT FRAME =====
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        title_label = ctk.CTkLabel(
            content_frame,
            text="Overzicht Schademeldingen",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(0, 20))

        # ===== SEARCH BAR =====
        search_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        search_frame.pack(pady=(0, 20))

        self.search_entry = ctk.CTkEntry(search_frame, width=300, placeholder_text="Zoek op naam, e-mail of schade...")
        self.search_entry.pack(side="left", padx=5)

        search_btn = ctk.CTkButton(search_frame, text="Zoeken", width=100, command=self.search_reports)
        search_btn.pack(side="left", padx=5)

        reset_btn = ctk.CTkButton(search_frame, text="Reset", width=80, command=self.load_reports)
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
            "Status", "ID", "Naam", "E-mail",
            "Fiets", "Schade", "Datum", "Acties"
        ]

        for idx, text in enumerate(headers):
            lbl = ctk.CTkLabel(
                self.table_frame,
                text=text,
                font=ctk.CTkFont(size=14, weight="bold")
            )
            lbl.grid(row=0, column=idx, padx=10, pady=10)

        # Initial load
        self.load_reports()

    # ==========================================================
    #     LOAD / SEARCH DATA
    # ==========================================================
    def load_reports(self):
        self.populate_table(self.app.db.get_all_damage_reports())

    def search_reports(self):
        keyword = self.search_entry.get().strip()
        if keyword == "":
            self.load_reports()
        else:
            results = self.app.db.search_damage_reports(keyword)
            self.populate_table(results)

    # ==========================================================
    #         TABLE POPULATION
    # ==========================================================
    def populate_table(self, data):
        # Eerst bestaande rijen verwijderen behalve de headers
        for widget in self.table_frame.winfo_children():
            info = widget.grid_info()
            if info["row"] != 0:
                widget.destroy()

        # Als er geen data is
        if not data:
            lbl = ctk.CTkLabel(self.table_frame, text="Geen schademeldingen gevonden.")
            lbl.grid(row=1, column=0, pady=20, columnspan=8)
            return

        # Elke rij in de tabel plaatsen
        for row_index, row in enumerate(data, start=1):
            report_id = row[0]
            name = row[1]
            email = row[2]
            bike = row[3]
            damages = row[4]
            created_at = row[5]
            status = row[6]  # nieuw veld

            # ===== STATUS BADGE =====
            color = "#777777"  # wacht
            if status == "reparatie":
                color = "#e67e22"  # oranje
            elif status == "gerepareerd":
                color = "#27ae60"  # groen

            status_label = ctk.CTkLabel(
                self.table_frame,
                text=status.capitalize(),
                fg_color=color,
                corner_radius=6,
                text_color="black" if status == "gerepareerd" else "white",
                padx=10,
                pady=4
            )
            status_label.grid(row=row_index, column=0, padx=10, pady=8)

            # ===== VELDEN TONEN =====

            columns = [
                report_id, name, email, bike, damages, created_at
            ]

            for col_index, cell in enumerate(columns, start=1):

                # Schade-kolom (wrap)
                if col_index == 5:
                    lbl = ctk.CTkLabel(
                        self.table_frame,
                        text=str(cell),
                        justify="left",
                        wraplength=250,
                        anchor="w"
                    )
                else:
                    lbl = ctk.CTkLabel(
                        self.table_frame,
                        text=str(cell),
                        anchor="w"
                    )

                lbl.grid(row=row_index, column=col_index, padx=10, pady=8, sticky="w")

            # ===== ACTIE KNOPPEN =====
            action_frame = ctk.CTkFrame(self.table_frame, fg_color="transparent")
            action_frame.grid(row=row_index, column=7, padx=10, pady=8)

            # Bekijken
            view_btn = ctk.CTkButton(
                action_frame,
                text="Bekijken",
                width=80,
                command=lambda rid=report_id: self.view_popup(rid)
            )
            view_btn.pack(side="left", padx=5)

            # Verwijderen
            del_btn = ctk.CTkButton(
                action_frame,
                text="Verwijderen",
                width=100,
                fg_color="#8b0000",
                command=lambda rid=report_id: self.confirm_delete(rid)
            )
            del_btn.pack(side="left", padx=5)

            # → Reparatie knop (alleen tonen als status != gerepareerd)
            if status != "gerepareerd":
                repair_btn = ctk.CTkButton(
                    action_frame,
                    text="→ Reparatie",
                    width=100,
                    fg_color="#e67e22",
                    command=lambda rid=report_id: self.mark_for_repair(rid)
                )
                repair_btn.pack(side="left", padx=5)

    def mark_for_repair(self, report_id):
        self.app.db.update_damage_status(report_id, "reparatie")
        self.load_reports()

    # ==========================================================
    #         VIEW POPUP
    # ==========================================================
    def view_popup(self, report_id):
        data = self.app.db.get_damage_report(report_id)
        if not data:
            messagebox.showerror("Fout", "Schademelding niet gevonden.")
            return

        popup = ctk.CTkToplevel(self)
        popup.title("Schade Details")
        popup.geometry("450x500")

        fields = [
            ("ID", data[0]),
            ("Naam", data[1]),
            ("E-mail", data[2]),
            ("Type fiets", data[3]),
            ("Schade", data[4]),
            ("Datum", data[5])
        ]

        for label, value in fields:
            lbl = ctk.CTkLabel(popup, text=f"{label}: {value}", font=ctk.CTkFont(size=14))
            lbl.pack(pady=10, anchor="w", padx=20)

    # ==========================================================
    #         DELETE CONFIRMATION
    # ==========================================================
    def confirm_delete(self, report_id):
        popup = ctk.CTkToplevel(self)
        popup.title("Bevestigen")
        popup.geometry("300x150")

        lbl = ctk.CTkLabel(popup, text="Weet u zeker dat u deze melding wilt verwijderen?")
        lbl.pack(pady=20)

        btn_frame = ctk.CTkFrame(popup, fg_color="transparent")
        btn_frame.pack()

        cancel_btn = ctk.CTkButton(btn_frame, text="Nee", width=80, command=popup.destroy)
        cancel_btn.pack(side="left", padx=10)

        yes_btn = ctk.CTkButton(
            btn_frame,
            text="Ja, verwijderen",
            width=120,
            fg_color="#8b0000",
            command=lambda: self.delete_report(report_id, popup)
        )
        yes_btn.pack(side="left", padx=10)

    def delete_report(self, report_id, popup):
        self.app.db.delete_damage_report(report_id)
        popup.destroy()
        self.load_reports()
