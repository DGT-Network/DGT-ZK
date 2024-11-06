# emulation.py
# ---------------------------------------------------------------------
# DGT-ZK Protocol: Bulletproof Emulation Module
#
# This module provides an emulated Bulletproof implementation for testing
# and debugging purposes. It integrates with shared utility and core
# modules for consistent function calls across different implementations.
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

from .bulletproofs_utils import compute_challenge  # Shared utility for challenge computation
from .range_proof import check_range  # Placeholder for range check utility if available


def generate_bulletproof(commitment, range_min, range_max, simulate_correct=True):
    """
    Generates an emulated Bulletproof for a given commitment within a specified range.

    Parameters:
        commitment (int): Emulated commitment representing the transactions amount.
        range_min (int): The minimum allowed value in the range.
        range_max (int): The maximum allowed value in the range.
        simulate_correct (bool): If True, simulates a valid proof; if False, simulates an invalid proof.

    Returns:
        proof (str): Emulated Bulletproof proof, represented as a string for simplicity.
    """
    # Check that the commitment falls within range for correct emulation behavior
    if not check_range(commitment, range_min, range_max):
        raise ValueError("Commitment is out of the specified range.")

    # Simulate proof generation
    proof_status = "valid" if simulate_correct else "invalid"

    # Emulate proof as a hash-based identifier using a shared utility function
    proof = compute_challenge(f"{commitment}-{range_min}-{range_max}-{proof_status}")

    return proof


def verify_bulletproof(commitment, proof, range_min, range_max, expected_correct=True):
    """
    Verifies an emulated Bulletproof within a specified range.

    Parameters:
        commitment (int): Emulated commitment representing the transactions amount.
        proof (str): The emulated Bulletproof proof to verify.
        range_min (int): The minimum allowed value in the range.
        range_max (int): The maximum allowed value in the range.
        expected_correct (bool): If True, expects proof to be correct; if False, expects proof to be incorrect.

    Returns:
        bool: True if the emulated proof is considered valid; otherwise, False.
    """
    # Generate a "correct" proof for comparison using the same shared utility function
    correct_proof = generate_bulletproof(commitment, range_min, range_max, simulate_correct=expected_correct)

    # Simulate verification by comparing the input proof to the "correct" proof
    return proof == correct_proof
