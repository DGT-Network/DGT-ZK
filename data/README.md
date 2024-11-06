DGT-ZK Protocol: Data Package
--------------------------------

This package provides essential modules for managing transactions, signatures, data storage, and export functionalities for the DGT-ZK Protocol. The data package uses an LMDB-based Key-Value storage system to handle ledger and notary transactions, with support for digital signatures and Ethereum-compatible addresses.

## Package Modules

- **ledger_db.py**: Manages transaction storage, retrieval, and balance calculations in the ledger.
- **notary_db.py**: Stores encrypted notary records and provides retrieval functions.
- **transaction.py**: Defines the transaction structure and provides creation and validation functions.
- **signature.py**: Manages ECDSA digital signatures, key generation, and Ethereum-compatible address generation.
- **utils.py**: Contains utility functions for data formatting, hashing, and JSON conversion.
- **export.py**: Exports database records to CSV format for analysis and testing.

## Setup Instructions

### Dependencies

To use the package, install the necessary dependencies:
```bash
pip install lmdb ecdsa eth_keys eth_utils
```
# LMDB Database Initialization

Build environments with:

```python
from lmdb import Environment

# Ledger database
ledger_db = Environment("ledger_db", max_dbs=1)

# Notary database
notary_db = Environment("notary_db", max_dbs=1)
```
## Package Modules:
### 1. ledger_db.py

**Description**: Manages transactions, such as saving, retrieving, and calculating balances. This module utilizes LMDB to store Key-Value pairs, where keys are prefixed with TX_FAMILY to group transaction types (e.g., financial, notary). Includes methods for saving transactions, retrieving transaction details, and calculating user balances.


**Core Functions:**

---------------------------

1) __init__:

Initializes the LMDB database with a specified path and size.
map_size sets the maximum database size, which can be adjusted as needed.
save_transaction:

Stores a transaction in the ledger with a unique key generated from TX_FAMILY and a hash of the transaction data.
This key structure enables grouping and retrieval of transactions based on their family type (e.g., financial_tx or notary_tx).

**Parameters**:

- tx: Dictionary containing transaction data, including TX_FAMILY, sender, recipient, amount, and signature.
- Transaction ID: A hash of the transaction is generated using SHA-256, ensuring each transaction has a unique identifier.
----------------------------------

2) get_transaction:

Retrieves a transaction by its ID and TX_FAMILY.

**Parameters**:
- tx_id: Unique transaction ID (hash).
- tx_family: Transaction family type for filtering.

Returns the transaction as a dictionary if found, or None if the transaction ID does not exist.

----------------------------------

3) get_balance:

Calculates the balance for a specific address by iterating over all transactions in the TX_FAMILY.

**Parameters**:
- address: The public address whose balance is being calculated.
- tx_family: Specifies the transaction family for filtering (default is financial_tx).

If the address is a recipient, the amount is added to the balance. If the address is a sender, the amount is subtracted.

Returns the total balance for the address.

----------------------------------

4) close:

Closes the LMDB environment to free resources. This should be called when the database is no longer needed to ensure data integrity.

**Usage Example**
```python
from data.ledger_db import LedgerDB

# Initialize the LedgerDB

ledger_db = LedgerDB(db_path='ledger_db')

# Example transactions data
transaction = {
    "TX_FAMILY": "financial_tx",
    "sender": "sender_public_key",
    "recipient": "recipient_public_key",
    "amount": 500,
    "signature": "sample_signature",
    "timestamp": "2024-01-01T10:00:00Z"
}

# Save the transactions
ledger_db.save_transaction(transaction)

# Retrieve the transactions by its ID
tx_id = sha256(json.dumps(transaction, sort_keys=True).encode()).hexdigest()
retrieved_tx = ledger_db.get_transaction(tx_id, tx_family="financial_tx")
print("Retrieved Transaction:", retrieved_tx)

# Calculate balance for the recipient
balance = ledger_db.get_balance("recipient_public_key")
print("Recipient Balance:", balance)

# Close the database
ledger_db.close()
```

### 2. notary_db.py

**Description**: This module emulates a notary system by securely storing encrypted records in a separate LMDB database. It supports operations like storing notarized data, retrieving records, and listing all notary entries for verification or testing.

**Core Functions**:

-----------------------

1) __init__:

Initializes the LMDB database with a specified path and size for managing notary records.
map_size defines the maximum storage size for the database.
save_notary_record:

Saves a notary record in the database, assigning a unique record_id by hashing the record content.

**Parameters**:
- record: Dictionary containing the notary data, such as content, timestamp, and signature.
- Record ID: Uses SHA-256 to generate a unique identifier for each record, ensuring no duplicates.

----------------------------------

2) get_notary_record:

Retrieves a specific notary record by its record_id.

**Parameters**:
- record_id: The unique hash identifier for the notary record.

- Returns the record as a dictionary if it exists, or None if it’s not found.

----------------------------------

3) list_notary_records:

Lists all stored notary records in the database. Useful for verification and testing, allowing easy access to all stored records without knowing specific IDs.
Returns a list of dictionaries, each representing a notary record.

----------------------------------

4) close:

Closes the LMDB database environment to free up resources. Should be called when the database is no longer needed.

**Usage Example**

Here’s a usage example showing how to work with the NotaryDB module:

```python
from data.notary_db import NotaryDB

# Initialize NotaryDB
notary_db = NotaryDB(db_path='notary_db')

# Example notary record data
record = {
    "content": "Encrypted notary data",
    "timestamp": "2024-01-01T10:00:00Z",
    "signature": "notary_signature"
}

# Save the notary record
notary_db.save_notary_record(record)

# Retrieve the notary record by its ID
record_id = sha256(json.dumps(record, sort_keys=True).encode()).hexdigest()
retrieved_record = notary_db.get_notary_record(record_id)
print("Retrieved Record:", retrieved_record)

# List all notary records
all_records = notary_db.list_notary_records()
print("All Notary Records:", all_records)

# Close the database
notary_db.close()
```

### 3. transaction.py

**Description**: Defines transaction structure and provides functions for creating and validating transactions. Transactions are composed of a header (sender, recipient, timestamp, and signature) and a body (transaction details or encrypted content for notary transactions). This module interacts with ledger_db and notary_db.

**Core Functions**:

1) create_transaction:

Creates a new transaction and signs it with the sender’s private key.

**Parameters**:
- tx_family: Specifies the transaction family (e.g., financial_tx or notary_tx).
- sender: Public key of the transaction’s sender.
- recipient: Public key or address of the recipient.
- amount: The amount transferred in the transaction.
- private_key: The sender’s private key used to sign the transaction.
- is_notary: Boolean flag that indicates whether to store the transaction in notary_db (if True) or ledger_db (if False).

**Process**:
The transaction header is created, containing essential information such as sender, recipient, timestamp, and amount.
A unique transaction ID (tx_id) is generated by hashing the transaction header.
The transaction is signed using the sender’s private key.
Depending on is_notary, the transaction is stored either in notary_db or ledger_db.

**Returns**:
The completed transaction as a dictionary, including the transaction signature.

----------

2) validate_transaction:

Validates the structure and integrity of a transaction, as well as its digital signature.

**Parameters**:
- tx: The transaction data to validate.
- public_key: The public key of the sender, used to verify the transaction signature.

**Process**:

Checks that required fields (sender, recipient, timestamp, amount) are present in the transaction header.
Verifies the transaction’s signature using the verify_signature function.

**Returns**:
True if the transaction is valid and the signature matches; False otherwise.

**Usage Example**
Here’s an example of how to use the transaction.py module to create and validate a transaction:

```python
from data.transaction import create_transaction, validate_transaction
from encryption.signature import generate_keys

# Generate sender's keys
private_key, public_key = generate_keys()

# Transaction parameters
tx_family = "financial_tx"
sender = public_key
recipient = "recipient_public_key_example"
amount = 100

# Create and store a financial transactions
transaction = create_transaction(tx_family, sender, recipient, amount, private_key)

# Validate the created transactions
is_valid = validate_transaction(transaction, public_key)
print("Transaction valid:", is_valid)
```

### 5. utils.py
**Description**: Contains utility functions for formatting data, hashing, and data conversions. This module provides helper functions that support data formatting, hashing, and JSON conversion to streamline interactions with the databases and for easier data handling.

**Core Functions**:

-------------------

1) format_key:

Formats a key by prefixing it with TX_FAMILY, which helps categorize and distinguish transaction types in the database.

**Parameters**:
- tx_family: A string representing the transaction family (e.g., financial_tx or notary_tx).
- key: The original key or identifier to format.

**Returns**:
The formatted key as a string with the tx_family prefix, useful for database categorization and retrieval.

--------------

2) hash_transaction:

Hashes transaction details using SHA-256 to create a unique transaction ID. This helps in maintaining a consistent and unique identifier for each transaction.

**Parameters**:
- tx: A dictionary containing transaction details to be hashed.

**Returns**:
The SHA-256 hash of the transaction as a hex string, representing a unique transaction ID.

-------------

3) convert_to_json:

Converts a dictionary to a JSON-formatted string for compatibility and readability, especially useful when storing or displaying data.

**Parameters**:
- data: The dictionary or data structure to convert.

**Returns**:
JSON-encoded string representation of the data, or None if conversion fails due to incompatible types.

**Usage Example**
Here’s an example demonstrating the use of utils.py:

```python 
from data.utils import format_key, hash_transaction, convert_to_json

# Example transactions data
transaction = {
    "sender": "sender_public_key",
    "recipient": "recipient_public_key",
    "amount": 500,
    "timestamp": "2024-01-01T10:00:00Z"
}

# Format key with TX_FAMILY
formatted_key = format_key("financial_tx", "12345")
print("Formatted Key:", formatted_key)

# Hash transactions to generate a unique transactions ID
tx_id = hash_transaction(transaction)
print("Transaction ID:", tx_id)

# Convert transactions to JSON format
json_data = convert_to_json(transaction)
print("Transaction JSON:", json_data)
```

### 6. export.py
**Description**: This module exports database records to a CSV format for easier analysis and testing. It supports exporting all or filtered records, allowing inspection of stored transactions and notary entries without requiring a blockchain network.

**Core Functions**:

1) export_to_csv:

Exports all records from the specified LMDB database to a CSV file.

**Parameters**:
- database: The LMDB database environment, either ledger_db or notary_db.
- file_path: Path where the exported CSV file will be saved.

**Process**:
Opens the CSV file, writes a header, and iterates over all key-value pairs in the database.
Each record is saved in CSV format with a Key column (representing the record’s unique ID) and a Data column containing the record’s JSON data.

---------------------

2) export_filtered_to_csv:

Exports only records of a specific TX_FAMILY to a CSV file.

**Parameters**:
- database: The LMDB database environment, either ledger_db or notary_db.
- tx_family: Transaction family or type, used to filter the records for export.
- file_path: Path where the exported CSV file will be saved.

**Process**:
Opens the CSV file, writes a header, and iterates over key-value pairs.
Filters records based on the tx_family prefix in the key.
Saves each matching record with a Key column (unique ID) and a Data column containing JSON data.


**Usage Example**
```python
from lmdb import Environment
from data.export import export_to_csv, export_filtered_to_csv

# Example LMDB environment initialization for ledger_db
ledger_db_env = Environment("ledger_db", max_dbs=1)

# Export all records from the ledger_db
export_to_csv(ledger_db_env, "all_transactions.csv")

# Export only "financial_tx" records from the ledger_db
export_filtered_to_csv(ledger_db_env, "financial_tx", "financial_transactions.csv")
```




## More Examples

###  Transaction Management
Create and Save a Transaction:

```python 
from data.transaction import create_transaction
from encryption.signature import generate_keys

# Generate sender keys
private_key, public_key = generate_keys()
recipient = "recipient_public_key"

# Create a financial transactions
transaction = create_transaction("financial_tx", public_key, recipient, 100, private_key)
print("Transaction created:", transaction)
```

### Validate a Transaction:

```python
from data.transaction import validate_transaction

# Validate the transactions with sender's public key
is_valid = validate_transaction(transaction, public_key)
print("Transaction valid:", is_valid)
```

### Signature Management

Generate keys, sign transactions, and verify signatures:

```python
from encryption.signature import generate_keys, sign_transaction, verify_signature

private_key, public_key = generate_keys()
transaction_data = {"sender": public_key, "amount": 100}

signature = sign_transaction(transaction_data, private_key)
is_verified = verify_signature(transaction_data, public_key, signature)
print("Signature valid:", is_verified)
```

### Export Data to CSV

Export all records or filter by transaction family:
```python

from data.export import export_to_csv, export_filtered_to_csv

# Export all records
export_to_csv(ledger_db, "all_records.csv")

# Export only financial transactions
export_filtered_to_csv(ledger_db, "financial_tx", "financial_transactions.csv")
```

### Utility Functions

Format keys, hash transactions, and convert data to JSON:

```python 
from data.utils import format_key, hash_transaction, convert_to_json

formatted_key = format_key("financial_tx", "12345")
print("Formatted Key:", formatted_key)

tx_id = hash_transaction(transaction_data)
print("Transaction ID:", tx_id)

json_data = convert_to_json(transaction_data)
print("JSON Data:", json_data)
```

Closing Databases

Always close LMDB environments when done:
```python
ledger_db.close()
notary_db.close()
```
