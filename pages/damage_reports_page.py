import customtkinter as ctk
from pages.portal_header import PortalHeader
from tkinter import messagebox


class DamageReportsPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # ==== header ====
        header = PortalHeader(self, app, "Schademeldingen")
        header.pack(fill="x")

        # ==== content frame (AI gemaakt)====
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # ==== titel ====
        title_label = ctk.CTkLabel(
            content_frame,
            text="Overzicht Schademeldingen",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(0, 15))

        # ==== searchbar ====
        search_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        search_frame.pack(pady=(0, 15))

        self.search_entry = ctk.CTkEntry(
            search_frame,
            width=300,
            placeholder_text="Zoek op naam, e-mail of schade..."
        )
        self.search_entry.pack(side="left", padx=5)

        search_btn = ctk.CTkButton(
            search_frame,
            text="Zoeken",
            width=100,
            command=self.search_reports
        )
        search_btn.pack(side="left", padx=5)

        reset_btn = ctk.CTkButton(
            search_frame,
            text="Refresh",
            width=100,
            command=self.load_reports
        )
        reset_btn.pack(side="left", padx=5)

        # ==== melding toevoegen ====
        add_btn = ctk.CTkButton(
            content_frame,
            text="Melding toevoegen",
            width=150,
            command=lambda: self.app.show_page("DamagePage")
        )
        add_btn.pack(pady=(0, 15))

        # ==== table ====
        self.table_frame = ctk.CTkScrollableFrame(
            content_frame,
            width=1100,
            height=450,
            fg_color="#1E1E1E"
        )
        self.table_frame.pack(fill="both", expand=True)

        # ==== header titels ====
        headers = [
            "Status", "ID", "Naam", "E-mail",
            "Fiets", "Schade", "Acties"
        ]

        for idx, title in enumerate(headers):
            lbl = ctk.CTkLabel(
                self.table_frame,
                text=title,
                font=ctk.CTkFont(size=14, weight="bold")
            )
            lbl.grid(row=0, column=idx, padx=10, pady=10)

        self.load_reports()

    # ==== load/search ====
    def load_reports(self):
        self.populate_table(self.app.db.get_all_damage_reports())

    def search_reports(self):
        keyword = self.search_entry.get().strip()
        if keyword == "":
            self.load_reports()
        else:
            results = self.app.db.search_damage_reports(keyword)
            self.populate_table(results)

    # ==== populate table (AI gemaakt)====
    def populate_table(self, data):
        for widget in self.table_frame.winfo_children():
            if widget.grid_info()["row"] != 0:
                widget.destroy()

        if not data:
            lbl = ctk.CTkLabel(
                self.table_frame,
                text="Geen schademeldingen gevonden."
            )
            lbl.grid(row=1, column=0, columnspan=7, pady=20)
            return

        for row_index, row in enumerate(data, start=1):
            (
                report_id,
                name,
                email,
                bike_type,
                damages,
                created_at,
                status
            ) = row

            status = status or "wacht"

            # ==== status ====
            color = "#777777"   # wacht
            if status == "reparatie":
                color = "#2a4d8f"
            elif status == "gerepareerd":
                color = "#2f8f46"

            status_lbl = ctk.CTkLabel(
                self.table_frame,
                text=status,
                fg_color=color,
                corner_radius=6,
                padx=8,
                pady=4
            )
            status_lbl.grid(row=row_index, column=0, padx=10, pady=6)

            # ==== inputvelden ====
            values = [
                report_id,
                name,
                email,
                bike_type
            ]

            for col_index, cell in enumerate(values, start=1):
                lbl = ctk.CTkLabel(self.table_frame, text=str(cell))
                lbl.grid(row=row_index, column=col_index, padx=10, pady=6, sticky="w")

            # ==== schade tekst ====
            damage_text = self.wrap_damage_text(damages)
            damage_lbl = ctk.CTkLabel(
                self.table_frame,
                text=damage_text,
                justify="left"
            )
            damage_lbl.grid(row=row_index, column=5, padx=10, pady=6, sticky="w")

            # ==== acties ====
            action_frame = ctk.CTkFrame(self.table_frame, fg_color="transparent")
            action_frame.grid(row=row_index, column=6, padx=10, pady=6)

            # === bekijken ====
            view_btn = ctk.CTkButton(
                action_frame,
                text="Bekijken",
                width=80,
                command=lambda rid=report_id: self.view_popup(rid)
            )
            view_btn.pack(side="left", padx=5)

            # ==== verwijderen ====
            delete_btn = ctk.CTkButton(
                action_frame,
                text="Verwijderen",
                width=100,
                fg_color="#8b0000",
                command=lambda rid=report_id: self.confirm_delete(rid)
            )
            delete_btn.pack(side="left", padx=5)

            # ==== reparatie-knop ====
            if status == "wacht":
                rep_btn = ctk.CTkButton(
                    action_frame,
                    text="Reparatie",
                    width=100,
                    fg_color="#2a4d8f",
                    command=lambda rid=report_id: self.mark_for_repair(rid)
                )
                rep_btn.pack(side="left", padx=5)

    # ==== wrap schade tekst (max 2 regels) ====
    def wrap_damage_text(self, text, max_chars=32):
        if not text:
            return "-"

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

    # ==== reperatie maken ding ====
    def mark_for_repair(self, report_id):
        self.app.db.update_damage_status(report_id, "reparatie")
        self.load_reports()

    # ==== error popup ====
    def view_popup(self, report_id):
        data = self.app.db.get_damage_report(report_id)
        if not data:
            messagebox.showerror("Fout", "Schademelding niet gevonden.")
            return

        popup = ctk.CTkToplevel(self)
        popup.title("Schade Details")
        popup.geometry("450x500")

        labels = [
            ("ID", data[0]),
            ("Naam", data[1]),
            ("E-mail", data[2]),
            ("Fiets", data[3]),
            ("Schade", data[4]),
            ("Datum", data[5]),
            ("Status", data[6])
        ]

        for text, value in labels:
            lbl = ctk.CTkLabel(
                popup,
                text=f"{text}: {value}",
                font=ctk.CTkFont(size=14)
            )
            lbl.pack(anchor="w", padx=20, pady=8)

    # ==== delete ====
    def confirm_delete(self, report_id):
        popup = ctk.CTkToplevel(self)
        popup.title("Bevestigen")
        popup.geometry("300x150")

        lbl = ctk.CTkLabel(
            popup,
            text="Weet u zeker dat je deze melding wil verwijderen?"
        )
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

    # ==== BROER FIX: auto-refresh wanneer pagina geopend ====
    def on_show(self):
        self.load_reports()
