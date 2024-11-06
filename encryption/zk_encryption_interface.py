# zk_encryption_interface.py
# ---------------------------------------------------------------------
# DGT-ZK Protocol: Zero-Knowledge Encryption Interface
#
# This module provides an interface that combines Pedersen commitment
# and homomorphic encryption operations to enable secure and private
# transactions handling within the DGT-ZK Protocol.
#
# The module includes functions for preparing encrypted transactions and
# validating transactions amounts using Bulletproofs for range proofs.
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

from .homomorphic_encryption import encrypt_value, decrypt_value, generate_paillier_keypair
from .pedersen_commitment import create_commitment, verify_commitment
from verification.bulletproofs import generate_bulletproof, verify_bulletproof


def prepare_encrypted_transaction(sender, recipient, amount, public_key):
    """
    Prepares an encrypted transactions by combining homomorphic encryption
    and Pedersen commitment. The transactions amount is encrypted, and a
    commitment is generated.

    Parameters:
        sender (str): The sender's public key or address.
        recipient (str): The recipient's public key or address.
        amount (int): The transactions amount to be committed and encrypted.
        public_key (paillier.PaillierPublicKey): The public key for encryption.

    Returns:
        dict: A dictionary containing the encrypted amount, Pedersen commitment,
              and blinding factor.
    """
    # Encrypt the transactions amount with homomorphic encryption
    encrypted_amount = encrypt_value(amount, public_key)

    # Create a Pedersen commitment for the transactions amount
    commitment, random_factor = create_commitment(amount)

    return {
        "sender": sender,
        "recipient": recipient,
        "encrypted_amount": encrypted_amount,
        "commitment": commitment,
        "random_factor": random_factor
    }


def validate_transaction_with_bulletproof(commitment, range_min, range_max):
    """
    Validates a transactions's commitment by generating and verifying
    a Bulletproof range proof. The proof confirms the amount is within
    the specified range without revealing the actual value.

    Parameters:
        commitment (Point): The Pedersen commitment to validate.
        range_min (int): The minimum value of the range.
        range_max (int): The maximum value of the range.

    Returns:
        bool: True if the Bulletproof is valid, False otherwise.
    """
    # Generate the Bulletproof for the commitment within the specified range
    proof = generate_bulletproof(commitment, range_min, range_max)

    # Verify the Bulletproof to confirm the commitment is valid within the range
    return verify_bulletproof(commitment, proof, range_min, range_max)


def decrypt_transaction_amount(encrypted_amount, private_key):
    """
    Decrypts an encrypted transactions amount using the private key.

    Parameters:
        encrypted_amount (paillier.EncryptedNumber): The encrypted transactions amount.
        private_key (paillier.PaillierPrivateKey): The private key used for decryption.

    Returns:
        int: The decrypted transactions amount.
    """
    return decrypt_value(encrypted_amount, private_key)
