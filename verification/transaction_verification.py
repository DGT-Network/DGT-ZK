# transaction_verification.py
# ---------------------------------------------------------------------
# DGT-ZK Protocol: Transaction Verification and Compliance Module
#
# This module provides compliance and verification functions to ensure that
# transactions within the DGT-ZK Protocol adhere to regulatory and security
# standards. Functions include compliance checks (KYC/AML) and transaction
# verification routines such as validating amounts, checking range proofs,
# verifying digital signatures, and ensuring addresses are not blacklisted.
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

from transactions.transaction_utils import hash_data, validate_tx_structure
from verification.verification_constants import (
    COMPLIANCE_LEVEL_BASIC,
    COMPLIANCE_LEVEL_ADVANCED,
    ENABLE_BULLETPROOF_VALIDATION,
    MAX_TRANSACTION_AMOUNT,
    BLACKLIST_DB_PATH,
    WHITELIST_DB_PATH
)
from verification.bulletproofs import create_range_proof, validate_range_proof
from verification.psi_protocol import perform_psi_check


def compliance_check(tx, level=COMPLIANCE_LEVEL_BASIC):
    """
    Conducts compliance checks on the transaction based on KYC/AML standards.

    Parameters:
        tx (dict): The transaction data to verify.
        level (int): Compliance level (e.g., BASIC or ADVANCED).

    Returns:
        bool: True if the transaction passes compliance; False otherwise.
    """
    # Validate transaction structure
    if not validate_tx_structure(tx):
        return False

    # Basic compliance checks (e.g., amount limits)
    if level >= COMPLIANCE_LEVEL_BASIC:
        if not (0 < tx["amount"] <= MAX_TRANSACTION_AMOUNT):
            return False

    # Advanced compliance checks (e.g., whitelist/blacklist verification)
    if level >= COMPLIANCE_LEVEL_ADVANCED:
        if not (is_whitelisted(tx["recipient"]) and not is_blacklisted(tx["recipient"])):
            return False

        # Private Set Intersection for additional compliance if PSI is enabled
        if not perform_psi_check(tx["recipient"], BLACKLIST_DB_PATH, WHITELIST_DB_PATH):
            return False

    return True


def verify_amount_range(tx):
    """
    Verifies that the transaction amount falls within the allowed range using Bulletproofs.

    Parameters:
        tx (dict): The transaction data to verify.

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
    Verifies the transaction's digital signature.

    Parameters:
        tx (dict): The transaction data to verify.
        public_key (str): The public key of the sender for signature validation.

    Returns:
        bool: True if the signature is valid; False otherwise.
    """
    from encryption.signature import verify_signature as verify  # Import from the encryption package
    return verify(tx, public_key)


def is_blacklisted(address):
    """
    Checks if an address is blacklisted.

    Parameters:
        address (str): Address to check against the blacklist.

    Returns:
        bool: True if the address is blacklisted; False otherwise.
    """
    # Placeholder for blacklist database check
    blacklist = get_blacklist_addresses()
    return address in blacklist


def is_whitelisted(address):
    """
    Checks if an address is whitelisted.

    Parameters:
        address (str): Address to check against the whitelist.

    Returns:
        bool: True if the address is whitelisted; False otherwise.
    """
    # Placeholder for whitelist database check
    whitelist = get_whitelist_addresses()
    return address in whitelist


def get_blacklist_addresses():
    """
    Retrieves a list of blacklisted addresses (for compliance purposes).

    Returns:
        list: List of blacklisted addresses.
    """
    # For real implementations, query BLACKLIST_DB_PATH
    return ["0xBlacklistedAddress1", "0xBlacklistedAddress2"]


def get_whitelist_addresses():
    """
    Retrieves a list of whitelisted addresses (for compliance purposes).

    Returns:
        list: List of whitelisted addresses.
    """
    # For real implementations, query WHITELIST_DB_PATH
    return ["0xWhitelistedAddress1", "0xWhitelistedAddress2"]


# Example Usage
if __name__ == "__main__":
    # Sample transaction data
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

    # Perform advanced compliance check
    is_advanced_compliant = compliance_check(transaction, level=COMPLIANCE_LEVEL_ADVANCED)
    print("Compliance Check (Advanced):", is_advanced_compliant)

    # Verify the transaction's amount range
    is_in_range = verify_amount_range(transaction)
    print("Amount Range Verification:", is_in_range)

    # Verify the transaction's signature
    sender_public_key = "sender_public_key_example"
    is_signature_valid = verify_signature(transaction, sender_public_key)
    print("Signature Verification:", is_signature_valid)
