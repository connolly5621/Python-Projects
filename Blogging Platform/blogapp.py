from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Database initialization
def init_db():
    try:
        conn = sqlite3.connect('blog.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                date_posted TEXT NOT NULL
            );
        ''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred while initializing the database: {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM posts ORDER BY id DESC')
    posts = cursor.fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/new', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        date_posted = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn = sqlite3.connect('blog.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO posts (title, content, date_posted) VALUES (?, ?, ?)', (title, content, date_posted))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('create.html')
    
@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit(post_id):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        cursor.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (title, content, post_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    cursor.execute('SELECT * FROM posts WHERE id =?', (post_id,))
    post = cursor.fetchone()
    conn.close()

    if post:
        return render_template('edit.html', post=post)
    else:
        return 'Post not found', 404
    
@app.route('/delete/<int:post_id>')
def delete(post_id):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port = 5001)