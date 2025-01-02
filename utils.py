import tkinter as tk
from PIL import Image, ImageTk

def create_contact_widget(contact_frame, name, img_path, contact_list_frame, load_chat):
    """Create and return a contact widget for the list."""
    contact_frame = tk.Frame(contact_list_frame, bg="#ffffff", pady=5)
    contact_frame.pack(fill=tk.X, padx=5, pady=2)

    try:
        img = Image.open(img_path).resize((40, 40), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error loading image for {name}: {e}")
        img = ImageTk.PhotoImage(Image.new('RGB', (40, 40), color="#ccc"))

    contact_img_label = tk.Label(contact_frame, image=img, bg="#ffffff")
    contact_img_label.image = img
    contact_img_label.pack(side=tk.LEFT, padx=5)

    contact_name_label = tk.Label(contact_frame, text=name, font=("Helvetica", 12), bg="#ffffff", anchor="w")
    contact_name_label.pack(side=tk.LEFT, padx=5)

    contact_frame.bind("<Button-1>", lambda e: load_chat(name))
    contact_img_label.bind("<Button-1>", lambda e: load_chat(name))
    contact_name_label.bind("<Button-1>", lambda e: load_chat(name))

    return contact_frame
