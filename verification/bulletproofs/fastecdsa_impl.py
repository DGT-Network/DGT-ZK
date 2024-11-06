# fastecdsa_impl.py
# ---------------------------------------------------------------------
# DGT-ZK Protocol: Bulletproofs Implementation with Fastecdsa
#
# This module provides functions to simulate Bulletproof generation and
# verification using the fastecdsa library on Linux. Note that this is not
# a full Bulletproof implementation; it uses elliptic curve operations to
# emulate some aspects of Bulletproofs.
#
# Supported Platform: Linux
# Dependencies: Requires `fastecdsa` library if available.
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

try:
    from fastecdsa.curve import secp256k1
    from fastecdsa.point import Point
    from fastecdsa.util import int_to_bytes
    import secrets

    HAS_FASTECDSA = True
except ImportError:
    # If fastecdsa is not available, set a flag and provide warnings
    HAS_FASTECDSA = False
    secp256k1 = None
    Point = None
    int_to_bytes = None
    secrets = None


def generate_bulletproof(amount, range_min, range_max, g=None, h=None, blinding_factor=None, **kwargs):
    """
    Generates a simulated Bulletproof for a given commitment within a specified range
    using elliptic curve operations with fastecdsa.

    Parameters:
        amount (int): Transaction amount to be committed and proven.
        range_min (int): The minimum allowed value in the range.
        range_max (int): The maximum allowed value in the range.
        g (Point): Base point (generator) for the commitment. Defaults to secp256k1.G.
        h (Point): Secondary generator for the commitment. Defaults to a point on secp256k1.
        blinding_factor (int, optional): Blinding factor to use in the commitment.
        **kwargs: Additional backend-specific arguments.

    Returns:
        commitment (Point): The elliptic curve commitment to the transactions amount.
        proof (bytes): Simulated proof, represented as a SHA-256 hash.

    Raises:
        ImportError: If fastecdsa is not available.
        ValueError: If the amount is out of the specified range.
    """
    if not HAS_FASTECDSA:
        raise ImportError("fastecdsa library is required but not installed.")

    # Validate amount within the range
    if not (range_min <= amount <= range_max):
        raise ValueError("Amount is out of the specified range.")

    # Set default generators if not provided
    g = g or secp256k1.G
    h = h or secp256k1.G  # Here, ideally, a distinct point on the curve should be used for h

    # Generate a random blinding factor if not provided
    blinding_factor = blinding_factor or secrets.randbelow(secp256k1.q)

    # Create Pedersen Commitment: C = g^amount * h^blinding_factor
    commitment = (g * amount) + (h * blinding_factor)

    # Simulate proof generation by hashing commitment and range
    proof_data = f"{commitment.x}{commitment.y}{range_min}{range_max}".encode()
    proof = sha256(proof_data).digest()

    return commitment, proof


def verify_bulletproof(commitment, proof, range_min, range_max, g=None, h=None, **kwargs):
    """
    Verifies a simulated Bulletproof for a given commitment within a specified range.

    Parameters:
        commitment (Point): Elliptic curve commitment to the transactions amount.
        proof (bytes): The simulated Bulletproof proof to verify.
        range_min (int): The minimum allowed value in the range.
        range_max (int): The maximum allowed value in the range.
        g (Point): Base point (generator) for the commitment. Defaults to secp256k1.G.
        h (Point): Secondary generator for the commitment. Defaults to a point on secp256k1.
        **kwargs: Additional backend-specific arguments.

    Returns:
        bool: True if the simulated proof is valid; otherwise False.

    Raises:
        ImportError: If fastecdsa is not available.
    """
    if not HAS_FASTECDSA:
        raise ImportError("fastecdsa library is required but not installed.")

    # Set default generators if not provided
    g = g or secp256k1.G
    h = h or secp256k1.G

    # Recompute the proof based on the provided commitment and range
    proof_data = f"{commitment.x}{commitment.y}{range_min}{range_max}".encode()
    expected_proof = sha256(proof_data).digest()

    # Compare the computed proof with the provided proof
    return proof == expected_proof


