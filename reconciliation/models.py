from datetime import datetime
from typing import Optional

class Transaction:
    def __init__(self, reference_id: str, amount: float, currency: str, timestamp: datetime):
        self.reference_id = reference_id
        self.amount = amount
        self.currency = currency
        self.timestamp = timestamp
