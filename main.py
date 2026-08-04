from cards import doublers, sources, reducers, creature_bonuses, untap_loop_sources, devoted_druid, extra_tap_sources
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Kinnan Mana Calculator")
root.geometry("600x400")

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
  var = tk.BooleanVar()
  check = ttk.Checkbutton(scrollable_frame, text=source["name"], variable=var)
  check.pack()
  source["var"] = var


ttk.Label(root, text="Doublers").pack()
for doubler in doublers:
  var = tk.BooleanVar()
  check = ttk.Checkbutton(root, text=doubler["name"], variable=var)
  check.pack()
  doubler["var"] = var
  
ttk.Label(root, text="Reducers").pack()
for reducer in reducers:
  var = tk.BooleanVar()
  check = ttk.Checkbutton(root, text=reducer["name"], variable=var)
  check.pack()
  reducer["var"] = var
  
root.after(3000, lambda: print([d["name"] for d in doublers if d["var"].get()],
                                [r["name"] for r in reducers if r["var"].get()]))

root.mainloop()