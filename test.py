import io
import urllib.request
import urllib.parse
import json
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

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

def load_card_image(image_url):
  request = urllib.request.Request(image_url, headers={"User-Agent":"KinnanManaCalculator/1.0"})
  with urllib.request.urlopen(request) as response:
    image_data = response.read()
    
    pil_image = Image.open(io.BytesIO(image_data))
    pil_image = pil_image.resize((150, 210))
    return ImageTk.PhotoImage(pil_image)
  
root = tk.Tk()
root.title("Test Image")

image_url = fetch_card_image_url("Sol Ring")
photo = load_card_image(image_url)
test_label = ttk.Label(root, image=photo)
test_label.image = photo
test_label.pack()

root.mainloop()