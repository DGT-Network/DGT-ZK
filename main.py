# main.py
# ---------------------------------------------------------------------
# DGT-ZK Protocol: Main Entry Point
#
# This script serves as the primary entry point for the DGT-ZK Protocol.
# It coordinates core actions such as transaction creation, encryption,
# compliance verification, and anchoring within the protocol.
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

from transactions.transaction_flow import TransactionFlow
from data.export import export_to_csv
from data.ledger_db import LedgerDB
from data.notary_db import NotaryDB
from verification.compliance_verification import ComplianceVerification
from encryption.signature import generate_keys

def main():
    # Initialize core components
    print("Initializing DGT-ZK Protocol...")
    ledger = LedgerDB()
    notary = NotaryDB()
    tx_flow = TransactionFlow()
    compliance = ComplianceVerification(scheme_type="schnorr")

    # Generate keys for a sample transaction
    sender_private_key, sender_public_key = generate_keys()
    recipient_private_key, recipient_public_key = generate_keys()

    # Create a sample transaction
    print("Creating a sample transaction...")
    tx_family = "financial_tx"
    amount = 100
    transaction = tx_flow.create_and_encrypt_transaction(
        tx_family, sender_public_key, recipient_public_key, amount, sender_private_key
    )
    print("Transaction created:", transaction)

    # Compliance check
    print("Performing compliance check...")
    is_compliant = compliance.verify_transaction(transaction)
    print("Compliance status:", "Compliant" if is_compliant else "Non-compliant")

    # Validate and anchor transaction
    print("Validating and anchoring transaction...")
    if tx_flow.validate_and_anchor_transaction(transaction, sender_public_key, notary=True):
        print("Transaction validated and anchored successfully.")
    else:
        print("Transaction validation failed.")

    # Export ledger records for review
    print("Exporting transaction records...")
    export_to_csv(ledger, "ledger_records.csv")
    print("Ledger records exported to ledger_records.csv.")

    # Close database connections
    tx_flow.close()
    ledger.close()
    notary.close()

if __name__ == "__main__":
    main()
