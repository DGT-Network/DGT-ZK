# ---------------------------------------------------------------------
# DGT-ZK Protocol: Bulletproofs Range Proof Module
#
# This module implements range proofs as part of the Bulletproofs functionality
# within the DGT-ZK Protocol. Range proofs ensure that a committed value lies
# within a specific range without revealing the actual value. This implementation
# supports multiple backends, including FFI (dalek-bulletproofs), fastecdsa, and an emulation
# for debugging and testing purposes.
#
# This module is part of the `bulletproofs` subpackage under the `verification` package
# and contributes to secure, private, and efficient verification within the DGT-ZK Protocol.
#
# Dependencies:
# - ecdsa
# - fastecdsa (optional, for fastecdsa-based implementation)
# - ffi (optional, for dalek-bulletproofs FFI-based implementation)
# - emulation (optional, for non-production testing)
#
# Description of Core Functions:
# - create_range_proof(value, min_value, max_value): Generates a range proof
#   for a committed value within the specified range.
# - validate_range_proof(commitment, proof, min_value, max_value): Verifies
#   that the proof for the committed value is within the given range.
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


from fastecdsa.curve import secp256k1
from fastecdsa.point import Point
from bulletproofs_core import generate_bulletproof, verify_bulletproof
from bulletproof_utils import compute_challenge
import secrets


def create_range_proof(amount, g, h, range_min, range_max):
    """
    Creates a range proof for a given amount using Pedersen Commitment and Bulletproofs.

    Parameters:
        amount (int): Transaction amount to be committed and proven.
        g, h (Point): Generators for Pedersen Commitment.
        range_min, range_max (int): Range limits for proof verification.

    Returns:
        tuple: (commitment, proof) where `commitment` is the Pedersen Commitment,
               and `proof` is the Bulletproof for range verification.
    """
    blinding_factor = secrets.randbelow(secp256k1.q)
    commitment = (g * amount) + (h * blinding_factor)
    proof = generate_bulletproof(commitment, range_min, range_max)
    return commitment, proof


def validate_range_proof(commitment, proof, range_min, range_max):
    """
    Validates a range proof for a given commitment using Bulletproofs.

    Parameters:
        commitment (Point): Pedersen Commitment to validate.
        proof (dict): The Bulletproof range proof to verify.
        range_min, range_max (int): Range limits for the committed amount.

    Returns:
        bool: True if proof is valid; False otherwise.
    """
    return verify_bulletproof(commitment, proof, range_min, range_max)
