
from datetime import datetime


# =====================================
# CLASS NASABAH
# =====================================

class Nasabah:
    def __init__(self, nama, NIK, no_hp, saldo):
        self.nama = nama
        self.NIK = NIK
        self.no_hp = no_hp
        self.saldo = float(saldo)
        self.riwayat_transaksi = []

    def tambah_transaksi(self, transaksi):
        self.riwayat_transaksi.append(transaksi)


# =====================================
# CLASS TRANSAKSI (PARENT CLASS)
# =====================================

class Transaksi:
    def __init__(self, no_transaksi, jenis, jumlah):
        self.no_transaksi = no_transaksi
        self.jenis = jenis
        self.jumlah = float(jumlah)
        self.tanggal = datetime.now()

    def proses_transaksi(self, nasabah):
        raise NotImplementedError(
            "Method harus diimplementasikan oleh child class"
        )

    def ringkasan(self):
        return (
            f"No Transaksi : {self.no_transaksi}\n"
            f"Jenis        : {self.jenis}\n"
            f"Jumlah       : Rp{self.jumlah:,.2f}\n"
            f"Tanggal      : {self.tanggal}"
        )


# =====================================
# CLASS SETORAN (CHILD CLASS)
# =====================================

class Setoran(Transaksi):
    def __init__(self, no_transaksi, jumlah):
        super().__init__(no_transaksi, "Setoran", jumlah)

    def proses_transaksi(self, nasabah):
        if self.jumlah <= 0:
            print("Jumlah setoran harus lebih dari 0!")
            return False

        nasabah.saldo += self.jumlah
        nasabah.tambah_transaksi(self)

        print("\nSetoran berhasil!")
        print(f"Saldo sekarang: Rp{nasabah.saldo:,.2f}")
        return True

    def ringkasan(self):
        return "=== TRANSAKSI SETORAN ===\n" + super().ringkasan()


# =====================================
# CLASS TARIK (CHILD CLASS)
# =====================================

class Tarik(Transaksi):
    def __init__(self, no_transaksi, jumlah):
        super().__init__(no_transaksi, "Tarik Tunai", jumlah)

    def proses_transaksi(self, nasabah):
        if self.jumlah <= 0:
            print("Jumlah penarikan harus lebih dari 0!")
            return False

        if self.jumlah > nasabah.saldo:
            print("Saldo tidak mencukupi!")
            return False

        nasabah.saldo -= self.jumlah
        nasabah.tambah_transaksi(self)

        print("\nPenarikan berhasil!")
        print(f"Saldo sekarang: Rp{nasabah.saldo:,.2f}")
        return True

    def ringkasan(self):
        return "=== TRANSAKSI TARIK TUNAI ===\n" + super().ringkasan()


# =====================================
# CLASS TRANSFER (CHILD CLASS)
# =====================================

class Transfer(Transaksi):
    def __init__(self, no_transaksi, jumlah, rekening_tujuan):
        super().__init__(no_transaksi, "Transfer", jumlah)
        self.rekening_tujuan = rekening_tujuan

    def proses_transaksi(self, nasabah, daftar_nasabah):
        if self.jumlah <= 0:
            print("Jumlah transfer harus lebih dari 0!")
            return False

        if self.jumlah > nasabah.saldo:
            print("Saldo tidak mencukupi!")
            return False

        # Mencari rekening tujuan berdasarkan NIK
        tujuan = next(
            (n for n in daftar_nasabah
             if n.NIK == self.rekening_tujuan),
            None
        )

        if tujuan is None:
            print("Nasabah tujuan tidak ditemukan!")
            return False

        if tujuan is nasabah:
            print("Tidak dapat transfer ke rekening sendiri!")
            return False

        # Proses transfer
        nasabah.saldo -= self.jumlah
        tujuan.saldo += self.jumlah

        nasabah.tambah_transaksi(self)

        print("\nTransfer berhasil!")
        print(f"Tujuan transfer : {tujuan.nama}")
        print(f"Jumlah          : Rp{self.jumlah:,.2f}")
        print(f"Saldo sekarang  : Rp{nasabah.saldo:,.2f}")
        return True

    def ringkasan(self):
        return (
            "=== TRANSAKSI TRANSFER ===\n"
            + super().ringkasan()
            + f"\nRekening Tujuan: {self.rekening_tujuan}"
        )


# =====================================
# PROGRAM UTAMA SISTEM ATM
# =====================================

daftar_nasabah = [
    Nasabah("Ahmad", "12345", "08123456789", 1000000),
    Nasabah("Budi", "67890", "08234567890", 500000)
]

nomor_transaksi = 1


def cari_nasabah(nik):
    for nasabah in daftar_nasabah:
        if nasabah.NIK == nik:
            return nasabah
    return None


def input_jumlah():
    try:
        jumlah = float(input("Masukkan jumlah uang: Rp"))
        return jumlah
    except ValueError:
        print("Input harus berupa angka!")
        return None


def jalankan_atm():
    global nomor_transaksi

    print("=" * 40)
    print("       SISTEM ATM SEDERHANA")
    print("=" * 40)

    nik = input("Masukkan NIK: ")
    nasabah = cari_nasabah(nik)

    if nasabah is None:
        print("Nasabah tidak ditemukan!")
        return

    print(f"\nSelamat datang, {nasabah.nama}!")

    while True:
        print("\n========== MENU ATM ==========")
        print("1. Cek Saldo")
        print("2. Setoran")
        print("3. Tarik Tunai")
        print("4. Transfer")
        print("5. Riwayat Transaksi")
        print("6. Keluar")
        print("==============================")

        pilihan = input("Pilih menu (1-6): ")

        if pilihan == "1":
            print(f"\nSaldo Anda: Rp{nasabah.saldo:,.2f}")

        elif pilihan == "2":
            jumlah = input_jumlah()
            if jumlah is None:
                continue

            transaksi = Setoran(
                str(nomor_transaksi), jumlah
            )

            if transaksi.proses_transaksi(nasabah):
                nomor_transaksi += 1
                print(transaksi.ringkasan())

        elif pilihan == "3":
            jumlah = input_jumlah()
            if jumlah is None:
                continue

            transaksi = Tarik(
                str(nomor_transaksi), jumlah
            )

            if transaksi.proses_transaksi(nasabah):
                nomor_transaksi += 1
                print(transaksi.ringkasan())

        elif pilihan == "4":
            tujuan = input("Masukkan NIK tujuan: ")
            jumlah = input_jumlah()

            if jumlah is None:
                continue

            transaksi = Transfer(
                str(nomor_transaksi), jumlah, tujuan
            )

            if transaksi.proses_transaksi(
                nasabah, daftar_nasabah
            ):
                nomor_transaksi += 1
                print(transaksi.ringkasan())

        elif pilihan == "5":
            print("\n====== RIWAYAT TRANSAKSI ======")

            if not nasabah.riwayat_transaksi:
                print("Belum ada transaksi.")
            else:
                for transaksi in nasabah.riwayat_transaksi:
                    print(transaksi.ringkasan())
                    print("-" * 35)

        elif pilihan == "6":
            print(f"\nTerima kasih, {nasabah.nama}!")
            print("Silakan ambil kartu ATM Anda.")
            break

        else:
            print("Pilihan tidak valid!")


# Menjalankan program
if __name__ == "__main__":
    jalankan_atm()
