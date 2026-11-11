"""Aplikasi ATM terminal untuk latihan; seluruh saldo dan transaksi hanya simulasi."""

from decimal import Decimal, InvalidOperation

from exception import JumlahTidakValidError, SaldoTidakCukupError
from laporan import BOLD, BLUE, CYAN, GREEN, RED, RESET, YELLOW
from nasabah import Nasabah
from rekening import Rekening


def format_rupiah(jumlah):
    return f"Rp{jumlah:,.2f}"


def input_jumlah(prompt):
    teks = input(prompt).strip().replace(",", ".")
    try:
        jumlah = Decimal(teks)
    except InvalidOperation as error:
        raise ValueError("Input harus berupa angka.") from error
    if not jumlah.is_finite():
        raise ValueError("Input harus berupa angka yang valid.")
    return jumlah


def cetak_struk(transaksi, saldo):
    print(f"\n{CYAN}┌──────────── STRUK TRANSAKSI ────────────┐{RESET}")
    print(f"{CYAN}│{RESET} {transaksi.info()}")
    print(f"{CYAN}│{RESET} Saldo sekarang: {format_rupiah(saldo)}")
    print(f"{CYAN}└────────────────────────────────────────┘{RESET}")


def main():
    # Semua identitas, rekening, dan saldo di bawah ini adalah data fiktif demo.
    nasabah_utama = Nasabah("Alya Demo", "DEMO-001", "08xx-xxx-0001")
    nasabah_tujuan = Nasabah("Bima Demo", "DEMO-002", "08xx-xxx-0002")
    rekening_utama = Rekening(nasabah_utama, saldo_awal=274840)
    rekening_tujuan = Rekening(nasabah_tujuan, saldo_awal=1000000)
    daftar_rekening = {
        nasabah_utama.get_nik(): rekening_utama,
        nasabah_tujuan.get_nik(): rekening_tujuan,
    }

    print(f"{YELLOW}DEMO SAJA — jangan gunakan data atau uang sungguhan.{RESET}")
    print(f"{BOLD}Login demo dengan ID DEMO-001 atau DEMO-002.{RESET}")
    id_nasabah = input("Masukkan ID nasabah: ").strip()
    rekening_aktif = daftar_rekening.get(id_nasabah)
    if rekening_aktif is None:
        print(f"{RED}❌ ID demo tidak ditemukan.{RESET}")
        return

    nama = rekening_aktif.get_nasabah().get_nama()
    while True:
        print(f"\n{BLUE}{'═' * 52}{RESET}")
        print(f"{BOLD}  ATM DEMO  ·  Halo, {nama}! 👋{RESET}")
        print(f"{BLUE}{'═' * 52}{RESET}")
        print("  [1] 🔵 Cek saldo        [4] 🔄 Transfer")
        print("  [2] 🔴 Tarik tunai      [5] 📊 Laporan & riwayat")
        print("  [3] 🟢 Setor tunai      [6] 🚪 Keluar")
        print(f"{BLUE}{'─' * 52}{RESET}")

        try:
            pilihan = input(f"{YELLOW}Pilih menu (1-6): {RESET}").strip()
            if pilihan == "1":
                rekening_aktif.cek_saldo()
            elif pilihan == "2":
                transaksi = rekening_aktif.tarik_tunai(
                    input_jumlah("Nominal tarik tunai (Rp): ")
                )
                print(f"{GREEN}✔ Tarik tunai berhasil.{RESET}")
                cetak_struk(transaksi, rekening_aktif.get_saldo())
            elif pilihan == "3":
                transaksi = rekening_aktif.setor_tunai(
                    input_jumlah("Nominal setor tunai (Rp): ")
                )
                print(f"{GREEN}✔ Setor tunai berhasil.{RESET}")
                cetak_struk(transaksi, rekening_aktif.get_saldo())
            elif pilihan == "4":
                print(f"\n{CYAN}Pilih rekening tujuan demo:{RESET}")
                for nomor, (id_tujuan, rekening) in enumerate(daftar_rekening.items(), 1):
                    if rekening is not rekening_aktif:
                        print(f"  {nomor}. {rekening.get_nasabah().get_nama()} ({id_tujuan})")
                id_tujuan = input("ID tujuan (mis. DEMO-002): ").strip()
                rekening_penerima = daftar_rekening.get(id_tujuan)
                if rekening_penerima is None:
                    print(f"{RED}❌ Rekening tujuan demo tidak ditemukan.{RESET}")
                    continue
                transaksi = rekening_aktif.transfer(
                    rekening_penerima,
                    input_jumlah("Nominal transfer simulasi (Rp): "),
                )
                print(f"{GREEN}✔ Transfer simulasi berhasil.{RESET}")
                cetak_struk(transaksi, rekening_aktif.get_saldo())
            elif pilihan == "5":
                rekening_aktif.lihat_laporan()
            elif pilihan == "6":
                print(f"\n{GREEN}Terima kasih, {nama}! Sampai jumpa. 👋{RESET}")
                break
            else:
                print(f"{RED}❌ Pilihan tidak valid. Masukkan angka 1–6.{RESET}")
        except ValueError as error:
            print(f"{RED}❌ ERROR: {error}{RESET}")
        except JumlahTidakValidError as error:
            print(f"{RED}❌ ERROR: {error}{RESET}")
        except SaldoTidakCukupError as error:
            print(f"{RED}❌ ERROR: {error}{RESET}")
        except (EOFError, KeyboardInterrupt):
            print(f"\n{YELLOW}Sesi demo dihentikan.{RESET}")
            break


if __name__ == "__main__":
    main()
