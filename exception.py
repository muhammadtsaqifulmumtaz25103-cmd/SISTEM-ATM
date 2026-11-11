"""Exception khusus untuk operasi ATM demo."""


class SaldoTidakCukupError(Exception):
    def __init__(self, saldo, dibutuhkan):
        super().__init__(
            f"Saldo tidak cukup! Saldo: Rp{saldo:,.2f}, "
            f"Dibutuhkan: Rp{dibutuhkan:,.2f}"
        )


class JumlahTidakValidError(Exception):
    def __init__(self, jumlah):
        super().__init__(f"Jumlah tidak valid: {jumlah}. Harus lebih dari 0.")
