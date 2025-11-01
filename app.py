
# from flask import Flask, render_template, request, redirect, url_for, session, jsonify, g, make_response
# from flask_wtf.csrf import CSRFProtect
# from flask_mail import Mail, Message
# from functools import wraps
# import sqlite3
# from pathlib import Path
# import os
# from dotenv import load_dotenv

# # ----------------------------
# # Load environment variables
# # ----------------------------
# load_dotenv()

# app = Flask(__name__)

# # Secure configuration
# app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')
# csrf = CSRFProtect(app)
# ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'Abhi@')

# # ----------------------------
# # Flask-Mail Configuration
# # ----------------------------
# app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
# app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
# app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
# app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
# app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
# app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

# mail = Mail(app)

# # ----------------------------
# # Database setup
# # ----------------------------
# BASE_DIR = Path(__file__).parent
# DATABASE = BASE_DIR / 'messages.db'

# def get_db():
#     if not hasattr(g, '_database'):
#         g._database = sqlite3.connect(DATABASE)
#         g._database.row_factory = sqlite3.Row
#         g._database.execute("PRAGMA foreign_keys = ON")
#     return g._database

# @app.teardown_appcontext
# def close_db(exception):
#     db = getattr(g, '_database', None)
#     if db is not None:
#         db.close()

# def init_db():
#     """Initialize messages table"""
#     try:
#         with app.app_context():
#             db = get_db()
#             db.execute("""
#                 CREATE TABLE IF NOT EXISTS messages (
#                     id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     name TEXT NOT NULL,
#                     email TEXT NOT NULL,
#                     subject TEXT,
#                     message TEXT NOT NULL,
#                     timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
#                     UNIQUE(name, email, message, timestamp) ON CONFLICT IGNORE
#                 )
#             """)
#             db.commit()
#         print("✓ Database initialized successfully")
#     except Exception as e:
#         print(f"✗ Database initialization failed: {e}")

# # ----------------------------
# # Authentication decorator
# # ----------------------------
# def admin_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if not session.get('is_admin'):
#             return redirect(url_for('admin_login'))
#         return f(*args, **kwargs)
#     return decorated_function

# # ----------------------------
# # Routes
# # ----------------------------
# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/submit', methods=['POST'])
# @csrf.exempt
# def submit():
#     """Handle contact form submission"""
#     if request.method == 'POST':
#         try:
#             name = request.form.get('name', '').strip()
#             email = request.form.get('email', '').strip()
#             subject = request.form.get('subject', '').strip() or "No subject"
#             message = request.form.get('message', '').strip()

#             if not all([name, email, message]):
#                 return jsonify({
#                     'success': False,
#                     'error': 'Name, email, and message are required!'
#                 }), 400

#             db = get_db()

#             existing = db.execute('''
#                 SELECT 1 FROM messages 
#                 WHERE name=? AND email=? AND message=?
#                 AND timestamp > datetime('now', '-10 minutes')
#                 LIMIT 1
#             ''', (name, email, message)).fetchone()

#             if not existing:
#                 db.execute(
#                     'INSERT INTO messages (name, email, subject, message) VALUES (?, ?, ?, ?)',
#                     (name, email, subject, message)
#                 )
#                 db.commit()

#                 # ✅ Send email notification to admin
#                 try:
#                     msg = Message(
#                         subject=f"📩 New Contact Form Submission: {subject}",
#                         recipients=[app.config['MAIL_USERNAME']],
#                         body=f"""
# You have received a new message from your portfolio contact form.

# 👤 Name: {name}
# 📧 Email: {email}
# 📝 Subject: {subject}
# 💬 Message:
# {message}

# Regards,
# Your Flask Portfolio Bot 🚀
#                         """
#                     )
#                     mail.send(msg)
#                     print("✅ Email sent successfully!")
#                 except Exception as e:
#                     print(f"⚠️ Email not sent: {e}")

#             return jsonify({'success': True, 'redirect': url_for('thank_you')})

#         except Exception as e:
#             print(f"❌ Error: {e}")
#             return jsonify({'success': False, 'error': 'Server error. Please try again later.'}), 500

# @app.route('/thank-you')
# def thank_you():
#     response = make_response(render_template('thank_you.html'))
#     response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
#     response.headers['Pragma'] = 'no-cache'
#     response.headers['Expires'] = '0'
#     return response

# # ----------------------------
# # Admin routes
# # ----------------------------
# @app.route('/admin')
# def admin_home():
#     if session.get('is_admin'):
#         return redirect(url_for('view_messages'))
#     return redirect(url_for('admin_login'))

# @app.route('/admin/login', methods=['GET', 'POST'])
# @csrf.exempt
# def admin_login():
#     error = None
#     if request.method == 'POST':
#         password = request.form.get('password')
#         if password == ADMIN_PASSWORD:
#             session['is_admin'] = True
#             return redirect(url_for('view_messages'))
#         else:
#             error = "Invalid password"
#     return render_template('admin_login.html', error=error)

# @app.route('/admin/messages')
# @admin_required
# def view_messages():
#     db = get_db()
#     messages = db.execute('''
#         SELECT name, email, subject, message, timestamp 
#         FROM messages 
#         ORDER BY timestamp DESC
#     ''').fetchall()

#     messages_list = [dict(msg) for msg in messages]
#     return render_template('admin_messages.html', messages=messages_list)

# @app.route('/admin/logout')
# def admin_logout():
#     session.pop('is_admin', None)
#     return redirect(url_for('index'))

# # ----------------------------
# # Debug routes (optional)
# # ----------------------------
# @app.route('/debug/messages')
# def debug_messages():
#     db = get_db()
#     messages = db.execute('SELECT * FROM messages').fetchall()
#     return jsonify([dict(msg) for msg in messages])

# @app.route('/debug/session')
# def debug_session():
#     return jsonify(dict(session))

# # ----------------------------
# # Main entry point
# # ----------------------------
# if __name__ == '__main__':
#     if not DATABASE.exists():
#         init_db()

#     with app.app_context():
#         db = get_db()
#         db.execute("""
#             DELETE FROM messages 
#             WHERE id NOT IN (
#                 SELECT MIN(id)
#                 FROM messages
#                 GROUP BY name, email, message, strftime('%Y-%m-%d %H:%M', timestamp)
#             )
#         """)
#         db.commit()

#     app.run(debug=True, port=5000)






from flask import Flask, render_template, request, redirect, url_for, session, jsonify, g, make_response
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail, Message
from functools import wraps
import sqlite3
from pathlib import Path
import os
from dotenv import load_dotenv

# ----------------------------
# Load environment variables
# ----------------------------
load_dotenv()

app = Flask(__name__)

# Secure configuration
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')
csrf = CSRFProtect(app)
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'Abhi@')

# ----------------------------
# Flask-Mail Configuration
# ----------------------------
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

mail = Mail(app)

# ----------------------------
# Database setup
# ----------------------------
BASE_DIR = Path(__file__).parent
DATABASE = BASE_DIR / 'messages.db'

def get_db():
    if not hasattr(g, '_database'):
        g._database = sqlite3.connect(DATABASE)
        g._database.row_factory = sqlite3.Row
        g._database.execute("PRAGMA foreign_keys = ON")
    return g._database

@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    """Initialize messages table"""
    try:
        with app.app_context():
            db = get_db()
            db.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    subject TEXT,
                    message TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(name, email, message, timestamp) ON CONFLICT IGNORE
                )
            """)
            db.commit()
        print("✓ Database initialized successfully")
    except Exception as e:
        print(f"✗ Database initialization failed: {e}")

# ----------------------------
# Authentication decorator
# ----------------------------
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# ----------------------------
# Routes
# ----------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
@csrf.exempt
def submit():
    """Handle contact form submission"""
    if request.method == 'POST':
        try:
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            subject = request.form.get('subject', '').strip() or "No subject"
            message = request.form.get('message', '').strip()

            if not all([name, email, message]):
                return jsonify({
                    'success': False,
                    'error': 'Name, email, and message are required!'
                }), 400

            db = get_db()

            existing = db.execute('''
                SELECT 1 FROM messages 
                WHERE name=? AND email=? AND message=?
                AND timestamp > datetime('now', '-10 minutes')
                LIMIT 1
            ''', (name, email, message)).fetchone()

            if not existing:
                db.execute(
                    'INSERT INTO messages (name, email, subject, message) VALUES (?, ?, ?, ?)',
                    (name, email, subject, message)
                )
                db.commit()

                # ✅ Send email notification to admin
                try:
                    msg = Message(
                        subject=f"📩 New Contact Form Submission: {subject}",
                        recipients=[app.config['MAIL_USERNAME']],
                        body=f"""
You have received a new message from your portfolio contact form.

👤 Name: {name}
📧 Email: {email}
📝 Subject: {subject}
💬 Message:
{message}

Regards,
Your Flask Portfolio Bot 🚀
                        """
                    )
                    mail.send(msg)
                    print("✅ Email sent successfully!")
                except Exception as e:
                    print(f"⚠️ Email not sent: {e}")

            return jsonify({'success': True, 'redirect': url_for('thank_you')})

        except Exception as e:
            print(f"❌ Error: {e}")
            return jsonify({'success': False, 'error': 'Server error. Please try again later.'}), 500

@app.route('/thank-you')
def thank_you():
    response = make_response(render_template('thank_you.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# ----------------------------
# Admin routes
# ----------------------------
@app.route('/admin')
def admin_home():
    if session.get('is_admin'):
        return redirect(url_for('view_messages'))
    return redirect(url_for('admin_login'))

@app.route('/admin/login', methods=['GET', 'POST'])
@csrf.exempt
def admin_login():
    error = None
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['is_admin'] = True
            return redirect(url_for('view_messages'))
        else:
            error = "Invalid password"
    return render_template('admin_login.html', error=error)

@app.route('/admin/messages')
@admin_required
def view_messages():
    db = get_db()
    messages = db.execute('''
        SELECT name, email, subject, message, timestamp 
        FROM messages 
        ORDER BY timestamp DESC
    ''').fetchall()

    messages_list = [dict(msg) for msg in messages]
    return render_template('admin_messages.html', messages=messages_list)

@app.route('/admin/logout')
def admin_logout():
    session.pop('is_admin', None)
    return redirect(url_for('index'))

# ----------------------------
# Debug routes (optional)
# ----------------------------
@app.route('/debug/messages')
def debug_messages():
    db = get_db()
    messages = db.execute('SELECT * FROM messages').fetchall()
    return jsonify([dict(msg) for msg in messages])

@app.route('/debug/session')
def debug_session():
    return jsonify(dict(session))

# ----------------------------
# Main entry point (Local + Vercel)
# ----------------------------
def prepare_database():
    """Ensure database exists and remove duplicate messages"""
    if not DATABASE.exists():
        init_db()

    with app.app_context():
        db = get_db()
        db.execute("""
            DELETE FROM messages 
            WHERE id NOT IN (
                SELECT MIN(id)
                FROM messages
                GROUP BY name, email, message, strftime('%Y-%m-%d %H:%M', timestamp)
            )
        """)
        db.commit()

# Local run
if __name__ == '__main__':
    prepare_database()
    app.run(debug=True, port=5000)
else:
    # Vercel entry point
    prepare_database()
    app = app
