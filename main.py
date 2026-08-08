import tkinter as tk
from tkinter import ttk
from cards import doublers, sources, reducers, creature_bonuses, untap_loop_sources, devoted_druid, extra_tap_sources
from mana import create_pool, get_total_multiplier, tap_source, is_infinite_loop, add_mana, devoted_druid_total, add_to_battlefield
import io
import os
import urllib.request
import urllib.parse
import json
from PIL import Image, ImageTk
import time
from tkinter import messagebox

CACHE_DIR = "image_cache"

def fetch_card_image_url(card_name):
  url = "https://api.scryfall.com/cards/named?fuzzy=" + urllib.parse.quote(card_name)
  request = urllib.request.Request(url, headers={
    "User-Agent": "KinnanManaCalculator/1.0",
    "Accept" : "application/json"
  })
  
  with urllib.request.urlopen(request) as response:
    data = json.loads(response.read())
  return data["image_uris"]["normal"]

print(fetch_card_image_url("Sol Ring"))

def get_cached_image_patch(card_name):
  safe_name = card_name.replace(" ", "_").replace(",", "").replace("'", "")
  return os.path.join(CACHE_DIR, safe_name + ".jpg")

def load_card_image_cached(card_name):
  os.makedirs(CACHE_DIR, exist_ok=True)
  path = get_cached_image_patch(card_name)
  
  if os.path.exists(path):
    pil_image = Image.open(path)
  else:
    image_url = fetch_card_image_url(card_name)
    request = urllib.request.Request(image_url, headers={"User-Agent":"KinnanManaCalculator/1.0"})
    with urllib.request.urlopen(request) as response:
      image_data = response.read()
    time.sleep(0.1)
    with open(path, "wb") as f:
      f.write(image_data)
    pil_image = Image.open(io.BytesIO(image_data))
    
  pil_image = pil_image.resize((150, 210))
  return ImageTk.PhotoImage(pil_image)

root = tk.Tk()
root.title("Kinnan Mana Calculator")
root.geometry("600x400")

pool = create_pool()
batttlefield = []

def sync_battlefield():
    all_groups = [sources, untap_loop_sources, extra_tap_sources, [devoted_druid]]
    for group in all_groups:
        for card in group:
            if card["var"].get():
                already_there = False
                for permanent in batttlefield:
                    if permanent["name"] == card["name"]:
                        already_there = True
                if not already_there:
                    add_to_battlefield(batttlefield, card["name"], card["type"])

# ---Pool Section ---
pool_frame = ttk.Frame(root)
pool_frame.pack(fill="x")

pool_vars = {}
for color in ["W", "U", "B", "R", "G", "C"]:
    var = tk.StringVar(value=f"{color}: {pool[color]}")
    label = ttk.Label(pool_frame, textvariable=var)
    label.pack(side="left", padx=5)
    pool_vars[color]= var
    
def update_pool_display():
    for color in ["W", "U", "B", "R", "G", "C"]:
        pool_vars[color].set(f"{color}: {pool[color]}")


def tap_and_update(source):
    for doubler in doublers:
        doubler["active"] = doubler["var"].get()
    multiplier = get_total_multiplier(doublers)
    tap_source(pool, source, multiplier)
    update_pool_display()
    source["tap_button"].config(state="disabled")


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
    
    photo = load_card_image_cached(source["name"])
    image_label = ttk.Label(card, image=photo)
    image_label.pack(anchor="w")
    source["photo"] = photo
    
    var = tk.BooleanVar()
    check = ttk.Checkbutton(card, text=source["name"], variable=var)
    check.pack()
    source["var"] = var
    
    tap_button = ttk.Button(card, text="Tap", command=lambda s=source: tap_and_update(s))
    tap_button.pack(anchor="w")
    source["tap_button"] = tap_button
    
ttk.Label(root, text="Untap Loops").pack()
for card in untap_loop_sources:
    card_frame = ttk.Frame(root, relief="ridge", borderwidth=1, padding=5)
    card_frame.pack(fill="x", pady=2)
        
    var = tk.BooleanVar()
    check = ttk.Checkbutton(card_frame, text=card["name"], variable=var)
    check.pack(anchor="w")
    card["var"] = var
    
    tap_button = ttk.Button(card_frame, text="Tap", command=lambda s=card: tap_untap_loop(s))
    tap_button.pack(anchor="w")
    card["tap_button"] = tap_button
    
# --- Infinite Loops section ---
def tap_untap_loop(source):
    for doubler in doublers:
        doubler["active"] = doubler["var"].get()
    multiplier = get_total_multiplier(doublers)
    
    if is_infinite_loop(source, source["untap_cost"], multiplier):
        messagebox.showinfo("Infinite Mana!", f"{source['name']} is an infinite mana loop with your current board.")
    else:
        tap_source(pool, source, multiplier)
        update_pool_display() 
    source["tap_button"].config(state="disabled") 

# --- Devoted Druid section ---
ttk.Label(root, text="Devoted Druid").pack()
devoted_druid_frame = ttk.Frame(root, relief="ridge", borderwidth=1, padding=5)
devoted_druid_frame.pack(fill="x", pady=2)

devoted_druid_var = tk.BooleanVar()
check = ttk.Checkbutton(devoted_druid_frame, text=devoted_druid["name"], variable=devoted_druid_var)
check.pack(anchor="w")
devoted_druid["var"] = devoted_druid_var

tap_twice_var = tk.BooleanVar()
tap_twice_check = ttk.Checkbutton(devoted_druid_frame, text="Sacrifice for 2nd tap", variable=tap_twice_var)
tap_twice_check.pack(anchor="w")

def tap_devoted_druid():
    for doubler in doublers:
        doubler["active"] = doubler["var"].get()
    multiplier = get_total_multiplier(doublers)

    total_mana = devoted_druid_total(devoted_druid, multiplier, tap_twice_var.get())
    add_mana(pool, devoted_druid["color"], total_mana)
    update_pool_display() 
    
    devoted_druid_tap_button.config(state="disabled")
    tap_twice_check.config(state="disabled")       

devoted_druid_tap_button = ttk.Button(devoted_druid_frame, text="Tap", command=tap_devoted_druid)
devoted_druid_tap_button.pack(anchor="w")

# --- New Turn section ---
def new_turn():
    global pool, battlefield
    pool = create_pool()
    battlefield = []
    
    for source in sources:
        source["tap_button"].config(state="normal")
    for card in untap_loop_sources:
        card["tap_button"].config(state="normal")
    
    devoted_druid_tap_button.config(state="normal")
    tap_twice_check.config(state="normal")
    
    update_pool_display()
    
new_turn_button = ttk.Button(root, text="New Turn", command=new_turn)
new_turn_button.pack()

root.mainloop()