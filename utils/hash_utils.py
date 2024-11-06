# hash_utils.py
# ---------------------------------------------------------------------
# DGT-ZK Protocol: Hashing Utilities Module
#
# Provides hashing functions for standard cryptographic operations.
# This module supports SHA-256 and Keccak for consistent data hashing
# across the protocol.
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

import hashlib
from eth_utils import keccak

def hash_sha256(data):
    """
    Hashes data using SHA-256.

    Parameters:
        data (str): The data to hash.

    Returns:
        str: Hex-encoded SHA-256 hash of the input data.
    """
    return hashlib.sha256(data.encode()).hexdigest()

def hash_keccak(data):
    """
    Hashes data using Keccak (Ethereum-compatible).

    Parameters:
        data (str): The data to hash.

    Returns:
        str: Hex-encoded Keccak hash of the input data.
    """
    return keccak(text=data).hex()
