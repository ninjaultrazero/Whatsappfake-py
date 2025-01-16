import time
import threading
import customtkinter as ctk
from PIL import Image, ImageTk
import random
import json

class WhatsAppWebInterface:
    def __init__(self, root):
        ctk.set_appearance_mode("System")  # Modes: "System", "Dark", "Light"
        ctk.set_default_color_theme("green")  # Themes: "blue", "green", "dark-blue"

        self.root = root
        self.root.title("WhatsApp Web")
        self.root.geometry("800x600")

        self.chat_history = {}
        self.current_contact = None
        self.load_chat_history()

        # Left-side contacts panel
        self.contacts_frame = ctk.CTkFrame(self.root, width=250)
        self.contacts_frame.pack(side="left", fill="y")

        self.contacts_header = ctk.CTkLabel(
            self.contacts_frame,
            text="WhatsApp",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.contacts_header.pack(fill="x", pady=10)

        self.toggle_search_button = ctk.CTkButton(
            self.contacts_frame,
            text="Search",
            command=self.toggle_search_bar
        )
        self.toggle_search_button.pack(fill="x", padx=10, pady=5)

        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self.update_contacts_list)
        self.search_entry = ctk.CTkEntry(
            self.contacts_frame,
            placeholder_text="Search...",
            textvariable=self.search_var
        )
        self.search_entry.pack(fill="x", padx=10, pady=5)
        self.search_entry.pack_forget()

        self.contacts_canvas = ctk.CTkScrollableFrame(self.contacts_frame)
        self.contacts_canvas.pack(fill="both", expand=True)

        self.contacts = {
            "Alice": "./foto/Alice.png",
            "lucio": "./foto/vesuvio.png",
            "Prof Greco": "./foto/logonapoli.png",
            "Steve": "./foto/steve.png",
            "Eve": "./foto/lamborghini.png",
            "Elon": "./foto/elonmusk.png",
            "De Laurentis": "./foto/delaure.png",
            "lukaku": "./foto/lukaku.png",
            "Siri": "./foto/siri.png",
            "Jack": "./foto/jack.png",
            "Asus": "./foto/asus.png",
            "Leo": "./foto/leo.png",
            "Mia": "./foto/gatto.png",      
            "Meret": "./foto/meret.png",
            "Batman": "./foto/batman.png",
            "Paul": "./foto/paul.png",
            "Prime": "./foto/optimus.png",
            "Ronaldo": "./foto/ronaldo.png",
            "Presidente": "./foto/mattarella.png",
            "Spiderman": "./foto/spiderman.png",
            "Bob Marley": "./foto/bobma.png",
            "Peter Parker": "./foto/peter.png",
            "Tony Stark": "./foto/tony.png",
            "Eve ning": "./foto/evee.png",      
        }
        self.contact_widgets = []
        self.populate_contacts()

        # Right-side chat area
        self.chat_frame = ctk.CTkFrame(self.root)
        self.chat_frame.pack(side="right", fill="both", expand=True)

        self.contact_header = ctk.CTkLabel(
            self.chat_frame,
            text="Select a contact to start chatting",
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=5,
            fg_color="#128C7E",
            text_color="black"
        )
        self.contact_header.pack(fill="x")

        self.chat_area = ctk.CTkScrollableFrame(self.chat_frame, fg_color="#ece5dd")
        self.chat_area.pack(fill="both", expand=True, pady=10, padx=10)

        self.message_frame = ctk.CTkFrame(self.chat_frame)
        self.message_frame.pack(fill="x")

        self.message_entry = ctk.CTkEntry(
            self.message_frame,
            placeholder_text="Type your message..."
        )
        self.message_entry.pack(side="left", fill="x", expand=True, padx=10, pady=5)
        self.message_entry.bind("<Return>", lambda e: self.send_message())

        self.send_button = ctk.CTkButton(
            self.message_frame,
            text="Send",
            command=self.send_message
        )
        self.send_button.pack(side="right", padx=10, pady=5)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.timer_thread = threading.Thread(target=self.timer)
        self.timer_thread.start()

    def toggle_search_bar(self):
        if self.search_entry.winfo_viewable():
            self.search_entry.pack_forget()
        else:
            self.search_entry.pack(fill="x", padx=10, pady=5)

    def populate_contacts(self):
        for name, img_path in self.contacts.items():
            self.create_contact_widget(name, img_path)

    def create_contact_widget(self, name, img_path):
        contact_frame = ctk.CTkFrame(self.contacts_canvas, corner_radius=10)
        contact_frame.pack(fill="x", pady=5, padx=10)

        try:
            img = Image.open(img_path)
            ctk_image = ctk.CTkImage(dark_image=img, size=(40, 40))  # Use CTkImage for scaling
        except Exception as e:
            print(f"Error loading image for {name}: {e}")
            img = Image.new("RGB", (40, 40), color="#ccc")
            ctk_image = ctk.CTkImage(dark_image=img, size=(40, 40))

        img_label = ctk.CTkLabel(contact_frame, image=ctk_image, text="")
        img_label.pack(side="left", padx=10)

        name_label = ctk.CTkLabel(contact_frame, text=name, font=ctk.CTkFont(size=14))
        name_label.pack(side="left", padx=10)

        contact_frame.bind("<Button-1>", lambda e: self.load_chat(name))
        name_label.bind("<Button-1>", lambda e: self.load_chat(name))

        self.contact_widgets.append((name, contact_frame))


    def update_contacts_list(self, *args):
        search_query = self.search_var.get().lower()
        for name, widget in self.contact_widgets:
            if search_query in name.lower():
                widget.pack(fill="x", pady=5, padx=10)
            else:
                widget.pack_forget()

    def load_chat(self, contact):
        self.current_contact = contact
        self.contact_header.configure(text=f"Chat with {contact}")
        for widget in self.chat_area.winfo_children():
            widget.destroy()

        messages = self.chat_history.get(contact, [])
        for message, sender in messages:
            self.display_message(message, sender)

    def display_message(self, message, sender):
        fg_color = "#DCF8C6" if sender == "you" else "#FFFFFF"
        message_label = ctk.CTkLabel(
            self.chat_area,
            text=message,
            fg_color=fg_color,
            text_color="black",
            corner_radius=5,
            justify="left",
            anchor="w",
            pady=5,
            padx=10
        )
        message_label.pack(anchor="e" if sender == "you" else "w", pady=5, padx=10)

    def send_message(self, event=None):
        message = self.message_entry.get().strip()
        if message and self.current_contact:
            self.display_message(message, "you")
            self.chat_history.setdefault(self.current_contact, []).append((message, "you"))
            self.message_entry.delete(0, "end")
            self.save_chat_history()
            self.bot_reply()

    def bot_reply(self):
        if self.current_contact:
            reply = random.choice(["Hello!", "How can I help?", "Good day!"])
            self.display_message(reply, "bot")
            self.chat_history[self.current_contact].append((reply, "bot"))
            self.save_chat_history()

    def save_chat_history(self):
        with open("chat_history.json", "w") as f:
            json.dump(self.chat_history, f)

    def load_chat_history(self):
        try:
            with open("chat_history.json", "r") as f:
                self.chat_history = json.load(f)
        except FileNotFoundError:
            self.chat_history = {}

    def on_closing(self):
        """Handle closing."""
        self.chat_history.clear()  # Reset in-memory history
        with open("chat_history.json", "w") as f:  # Open the chat history file in write mode
            json.dump({}, f)  # Empty the file content
        self.root.destroy()  # Close the application

    def timer(self):
        """Timer function."""
        time.sleep(15)  # Wait for 15 seconds
        self.bot_reply()  # Send a bot message
        self.timer_thread = threading.Thread(target=self.timer)  # Create a new timer thread

if __name__ == "__main__":
    root = ctk.CTk()
    app = WhatsAppWebInterface(root)
    root.mainloop()