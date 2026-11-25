import unittest
from contextlib import redirect_stdout
from decimal import Decimal
from io import StringIO

from exception import JumlahTidakValidError, SaldoTidakCukupError
from nasabah import Nasabah
from rekening import Rekening


class RekeningTests(unittest.TestCase):
    def setUp(self):
        self.pengirim = Rekening(Nasabah("Alya", "DEMO-001", "08xx"), 1000)
        self.penerima = Rekening(Nasabah("Bima", "DEMO-002", "08yy"), 250)

    def test_initial_balance_must_be_finite_and_non_negative(self):
        nasabah = Nasabah("Alya", "DEMO-001", "08xx")
        for saldo in (-1, "NaN", "Infinity"):
            with self.subTest(saldo=saldo):
                with self.assertRaises(ValueError):
                    Rekening(nasabah, saldo)

    def test_deposit_increases_balance_and_records_transaction(self):
        transaksi = self.pengirim.setor_tunai("125.50")

        self.assertEqual(self.pengirim.get_saldo(), Decimal("1125.50"))
        self.assertEqual(transaksi.get_jenis(), "Setor Tunai")
        self.assertEqual(transaksi.get_jumlah(), Decimal("125.50"))
        self.assertEqual(self.pengirim.get_riwayat(), (transaksi,))

    def test_withdrawal_decreases_balance_and_records_transaction(self):
        transaksi = self.pengirim.tarik_tunai(300)

        self.assertEqual(self.pengirim.get_saldo(), Decimal("700"))
        self.assertEqual(transaksi.get_jenis(), "Tarik Tunai")
        self.assertEqual(transaksi.get_jumlah(), Decimal("300"))
        self.assertEqual(self.pengirim.get_riwayat(), (transaksi,))

    def test_withdrawal_of_entire_balance_is_allowed(self):
        self.pengirim.tarik_tunai(1000)

        self.assertEqual(self.pengirim.get_saldo(), Decimal("0"))

    def test_insufficient_withdrawal_does_not_change_account(self):
        with self.assertRaises(SaldoTidakCukupError):
            self.pengirim.tarik_tunai(1000.01)

        self.assertEqual(self.pengirim.get_saldo(), Decimal("1000"))
        self.assertEqual(self.pengirim.get_riwayat(), ())

    def test_non_positive_and_malformed_amounts_are_rejected(self):
        for jumlah in (0, -1, "NaN", "abc", None):
            with self.subTest(jumlah=jumlah):
                with self.assertRaises(JumlahTidakValidError):
                    self.pengirim.setor_tunai(jumlah)

        self.assertEqual(self.pengirim.get_saldo(), Decimal("1000"))
        self.assertEqual(self.pengirim.get_riwayat(), ())

    def test_transfer_updates_both_balances_and_both_histories(self):
        transaksi = self.pengirim.transfer(self.penerima, "125.50")

        self.assertEqual(self.pengirim.get_saldo(), Decimal("874.50"))
        self.assertEqual(self.penerima.get_saldo(), Decimal("375.50"))
        self.assertEqual(self.pengirim.get_riwayat(), (transaksi,))
        riwayat_penerima = self.penerima.get_riwayat()
        self.assertEqual(len(riwayat_penerima), 1)
        self.assertEqual(riwayat_penerima[0].get_jenis(), "Terima Transfer")
        self.assertEqual(riwayat_penerima[0].get_jumlah(), Decimal("125.50"))

    def test_transfer_to_self_is_rejected_without_changes(self):
        with self.assertRaisesRegex(ValueError, "rekening sendiri"):
            self.pengirim.transfer(self.pengirim, 100)

        self.assertEqual(self.pengirim.get_saldo(), Decimal("1000"))
        self.assertEqual(self.pengirim.get_riwayat(), ())

    def test_insufficient_transfer_does_not_change_either_account(self):
        with self.assertRaises(SaldoTidakCukupError):
            self.pengirim.transfer(self.penerima, 1000.01)

        self.assertEqual(self.pengirim.get_saldo(), Decimal("1000"))
        self.assertEqual(self.penerima.get_saldo(), Decimal("250"))
        self.assertEqual(self.pengirim.get_riwayat(), ())
        self.assertEqual(self.penerima.get_riwayat(), ())

    def test_cek_saldo_returns_current_balance(self):
        output = StringIO()
        with redirect_stdout(output):
            saldo = self.pengirim.cek_saldo()

        self.assertEqual(saldo, Decimal("1000"))
        self.assertIn("Alya", output.getvalue())
        self.assertIn("DEMO-001", output.getvalue())


if __name__ == "__main__":
    unittest.main()