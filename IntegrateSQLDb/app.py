#Integrate a SQLite database with Flask to perform CRUD operations on a list of items.
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database configuration
DATABASE = 'items.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This enables column access by name
    return conn

# Create table if it doesn't exist
def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT
            )
        ''')
        db.commit()

# Initialize the database
init_db()

@app.route('/')
def index():
    db = get_db()
    cur = db.execute('SELECT * FROM items')
    items = cur.fetchall()
    return render_template('index.html', items=items)

@app.route('/create', methods=['GET', 'POST'])
def create_item():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']

        db = get_db()
        db.execute('INSERT INTO items (name, description) VALUES (?, ?)', (name, description))
        db.commit()

        return redirect(url_for('index'))
    
    return render_template('create.html')

@app.route('/update/<int:item_id>', methods=['GET', 'POST'])
def update_item(item_id):
    db = get_db()
    cur = db.execute('SELECT * FROM items WHERE id = ?', (item_id,))
    item = cur.fetchone()

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']

        db.execute('UPDATE items SET name = ?, description = ? WHERE id = ?', (name, description, item_id))
        db.commit()

        return redirect(url_for('index'))

    return render_template('update.html', item=item)

@app.route('/delete/<int:item_id>')
def delete_item(item_id):
    db = get_db()
    db.execute('DELETE FROM items WHERE id = ?', (item_id,))
    db.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
