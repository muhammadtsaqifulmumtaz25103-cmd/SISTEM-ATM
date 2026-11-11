# ATM Demo Terminal

Aplikasi ATM sederhana berbasis Python dengan OOP, menu interaktif, warna ANSI, ringkasan saldo, struk, dan riwayat transaksi. Seluruh rekening dan transaksi hanya simulasi lokal; aplikasi ini tidak terhubung ke bank atau memindahkan uang sungguhan.

## Menjalankan

Gunakan Python 3.10 atau lebih baru. Tidak ada dependensi tambahan.

```powershell
python main.py
```

Masuk dengan ID demo `DEMO-001` atau `DEMO-002`. Saldo dan riwayat kembali ke nilai awal setiap kali program dimulai.

## Menu

1. Cek saldo
2. Tarik tunai simulasi
3. Setor tunai simulasi
4. Transfer simulasi ke rekening demo lain
5. Lihat laporan dan lima transaksi terakhir
6. Keluar

Nominal menerima angka desimal dengan titik atau koma, misalnya `25000` atau `25000,50`.

## Modul

- `main.py`: menu terminal dan alur program.
- `nasabah.py`: data nasabah demo.
- `rekening.py`: logika saldo dan transaksi.
- `transaksi.py`: transaksi, transfer, dan detail struk.
- `laporan.py`: ringkasan dan riwayat.
- `exception.py`: exception validasi saldo dan nominal.

Jangan masukkan NIK, nomor telepon, kata sandi, atau informasi keuangan sungguhan. Ini adalah proyek latihan, bukan layanan bank produksi.
