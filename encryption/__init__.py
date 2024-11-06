# __init__.py
# ---------------------------------------------------------------------
# DGT-ZK Protocol: Encryption Package Initialization
#
# This module initializes the encryption package, importing essential
# functions from homomorphic encryption and Pedersen commitment modules.
# It also imports the zk_encryption_interface for combined cryptographic
# operations. These functions facilitate secure transactions handling and
# commitment-based verifications for the DGT-ZK Protocol.
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

from .homomorphic_encryption import encrypt_value, decrypt_value
from .pedersen_commitment import create_commitment, verify_commitment
from .zk_encryption_interface import prepare_encrypted_transaction, validate_transaction_with_bulletproof

__all__ = [
    "encrypt_value",
    "decrypt_value",
    "create_commitment",
    "verify_commitment",
    "prepare_encrypted_transaction",
    "validate_transaction_with_bulletproof"
]
