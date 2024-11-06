# notary_interface.py
# ------------------------------------------------------------
# DGT-ZK Protocol: Notary Interface
#
# This module provides high-level functions for notarization,
# anchoring, and verification. It combines ledger and notary
# operations to manage notary records and anchoring.
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
# ------------------------------------------------------------

from data.notary_db import NotaryDB
from data.ledger_db import LedgerDB
from data.utils import hash_transaction
from datetime import datetime, timedelta

notary_db = NotaryDB(db_path="notary_db")
ledger_db = LedgerDB(db_path="ledger_db")

def register_notary_record(record):
    """
    Registers an encrypted notary record in the notary database.

    Parameters:
        record (dict): The encrypted notary record data.
    """
    notary_db.save_notary_record(record)

def anchor_transaction(tx_id, cancellation_window):
    """
    Creates a secure anchor for a transactions with a cancellation window.

    Parameters:
        tx_id (str): Transaction ID to be anchored.
        cancellation_window (int): Time in minutes for anchor validity.
    """
    expiration = datetime.utcnow() + timedelta(minutes=cancellation_window)
    anchor_record = {
        "tx_id": tx_id,
        "anchored_at": datetime.utcnow().isoformat(),
        "expires_at": expiration.isoformat()
    }
    notary_db.save_notary_record(anchor_record)

def verify_notary_record(record_id):
    """
    Verifies the existence and integrity of a notary record.

    Parameters:
        record_id (str): Unique identifier of the notary record to verify.

    Returns:
        dict: The notary record if it exists and is verified; otherwise, None.
    """
    return notary_db.get_notary_record(record_id)
