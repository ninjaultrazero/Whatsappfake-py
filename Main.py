import tkinter as tk
from tkinter import scrolledtext, END
from PIL import Image, ImageTk


class WhatsAppWebInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("WhatsApp Web")
        self.root.geometry("800x600")
        self.root.configure(bg="#ece5dd")

        # Chat history stored in memory (not persisted)
        self.chat_history = {}
        self.current_contact = None

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

        # Contacts list container
        self.contacts_list_frame = tk.Frame(self.contacts_frame, bg="#ffffff")
        self.contacts_list_frame.pack(fill=tk.BOTH, expand=True)

        # Dummy contacts with images
        self.contacts = {
            "Alice": "Alice.png",
            "Bob": "Bob.png",
            "Charlie": "Charlie.png",
            "David": "David.png",
            "Eve": "Eve.png",
        }
        for name, img_path in self.contacts.items():
            self.create_contact_widget(name, img_path)

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

        # Chat area
        self.chat_area = scrolledtext.ScrolledText(
            self.chat_frame, state='disabled', wrap='word',
            font=("Helvetica", 12), bg="#ffffff", bd=0
        )
        self.chat_area.pack(pady=(10, 0), padx=10, fill=tk.BOTH, expand=True)

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

    def load_chat(self, contact):
        """Load chat for the selected contact."""
        self.current_contact = contact
        self.chat_area.config(state='normal')
        self.chat_area.delete(1.0, END)  # Clear chat area

        # Update header with contact name
        self.contact_header.config(text=f"Chat with {contact}")

        # Load chat messages for the selected contact
        if contact in self.chat_history:
            for message in self.chat_history[contact]:
                self.chat_area.insert(END, message + "\n")
        self.chat_area.config(state='disabled')

    def send_message(self):
        """Send a message and display it in the chat area."""
        message = self.message_entry.get()
        if message and self.current_contact:
            self.chat_area.config(state='normal')
            self.chat_area.insert(END, f"You: {message}\n")
            self.chat_area.config(state='disabled')

            # Store the message in memory for the session
            if self.current_contact not in self.chat_history:
                self.chat_history[self.current_contact] = []
            self.chat_history[self.current_contact].append(f"You: {message}")

            # Clear the message entry box
            self.message_entry.delete(0, tk.END)

    def on_closing(self):
        """Clear chat history (session only) and close the application."""
        self.chat_history.clear()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = WhatsAppWebInterface(root)
    root.mainloop()
