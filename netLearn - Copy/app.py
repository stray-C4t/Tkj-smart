import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = 'kunci_rahasia_kamu_di_sini'

# ==============================
# 🔥 DATABASE CONFIG (WAJIB)
# ==============================
basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(basedir, 'database.db')

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ==============================
# 🔥 AUTO TAMBAH COLUMN (AMAN)
# ==============================
conn = get_db_connection()
try:
    conn.execute("ALTER TABLE user_progress ADD COLUMN updated_at TEXT")
    conn.commit()
except:
    pass
conn.close()


# ==============================
# HOME
# ==============================
@app.route('/')
def index():
    return render_template('index.html')


# ==============================
# LOGIN
# ==============================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute(
            'SELECT * FROM users WHERE username=? AND password=?',
            (username, password)
        ).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['nama_lengkap'] = user['nama_lengkap']
            session['role'] = user['role']

            return redirect('/dashboard')
        else:
            flash('Username / Password salah!')
            return redirect('/login')

    return render_template('login.html')


# ==============================
# LOGOUT
# ==============================
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


# ==============================
# DASHBOARD
# ==============================
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    conn = get_db_connection()

    progress_data = conn.execute('''
        SELECT up.progress, m.judul, m.deskripsi_singkat, m.id
        FROM user_progress up
        JOIN modul m ON up.modul_id = m.id
        WHERE up.user_id = ?
        ORDER BY up.id DESC
        LIMIT 1
    ''', (user_id,)).fetchone()

    rekomendasi = conn.execute('''
        SELECT * FROM modul ORDER BY RANDOM() LIMIT 3
    ''').fetchall()

    conn.close()

    if progress_data:
        progres = progress_data['progress']
        materi = progress_data['judul']
        deskripsi = progress_data['deskripsi_singkat']
        modul_id = progress_data['id']
    else:
        progres = 0
        materi = None
        deskripsi = None
        modul_id = None

    return render_template(
        'dashboard.html',
        progres=progres,
        materi=materi,
        deskripsi=deskripsi,
        modul_id=modul_id,
        rekomendasi=rekomendasi
    )


# ==============================
# MODUL
# ==============================
@app.route('/modul/<kat>')
def show_modul(kat):
    conn = get_db_connection()
    materi = conn.execute(
        'SELECT * FROM modul WHERE kategori=?',
        (kat.lower(),)
    ).fetchall()
    conn.close()

    return render_template('modul_kategori.html', materi_list=materi)


@app.route('/modul/baca/<int:id>')
def baca_modul(id):
    conn = get_db_connection()

    materi = conn.execute(
        'SELECT * FROM modul WHERE id=?',
        (id,)
    ).fetchone()

    rekomendasi = conn.execute(
        'SELECT * FROM modul WHERE id!=? LIMIT 3',
        (id,)
    ).fetchall()

    conn.close()

    return render_template('baca_modul.html', m=materi, rekomendasi=rekomendasi)


# ==============================
# UPDATE PROGRESS
# ==============================
@app.route('/update-progress', methods=['POST'])
def update_progress():
    if 'user_id' not in session:
        return {"status": "error"}

    data = request.get_json()
    user_id = session['user_id']
    modul_id = data['modul_id']
    progress = data['progress']
    now = datetime.now().strftime('%Y-%m-%d')

    conn = get_db_connection()

    existing = conn.execute(
        'SELECT * FROM user_progress WHERE user_id=? AND modul_id=?',
        (user_id, modul_id)
    ).fetchone()

    if existing:
        conn.execute(
            '''
            UPDATE user_progress 
            SET progress=?, updated_at=? 
            WHERE user_id=? AND modul_id=?
            ''',
            (progress, now, user_id, modul_id)
        )
    else:
        conn.execute(
            '''
            INSERT INTO user_progress 
            (user_id, modul_id, progress, updated_at)
            VALUES (?, ?, ?, ?)
            ''',
            (user_id, modul_id, progress, now)
        )

    conn.commit()
    conn.close()

    return {"status": "success"}


# ==============================
# ACCOUNT (GRAFIK)
# ==============================
@app.route('/account')
def account():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    conn = get_db_connection()

    # 🔥 BAR CHART (5 hari)
    labels = []
    data = []

    for i in range(4, -1, -1):
        hari = datetime.now() - timedelta(days=i)
        tanggal = hari.strftime('%Y-%m-%d')

        labels.append(hari.strftime('%d/%m'))

        jumlah = conn.execute('''
            SELECT COUNT(*) FROM user_progress
            WHERE user_id=? AND DATE(updated_at)=?
        ''', (user_id, tanggal)).fetchone()[0]

        data.append(jumlah)

    # 🔥 PIE CHART
    kategori = conn.execute('''
        SELECT m.kategori, COUNT(*) as total
        FROM user_progress up
        JOIN modul m ON up.modul_id = m.id
        WHERE up.user_id=? AND up.progress=100
        GROUP BY m.kategori
    ''', (user_id,)).fetchall()

    pie_labels = [k['kategori'] for k in kategori]
    pie_data = [k['total'] for k in kategori]

    # 🔥 STATISTIK
    total_poin = conn.execute('''
        SELECT SUM(score) FROM user_quiz WHERE user_id=?
    ''', (user_id,)).fetchone()[0] or 0

    kuis_selesai = conn.execute('''
        SELECT COUNT(*) FROM user_quiz WHERE user_id=?
    ''', (user_id,)).fetchone()[0]

    modul_selesai = conn.execute('''
        SELECT COUNT(*) FROM user_progress 
        WHERE user_id=? AND progress=100
    ''', (user_id,)).fetchone()[0]

    conn.close()

    return render_template(
        'account.html',
        poin=total_poin,
        kuis_selesai=kuis_selesai,
        modul_selesai=modul_selesai,
        bar_labels=labels,
        bar_data=data,
        pie_labels=pie_labels,
        pie_data=pie_data
    )


# ==============================
# SUBMIT QUIZ
# ==============================
@app.route('/submit-quiz', methods=['POST'])
def submit_quiz():
    if 'user_id' not in session:
        return {"status": "error"}

    data = request.get_json()
    user_id = session['user_id']
    quiz_id = data['quiz_id']
    score = data['score']
    max_score = data['max_score']

    conn = get_db_connection()

    existing = conn.execute(
        'SELECT * FROM user_quiz WHERE user_id=? AND quiz_id=?',
        (user_id, quiz_id)
    ).fetchone()

    if existing:
        if score > existing['score']:
            conn.execute(
                'UPDATE user_quiz SET score=? WHERE user_id=? AND quiz_id=?',
                (score, user_id, quiz_id)
            )
    else:
        conn.execute(
            'INSERT INTO user_quiz (user_id, quiz_id, score, max_score) VALUES (?, ?, ?, ?)',
            (user_id, quiz_id, score, max_score)
        )

    conn.commit()
    conn.close()

    return {"status": "success"}


# ==============================
# RUN
# ==============================
if __name__ == '__main__':
    app.run(debug=True)
