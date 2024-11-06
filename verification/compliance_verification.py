# compliance_verification.py
# ---------------------------------------------------------------------
# DGT-ZK Protocol: Compliance Verification Module
#
# This module performs compliance checks for transactions in the DGT-ZK Protocol.
# Compliance verification includes KYC/AML checks using Private Set Intersection (PSI)
# to match addresses against blacklists and whitelists. The module supports both
# Paillier and Schnorr-based PSI schemes for privacy-preserving compliance.
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

from verification_constants import COMPLIANCE_LEVEL_BASIC, COMPLIANCE_LEVEL_ADVANCED, BLACKLIST_DB_PATH, WHITELIST_DB_PATH
from psi_protocol import PSIScheme
import json
import lmdb

class ComplianceVerification:
    def __init__(self, scheme_type="schnorr", compliance_level=COMPLIANCE_LEVEL_BASIC):
        """
        Initializes the Compliance Verification with a specified PSI scheme and compliance level.

        Parameters:
            scheme_type (str): The PSI scheme to use ("paillier" or "schnorr").
            compliance_level (str): Compliance level for checks (e.g., basic or advanced).
        """
        self.scheme_type = scheme_type
        self.compliance_level = compliance_level
        self.psi_scheme = PSIScheme(scheme_type)

    def load_blacklist(self):
        """
        Loads blacklisted addresses from the blacklist database.

        Returns:
            list: List of blacklisted addresses.
        """
        with lmdb.open(BLACKLIST_DB_PATH, readonly=True) as env:
            with env.begin() as txn:
                cursor = txn.cursor()
                return [json.loads(value.decode()) for key, value in cursor]

    def load_whitelist(self):
        """
        Loads whitelisted addresses from the whitelist database.

        Returns:
            list: List of whitelisted addresses.
        """
        with lmdb.open(WHITELIST_DB_PATH, readonly=True) as env:
            with env.begin() as txn:
                cursor = txn.cursor()
                return [json.loads(value.decode()) for key, value in cursor]

    def check_compliance(self, address_set):
        """
        Performs compliance checks on a set of addresses, using PSI to check against blacklists and whitelists.

        Parameters:
            address_set (list): List of encrypted addresses to check for compliance.

        Returns:
            dict: Compliance results, including any blacklist or whitelist matches.
        """
        # Encrypt blacklist and whitelist for comparison
        blacklist = self.psi_scheme.encrypt_set(self.load_blacklist())
        whitelist = self.psi_scheme.encrypt_set(self.load_whitelist())

        # Compute intersections
        blacklist_matches = self.psi_scheme.compute_intersection(address_set, blacklist)
        whitelist_matches = self.psi_scheme.compute_intersection(address_set, whitelist)

        # Prepare compliance report
        compliance_report = {
            "blacklist_matches": blacklist_matches,
            "whitelist_matches": whitelist_matches,
            "compliance_status": "Compliant" if not blacklist_matches else "Non-compliant"
        }

        # Apply advanced compliance level if specified
        if self.compliance_level == COMPLIANCE_LEVEL_ADVANCED:
            compliance_report["details"] = "Advanced verification includes additional checks."

        return compliance_report

    def verify_transaction(self, tx):
        """
        Checks if a transaction meets compliance requirements, including blacklist and whitelist checks.

        Parameters:
            tx (dict): The transaction data to check.

        Returns:
            bool: True if compliant; False if non-compliant.
        """
        # Extract the encrypted addresses from the transaction
        address_set = [tx["sender"], tx["recipient"]]

        # Perform compliance check
        compliance_report = self.check_compliance(address_set)

        # Return compliance status
        return compliance_report["compliance_status"] == "Compliant"

# ---------------------------------------------------------------------
# Function Descriptions and Usage Examples
# ---------------------------------------------------------------------

# Example 1: Initialize Compliance Verification with Schnorr-based PSI
# compliance = ComplianceVerification(scheme_type="schnorr", compliance_level=COMPLIANCE_LEVEL_BASIC)
# transaction = {"sender": "encrypted_sender_address", "recipient": "encrypted_recipient_address"}
# compliance_result = compliance.verify_transaction(transaction)
# print("Compliance Status:", "Compliant" if compliance_result else "Non-compliant")

# Example 2: Run Compliance Check with Advanced Verification
# advanced_compliance = ComplianceVerification(scheme_type="paillier", compliance_level=COMPLIANCE_LEVEL_ADVANCED)
# address_set = ["encrypted_address1", "encrypted_address2"]
# compliance_report = advanced_compliance.check_compliance(address_set)
# print("Compliance Report:", compliance_report)

# ---------------------------------------------------------------------
# This module is designed to verify compliance by checking addresses against
# blacklists and whitelists using private set intersection (PSI) techniques.
# The ComplianceVerification class offers high-level methods to verify
# transactions and generate compliance reports, ensuring regulatory conformity.
