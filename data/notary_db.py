# notary_db.py
# ---------------------------------------------------------------------
# DGT-ZK Protocol: Notary Database Module
#
# This module emulates a notary system by securely storing encrypted
# records in a separate LMDB database. It enables notary operations
# within the DGT-ZK Protocol by providing functions to store notarized
# data, retrieve records by ID, list all notary entries, and delete records
# for verification or testing purposes.
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

import lmdb
import json
from hashlib import sha256
from datetime import datetime


class NotaryDB:
    def __init__(self, db_path='notary_db', map_size=10 ** 9):
        """
        Initializes the LMDB database for notary records management.

        Parameters:
            db_path (str): Path to the LMDB database file.
            map_size (int): Maximum size of the LMDB database in bytes.
        """
        self.env = lmdb.open(db_path, map_size=map_size, max_dbs=1)

    def save_notary_record(self, content, signature, expiration_minutes=0):
        """
        Stores an encrypted notary record in the database, with optional
        expiration information.

        Parameters:
            content (str): The notary record content to be stored.
            signature (str): Digital signature for the notary record.
            expiration_minutes (int): Optional expiration time in minutes. If set,
                                      the record will have an expiry timestamp.

        Returns:
            str: Record ID generated for the stored notary record.
        """
        # Generate unique record ID
        record_data = {
            "content": content,
            "signature": signature,
            "timestamp": datetime.utcnow().isoformat(),
        }

        if expiration_minutes > 0:
            expiration_time = datetime.utcnow() + timedelta(minutes=expiration_minutes)
            record_data["expires_at"] = expiration_time.isoformat()

        record_id = sha256(json.dumps(record_data, sort_keys=True).encode()).hexdigest()
        record_key = f"notary_{record_id}".encode()

        with self.env.begin(write=True) as txn:
            txn.put(record_key, json.dumps(record_data).encode())

        return record_id

    def get_notary_record(self, record_id):
        """
        Retrieves a specific notary record by its ID and checks expiration.

        Parameters:
            record_id (str): Unique record ID (hash).

        Returns:
            dict: Notary record details or None if not found or expired.
        """
        record_key = f"notary_{record_id}".encode()
        with self.env.begin(write=False) as txn:
            record_data = txn.get(record_key)
            if record_data:
                record = json.loads(record_data.decode())
                if "expires_at" in record:
                    expiration_time = datetime.fromisoformat(record["expires_at"])
                    if datetime.utcnow() > expiration_time:
                        self.delete_notary_record(record_id)
                        return None
                return record
            return None

    def list_notary_records(self, include_expired=False):
        """
        Lists all stored notary records for verification or testing,
        optionally filtering out expired records.

        Parameters:
            include_expired (bool): If True, includes expired records.

        Returns:
            list[dict]: A list of all valid notary records in the database.
        """
        records = []
        with self.env.begin(write=False) as txn:
            cursor = txn.cursor()
            for key, value in cursor:
                if key.startswith(b"notary_"):
                    record = json.loads(value.decode())
                    if "expires_at" in record and not include_expired:
                        expiration_time = datetime.fromisoformat(record["expires_at"])
                        if datetime.utcnow() > expiration_time:
                            continue
                    records.append(record)
        return records

    def delete_notary_record(self, record_id):
        """
        Deletes a specific notary record by its ID.

        Parameters:
            record_id (str): Unique record ID to delete.

        Returns:
            bool: True if the record was deleted, False if not found.
        """
        record_key = f"notary_{record_id}".encode()
        with self.env.begin(write=True) as txn:
            return txn.delete(record_key)

    def close(self):
        """
        Closes the LMDB environment to release resources.
        """
        self.env.close()
