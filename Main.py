import tkinter as tk
from tkinter import scrolledtext

def send_message(event=None):
    """Send a message and display it in the chatbox in Frame 2."""
    message = message_input.get().strip()  # Get the message text
    if message:  # If there is a message
        chat_display.config(state=tk.NORMAL)  # Allow editing of the chat display
        chat_display.insert(tk.END, f"You: {message}\n")  # Insert message into chat display
        chat_display.config(state=tk.DISABLED)  # Make it read-only again
        chat_display.yview(tk.END)  # Scroll to the bottom
        message_input.delete(0, tk.END)  # Clear the input field

# Main Window
root = tk.Tk()
root.title("Chatbox")
root.geometry("800x500")
1
# Frame 1: Sidebar (you can remove this if not needed)
frame_1 = tk.Frame(root, bg="#1B222A", width=200)
frame_1.pack(fill=tk.Y, side=tk.LEFT)

# Frame 2: Chat Area (Where the chat messages appear)
frame_2 = tk.Frame(root, bg="#161C20")  # Background color of Frame 2 is set to #161C20
frame_2.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Chat Display (ScrolledText in Frame 2 for chat history)
chat_display = scrolledtext.ScrolledText(frame_2, wrap=tk.WORD, bg="#161C20", fg="#D3D3D3", font=("Helvetica", 12))
chat_display.pack(fill=tk.BOTH, expand=True)
chat_display.config(state=tk.DISABLED)  # Read-only chat display

# Message Input Area (Below the chat display in Frame 2)
input_frame = tk.Frame(frame_2, bg="#161C20")  # Input frame with matching background color
input_frame.pack(fill=tk.X, padx=0, pady=5)

message_input = tk.Entry(input_frame, font=("Helvetica", 14), bg="#ffffff")
message_input.pack(side=tk.LEFT, fill=tk.X, padx=(0, 0), pady=5)  # Make the input field fixed-width

# Send Button (Changed to match the background of Frame 2)
send_button = tk.Button(input_frame, text="Send", bg="#161C20", fg="#ffffff", font=("Helvetica", 12, "bold"),
                         command=send_message)
send_button.pack(side=tk.RIGHT, padx=(0, 0), pady=0)

# Bind Enter key to send_message
message_input.bind("<Return>", send_message)

root.mainloop()
