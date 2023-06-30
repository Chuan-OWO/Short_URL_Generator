from flask import Flask, request, redirect, render_template,jsonify
import sqlite3
import random
import string

app = Flask(__name__)



# 創建短網址的 SQLite 資料庫
conn = sqlite3.connect('shorturls.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS urls
(id INTEGER PRIMARY KEY AUTOINCREMENT,long_url TEXT, short_code TEXT,create_time datetime not null DEFAULT (strftime('%Y-%m-%d', 'now', 'localtime')))''')

conn.commit()

# ask
@app.route('/')
@app.route('/ask')
def index():
    return render_template('index.html')

# 短網址轉址路由
@app.route('/shout_url/<short_code>')
def redirect_to_url(short_code):
    conn = sqlite3.connect('shorturls.db')
    c = conn.cursor()
    c.execute("SELECT long_url FROM urls WHERE short_code=?", (short_code,))
    result = c.fetchone()
    print(result)
    print(result[0])
    if result:
        long_url = result[0]
        return redirect(long_url)
    else:
        return "Invalid short URL"

# 短網址的路由
@app.route('/api/create', methods=['POST'])
def create_short_url():
    output = {
        'success': False,
        'code': '1000',
        'error': '輸入資料失敗'
    }
    data = request.json
    long_url = str(data['url'])
    print (long_url)

    short_code = generate_short_code()
    conn = sqlite3.connect('shorturls.db')
    c = conn.cursor()
    c.execute("SELECT short_code FROM urls WHERE long_url=?", (long_url,))
    short_code_row =c.fetchone()
    print(short_code_row)
    if short_code_row is not None:
        short_code = short_code_row[0]
        short_url = request.host_url + 'shout_url/' + short_code
        output = {'success': True, 'code': '0001', 'short_url': short_url}
        return jsonify(output)
    else:
        c.execute("INSERT INTO urls (long_url, short_code) VALUES (?, ?)", (long_url, short_code))
        conn.commit()
        short_url = request.host_url + 'shout_url/' + short_code
        output = {'success': True, 'code': '0002', 'short_url': short_url}
        return jsonify(output)

# 生成隨機的短網址代碼
def generate_short_code():
    characters = string.ascii_letters + string.digits
    short_code = ''.join(random.choices(characters, k=8))
    return short_code

#route logs
@app.route('/logs')
def logs():
    conn = sqlite3.connect('shorturls.db')
    c = conn.cursor()
    c.execute("SELECT * from urls")
    logs = c.fetchall()
    conn.close()
    return render_template('logs.html',logs=logs)

#route delete 
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    delete_url(id)
    return redirect('/logs')

#delete id
def delete_url(id):
    conn = sqlite3.connect('shorturls.db')
    c = conn.cursor()
    c.execute('DELETE FROM urls WHERE id = ?', (id,))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    app.run(debug=True)
