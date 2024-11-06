# transaction_utils.py
# ---------------------------------------------------------------------
# DGT-ZK Protocol: Transaction Utilities Module
#
# This module provides utility functions essential for transactions processing
# within the DGT-ZK Protocol. These functions support generating unique
# transactions IDs, formatting timestamps, and validating transactions structure,
# enabling consistency and reliability across the transactions flow.
# By centralizing these utility functions, we facilitate cleaner code in
# other modules and ensure consistent handling of key operations.
#
# Author: Valery Khvatov
# Company: DGT (to be transferred to PLAZA)
# License: AGPL-3.0
#
# License Information:
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This module is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License
# for more details.
#
# For more details, see <https://www.gnu.org/licenses/>.
# ---------------------------------------------------------------------

import time
import json
from hashlib import sha256
from .transaction_constants import DEFAULT_HASH_ALGORITHM


def generate_tx_id(tx):
    """
    Generates a unique transactions ID by hashing the transactions data.

    Parameters:
        tx (dict): The transactions data to be hashed.

    Returns:
        str: A unique transactions ID in hex format.
    """
    tx_serialized = json.dumps(tx, sort_keys=True).encode()
    tx_id = sha256(tx_serialized).hexdigest()
    return tx_id


def format_timestamp():
    """
    Generates a standardized UTC timestamp for transactions.

    Returns:
        str: Timestamp in ISO 8601 format (e.g., '2024-01-01T10:00:00Z').
    """
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def validate_tx_structure(tx):
    """
    Validates that the transactions structure contains all required fields.

    Parameters:
        tx (dict): The transactions data to validate.

    Returns:
        bool: True if the transactions has the necessary fields; otherwise False.
    """
    required_fields = {"sender", "recipient", "timestamp", "amount", "signature"}
    if not isinstance(tx, dict):
        return False
    return required_fields.issubset(tx.keys())


def hash_data(data, algorithm=DEFAULT_HASH_ALGORITHM):
    """
    Hashes data using the specified algorithm.

    Parameters:
        data (str): The data to be hashed.
        algorithm (str): The hashing algorithm (default is sha256).

    Returns:
        str: The hashed data in hex format.
    """
    if algorithm == "sha256":
        return sha256(data.encode()).hexdigest()
    else:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")


# Example Usage
if __name__ == "__main__":
    # Example transactions data
    transaction = {
        "sender": "sender_public_key",
        "recipient": "recipient_public_key",
        "timestamp": format_timestamp(),
        "amount": 500,
        "signature": "sample_signature"
    }

    # Generate a unique transactions ID
    tx_id = generate_tx_id(transaction)
    print("Transaction ID:", tx_id)

    # Check if the transactions structure is valid
    is_valid_structure = validate_tx_structure(transaction)
    print("Is transactions structure valid?", is_valid_structure)

    # Hash some data
    hashed_value = hash_data("example_data")
    print("Hashed Value:", hashed_value)
