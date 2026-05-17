import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name="keuangan_umkm.db"):
        self.db_name = db_name
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Tabel Transaksi
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transaksi (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tanggal TEXT,
                jenis TEXT,
                kategori TEXT,
                deskripsi TEXT,
                nominal REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabel Kategori
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS kategori (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama TEXT UNIQUE,
                jenis TEXT
            )
        ''')
        
        # Kategori Default
        default_kategori = [
            ('Penjualan', 'PENDAPATAN'), ('Jasa', 'PENDAPATAN'),
            ('Beli Bahan Baku', 'PENGELUARAN'), ('Gaji Karyawan', 'PENGELUARAN'),
            ('Listrik & Air', 'PENGELUARAN'), ('Sewa Tempat', 'PENGELUARAN'),
            ('Lain-lain', 'PENGELUARAN')
        ]
        cursor.executemany("INSERT OR IGNORE INTO kategori (nama, jenis) VALUES (?, ?)", default_kategori)
        
        conn.commit()
        conn.close()
    
    def tambah_transaksi(self, tanggal, jenis, kategori, deskripsi, nominal):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO transaksi (tanggal, jenis, kategori, deskripsi, nominal)
            VALUES (?, ?, ?, ?, ?)
        ''', (tanggal, jenis, kategori, deskripsi, nominal))
        conn.commit()
        conn.close()
        return cursor.lastrowid
    
    def edit_transaksi(self, transaksi_id, tanggal, jenis, kategori, deskripsi, nominal):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE transaksi 
            SET tanggal=?, jenis=?, kategori=?, deskripsi=?, nominal=?
            WHERE id=?
        ''', (tanggal, jenis, kategori, deskripsi, nominal, transaksi_id))
        result = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return result
    
    def hapus_transaksi(self, transaksi_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM transaksi WHERE id=?', (transaksi_id,))
        result = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return result
    
    def get_transaksi(self, start_date=None, end_date=None):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        query = 'SELECT * FROM transaksi'
        params = []
        
        if start_date and end_date:
            query += ' WHERE tanggal BETWEEN ? AND ?'
            params = [start_date, end_date]
        elif start_date:
            query += ' WHERE tanggal >= ?'
            params = [start_date]
        elif end_date:
            query += ' WHERE tanggal <= ?'
            params = [end_date]
            
        query += ' ORDER BY tanggal DESC, id DESC'
        cursor.execute(query, params)
        data = cursor.fetchall()
        conn.close()
        return data
    
    def get_transaksi_by_id(self, transaksi_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM transaksi WHERE id=?', (transaksi_id,))
        data = cursor.fetchone()
        conn.close()
        return data
    
    def get_kategori(self, jenis=None):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        if jenis:
            cursor.execute('SELECT nama FROM kategori WHERE jenis=?', (jenis,))
        else:
            cursor.execute('SELECT nama FROM kategori')
            
        data = [row[0] for row in cursor.fetchall()]
        conn.close()
        return data
    
    def get_laporan(self, start_date, end_date):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COALESCE(SUM(nominal), 0) FROM transaksi 
            WHERE jenis = 'PENDAPATAN' AND tanggal BETWEEN ? AND ?
        ''', (start_date, end_date))
        pendapatan = cursor.fetchone()[0]
        
        cursor.execute('''
            SELECT COALESCE(SUM(nominal), 0) FROM transaksi 
            WHERE jenis = 'PENGELUARAN' AND tanggal BETWEEN ? AND ?
        ''', (start_date, end_date))
        pengeluaran = cursor.fetchone()[0]
        
        conn.close()
        return pendapatan, pengeluaran
    
    def get_export_data(self, start_date, end_date):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT tanggal, jenis, kategori, deskripsi, nominal 
            FROM transaksi WHERE tanggal BETWEEN ? AND ? 
            ORDER BY tanggal DESC
        ''', (start_date, end_date))
        data = cursor.fetchall()
        conn.close()
        return data