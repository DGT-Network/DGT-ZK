# transaction_verification.py
# ---------------------------------------------------------------------
# DGT-ZK Protocol: Transaction Verification and Compliance Module
#
# This module provides compliance and verification functions to ensure that
# transactions within the DGT-ZK Protocol adhere to regulatory and security
# standards. Functions include compliance checks (KYC/AML) and transactions
# verification routines such as validating amounts, checking range proofs,
# and ensuring addresses are not blacklisted.
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

from .transaction_utils import hash_data, validate_tx_structure
from .transaction_constants import (
    COMPLIANCE_LEVEL_BASIC,
    COMPLIANCE_LEVEL_ADVANCED,
    ENABLE_BULLETPROOF_VALIDATION,
    MAX_TRANSACTION_AMOUNT
)
from verification.bulletproofs import create_range_proof, validate_range_proof


def compliance_check(tx, level=COMPLIANCE_LEVEL_BASIC):
    """
    Conducts compliance checks on the transactions based on KYC/AML standards.

    Parameters:
        tx (dict): The transactions data to verify.
        level (int): Compliance level (e.g., BASIC or ADVANCED).

    Returns:
        bool: True if the transactions passes compliance; False otherwise.
    """
    # Check if transactions structure is valid
    if not validate_tx_structure(tx):
        return False

    # Basic compliance level checks
    if level >= COMPLIANCE_LEVEL_BASIC:
        if tx["amount"] <= 0 or tx["amount"] > MAX_TRANSACTION_AMOUNT:
            return False

    # Advanced compliance level checks (e.g., blacklist verification)
    if level >= COMPLIANCE_LEVEL_ADVANCED:
        # Additional checks can be implemented here, such as blacklist verification
        if tx.get("recipient") in get_blacklist_addresses():
            return False

    return True


def verify_amount_range(tx):
    """
    Verifies that the transactions amount falls within the allowed range using Bulletproofs.

    Parameters:
        tx (dict): The transactions data to verify.

    Returns:
        bool: True if the amount is within the valid range; False otherwise.
    """
    if not ENABLE_BULLETPROOF_VALIDATION:
        return True  # Skip validation if Bulletproofs are disabled

    amount = tx["amount"]
    commitment, proof = create_range_proof(amount, min_value=0, max_value=MAX_TRANSACTION_AMOUNT)
    return validate_range_proof(commitment, proof, min_value=0, max_value=MAX_TRANSACTION_AMOUNT)


def verify_signature(tx, public_key):
    """
    Verifies that the transactions's digital signature is valid.

    Parameters:
        tx (dict): The transactions data to verify.
        public_key (str): The public key of the sender for signature validation.

    Returns:
        bool: True if the signature is valid; False otherwise.
    """
    from encryption.signature import verify_signature as verify  # Import from the encryption package
    return verify(tx, public_key)


def get_blacklist_addresses():
    """
    Retrieves a list of blacklisted addresses (for compliance purposes).

    Returns:
        list: List of blacklisted addresses.
    """
    # In a real implementation, this would query a database or external API.
    # For testing purposes, we'll use a hardcoded list.
    return ["0xBlacklistedAddress1", "0xBlacklistedAddress2"]


# Example Usage
if __name__ == "__main__":
    # Sample transactions data
    transaction = {
        "sender": "sender_public_key",
        "recipient": "recipient_public_key",
        "timestamp": "2024-01-01T10:00:00Z",
        "amount": 1000,
        "signature": "sample_signature"
    }

    # Perform compliance check at basic level
    is_compliant = compliance_check(transaction, level=COMPLIANCE_LEVEL_BASIC)
    print("Compliance Check (Basic):", is_compliant)

    # Verify the transactions amount range
    is_in_range = verify_amount_range(transaction)
    print("Amount Range Verification:", is_in_range)

    # Verify the transactions signature
    sender_public_key = "sender_public_key_example"
    is_signature_valid = verify_signature(transaction, sender_public_key)
    print("Signature Verification:", is_signature_valid)
