# signature.py
# ---------------------------------------------------------------------
# DGT-ZK Protocol: Signature and Address Management Module
#
# This module manages ECDSA digital signatures compatible with Ethereum
# address standards. It provides functions for key generation, signing
# transactions, verifying signatures, generating Ethereum-compatible
# addresses, and creating secure secondary addresses for enhanced privacy.
# The `ecdsa` library is used for ECDSA signing and verification, while
# `eth_keys` and `eth_utils` are used to format Ethereum-compatible addresses.
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

from ecdsa import SigningKey, VerifyingKey, SECP256k1, BadSignatureError
from eth_keys import keys
from eth_utils import keccak
import secrets

def generate_keys():
    """
    Generates a public and private key pair using ECDSA (SECP256k1 curve).

    Returns:
        tuple: (private_key, public_key) as hex-encoded strings.
    """
    private_key_obj = SigningKey.generate(curve=SECP256k1)
    public_key_obj = private_key_obj.get_verifying_key()
    private_key = private_key_obj.to_string().hex()
    public_key = public_key_obj.to_string().hex()
    return private_key, public_key

def sign_transaction(tx, private_key):
    """
    Signs a transactions using the provided private key.

    Parameters:
        tx (dict): The transactions data to sign.
        private_key (str): Hex-encoded private key.

    Returns:
        str: Hex-encoded digital signature.
    """
    private_key_obj = SigningKey.from_string(bytes.fromhex(private_key), curve=SECP256k1)
    message = keccak(text=str(tx)).digest()
    signature = private_key_obj.sign(message).hex()
    return signature

def verify_signature(tx, public_key, signature):
    """
    Verifies the transactions's digital signature using the provided public key.

    Parameters:
        tx (dict): The transactions data to verify.
        public_key (str): Hex-encoded public key.
        signature (str): Hex-encoded digital signature to verify.

    Returns:
        bool: True if the signature is valid; False otherwise.
    """
    public_key_obj = VerifyingKey.from_string(bytes.fromhex(public_key), curve=SECP256k1)
    message = keccak(text=str(tx)).digest()
    try:
        return public_key_obj.verify(bytes.fromhex(signature), message)
    except BadSignatureError:
        return False

def get_eth_address(public_key):
    """
    Converts a public key to an Ethereum-compatible address format.

    Parameters:
        public_key (str): Hex-encoded public key.

    Returns:
        str: Ethereum-compatible address as a hex string.
    """
    public_key_bytes = bytes.fromhex(public_key)
    eth_address = keccak(public_key_bytes).hex()[-40:]
    return f"0x{eth_address}"

def create_secondary_address(g, h):
    """
    Creates a secondary protected address using Pedersen-style commitments.

    Parameters:
        g (Point): The generator point G on the elliptic curve.
        h (Point): The generator point H on the elliptic curve.

    Returns:
        tuple: (secondary_address, secret_s, secret_r) where:
               - secondary_address (Point) is the created address.
               - secret_s and secret_r (int) are random secrets used in the commitment.
    """
    # Generate random secrets
    secret_s = secrets.randbelow(SECP256k1.order)
    secret_r = secrets.randbelow(SECP256k1.order)

    # Compute the secondary address as a commitment: Addr_secondary = g^s * h^r
    secondary_address = (g * secret_s) + (h * secret_r)

    return secondary_address, secret_s, secret_r
