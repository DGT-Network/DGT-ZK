# time_utils.py
# ---------------------------------------------------------------------
# DGT-ZK Protocol: Time Utilities Module
#
# Provides time-related utility functions, such as generating and
# formatting timestamps, for standardized time management across modules.
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

from datetime import datetime, timezone

def current_timestamp():
    """
    Returns the current timestamp in ISO 8601 format (UTC).

    Returns:
        str: ISO 8601 formatted timestamp.
    """
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def timestamp_to_iso(timestamp):
    """
    Converts a Unix timestamp to ISO 8601 format.

    Parameters:
        timestamp (int): Unix timestamp.

    Returns:
        str: ISO 8601 formatted timestamp.
    """
    return datetime.fromtimestamp(timestamp, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
