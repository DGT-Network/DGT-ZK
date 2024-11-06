# bulletproofs_core.py
# ---------------------------------------------------------------------
# DGT-ZK Protocol: Bulletproofs Core Module
#
# This module provides core functions for generating and verifying
# Bulletproofs. It routes calls to the appropriate implementation,
# including dalek-bulletproofs (Rust FFI), fastecdsa, or emulation.
#
# Note: Ensure that the appropriate backend is configured by setting
# the BULLETPROOF_IMPLEMENTATION flag in the main configuration.
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

from .emulation import generate_bulletproof as emu_generate_bulletproof
from .emulation import verify_bulletproof as emu_verify_bulletproof

try:
    from .ffi_dalek import generate_bulletproof as dalek_generate_bulletproof
    from .ffi_dalek import verify_bulletproof as dalek_verify_bulletproof

    HAS_DALEK = True
except ImportError:
    HAS_DALEK = False

try:
    from .fastecdsa_impl import generate_bulletproof as fastecdsa_generate_bulletproof
    from .fastecdsa_impl import verify_bulletproof as fastecdsa_verify_bulletproof

    HAS_FASTECDSA = True
except ImportError:
    HAS_FASTECDSA = False

# Configuration flag to determine which Bulletproof implementation to use
BULLETPROOF_IMPLEMENTATION = "emulation"  # Options: "dalek", "fastecdsa", "emulation"


def generate_bulletproof(commitment, range_min, range_max, **kwargs):
    """
    Generates a Bulletproof for a given commitment within a specified range,
    using the configured backend (dalek-bulletproofs, fastecdsa, or emulation).

    Parameters:
        commitment (int): The Pedersen Commitment representing the transactions amount.
        range_min (int): The minimum allowed value in the range.
        range_max (int): The maximum allowed value in the range.
        **kwargs: Additional arguments for backend-specific configurations.

    Returns:
        proof: The Bulletproof or mock proof for range verification.

    Raises:
        ValueError: If no valid implementation is configured.
    """
    if BULLETPROOF_IMPLEMENTATION == "dalek" and HAS_DALEK:
        return dalek_generate_bulletproof(commitment, range_min, range_max, **kwargs)
    elif BULLETPROOF_IMPLEMENTATION == "fastecdsa" and HAS_FASTECDSA:
        return fastecdsa_generate_bulletproof(commitment, range_min, range_max, **kwargs)
    elif BULLETPROOF_IMPLEMENTATION == "emulation":
        return emu_generate_bulletproof(commitment, range_min, range_max, **kwargs)
    else:
        raise ValueError("Invalid or unsupported Bulletproof implementation selected.")


def verify_bulletproof(commitment, proof, range_min, range_max, **kwargs):
    """
    Verifies a Bulletproof for a given commitment within a specified range,
    using the configured backend (dalek-bulletproofs, fastecdsa, or emulation).

    Parameters:
        commitment (int): The Pedersen Commitment representing the transactions amount.
        proof: The Bulletproof proof to verify.
        range_min (int): The minimum allowed value in the range.
        range_max (int): The maximum allowed value in the range.
        **kwargs: Additional arguments for backend-specific configurations.

    Returns:
        bool: True if the proof is valid and commitment is within the range; otherwise False.

    Raises:
        ValueError: If no valid implementation is configured.
    """
    if BULLETPROOF_IMPLEMENTATION == "dalek" and HAS_DALEK:
        return dalek_verify_bulletproof(commitment, proof, range_min, range_max, **kwargs)
    elif BULLETPROOF_IMPLEMENTATION == "fastecdsa" and HAS_FASTECDSA:
        return fastecdsa_verify_bulletproof(commitment, proof, range_min, range_max, **kwargs)
    elif BULLETPROOF_IMPLEMENTATION == "emulation":
        return emu_verify_bulletproof(commitment, proof, range_min, range_max, **kwargs)
    else:
        raise ValueError("Invalid or unsupported Bulletproof implementation selected.")
