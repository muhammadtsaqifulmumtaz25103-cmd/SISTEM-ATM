import unittest
from datetime import datetime
from decimal import Decimal

from transaksi import Transaksi, TransaksiMasuk, TransaksiTransfer


class TransaksiTests(unittest.TestCase):
    def test_base_transaction_exposes_values_and_formatted_info(self):
        transaksi = Transaksi("Setor Tunai", "1250.50")

        self.assertEqual(transaksi.get_jenis(), "Setor Tunai")
        self.assertEqual(transaksi.get_jumlah(), Decimal("1250.50"))
        self.assertIsInstance(transaksi.get_tanggal(), datetime)
        self.assertIn("Setor Tunai", transaksi.info())
        self.assertIn("Rp1,250.50", transaksi.info())

    def test_outgoing_transfer_info_contains_destination(self):
        transaksi = TransaksiTransfer(100, "Bima")

        self.assertEqual(transaksi.get_jenis(), "Transfer")
        self.assertEqual(transaksi.get_jumlah(), Decimal("100"))
        self.assertIn("Bima", transaksi.info())

    def test_incoming_transfer_info_contains_sender(self):
        transaksi = TransaksiMasuk(75, "Alya")

        self.assertEqual(transaksi.get_jenis(), "Terima Transfer")
        self.assertEqual(transaksi.get_jumlah(), Decimal("75"))
        self.assertIn("Alya", transaksi.info())


if __name__ == "__main__":
    unittest.main()