"""Data nasabah demo dengan atribut privat dan setter tervalidasi."""


class Nasabah:
    def __init__(self, nama, nik, no_hp):
        self.set_nama(nama)
        self.set_nik(nik)
        self.set_no_hp(no_hp)

    @staticmethod
    def _validasi_teks(nilai, label):
        if not isinstance(nilai, str) or not nilai.strip():
            raise ValueError(f"{label} tidak boleh kosong.")
        return nilai.strip()

    def get_nama(self):
        return self.__nama

    def set_nama(self, nama):
        self.__nama = self._validasi_teks(nama, "Nama")

    def get_nik(self):
        return self.__nik

    def set_nik(self, nik):
        self.__nik = self._validasi_teks(nik, "ID nasabah")

    def get_no_hp(self):
        return self.__no_hp

    def set_no_hp(self, no_hp):
        self.__no_hp = self._validasi_teks(no_hp, "Nomor telepon")

    def __str__(self):
        return f"{self.__nama} | ID: {self.__nik}"
