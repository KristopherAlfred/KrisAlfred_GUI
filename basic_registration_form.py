import tkinter as tk
from tkinter import ttk

# ── Colors ────────────────────────────────────────────────────────────────────
BG       = "#ffffff"
BORDER   = "#cccccc"
PH_FG    = "#aaaaaa"
TEXT_FG  = "#333333"
ICON_FG  = "#555555"
YELLOW   = "#f5a623"
YELLOW_H = "#d4891a"
ERR_FG   = "#cc0000"
ERR_BG   = "#fff0f0"

F_TITLE = ("Arial", 15, "bold")
F_BODY  = ("Arial", 11)
F_BTN   = ("Arial", 12, "bold")
F_SMALL = ("Arial", 10)
F_ERR   = ("Arial", 9)


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


# ── Bordered input row: [icon | entry]  ───────────────────────────────────────
def make_input(parent, ph, icon, show_ch="", width=32):
    """
    Returns the PHEntry widget.
    Draws a 1-px grey border using a Frame wrapper + inner white frame trick.
    """
    # outer 1-px border frame
    outer = tk.Frame(parent, bg=BORDER, padx=1, pady=1)
    outer.pack(fill="x", pady=4)

    inner = tk.Frame(outer, bg=BG)
    inner.pack(fill="x")

    # icon label  (left side, same height as entry)
    icon_lbl = tk.Label(inner, text=icon, font=("Arial", 12),
                        bg=BG, fg=ICON_FG, width=2, anchor="center")
    icon_lbl.pack(side="left", padx=(6, 0), pady=4)

    # thin grey divider between icon and text
    div = tk.Frame(inner, bg=BORDER, width=1)
    div.pack(side="left", fill="y", pady=4)

    entry = PHEntry(inner, ph=ph, show_ch=show_ch,
                    font=F_BODY, bg=BG, fg=PH_FG,
                    relief="flat", bd=0,
                    insertbackground=TEXT_FG,
                    highlightthickness=0,
                    width=width)
    entry.pack(side="left", fill="x", expand=True, ipady=7, padx=(8, 6))
    return entry


# ── Info popup ────────────────────────────────────────────────────────────────
class InfoPopup(tk.Toplevel):
    def __init__(self, parent, first, last, email, gender, country):
        super().__init__(parent)
        self.title("Registration Information")
        self.resizable(False, False)
        self.configure(bg="#f0f0f0")
        self.grab_set()

        body = tk.Frame(self, bg="#f0f0f0", padx=20, pady=20)
        body.pack()

        cv = tk.Canvas(body, width=44, height=44,
                       bg="#f0f0f0", highlightthickness=0)
        cv.create_oval(2, 2, 42, 42, fill="#0078d4", outline="")
        cv.create_text(22, 22, text="i",
                       font=("Georgia", 17, "bold"), fill="white")
        cv.grid(row=0, column=0, padx=(0, 14), sticky="n")

        lines = "\n".join([
            f"First Name: {first}",
            f"Last Name: {last}",
            f"Email: {email}",
            f"Gender: {gender}",
            f"Country: {country}",
        ])
        tk.Label(body, text=lines, font=("Segoe UI", 10),
                 bg="#f0f0f0", fg="#111111",
                 justify="left").grid(row=0, column=1, sticky="w")

        tk.Frame(self, bg="#cccccc", height=1).pack(fill="x")
        btn_row = tk.Frame(self, bg="#f0f0f0", pady=10, padx=10)
        btn_row.pack(fill="x")
        tk.Button(btn_row, text="OK", width=8,
                  font=("Segoe UI", 10), relief="raised",
                  command=self.destroy).pack(side="right")

        self.update_idletasks()
        px = parent.winfo_rootx() + parent.winfo_width()  // 2
        py = parent.winfo_rooty() + parent.winfo_height() // 2
        self.geometry(f"+{px - self.winfo_width()//2}+{py - self.winfo_height()//2}")


# ── Main App ──────────────────────────────────────────────────────────────────
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Responsive Registration Form")
        self.configure(bg=BG)
        self.resizable(False, False)
        self._build()
        self._center()

    def _build(self):
        W = 420   # fixed form width

        # ── outer padding frame ──
        wrap = tk.Frame(self, bg=BG, padx=30, pady=24)
        wrap.pack()

        # ── Title ──
        tk.Label(wrap, text="Responsive Registration\nForm",
                 font=F_TITLE, bg=BG, fg="#111111",
                 justify="center").pack(pady=(0, 18))

        # ── Email ──
        self.email_e = make_input(wrap, "Email", "✉")

        # ── Password ──
        self.pass_e = make_input(wrap, "Password", "🔒", show_ch="•")

        # ── Re-type Password ──
        self.pass2_e = make_input(wrap, "Re-type Password", "🔒", show_ch="•")

        # ── First Name / Last Name  (two columns) ──
        row = tk.Frame(wrap, bg=BG)
        row.pack(fill="x", pady=0)

        # left column
        left_col = tk.Frame(row, bg=BG)
        left_col.pack(side="left", fill="x", expand=True, padx=(0, 5))
        outer_l = tk.Frame(left_col, bg=BORDER, padx=1, pady=1)
        outer_l.pack(fill="x", pady=4)
        inner_l = tk.Frame(outer_l, bg=BG)
        inner_l.pack(fill="x")
        tk.Label(inner_l, text="👤", font=("Arial", 12),
                 bg=BG, fg=ICON_FG, width=2).pack(side="left", padx=(6,0), pady=4)
        tk.Frame(inner_l, bg=BORDER, width=1).pack(side="left", fill="y", pady=4)
        self.first_e = PHEntry(inner_l, ph="First Name",
                               font=F_BODY, bg=BG, fg=PH_FG,
                               relief="flat", bd=0,
                               insertbackground=TEXT_FG,
                               highlightthickness=0, width=12)
        self.first_e.pack(side="left", fill="x", expand=True,
                          ipady=7, padx=(8, 6))

        # right column
        right_col = tk.Frame(row, bg=BG)
        right_col.pack(side="left", fill="x", expand=True, padx=(5, 0))
        outer_r = tk.Frame(right_col, bg=BORDER, padx=1, pady=1)
        outer_r.pack(fill="x", pady=4)
        inner_r = tk.Frame(outer_r, bg=BG)
        inner_r.pack(fill="x")
        tk.Label(inner_r, text="👤", font=("Arial", 12),
                 bg=BG, fg=ICON_FG, width=2).pack(side="left", padx=(6,0), pady=4)
        tk.Frame(inner_r, bg=BORDER, width=1).pack(side="left", fill="y", pady=4)
        self.last_e = PHEntry(inner_r, ph="Last Name",
                              font=F_BODY, bg=BG, fg=PH_FG,
                              relief="flat", bd=0,
                              insertbackground=TEXT_FG,
                              highlightthickness=0, width=12)
        self.last_e.pack(side="left", fill="x", expand=True,
                         ipady=7, padx=(8, 6))

        # ── Gender ──
        gender_row = tk.Frame(wrap, bg=BG)
        gender_row.pack(fill="x", pady=(10, 4))
        self.gender_var = tk.StringVar(value="")
        for val in ("Male", "Female"):
            tk.Radiobutton(gender_row, text=val,
                           variable=self.gender_var, value=val,
                           font=F_SMALL, bg=BG, fg="#333333",
                           selectcolor=BG, activebackground=BG,
                           cursor="hand2").pack(side="left", padx=(0, 20))

        # ── Country dropdown ──
        countries = ["USA", "Canada", "Mexico", "UK", "Germany",
                     "France", "Australia", "India", "Japan", "Brazil", "Other"]
        self.country_var = tk.StringVar(value="Select a country")

        sty = ttk.Style()
        sty.theme_use("clam")
        sty.configure("W.TCombobox",
                      fieldbackground=BG, background=BG,
                      foreground=PH_FG, arrowcolor="#555555",
                      bordercolor=BORDER, lightcolor=BORDER,
                      darkcolor=BORDER,
                      selectbackground=BG, selectforeground=TEXT_FG,
                      padding=8)
        sty.map("W.TCombobox",
                fieldbackground=[("readonly", BG)],
                foreground=[("readonly", PH_FG)],
                selectforeground=[("readonly", TEXT_FG)])

        self.country_cb = ttk.Combobox(wrap, textvariable=self.country_var,
                                       values=countries, state="readonly",
                                       style="W.TCombobox", font=F_BODY)
        self.country_cb.pack(fill="x", pady=4)

        def _on_pick(_):
            sty.map("W.TCombobox",
                    foreground=[("readonly", TEXT_FG)])
        self.country_cb.bind("<<ComboboxSelected>>", _on_pick)

        # ── Checkboxes ──
        self.terms_var = tk.BooleanVar()
        self.news_var  = tk.BooleanVar()
        ck = tk.Frame(wrap, bg=BG)
        ck.pack(fill="x", pady=(10, 0))
        for var, txt in ((self.terms_var, "I agree with terms and conditions"),
                         (self.news_var,  "I want to receive the newsletter")):
            tk.Checkbutton(ck, text=txt, variable=var,
                           font=F_SMALL, bg=BG, fg="#333333",
                           selectcolor=BG, activebackground=BG,
                           highlightthickness=0,
                           cursor="hand2").pack(anchor="w", pady=3)

        # ── Error label (hidden until needed) ──
        self.err_lbl = tk.Label(wrap, text="", font=F_ERR,
                                bg=ERR_BG, fg=ERR_FG,
                                wraplength=360, justify="left",
                                padx=10, pady=6)

        # ── Register button ──
        self.btn = tk.Button(wrap, text="Register",
                             font=F_BTN, bg=YELLOW, fg="white",
                             relief="flat", bd=0, cursor="hand2",
                             activebackground=YELLOW_H,
                             activeforeground="white",
                             pady=13,
                             command=self._submit)
        self.btn.pack(fill="x", pady=(16, 4))
        self.btn.bind("<Enter>", lambda _: self.btn.config(bg=YELLOW_H))
        self.btn.bind("<Leave>", lambda _: self.btn.config(bg=YELLOW))

    # ── validation ────────────────────────────────────────────────────────────
    def _submit(self):
        email   = self.email_e.value().strip()
        pwd     = self.pass_e.value()
        pwd2    = self.pass2_e.value()
        first   = self.first_e.value().strip()
        last    = self.last_e.value().strip()
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
            self.err_lbl.pack(fill="x", pady=(10, 0), before=self.btn)
            return

        self.err_lbl.pack_forget()
        InfoPopup(self, first, last, email, gender, country)

    # ── center ────────────────────────────────────────────────────────────────
    def _center(self):
        self.update_idletasks()
        w = self.winfo_width();  h = self.winfo_height()
        sw = self.winfo_screenwidth(); sh = self.winfo_screenheight()
        self.geometry(f"+{(sw-w)//2}+{(sh-h)//2}")


if __name__ == "__main__":
    App().mainloop()
