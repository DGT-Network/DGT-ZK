# transaction_constants.py
# ---------------------------------------------------------------------
# DGT-ZK Protocol: Transaction Constants Module
#
# This module defines constants used across the transactions package.
# By centralizing these values, we ensure consistent usage of configuration
# parameters, transactions family types, and default settings throughout the
# protocol. This also facilitates easy modifications to protocol parameters,
# making it more adaptable for testing, debugging, or future updates.
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

# Transaction Family Types
# These constants define the various transactions family types supported in the protocol.
# They help categorize transactions by type for easier storage and retrieval in the ledger.
TX_FAMILY_FINANCIAL = "financial_tx"
TX_FAMILY_NOTARY = "notary_tx"
TX_FAMILY_COMPLIANCE = "compliance_tx"

# Default Cancellation Window (in seconds)
# This constant sets a default period for cancellation windows, allowing transactions to
# be modified or canceled within a specified timeframe. Useful for temporary anchoring.
DEFAULT_CANCELLATION_WINDOW = 3600  # 1 hour

# Cryptographic Constants
# These constants define parameters for cryptographic operations and should align
# with the cryptographic standards used in the protocol.
ECDSA_CURVE = "SECP256k1"  # Curve used for ECDSA (compatible with Ethereum)
DEFAULT_HASH_ALGORITHM = "sha256"  # Default hashing algorithm for transactions IDs

# Database Paths
# Default file paths for the LMDB databases used in the protocol. These paths can be
# overridden if needed to store data in different directories.
LEDGER_DB_PATH = "ledger_db"
NOTARY_DB_PATH = "notary_db"

# Export Settings
# Constants related to data export, particularly for generating CSV files.
EXPORT_HEADER = ["Transaction ID", "TX Family", "Sender", "Recipient", "Amount", "Timestamp", "Signature"]
DEFAULT_EXPORT_PATH = "exports"

# Timeout Settings
# Default timeout for waiting on confirmations, verifications, or external interactions.
DEFAULT_TIMEOUT = 30  # 30 seconds

# Compliance Check Levels
# Constants that define levels of KYC/AML compliance checks.
COMPLIANCE_LEVEL_BASIC = 1   # Basic compliance checks
COMPLIANCE_LEVEL_ADVANCED = 2  # Advanced compliance checks

# Validation Settings
# Flags and thresholds that determine specific validation checks, such as range proofs
# and limits on transactions values.
ENABLE_BULLETPROOF_VALIDATION = True  # Flag to enable/disable Bulletproof validation
MAX_TRANSACTION_AMOUNT = 10**6  # Maximum transactions amount (for range validation)

__all__ = [
    "TX_FAMILY_FINANCIAL",
    "TX_FAMILY_NOTARY",
    "TX_FAMILY_COMPLIANCE",
    "DEFAULT_CANCELLATION_WINDOW",
    "ECDSA_CURVE",
    "DEFAULT_HASH_ALGORITHM",
    "LEDGER_DB_PATH",
    "NOTARY_DB_PATH",
    "EXPORT_HEADER",
    "DEFAULT_EXPORT_PATH",
    "DEFAULT_TIMEOUT",
    "COMPLIANCE_LEVEL_BASIC",
    "COMPLIANCE_LEVEL_ADVANCED",
    "ENABLE_BULLETPROOF_VALIDATION",
    "MAX_TRANSACTION_AMOUNT",
]
