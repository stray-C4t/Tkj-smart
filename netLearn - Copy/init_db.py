import sqlite3

def init_db():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    with connection:
        # 🔥 DROP semua tabel biar clean saat init ulang
        connection.execute('DROP TABLE IF EXISTS modul')
        connection.execute('DROP TABLE IF EXISTS video')
        connection.execute('DROP TABLE IF EXISTS quiz_list')
        connection.execute('DROP TABLE IF EXISTS quiz_questions')
        connection.execute('DROP TABLE IF EXISTS users')
        connection.execute('DROP TABLE IF EXISTS user_progress')
        connection.execute('DROP TABLE IF EXISTS user_quiz')

        # =========================
        # 📚 TABEL MODUL
        # =========================
        connection.execute('''
            CREATE TABLE modul (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                judul TEXT NOT NULL,
                kategori TEXT NOT NULL,
                konten TEXT NOT NULL,
                deskripsi_singkat TEXT,
                icon TEXT
            )
        ''')

        # =========================
        # 👤 TABEL USERS (FIX: hanya 1 tabel)
        # =========================
        connection.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                nama_lengkap TEXT,
                password TEXT NOT NULL,
                role TEXT DEFAULT 'siswa',
                email TEXT
            )
        ''')

        # =========================
        # 📈 PROGRESS MODUL
        # =========================
        connection.execute('''
            CREATE TABLE user_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                modul_id INTEGER,
                progress INTEGER DEFAULT 0
            )
        ''')

        # =========================
        # 🧠 QUIZ LIST
        # =========================
        connection.execute('''
            CREATE TABLE quiz_list (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                judul TEXT NOT NULL,
                icon TEXT NOT NULL
            )
        ''')

        # =========================
        # ❓ QUIZ QUESTIONS
        # =========================
        connection.execute('''
            CREATE TABLE quiz_questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quiz_id INTEGER,
                pertanyaan TEXT NOT NULL,
                opsi_a TEXT NOT NULL,
                opsi_b TEXT NOT NULL,
                opsi_c TEXT NOT NULL,
                opsi_d TEXT NOT NULL,
                jawaban_benar TEXT NOT NULL
            )
        ''')

        # =========================
        # 🏆 USER QUIZ (FIXED)
        # =========================
        connection.execute('''
            CREATE TABLE user_quiz (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                quiz_id INTEGER,
                score INTEGER,
                max_score INTEGER
            )
        ''')

        # =========================
        # 🎥 VIDEO
        # =========================
        connection.execute('''
            CREATE TABLE video(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                judul TEXT NOT NULL,
                thumbnail TEXT NOT NULL,
                durasi TEXT NOT NULL,
                deskripsi TEXT NOT NULL,
                youtube_id TEXT NOT NULL
            )
        ''')

        # =========================
        # 📚 DATA MODUL
        # =========================
        data_materi = [
            ('Konfigurasi Dasar MikroTik', 'mikrotik', 
             '<h2>Langkah Awal</h2><p>Gunakan Winbox untuk login ke router...</p>', 
             'Belajar cara setting IP Address dan DHCP Server di MikroTik.', 
             'fas fa-microchip'),

            ('Routing Statis MikroTik', 'mikrotik', 
             '<h2>Konsep Routing</h2><p>Routing statis dilakukan secara manual...</p>', 
             'Panduan menghubungkan dua jaringan berbeda dengan Static Route.', 
             'fas fa-route'),

            ('VLAN Dasar Cisco', 'cisco', 
             '<h2>Apa itu VLAN?</h2><p>Virtual LAN memungkinkan pemisahan jaringan...</p>', 
             'Cara membuat dan mengelola VLAN pada Switch Cisco.', 
             'fas fa-network-wired'),

            ('Inter-VLAN Routing', 'cisco', 
             '<h2>Router on a Stick</h2><p>Menghubungkan antar VLAN...</p>', 
             'Menghubungkan komunikasi antar VLAN.', 
             'fas fa-project-diagram'),

            ('Installasi Web Server Apache', 'linux', 
             '<h2>Step by Step</h2><p>apt install apache2...</p>', 
             'Membangun web server Ubuntu.', 
             'fas fa-server'),

            ('Manajemen User Linux', 'linux', 
             '<h2>Hak Akses</h2><p>chmod dan chown...</p>', 
             'Mengatur user dan permission.', 
             'fas fa-user-shield')
        ]

        connection.executemany('''
            INSERT INTO modul (judul, kategori, konten, deskripsi_singkat, icon)
            VALUES (?, ?, ?, ?, ?)
        ''', data_materi)

        # =========================
        # 👤 USER DEFAULT
        # =========================
        connection.execute('''
            INSERT INTO users (username, nama_lengkap, password, role, email)
            VALUES ('admin', 'Admin', 'admin', 'admin', 'admin@gmail.com')
        ''')

        connection.execute('''
            INSERT INTO users (username, nama_lengkap, password, role, email)
            VALUES ('siswa1', 'Abi Manyu Alfian Hidayanto', '12345', 'siswa', 'abimanyu@gmail.com')
        ''')

        # =========================
        # 🎥 VIDEO SAMPLE
        # =========================
        connection.execute('''
            INSERT INTO video (judul, thumbnail, durasi, deskripsi, youtube_id)
            VALUES (?, ?, ?, ?, ?)
        ''', ('Tutorial Linux', 'thumb.jpg', '10:00', 'Belajar Linux dasar', 'dQw4w9WgXcQ'))

    connection.commit()
    connection.close()
    print("✅ Database berhasil dibuat ulang dengan struktur terbaru!")

if __name__ == '__main__':
    init_db()
