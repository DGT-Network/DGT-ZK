# DGT-ZK Protocol: Utils Package

The `utils` package provides a set of essential utility functions and modules that support the core functionalities of the DGT-ZK Protocol. This package centralizes common operations such as hashing, data validation, formatting, and timestamp management, ensuring consistency and reusability across all modules in the protocol.

## Package Structure

The package is organized into four main modules, each focusing on a specific type of utility function. Each module is designed to handle a particular aspect of utility operations, making the overall code more modular and easier to maintain.

### Modules

* **hash_utils.py**: Contains cryptographic hashing functions, using standard algorithms such as SHA-256 and Keccak.
* **helpers.py**: Provides general helper functions, including data validation and type checks.
* **format_utils.py**: Includes data formatting utilities, such as JSON serialization and hexadecimal conversions.
* **time_utils.py**: Manages timestamp generation and formatting, ensuring consistent time-related operations across the protocol.

## Setup Instructions

To install any dependencies, ensure you have the following installed:

```bash
pip install eth-utils
```

## Module Descriptions and Usage

### 1. hash_utils.py

**Purpose**: Standardizes cryptographic hashing operations for the protocol.

#### Functions

* `hash_sha256(data)`: Generates an SHA-256 hash of the input data.
* `hash_keccak(data)`: Generates an Ethereum-compatible Keccak hash of the input data.

#### Example Usage

```python
from utils.hash_utils import hash_sha256, hash_keccak

data = "sample_data"
sha256_hash = hash_sha256(data)
keccak_hash = hash_keccak(data)

print("SHA-256 Hash:", sha256_hash)
print("Keccak Hash:", keccak_hash)
```

### 2. helpers.py

**Purpose**: Provides utility functions for data validation and general checks.

#### Functions

* `is_hex_string(data)`: Checks if a string is a valid hexadecimal.
* `is_valid_amount(amount)`: Verifies if an amount is a non-negative integer.

#### Example Usage

```python
from utils.helpers import is_hex_string, is_valid_amount

hex_data = "a1b2c3"
amount = 100

print("Is valid hex:", is_hex_string(hex_data))
print("Is valid amount:", is_valid_amount(amount))
```

### 3. format_utils.py

**Purpose**: Manages data formatting for JSON serialization, hex conversion, and binary-to-hex transformations.

#### Functions

* `to_json(data)`: Converts a dictionary to JSON format.
* `from_json(json_data)`: Parses JSON data to a dictionary.
* `to_hex(data)`: Converts binary data to a hexadecimal string.

#### Example Usage

```python
from utils.format_utils import to_json, from_json, to_hex

data = {"key": "value"}
json_data = to_json(data)
parsed_data = from_json(json_data)
binary_data = b'\x01\x02'
hex_data = to_hex(binary_data)

print("JSON Data:", json_data)
print("Parsed Data:", parsed_data)
print("Hex Data:", hex_data)
```

### 4. time_utils.py

**Purpose**: Handles time-related functions, such as generating timestamps in ISO 8601 format.

#### Functions

* `current_timestamp()`: Returns the current timestamp in UTC ISO 8601 format.
* `timestamp_to_iso(timestamp)`: Converts a Unix timestamp to ISO 8601 format.

#### Example Usage

```python
from utils.time_utils import current_timestamp, timestamp_to_iso

print("Current Timestamp:", current_timestamp())
print("ISO Timestamp:", timestamp_to_iso(1627891234))
```

## Package Initialization (`__init__.py`)

The `__init__.py` file imports key functions from each module, providing a unified interface for accessing all utilities.

#### Example Usage

```python
from utils import hash_sha256, is_hex_string, to_json, current_timestamp

data = "example"
print("SHA-256 Hash:", hash_sha256(data))
print("Is Hex:", is_hex_string("a1b2"))
print("JSON Data:", to_json({"key": "value"}))
print("Timestamp:", current_timestamp())