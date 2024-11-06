# pedersen_commitment.py
# ---------------------------------------------------------------------
# DGT-ZK Protocol: Pedersen Commitment Module
#
# This module provides functions to create and verify Pedersen commitments
# using the ecdsa library. Pedersen commitments allow secure verification of
# committed values (e.g., transactions amounts) without revealing the actual
# values, supporting privacy and security within the DGT-ZK Protocol.
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

from ecdsa import SECP256k1, SigningKey
import secrets

# Define the elliptic curve and generator point
curve = SECP256k1
G = curve.generator
n = curve.order


def generate_random():
    """
    Generates a random blinding factor for use in Pedersen commitments.

    Returns:
        int: A random integer to be used as the blinding factor.
    """
    return secrets.randbelow(n)


def create_commitment(value, random_factor=None):
    """
    Creates a Pedersen commitment for a given value with an optional random factor.

    Parameters:
        value (int): The value to commit to (e.g., transactions amount).
        random_factor (int, optional): The blinding factor. If not provided, a random value is used.

    Returns:
        tuple: (commitment, random_factor) where commitment is an elliptic curve point
               representing the Pedersen commitment.
    """
    random_factor = random_factor or generate_random()
    commitment = (G * value) + (G * random_factor)
    return commitment, random_factor


def verify_commitment(commitment, value, random_factor):
    """
    Verifies a Pedersen commitment by checking if it matches the provided value and random factor.

    Parameters:
        commitment (Point): The commitment point to verify.
        value (int): The committed value.
        random_factor (int): The random factor used in the commitment.

    Returns:
        bool: True if the commitment is valid, False otherwise.
    """
    expected_commitment = (G * value) + (G * random_factor)
    return commitment == expected_commitment
