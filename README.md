# 🎟️ Campus Event Management System

A full-stack Flask web application designed to streamline campus event management. This system allows administrators to create and manage events while enabling students to view details and generate QR-code based tickets for entry.

## 🚀 Features

* **Admin Dashboard:** Secure login for administrators to create, edit, and delete events.
* **Public Event Portal:** Students can browse upcoming events without logging in.
* **Ticket Generation:** Dynamic QR code generation for event registration.
* **Database Integration:** Uses SQLite for robust data handling.
* **Responsive Design:** Clean interface built with HTML/CSS.

## 🛠️ Tech Stack

* **Backend:** Python, Flask
* **Database:** SQLite (SQLAlchemy)
* **Frontend:** HTML5, CSS3
* **Utilities:** qrcode, bcrypt (for security)

## 💻 How to Run Locally

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/Event-Management-System.git](https://github.com/YOUR_USERNAME/Event-Management-System.git)
    cd Event-Management-System
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Initialize the Database**
    ```bash
    python app.py setup
    ```

4.  **Run the Application**
    ```bash
    python app.py
    ```
    Visit `http://127.0.0.1:5000` in your browser.

## 🔐 Admin Credentials (For Testing)
* **Username:** admin
* **Password:** admin123

## 📸 Screenshots
<img width="1914" height="863" alt="Screenshot 2025-11-24 153951" src="https://github.com/user-attachments/assets/8e5bb4c0-4c9d-4ffb-b955-d955ab1ca23f" /><img width="1897" height="896" alt="Screenshot 2025-11-24 154038" src="https://github.com/user-attachments/assets/03e4d874-b3e1-4aab-b5e9-e5c86185b458" />

