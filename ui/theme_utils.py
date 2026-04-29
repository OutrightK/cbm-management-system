import tkinter as tk


def apply_popup_theme(window, dark_mode):
    if dark_mode:
        bg = "#2d3436"
        fg = "#ecf0f1"
        card_bg = "#353b48"
        button_bg = "#1abc9c"
    else:
        bg = "#ecf0f1"
        fg = "#2d3436"
        card_bg = "white"
        button_bg = "#1abc9c"

    window.config(bg=bg)

    def update_children(widget):
        for child in widget.winfo_children():
            try:
                if isinstance(child, tk.Frame):
                    child.config(bg=card_bg)

                elif isinstance(child, tk.Label):
                    child.config(bg=card_bg, fg=fg)

                elif isinstance(child, tk.Button):
                    child.config(
                        bg=button_bg,
                        fg="white",
                        activebackground=button_bg,
                        activeforeground="white",
                        relief="flat"
                    )
            except Exception:
                pass

            update_children(child)

    update_children(window)