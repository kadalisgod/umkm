from database import Database

class Transaksi:
    def __init__(self):
        self.db = Database()
    
    def simpan(self, tanggal, jenis, kategori, deskripsi, nominal):
        return self.db.tambah_transaksi(tanggal, jenis, kategori, deskripsi, nominal)
    
    def edit(self, transaksi_id, tanggal, jenis, kategori, deskripsi, nominal):
        return self.db.edit_transaksi(transaksi_id, tanggal, jenis, kategori, deskripsi, nominal)
    
    def hapus(self, transaksi_id):
        return self.db.hapus_transaksi(transaksi_id)
    
    def get_by_id(self, transaksi_id):
        return self.db.get_transaksi_by_id(transaksi_id)
    
    def get_all(self, start_date=None, end_date=None):
        return self.db.get_transaksi(start_date, end_date)