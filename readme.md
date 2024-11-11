# Fiat to USDC Conversion System

## Overview

This document outlines the architecture, methodology, reconciliation algorithm, and technical components for a fiat-to-USDC conversion system. The system is designed to convert fiat deposits into USDC and transfer the equivalent amount to user wallets. It includes detailed logging, discrepancy handling, and error management to ensure accurate and auditable transactions.

### Diagrams

[Architecture and Flow Diagram](https://excalidraw.com/#json=Q_c7K3jvF_3TjCtWk98s5,qkzOHrWRleywk0i2WHc2HA)

---

## Code: Reconciliation Algorithm Implementation

This Python implementation includes detailed logging, error handling, and timestamp tracking to support transparency and traceability in the reconciliation process.

```python
import logging
from datetime import datetime

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Sample data for fiat deposits and USDC transfers
fiat_deposits = [
    {'reference_id': '12345', 'amount': 1000.00, 'currency': 'USD', 'timestamp': datetime(2024, 11, 1, 10, 30)},
    {'reference_id': '12346', 'amount': 500.00, 'currency': 'USD', 'timestamp': datetime(2024, 11, 1, 11, 15)},
]

usdc_transfers = [
    {'reference_id': '12345', 'amount': 1000.00, 'currency': 'USDC', 'timestamp': datetime(2024, 11, 1, 10, 45)},
    {'reference_id': '12346', 'amount': 500.00, 'currency': 'USDC', 'timestamp': datetime(2024, 11, 1, 11, 30)},
]

# Reconciliation function
def reconcile_transactions(fiat_deposits, usdc_transfers):
    matched_transactions = []
    discrepancies = []

    for deposit in fiat_deposits:
        match_found = False
        for transfer in usdc_transfers:
            if deposit['reference_id'] == transfer['reference_id']:
                if deposit['amount'] == transfer['amount']:
                    logging.info(f"Match found for Reference ID {deposit['reference_id']}")
                    matched_transactions.append({
                        'reference_id': deposit['reference_id'],
                        'fiat_amount': deposit['amount'],
                        'usdc_amount': transfer['amount'],
                        'status': 'Matched',
                        'match_time': datetime.now()
                    })
                    usdc_transfers.remove(transfer)
                    match_found = True
                    break
                else:
                    logging.warning(f"Amount mismatch for Reference ID {deposit['reference_id']}: "
                                    f"Fiat {deposit['amount']} vs USDC {transfer['amount']}")
                    discrepancies.append({
                        'reference_id': deposit['reference_id'],
                        'issue': 'Amount mismatch',
                        'fiat_amount': deposit['amount'],
                        'usdc_amount': transfer['amount'],
                        'timestamp': datetime.now()
                    })
                    match_found = True
                    usdc_transfers.remove(transfer)
                    break

        if not match_found:
            logging.error(f"No matching transfer found for Reference ID {deposit['reference_id']}")
            discrepancies.append({
                'reference_id': deposit['reference_id'],
                'issue': 'No matching transfer found',
                'fiat_amount': deposit['amount'],
                'usdc_amount': None,
                'timestamp': datetime.now()
            })

    if discrepancies:
        logging.error(f"Reconciliation completed with {len(discrepancies)} discrepancies found.")
    else:
        logging.info("Reconciliation completed successfully with all matches found.")

    return {
        'matched_transactions': matched_transactions,
        'discrepancies': discrepancies
    }

# Run reconciliation
result = reconcile_transactions(fiat_deposits, usdc_transfers)
print("Matched Transactions:", result['matched_transactions'])
print("Discrepancies:", result['discrepancies'])

## Enhancements Added

### Detailed Logging
- **Levels**: Includes INFO, WARNING, and ERROR levels for various events to provide traceability and insights into the reconciliation process.
- **Usage**: Logs successful matches, amount mismatches, and unmatched deposits for further analysis.

### Discrepancy Handling
- **Issues Captured**: Identifies issues like amount mismatches and unmatched deposits.
- **Reviewable Output**: Logs each discrepancy and includes it in the output for audit purposes.

### Timestamp Tracking
- **Purpose**: Records each transaction and discrepancy with a timestamp.
- **Benefit**: Enables better audit and tracking for each action.

### Extended Return Structure
- **Components**: Returns both `matched_transactions` and `discrepancies` for further analysis.
- **Flexibility**: Supports more detailed output for error analysis and reporting.

### Removals and Edge Handling
- **Duplicate Handling**: Removes transfers from the `usdc_transfers` list once matched to prevent duplicate matching.

---

## Methodology

### Key Components and Architecture Overview

#### Treasury Wallet
- **Description**: A centralized, secure on-chain wallet that holds USDC for distribution.
- **Features**: Multi-sig or hardware wallet security, high availability, and role-based access control.

#### Fiat Bank Account (Onramp)
- **Description**: The entry point for fiat deposits.
- **Security**: Encrypted connections and real-time monitoring for transactions.

#### Liquidity Pool (Rebalancing Mechanism)
- **Description**: Ensures the treasury wallet remains funded during high transaction volumes.
- **Functionality**: Automated rebalancing and interfaces with external exchanges if necessary.

#### User Wallets
- **Security**: Checks wallet addresses using checksum and format validation.

#### Reconciliation System
- **Features**: Automated matching, real-time updates, and discrepancy alerting.

#### Transaction Monitoring System
- **Capabilities**: Handles retries for failed transactions, confirms transfers, and notifies users.

---

## Transaction Flow

1. **User Initiates a Fiat Transfer**
   - User sends fiat to the onramp bank account with a reference ID.

2. **Fiat Deposit Detection**
   - System detects the deposit and logs the transaction.

3. **Fiat-to-USDC Conversion Check**
   - System checks treasury or liquidity pool for sufficient USDC balance.

4. **USDC Transfer Execution**
   - Transfer to the user’s wallet is initiated and logged.

5. **Confirmation and Reconciliation**
   - Cross-verifies fiat deposit with on-chain transaction and updates the internal ledger.

---

## Reconciliation Algorithms

1. **Transaction Matching**
   - Matches fiat deposits with USDC transactions using unique identifiers.

2. **Double-entry Ledger System**
   - Each fiat deposit is a debit; corresponding USDC transfer is a credit.

3. **Batch Verification**
   - Periodic matching jobs handle missed events.

4. **Error Handling Workflow**
   - Includes retry mechanisms, user notifications, and alerts for unresolved issues.

---

## Technical Component Architecture

- **Webhooks/API Integrator**: Monitors fiat deposit data.
- **Liquidity Manager Module**: Manages treasury funding.
- **Blockchain Interaction Module**: Uses smart contracts to send USDC.
- **Reconciliation Engine**: Matches records and handles audits.
- **User Notification System**: Sends real-time updates via email or SMS.
