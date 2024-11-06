# verification_constants.py
# ---------------------------------------------------------------------
# DGT-ZK Protocol: Verification Constants Module
#
# This module defines constants used throughout the verification package
# for the DGT-ZK Protocol. Constants include settings for Private Set
# Intersection (PSI) schemes, paths to databases for blacklists and whitelists,
# compliance check levels, cryptographic configurations, and default
# settings for regulatory checks.
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

# Constants for PSI (Private Set Intersection) Schemes
PSI_PAILLIER = "paillier"    # Homomorphic encryption-based PSI
PSI_SCHNORR = "schnorr"      # Schnorr-based PSI for key exchange

# Cryptographic Constants
DEFAULT_HASH_ALGORITHM = "sha256"    # Default hashing algorithm for integrity checks
KEY_SIZE = 2048                      # Key size for cryptographic operations
DEFAULT_CURVE = "SECP256k1"          # Curve for ECDSA (used in Schnorr and signatures)

# Compliance Check Levels
COMPLIANCE_LEVEL_BASIC = 1           # Basic KYC/AML check
COMPLIANCE_LEVEL_ADVANCED = 2        # Advanced KYC/AML with enhanced verification

# Path Constants for Blacklist and Whitelist Databases
BLACKLIST_DB_PATH = "databases/blacklist_db"     # Path to blacklist database
WHITELIST_DB_PATH = "databases/whitelist_db"     # Path to whitelist database

# Default Timeout and Expiry Settings for Anchored Transactions
DEFAULT_CANCELLATION_WINDOW = 300    # Time in seconds for transaction cancellation

# Bulletproofs Validation Toggle
ENABLE_BULLETPROOF_VALIDATION = True  # Enable Bulletproof range proof validation

# Compliance Validation Flags
ENABLE_KYC_CHECK = True              # Flag to enable KYC checks in compliance verification
ENABLE_AML_CHECK = True              # Flag to enable AML checks in compliance verification

# Default PSI Parameters for Scheme Selection
DEFAULT_PSI_SCHEME = PSI_PAILLIER    # Default PSI scheme (switchable as needed)

# Other Settings
DATA_ENCODING = "utf-8"              # Default encoding for data serialization
REGULATORY_REPORT_PATH = "reports/regulatory_compliance" # Path for storing regulatory reports


# ---------------------------------------------------------------------
# Function Descriptions and Usage Examples
# ---------------------------------------------------------------------

# This module does not contain functions, but rather defines constants
# that are used across the verification package for consistent configuration.
# Below are example usage scenarios in other modules:

# Example 1: Using PSI Scheme Constants
# psi_scheme = verification_constants.DEFAULT_PSI_SCHEME
# if psi_scheme == verification_constants.PSI_SCHNORR:
#     # Implement Schnorr-based PSI operations

# Example 2: Accessing Blacklist Database Path
# blacklist_db_path = verification_constants.BLACKLIST_DB_PATH

# Example 3: Configuring Compliance Level
# compliance_level = verification_constants.COMPLIANCE_LEVEL_ADVANCED
# if compliance_level >= verification_constants.COMPLIANCE_LEVEL_ADVANCED:
#     # Perform additional verification

# Example 4: Using Default Hash Algorithm
# hash_algorithm = verification_constants.DEFAULT_HASH_ALGORITHM
# hashed_value = hash_data("sample_data", algorithm=hash_algorithm)

# Example 5: Regulatory Reporting Path
# report_path = verification_constants.REGULATORY_REPORT_PATH
# save_report(report_data, path=report_path)

# These constants enable centralized configuration, which enhances the flexibility
# and adaptability of the DGT-ZK Protocol’s verification package to meet
# compliance and regulatory standards efficiently.
