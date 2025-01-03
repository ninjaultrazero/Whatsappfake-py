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
        self.root.title("WhatsApp Web")  # Set the window title
        self.root.geometry("800x600")  # Set the window size
        self.root.configure(bg="#ece5dd")  # Set the background color

        # Chat history stored in memory and saved to JSON file
        self.chat_history = {}  # Dictionary to hold chat history
        self.current_contact = None  # Currently selected contact

        # Check if the chat history JSON file exists, and load it
        self.load_chat_history()  # Load chat history from file

        # Left-side contacts panel
        self.contacts_frame = tk.Frame(self.root, width=250, bg="#075E54", bd=0)  # Frame for contacts
        self.contacts_frame.pack(side=tk.LEFT, fill=tk.Y)  # Pack the frame to the left

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
        self.contacts_header.pack(fill=tk.X)  # Pack the header to fill the width

        # Search bar toggle button
        self.search_bar_visible = False  # Flag to track search bar visibility
        self.toggle_search_button = tk.Button(
            self.contacts_frame,
            text="Search",
            command=self.toggle_search_bar,  # Command to toggle search bar
            bg="#128C7E",
            fg="#ffffff",
            font=("Helvetica", 12, "bold"),
            bd=0,
            padx=10,
            pady=5
        )
        self.toggle_search_button.pack(fill=tk.X, padx=10, pady=5)  # Pack the button

        # Search bar (hidden initially)
        self.search_var = tk.StringVar()  # Variable to hold search query
        self.search_var.trace("w", self.update_contacts_list)  # Update contacts list on change
        self.search_entry = tk.Entry(
            self.contacts_frame, textvariable=self.search_var, font=("Helvetica", 12),
            bd=0, bg="#ffffff", highlightbackground="#e0e0e0", highlightthickness=1,
            relief=tk.FLAT
        )
        self.search_entry.pack(fill=tk.X, padx=10, pady=5)  # Pack the search entry
        self.search_entry.pack_forget()  # Initially hide the search entry

        # Contacts list container with a canvas for scrolling
        self.contacts_canvas = tk.Canvas(self.contacts_frame, bg="#ffffff")  # Canvas for contacts
        self.contacts_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # Pack the canvas

        # Scrollbar for contacts
        self.contacts_scrollbar = tk.Scrollbar(self.contacts_frame, orient="vertical", command=self.contacts_canvas.yview)  # Vertical scrollbar
        self.contacts_scrollbar.pack(side=tk.RIGHT, fill="y")  # Pack the scrollbar

        self.contacts_canvas.configure(yscrollcommand=self.contacts_scrollbar.set)  # Link scrollbar to canvas
        self.contacts_canvas.bind("<Configure>", lambda e: self.contacts_canvas.configure(scrollregion=self.contacts_canvas.bbox("all")))  # Configure scroll region

        self.contacts_list_frame = tk.Frame(self.contacts_canvas, bg="#ffffff")  # Frame for contact list
        self.contacts_canvas.create_window((0, 0), window=self.contacts_list_frame, anchor="nw")  # Create window in canvas

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
            "Tom ": "Alice.png",
            "Bob Marlie": "Bob.png",
            "Charlie stekka": "Charlie.png",
            "David Silva": "David.png",
            "Eve ning": "Eve.png",
        }

        self.contact_widgets = []  # Store references to contact widgets
        self.populate_contacts()  # Populate the contacts list

        # Right-side chat area
        self.chat_frame = tk.Frame(self.root, bg="#ece5dd", bd=0)  # Frame for chat area
        self.chat_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)  # Pack the chat frame to the right

        # Header for current contact
        self.contact_header = tk.Label(
            self.chat_frame,
            text="Select a contact to start chatting",  # Default message
            bg="#128C7E",
            fg="#ffffff",
            font=("Helvetica", 14, "bold"),
            anchor="w",
            padx=10,
            pady=10
        )
        self.contact_header.pack(fill=tk.X)  # Pack the contact header
        
        # Chat area (ScrollFrame style)
        self.chat_area_frame = tk.Frame(self.chat_frame, bg="#ece5dd")  # Frame for chat messages
        self.chat_area_frame.pack(pady=(10, 0), padx=10, fill=tk.BOTH, expand=True)  # Pack the chat area

        self.chat_area_canvas = tk.Canvas(self.chat_area_frame, bg="#ffffff")  # Canvas for chat messages
        self.chat_area_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # Pack the canvas

        self.chat_area_scrollbar = tk.Scrollbar(self.chat_area_frame, orient="vertical", command=self.chat_area_canvas.yview)  # Vertical scrollbar for chat
        self.chat_area_scrollbar.pack(side=tk.RIGHT, fill="y")  # Pack the scrollbar

        self.chat_area_canvas.configure(yscrollcommand=self.chat_area_scrollbar.set)  # Link scrollbar to canvas
        self.chat_area_canvas.bind("<Configure>", lambda e: self.chat_area_canvas.configure(scrollregion=self.chat_area_canvas.bbox("all")))  # Configure scroll region

        self.chat_area_inner_frame = tk.Frame(self.chat_area_canvas, bg="#ffffff")  # Inner frame for chat messages
        self.chat_area_canvas.create_window((0, 0), window=self.chat_area_inner_frame, anchor="nw")  # Create window in canvas

        # Message entry frame
        self.message_frame = tk.Frame(self.chat_frame, bg="#f0f0f0", pady=5)  # Frame for message entry
        self.message_frame.pack(fill=tk.X)  # Pack the message frame

        # Message entry box
        self.message_entry = tk.Entry(
            self.message_frame, font=("Helvetica", 12), bd=0, bg="#ffffff",
            highlightbackground="#e0e0e0", highlightthickness=1, relief=tk.FLAT
        )
        self.message_entry.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.X, expand=True)  # Pack the entry box
        self.message_entry.bind("<Return>", lambda event: self.send_message())  # Bind Enter key to send message

        # Send button
        self.send_button = tk.Button(
            self.message_frame, text="Send", command=self.send_message,  # Command to send message
            bg="#25D366", fg="#ffffff", font=("Helvetica", 12, "bold"), bd=0,
            padx=20, pady=5
        )
        self.send_button.pack(side=tk.RIGHT, padx=10, pady=5)  # Pack the send button

        # Handle application close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)  # Set protocol for closing the window

        # Start the timer thread
        self.timer_thread = threading.Thread(target=self.timer)  # Create a thread for the timer
        self.timer_thread.start()  # Start the timer thread

    def toggle_search_bar(self):
        """Toggle the visibility of the search bar."""
        if self.search_bar_visible:  # If the search bar is visible
            self.search_entry.pack_forget()  # Hide the search entry
        else:
            self.search_entry.pack(fill=tk.X, padx=10, pady=5)  # Show the search entry
        self.search_bar_visible = not self.search_bar_visible  # Toggle the visibility flag

    def create_contact_widget(self, name, img_path):
        """Create a contact widget with an image and bind events."""
        contact_frame = tk.Frame(self.contacts_list_frame, bg="#ffffff", pady=5)  # Frame for each contact
        contact_frame.pack(fill=tk.X, padx=5, pady =2)  # Pack the contact frame

        # Load the avatar image
        try:
            img = Image.open(img_path).resize((40, 40), Image.LANCZOS)  # Load the image and resize it
            img = ImageTk.PhotoImage(img)  # Convert the image to a PhotoImage
        except Exception as e:
            print(f"Error loading image for {name}: {e}")  # Print error if image loading fails
            img = ImageTk.PhotoImage(Image.new('RGB', (40, 40), color="#ccc"))  # Use a placeholder image if loading fails

        contact_img_label = tk.Label(contact_frame, image=img, bg="#ffffff")  # Label for contact image
        contact_img_label.image = img  # Keep a reference to avoid garbage collection
        contact_img_label.pack(side=tk.LEFT, padx=5)  # Pack the image label

        contact_name_label = tk.Label(contact_frame, text=name, font=("Helvetica", 12), bg="#ffffff", anchor="w")  # Label for contact name
        contact_name_label.pack(side=tk.LEFT, padx=5)  # Pack the name label

        contact_frame.bind("<Button-1>", lambda e: self.load_chat(name))  # Bind click event to load chat
        contact_img_label.bind("<Button-1>", lambda e: self.load_chat(name))  # Bind click event to load chat
        contact_name_label.bind("<Button-1>", lambda e: self.load_chat(name))  # Bind click event to load chat

        self.contact_widgets.append((name, contact_frame))  # Store the contact widget

    def populate_contacts(self):
        """Populate the contacts list."""
        for name, img_path in self.contacts.items():  # Iterate through contacts
            self.create_contact_widget(name, img_path)  # Create a widget for each contact

    def update_contacts_list(self, *args):
        """Update the displayed contacts based on the search query."""
        search_query = self.search_var.get().lower()  # Get the search query
        for name, widget in self.contact_widgets:  # Iterate through contact widgets
            if search_query in name.lower():  # Check if the contact name matches the search query
                widget.pack(fill=tk.X, padx=5, pady=2)  # Show the contact widget
            else:
                widget.pack_forget()  # Hide the contact widget

    def load_chat(self, contact):
        """Load chat for the selected contact."""
        self.current_contact = contact  # Set the current contact
        self.contact_header.config(text=f"Chat with {contact}")  # Update the header with the contact name
        # Clear chat area
        for widget in self.chat_area_inner_frame.winfo_children():  # Destroy existing chat widgets
            widget.destroy()

        if contact in self.chat_history:  # Check if there is chat history for the contact
            for message in self.chat_history[contact]:  # Iterate through messages
                if isinstance(message, tuple) and len(message) == 2:  # Check if message is a tuple
                    message_text, sender = message  # Unpack message
                    if sender == "you":  # Check if the message is from the user
                        self.create_message_widget(message_text, "right")  # Display user message
                    else:
                        self.create_message_widget(message_text, "left")  # Display contact message
        else:
            self.create_message_widget("No messages yet", "left")  # Display default message if no history

    def create_message_widget(self, message, position):
        """Create a message widget for displaying a message."""
        window_width = self.root.winfo_width()  # Get the window width
        contact_panel_width = self.contacts_frame.winfo_width()  # Get the contacts panel width
        chat_width = window_width - contact_panel_width - 10  # Calculate chat width

        bg_color = "#DCF8C6" if position == "right" else "#FFFFFF"  # Set background color based on position
        anchor = 'e' if position == "right" else 'w'  # Set anchor based on position

        message_frame = tk.Frame(self.chat_area_inner_frame, bg=bg_color, padx=10, pady=5, width=chat_width)  # Frame for message
        message_frame.pack(fill=tk.X, padx=10, pady=2, anchor=anchor)  # Pack the message frame

        message_label = tk.Label(message_frame, text=message, bg=bg_color, wraplength=chat_width, justify='left', font=("Helvetica", 12))  # Label for message text
        message_label.pack(fill=tk.BOTH, expand=True)  # Pack the message label

        # Scroll to bottom
        self.chat_area_canvas.yview_moveto(1)  # Scroll to the bottom of the chat area

    def send_message(self, event=None):
        """Handle sending a message."""
        message = self.message_entry.get()  # Get the message from the entry box
        self.send_user_message(message)  # Send the user's message

    def send_user_message(self, message):
        """Send user message."""
        if message and self.current_contact:  # Check if message is not empty and a contact is selected
            self.create_message_widget(f"You: {message}", "right")  # Display the user's message
            if self.current_contact not in self.chat_history:  # If no history for the contact, create an entry
                self.chat_history[self.current_contact] = []
            self.chat_history[self.current_contact].append((message, "you"))  # Append the message to chat history
            self.save_chat_history()  # Save the updated chat history
            self.message_entry.delete(0, tk.END)  # Clear the message entry
            self.send_bot_message()  # Trigger a bot response

    def send_bot_message(self):
        """Send a random bot message."""
        bot_messages = [  # List of predefined bot messages
            "Hello! How can I help you today?",
            "I'm here to assist you!",
            "What would you like to know?",
            "Feel free to ask me anything!",
            "How's your day going?"
        ]
        if self.current_contact:  # Check if a contact is selected
            bot_message = random.choice(bot_messages)  # Select a random bot message
            self.create_message_widget(f"Bot: {bot_message}", "left")  # Display the bot's message
            if self.current_contact not in self.chat_history:  # If no history for the contact, create an entry
                self.chat_history[self.current_contact] = []
            self.chat_history[self.current_contact].append((bot_message, "bot"))  # Append the bot message to chat history
            self.save_chat_history()  # Save the updated chat history

    def save_chat_history(self):
        """Save chat history to file."""
        with open("chat_history.json", "w") as f:  # Open the chat history file in write mode
            json.dump(self.chat_history, f)  # Write the chat history to the file

    def load_chat_history(self):
        """Load chat history."""
        # Clean the file by resetting it
        with open("chat_history.json", "w") as f:  # Open the chat history file in write mode
            json.dump({}, f)  # Empty the file content
        self.chat_history = {}  # Initialize chat history as an empty dictionary

    def on_closing(self):
        """Handle closing."""
        self.chat_history.clear()  # Reset in-memory history
        with open("chat_history.json", "w") as f:  # Open the chat history file in write mode
            json.dump({}, f)  # Empty the file content
        self.root.destroy()  # Close the application

    def timer(self):
        """Timer function."""
        time.sleep(15)  # Wait for 15 seconds
        self.send_bot_message()  # Send a bot message
        self.timer_thread = threading.Thread(target=self.timer)  # Create a new timer thread

if __name__ == "__main__":
    root = tk.Tk()  # Create the main application window
    app = WhatsAppWebInterface(root)  # Initialize the WhatsApp web interface
    root.mainloop()  # Start the main event loop