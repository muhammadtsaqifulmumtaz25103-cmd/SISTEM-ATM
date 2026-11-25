import unittest
from decimal import Decimal
from unittest.mock import patch

from main import format_rupiah, input_jumlah


class MainInputTests(unittest.TestCase):
    def test_input_jumlah_accepts_dot_and_comma_decimal_separator(self):
        for text, expected in ((" 25000.50 ", "25000.50"), ("25000,50", "25000.50")):
            with self.subTest(text=text), patch("builtins.input", return_value=text):
                self.assertEqual(input_jumlah("Nominal: "), Decimal(expected))

    def test_input_jumlah_rejects_invalid_and_non_finite_values(self):
        for text in ("abc", "", "NaN", "Infinity"):
            with self.subTest(text=text), patch("builtins.input", return_value=text):
                with self.assertRaises(ValueError):
                    input_jumlah("Nominal: ")

    def test_format_rupiah_uses_two_decimal_places_and_grouping(self):
        self.assertEqual(format_rupiah(Decimal("1234567.5")), "Rp1,234,567.50")


if __name__ == "__main__":
    unittest.main()