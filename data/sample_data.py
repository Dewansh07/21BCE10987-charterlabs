from datetime import datetime

# Sample fiat deposit and USDC transfer data
fiat_deposits = [
    {'reference_id': '9876', 'amount': 1000.00, 'currency': 'USD', 'timestamp': datetime(2024, 11, 1, 10, 30)},
    {'reference_id': '12346', 'amount': 500.00, 'currency': 'USD', 'timestamp': datetime(2024, 11, 1, 11, 15)},
]

usdc_transfers = [
    {'reference_id': '9876', 'amount': 1000.00, 'currency': 'USDC', 'timestamp': datetime(2024, 11, 1, 10, 45)},
    {'reference_id': '12346', 'amount': 500.00, 'currency': 'USDC', 'timestamp': datetime(2024, 11, 1, 11, 30)},
]
