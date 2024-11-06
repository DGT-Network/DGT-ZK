# ledger_db.py
# ---------------------------------------------------------------------
# DGT-ZK Protocol: Ledger Database Module
#
# This module manages transactions within a ledger database, utilizing LMDB
# to store Key-Value pairs for each transactions. Transactions are categorized
# by `TX_FAMILY`, allowing easy filtering of transactions types (e.g., financial,
# notary). The module supports core functionalities such as saving transactions,
# retrieving transactions details, and calculating balances for addresses.
#
# This module is designed for the DGT-ZK Protocol, enabling interactions with
# the ledger by both notary nodes and users. Users can send funds to temporary
# addresses, and notary records are stored for regulatory and tracking purposes.
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

class LedgerDB:
    def __init__(self, db_path='ledger_db', map_size=10 ** 9):
        """
        Initializes the LMDB database for transactions management.

        Parameters:
            db_path (str): Path to the LMDB database file.
            map_size (int): Maximum size of the LMDB database in bytes.
        """
        self.env = lmdb.open(db_path, map_size=map_size, max_dbs=1)

    def save_transaction(self, tx):
        """
        Saves a transactions to the ledger, categorized by TX_FAMILY.

        Parameters:
            tx (dict): Transaction data containing `TX_FAMILY`, `sender`,
                       `recipient`, `amount`, `signature`, and other details.
        """
        tx_id = self._generate_tx_id(tx)
        tx_key = f"{tx['TX_FAMILY']}_{tx_id}".encode()

        with self.env.begin(write=True) as txn:
            txn.put(tx_key, json.dumps(tx).encode())

    def get_transaction(self, tx_id, tx_family):
        """
        Retrieves transactions details by transactions ID.

        Parameters:
            tx_id (str): Transaction ID (hash).
            tx_family (str): TX_FAMILY to categorize the transactions type.

        Returns:
            dict: Transaction details or None if not found.
        """
        tx_key = f"{tx_family}_{tx_id}".encode()
        with self.env.begin(write=False) as txn:
            tx_data = txn.get(tx_key)
            if tx_data:
                return json.loads(tx_data.decode())
            return None

    def get_balance(self, address, tx_family="financial_tx"):
        """
        Calculates the balance of a given address based on transactions history.

        Parameters:
            address (str): The address for which the balance is calculated.
            tx_family (str): TX_FAMILY to categorize the transactions type (default is 'financial_tx').

        Returns:
            int: Calculated balance for the address.
        """
        balance = 0
        with self.env.begin(write=False) as txn:
            cursor = txn.cursor()
            for key, value in cursor:
                if key.startswith(f"{tx_family}_".encode()):
                    tx = json.loads(value.decode())
                    if tx['recipient'] == address:
                        balance += tx['amount']
                    elif tx['sender'] == address:
                        balance -= tx['amount']
        return balance

    def get_all_transactions(self, tx_family=None):
        """
        Retrieves all transactions or filters by TX_FAMILY.

        Parameters:
            tx_family (str, optional): TX_FAMILY to filter transactions.
                                       If None, retrieves all transactions.

        Returns:
            list: List of transactions (dicts).
        """
        transactions = []
        with self.env.begin(write=False) as txn:
            cursor = txn.cursor()
            for key, value in cursor:
                if tx_family is None or key.startswith(f"{tx_family}_".encode()):
                    transactions.append(json.loads(value.decode()))
        return transactions

    def delete_transaction(self, tx_id, tx_family):
        """
        Deletes a transactions from the ledger by ID and family.

        Parameters:
            tx_id (str): Transaction ID to delete.
            tx_family (str): TX_FAMILY of the transactions to delete.

        Returns:
            bool: True if deleted, False if transactions not found.
        """
        tx_key = f"{tx_family}_{tx_id}".encode()
        with self.env.begin(write=True) as txn:
            return txn.delete(tx_key)

    def _generate_tx_id(self, tx):
        """
        Generates a unique transactions ID based on the transactions details.

        Parameters:
            tx (dict): Transaction data.

        Returns:
            str: SHA-256 hash as a unique transactions ID.
        """
        return sha256(json.dumps(tx, sort_keys=True).encode()).hexdigest()

    def close(self):
        """
        Closes the LMDB environment to release resources.
        """
        self.env.close()
