import tkinter as tk
from tkinter import ttk
from cards import doublers, sources, reducers, creature_bonuses, untap_loop_sources, devoted_druid, extra_tap_sources

root = tk.Tk()
root.title("Kinnan Mana Calculator")
root.geometry("600x400")

# --- Doublers section ---
doublers_open = True
def toggle_doublers():
    global doublers_open
    if doublers_open:
        doublers_frame.pack_forget()
        doublers_open = False
    else:
        doublers_frame.pack(fill="x")
        doublers_open = True

doublers_button = ttk.Button(root, text="Doublers", command=toggle_doublers)
doublers_button.pack(fill="x")

doublers_frame = ttk.Frame(root)
doublers_frame.pack(fill="x")
for doubler in doublers:
    var = tk.BooleanVar()
    check = ttk.Checkbutton(doublers_frame, text=doubler["name"], variable=var)
    check.pack()
    doubler["var"] = var

# --- Reducers section ---
reducers_open = True
def toggle_reducers():
    global reducers_open
    if reducers_open:
        reducers_frame.pack_forget()
        reducers_open = False
    else:
        reducers_frame.pack(fill="x")
        reducers_open = True

reducers_button = ttk.Button(root, text="Reducers", command=toggle_reducers)
reducers_button.pack(fill="x")

reducers_frame = ttk.Frame(root)
reducers_frame.pack(fill="x")
for reducer in reducers:
    var = tk.BooleanVar()
    check = ttk.Checkbutton(reducers_frame, text=reducer["name"], variable=var)
    check.pack()
    reducer["var"] = var

# --- Sources section ---
sources_open = True
def toggle_sources():
    global sources_open
    if sources_open:
        container.pack_forget()
        sources_open = False
    else:
        container.pack(fill="both", expand=True)
        sources_open = True

sources_button = ttk.Button(root, text="Mana Sources", command=toggle_sources)
sources_button.pack(fill="x")

container = ttk.Frame(root)
canvas = tk.Canvas(container)
scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

container.pack(fill="both", expand=True)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

for source in sources:
    card = ttk.Frame(scrollable_frame, relief="ridge", borderwidth=1, padding=5)
    card.pack(fill="x", pady=2)
    
    var = tk.BooleanVar()
    check = ttk.Checkbutton(card, text=source["name"], variable=var)
    check.pack()
    source["var"] = var
    
    tap_button = ttk.Button(card, text="Tap")
    tap_button.pack(anchor="w")

root.after(3000, lambda: print([d["name"] for d in doublers if d["var"].get()],
                                [r["name"] for r in reducers if r["var"].get()]))

root.mainloop()