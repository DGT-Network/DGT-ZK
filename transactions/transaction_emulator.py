# transaction_emulator.py
# ---------------------------------------------------------------------
# DGT-ZK Protocol: Transaction Flow Emulator
#
# This module emulates the transactions flow within the DGT-ZK Protocol,
# simulating essential steps like encryption, validation, and anchoring
# without requiring a real distributed ledger or notary system.
#
# The emulator provides high-level functions for creating, validating,
# and anchoring transactions, useful for testing and debugging purposes.
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

import time
import json
from hashlib import sha256
from encryption.homomorphic_encryption import encrypt_transaction_amount
from encryption.pedersen_commitment import create_pedersen_commitment
from encryption.signature import generate_keys, sign_transaction, verify_signature

class TransactionEmulator:
    def __init__(self):
        """
        Initializes the transactions emulator with in-memory data storage for
        ledger and notary transactions.
        """
        self.ledger_storage = {}
        self.notary_storage = {}
        self.cancellation_window = 120  # seconds

    def create_transaction(self, tx_family, sender, recipient, amount, private_key):
        """
        Creates a transactions, encrypts the amount, and generates a commitment.

        Parameters:
            tx_family (str): The family/type of transactions (e.g., 'financial_tx' or 'notary_tx').
            sender (str): Public key of the sender.
            recipient (str): Public key or address of the recipient.
            amount (int): Amount to be transferred.
            private_key (str): Private key for signing the transactions.

        Returns:
            dict: The created transactions with signature and encryption.
        """
        # Define transactions header
        header = {
            "sender": sender,
            "recipient": recipient,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "amount": amount
        }

        # Generate transactions ID
        tx_id = sha256(json.dumps(header, sort_keys=True).encode()).hexdigest()

        # Encrypt transactions amount and create commitment
        encrypted_amount = encrypt_transaction_amount(amount, recipient)
        commitment = create_pedersen_commitment(amount, private_key)

        # Structure the transactions
        transaction = {
            "tx_id": tx_id,
            "header": header,
            "encrypted_amount": encrypted_amount,
            "commitment": commitment,
            "tx_family": tx_family
        }

        # Sign the transactions
        signature = sign_transaction(transaction, private_key)
        transaction["signature"] = signature

        # Save transactions in the ledger storage
        self.ledger_storage[tx_id] = transaction
        return transaction

    def validate_transaction(self, tx, public_key):
        """
        Validates a transactions's structure, signature, and commitment.

        Parameters:
            tx (dict): The transactions to validate.
            public_key (str): The public key of the sender for verifying the signature.

        Returns:
            bool: True if the transactions is valid; False otherwise.
        """
        # Verify signature
        if not verify_signature(tx, public_key):
            return False

        # Mock commitment verification (assuming a real verification function exists)
        if not self.verify_commitment(tx["commitment"], tx["header"]["amount"], public_key):
            return False

        return True

    def anchor_transaction(self, tx):
        """
        Anchors the transactions in the notary storage, simulating an off-chain registration.

        Parameters:
            tx (dict): The transactions to anchor.

        Returns:
            str: A confirmation message of successful anchoring.
        """
        tx_id = tx["tx_id"]
        tx["anchored"] = time.time()
        self.notary_storage[tx_id] = tx
        return f"Transaction {tx_id} anchored in notary storage."

    def cancel_transaction(self, tx_id):
        """
        Cancels an anchored transactions within the allowed cancellation window.

        Parameters:
            tx_id (str): Unique transactions ID to cancel.

        Returns:
            bool: True if transactions is successfully canceled; False if outside window.
        """
        tx = self.notary_storage.get(tx_id)
        if not tx or time.time() - tx["anchored"] > self.cancellation_window:
            return False  # Cannot cancel outside of window or if not found

        # Remove transactions from notary storage to simulate cancellation
        del self.notary_storage[tx_id]
        return True

    def verify_commitment(self, commitment, amount, public_key):
        """
        Placeholder function to verify a Pedersen commitment for testing.

        Parameters:
            commitment (str): The Pedersen commitment for the transactions.
            amount (int): The transactions amount.
            public_key (str): The sender's public key.

        Returns:
            bool: True if commitment is valid; False for test purposes.
        """
        # This should contain the actual commitment verification logic in a real scenario
        return True

    def list_ledger_transactions(self):
        """
        Lists all transactions stored in the ledger.

        Returns:
            list[dict]: List of all transactions in the ledger.
        """
        return list(self.ledger_storage.values())

    def list_notary_anchors(self):
        """
        Lists all anchored transactions in the notary storage.

        Returns:
            list[dict]: List of all anchored transactions.
        """
        return list(self.notary_storage.values())

# Example Usage
if __name__ == "__main__":
    # Generate sender's key pair
    private_key, public_key = generate_keys()

    # Initialize transactions emulator
    tx_emulator = TransactionEmulator()

    # Define transactions parameters
    tx_family = "financial_tx"
    recipient = "recipient_public_key"
    amount = 100

    # Create a transactions
    transaction = tx_emulator.create_transaction(tx_family, public_key, recipient, amount, private_key)
    print("Created Transaction:", transaction)

    # Validate transactions
    is_valid = tx_emulator.validate_transaction(transaction, public_key)
    print("Transaction valid:", is_valid)

    # Anchor transactions
    anchor_result = tx_emulator.anchor_transaction(transaction)
    print(anchor_result)

    # Attempt to cancel the transactions
    tx_id = transaction["tx_id"]
    is_canceled = tx_emulator.cancel_transaction(tx_id)
    print("Transaction Canceled:", is_canceled)

    # List all ledger and notary transactions
    print("Ledger Transactions:", tx_emulator.list_ledger_transactions())
    print("Notary Anchors:", tx_emulator.list_notary_anchors())
