# format_utils.py
# ---------------------------------------------------------------------
# DGT-ZK Protocol: Formatting Utilities Module
#
# Provides functions for data formatting, including JSON and hex
# encoding/decoding, for standardized data handling across modules.
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

import json
import binascii

def to_json(data):
    """
    Converts data to JSON format.

    Parameters:
        data (dict): The data to serialize.

    Returns:
        str: JSON-formatted string.
    """
    return json.dumps(data)

def from_json(json_data):
    """
    Parses a JSON-formatted string to a dictionary.

    Parameters:
        json_data (str): JSON string to deserialize.

    Returns:
        dict: Parsed dictionary from JSON.
    """
    return json.loads(json_data)

def to_hex(data):
    """
    Converts binary data to hexadecimal format.

    Parameters:
        data (bytes): Binary data to convert.

    Returns:
        str: Hexadecimal string.
    """
    return binascii.hexlify(data).decode()
