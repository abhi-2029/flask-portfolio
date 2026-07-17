

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, g, make_response
from flask_wtf.csrf import CSRFProtect
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

# Database setup
BASE_DIR = Path(__file__).parent
DATABASE = BASE_DIR / 'messages.db'
DATABASE_URL = os.getenv('DATABASE_URL')

# ----------------------------
# Database connection handling
# ----------------------------
def get_db():
    if not hasattr(g, '_database'):
        if DATABASE_URL:
            import psycopg2
            import psycopg2.extras
            url = DATABASE_URL
            if url.startswith("postgres://"):
                url = url.replace("postgres://", "postgresql://", 1)
            g._database = psycopg2.connect(url)
            g._is_postgres = True
        else:
            g._database = sqlite3.connect(DATABASE)
            g._database.row_factory = sqlite3.Row
            g._database.execute("PRAGMA foreign_keys = ON")
            g._is_postgres = False
    return g._database

@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def db_execute(query, args=(), fetchall=False, fetchone=False, commit=False):
    db = get_db()
    is_postgres = getattr(g, '_is_postgres', False)
    
    if is_postgres:
        # Translate SQLite syntax to PostgreSQL
        query = query.replace('?', '%s')
        query = query.replace("datetime('now', '-10 minutes')", "NOW() - INTERVAL '10 minutes'")
        query = query.replace("strftime('%Y-%m-%d %H:%M', timestamp)", "to_char(timestamp, 'YYYY-MM-DD HH24:MI')")
        query = query.replace("INTEGER PRIMARY KEY AUTOINCREMENT", "SERIAL PRIMARY KEY")
        
        import psycopg2.extras
        cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(query, args)
        if commit:
            db.commit()
        
        rv = None
        if fetchall:
            rv = cur.fetchall()
        elif fetchone:
            rv = cur.fetchone()
        cur.close()
        return rv
    else:
        cur = db.execute(query, args)
        if commit:
            db.commit()
        
        rv = None
        if fetchall:
            rv = cur.fetchall()
        elif fetchone:
            rv = cur.fetchone()
        cur.close()
        return rv

def init_db():
    """Initialize messages table"""
    try:
        with app.app_context():
            db_execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    subject TEXT,
                    message TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(name, email, message, timestamp)
                )
            """, commit=True)
        print("[OK] Database initialized successfully")
    except Exception as e:
        print(f"[ERROR] Database initialization failed: {e}")

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
            subject = request.form.get('subject', '').strip()
            message = request.form.get('message', '').strip()

            # Validate fields
            if not all([name, email, message]):
                return jsonify({
                    'success': False,
                    'error': 'Name, email, and message are required!'
                }), 400

            db = get_db()

            # Avoid duplicates in last 10 minutes
            existing = db_execute('''
                SELECT 1 FROM messages 
                WHERE name=? AND email=? AND message=?
                AND timestamp > datetime('now', '-10 minutes')
                LIMIT 1
            ''', (name, email, message), fetchone=True)

            if not existing:
                db_execute(
                    'INSERT INTO messages (name, email, subject, message) VALUES (?, ?, ?, ?)',
                    (name, email, subject, message),
                    commit=True
                )

            return jsonify({
                'success': True,
                'redirect': url_for('thank_you')
            })
        except Exception:
            return jsonify({
                'success': False,
                'error': 'Server error. Please try again later.'
            }), 500

@app.route('/thank-you')
def thank_you():
    """Thank you page with cache disabled"""
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
    """Shortcut route for admin"""
    if session.get('is_admin'):
        return redirect(url_for('view_messages'))
    return redirect(url_for('admin_login'))

@app.route('/admin/login', methods=['GET', 'POST'])
@csrf.exempt
def admin_login():
    """Admin login"""
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
    """View all messages"""
    messages = db_execute('''
        SELECT name, email, subject, message, timestamp 
        FROM messages 
        ORDER BY timestamp DESC
    ''', fetchall=True)

    messages_list = [dict(msg) for msg in messages]
    return render_template('admin_messages.html', messages=messages_list)

@app.route('/admin/logout')
def admin_logout():
    """Logout admin"""
    session.pop('is_admin', None)
    return redirect(url_for('index'))

# ----------------------------
# Main entry point
# ----------------------------
if __name__ == '__main__':
    if not DATABASE.exists():
        init_db()

    # Configuration sanity checks
    # If not running in debug/dev, raise error for insecure defaults
    is_debug = os.getenv('FLASK_DEBUG', 'false').lower() in ('true', '1') or app.debug
    if not is_debug:
        if app.secret_key == 'default_secret_key':
            raise RuntimeError("CRITICAL: Flask SECRET_KEY cannot be default_secret_key in production!")
        if ADMIN_PASSWORD == 'Abhi@':
            raise RuntimeError("CRITICAL: ADMIN_PASSWORD cannot be Abhi@ in production!")

    # Remove duplicate entries on startup
    with app.app_context():
        db_execute("""
            DELETE FROM messages 
            WHERE id NOT IN (
                SELECT MIN(id)
                FROM messages
                GROUP BY name, email, message, strftime('%Y-%m-%d %H:%M', timestamp)
            )
        """, commit=True)

    app.run(debug=True, port=5000)

