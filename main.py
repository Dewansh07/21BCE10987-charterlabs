from config.logging_config import setup_logging
from data.sample_data import fiat_deposits, usdc_transfers
from reconciliation.reconciler import reconcile_transactions

# Initialize logging
setup_logging()

# Run the reconciliation process
result = reconcile_transactions(fiat_deposits, usdc_transfers)

# Display results
print("Matched Transactions:")
for match in result['matched_transactions']:
    print(match)

print("\nDiscrepancies:")
for discrepancy in result['discrepancies']:
    print(discrepancy)
