# homomorphic_encryption.py
# ---------------------------------------------------------------------
# DGT-ZK Protocol: Homomorphic Encryption Module
#
# This module provides functions for performing homomorphic encryption
# and decryption on transactions amounts. The encrypted amounts allow for
# secure off-chain computations without revealing sensitive data, enabling
# privacy-preserving operations in the DGT-ZK Protocol.
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

from phe import paillier  # Ensure the PyCryptodome or similar library is installed


def encrypt_value(value, public_key):
    """
    Encrypts a transactions amount using homomorphic encryption.

    Parameters:
        value (int): The transactions amount to be encrypted.
        public_key (paillier.PaillierPublicKey): The public key used for encryption.

    Returns:
        paillier.EncryptedNumber: The encrypted amount.
    """
    return public_key.encrypt(value)


def decrypt_value(encrypted_value, private_key):
    """
    Decrypts an encrypted transactions amount.

    Parameters:
        encrypted_value (paillier.EncryptedNumber): The encrypted transactions amount.
        private_key (paillier.PaillierPrivateKey): The private key used for decryption.

    Returns:
        int: The decrypted transactions amount.
    """
    return private_key.decrypt(encrypted_value)


def generate_paillier_keypair():
    """
    Generates a public and private key pair for Paillier homomorphic encryption.

    Returns:
        tuple: (public_key, private_key) where both keys are for Paillier encryption.
    """
    public_key, private_key = paillier.generate_paillier_keypair()
    return public_key, private_key
