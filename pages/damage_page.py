import customtkinter as ctk
from tkinter import messagebox
from pages.portal_header import PortalHeader


class DamagePage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # ===== header =====
        header = PortalHeader(self, app, "Schademelding toevoegen")
        header.pack(fill="x")

        # ===== inner container =====
        self.inner_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.inner_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # ===== titel =====
        title_label = ctk.CTkLabel(
            self.inner_frame,
            text="Schade melden",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(10, 10))

        # ===== formulier links =====
        form_frame = ctk.CTkFrame(self.inner_frame, corner_radius=10)
        form_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 20), pady=10)

        form_inner = ctk.CTkFrame(form_frame, fg_color="transparent")
        form_inner.pack(padx=20, pady=20, fill="x")

        # naam
        ctk.CTkLabel(form_inner, text="Naam klant:").grid(row=0, column=0, sticky="e", padx=10, pady=5)
        self.name_entry = ctk.CTkEntry(form_inner, width=260)
        self.name_entry.grid(row=0, column=1, sticky="w", padx=10, pady=5)

        # e-mail
        ctk.CTkLabel(form_inner, text="E-mailadres:").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.email_entry = ctk.CTkEntry(form_inner, width=260)
        self.email_entry.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        # type fiets
        ctk.CTkLabel(form_inner, text="Type fiets:").grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.bike_type_var = ctk.StringVar(value="Herenfiets")
        self.bike_menu = ctk.CTkOptionMenu(
            form_inner,
            values=["Herenfiets", "Damesfiets", "E-bike"],
            variable=self.bike_type_var,
            width=260
        )
        self.bike_menu.grid(row=2, column=1, sticky="w", padx=10, pady=5)

        # schade opties
        ctk.CTkLabel(form_inner, text="Schade type:").grid(row=3, column=0, sticky="ne", padx=10, pady=5)

        self.damage_flat_var = ctk.BooleanVar()
        self.damage_light_var = ctk.BooleanVar()
        self.damage_wheel_var = ctk.BooleanVar()
        self.damage_collision_var = ctk.BooleanVar()
        self.damage_other_var = ctk.BooleanVar()

        ctk.CTkCheckBox(form_inner, text="Lekke band", variable=self.damage_flat_var)\
            .grid(row=3, column=1, sticky="w", padx=10, pady=2)

        ctk.CTkCheckBox(form_inner, text="Kapot licht", variable=self.damage_light_var)\
            .grid(row=4, column=1, sticky="w", padx=10, pady=2)

        ctk.CTkCheckBox(form_inner, text="Slag in wiel", variable=self.damage_wheel_var)\
            .grid(row=5, column=1, sticky="w", padx=10, pady=2)

        ctk.CTkCheckBox(form_inner, text="Botsing schade", variable=self.damage_collision_var)\
            .grid(row=6, column=1, sticky="w", padx=10, pady=2)

        ctk.CTkCheckBox(form_inner, text="Anders", variable=self.damage_other_var)\
            .grid(row=7, column=1, sticky="w", padx=10, pady=2)

        # “Anders” beschrijving
        ctk.CTkLabel(form_inner, text="Beschrijving (indien anders):")\
            .grid(row=8, column=0, sticky="ne", padx=10, pady=5)
        self.other_text = ctk.CTkTextbox(form_inner, width=260, height=80)
        self.other_text.grid(row=8, column=1, sticky="w", padx=10, pady=5)

        # opslaan-knop
        submit_button = ctk.CTkButton(
            self.inner_frame,
            text="Schademelding opslaan",
            width=200,
            command=self.save_damage
        )
        submit_button.grid(row=2, column=0, sticky="w", pady=10)

        # layout
        self.inner_frame.grid_columnconfigure(0, weight=1)
        self.inner_frame.grid_columnconfigure(1, weight=1)

    # ===== schade opslaan =====
    def save_damage(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        bike_type = self.bike_type_var.get()

        if not name or not email:
            messagebox.showerror("Fout", "Naam en e-mail zijn verplicht.")
            return

        damages = []
        if self.damage_flat_var.get():
            damages.append("Lekke band")
        if self.damage_light_var.get():
            damages.append("Kapot licht")
        if self.damage_wheel_var.get():
            damages.append("Slag in wiel")
        if self.damage_collision_var.get():
            damages.append("Botsingschade")
        if self.damage_other_var.get():
            damages.append("Andere schade: " + self.other_text.get("1.0", "end").strip())

        if not damages:
            messagebox.showerror("Fout", "Selecteer minstens één schadeoptie.")
            return

        damages_str = ", ".join(damages)

        # opslaan in database
        self.app.db.add_damage_report(
            name=name,
            email=email,
            bike_type=bike_type,
            damages=damages_str
        )

        messagebox.showinfo("Succes", "Schade succesvol opgeslagen.")

        # terug naar schadeoverzicht
        self.app.show_page("DamageReportsPage")

        # velden resetten
        self.name_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.other_text.delete("1.0", "end")
        self.damage_flat_var.set(False)
        self.damage_light_var.set(False)
        self.damage_wheel_var.set(False)
        self.damage_collision_var.set(False)
        self.damage_other_var.set(False)
