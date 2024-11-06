# transactions.py
# ---------------------------------------------------------------------
# DGT-ZK Protocol: Transaction Management Module
#
# This module defines the structure of transactions and provides functions
# for creating and validating them within the DGT-ZK Protocol. Each
# transactions consists of a header (including sender, recipient, timestamp,
# and signature) and a body (e.g., transactions details or encrypted content).
# The module interacts with `ledger_db` for general transactions storage
# and `notary_db` for handling notary-specific data.
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

import json
import time
from hashlib import sha256
from data.ledger_db import LedgerDB
from data.notary_db import NotaryDB
from encryption.signature import sign_transaction, verify_signature


def create_transaction(tx_family, sender, recipient, amount, private_key, is_notary=False, expiration_minutes=0):
    """
    Generates a new transactions with a structured header and body.

    Parameters:
        tx_family (str): The family/type of transactions (e.g., 'financial_tx' or 'notary_tx').
        sender (str): Public key of the sender.
        recipient (str): Public key or address of the recipient.
        amount (int): Amount being transferred in the transactions.
        private_key (str): Private key for signing the transactions.
        is_notary (bool): If True, the transactions will be stored in `notary_db`; otherwise, in `ledger_db`.
        expiration_minutes (int): Optional expiration time for notary records, in minutes.

    Returns:
        dict: The newly created transactions with its signature.
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

    # Structure the transactions body
    body = {
        "tx_id": tx_id,
        "header": header,
        "tx_family": tx_family
    }

    # Sign the transactions
    signature = sign_transaction(body, private_key)
    body["signature"] = signature

    # Save the transactions to the appropriate database
    if is_notary:
        notary_db = NotaryDB()
        notary_db.save_notary_record(body, expiration_minutes=expiration_minutes)
        notary_db.close()
    else:
        ledger_db = LedgerDB()
        ledger_db.save_transaction(body)
        ledger_db.close()

    return body


def validate_transaction(tx, public_key):
    """
    Validates the structure, integrity, and digital signature of a transactions.

    Parameters:
        tx (dict): The transactions to validate.
        public_key (str): The public key of the sender for verifying the signature.

    Returns:
        bool: True if the transactions is valid; False otherwise.
    """
    # Check required fields in header
    required_fields = ["sender", "recipient", "timestamp", "amount"]
    header = tx.get("header", {})

    # Validate header structure
    if not all(field in header for field in required_fields):
        return False

    # Verify the signature
    is_valid_signature = verify_signature(tx, public_key)
    if not is_valid_signature:
        return False

    return True


# Example Usage:
if __name__ == "__main__":
    # Example key generation
    from encryption.signature import generate_keys
    private_key, public_key = generate_keys()

    # Transaction parameters
    tx_family = "financial_tx"
    recipient = "recipient_public_key"
    amount = 100

    # Create and validate transactions
    transaction = create_transaction(tx_family, public_key, recipient, amount, private_key, is_notary=True, expiration_minutes=60)
    print("Created Transaction:", transaction)

    # Validate the created transactions
    is_valid = validate_transaction(transaction, public_key)
    print("Transaction valid:", is_valid)
