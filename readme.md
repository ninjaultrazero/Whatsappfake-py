# WhatsApp Web Interface 🟢

This project is a custom implementation of a WhatsApp-like chat interface using **CustomTkinter** and **Pillow** libraries. 🎉 The interface includes features such as chat history, contact management, and automated bot replies. 🤖

---

## 📦 Installation and Setup

To get started, follow these steps to set up your environment and run the application:

```bash
# Create a virtual environment
python -m venv myenv

# Activate the virtual environment
./myenv/Scripts/activate.bat

# Upgrade pip
python -m pip install --upgrade pip

# Install required libraries
pip install customtkinter
pip install Pillow
```

---

## 🚀 Features

### 🌟 Main Features

1. **Contact Management** 📇
   - Displays a list of contacts with profile pictures.
   - Search bar for quick contact filtering.
2. **Chat Interface** 💬
   - Send and receive messages.
   - Differentiated styling for sent and received messages.
3. **Bot Replies** 🤖
   - Automated bot responses to simulate conversation.
4. **Chat History** 📝
   - Persistent storage of chat history using JSON.
5. **Dark Mode Support** 🌒
   - Adjusts appearance based on system settings.
6. **Resizable UI** 📱
   - Responsive design for better usability.

---

## 🛠️ Code Structure

### Key Components

1. **Contacts Panel**:
   - A scrollable panel to display all contacts with a toggleable search bar.
2. **Chat Area**:
   - Displays messages exchanged with the currently selected contact.
   - Contains an input box and a send button for new messages.
3. **Bot Integration**:
   - Simulates a chatbot with predefined responses.
4. **Persistent Storage**:
   - Saves and loads chat history in `chat_history.json`.

### Libraries Used

- **CustomTkinter**: For modern GUI components and themes.
- **Pillow**: For handling and resizing contact images.
- **Threading**: For background tasks like bot replies.
- **JSON**: For saving and loading chat data.

---

## ⚙️ How It Works

1. **Initialization**:
   - The app initializes with a predefined list of contacts.
   - Chat history is loaded from `chat_history.json`.
2. **Contact Selection**:
   - Click on a contact to view or start a conversation.
3. **Message Sending**:
   - Type a message and press `Enter` or click "Send" to send it.
   - Messages are displayed with unique styles based on the sender.
4. **Bot Interaction**:
   - A bot responds automatically with random messages after a short delay.
5. **Timer Functionality**:
   - Simulates periodic bot replies using a timer thread.

---

## 📸 Screenshots

- **Contact List View**
- **Chat View with Messages**
- **Bot Reply Example**

*(Add screenshots here to visually represent the application.)*

---

## 🔧 Known Issues

- Profile images must exist at the specified paths; otherwise, a default placeholder is used.
- Limited bot reply options (can be extended).

---

## 🤝 Contributing

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Make your changes and commit: `git commit -m 'Add feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Submit a pull request.

---

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## 🙏 Acknowledgments

- Inspired by WhatsApp Web's interface.
- Developed using **CustomTkinter** for a modern desktop GUI.

---

## 🛡️ Disclaimer

This project is for educational purposes only and is not affiliated with or endorsed by WhatsApp.

---

### 🔗 Links

- [CustomTkinter Documentation](https://github.com/TomSchimansky/CustomTkinter)
- [Pillow Documentation](https://pillow.readthedocs.io/)

