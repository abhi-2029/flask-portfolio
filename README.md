# 🌐 Flask SDE Portfolio Website

A personal portfolio built using **Flask (Python)**, **HTML5**, **CSS3 (Vanilla)**, and **JavaScript**, featuring a responsive developer UI, dark mode toggle, contact message database backend, local container orchestration, and cloud database compatibility.

---

## 🚀 Key Features

*   **🎨 Premium Flat UI:** Sleek, high-fidelity developer interface with tags, icons, hover actions, and interactive details.
*   **🌙 Dark & Light Mode Toggle:** Native light/dark themes with theme preference persistence.
*   **📬 Contact Dashboard:** AJAX-based asynchronous form submissions with an integrated, secure admin message dashboard (`/admin`).
*   **💾 Hybrid Database Adapter:** Automatically routes reads/writes to **PostgreSQL** in production environments (using `DATABASE_URL`), and falls back seamlessly to **SQLite** (`messages.db`) for lightweight local development.
*   **🐳 Containerized Environments:** Completely configured with a production **Dockerfile** and local developer orchestration using **Docker Compose**.
*   **☁️ Production-Ready:** Fully optimized and packaged for modern container-based clouds (like Render, Vercel, or Heroku) running Python 3.12/3.13.

---

## 🛠️ Technology Stack

*   **Core:** Python 3.13 / Flask / Gunicorn
*   **Frontend:** Vanilla CSS3, Javascript, FontAwesome, Particles.js, Typed.js
*   **Database:** PostgreSQL (Production / Neon / Supabase) & SQLite3 (Local)
*   **DevOps:** Docker, Docker Compose, Git & GitHub Actions

---

## 🗂️ Folder Structure

```text
flask-portfolio/
│
├── app.py                         # Main Flask backend controller (PostgreSQL & SQLite)
├── requirements.txt               # Python package dependencies
├── .env                           # Local environment secrets (SECRET_KEY, ADMIN_PASSWORD)
├── Dockerfile                     # Production container blueprint
├── docker-compose.yml             # Local multi-container development blueprint
├── messages.db                    # Auto-generated local SQLite database (untracked)
│
├── static/
│   ├── css/
│   │   └── style.css              # Custom styling sheet (fully responsive)
│   ├── js/
│   │   └── script.js              # Custom scripts, form validation, & animations
│   ├── docs/
│   │   └── AbhishekRanjanCV.pdf   # Latest curriculum vitae
│   └── images/
│       └── my-image.jpg           # Profile avatar
│
└── templates/
    ├── index.html                 # Main landing layout
    ├── skills.html                # Skills grid partial
    ├── experience.html            # Experience timeline partial
    ├── projects.html              # Custom project grid partial
    ├── education.html             # Academic partial
    ├── contact.html               # Contact form partial
    ├── admin_login.html           # Admin credentials portal
    ├── admin_messages.html        # Admin message panel
    └── thank_you.html             # Redirection success confirmation page
```

---

## ⚙️ Setup & Installation

### Option A: Local Run (Standard)

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/abhi-2029/flask-portfolio.git
    cd flask-portfolio
    ```

2.  **Create a Virtual Environment:**
    ```bash
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create local Environment Config:**  
    Create a `.env` file in the root directory:
    ```env
    SECRET_KEY=your_development_secret_key_here
    ADMIN_PASSWORD=your_secure_admin_password
    # Optional: DATABASE_URL=postgres://... (Falls back to SQLite if omitted)
    ```

5.  **Run the Server:**
    ```bash
    python app.py
    ```
    Visit `http://127.0.0.1:5000` in your web browser.

### Option B: Local Run (Docker Container Orchestration)

To spin up the web app along with a local PostgreSQL container automatically:

1.  **Start Containers:**
    ```bash
    docker compose up --build
    ```
2.  **Access the Portals:**
    *   **Portfolio Website:** `http://localhost:5000`
    *   **PostgreSQL Port:** Access local database via port `5432`

---

## ☁️ Production Deployment (Render)

1.  Create a new **Web Service** on Render and link your GitHub repository.
2.  Configure the environment runtime settings:
    *   **Build Command:** `pip install -r requirements.txt`
    *   **Start Command:** `gunicorn app:app`
3.  Configure **Environment Variables**:
    *   `SECRET_KEY` = *[Your production secret]*
    *   `ADMIN_PASSWORD` = *[Your admin login password]*
    *   `DATABASE_URL` = *[Link a Render PostgreSQL Database to auto-bind]*

---

## 👨‍💻 Author

**Abhishek Ranjan**  
🎓 *Computer Science Engineer* | 📍 *India*  
🌐 [LinkedIn](https://www.linkedin.com/in/abhishekranjan20/) | [GitHub](https://github.com/abhi-2029)

---

## 📜 License

MIT License © 2025 Abhishek Ranjan
