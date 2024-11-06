# ffi_dalek.py
# ---------------------------------------------------------------------
# DGT-ZK Protocol: Dalek Bulletproofs FFI Module
#
# This module provides functions to generate and verify Bulletproofs
# using the dalek-bulletproofs Rust library via Foreign Function Interface (FFI).
# It integrates with the bulletproofs_core and range_proof modules, ensuring
# seamless usage across the DGT-ZK Protocol.
#
# Note: Ensure the dalek-bulletproofs library is compiled and accessible
# as a shared library for this FFI module to function correctly.
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
# For more details, see <https://www.gnu.org/licenses/>.
# ---------------------------------------------------------------------

from cffi import FFI
import os

ffi = FFI()

# Define the path to the compiled dalek-bulletproofs shared library
library_path = "path/to/dalek_bulletproofs_library.dll"  # Update the path as needed
dalek = ffi.dlopen(library_path)

# Define the C function signatures that will be used in FFI
ffi.cdef("""
    unsigned char* create_bulletproof(uint64_t commitment, uint64_t range_min, uint64_t range_max);
    bool verify_bulletproof(uint64_t commitment, unsigned char* proof, uint64_t range_min, uint64_t range_max);
""")


def generate_bulletproof(commitment, range_min, range_max, **kwargs):
    """
    Generates a Bulletproof for the given commitment within a specified range
    using the dalek-bulletproofs library via FFI.

    Parameters:
        commitment (int): The Pedersen Commitment representing the transactions amount.
        range_min (int): The minimum allowed value in the range.
        range_max (int): The maximum allowed value in the range.
        **kwargs: Additional arguments (not used here, but provided for consistency).

    Returns:
        proof (bytes): The generated Bulletproof proof.

    Raises:
        RuntimeError: If the FFI call to the library fails.
    """
    try:
        # Call the dalek library to generate the Bulletproof
        proof_pointer = dalek.create_bulletproof(commitment, range_min, range_max)
        # Convert the proof pointer to bytes (assuming the proof is a byte array)
        proof = ffi.string(proof_pointer)
    except Exception as e:
        raise RuntimeError(f"Error generating Bulletproof via FFI: {e}")

    return proof


def verify_bulletproof(commitment, proof, range_min, range_max, **kwargs):
    """
    Verifies a Bulletproof within a specified range using the dalek-bulletproofs
    library via FFI.

    Parameters:
        commitment (int): The Pedersen Commitment representing the transactions amount.
        proof (bytes): The Bulletproof proof to verify.
        range_min (int): The minimum allowed value in the range.
        range_max (int): The maximum allowed value in the range.
        **kwargs: Additional arguments (not used here, but provided for consistency).

    Returns:
        bool: True if the proof is valid; otherwise False.

    Raises:
        RuntimeError: If the FFI call to the library fails.
    """
    try:
        # Convert the proof to a C-compatible pointer
        proof_c = ffi.new("unsigned char[]", proof)
        # Call the dalek library to verify the Bulletproof
        is_valid = dalek.verify_bulletproof(commitment, proof_c, range_min, range_max)
    except Exception as e:
        raise RuntimeError(f"Error verifying Bulletproof via FFI: {e}")

    return is_valid

#///////////////////////////////////////////////
# Explanation of Key Components
# 1) FFI Setup:
#  - library_path: Specifies the path to the compiled dalek-bulletproofs shared library. Update this path based on your setup.
#  - ffi.dlopen(library_path): Loads the shared library, making its functions accessible to Python.
#
# 2) Function Signatures (ffi.cdef):
#  - Defines the expected C function signatures for the functions exposed by dalek-bulletproofs.
#  - In this case, create_bulletproof generates a proof for a given commitment and range, and verify_bulletproof verifies a proof.
#
# 3) generate_bulletproof Function:
#  - Calls the create_bulletproof function from the dalek-bulletproofs library.
#  - Parameters: commitment, range_min, and range_max, with additional unused kwargs for consistency across implementations.
#  - Returns: proof in bytes, converted from the C pointer returned by dalek.create_bulletproof.
#  - Error Handling: If the FFI call fails, an exception is raised with an informative message.
#
# 4) verify_bulletproof Function:
#  - Calls the verify_bulletproof function from the dalek-bulletproofs library.
#  - Parameters: commitment, proof, range_min, and range_max, with proof being converted to a C-compatible pointer for the FFI call.
#  - Returns: True if the proof is valid; False otherwise.
#  - Error Handling: If the FFI call fails, an exception is raised with an informative message.
#
# USAGE:
# | from verification.bulletproofs.range_proof import create_range_proof, validate_range_proof
# |
# |# Example parameters
# |amount = 1000
# |range_min = 0
# |range_max = 5000
# |
# |# Generate and verify a range proof
# |commitment, proof = create_range_proof(amount, range_min=range_min, range_max=range_max)
# |is_valid = validate_range_proof(commitment, proof, range_min=range_min, range_max=range_max)
# |
# |print(f"Generated Proof: {proof}")
# |print(f"Proof Valid: {is_valid}")
