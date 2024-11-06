# encryption_utils.py
# ---------------------------------------------------------------------
# DGT-ZK Protocol: Encryption Utilities Module
#
# This module provides cryptographic helper functions for the DGT-ZK Protocol.
# It includes key cryptographic operations such as hashing and key exchange,
# with specific support for Schnorr-based PSI schemes and general cryptographic
# utilities.
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
import os
from ecdsa import SigningKey, VerifyingKey, SECP256k1
from ecdsa.util import randrange_from_seed__trytryagain

# Cryptographic Constants
DEFAULT_HASH_ALGORITHM = "sha256"
DEFAULT_CURVE = SECP256k1  # SECP256k1 curve for Schnorr and ECDSA operations

def hash_data(data, algorithm=DEFAULT_HASH_ALGORITHM):
    """
    Hashes data using the specified algorithm.

    Parameters:
        data (str or bytes): Data to hash.
        algorithm (str): Hashing algorithm to use (default: sha256).

    Returns:
        str: Hexadecimal string of the hashed data.
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    hash_func = getattr(hashlib, algorithm)
    return hash_func(data).hexdigest()

def generate_schnorr_keypair():
    """
    Generates a Schnorr keypair based on the SECP256k1 curve.

    Returns:
        tuple: (private_key, public_key) as hex-encoded strings.
    """
    private_key = SigningKey.generate(curve=DEFAULT_CURVE)
    public_key = private_key.get_verifying_key()
    return private_key.to_string().hex(), public_key.to_string().hex()

def schnorr_sign(message, private_key_hex):
    """
    Creates a Schnorr signature for a message.

    Parameters:
        message (str): The message to sign.
        private_key_hex (str): The hex-encoded private key.

    Returns:
        tuple: (r, s) representing the signature components.
    """
    private_key = SigningKey.from_string(bytes.fromhex(private_key_hex), curve=DEFAULT_CURVE)
    k = randrange_from_seed__trytryagain(os.urandom(32), DEFAULT_CURVE.order)
    r = (DEFAULT_CURVE.generator * k).x()
    e = int(hash_data(r.to_bytes(32, 'big') + message.encode()), 16)
    s = (k + e * int.from_bytes(private_key.to_string(), 'big')) % DEFAULT_CURVE.order
    return r, s

def schnorr_verify(message, r, s, public_key_hex):
    """
    Verifies a Schnorr signature.

    Parameters:
        message (str): The message that was signed.
        r (int): The r component of the signature.
        s (int): The s component of the signature.
        public_key_hex (str): The hex-encoded public key.

    Returns:
        bool: True if the signature is valid; False otherwise.
    """
    public_key = VerifyingKey.from_string(bytes.fromhex(public_key_hex), curve=DEFAULT_CURVE)
    e = int(hash_data(r.to_bytes(32, 'big') + message.encode()), 16)
    sG = DEFAULT_CURVE.generator * s
    eP = public_key.pubkey.point * e
    return (sG - eP).x() == r

# ---------------------------------------------------------------------
# Function Descriptions and Usage Examples
# ---------------------------------------------------------------------

# Example 1: Hashing Data
# data = "example_data"
# hashed_data = hash_data(data)
# print("Hashed Data:", hashed_data)

# Example 2: Generating Schnorr Keypair
# private_key, public_key = generate_schnorr_keypair()
# print("Schnorr Private Key:", private_key)
# print("Schnorr Public Key:", public_key)

# Example 3: Signing a Message with Schnorr Signature
# message = "message_to_sign"
# r, s = schnorr_sign(message, private_key)
# print("Schnorr Signature - r:", r)
# print("Schnorr Signature - s:", s)

# Example 4: Verifying a Schnorr Signature
# is_valid = schnorr_verify(message, r, s, public_key)
# print("Signature Valid:", is_valid)

# ---------------------------------------------------------------------
# This module provides cryptographic functions for hashing and key
# management, particularly for Schnorr-based signatures. Functions
# like `schnorr_sign` and `schnorr_verify` allow the use of Schnorr
# signature schemes, essential for privacy-preserving interactions
# in Private Set Intersection (PSI) and compliance verifications.
