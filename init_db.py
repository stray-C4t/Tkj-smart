import sqlite3

def init_db():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    
    with connection:
        
        connection.execute('''
            CREATE TABLE IF NOT EXISTS modul (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                judul TEXT NOT NULL,
                kategori TEXT NOT NULL,
                konten TEXT NOT NULL,
                deskripsi_singkat TEXT,
                icon TEXT
            )
        ''')
        
        connection.execute('''
			CREATE TABLE IF NOT EXISTS user_video (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				user_id INTEGER,
				video_id INTEGER,
				updated_at TEXT
			);
		''')
        
        connection.execute('''
			CREATE TABLE IF NOT EXISTS user_progress (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				user_id INTEGER,
				modul_id INTEGER,
				progress INTEGER DEFAULT 0,
				updated_at TEXT
			)
		''')
		
        connection.execute('''
			CREATE TABLE IF NOT EXISTS user_quiz (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				user_id INTEGER,
				quiz_id INTEGER,
				score INTEGER,
				max_score INTEGER,
				updated_at TEXT
			);
		''')
        
        cursor.execute('''
			CREATE TABLE IF NOT EXISTS quiz_list (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				judul TEXT NOT NULL,
				icon TEXT NOT NULL
			)
		''')
		
        cursor.execute('''
			CREATE TABLE IF NOT EXISTS quiz_questions (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				quiz_id INTEGER,
				pertanyaan TEXT NOT NULL,
				opsi_a TEXT NOT NULL,
				opsi_b TEXT NOT NULL,
				opsi_c TEXT NOT NULL,
				opsi_d TEXT NOT NULL,
				jawaban_benar TEXT NOT NULL,
				FOREIGN KEY (quiz_id) REFERENCES quiz_list (id) ON DELETE CASCADE
			)
		''')
        
        connection.executemany('''
            INSERT INTO modul (judul, kategori, konten, deskripsi_singkat, icon) 
            VALUES (?, ?, ?, ?, ?)
        ''')    
        
        connection.execute('''
            CREATE TABLE IF NOT EXISTS video(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                judul TEXT NOT NULL,
                thumbnail TEXT NOT NULL,  -- URL gambar thumbnail
                durasi TEXT NOT NULL,     -- Contoh: "10:25"
                deskripsi TEXT NOT NULL,       -- Deskripsi singkat (v.desc)
                youtube_id TEXT NOT NULL  -- ID untuk halaman nonton nanti
            )
		''')

        connection.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                nama_lengkap TEXT,
                password TEXT NOT NULL,
                role TEXT DEFAULT 'siswa',
                kelas TEXT,
                streak INTEGER DEFAULT 0,
                last_login DATE
            )
            ''')

        connection.execute('''
            CREATE TABLE IF NOT EXISTS activity_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                activity TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            ''')
        
        connection.execute('''
            INSERT INTO video (judul, thumbnail, durasi, deskripsi, youtube_id) 
            VALUES (?, ?, ?, ?, ?)
        ''', ('Judul Video', 'thumb.jpg', '10:00', 'Deskripsi video', 'xyz123'))
        
        try:
            connection.execute("ALTER TABLE users ADD COLUMN kelas TEXT")
        except:
            pass

        try:
            connection.execute("ALTER TABLE user_progress ADD COLUMN updated_at TEXT")
        except:
            pass

        try:
            connection.execute("ALTER TABLE user_quiz ADD COLUMN updated_at TEXT")
        except:
            pass

        try:
            connection.execute("ALTER TABLE user_video ADD COLUMN updated_at TEXT")
        except:
            pass

        try:
            cursor.execute("ALTER TABLE users ADD COLUMN streak INTEGER DEFAULT 0")
            cursor.execute("ALTER TABLE users ADD COLUMN last_login DATE")
            print("Kolom streak & last_login berhasil ditambahkan!")
        except sqlite3.OperationalError:
            print("Kolom sudah ada, tidak ada perubahan.")
        
    connection.commit()		
    connection.close()

if __name__ == '__main__':
    init_db()