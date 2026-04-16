import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = 'kunci_rahasia_kamu_di_sini' # Wajib ada untuk session

basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(basedir, 'database.db')

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# 🔥 INI TEMPATNYA
conn = get_db_connection()
try:
    conn.execute("ALTER TABLE user_progress ADD COLUMN updated_at TEXT")
    conn.commit()
except:
    pass
conn.close()

# Fungsi bantuan untuk koneksi ke database
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row # Agar data bisa dipanggil dengan nama kolom (contoh: user['role'])
    return conn

@app.route('/')
def index():
    # Data Fitur (Gambar 3)
    fitur_list = [
        {"judul": "Simulasi Jaringan", "desc": "Praktik konfigurasi router dan switch secara virtual.", "img": "https://picsum.photos/400/200?jaringan"},
        {"judul": "Modul TKJ", "desc": "Materi lengkap dari kelas X hingga XII.", "img": "https://picsum.photos/400/200?modul"},
        {"judul": "Video Tutorial", "desc": "Belajar teknis lewat panduan visual yang jelas.", "img": "https://picsum.photos/400/200?video"}
    ]

    # Data Guru (Gambar 4) - Kita ambil 3 untuk tampilan slider statis
    guru_all = [
        {"nama": "Pak Husni", "mapel": "Komputer Jaringan", "img": "https://i.pravatar.cc/150?u=5"},
    ]

    # Data FAQ (Gambar 5)
    faq_list = [
        {"tanya": "Apa itu TKJ Smart?", "jawab": "udah dijelasin dari awal masih aja nanya."},
    ]

    return render_template('index.html', fitur=fitur_list, guru=guru_all, faq=faq_list)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', 
                            (username, password)).fetchone()
        conn.close()

        if user:
            session['logged_in'] = True
            session['username'] = user['username']
            session['role'] = user['role']
            session['nama_lengkap'] = user['nama_lengkap']
            session['email'] = user['email']
            session['user_id'] = user['id']
            
            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('dashboard'))
        else:
            # Ganti teks return lama dengan ini:
            flash('Username atau Password salah!', 'danger') 
            return redirect(url_for('login')) # Kembali ke halaman login
            
    return render_template('login.html')
    
# --- LOGOUT ---
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
    
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')

    user_id = session['user_id']
    conn = get_db_connection()

    # 🔥 ambil progress terakhir user
    progress_data = conn.execute('''
        SELECT up.progress, m.judul, m.deskripsi_singkat, m.id
        FROM user_progress up
        JOIN modul m ON up.modul_id = m.id
        WHERE up.user_id = ?
        ORDER BY up.id DESC
        LIMIT 1
    ''', (user_id,)).fetchone()

    # 🔥 ambil rekomendasi random
    rekomendasi = conn.execute('''
        SELECT * FROM modul
        ORDER BY RANDOM()
        LIMIT 3
    ''').fetchall()

    conn.close()

    # 🔥 jika belum ada progress
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
    
@app.route('/modul/<kat>')
def show_modul(kat):
    kategori_dicari = kat.lower().strip() # Tambahkan strip() untuk hapus spasi tak terlihat
    
    conn = get_db_connection()
    # Debug: Cek apakah koneksi berhasil dan tabel ada isinya
    cek_isi = conn.execute('SELECT COUNT(*) FROM modul').fetchone()
    print(f"Total baris di tabel modul: {cek_isi[0]}") 
    
    materi = conn.execute('SELECT * FROM modul WHERE kategori = ?', (kategori_dicari,)).fetchall()
    conn.close()
    
    print(f"Mencari: '{kategori_dicari}', Hasil: {len(materi)} materi")
    
    return render_template('modul_kategori.html', 
                           materi_list=materi, 
                           nama_kategori=kat.capitalize())
    
@app.route('/modul/<int:modul_id>')
def detail_modul(modul_id):
    conn = get_db_connection()
    materi = conn.execute('SELECT * FROM modul WHERE id = ?', (modul_id,)).fetchone()
    conn.close()
    return render_template('detail_modul.html', materi=materi)    
    
@app.route('/modul/baca/<int:id>')
def baca_modul(id):
    conn = get_db_connection()
    # Ambil data materi berdasarkan ID
    materi = conn.execute('SELECT * FROM modul WHERE id = ?', (id,)).fetchone()
    # (Opsional) Ambil modul lain untuk navigasi di bawah
    rekomendasi = conn.execute('SELECT * FROM modul WHERE id != ? LIMIT 3', (id,)).fetchall()
    conn.close()
    
    if materi is None:
        return "Materi tidak ditemukan", 404
        
    return render_template('baca_modul.html', m=materi, rekomendasi=rekomendasi)

@app.route('/video')
def video_page():
    # Ambil input dari form search kamu: <input name="q">
    search_query = request.args.get('q', '')
    
    conn = get_db_connection()
    
    if search_query:
        # Cari berdasarkan judul atau deskripsi
        query = "SELECT * FROM video WHERE judul LIKE ? OR deskripsi LIKE ?"
        search_term = f"%{search_query}%"
        videos = conn.execute(query, (search_term, search_term)).fetchall()
    else:
        # Jika tidak ada search, tampilkan semua
        videos = conn.execute('SELECT * FROM video').fetchall()
        
    conn.close()
    
    # Kirim data ke file HTML kamu
    return render_template('video.html', videos=videos)

# Route untuk menonton video (ketika tombol 'Tonton Sekarang' diklik)
    
@app.route('/video/watch/<int:id>')
def watch_video(id):
    conn = get_db_connection()
    # Ambil video utama
    video = conn.execute('SELECT * FROM video WHERE id = ?', (id,)).fetchone()
    # Ambil video lainnya sebagai saran di samping (Sidebar)
    sidebar_videos = conn.execute('SELECT * FROM video WHERE id != ? LIMIT 4', (id,)).fetchall()
    conn.close()
    
    if video is None:
        return "Video tidak ditemukan", 404
        
    return render_template('video_watch.html', v=video, saran=sidebar_videos)
    
@app.route('/quiz')
def quiz_menu():
    conn = get_db_connection()
    # Mengambil data kuis untuk menu
    quizzes = conn.execute('SELECT * FROM quiz_list').fetchall()
    conn.close()
    # Pastikan nama variabelnya 'quiz_list' sesuai {% for q in quiz_list %} di HTML-mu
    return render_template('quiz_menu.html', quiz_list=quizzes)
    
@app.route('/quiz/kerjakan/<int:quiz_id>')
def quiz_pengerjaan(quiz_id):
    conn = get_db_connection()
    # Ambil soal dari database
    questions_raw = conn.execute('SELECT * FROM quiz_questions WHERE quiz_id = ?', (quiz_id,)).fetchall()
    
    # Ambil judul untuk header
    info_kuis = conn.execute('SELECT judul FROM quiz_list WHERE id = ?', (quiz_id,)).fetchone()
    conn.close()

    # KONVERSI: Mengubah baris database ke format Objek untuk JS kamu
    soal_list_js = []
    for q in questions_raw:
        soal_list_js.append({
            "id": q['id'],
            "tanya": q['pertanyaan'],
            "opsi": [q['opsi_a'], q['opsi_b'], q['opsi_c'], q['opsi_d']],
            "kunci": q['jawaban_benar'] # Pastikan isinya teks jawaban yang sama dengan opsi
        })

    return render_template('quiz_kerjakan.html', 
                           soal_list=soal_list_js, 
                           judul=info_kuis['judul'] if info_kuis else "Quiz")

from datetime import datetime, timedelta

@app.route('/account')
def account():
    conn = get_db_connection()

    user_id = session.get('user_id')

    # =========================
    # 📊 BAR CHART (5 HARI)
    # =========================
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

    # =========================
    # 🍩 PIE CHART (KATEGORI)
    # =========================
    kategori = conn.execute('''
        SELECT m.kategori, COUNT(*) as total
        FROM user_progress up
        JOIN modul m ON up.modul_id = m.id
        WHERE up.user_id=?
        GROUP BY m.kategori
    ''', (user_id,)).fetchall()

    pie_labels = [k['kategori'] for k in kategori]
    pie_data = [k['total'] for k in kategori]

    # =========================
    # DATA USER (SEBELUMNYA)
    # =========================
    user_data = {
        "sekolah": "SMKN 2 Probolinggo",
        "email": "abimanyu@example.com",
        "poin": 1250,
        "kuis_selesai": 12,
        "progres": 11
    }

    conn.close()

    return render_template(
        'account.html',
        user=user_data,
        bar_labels=labels,
        bar_data=data,
        pie_labels=pie_labels,
        pie_data=pie_data
    )

# --- ADMIN DASHBOARD (PROTECTED) ---
@app.route('/admin')
def admin_dashboard():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    modules = conn.execute('SELECT * FROM modul').fetchall()
    videos = conn.execute('SELECT * FROM video').fetchall()
    users = conn.execute('SELECT * FROM users').fetchall()
    # Ambil Judul Quiz + Hitung Jumlah Soalnya
    quizzes = conn.execute('''
        SELECT ql.*, COUNT(qq.id) as jumlah_soal 
        FROM quiz_list ql 
        LEFT JOIN quiz_questions qq ON ql.id = qq.quiz_id 
        GROUP BY ql.id
    ''').fetchall()
    conn.close()
    return render_template('admin_dashboard.html', modules=modules, videos=videos, users=users, quizzes=quizzes)

@app.route('/admin/add-modul')
def form_add_modul():
    return render_template('admin_form_modul.html', is_edit=False)

@app.route('/admin/add-video')
def form_add_video():
    return render_template('admin_form_video.html', is_edit=False)
    
# --- HALAMAN TAMBAH AKUN ---
@app.route('/admin/add-account')
def form_add_account():
    return render_template('admin_form_akun.html', is_edit=False)
        

@app.route('/admin/add-quiz')
def add_quiz():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))

    return render_template(
        'admin_full_quiz.html',
        quiz=None,
        questions=[],
        is_edit=False
    )    
    
# --- FUNGSI HAPUS ---

# Tambahkan juga route untuk hapus user agar dashboard fungsional
# --- DELETE USER ---
@app.route('/admin/delete-user/<int:id>')
def delete_user(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete-modul/<int:id>')
def delete_modul(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM modul WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete-video/<int:id>')
def delete_video(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM video WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_dashboard'))
    
# --- HAPUS SELURUH LATIHAN (JUDUL & SEMUA SOALNYA) ---
@app.route('/admin/delete-latihan/<int:id>')
def delete_latihan(id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    conn.execute('DELETE FROM quiz_list WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Latihan Soal berhasil dihapus!')
    return redirect(url_for('admin_dashboard'))

# --- HAPUS SATU SOAL SAJA ---
@app.route('/admin/delete-question/<int:id>/<int:quiz_id>')
def delete_question(id, quiz_id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    conn.execute('DELETE FROM quiz_questions WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Satu soal berhasil dihapus!')
    # Kembali ke halaman input soal agar bisa lanjut edit
    return redirect(url_for('add_questions', quiz_id=quiz_id))

# --- SAVE ACCOUNT ---
@app.route('/admin/save-account', methods=['POST'])
def save_account():
    user = request.form.get('username')
    pw = request.form.get('password')
    nama = request.form.get('nama_lengkap') # Ambil input nama
    role = request.form.get('role') # Ambil input role (admin/siswa)
    email = request.form.get('email')
    
    conn = get_db_connection()
    # Tambahkan kolom nama_lengkap dan role ke query
    conn.execute('INSERT INTO users (username, password, nama_lengkap, role) VALUES (?, ?, ?, ?)', 
                 (user, pw, nama, role))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_dashboard'))
    
@app.route('/admin/save-modul', methods=['POST'])
def save_modul():
    judul = request.form['judul']
    kategori = request.form['kategori']
    deskripsi_singkat = request.form['deskripsi_singkat']
    konten = request.form['konten']
    icon = request.form['icon'] # <--- Ambil icon
    
    conn = get_db_connection()
    conn.execute('INSERT INTO modul (judul, kategori, konten, icon) VALUES (?, ?, ?, ?)',
                 (judul, kategori, konten, icon))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_dashboard'))
   
@app.route('/admin/save-video', methods=['POST'])
def save_video():
    judul = request.form['judul']
    yt_id = request.form['youtube_id']
    durasi = request.form['durasi']
    deskripsi = request.form['deskripsi']
    
    # Otomatis buat link thumbnail dari YouTube
    # mqdefault adalah ukuran medium yang rapi untuk card
    thumb = f"https://img.youtube.com/vi/{yt_id}/mqdefault.jpg"
    
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO video (judul, youtube_id, durasi, deskripsi, thumbnail) 
        VALUES (?, ?, ?, ?, ?)
    ''', (judul, yt_id, durasi, deskripsi, thumb))
    
    conn.commit()
    conn.close()
    return redirect(url_for('admin_dashboard'))
    
from flask import request, jsonify
import json

@app.route('/admin/save-full-quiz', methods=['POST'])
def save_full_quiz():
    data = request.get_json()

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        'INSERT INTO quiz_list (judul, icon) VALUES (?, ?)',
        (data['judul'], data['icon'])
    )
    quiz_id = cur.lastrowid

    for q in data['questions']:
        cur.execute('''
            INSERT INTO quiz_questions 
            (quiz_id, pertanyaan, opsi_a, opsi_b, opsi_c, opsi_d, jawaban_benar)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            quiz_id,
            q['pertanyaan'],
            q['a'],
            q['b'],
            q['c'],
            q['d'],
            q['jawaban']
        ))

    conn.commit()
    conn.close()

    return jsonify({"status": "success"})

    conn.commit()
    conn.close()

    return jsonify({"status": "success"})
    
@app.route('/admin/edit-quiz/<int:quiz_id>')
def edit_quiz(quiz_id):
    conn = get_db_connection()

    quiz = conn.execute(
        'SELECT * FROM quiz_list WHERE id=?',
        (quiz_id,)
    ).fetchone()

    questions_raw = conn.execute(
        'SELECT * FROM quiz_questions WHERE quiz_id=?',
        (quiz_id,)
    ).fetchall()

    conn.close()

    # 🔥 FIX WAJIB
    quiz = dict(quiz) if quiz else None
    questions = [dict(q) for q in questions_raw]

    return render_template(
        'admin_full_quiz.html',
        quiz=quiz,
        questions=questions,
        is_edit=True
    )
    
@app.route('/admin/update-quiz/<int:quiz_id>', methods=['POST'])
def update_quiz(quiz_id):
    data = request.get_json()

    conn = get_db_connection()
    cur = conn.cursor()

    # update judul
    cur.execute(
        'UPDATE quiz_list SET judul=?, icon=? WHERE id=?',
        (data['judul'], data['icon'], quiz_id)
    )

    # hapus soal lama
    cur.execute('DELETE FROM quiz_questions WHERE quiz_id=?', (quiz_id,))

    # insert ulang
    for q in data['questions']:
        cur.execute('''
            INSERT INTO quiz_questions 
            (quiz_id, pertanyaan, opsi_a, opsi_b, opsi_c, opsi_d, jawaban_benar)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            quiz_id,
            q['pertanyaan'],
            q['a'],
            q['b'],
            q['c'],
            q['d'],
            q['jawaban']
        ))

    conn.commit()
    conn.close()

    return jsonify({"status": "success"})
    
@app.route('/admin/edit-modul/<int:id>')
def edit_modul(id):
    conn = get_db_connection()
    modul = conn.execute('SELECT * FROM modul WHERE id=?', (id,)).fetchone()
    conn.close()

    return render_template(
        'admin_form_modul.html',
        modul=dict(modul),
        is_edit=True
    )
    
@app.route('/admin/edit-video/<int:id>')
def edit_video(id):
    conn = get_db_connection()
    video = conn.execute('SELECT * FROM video WHERE id=?', (id,)).fetchone()
    conn.close()

    return render_template(
        'admin_form_video.html',
        video=dict(video),
        is_edit=True
    )
    
@app.route('/admin/edit-user/<int:id>')
def edit_user(id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id=?', (id,)).fetchone()
    conn.close()

    return render_template(
		'admin_form_akun.html',
		is_edit=True,
		user=dict(user)
	)
    
@app.route('/admin/update-modul/<int:id>', methods=['POST'])
def update_modul(id):
    conn = get_db_connection()
    conn.execute('''
        UPDATE modul
        SET judul=?, kategori=?, icon=?, deskripsi_singkat=?, konten=?
        WHERE id=?
    ''', (
        request.form['judul'],
        request.form['kategori'],
        request.form['icon'],
        request.form['deskripsi_singkat'],
        request.form['konten'],
        id
    ))
    conn.commit()
    conn.close()
    return redirect('/admin')
    
@app.route('/admin/update-video/<int:id>', methods=['POST'])
def update_video(id):
    conn = get_db_connection()
    conn.execute('''
        UPDATE video 
        SET judul=?, youtube_id=? 
        WHERE id=?
    ''', (
        request.form['judul'],
        request.form['youtube_id'],
        id
    ))
    conn.commit()
    conn.close()

    return redirect('/admin')
    
@app.route('/admin/update-user/<int:id>', methods=['POST'])
def update_user(id):
    conn = get_db_connection()

    if request.form['password']:  # kalau isi password
        conn.execute('''
            UPDATE users 
            SET username=?, nama_lengkap=?, email=?, role=?, password=? 
            WHERE id=?
        ''', (
            request.form['username'],
            request.form['nama_lengkap'],
            request.form['email'],
            request.form['role'],
            request.form['password'],
            id
        ))
    else:  # kalau password kosong → jangan diubah
        conn.execute('''
            UPDATE users 
            SET username=?, nama_lengkap=?, email=?, role=? 
            WHERE id=?
        ''', (
            request.form['username'],
            request.form['nama_lengkap'],
            request.form['email'],
            request.form['role'],
            id
        ))

    conn.commit()
    conn.close()

    return redirect('/admin')
    
@app.route('/update-progress', methods=['POST'])
def update_progress():
    if 'user_id' not in session:
        return {"status": "error"}

    data = request.get_json()
    modul_id = data['modul_id']
    progress = data['progress']
    user_id = session['user_id']

    conn = get_db_connection()

    # cek sudah ada atau belum
    existing = conn.execute(
        'SELECT * FROM user_progress WHERE user_id=? AND modul_id=?',
        (user_id, modul_id)
    ).fetchone()

    if existing:
        conn.execute(
            'UPDATE user_progress SET progress=? WHERE user_id=? AND modul_id=?',
            (progress, user_id, modul_id)
        )
    else:
        conn.execute(
            'INSERT INTO user_progress (user_id, modul_id, progress) VALUES (?, ?, ?)',
            (user_id, modul_id, progress)
        )
        
    now = datetime.now().strftime('%Y-%m-%d')

    conn.execute(
		'UPDATE user_progress SET progress=?, updated_at=? WHERE user_id=? AND modul_id=?',
		(progress, now, user_id, modul_id)
	)

    conn.commit()
    conn.close()

    return {"status": "success"}
    
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
        # 🔥 hanya update kalau score lebih tinggi
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

if __name__ == '__main__':
    app.run(debug=True)

