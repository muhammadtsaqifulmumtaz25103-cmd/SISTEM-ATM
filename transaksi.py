"""Model transaksi dan struk yang dapat ditampilkan di terminal."""

from datetime import datetime
from decimal import Decimal


class Transaksi:
    def __init__(self, jenis, jumlah):
        self.__jenis = jenis
        self.__jumlah = Decimal(str(jumlah))
        self.__tanggal = datetime.now()

    def get_jenis(self):
        return self.__jenis

    def get_jumlah(self):
        return self.__jumlah

    def get_tanggal(self):
        return self.__tanggal

    def info(self):
        tanggal = self.__tanggal.strftime("%d %b %Y, %H:%M")
        return f"{tanggal} | {self.__jenis:<16} | Rp{self.__jumlah:,.2f}"


class TransaksiTransfer(Transaksi):
    def __init__(self, jumlah, nama_tujuan):
        super().__init__("Transfer", jumlah)
        self.__nama_tujuan = nama_tujuan

    def info(self):
        return f"{super().info()} → {self.__nama_tujuan}"


class TransaksiMasuk(Transaksi):
    def __init__(self, jumlah, nama_pengirim):
        super().__init__("Terima Transfer", jumlah)
        self.__nama_pengirim = nama_pengirim

    def info(self):
        return f"{super().info()} ← {self.__nama_pengirim}"
