# helpers.py
# ---------------------------------------------------------------------
# DGT-ZK Protocol: Helper Utilities Module
#
# General-purpose helper functions for data validation and type checks.
# Provides utility functions for common operations, such as hex checks.
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

def is_hex_string(data):
    """
    Checks if the given data is a valid hexadecimal string.

    Parameters:
        data (str): The string to check.

    Returns:
        bool: True if the data is hex; False otherwise.
    """
    try:
        int(data, 16)
        return True
    except ValueError:
        return False

def is_valid_amount(amount):
    """
    Checks if the amount is a valid non-negative integer.

    Parameters:
        amount (int): The amount to validate.

    Returns:
        bool: True if the amount is non-negative; False otherwise.
    """
    return isinstance(amount, int) and amount >= 0
