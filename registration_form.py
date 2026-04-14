import tkinter as tk
from tkinter import ttk

# ── Palette: Deep Slate + Emerald Green ───────────────────────────────────────
BG         = "#1e2530"
CARD       = "#252d3a"
CARD_BORD  = "#2e3a4e"
INPUT_BG   = "#1a2133"
INPUT_FOC  = "#1e2a42"
BORDER     = "#2e3a4e"
BORDER_FOC = "#00b894"
ICON_FG    = "#4a9e8a"
PH_FG      = "#4a5568"
TEXT_FG    = "#e2e8f0"
TITLE_FG   = "#ffffff"
SUB_FG     = "#718096"
LABEL_FG   = "#a0aec0"
ACCENT     = "#00b894"
ACCENT_H   = "#00a381"
BTN_TXT    = "#ffffff"
ERR_BG     = "#2d1b1b"
ERR_FG     = "#fc8181"

F_TITLE = ("Helvetica", 17, "bold")
F_SUB   = ("Helvetica", 9)
F_LABEL = ("Helvetica", 8, "bold")
F_BODY  = ("Helvetica", 11)
F_BTN   = ("Helvetica", 12, "bold")
F_SMALL = ("Helvetica", 10)
F_ERR   = ("Helvetica", 9)
F_ICON  = ("Helvetica", 12)


# ── Placeholder Entry ─────────────────────────────────────────────────────────
class PHEntry(tk.Entry):
    def __init__(self, master, ph="", show_ch="", **kw):
        super().__init__(master, **kw)
        self._ph   = ph
        self._show = show_ch
        self._live = False
        self.config(fg=PH_FG, show="")
        self.insert(0, ph)
        self.bind("<FocusIn>",  self._in)
        self.bind("<FocusOut>", self._out)

    def _in(self, _):
        if not self._live:
            self.delete(0, "end")
            self.config(fg=TEXT_FG, show=self._show)
            self._live = True

    def _out(self, _):
        if not self.get():
            self._live = False
            self.config(show="", fg=PH_FG)
            self.insert(0, self._ph)

    def value(self):
        return self.get() if self._live else ""


# ── Focus-aware bordered input ────────────────────────────────────────────────
class BorderedInput(tk.Frame):
    def __init__(self, master, ph, icon, show_ch="", **kw):
        super().__init__(master, bg=BORDER, padx=1, pady=1, **kw)
        self._inner = tk.Frame(self, bg=INPUT_BG)
        self._inner.pack(fill="x")

        self._icon = tk.Label(self._inner, text=icon, font=F_ICON,
                              bg=INPUT_BG, fg=ICON_FG, width=2, anchor="center")
        self._icon.pack(side="left", padx=(8, 0), pady=6)

        tk.Frame(self._inner, bg=BORDER, width=1).pack(
            side="left", fill="y", pady=6)

        self.entry = PHEntry(self._inner, ph=ph, show_ch=show_ch,
                             font=F_BODY, bg=INPUT_BG, fg=PH_FG,
                             relief="flat", bd=0,
                             insertbackground=ACCENT,
                             highlightthickness=0)
        self.entry.pack(side="left", fill="x", expand=True,
                        ipady=8, padx=(10, 8))

        self.entry.bind("<FocusIn>",  self._glow_on)
        self.entry.bind("<FocusOut>", self._glow_off)

    def _glow_on(self, _):
        self.config(bg=BORDER_FOC)
        self._inner.config(bg=INPUT_FOC)
        self._icon.config(bg=INPUT_FOC, fg=ACCENT)
        self.entry.config(bg=INPUT_FOC)

    def _glow_off(self, _):
        self.config(bg=BORDER)
        self._inner.config(bg=INPUT_BG)
        self._icon.config(bg=INPUT_BG, fg=ICON_FG)
        self.entry.config(bg=INPUT_BG)

    def value(self):
        return self.entry.value()


# ── Info Popup ────────────────────────────────────────────────────────────────
class InfoPopup(tk.Toplevel):
    def __init__(self, parent, first, last, email, gender, country):
        super().__init__(parent)
        self.title("Registration Information")
        self.resizable(False, False)
        self.configure(bg=CARD)
        self.grab_set()

        tk.Frame(self, bg=ACCENT, height=3).pack(fill="x")

        body = tk.Frame(self, bg=CARD, padx=24, pady=20)
        body.pack()

        cv = tk.Canvas(body, width=46, height=46,
                       bg=CARD, highlightthickness=0)
        cv.create_oval(2, 2, 44, 44, fill=ACCENT, outline="")
        cv.create_text(23, 23, text="i",
                       font=("Georgia", 17, "bold"), fill="white")
        cv.grid(row=0, column=0, padx=(0, 16), sticky="n", pady=(4, 0))

        lines = "\n".join([
            f"First Name:  {first}",
            f"Last Name:   {last}",
            f"Email:          {email}",
            f"Gender:        {gender}",
            f"Country:       {country}",
        ])
        tk.Label(body, text=lines,
                 font=("Helvetica", 10), bg=CARD, fg=TEXT_FG,
                 justify="left").grid(row=0, column=1, sticky="w")

        tk.Frame(self, bg=CARD_BORD, height=1).pack(fill="x")

        btn_row = tk.Frame(self, bg=CARD, pady=12, padx=16)
        btn_row.pack(fill="x")
        tk.Button(btn_row, text="  OK  ",
                  font=("Helvetica", 10, "bold"),
                  bg=ACCENT, fg="white", relief="flat",
                  cursor="hand2", padx=12, pady=4,
                  activebackground=ACCENT_H,
                  activeforeground="white",
                  command=self.destroy).pack(side="right")

        self.update_idletasks()
        px = parent.winfo_rootx() + parent.winfo_width()  // 2
        py = parent.winfo_rooty() + parent.winfo_height() // 2
        self.geometry(f"+{px - self.winfo_width()//2}+{py - self.winfo_height()//2}")


# ── Main App ──────────────────────────────────────────────────────────────────
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Registration")
        self.configure(bg=BG)
        self.resizable(False, True)
        self._build_scroll_shell()
        self._populate()
        self._finish_sizing()
        self._center()

    # ── scrollable canvas shell ───────────────────────────────────────────────
    def _build_scroll_shell(self):
        self._canvas = tk.Canvas(self, bg=BG, highlightthickness=0)
        self._sb = tk.Scrollbar(self, orient="vertical",
                                command=self._canvas.yview)
        self._canvas.configure(yscrollcommand=self._sb.set)

        self._canvas.pack(side="left", fill="both", expand=True)
        self._sb.pack(side="right", fill="y")

        self._inner = tk.Frame(self._canvas, bg=BG)
        self._win_id = self._canvas.create_window(
            (0, 0), window=self._inner, anchor="nw")

        self._inner.bind("<Configure>", self._on_inner_cfg)
        self._canvas.bind("<Configure>", self._on_canvas_cfg)

        # mouse-wheel scrolling (Windows + macOS)
        self.bind_all("<MouseWheel>",
                      lambda e: self._canvas.yview_scroll(
                          -1 * (e.delta // 120), "units"))
        # Linux scroll
        self.bind_all("<Button-4>",
                      lambda _: self._canvas.yview_scroll(-1, "units"))
        self.bind_all("<Button-5>",
                      lambda _: self._canvas.yview_scroll(1, "units"))

    def _on_inner_cfg(self, _):
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))

    def _on_canvas_cfg(self, e):
        self._canvas.itemconfig(self._win_id, width=e.width)

    def _finish_sizing(self):
        self.update_idletasks()
        max_h  = int(self.winfo_screenheight() * 0.92)
        cw     = self._inner.winfo_reqwidth()
        ch     = self._inner.winfo_reqheight()
        win_h  = min(ch, max_h)
        self._canvas.configure(width=cw, height=win_h)
        # hide scrollbar when content fits
        if ch <= max_h:
            self._sb.pack_forget()

    # ── all form widgets ──────────────────────────────────────────────────────
    def _populate(self):
        page = tk.Frame(self._inner, bg=BG, padx=36, pady=32)
        page.pack()

        # card
        card = tk.Frame(page, bg=CARD,
                        highlightthickness=1,
                        highlightbackground=CARD_BORD)
        card.pack()

        tk.Frame(card, bg=ACCENT, height=4).pack(fill="x")

        inner = tk.Frame(card, bg=CARD, padx=30, pady=26)
        inner.pack()

        # title
        tk.Label(inner, text="Create Account",
                 font=F_TITLE, bg=CARD, fg=TITLE_FG).pack(anchor="w")
        tk.Label(inner, text="Fill in the details below to register",
                 font=F_SUB, bg=CARD, fg=SUB_FG).pack(anchor="w", pady=(2, 18))

        def lbl(txt):
            tk.Label(inner, text=txt, font=F_LABEL,
                     bg=CARD, fg=LABEL_FG, anchor="w").pack(fill="x", pady=(10, 3))

        # Email
        lbl("EMAIL ADDRESS")
        self.email_w = BorderedInput(inner, "you@example.com", "✉")
        self.email_w.pack(fill="x")

        # Password
        lbl("PASSWORD")
        self.pass_w = BorderedInput(inner, "Enter password", "🔒", show_ch="•")
        self.pass_w.pack(fill="x")

        # Confirm Password
        lbl("CONFIRM PASSWORD")
        self.pass2_w = BorderedInput(inner, "Re-enter password", "🔒", show_ch="•")
        self.pass2_w.pack(fill="x")

        # First / Last Name
        lbl("FULL NAME")
        name_row = tk.Frame(inner, bg=CARD)
        name_row.pack(fill="x")

        lf = tk.Frame(name_row, bg=CARD)
        lf.pack(side="left", fill="x", expand=True, padx=(0, 6))
        self.first_w = BorderedInput(lf, "First Name", "👤")
        self.first_w.pack(fill="x")

        lr = tk.Frame(name_row, bg=CARD)
        lr.pack(side="left", fill="x", expand=True, padx=(6, 0))
        self.last_w = BorderedInput(lr, "Last Name", "👤")
        self.last_w.pack(fill="x")

        # Gender
        lbl("GENDER")
        g_row = tk.Frame(inner, bg=CARD)
        g_row.pack(fill="x")
        self.gender_var = tk.StringVar(value="")
        for val in ("Male", "Female"):
            tk.Radiobutton(g_row, text=val,
                           variable=self.gender_var, value=val,
                           font=F_SMALL, bg=CARD, fg=TEXT_FG,
                           selectcolor=ACCENT,
                           activebackground=CARD,
                           activeforeground=ACCENT,
                           cursor="hand2").pack(side="left", padx=(0, 24))

        # Country
        lbl("COUNTRY")
        countries = ["USA", "Canada", "Mexico", "UK", "Germany",
                     "France", "Australia", "India", "Japan", "Brazil", "Other"]
        self.country_var = tk.StringVar(value="Select a country")

        sty = ttk.Style()
        sty.theme_use("clam")
        sty.configure("D.TCombobox",
                      fieldbackground=INPUT_BG, background=INPUT_BG,
                      foreground=PH_FG, arrowcolor=ICON_FG,
                      bordercolor=BORDER, lightcolor=BORDER,
                      darkcolor=BORDER, selectbackground=INPUT_BG,
                      selectforeground=TEXT_FG, padding=9)
        sty.map("D.TCombobox",
                fieldbackground=[("readonly", INPUT_BG)],
                foreground=[("readonly", PH_FG)],
                bordercolor=[("focus", BORDER_FOC)])

        self.country_cb = ttk.Combobox(inner,
                                       textvariable=self.country_var,
                                       values=countries, state="readonly",
                                       style="D.TCombobox", font=F_BODY)
        self.country_cb.pack(fill="x")
        self.country_cb.bind("<<ComboboxSelected>>",
                             lambda _: sty.map("D.TCombobox",
                                               foreground=[("readonly", TEXT_FG)]))

        # Checkboxes
        self.terms_var = tk.BooleanVar()
        self.news_var  = tk.BooleanVar()
        ck = tk.Frame(inner, bg=CARD)
        ck.pack(fill="x", pady=(14, 0))
        for var, txt in (
            (self.terms_var, "I agree with the Terms & Conditions"),
            (self.news_var,  "I want to receive the newsletter"),
        ):
            tk.Checkbutton(ck, text=txt, variable=var,
                           font=F_SMALL, bg=CARD, fg=TEXT_FG,
                           selectcolor=ACCENT,
                           activebackground=CARD,
                           activeforeground=ACCENT,
                           highlightthickness=0,
                           cursor="hand2").pack(anchor="w", pady=3)

        # Error label
        self.err_lbl = tk.Label(inner, text="", font=F_ERR,
                                bg=ERR_BG, fg=ERR_FG,
                                wraplength=360, justify="left",
                                padx=10, pady=7)

        # Register button
        self.btn = tk.Button(inner, text="Register",
                             font=F_BTN, bg=ACCENT, fg=BTN_TXT,
                             relief="flat", bd=0, cursor="hand2",
                             activebackground=ACCENT_H,
                             activeforeground=BTN_TXT,
                             pady=13, command=self._submit)
        self.btn.pack(fill="x", pady=(20, 0))
        self.btn.bind("<Enter>", lambda _: self.btn.config(bg=ACCENT_H))
        self.btn.bind("<Leave>", lambda _: self.btn.config(bg=ACCENT))

        # Footer
        tk.Label(inner, text="Your information is kept private and secure.",
                 font=("Helvetica", 8), bg=CARD, fg=SUB_FG).pack(pady=(10, 0))

    # ── Validation ────────────────────────────────────────────────────────────
    def _submit(self):
        email   = self.email_w.value().strip()
        pwd     = self.pass_w.value()
        pwd2    = self.pass2_w.value()
        first   = self.first_w.value().strip()
        last    = self.last_w.value().strip()
        gender  = self.gender_var.get()
        country = self.country_var.get()

        errs = []
        if not email:
            errs.append("• Email is required.")
        if not first or not last:
            errs.append("• First and last name are required.")
        if not pwd:
            errs.append("• Password is required.")
        elif pwd != pwd2:
            errs.append("• Passwords do not match.")
        if not gender:
            errs.append("• Please select a gender.")
        if country == "Select a country":
            errs.append("• Please select a country.")
        if not self.terms_var.get():
            errs.append("• You must agree to the Terms & Conditions.")
        if not self.news_var.get():
            errs.append("• Please check the newsletter box.")

        if errs:
            self.err_lbl.config(text="\n".join(errs))
            self.err_lbl.pack(fill="x", pady=(14, 0), before=self.btn)
            self._canvas.after(60, lambda: self._canvas.yview_moveto(1.0))
            return

        self.err_lbl.pack_forget()
        InfoPopup(self, first, last, email, gender, country)

    # ── Center ────────────────────────────────────────────────────────────────
    def _center(self):
        self.update_idletasks()
        w  = self.winfo_width()
        h  = self.winfo_height()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        self.geometry(f"+{(sw-w)//2}+{(sh-h)//2}")


if __name__ == "__main__":
    App().mainloop()
