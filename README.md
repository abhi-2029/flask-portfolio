# 🌐 Flask Portfolio Website  

A personal portfolio built using **Flask**, **HTML**, **CSS**, and **JavaScript**, featuring responsive UI, dark mode, admin dashboard, and database integration for message storage.

---

## 🚀 Features
- 🎨 Modern and responsive UI  
- 🌙 Dark & light mode toggle  
- 📬 Contact form with database storage  
- 🔐 Admin login panel to view messages  
- 🧠 Built using Flask + SQLite3  
- ☁️ Deployable on **Render** or **Vercel**

---

## 🛠️ Tech Stack
**Frontend:** HTML, CSS, JavaScript  
**Backend:** Flask (Python)  
**Database:** SQLite3  
**Deployment:** Render  

---

🗂️ Folder Structure
```
flask-portfolio/
│
├── app.py                         # Main Flask backend file
├── requirements.txt               # Python dependencies
├── .env                           # Environment variables (SECRET_KEY, ADMIN_PASSWORD)
├── README.md                      # Documentation (fixed version below)
│
├── instance/                      # Database folder (auto-created)
│   └── messages.db                # SQLite database (auto-generated)
│
├── static/
│   ├── css/
│   │   └── style.css              # Your main CSS file
│   ├── js/
│   │   └── script.js              # JS file for UI, animations, etc.
│   └── images/
│       └── my-image.jpg           # Your profile image
│
└── templates/
    ├── index.html                 # Main portfolio HTML
    ├── skills.html                # Included in index
    ├── experience.html            # Included in index
    ├── projects.html              # Included in index
    ├── education.html             # Included in index
    ├── contact.html               # Included in index
    ├── admin_login.html           # Admin login page
    ├── admin_messages.html        # Messages dashboard
    └── thank_you.html             # After message submission
```
## ⚙️ Setup Instructions  

### 1️⃣ Clone the repository  
```bash
git clone https://github.com/abhi-2029/flask-portfolio.git
cd flask-portfolio
```
2️⃣ Create a virtual environment
```
python -m venv venv
source venv/Scripts/activate   # On Windows
source venv/bin/activate       # On Mac/Linux
```
3️⃣ Install dependencies
```
pip install -r requirements.txt
```
4️⃣ Run the app locally
```
python app.py
```
📦 Environment Variables

Create a .env file in your project root:
```
SECRET_KEY=your_secret_key  
ADMIN_PASSWORD=...@
```
🧾 Requirements.txt Example

If not already created, add this file:
```
Flask==3.0.3
Flask-WTF==1.2.1
python-dotenv==1.0.1
gunicorn==23.0.0
```
☁️ Deployment (Render)

1.Push your code to GitHub

2.Go to Render
 → New Web Service

3.Connect your GitHub repo

4.Use these settings:

   .Build Command: pip install -r requirements.txt

   .Start Command: gunicorn app:app

5.Add your environment variables under “Environment”

6.Click Deploy 🚀

🧩 Debugging on Render

If you get a 500 Internal Server Error,

   .Check the Logs tab in Render → Dashboard → Your Service.

   .You’ll see any Python or import-related errors there.

## 👨‍💻 Author

**Abhishek Ranjan**  
🎓 *Computer Science Engineer* | 📍 *India*  

🌐 [LinkedIn](https://www.linkedin.com/in/abhishekranjan20/) | [GitHub](https://github.com/abhi-2029)


 📜 License

MIT License © 2025 Abhishek Ranjan

🧠 Quote

“Code is like humor. When you have to explain it, it’s bad.”

