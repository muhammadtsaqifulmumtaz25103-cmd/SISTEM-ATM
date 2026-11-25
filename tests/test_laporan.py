import unittest
from contextlib import redirect_stdout
from decimal import Decimal
from io import StringIO

from laporan import Laporan
from transaksi import Transaksi


class LaporanTests(unittest.TestCase):
    def test_history_is_read_only_tuple_and_rekap_aggregates_by_type(self):
        laporan = Laporan()
        laporan.tambah_transaksi(Transaksi("Setor Tunai", "10.25"))
        laporan.tambah_transaksi(Transaksi("Setor Tunai", "4.75"))
        laporan.tambah_transaksi(Transaksi("Tarik Tunai", 3))

        self.assertEqual(
            laporan.rekap_transaksi(),
            {"Setor Tunai": Decimal("15.00"), "Tarik Tunai": Decimal("3")},
        )
        self.assertIsInstance(laporan.get_riwayat(), tuple)
        self.assertEqual(len(laporan.get_riwayat()), 3)

    def test_report_shows_transaction_summary(self):
        laporan = Laporan()
        laporan.tambah_transaksi(Transaksi("Setor Tunai", 25))
        output = StringIO()

        with redirect_stdout(output):
            laporan.cetak_laporan("Alya", Decimal("1025"))

        teks = output.getvalue()
        self.assertIn("Alya", teks)
        self.assertIn("Setor Tunai", teks)
        self.assertIn("Rp25.00", teks)

    def test_empty_report_shows_empty_state(self):
        laporan = Laporan()
        output = StringIO()
        with redirect_stdout(output):
            laporan.cetak_laporan("Alya", Decimal("0"))

        self.assertIn("Belum ada transaksi.", output.getvalue())

    def test_report_limits_recent_transactions_to_five(self):
        laporan = Laporan()
        for jumlah in range(1, 7):
            laporan.tambah_transaksi(Transaksi("Setor Tunai", jumlah))
        output = StringIO()

        with redirect_stdout(output):
            laporan.cetak_laporan("Alya", Decimal("21"))

        teks = output.getvalue()
        self.assertNotIn("Rp1.00", teks)
        self.assertIn("Rp2.00", teks)
        self.assertIn("Rp6.00", teks)
        self.assertLess(teks.index("Rp6.00"), teks.index("Rp5.00"))


if __name__ == "__main__":
    unittest.main()