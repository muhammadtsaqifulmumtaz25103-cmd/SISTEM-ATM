"""Logika rekening demo: cek saldo, setor, tarik, dan transfer."""

from decimal import Decimal

from exception import JumlahTidakValidError, SaldoTidakCukupError
from laporan import BOLD, GREEN, RESET, Laporan
from transaksi import Transaksi, TransaksiMasuk, TransaksiTransfer


class Rekening:
    def __init__(self, nasabah, saldo_awal=0):
        saldo = Decimal(str(saldo_awal))
        if not saldo.is_finite() or saldo < 0:
            raise ValueError("Saldo awal harus berupa angka yang valid dan tidak negatif.")
        self.__saldo = saldo
        self.__nasabah = nasabah
        self.__laporan = Laporan()

    def get_saldo(self):
        return self.__saldo

    def get_nasabah(self):
        return self.__nasabah

    def cek_saldo(self):
        print(f"\n{BOLD}--- DETAIL REKENING ---{RESET}")
        print(f"Nama  : {self.__nasabah.get_nama()}")
        print(f"ID    : {self.__nasabah.get_nik()}")
        print(f"Saldo : {GREEN}Rp{self.__saldo:,.2f}{RESET}")
        return self.__saldo

    @staticmethod
    def _validasi_jumlah(jumlah):
        try:
            jumlah = Decimal(str(jumlah))
        except (ValueError, TypeError, ArithmeticError) as error:
            raise JumlahTidakValidError(jumlah) from error
        if not jumlah.is_finite() or jumlah <= 0:
            raise JumlahTidakValidError(jumlah)
        return jumlah

    def tarik_tunai(self, jumlah):
        jumlah = self._validasi_jumlah(jumlah)
        if jumlah > self.__saldo:
            raise SaldoTidakCukupError(self.__saldo, jumlah)
        self.__saldo -= jumlah
        transaksi = Transaksi("Tarik Tunai", jumlah)
        self.__laporan.tambah_transaksi(transaksi)
        return transaksi

    def setor_tunai(self, jumlah):
        jumlah = self._validasi_jumlah(jumlah)
        self.__saldo += jumlah
        transaksi = Transaksi("Setor Tunai", jumlah)
        self.__laporan.tambah_transaksi(transaksi)
        return transaksi

    def transfer(self, rekening_tujuan, jumlah):
        jumlah = self._validasi_jumlah(jumlah)
        if rekening_tujuan is self:
            raise ValueError("Tidak dapat transfer ke rekening sendiri.")
        if jumlah > self.__saldo:
            raise SaldoTidakCukupError(self.__saldo, jumlah)

        transaksi = TransaksiTransfer(jumlah, rekening_tujuan.get_nasabah().get_nama())
        self.__saldo -= jumlah
        rekening_tujuan.__terima_transfer(jumlah, self.__nasabah.get_nama())
        self.__laporan.tambah_transaksi(transaksi)
        return transaksi

    def __terima_transfer(self, jumlah, nama_pengirim):
        self.__saldo += jumlah
        self.__laporan.tambah_transaksi(TransaksiMasuk(jumlah, nama_pengirim))

    def lihat_laporan(self):
        self.__laporan.cetak_laporan(self.__nasabah.get_nama(), self.__saldo)

    def get_riwayat(self):
        return self.__laporan.get_riwayat()
