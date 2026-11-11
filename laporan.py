"""Tampilan ringkasan rekening dan laporan transaksi."""

RESET = "\033[0m"
BOLD = "\033[1m"
BLUE = "\033[94m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"


class Laporan:
    def __init__(self):
        self.__riwayat = []

    def tambah_transaksi(self, transaksi):
        self.__riwayat.append(transaksi)

    def get_riwayat(self):
        return tuple(self.__riwayat)

    def rekap_transaksi(self):
        rekap = {}
        for transaksi in self.__riwayat:
            jenis = transaksi.get_jenis()
            rekap[jenis] = rekap.get(jenis, 0) + transaksi.get_jumlah()
        return rekap

    def cetak_laporan(self, nama_nasabah, saldo):
        print(f"\n{BOLD}Selamat datang, {nama_nasabah}! 👋{RESET}")
        print(f"{BLUE}┌──────────────────────────────────────────────┐{RESET}")
        print(f"{BLUE}│{RESET} {BOLD}TOTAL SALDO{RESET}                                  {BLUE}│{RESET}")
        print(f"{BLUE}│{RESET} {GREEN}{BOLD}Rp{saldo:,.2f}{RESET}                              {BLUE}│{RESET}")
        print(f"{BLUE}│{RESET} {CYAN}↗ {len(self.__riwayat)} Total Transaksi{RESET}                      {BLUE}│{RESET}")
        print(f"{BLUE}└──────────────────────────────────────────────┘{RESET}")

        print(f"\n{BOLD}Riwayat Transaksi Terakhir{RESET}")
        if not self.__riwayat:
            print(f"  {YELLOW}Belum ada transaksi.{RESET}")
        else:
            for transaksi in reversed(self.__riwayat[-5:]):
                print(f"  🔹 {transaksi.info()}")

        rekap = self.rekap_transaksi()
        if rekap:
            print(f"\n{BOLD}Rekap Transaksi:{RESET}")
            for jenis, total in rekap.items():
                print(f"  • {jenis:<18} {YELLOW}Rp{total:,.2f}{RESET}")
