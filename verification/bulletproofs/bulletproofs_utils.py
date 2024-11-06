# bulletproofs_utils.py
# ---------------------------------------------------------------------
# DGT-ZK Protocol: Bulletproofs Utilities Module
#
# This module provides shared utility functions for Bulletproofs implementation.
# These functions are used across all options (dalek-bulletproofs FFI,
# fastecdsa, and emulation) to ensure consistency and reduce redundancy.
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
from typing import List


def compute_challenge(transcript: str, length: int = 256) -> int:
    """
    Computes a cryptographic challenge based on a transcript using a hash function.
    This function is shared across implementations to ensure consistent proof creation.

    Parameters:
        transcript (str): Input string or data used to derive the challenge.
        length (int): Desired bit-length of the challenge (default: 256 bits).

    Returns:
        int: The computed challenge value as an integer.
    """
    # Hash the transcript using SHA-256 and convert to integer
    hash_value = hashlib.sha256(transcript.encode()).digest()
    challenge = int.from_bytes(hash_value, "big") % (2 ** length)

    return challenge


def multiexponentiation(bases: List[int], exponents: List[int]) -> int:
    """
    Efficiently computes the multiexponentiation of given bases and exponents.
    This function is used by all implementations to perform multi-exponentiation
    calculations consistently.

    Parameters:
        bases (list[int]): List of base elements.
        exponents (list[int]): Corresponding list of exponents.

    Returns:
        int: Result of the multiexponentiation computation.

    Raises:
        ValueError: If the lengths of bases and exponents do not match.
    """
    if len(bases) != len(exponents):
        raise ValueError("Bases and exponents must be of the same length.")

    result = 1
    for base, exponent in zip(bases, exponents):
        result *= base ** exponent  # Can be optimized further with specific libraries
    return result


def hash_to_point(data: str) -> int:
    """
    Hashes arbitrary data to an integer suitable for use as a point on an elliptic curve.
    This is used for consistency in hashing data to curve points across implementations.

    Parameters:
        data (str): Data to be hashed and converted to a point.

    Returns:
        int: Integer representation of the hash, used as a point on the curve.
    """
    # Hash data and convert to an integer point
    point = int(hashlib.sha256(data.encode()).hexdigest(), 16)
    return point


def validate_commitment_range(commitment: int, range_min: int, range_max: int) -> bool:
    """
    Validates that a commitment falls within a specified range. This function
    helps ensure that proofs align with the expected range constraints across
    implementations.

    Parameters:
        commitment (int): The commitment or value to be validated.
        range_min (int): Minimum allowable value.
        range_max (int): Maximum allowable value.

    Returns:
        bool: True if the commitment is within the specified range; otherwise, False.
    """
    return range_min <= commitment <= range_max
