root = tk.Tk()
root.title("Test Image")

image_url = fetch_card_image_url("Sol Ring")
photo = load_card_image_cached("Sol Ring")
test_label = ttk.Label(root, image=photo)
test_label.image = photo
test_label.pack()

root.mainloop()