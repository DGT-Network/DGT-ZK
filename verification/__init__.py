# __init__.py
# ---------------------------------------------------------------------
# DGT-ZK Protocol: Verification Package Initialization
#
# This package provides verification and compliance modules for the
# DGT-ZK Protocol, ensuring that transactions meet regulatory and
# security standards. It includes functionality for bulletproof range proofs,
# compliance checks (KYC/AML), Private Set Intersection (PSI) for
# whitelist/blacklist matching, and transaction verification.
#
# Modules Included:
# - bulletproofs: Provides Bulletproof range proof generation and validation.
# - verification_constants: Defines key constants used across modules.
# - encryption_utils: Supplies helper functions for encryption and hashing.
# - psi_protocol: Implements the Private Set Intersection (PSI) protocols.
# - compliance_verification: Handles KYC/AML compliance checks.
# - transaction_verification: Manages transaction validation and ensures compliance.
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

from .verification_constants import (
    COMPLIANCE_LEVEL_BASIC,
    COMPLIANCE_LEVEL_ADVANCED,
    ENABLE_BULLETPROOF_VALIDATION,
    MAX_TRANSACTION_AMOUNT,
    BLACKLIST_DB_PATH,
    WHITELIST_DB_PATH
)

from .encryption_utils import hash_data, generate_shared_secret, schnorr_key_exchange
from .psi_protocol import perform_psi_check
from .compliance_verification import compliance_check, is_blacklisted, is_whitelisted
from .transaction_verification import verify_signature, verify_amount_range, get_blacklist_addresses, get_whitelist_addresses

# Import Bulletproofs subpackage functionality
from .bulletproofs import create_range_proof, validate_range_proof

__all__ = [
    # Constants
    "COMPLIANCE_LEVEL_BASIC",
    "COMPLIANCE_LEVEL_ADVANCED",
    "ENABLE_BULLETPROOF_VALIDATION",
    "MAX_TRANSACTION_AMOUNT",
    "BLACKLIST_DB_PATH",
    "WHITELIST_DB_PATH",

    # Utility Functions
    "hash_data",
    "generate_shared_secret",
    "schnorr_key_exchange",

    # PSI Functions
    "perform_psi_check",

    # Compliance Functions
    "compliance_check",
    "is_blacklisted",
    "is_whitelisted",

    # Transaction Verification Functions
    "verify_signature",
    "verify_amount_range",
    "get_blacklist_addresses",
    "get_whitelist_addresses",

    # Bulletproofs Functions
    "create_range_proof",
    "validate_range_proof"
]
