# export.py
# ---------------------------------------------------------------------
# DGT-ZK Protocol: Data Export Module
#
# This module provides functions to export records from the LMDB database
# to CSV format, facilitating easier inspection, analysis, and testing
# of stored transactions and notary entries without requiring a blockchain
# network. The module supports exporting all records or filtering records
# by transactions family (TX_FAMILY).
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

import csv
import json
from lmdb import Environment


def export_to_csv(database: Environment, file_path: str):
    """
    Exports all records from the specified LMDB database to a CSV file.

    Parameters:
        database (Environment): The LMDB database environment from which records are exported.
        file_path (str): Path to the CSV file where data will be exported.
    """
    with open(file_path, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Key", "Data"])  # CSV header

        with database.begin(write=False) as txn:
            cursor = txn.cursor()
            for key, value in cursor:
                record_key = key.decode('utf-8')
                record_data = json.loads(value.decode('utf-8'))
                writer.writerow([record_key, json.dumps(record_data)])

    print(f"All records exported to {file_path}")


def export_filtered_to_csv(database: Environment, tx_family: str, file_path: str):
    """
    Exports only records of a specific TX_FAMILY from the specified LMDB database to a CSV file.

    Parameters:
        database (Environment): The LMDB database environment from which records are exported.
        tx_family (str): The transactions family or type (e.g., 'financial_tx', 'notary_tx') for filtering.
        file_path (str): Path to the CSV file where filtered data will be exported.
    """
    with open(file_path, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Key", "Data"])  # CSV header

        with database.begin(write=False) as txn:
            cursor = txn.cursor()
            for key, value in cursor:
                record_key = key.decode('utf-8')
                if record_key.startswith(f"{tx_family}_"):
                    record_data = json.loads(value.decode('utf-8'))
                    writer.writerow([record_key, json.dumps(record_data)])

    print(f"Filtered records of '{tx_family}' exported to {file_path}")
