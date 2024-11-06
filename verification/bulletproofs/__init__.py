# __init__.py
# ---------------------------------------------------------------------
# DGT-ZK Protocol: Bulletproofs Sub-package Initialization
#
# This module initializes the bulletproofs sub-package, exposing functions
# for generating and verifying Bulletproofs, as well as creating and
# validating range proofs. It allows seamless switching between different
# implementations (dalek-bulletproofs, fastecdsa, and emulation).
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

from .bulletproofs_core import generate_bulletproof, verify_bulletproof
from .range_proof import create_range_proof, validate_range_proof

# Define what should be accessible when importing from this package
__all__ = [
    "generate_bulletproof",
    "verify_bulletproof",
    "create_range_proof",
    "validate_range_proof"
]
