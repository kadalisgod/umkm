from flask import Flask, render_template, request, jsonify, send_file
from database import Database
from models import Transaksi
from datetime import datetime, timedelta
import os
import io

app = Flask(__name__)
db = Database()
model = Transaksi()

# ─── HALAMAN UTAMA ───────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')

# ─── API: GET TRANSAKSI ──────────────────────────────────────────
@app.route('/api/transaksi', methods=['GET'])
def get_transaksi():
    start = request.args.get('start', (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
    end   = request.args.get('end',   datetime.now().strftime('%Y-%m-%d'))
    data  = model.get_all(start, end)
    return jsonify([{
        'id': r[0], 'tanggal': r[1], 'jenis': r[2],
        'kategori': r[3], 'deskripsi': r[4], 'nominal': r[5]
    } for r in data])

# ─── API: TAMBAH TRANSAKSI ───────────────────────────────────────
@app.route('/api/transaksi', methods=['POST'])
def tambah_transaksi():
    d = request.json
    try:
        nominal = float(d['nominal'])
        if nominal <= 0:
            return jsonify({'success': False, 'message': 'Nominal harus lebih dari 0'}), 400
        model.simpan(d['tanggal'], d['jenis'], d['kategori'], d['deskripsi'], nominal)
        return jsonify({'success': True, 'message': 'Transaksi berhasil disimpan!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ─── API: EDIT TRANSAKSI ─────────────────────────────────────────
@app.route('/api/transaksi/<int:tid>', methods=['PUT'])
def edit_transaksi(tid):
    d = request.json
    try:
        nominal = float(d['nominal'])
        ok = model.edit(tid, d['tanggal'], d['jenis'], d['kategori'], d['deskripsi'], nominal)
        if ok:
            return jsonify({'success': True, 'message': 'Transaksi berhasil diupdate!'})
        return jsonify({'success': False, 'message': 'Data tidak ditemukan'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ─── API: HAPUS TRANSAKSI ────────────────────────────────────────
@app.route('/api/transaksi/<int:tid>', methods=['DELETE'])
def hapus_transaksi(tid):
    ok = model.hapus(tid)
    if ok:
        return jsonify({'success': True, 'message': 'Transaksi berhasil dihapus!'})
    return jsonify({'success': False, 'message': 'Data tidak ditemukan'}), 404

# ─── API: LAPORAN ────────────────────────────────────────────────
@app.route('/api/laporan', methods=['GET'])
def get_laporan():
    start = request.args.get('start', (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
    end   = request.args.get('end',   datetime.now().strftime('%Y-%m-%d'))
    pendapatan, pengeluaran = db.get_laporan(start, end)
    return jsonify({
        'pendapatan':  pendapatan,
        'pengeluaran': pengeluaran,
        'keuntungan':  pendapatan - pengeluaran
    })

# ─── API: KATEGORI ───────────────────────────────────────────────
@app.route('/api/kategori', methods=['GET'])
def get_kategori():
    jenis = request.args.get('jenis')
    return jsonify(db.get_kategori(jenis))

# ─── API: EXPORT EXCEL ──────────────────────────────────────────
@app.route('/api/export', methods=['GET'])
def export_excel():
    try:
        import pandas as pd
        start = request.args.get('start', (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
        end   = request.args.get('end',   datetime.now().strftime('%Y-%m-%d'))
        data  = db.get_export_data(start, end)
        if not data:
            return jsonify({'error': 'Tidak ada data'}), 400

        df = pd.DataFrame(data, columns=['Tanggal','Jenis','Kategori','Deskripsi','Nominal'])

        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Data Transaksi', index=False)
            pendapatan, pengeluaran = db.get_laporan(start, end)
            summary = pd.DataFrame({
                'RINGKASAN': ['Periode','Total Transaksi','Total Pendapatan','Total Pengeluaran','KEUNTUNGAN'],
                'NILAI': [f"{start} s.d. {end}", len(data),
                          f"Rp {int(pendapatan):,}", f"Rp {int(pengeluaran):,}",
                          f"Rp {int(pendapatan-pengeluaran):,}"]
            })
            summary.to_excel(writer, sheet_name='Ringkasan', index=False)
        buf.seek(0)

        fname = f"Laporan_{start}_sd_{end}.xlsx"
        return send_file(buf, as_attachment=True, download_name=fname,
                         mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    except ImportError:
        return jsonify({'error': 'Install pandas & openpyxl terlebih dahulu'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # host='0.0.0.0' agar bisa diakses dari HP via WiFi
    app.run(host='0.0.0.0', port=5000, debug=True)
