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
        self.load_chat_history()  # Make sure this function is defined below

        # Continue with other initializations
        self.contacts_frame = self.create_contacts_panel()  # Create contacts panel first
        self.initialize_ui()  # Initialize other UI elements

    def load_chat_history(self):
        """Load chat history from a JSON file."""
        try:
            if os.path.exists("chat_history.json"):
                with open("chat_history.json", "r") as f:
                    self.chat_history = json.load(f)
        except Exception as e:
            print(f"Error loading chat history: {e}")
            self.chat_history = {}  # In case of an error, initialize as an empty dictionary
