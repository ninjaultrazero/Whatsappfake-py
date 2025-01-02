import time
import threading
import tkinter as tk
from PIL import Image, ImageTk
import random
import json
import os

class WhatsAppWebInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("WhatsApp Web")
        self.root.geometry("800x600")
        self.root.configure(bg="#ece5dd")

        # Chat history stored in memory and saved to JSON file
        self.chat_history = {}
        self.current_contact = None

        # Check if the chat history JSON file exists, and load it
        self.load_chat_history()

        # Left-side contacts panel
        self.contacts_frame = tk.Frame(self.root, width=250, bg="#075E54", bd=0)
        self.contacts_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Header for contacts
        self.contacts_header = tk.Label(
            self.contacts_frame,
            text="WhatsApp",
            bg="#075E54",
            fg="#ffffff",
            font=("Helvetica", 18, "bold"),
            padx=10,
            pady=10,
            anchor="w"
        )
        self.contacts_header.pack(fill=tk.X)

        # Search bar toggle button
        self.search_bar_visible = False
        self.toggle_search_button = tk.Button(
            self.contacts_frame,
            text="Search",
            command=self.toggle_search_bar,
            bg="#128C7E",
            fg="#ffffff",
            font=("Helvetica", 12, "bold"),
            bd=0,
            padx=10,
            pady=5
        )
        self.toggle_search_button.pack(fill=tk.X, padx=10, pady=5)

        # Search bar (hidden initially)
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.update_contacts_list)
        self.search_entry = tk.Entry(
            self.contacts_frame, textvariable=self.search_var, font=("Helvetica", 12),
            bd=0, bg="#ffffff", highlightbackground="#e0e0e0", highlightthickness=1,
            relief=tk.FLAT
        )
        self.search_entry.pack(fill=tk.X, padx=10, pady=5)
        self.search_entry.pack_forget()

        # Contacts list container with a canvas for scrolling
        self.contacts_canvas = tk.Canvas(self.contacts_frame, bg="#ffffff")
        self.contacts_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar for contacts
        self.contacts_scrollbar = tk.Scrollbar(self.contacts_frame, orient="vertical", command=self.contacts_canvas.yview)
        self.contacts_scrollbar.pack(side=tk.RIGHT, fill="y")

        self.contacts_canvas.configure(yscrollcommand=self.contacts_scrollbar.set)
        self.contacts_canvas.bind("<Configure>", lambda e: self.contacts_canvas.configure(scrollregion=self.contacts_canvas.bbox("all")))

        self.contacts_list_frame = tk.Frame(self.contacts_canvas, bg="#ffffff")
        self.contacts_canvas.create_window((0, 0), window=self.contacts_list_frame, anchor="nw")

        # Dummy contacts with images
        self.contacts = {
            "Alice": "Alice.png",
            "Bob": "Alice.png",
            "Charlie": "Alice.png",
            "David": "Alice.png",
            "Eve": "Alice.png",
            "Frank": "Alice.png",
            "Grace": "Alice.png",
            "Hannah": "Alice.png",
            "Ivy": "Alice.png",
            "Jack": "Alice.png",
            "Katherine": "Alice.png",
            "Leo": "Alice.png",
            "Mia": "Alice.png",
            "Nina": "Alice.png",
            "Oscar": "Alice.png",
            "Paul": "Alice.png",
            "Quincy": "Alice.png",
            "Riley": "Alice.png",
            "Sophie": "Alice.png",
            "Tom": "Alice.png",
            "Bob Marlie": "Bob.png",
            "Charlie stekka": "Charlie.png",
            "David Silva": "David.png",
            "Eve ning": "Eve.png",
        }

        self.contact_widgets = []  # Store references to contact widgets
        self.populate_contacts()

        # Right-side chat area
        self.chat_frame = tk.Frame(self.root, bg="#ece5dd", bd=0)
        self.chat_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Header for current contact
        self.contact_header = tk.Label(
            self.chat_frame,
            text="Select a contact to start chatting",
            bg="#128C7E",
            fg="#ffffff",
            font=("Helvetica", 14, "bold"),
            anchor="w",
            padx=10,
            pady=10
        )
        self.contact_header.pack(fill=tk.X)

        # Chat area (ScrollFrame style)
        self.chat_area_frame = tk.Frame(self.chat_frame, bg="#ece5dd")
        self.chat_area_frame.pack(pady=(10, 0), padx=10, fill=tk.BOTH, expand=True)

        self.chat_area_canvas = tk.Canvas(self.chat_area_frame, bg="#ffffff")
        self.chat_area_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.chat_area_scrollbar = tk.Scrollbar(self.chat_area_frame, orient="vertical", command=self.chat_area_canvas.yview)
        self.chat_area_scrollbar.pack(side=tk.RIGHT, fill="y")

        self.chat_area_canvas.configure(yscrollcommand=self.chat_area_scrollbar.set)
        self.chat_area_canvas.bind("<Configure>", lambda e: self.chat_area_canvas.configure(scrollregion=self.chat_area_canvas.bbox("all")))

        self.chat_area_inner_frame = tk.Frame(self.chat_area_canvas, bg="#ffffff")
        self.chat_area_canvas.create_window((0, 0), window=self.chat_area_inner_frame, anchor="nw")

        # Message entry frame
        self.message_frame = tk.Frame(self.chat_frame, bg="#f0f0f0", pady=5)
        self.message_frame.pack(fill=tk.X)

        # Message entry box
        self.message_entry = tk.Entry(
            self.message_frame, font=("Helvetica", 12), bd=0, bg="#ffffff",
            highlightbackground="#e0e0e0", highlightthickness=1, relief=tk.FLAT
        )
        self.message_entry.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.X, expand=True)
        self.message_entry.bind("<Return>", lambda event: self.send_message())  # Bind Enter key

        # Send button
        self.send_button = tk.Button(
            self.message_frame, text="Send", command=self.send_message,
            bg="#25D366", fg="#ffffff", font=("Helvetica", 12, "bold"), bd=0,
            padx=20, pady=5
        )
        self.send_button.pack(side=tk.RIGHT, padx=10, pady=5)

        # Handle application close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Start the timer thread
        self.timer_thread = threading.Thread(target=self.timer)
        self.timer_thread.start()

    def toggle_search_bar(self):
        """Toggle the visibility of the search bar."""
        if self.search_bar_visible:
            self.search_entry.pack_forget()
        else:
            self.search_entry.pack(fill=tk.X, padx=10, pady=5)
        self.search_bar_visible = not self.search_bar_visible

    def create_contact_widget(self, name, img_path):
        """Create a contact widget with an image and bind events."""
        contact_frame = tk.Frame(self.contacts_list_frame, bg="#ffffff", pady=5)
        contact_frame.pack(fill=tk.X, padx=5, pady=2)

        # Load the avatar image
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

        contact_frame.bind("<Button-1>", lambda e: self.load_chat(name))
        contact_img_label.bind("<Button-1>", lambda e: self.load_chat(name))
        contact_name_label.bind("<Button-1>", lambda e: self.load_chat(name))

        self.contact_widgets.append((name, contact_frame))

    def populate_contacts(self):
        """Populate the contacts list."""
        for name, img_path in self.contacts.items():
            self.create_contact_widget(name, img_path)

    def update_contacts_list(self, *args):
        """Update the displayed contacts based on the search query."""
        search_query = self.search_var.get().lower()
        for name, widget in self.contact_widgets:
            if search_query in name.lower():
                widget.pack(fill=tk.X, padx=5, pady=2)
            else:
                widget.pack_forget()

    def load_chat(self, contact):
        """Load chat for the selected contact.""" 
        self.current_contact = contact
        self.contact_header.config(text=f"Chat with {contact}")
        # Clear chat area
        for widget in self.chat_area_inner_frame.winfo_children():
            widget.destroy()

        if contact in self.chat_history:
            for message in self.chat_history[contact]:
                if isinstance(message, tuple) and len(message) == 2:
                    message_text, sender = message
                    if sender == "you":
                        self.create_message_widget(message_text, "right")
                    else:
                        self.create_message_widget(message_text, "left")
        else:
            self.create_message_widget("No messages yet", "left")

    def create_message_widget(self, message, position):
        """Create a message widget for displaying a message."""
        window_width = self.root.winfo_width()
        contact_panel_width = self.contacts_frame.winfo_width()
        chat_width = window_width - contact_panel_width - 10  # Padding for margin

        bg_color = "#DCF8C6" if position == "right" else "#FFFFFF"
        anchor = 'e' if position == "right" else 'w'

        message_frame = tk.Frame(self.chat_area_inner_frame, bg=bg_color, padx=10, pady=5, width=chat_width)
        message_frame.pack(fill=tk.X, padx=10, pady=2, anchor=anchor)

        message_label = tk.Label(message_frame, text=message, bg=bg_color, wraplength=chat_width, justify='left', font=("Helvetica", 12))
        message_label.pack(fill=tk.BOTH, expand=True)

        # Scroll to bottom
        self.chat_area_canvas.yview_moveto(1)

    def send_message(self, event=None):
        """Handle sending a message."""
        message = self.message_entry.get()
        self.send_user_message(message)

    def send_user_message(self, message):
        """Send user message."""
        if message and self.current_contact:
            self.create_message_widget(f"You: {message}", "right")
            if self.current_contact not in self.chat_history:
                self.chat_history[self.current_contact] = []
            self.chat_history[self.current_contact].append((message, "you"))
            self.save_chat_history()
            self.message_entry.delete(0, tk.END)
            self.send_bot_message()

    def send_bot_message(self):
        """Send a random bot message."""
        bot_messages = [
            "Hello! How can I help you today?",
            "I'm here to assist you!",
            "What would you like to know?",
            "Feel free to ask me anything!",
            "How's your day going?"
        ]
        if self.current_contact:
            bot_message = random.choice(bot_messages)
            self.create_message_widget(f"Bot: {bot_message}", "left")
            if self.current_contact not in self.chat_history:
                self.chat_history[self.current_contact] = []
            self.chat_history[self.current_contact].append((bot_message, "bot"))
            self.save_chat_history()

    def save_chat_history(self):
        """Save chat history to file."""
        with open("chat_history.json", "w") as f:
            json.dump(self.chat_history, f)

    def load_chat_history(self):
        """Load chat history."""
        # Clean the file by resetting it
        with open("chat_history.json", "w") as f:
            json.dump({}, f)  # Empty the file content
        self.chat_history = {}

    def on_closing(self):
        """Handle closing."""
        self.chat_history.clear()  # Reset in-memory history
        with open("chat_history.json", "w") as f:
            json.dump({}, f)  # Empty the file content
        self.root.destroy()

    def timer(self):
        """Timer function."""
        time.sleep(15)
        self.send_bot_message()
        self.timer_thread = threading.Thread(target=self.timer())    

if __name__ == "__main__":
    root = tk.Tk()
    app = WhatsAppWebInterface(root)
    root.mainloop()
