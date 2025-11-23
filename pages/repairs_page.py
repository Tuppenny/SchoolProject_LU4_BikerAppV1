import customtkinter as ctk
from pages.portal_header import PortalHeader
from tkinter import messagebox


class RepairsPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # ===== header titel =====
        header = PortalHeader(self, app, "Reparaties")
        header.pack(fill="x")

        # ===== content frame (AI gemaakt) =====
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        title_label = ctk.CTkLabel(
            content_frame,
            text="Reparatie-overzicht",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(0, 20))

        top_bar = ctk.CTkFrame(content_frame, fg_color="transparent")
        top_bar.pack(pady=(0, 15))

        # ==== zoekveld ====
        self.search_entry = ctk.CTkEntry(
            top_bar,
            width=300,
            placeholder_text="Zoek op naam, fiets of schade"
        )
        self.search_entry.pack(side="left", padx=5)

        # ==== zoekknop ====
        search_btn = ctk.CTkButton(
            top_bar,
            text="Zoeken",
            width=100,
            command=self.search_repairs
        )
        search_btn.pack(side="left", padx=5)

        # ==== refresh knop ====
        refresh_btn = ctk.CTkButton(
            top_bar,
            text="Refresh",
            width=90,
            command=self.load_repairs
        )
        refresh_btn.pack(side="left", padx=5)

        # ===== table frame (AI gemaakt) =====
        self.table_frame = ctk.CTkScrollableFrame(
            content_frame,
            width=950,
            height=500,
            fg_color="#1E1E1E"
        )
        self.table_frame.pack(fill="both", expand=True)

        # ==== Tabeltitels ====
        headers = [
            "Status", "ID", "Naam", "E-mail",
            "Fiets", "Schade", "Datum", "Acties"
        ]

        for idx, text in enumerate(headers):
            lbl = ctk.CTkLabel(
                self.table_frame,
                text=text,
                font=ctk.CTkFont(size=14, weight="bold"),
            )
            lbl.grid(row=0, column=idx, padx=10, pady=10)

        # ==== initial load ====
        self.load_repairs()

    # ==== reparaties laden ====
    def load_repairs(self):
        data = self.app.db.get_open_repairs()
        self.populate_table(data)


    # ==== table vullen (AI gemaakt)====
    def populate_table(self, data):
        # Oude rijen verwijderen behalve headers
        for widget in self.table_frame.winfo_children():
            info = widget.grid_info()
            if info["row"] != 0:
                widget.destroy()

        if not data:
            lbl = ctk.CTkLabel(self.table_frame, text="Geen open reparaties.")
            lbl.grid(row=1, column=0, pady=20, columnspan=8)
            return

        for row_index, row in enumerate(data, start=1):
            report_id = row[0]
            name = row[1]
            email = row[2]
            bike = row[3]
            damages = row[4]
            created_at = row[5]
            status = row[6]

            # ===== status =====
            color = "#777777"  # wacht
            if status == "reparatie":
                color = "#e67e22"
            elif status == "gerepareerd":
                color = "#27ae60"

            status_label = ctk.CTkLabel(
                self.table_frame,
                text=status.capitalize(),
                fg_color=color,
                corner_radius=6,
                text_color="white",
                padx=10,
                pady=4
            )
            status_label.grid(row=row_index, column=0, padx=10, pady=8)

            # ===== data cells (AI gemaakt) =====
            columns = [
                report_id, name, email, bike, damages, created_at
            ]

            for col_index, cell in enumerate(columns, start=1):

                # ==== Schade kolom wrappen ====
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

            # ===== actie knoppen\ =====
            action_frame = ctk.CTkFrame(self.table_frame, fg_color="transparent")
            action_frame.grid(row=row_index, column=7, padx=10, pady=8)

            # ==== bekjken ====
            view_btn = ctk.CTkButton(
                action_frame,
                text="Bekijken",
                width=80,
                command=lambda rid=report_id: self.view_popup(rid)
            )
            view_btn.pack(side="left", padx=5)

            # ==== start reparatie ====
            if status == "wacht":
                rep_btn = ctk.CTkButton(
                    action_frame,
                    text="Start reparatie",
                    width=130,
                    fg_color="#e67e22",
                    command=lambda rid=report_id: self.set_status(rid, "reparatie")
                )
                rep_btn.pack(side="left", padx=5)

            # ==== gerepareerd ====
            if status == "reparatie":
                done_btn = ctk.CTkButton(
                    action_frame,
                    text="Gerepareerd",
                    width=130,
                    fg_color="#27ae60",
                    command=lambda rid=report_id: self.set_status(rid, "gerepareerd")
                )
                done_btn.pack(side="left", padx=5)

    # ==== update status ====

    def set_status(self, report_id, new_status):
        self.app.db.update_damage_status(report_id, new_status)
        self.load_repairs()

    # ==== popup ding ====
    def view_popup(self, report_id):
        data = self.app.db.get_damage_report(report_id)
        if not data:
            messagebox.showerror("Fout", "Schade niet gevonden.")
            return

        popup = ctk.CTkToplevel(self)
        popup.title("Reparatie Details")
        popup.geometry("500x500")

        fields = [
            ("ID", data[0]),
            ("Naam", data[1]),
            ("E-mail", data[2]),
            ("Fiets", data[3]),
            ("Schade", data[4]),
            ("Melding gedaan op", data[5]),
            ("Status", data[6]),
        ]

        for label, value in fields:
            lbl = ctk.CTkLabel(popup, text=f"{label}: {value}", font=ctk.CTkFont(size=14))
            lbl.pack(pady=10, anchor="w", padx=20)


    # ==== searchbar ====

    def search_repairs(self):
        keyword = self.search_entry.get().strip()
        if keyword == "":
            self.load_repairs()
            return

        results = self.app.db.search_damage_reports(keyword)
        self.populate_table(results)
