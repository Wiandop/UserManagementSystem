from flask import Flask, render_template, request
import sqlite3

app = Flask("User Management System")

# Function to get a database connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    return conn

# Initialize the database if it doesn't exist
def init_db():
    conn = get_db_connection()

    table_exists = conn.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='users'
    """).fetchone()

    if not table_exists:
        db = open('init-db.sql', 'r')
        conn.executescript(db.read())
        conn.commit()
        db.close()
    
    conn.close()

# Main page
@app.route('/')
def index():
    return render_template('index.html')

# Page with the list of active users
@app.route('/users')
def get_active_users():
    conn = get_db_connection()
    
    # Fetch all active users
    users = conn.execute('''
        SELECT id, login, money_amount, card_number 
        FROM users 
        WHERE status = 1
    ''').fetchall()
    
    conn.close()
    
    return render_template('users.html', users=users)

# Search user by login
@app.route('/by-login')
def get_user_by_login():
    login = request.args.get('login', '')
    
    if not login:
        return render_template('error.html', error_message="Please provide a login parameter"), 400
    
    conn = get_db_connection()
    user = conn.execute('''
        SELECT id, login, money_amount, card_number 
        FROM users 
        WHERE login = ? AND status = 1
    ''', (login,)).fetchone()
    
    conn.close()
    
    if user is None:
        return render_template('error.html', error_message=f"No active user found with login: {login}"), 404
    
    return render_template('user_detail.html', user=user)

# Search user by ID
@app.route('/by-id')
def get_user_by_id():
    user_id = request.args.get('id', 0)
    
    if not user_id.isdigit():
        return render_template('error.html', error_message="Invalid ID parameter"), 400
    
    user_id = int(user_id)

    conn = get_db_connection()
    user = conn.execute('''
        SELECT id, login, money_amount, card_number 
        FROM users 
        WHERE id = ? AND status = 1
    ''', (user_id,)).fetchone()
    
    conn.close()
    
    if user is None:
        return render_template('error.html', error_message=f"No active user found with ID: {user_id}"), 404
    
    return render_template('user_detail.html', user=user)

if __name__ == '__main__':
    init_db()
    app.run(debug=False, host='localhost', port=8000)