import unittest

from nasabah import Nasabah


class NasabahTests(unittest.TestCase):
    def test_text_fields_are_trimmed(self):
        nasabah = Nasabah("  Alya  ", "  DEMO-001  ", "  08xx  ")

        self.assertEqual(nasabah.get_nama(), "Alya")
        self.assertEqual(nasabah.get_nik(), "DEMO-001")
        self.assertEqual(nasabah.get_no_hp(), "08xx")

    def test_empty_or_non_string_fields_are_rejected(self):
        for value in ("", "   ", None, 123):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    Nasabah(value, "DEMO-001", "08xx")

    def test_setter_does_not_replace_valid_value_on_error(self):
        nasabah = Nasabah("Alya", "DEMO-001", "08xx")

        with self.assertRaises(ValueError):
            nasabah.set_nama("  ")

        self.assertEqual(nasabah.get_nama(), "Alya")

    def test_string_representation_contains_name_and_id(self):
        nasabah = Nasabah("Alya", "DEMO-001", "08xx")

        self.assertEqual(str(nasabah), "Alya | ID: DEMO-001")


if __name__ == "__main__":
    unittest.main()