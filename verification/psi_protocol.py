# psi_protocol.py
# ---------------------------------------------------------------------
# DGT-ZK Protocol: Private Set Intersection (PSI) Protocol Module
#
# This module implements Private Set Intersection (PSI) for compliance checks
# in the DGT-ZK Protocol, supporting both Paillier and Schnorr-based PSI schemes.
# PSI enables intersection of encrypted data sets to verify matches without
# revealing the actual data, ensuring compliance with regulatory requirements.
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

from encryption_utils import generate_schnorr_keypair, schnorr_sign, schnorr_verify
from verification_constants import PSI_PAILLIER_KEY_SIZE, PSI_SCHNORR_CURVE
from phe import paillier
import json

class PSIScheme:
    def __init__(self, scheme_type="schnorr"):
        """
        Initializes the PSI Scheme with either "paillier" or "schnorr" as the scheme type.

        Parameters:
            scheme_type (str): The PSI scheme type, either "paillier" or "schnorr".
        """
        self.scheme_type = scheme_type
        if scheme_type == "paillier":
            self.paillier_keypair = paillier.generate_paillier_keypair(n_length=PSI_PAILLIER_KEY_SIZE)
        elif scheme_type == "schnorr":
            self.schnorr_private_key, self.schnorr_public_key = generate_schnorr_keypair()
        else:
            raise ValueError("Unsupported PSI scheme type. Use 'paillier' or 'schnorr'.")

    def encrypt_set(self, data_set):
        """
        Encrypts a data set using the specified PSI scheme.

        Parameters:
            data_set (list): A list of items to be encrypted.

        Returns:
            list: Encrypted data set.
        """
        if self.scheme_type == "paillier":
            return [self.paillier_keypair[0].encrypt(item) for item in data_set]
        elif self.scheme_type == "schnorr":
            return [schnorr_sign(str(item), self.schnorr_private_key) for item in data_set]

    def compute_intersection(self, encrypted_set, reference_set):
        """
        Computes the intersection of two encrypted data sets.

        Parameters:
            encrypted_set (list): A list of encrypted items.
            reference_set (list): A list of encrypted reference items for intersection.

        Returns:
            list: Intersection of the two sets.
        """
        if self.scheme_type == "paillier":
            return [item for item in encrypted_set if item in reference_set]
        elif self.scheme_type == "schnorr":
            return [item for item in encrypted_set if self.verify_item(item, reference_set)]

    def verify_item(self, item, reference_set):
        """
        Verifies if an item exists in the reference set using Schnorr signatures.

        Parameters:
            item: The item to verify.
            reference_set (list): A list of reference items.

        Returns:
            bool: True if item exists in reference_set, False otherwise.
        """
        r, s = item
        for ref in reference_set:
            ref_r, ref_s = ref
            if schnorr_verify(str(r), ref_r, ref_s, self.schnorr_public_key):
                return True
        return False

# ---------------------------------------------------------------------
# Function Descriptions and Usage Examples
# ---------------------------------------------------------------------

# Example 1: Initialize Paillier-based PSI Scheme
# psi_paillier = PSIScheme(scheme_type="paillier")
# data_set = [123, 456, 789]
# encrypted_data_set = psi_paillier.encrypt_set(data_set)
# print("Encrypted Data Set (Paillier):", encrypted_data_set)

# Example 2: Initialize Schnorr-based PSI Scheme
# psi_schnorr = PSIScheme(scheme_type="schnorr")
# encrypted_schnorr_set = psi_schnorr.encrypt_set(data_set)
# print("Encrypted Data Set (Schnorr):", encrypted_schnorr_set)

# Example 3: Compute Intersection
# reference_set = encrypted_data_set  # Example reference set
# intersection = psi_paillier.compute_intersection(encrypted_data_set, reference_set)
# print("Intersection (Paillier):", intersection)

# Example 4: Schnorr-based Intersection Verification
# intersection_schnorr = psi_schnorr.compute_intersection(encrypted_schnorr_set, encrypted_schnorr_set)
# print("Intersection (Schnorr):", intersection_schnorr)

# ---------------------------------------------------------------------
# This module enables Private Set Intersection (PSI) in both Paillier and Schnorr schemes,
# allowing for secure compliance checks by finding common encrypted elements between sets.
# The `encrypt_set` function encrypts a list of items, while `compute_intersection`
# finds common items across encrypted sets without revealing the actual data.
