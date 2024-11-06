# DGT-ZK Protocol: Transactions Package

This package provides the core modules for managing, verifying, and securely anchoring transactions in the DGT-ZK Protocol. It integrates essential functionalities such as creating, validating, anchoring, and compliance verification of transactions, designed to support decentralized, secure transaction flows.

## Package Modules

### 1. `transaction_constants.py`

This module defines constants to ensure consistent usage across all transaction modules.

**Explanation of Key Constants:**

* **Transaction Family Types**: Constants like `TX_FAMILY_FINANCIAL` help categorize transaction types (e.g., financial, notary) for easier storage and retrieval.
* **DEFAULT_CANCELLATION_WINDOW**: Sets a period for temporary anchoring, allowing for transaction cancellation within a certain timeframe.
* **Cryptographic Constants**: Ensures consistency in cryptographic algorithms (curves, hashes) used for signatures.
* **Database Paths**: Default paths for LMDB databases, facilitating environment setup.
* **Compliance Check Levels**: Defines levels for KYC/AML compliance validation, making it adaptable to regulatory requirements.
* **Validation Settings**: Options like `ENABLE_BULLETPROOF_VALIDATION` allow for flexible configuration of validation settings.

### 2. `transaction_utils.py`

This module provides utility functions commonly used across the transaction package.

**Key Functions and Descriptions:**

* `generate_tx_id(tx)`: Generates a unique ID for a transaction using a hash of the transaction data.
* `format_timestamp()`: Returns a UTC timestamp in ISO 8601 format for consistent logging.
* `validate_tx_structure(tx)`: Ensures a transaction has the required fields (`sender`, `recipient`, `amount`, etc.).
* `hash_data(data, algorithm)`: Hashes data using the specified algorithm, defaulting to SHA-256.

**Example Usage Summary**: The module provides essential functions for generating IDs, validating transaction structures, and hashing data, ensuring uniform transaction management.

### 3. `transaction_verification.py`

This module handles compliance and verification checks.

**Key Functions and Descriptions:**

* `compliance_check(tx, level)`: Verifies that a transaction complies with specified KYC/AML levels.
* `verify_amount_range(tx)`: Checks that the transaction amount falls within valid ranges using Bulletproofs.
* `verify_signature(tx, public_key)`: Validates the transaction's digital signature.
* `get_blacklist_addresses()`: Returns a list of blacklisted addresses, useful for compliance checks.

**Example Usage Summary**: The module enforces protocol compliance, validates transaction ranges, and confirms digital signatures, aligning transactions with regulatory requirements.

### 4. `transaction_anchor.py`

Implements anchoring logic, allowing transactions to be securely anchored in the database.

**Key Functions and Descriptions:**

* `__init__(self, db_type="ledger", cancellation_window=60)`: Initializes the anchoring system with a specific database type and cancellation window.
* `anchor_transaction(self, tx)`: Anchors a transaction in the selected database with a timestamp and unique ID.
* `verify_anchor(self, tx_id)`: Checks if a transaction is anchored.
* `cancel_anchor(self, tx_id)`: Cancels a transaction within the specified window.
* `list_anchors(self)`: Lists all anchored transactions.

**Example Usage Summary**: The module facilitates anchoring, verification, and cancellation of transactions, providing a secure transaction history.

### 5. `transaction_flow.py`

Integrates all functionalities to manage the main transaction flow, covering encryption, validation, and anchoring.

**Key Functions and Descriptions:**

* `create_and_encrypt_transaction`: Manages the complete transaction lifecycle, including header creation, encryption, commitment generation, signing, and optional anchoring.
* `validate_and_anchor_transaction`: Verifies transaction integrity and commitment, anchoring if valid.
* `cancel_transaction`: Allows transaction cancellation within the specified window.

**Example Usage Summary**: This module orchestrates the transaction lifecycle, ensuring secure, compliant record-keeping.

### 6. `transaction_emulator.py` (Optional)

An emulator that simulates transaction flows, useful for testing or simulating operations without connecting to an external network.

**Key Features:**

* **In-Memory Storage**: Uses dictionaries for emulated ledger and notary storage, facilitating easy testing.
* **Transaction Creation**: Functions for creating transactions with encryption and commitments, closely resembling real protocol behavior.
* **Validation and Anchoring**: Simulates signing, verification, and storage for testing purposes.
* **Cancellation Logic**: Implements a simulated `cancel_transaction` method.
* **List Functions**: Includes listing functions for inspecting ledger and notary states, ideal for verifying the emulator’s current state.

## Setup Instructions

### Dependencies

To use the package, install the necessary dependencies:

```bash
pip install lmdb ecdsa eth_keys eth_utils
```

### LMDB Database Initialization

Initialize the LMDB environments for `ledger_db` and `notary_db`:

```python
from lmdb import Environment

# Ledger database
ledger_db = Environment("ledger_db", max_dbs=1)

# Notary database
notary_db = Environment("notary_db", max_dbs=1)
```

## Example Usage

### 1. Transaction Management

Creating and encrypting a transaction:

```python
from transactions.transaction_flow import TransactionFlow
from encryption.signature import generate_keys

# Key generation for sender
private_key, public_key = generate_keys()

# Initialize transaction flow
tx_flow = TransactionFlow()

# Create a transaction with encryption and optional anchoring
tx = tx_flow.create_and_encrypt_transaction(
    tx_family="financial_tx",
    sender=public_key,
    recipient="recipient_public_key",
    amount=100,
    private_key=private_key,
    notary=True
)
print("Created Transaction:", tx)
```

### 2. Verifying and Anchoring a Transaction

```python
# Validate and optionally anchor the transaction
is_valid = tx_flow.validate_and_anchor_transaction(tx, public_key, notary=True)
print("Transaction Valid and Anchored:", is_valid)
```

### 3. Canceling an Anchored Transaction

```python
# Cancel the transaction if within cancellation window
is_canceled = tx_flow.cancel_transaction(tx["tx_id"])
print("Transaction Canceled:", is_canceled)
```

### 4. Listing All Anchored Transactions

```python
# Retrieve a list of all anchored transactions
all_anchors = tx_flow.transaction_anchor.list_anchors()
print("All Anchored Transactions:", all_anchors)
```

## Closing Databases

Always close database connections when done:

```python
tx_flow.close()
```

This README provides a full overview of the transactions package, setup instructions, and key usage examples. The package is designed to support secure, compliant transaction management within the DGT-ZK Protocol framework, from creation and encryption to validation, anchoring, and cancellation.