# utils.py
# ---------------------------------------------------------------------
# DGT-ZK Protocol: Utility Functions Module
#
# This module provides utility functions for data formatting, hashing,
# and JSON conversion. It includes helper functions to format transactions
# keys, hash transactions details, and convert data to JSON format, making
# interactions with the database simpler and ensuring consistent handling
# across the DGT-ZK Protocol.
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

import json
from hashlib import sha256


def format_key(tx_family, key):
    """
    Formats keys with TX_FAMILY prefix for better categorization.

    Parameters:
        tx_family (str): Transaction family or type (e.g., 'financial_tx', 'notary_tx').
        key (str): The original key or identifier.

    Returns:
        str: Formatted key with `tx_family` prefix.
    """
    return f"{tx_family}_{key}"


def hash_transaction(tx):
    """
    Hashes transactions details to create a unique transactions ID.

    Parameters:
        tx (dict): The transactions data to hash.

    Returns:
        str: SHA-256 hash of the transactions data as a unique transactions ID.
    """
    tx_data = json.dumps(tx, sort_keys=True).encode()
    return sha256(tx_data).hexdigest()


def convert_to_json(data):
    """
    Converts data to JSON format for compatibility and readability.

    Parameters:
        data (dict): Data to convert to JSON format.

    Returns:
        str: JSON-encoded string representation of the data.
    """
    try:
        return json.dumps(data, indent=4)
    except (TypeError, ValueError) as e:
        print(f"Error converting to JSON: {e}")
        return None
