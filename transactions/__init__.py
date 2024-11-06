# __init__.py
# ---------------------------------------------------------------------
# DGT-ZK Protocol: Transactions Package Initialization
#
# This file initializes the transactions package, importing essential
# classes and functions for managing and processing transactions within
# the DGT-ZK Protocol. The package integrates functions for transactions
# creation, validation, anchoring, and utility functions, creating a
# comprehensive interface for transactions flow operations.
#
# The package includes the main transactions flow manager, constants,
# utilities, verification, and anchoring logic.
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

# Import key components from modules in the package
from .transaction_flow import TransactionFlow
from .transaction_constants import TX_FAMILY_FINANCIAL, TX_FAMILY_NOTARY

__all__ = [
    "TransactionFlow",
    "TX_FAMILY_FINANCIAL",
    "TX_FAMILY_NOTARY",
    "CANCELLATION_WINDOW",
    "generate_transaction_id",
    "format_transaction_data",
    "verify_kyc_compliance",
    "validate_transaction_structure",
    "anchor_transaction"
]

# This package provides a comprehensive suite of functions and classes
# for managing transactions flows within the DGT-ZK Protocol, including
# functionalities for creating, verifying, anchoring, and managing
# transactions data.
