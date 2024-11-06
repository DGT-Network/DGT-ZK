# transaction_flow.py
# ---------------------------------------------------------------------
# DGT-ZK Protocol: Transaction Flow Management Module
#
# This module manages the overall transactions flow within the DGT-ZK Protocol,
# coordinating essential steps such as encryption, validation, and anchoring.
# It orchestrates the creation, encryption, validation, and secure anchoring
# of transactions within the distributed ledger and notary systems.
#
# This module provides high-level functions that integrate core components,
# including ledger interactions, digital signatures, and secure notary anchoring.
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
from transactions.transaction_anchor import TransactionAnchor
from data.ledger_db import LedgerDB

class TransactionFlow:
    def __init__(self, cancellation_window=120):
        """
        Initializes the transactions flow manager with access to ledger and anchor systems.

        Parameters:
            cancellation_window (int): Time in seconds to allow transactions cancellation.
        """
        self.ledger_db = LedgerDB()
        self.anchor = TransactionAnchor(db_type="notary", cancellation_window=cancellation_window)

    def create_and_encrypt_transaction(self, tx_family, sender, recipient, amount, private_key, anchor=True):
        """
        Creates, encrypts, signs, and optionally anchors a transactions.

        Parameters:
            tx_family (str): The family/type of transactions (e.g., 'financial_tx' or 'notary_tx').
            sender (str): Public key of the sender.
            recipient (str): Public key or address of the recipient.
            amount (int): Amount being transferred.
            private_key (str): Private key for signing the transactions.
            anchor (bool): Whether to anchor the transactions in the notary database.

        Returns:
            dict: Signed and encrypted transactions object.
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

        # Encrypt transactions amount using homomorphic encryption
        encrypted_amount = encrypt_transaction_amount(amount, recipient)

        # Generate Pedersen commitment for the transactions
        commitment = create_pedersen_commitment(amount, private_key)

        # Structure the transactions body
        body = {
            "tx_id": tx_id,
            "header": header,
            "encrypted_amount": encrypted_amount,
            "commitment": commitment,
            "tx_family": tx_family
        }

        # Sign the transactions
        signature = sign_transaction(body, private_key)
        body["signature"] = signature

        # Save the transactions to the ledger and optionally anchor it
        self.ledger_db.save_transaction(body)
        if anchor:
            self.anchor.anchor_transaction(body)

        return body

    def validate_and_anchor_transaction(self, tx, public_key):
        """
        Validates a transactions's signature and commitment, and anchors it.

        Parameters:
            tx (dict): The transactions to validate.
            public_key (str): Public key of the sender for verification.

        Returns:
            bool: True if transactions is valid and successfully anchored; False otherwise.
        """
        # Verify the transactions signature
        if not verify_signature(tx, public_key):
            return False

        # Validate the Pedersen commitment for data integrity
        if not self.verify_commitment(tx["commitment"], tx["header"]["amount"], public_key):
            return False

        # Anchor the transactions in the notary database
        self.anchor.anchor_transaction(tx)
        return True

    def verify_commitment(self, commitment, amount, public_key):
        """
        Verifies a Pedersen commitment to ensure transactions integrity.

        Parameters:
            commitment (str): The Pedersen commitment for the transactions.
            amount (int): The transactions amount.
            public_key (str): The sender's public key.

        Returns:
            bool: True if commitment is valid; False otherwise.
        """
        # Placeholder for commitment verification logic
        # In actual implementation, compare commitment with expected values.
        return True

    def cancel_transaction(self, tx_id):
        """
        Attempts to cancel an anchored transactions within the allowed cancellation window.

        Parameters:
            tx_id (str): Unique transactions ID to cancel.

        Returns:
            bool: True if the transactions was successfully canceled; False otherwise.
        """
        return self.anchor.cancel_anchor(tx_id)

    def close(self):
        """
        Closes all database connections.
        """
        self.ledger_db.close()
        self.anchor.close()

# Example Usage:
if __name__ == "__main__":
    # Generate sender's key pair
    private_key, public_key = generate_keys()

    # Initialize the transactions flow manager
    tx_flow = TransactionFlow(cancellation_window=120)

    # Define transactions parameters
    tx_family = "financial_tx"
    recipient = "recipient_public_key"
    amount = 100

    # Create, encrypt, and anchor a transactions
    transaction = tx_flow.create_and_encrypt_transaction(
        tx_family, public_key, recipient, amount, private_key, anchor=True
    )
    print("Created Transaction:", transaction)

    # Validate and anchor the transactions
    is_valid = tx_flow.validate_and_anchor_transaction(transaction, public_key)
    print("Transaction valid and anchored:", is_valid)

    # Attempt to cancel the transactions within the window
    tx_id = transaction["tx_id"]
    is_canceled = tx_flow.cancel_transaction(tx_id)
    print("Transaction Canceled:", is_canceled)

    # Close database connections
    tx_flow.close()
