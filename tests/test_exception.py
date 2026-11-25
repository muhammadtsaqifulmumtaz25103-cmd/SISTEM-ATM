import unittest

from exception import JumlahTidakValidError, SaldoTidakCukupError


class ExceptionTests(unittest.TestCase):
    def test_jumlah_tidak_valid_error_explains_positive_amount_requirement(self):
        error = JumlahTidakValidError(0)

        self.assertIn("Jumlah tidak valid: 0", str(error))
        self.assertIn("Harus lebih dari 0", str(error))

    def test_saldo_tidak_cukup_error_reports_balance_and_required_amount(self):
        error = SaldoTidakCukupError(100, 150)

        self.assertIn("Saldo: Rp100.00", str(error))
        self.assertIn("Dibutuhkan: Rp150.00", str(error))


if __name__ == "__main__":
    unittest.main()