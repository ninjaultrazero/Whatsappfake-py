import json

def load_chat_history():
    """Load the chat history from a JSON file."""
    try:
        with open("chat_history.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_chat_history(chat_history):
    """Save the chat history to a JSON file."""
    with open("chat_history.json", "w") as f:
        json.dump(chat_history, f)
