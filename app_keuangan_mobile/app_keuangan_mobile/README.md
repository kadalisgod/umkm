# 📱 Aplikasi Keuangan UMKM - Versi Mobile (Web)

## Struktur File
```
app_keuangan_mobile/
├── app.py          ← Server Flask (BARU)
├── database.py     ← Sama seperti sebelumnya
├── models.py       ← Sama seperti sebelumnya
├── requirements.txt
└── templates/
    └── index.html  ← UI mobile-friendly (BARU)
```

---

## 🚀 Cara Menjalankan

### 1. Install dependensi
```bash
pip install flask pandas openpyxl
```

### 2. Jalankan server
```bash
python app.py
```

Server akan berjalan di:
- **PC sendiri:** http://localhost:5000
- **Dari HP (1 WiFi):** http://[IP-PC]:5000

### 3. Cari IP PC kamu
```bash
# Windows
ipconfig
# Cari "IPv4 Address" misalnya 192.168.1.10

# Lalu buka di HP:
# http://192.168.1.10:5000
```

---

## 📱 Akses dari Smartphone

Syarat: **HP dan PC harus terhubung WiFi yang sama**

1. Jalankan `python app.py` di PC
2. Buka **browser HP** (Chrome/Safari)
3. Ketik `http://[IP-PC]:5000`
4. Bisa juga **tambahkan ke Home Screen** untuk tampilan seperti aplikasi

---

## ✅ Fitur
- Dashboard ringkasan keuangan
- Tambah / Edit / Hapus transaksi
- Filter berdasarkan tanggal
- Laporan per kategori
- Export Excel
- UI mobile-friendly & dark mode
