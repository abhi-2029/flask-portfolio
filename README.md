# 🚀 Personal Portfolio Website (Flask + SQLite)

This is my personal **Portfolio Website**, built using **Flask**, **HTML**, **CSS**, and **JavaScript** — featuring:
- A responsive 3D interactive UI
- Smooth navigation across sections (Home, Skills, Experience, Projects, Achievements, Contact)
- Secure **Admin Panel** for viewing messages
- Contact form with data stored in an **SQLite database**

---

## 🧩 Features

- 📂 **Flask Backend** with CSRF protection
- 💬 **Contact Form** storing messages in SQLite
- 🔒 **Admin Dashboard** (password protected)
- 🌙 **Dark Mode + Responsive Mobile UI**
- ⚙️ Fully deployable on **Render**

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-------------|
| Backend | Flask (Python) |
| Frontend | HTML, CSS, JavaScript |
| Database | SQLite |
| Deployment | Render |
| Security | Flask-WTF CSRF, Sessions |

---

## 🗄️ Folder Structure
portfolio/
│
├── static/
│ ├── css/
│ ├── js/
│ ├── images/
│ └── docs/
│
├── templates/
│ ├── index.html
│ ├── contact.html
│ ├── admin_login.html
│ ├── admin_messages.html
│ └── thank_you.html
│
├── instance/
│ └── messages.db (auto-created)
│
├── app.py
├── requirements.txt
├── .env
└── README.md

---

## 🔑 Environment Variables (.env file)

Before running or deploying, create a `.env` file in your root directory with the following content:
SECRET_KEY=your_secret_key
ADMIN_PASSWORD=Abhi@


---

## 🧠 Running Locally

### 1️⃣ Create Virtual Environment
```bash
python -m venv venv

2️⃣ Activate It
venv\Scripts\activate
Mac/Linux:
source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run Flask App
python app.py

☁️ Deploying on Render
1️⃣ Create a new web service on Render
2️⃣ Connect your GitHub repository
3️⃣ Set build settings:

Environment:
Python 3

Build Command:pip install -r requirements.txt
Start Command:gunicorn app:app

4️⃣ Add Environment Variables in Render Dashboard:
| Key            | Value           |
| -------------- | --------------- |
| SECRET_KEY     | your_secret_key |
| ADMIN_PASSWORD | ...@           |

5️⃣ Deploy 🎉
Render will automatically build and host your Flask portfolio.

🛠 Requirements.txt Example
If you don’t have it, create requirements.txt in root:
Flask==3.0.3
Flask-WTF==1.2.1
python-dotenv==1.0.1
gunicorn==23.0.0

🔍 Debugging on Render
If you get 500 Internal Server Error,
check the Logs tab under Render → Dashboard → Your Web Service.
You’ll see any Python or import-related errors there.

👨‍💻 Author
Abhishek Ranjan
🎓 Computer Science Engineer | 📍 India
🌐 [LinkedIn](https://www.linkedin.com/in/abhishekranjan20/)
 |[ GitHub](https://github.com/abhi-2029)

📜 License
MIT License © 2025 Abhishek Ranjan

---

## 🧠 QUICK DEPLOYMENT SUMMARY (Render)

1. Push your code to GitHub  
2. Create `.env` file (with SECRET_KEY, ADMIN_PASSWORD)  
3. Add `requirements.txt` (as above)  
4. On Render:
   - New → Web Service → Connect GitHub repo  
   - Build command: `pip install -r requirements.txt`  
   - Start command: `gunicorn app:app`  
5. Add your environment variables under “Environment”  
6. Click **Deploy**

✅ Within 2–3 minutes, your Flask portfolio will go live with a permanent Render link like:

✨ “Don’t wait for the right opportunity — create it, refine it, and let your consistency turn it into success.” 🚀

