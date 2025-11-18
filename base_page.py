import customtkinter as ctk

class BasePage(ctk.CTkFrame):
    def __init__(self, parent, app, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.app = app

        # ----------- TOP NAV BAR -----------
        nav_bar = ctk.CTkFrame(
            self,
            height=60,
            fg_color="#2E2E2E"
        )
        nav_bar.pack(fill="x")

        shadow = ctk.CTkFrame(self, height=2, fg_color="#1E1E1E")
        shadow.pack(fill="x")

        # Logo
        logo_label = ctk.CTkLabel(
            nav_bar,
            text="Biker Haaglanden",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        logo_label.pack(side="left", padx=20, pady=10)

        staff_button = ctk.CTkButton(
            nav_bar,
            text="Medewerkerportaal",
            width=160,
            command=lambda: app.show_page("StaffLoginPage")
        )
        staff_button.pack(side="right", padx=20, pady=10)

        # ----------- HEADER MENU BAR ----------
        header_bar = ctk.CTkFrame(self, height=45, fg_color="#252525")
        header_bar.pack(fill="x")

        nav_container = ctk.CTkFrame(header_bar, fg_color="transparent")
        nav_container.pack(side="right", padx=30, pady=5)

        # ----- Helper functies -----
        def make_nav_item(text, page=None):
            label = ctk.CTkLabel(
                nav_container,
                text=text,
                font=ctk.CTkFont(size=16),
                text_color="white",
                cursor="hand2"
            )

            # Hover underline
            def on_enter(e):
                label.configure(font=ctk.CTkFont(size=16, underline=True))

            def on_leave(e):
                label.configure(font=ctk.CTkFont(size=16, underline=False))

            label.bind("<Enter>", on_enter)
            label.bind("<Leave>", on_leave)

            # Navigation
            if page:
                label.bind("<Button-1>", lambda e: app.show_page(page))

            return label

        # ----- Menu items -----
        home_btn = make_nav_item("Home", "HomePage")
        home_btn.pack(side="left", padx=12)

        div1 = ctk.CTkFrame(nav_container, width=2, height=20, fg_color="#444444")
        div1.pack(side="left", padx=12)

        reserve_btn = make_nav_item("Reserveren", "ReservationPage")
        reserve_btn.pack(side="left", padx=12)

        div2 = ctk.CTkFrame(nav_container, width=2, height=20, fg_color="#444444")
        div2.pack(side="left", padx=12)

        over_btn = make_nav_item("Over ons", "OverOnsPage")
        over_btn.pack(side="left", padx=12)

        div3 = ctk.CTkFrame(nav_container, width=2, height=20, fg_color="#444444")
        div3.pack(side="left", padx=12)

        contact_btn = make_nav_item("Contact", "ContactPage")
        contact_btn.pack(side="left", padx=12)

        # ----------- MAX-WIDTH CONTENT AREA ----------
        self.content_container = ctk.CTkFrame(self, fg_color="transparent")
        self.content_container.pack(fill="both", expand=True)

        self.content_container.grid_rowconfigure(0, weight=1)
        self.content_container.grid_columnconfigure(0, weight=1)

        self.inner_frame = ctk.CTkFrame(self.content_container, fg_color="transparent")
        self.inner_frame.grid(row=0, column=0, pady=40)

        self.inner_frame.configure(width=900)
        self.inner_frame.configure(height=500)
        self.inner_frame.grid_propagate(False)  # <-- GRID versie!

